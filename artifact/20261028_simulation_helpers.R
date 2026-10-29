# Source from the manuscript root. See 20261028_simulation_pipeline.md for usage.
# Requires GeneralDualSimplex. Does not change scaling, fitting, or evaluation.

save_projected_truth <- function(dso, ground_truth,
                                 dims = seq_len(nrow(ground_truth$H))) {
  W <- ground_truth$W[colnames(dso@projection$Phi), , drop = FALSE]
  H <- ground_truth$H[, colnames(dso@projection$Psi), drop = FALSE]

  # Normalize the true profiles using THIS run's fitted scaling weights.
  W_tilde <- sweep(W, 1L, dso@scaling$r, "*")
  W_tilde <- sweep(W_tilde, 2L, colSums(W_tilde), "/")
  H_tilde <- sweep(H, 2L, dso@scaling$c, "*")
  H_tilde <- sweep(H_tilde, 1L, rowSums(H_tilde), "/")

  dso@misc$true_vertices <- list(
    Omega = dso@projection$Phi[dims, , drop = FALSE] %*% W_tilde,
    X = H_tilde %*% t(dso@projection$Psi[dims, , drop = FALSE]),
    dims = dims,
    scaling_id = dso@scaling$id,
    projection_id = dso@projection$id
  )
  dso
}

# Use keep_history = FALSE only for final analysis objects: trajectories and
# warm starts are then unavailable. Factors, evaluation, and raw endpoints stay.
pack_simulation_dso <- function(dso, keep_history = TRUE, compact_data = FALSE) {
  state <- stats::setNames(
    lapply(methods::slotNames(dso), function(name) methods::slot(dso, name)),
    methods::slotNames(dso)
  )

  # R6 methods carry environments into RDS. Store only constructor inputs;
  # unpack_simulation_dso restores the public classes from the installed package.
  if (!is.null(dso@scaling)) {
    fields <- c("r", "c", "a", "b", "type", "params", "sinkhorn", "parent")
    state$scaling <- stats::setNames(
      lapply(fields, function(name) dso@scaling[[name]]), fields
    )
  }
  if (!is.null(dso@projection)) {
    fields <- c("Phi", "sigma", "Psi", "a", "b", "k", "method", "seed", "parent")
    state$projection <- stats::setNames(
      lapply(fields, function(name) dso@projection[[name]]), fields
    )
  }

  if (compact_data) state$data <- pack_observed_matrix(state$data)

  if (!keep_history && !is.null(state$optimization)) {
    state$optimization@history <- state$optimization@history[FALSE, , drop = FALSE]
    for (name in c("history", "X_tilde_history", "Q_history")) {
      state$optimization@raw[[name]] <- NULL
    }
    state$misc$storage$history_removed <- TRUE
  }

  list(
    package_version = as.character(utils::packageVersion("GeneralDualSimplex")),
    state = state
  )
}

unpack_simulation_dso <- function(packed) {
  state <- packed$state
  if (is.list(state$data) && identical(state$data$format, "matrix-values-v1")) {
    state$data <- unpack_observed_matrix(state$data)
  }
  if (!is.null(state$scaling)) {
    state$scaling <- do.call(GeneralDualSimplex::DSScaling$new, state$scaling)
  }
  if (!is.null(state$projection)) {
    state$projection <- do.call(GeneralDualSimplex::DSProjection$new, state$projection)
  }
  do.call(methods::new, c(list(Class = "DualSimplexObject"), state))
}

# These archive a base data.frame and replace only its result list-column.
save_simulation_rds <- function(experiments, file, compress = "xz",
                                keep_history = TRUE, compact_data = FALSE) {
  saved <- as.data.frame(experiments)
  saved[["result"]] <- lapply(saved[["result"]], pack_simulation_dso,
                            keep_history = keep_history, compact_data = compact_data)
  saveRDS(saved, file, compress = compress, version = 3)
  invisible(file)
}

read_simulation_rds <- function(file) {
  saved <- readRDS(file)
  saved[["result"]] <- lapply(saved[["result"]], unpack_simulation_dso)
  saved
}

# Store counts as 1/2/4-byte integers; shuffle the eight bytes of other doubles.
# Matrix class, slots and double values are restored before constructing the DSO.
pack_observed_matrix <- function(data) {
  if (!methods::is(data, "dMatrix")) return(data)
  slots <- stats::setNames(
    lapply(methods::slotNames(data), function(name) methods::slot(data, name)),
    methods::slotNames(data)
  )
  x <- slots$x
  counts <- all(is.finite(x)) &&
    all(x >= 0 & x <= .Machine$integer.max & x == trunc(x))
  width <- 8L
  negative_zero <- integer()
  if (counts) {
    width <- if (all(x <= 255)) 1L else if (all(x <= 65535)) 2L else 4L
    slots$x <- writeBin(as.integer(x), raw(), size = width, endian = "little")
    negative_zero <- which(x == 0 & 1 / x < 0)
  } else {
    slots$x <- as.vector(t(matrix(
      writeBin(x, raw(), size = 8L, endian = "little"), nrow = 8L
    )))
  }
  list(format = "matrix-values-v1", class = class(data), slots = slots,
       counts = counts, width = width, negative_zero = negative_zero,
       x_attributes = attributes(x))
}

unpack_observed_matrix <- function(encoded) {
  if (encoded$counts) {
    x <- as.double(readBin(encoded$slots$x, integer(),
                          n = length(encoded$slots$x) / encoded$width,
                          size = encoded$width, signed = encoded$width == 4L,
                          endian = "little"))
    x[encoded$negative_zero] <- -0
  } else {
    bytes <- as.vector(t(matrix(encoded$slots$x, ncol = 8L)))
    x <- readBin(bytes, double(), n = length(bytes) / 8L,
                 size = 8L, endian = "little")
  }
  attributes(x) <- encoded$x_attributes
  encoded$slots$x <- x
  do.call(methods::new, c(list(Class = encoded$class), encoded$slots))
}

# Add simplex edges to an existing GSVD DualPlot, using the same plotted dims.
# vertices is the list saved by save_projected_truth(): X and Omega matrices.
add_true_vertices <- function(plot, vertices, dims = 2:3, colour = "black",
                              linetype = "dashed", linewidth = 0.4) {
  dims <- paste0("dim", dims)
  edge_layer <- function(coordinates) {
    pairs <- utils::combn(seq_len(nrow(coordinates)), 2L)
    edges <- data.frame(
      x = coordinates[pairs[1L, ], 1L],
      y = coordinates[pairs[1L, ], 2L],
      xend = coordinates[pairs[2L, ], 1L],
      yend = coordinates[pairs[2L, ], 2L]
    )
    ggplot2::geom_segment(
      data = edges, ggplot2::aes(x = x, y = y, xend = xend, yend = yend),
      inherit.aes = FALSE, show.legend = FALSE,
      colour = colour, linetype = linetype, linewidth = linewidth
    )
  }

  # DualPlot puts features (Psi) on the left and samples (Phi) on the right.
  plot[[1L]] <- plot[[1L]] + edge_layer(vertices$X[, dims, drop = FALSE])
  plot[[2L]] <- plot[[2L]] + edge_layer(t(vertices$Omega[dims, , drop = FALSE]))
  plot
}
