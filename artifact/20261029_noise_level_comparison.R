# Run from the manuscript root in its renv. Uses base R and the existing helper.
# This compares proposed calibration conventions; it does not change the helper.
source("artifact/20261028_noise_grid.R")
output <- "out/20261029_noise_level_comparison"
dir.create(output, recursive = TRUE, showWarnings = FALSE)
base <- readRDS("/data/simulation_ground_truth_k3.rds")

moments <- do.call(rbind, lapply(seq_len(nrow(base)), function(i) {
  mu <- base$simulation[[i]]$W %*% base$simulation[[i]]$H
  data.frame(K = base$K[i], fold = base$MARKER_FOLD[i], seed = base$SEED[i],
             n = length(mu), mean_mu = mean(mu), mean_mu2 = mean(mu^2),
             signal_variance = mean((mu - mean(mu))^2),
             between_gene_variance = mean((rowMeans(mu) - mean(mu))^2),
             within_gene_variance = mean((mu - rowMeans(mu))^2))
}))
write.csv(moments, file.path(output, "per_simulation_moments.csv"), row.names = FALSE)

groups <- c(list(pilot_fold5_seeds1to10 = which(base$K == 3 & base$MARKER_FOLD == 5 & base$SEED %in% 1:10)),
            setNames(lapply(c(2, 5, 10, 100), function(f) which(base$K == 3 & base$MARKER_FOLD == f)),
                     paste0("fold", c(2, 5, 10, 100), "_all30")))
summary <- do.call(rbind, lapply(names(groups), function(name) {
  m <- moments[groups[[name]], ]
  a <- colSums(m[c("mean_mu", "mean_mu2", "signal_variance", "between_gene_variance", "within_gene_variance")] * m$n) / sum(m$n)
  data.frame(setup = name, simulations = nrow(m), t(a),
             pooled_variance = a[["mean_mu2"]] - a[["mean_mu"]]^2,
             min_signal_variance = min(m$signal_variance), max_signal_variance = max(m$signal_variance),
             nb_floor_phi001 = 0.01 * a[["mean_mu2"]] / a[["signal_variance"]],
             nb_floor_phi01 = 0.1 * a[["mean_mu2"]] / a[["signal_variance"]])
}))
write.csv(summary, file.path(output, "setup_summary.csv"), row.names = FALSE)
cat("Setup moments (population variances; average within each matrix):\n")
print(summary, digits = 10, row.names = FALSE)

pilot <- base$simulation[groups[[1]]]
S <- summary$signal_variance[1]
old <- find_grid_points(pilot)
old_details <- attr(old, "details")
old_levels <- old_details
old_levels$target_level <- old_details$target / S
for (name in c("poisson", "normal", "mul", "nb_0.01", "nb_0.1", "normal_clipped")) {
  old_levels[[paste0(name, "_level")]] <- old_details[[name]] / S
}
write.csv(old_levels, file.path(output, "current_grid_levels.csv"), row.names = FALSE)
cat("\nCurrent grid, expressed as noise variance / signal variance:\n")
print(old_levels, digits = 8, row.names = FALSE)

# Illustrative seven-point grid, not a user-approved replacement default.
levels <- 2^(-3:3)
candidate <- find_grid_points(pilot, target = levels * S)
candidate_details <- attr(candidate, "details")
comparison <- data.frame(level = levels, old_target = old_details$target,
                         new_target = candidate_details$target,
                         target_ratio = candidate_details$target / old_details$target,
                         old_fraction = old$fraction, new_fraction = candidate$fraction,
                         fraction_ratio = candidate$fraction / old$fraction,
                         old_normal_sd = old$normal_sd, new_normal_sd = candidate$normal_sd,
                         normal_sd_ratio = candidate$normal_sd / old$normal_sd,
                         old_mul_sd = old$mul_sd, new_mul_sd = candidate$mul_sd,
                         mul_sd_ratio = candidate$mul_sd / old$mul_sd,
                         achieved_poisson_level = candidate_details$poisson / S,
                         achieved_normal_level = candidate_details$normal / S,
                         achieved_mul_level = candidate_details$mul / S,
                         clipped_normal_mse_level = candidate_details$normal_clipped / S)
write.csv(comparison, file.path(output, "illustrative_grid_comparison.csv"), row.names = FALSE)
cat("\nIllustrative new doubling levels 1/8 through 8, compared by grid position:\n")
print(comparison, digits = 8, row.names = FALSE)

# NB at a matched level requires its own fraction for each dispersion.
# The existing helper instead reuses the Poisson fractions.
nb <- expand.grid(level = levels, dispersion = c(0.01, 0.1))
nb$target <- nb$level * S
nb$variance_floor <- nb$dispersion * summary$mean_mu2[1]
nb$attainable_finite_fraction <- nb$target > nb$variance_floor
nb$fraction_exact <- NA_real_
ok <- nb$attainable_finite_fraction
nb$fraction_exact[ok] <- summary$mean_mu[1] / (nb$target[ok] - nb$variance_floor[ok])
nb$fraction_rounded <- NA_real_
for (i in which(ok)) {
  nb$fraction_rounded[i] <- nice_value(nb$fraction_exact[i], nb$target[i],
    function(f) summary$mean_mu[1] / f + nb$dispersion[i] * summary$mean_mu2[1], 0.03)
}
nb$achieved_level <- (summary$mean_mu[1] / nb$fraction_rounded + nb$variance_floor) / S
write.csv(nb, file.path(output, "matched_nb_grid.csv"), row.names = FALSE)
cat("\nNB matched to the illustrative levels (NA means unattainable):\n")
print(nb, digits = 8, row.names = FALSE)

# Relabelling retains the same target vector, and hence the same old parameters.
reconstructed_targets <- (old_details$target / S) * S
cat("\nMaximum target reconstruction error from relabelling:",
    max(abs(reconstructed_targets - old_details$target)), "\n")
cat("Maximum signal-variance decomposition error:",
    max(abs(moments$signal_variance - moments$between_gene_variance - moments$within_gene_variance)), "\n")
capture.output(sessionInfo(), file = file.path(output, "sessionInfo.txt"))
