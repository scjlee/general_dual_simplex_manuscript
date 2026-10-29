# Illustrative storage checks, not a run of the user's full experiment grid.
# Run from the manuscript root; optional first argument: temporary package library.
args <- commandArgs(TRUE)
if (length(args)) .libPaths(c(args[1L], .libPaths()))
library(GeneralDualSimplex)
source("artifact/20261028_simulation_helpers.R")
out <- "out/20261028_storage_validation"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
same <- function(x, y) stopifnot(identical(x, y))

# Width boundaries, signed zero, fractional/negative data, non-finite values,
# large exact integers, and values at the limits of the double range.
values <- list(
  c(0, -0, 1, 255), c(0, -0, 256, 65535),
  c(0, -0, 65536, .Machine$integer.max),
  c(0, -0, 1.25, NA_real_, NaN, Inf, -Inf,
    .Machine$double.xmin, .Machine$double.xmax),
  c(2147483648, 2^53), c(-2, -1, 0, 1)
)
for (x in values) {
  d <- CreateDSO(matrix(x, ncol = 1))
  m <- unpack_observed_matrix(unserialize(serialize(pack_observed_matrix(d@data), NULL)))
  same(serialize(d@data, NULL), serialize(m, NULL))
  same(d@data_id, rlang::hash(m))
}

set.seed(7)
matrices <- list(
  methods::as(Matrix::rsparsematrix(40, 25, 0.2), "generalMatrix"),
  methods::as(Matrix::Matrix(0, 10, 8, sparse = TRUE), "generalMatrix"),
  methods::as(Matrix::Matrix(matrix(c(0, -0, 1, 255), 2), sparse = TRUE), "generalMatrix")
)
for (m in matrices) {
  restored <- unpack_observed_matrix(unserialize(serialize(pack_observed_matrix(m), NULL)))
  same(serialize(m, NULL), serialize(restored, NULL))
  same(rlang::hash(m), rlang::hash(restored))
  stopifnot(methods::validObject(restored))
}

# Named x slots retain their attributes too.
m <- CreateDSO(matrix(1:6, 2))@data
names(m@x) <- letters[1:6]
same(serialize(m, NULL), serialize(unpack_observed_matrix(pack_observed_matrix(m)), NULL))

# Full-object checks reuse the earlier accepted fixture and metrics.
fixture <- readRDS("out/20261028_simulation_validation/full_gzip.rds")
for (d in fixture$result) {
  restored <- unpack_simulation_dso(unserialize(serialize(
    pack_simulation_dso(d, keep_history = FALSE, compact_data = TRUE), NULL
  )))
  same(serialize(d@data, NULL), serialize(restored@data, NULL))
  same(d@data_id, rlang::hash(restored@data))
  same(GetData(d, "scaled"), GetData(restored, "scaled"))
  same(GetFactors(d, "deconvolution"), GetFactors(restored, "deconvolution"))
  same(GetBaryCoord(d), GetBaryCoord(restored))
  same(Lineage(d), Lineage(restored))
  same(d@misc, restored@misc[setdiff(names(restored@misc), "storage")])
  stopifnot(methods::validObject(restored), nrow(restored@optimization@history) == 0L)
  original <- pack_simulation_dso(d, keep_history = FALSE)
  same(original, pack_simulation_dso(restored, keep_history = FALSE))
}
# The new reader still handles old archives with the original Matrix storage.
old <- read_simulation_rds("out/20261028_simulation_validation/packed_xz.rds")
same(lapply(old$result, pack_simulation_dso), lapply(fixture$result, pack_simulation_dso))

# A reader that only sources the helper must also work before Matrix is loaded.
save_simulation_rds(fixture[1, ], file.path(out, "fresh_session.rds"),
                    compress = "gzip", keep_history = FALSE, compact_data = TRUE)
saveRDS(serialize(fixture$result[[1]]@data, NULL),
         file.path(out, "expected_matrix_bytes.rds"))
reader_script <- file.path(out, "fresh_reader.R")
writeLines(c(
  paste0(".libPaths(", paste(capture.output(dput(.libPaths())), collapse = "\n"), ")"),
  'source("artifact/20261028_simulation_helpers.R")',
  'stopifnot(!"Matrix" %in% loadedNamespaces())',
  'x <- read_simulation_rds("out/20261028_storage_validation/fresh_session.rds")',
  'expected <- readRDS("out/20261028_storage_validation/expected_matrix_bytes.rds")',
  'stopifnot(identical(serialize(x$result[[1]]@data, NULL), expected))',
  'stopifnot(methods::validObject(x$result[[1]]))',
  'cat("Fresh-session reader passed.\\n")'
), reader_script)
status <- system2(file.path(R.home("bin"), "Rscript"),
                  c("--vanilla", shQuote(reader_script)),
                  stdout = file.path(out, "fresh_reader.log"),
                  stderr = file.path(out, "fresh_reader.log"))
stopifnot(status == 0L)

# Representative dimensions are taken from the user's reported 3000 x 500 input.
set.seed(53)
sim <- GenerateMixture(3000, 500, 3, n_marker = 20, marker_fold = 5,
                       profile_spread_sd = 0.2)
observations <- list(
  none = sim$W %*% sim$H,
  Poisson = ApplyNBNoise(sim, dispersion = 0, library_size_fraction = 0.08)$Observed,
  Mul = ApplyMultiplicativeNoise(sim, sd = 0.25)$Observed,
  Normal = ApplyNormalNoise(sim, sd = 3)$Observed
)
measurements <- list()
for (noise in names(observations)) {
  d <- CreateDSO(observations[[noise]]) |>
    CalculateMatrixStats(stats = c("total", "var", "sd")) |>
    ScaleDSO("expression") |> FindProjection(k = 4, method = "svd") |>
    FindSolution(k = 3, solver = "positivity", init = "random", seed = 1L,
                 step_init = 0.1, max_iter = 200) |>
    RunReduction(gsvd_dims = 1:3)
  d <- save_projected_truth(d, sim)
  d@misc$evaluation <- EvaluateBenchmark(d, sim)
  experiment <- data.frame(noise = noise)
  experiment$result <- list(d)
  before <- serialize(pack_simulation_dso(d, keep_history = FALSE), NULL)

  for (compress in c("gzip", "zstd")) {
    for (compact in c(FALSE, TRUE)) {
      file <- file.path(out, paste(noise, compress, compact, "rds", sep = "."))
      elapsed <- system.time(save_simulation_rds(
        experiment, file, compress = compress, keep_history = FALSE,
        compact_data = compact
      ))[["elapsed"]]
      restored <- read_simulation_rds(file)$result[[1]]
      same(before, serialize(pack_simulation_dso(restored, keep_history = FALSE), NULL))
      same(before, serialize(pack_simulation_dso(d, keep_history = FALSE), NULL))
      same(EvaluateBenchmark(d, sim), EvaluateBenchmark(restored, sim))
      same(d@data_id, rlang::hash(restored@data))
      row <- data.frame(noise, compress, compact_data = compact,
                        bytes = file.info(file)$size, write_seconds = elapsed)
      measurements[[length(measurements) + 1L]] <- row
      print(row, row.names = FALSE)
      # Files are temporary products of this test; the CSV retains their sizes.
      unlink(file)
    }
  }
}
measurements <- do.call(rbind, measurements)
write.csv(measurements, file.path(out, "measurements.csv"), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
cat("All storage checks passed: exact values, bytes, hashes, full DSO state,\n",
    "evaluation, original-object preservation and old-archive reading.\n")
