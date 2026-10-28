# Checks for 20261028_noise_grid.R. Run from the manuscript root:
#   Rscript artifact/20261028_noise_grid_validation.R
# The Monte Carlo part needs GeneralDualSimplex 0.29.0; the renv has 0.28.0,
# so a scratch library built from the package commit is put first on the path.
.libPaths(c("out/20261028_marginal_check/lib", .libPaths()))
library(GeneralDualSimplex)
source("artifact/20261028_noise_grid.R")
options(width = 200)
cat("GeneralDualSimplex", as.character(packageVersion("GeneralDualSimplex")), "\n")

base <- readRDS("/data/simulation_ground_truth_k3.rds")
setup <- function(fold, seeds = 1:30) base$simulation[base$MARKER_FOLD == fold & base$SEED %in% seeds]

cat("\n== 1. K = 3, fold 5, seeds 1-10 (the pilot base) ==\n")
grid <- find_grid_points(setup(5, 1:10))
str(unclass(grid)[1:4])
print(attr(grid, "moments"))
print(signif(attr(grid, "details"), 4), row.names = FALSE)
details <- attr(grid, "details")
cat("max |implied / target - 1|, Poisson, Normal, Mul:",
    signif(sapply(details[c("poisson", "normal", "mul")], function(v) max(abs(v / details$target - 1))), 3), "\n")

cat("\n== 2. Each marker fold, all 30 seeds ==\n")
for (fold in c(2, 5, 10, 100)) {
  g <- find_grid_points(setup(fold))
  cat(sprintf("fold %3d  mean_mu %.2f  mean_mu2 %.0f\n", fold, attr(g, "moments")[1], attr(g, "moments")[2]))
  cat("  fraction :", g$fraction, "\n  normal_sd:", g$normal_sd, "\n  mul_sd   :", g$mul_sd, "\n")
}

cat("\n== 3. Monte Carlo: mean (Observed / scale - V*)^2, one draw, fold 5 seed 1 ==\n")
sim <- setup(5, 1)[[1]]
V_star <- sim$W %*% sim$H
expected <- noise_variance(signal_moments(list(sim)), grid$fraction, grid$normal_sd, grid$mul_sd, grid$dispersion)
mse <- function(observed, scale) mean((observed / scale - V_star)^2)
set.seed(1)
measured <- t(sapply(seq_along(grid$fraction), function(i) c(
  poisson = mse(ApplyNBNoise(sim, dispersion = 0, library_size_fraction = grid$fraction[i])$Observed, grid$fraction[i]),
  normal = mse(V_star + rnorm(length(V_star), sd = grid$normal_sd[i]), 1),
  normal_clipped = mse(ApplyNormalNoise(sim, sd = grid$normal_sd[i])$Observed, 1),
  mul = mse(ApplyMultiplicativeNoise(sim, sd = grid$mul_sd[i])$Observed, exp(grid$mul_sd[i]^2 / 2)),
  sapply(grid$dispersion, function(phi) mse(ApplyNBNoise(sim, dispersion = phi,
    library_size_fraction = grid$fraction[i])$Observed, grid$fraction[i]))
)))
colnames(measured)[5:6] <- paste0("nb_", grid$dispersion)
expected <- cbind(expected, normal_clipped = clipped_normal_mse(list(sim), grid$normal_sd))[, colnames(measured)]
cat("measured / expected - 1:\n")
print(signif(measured / expected - 1, 2))
