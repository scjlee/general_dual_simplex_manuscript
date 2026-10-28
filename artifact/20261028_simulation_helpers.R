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
pack_simulation_dso <- function(dso, keep_history = TRUE) {
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
                                keep_history = TRUE) {
  saved <- as.data.frame(experiments)
  saved[["result"]] <- lapply(saved[["result"]], pack_simulation_dso,
                            keep_history = keep_history)
  saveRDS(saved, file, compress = compress, version = 3)
  invisible(file)
}

read_simulation_rds <- function(file) {
  saved <- readRDS(file)
  saved[["result"]] <- lapply(saved[["result"]], unpack_simulation_dso)
  saved
}
