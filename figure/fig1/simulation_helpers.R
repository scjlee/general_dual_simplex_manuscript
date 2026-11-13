# Unchanged reader functions from artifact/20261028_simulation_helpers.R.

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

read_simulation_rds <- function(file) {
  saved <- readRDS(file)
  saved[["result"]] <- lapply(saved[["result"]], unpack_simulation_dso)
  saved
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
