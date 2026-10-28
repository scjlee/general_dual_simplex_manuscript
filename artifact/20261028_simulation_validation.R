# Illustrative verification, not a run of the user's missing ground-truth grid.
# Run from the manuscript root. Optional first argument: temporary package library.
args <- commandArgs(TRUE)
if (length(args)) .libPaths(c(args[1L], .libPaths()))
library(GeneralDualSimplex)
source("artifact/20261028_simulation_helpers.R")
dir.create("out/20261028_simulation_validation", recursive = TRUE, showWarnings = FALSE)
out <- "out/20261028_simulation_validation"
cat("package", as.character(packageVersion("GeneralDualSimplex")), "\n")

set.seed(53)
sim <- GenerateMixture(180, 70, 3, n_marker = 6, marker_fold = 5,
                       profile_spread_sd = 0.2)
observations <- list(
  none = sim$W %*% sim$H,
  Poisson = ApplyNBNoise(sim, dispersion = 0, library_size_fraction = 0.08)$Observed,
  Mul = ApplyMultiplicativeNoise(sim, sd = 0.25)$Observed,
  Normal = ApplyNormalNoise(sim, sd = 3)$Observed
)

same <- function(x, y) stopifnot(identical(x, y))
near <- function(x, y) stopifnot(max(abs(x - y)) < 1e-10)
results <- list()
checks <- list()
for (noise in names(observations)) {
  for (marginal in c("expression", "uniform")) {
    d <- CreateDSO(observations[[noise]]) |>
      CalculateMatrixStats(stats = c("total", "var", "sd")) |>
      ScaleDSO(type = marginal) |>
      FindProjection(k = 20, method = "svd") |>
      FindSolution(k = 3, init = "random", solver = "positivity", step_init = 0.1) |>
      RunReduction(gsvd_dims = 1:3)
    d@misc$evaluation <- EvaluateBenchmark(d, sim)
    d <- save_projected_truth(d, sim)

    # Independent expressions for direct application of the two projection maps.
    W0 <- diag(d@scaling$r) %*% sim$W
    W0 <- W0 %*% diag(1 / colSums(W0))
    H0 <- sim$H %*% diag(d@scaling$c)
    H0 <- diag(1 / rowSums(H0)) %*% H0
    near(d@misc$true_vertices$Omega, d@projection$Phi[1:3, ] %*% W0)
    near(d@misc$true_vertices$X, H0 %*% t(d@projection$Psi[1:3, ]))
    near(d@misc$true_vertices$Omega[1, ], rep(1, 3))
    near(d@misc$true_vertices$X[, 1], rep(1, 3))
    if (noise == "none") {
      true_mass <- as.vector(crossprod(d@scaling$r, sim$W)) *
        as.vector(sim$H %*% d@scaling$c)
      near(d@misc$true_vertices$Omega %*% diag(true_mass) %*%
             d@misc$true_vertices$X, diag(d@projection$sigma[1:3]))
    }

    # Pure profiles and arbitrary convex combinations must use the same map.
    B <- matrix(seq_len(15), 3, 5)
    B <- sweep(B, 2, colSums(B), "/")
    near(d@projection$Phi[1:3, ] %*% (W0 %*% B),
         d@misc$true_vertices$Omega %*% B)
    near((t(B) %*% H0) %*% t(d@projection$Psi[1:3, ]),
         t(B) %*% d@misc$true_vertices$X)

    packed <- pack_simulation_dso(d)
    restored <- unpack_simulation_dso(unserialize(serialize(packed, NULL)))
    stopifnot(methods::validObject(restored))
    same(pack_simulation_dso(restored), packed)
    same(d@scaling$id, restored@scaling$id)
    same(d@projection$id, restored@projection$id)
    same(GetData(d, "scaled"), GetData(restored, "scaled"))
    same(GetFactors(d, "deconvolution"), GetFactors(restored, "deconvolution"))
    same(GetTrajectory(d), GetTrajectory(restored))
    same(GetBaryCoord(d), GetBaryCoord(restored))
    same(Lineage(d), Lineage(restored))
    same(EvaluateBenchmark(d, sim), EvaluateBenchmark(restored, sim))

    # K+1 dimensions suffice for this fit and its spectral-ratio diagnostic.
    smaller <- FindProjection(GetData(d, "scaled"), k = 4, method = "svd",
                               parent = d@scaling$id)
    same(smaller$sigma, d@projection$sigma[1:4])
    same(smaller$Phi[1:3, ], d@projection$Phi[1:3, ])
    same(smaller$Psi[1:3, ], d@projection$Psi[1:3, ])

    before <- serialize(packed, NULL)
    trimmed <- unpack_simulation_dso(pack_simulation_dso(d, keep_history = FALSE))
    same(serialize(pack_simulation_dso(d), NULL), before)
    same(GetFactors(d, "deconvolution"), GetFactors(trimmed, "deconvolution"))
    same(GetBaryCoord(d), GetBaryCoord(trimmed))
    same(d@misc$true_vertices, trimmed@misc$true_vertices)
    stopifnot(nrow(trimmed@optimization@history) == 0L,
              is.null(trimmed@optimization@raw$X_tilde_history),
              is.null(trimmed@optimization@raw$history))

    id <- paste(noise, marginal, sep = "_")
    results[[id]] <- d
    checks[[id]] <- data.frame(noise, marginal,
                               iterations = d@optimization@iterations,
                               outcome = d@optimization@outcome)
  }
}

# Reorder and subset the data axes, while passing the original, complete truth.
d <- CreateDSO(observations$Poisson[180:50, 70:15]) |>
  ScaleDSO("uniform") |> FindProjection(5, method = "svd")
d <- save_projected_truth(d, sim, dims = 1:5)
aligned <- list(W = sim$W[colnames(d@projection$Phi), , drop = FALSE],
                H = sim$H[, colnames(d@projection$Psi), drop = FALSE])
same(d@misc$true_vertices, save_projected_truth(d, aligned, dims = 1:5)@misc$true_vertices)
stopifnot(identical(dim(d@misc$true_vertices$Omega), c(5L, 3L)),
          identical(dim(d@misc$true_vertices$X), c(3L, 5L)))

# Other solver endpoints have different raw histories; the optional trim covers both.
for (solver in c("qp", "alignment")) {
  d <- CreateDSO(observations$Poisson) |> ScaleDSO("expression") |>
    FindProjection(4, method = "svd") |>
    FindSolution(k = 3, solver = solver, max_iter = 5)
  same(GetTrajectory(d), GetTrajectory(unpack_simulation_dso(pack_simulation_dso(d))))
  restored <- unpack_simulation_dso(pack_simulation_dso(d, keep_history = FALSE))
  same(GetFactors(d), GetFactors(restored))
  stopifnot(nrow(restored@optimization@history) == 0L)
}

experiments <- data.frame(run = names(results))
experiments$result <- unname(results)
before <- serialize(lapply(experiments$result, pack_simulation_dso), NULL)
measurements <- list()
for (format in c("full_gzip", "full_xz", "packed_xz", "packed_trimmed_xz")) {
  path <- file.path(out, paste0(format, ".rds"))
  elapsed <- system.time({
    if (format == "full_gzip") saveRDS(experiments, path, compress = "gzip")
    if (format == "full_xz") saveRDS(experiments, path, compress = "xz")
    if (format == "packed_xz") save_simulation_rds(experiments, path)
    if (format == "packed_trimmed_xz") {
      save_simulation_rds(experiments, path, keep_history = FALSE)
    }
  })[["elapsed"]]
  measurements[[format]] <- data.frame(format, bytes = file.info(path)$size,
                                       write_seconds = elapsed)
}
same(serialize(lapply(experiments$result, pack_simulation_dso), NULL), before)
restored <- read_simulation_rds(file.path(out, "packed_xz.rds"))
same(restored$run, experiments$run)
same(lapply(restored$result, pack_simulation_dso),
     lapply(experiments$result, pack_simulation_dso))

# A repeated reference to one R6 object must not become a mutable shared instance.
shared <- experiments[rep(1L, 2L), ]
path <- file.path(out, "shared.rds")
save_simulation_rds(shared, path)
restored <- read_simulation_rds(path)
stopifnot(!identical(restored$result[[1]]@projection, restored$result[[2]]@projection))

measurements <- do.call(rbind, measurements)
rownames(measurements) <- NULL
write.csv(measurements, file.path(out, "size_measurements.csv"), row.names = FALSE)
write.csv(do.call(rbind, checks), file.path(out, "fixture_runs.csv"), row.names = FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
print(measurements, row.names = FALSE)
cat("All focused checks passed. Fixture outcomes are not scientific results.\n")
