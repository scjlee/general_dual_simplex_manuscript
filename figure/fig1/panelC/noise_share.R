# Figure 1C data: where the noise sits after bi-whitening, per gene.
# Run from the manuscript root: Rscript figure/fig1/panelC/noise_share.R
# then python3 figure/fig1/panelC/make_fig1C.py (SVG master).
# Settings: panel A's simulation parameters (figure/fig1/panelA/simulation.rds).
# Five independent replicates: replicate r calls set.seed(r), then simulates the signal
# (GenerateMixture) and then the noise, so replicates share only parameters. Within a
# replicate, the signal is shared across noise models. Replicate 1 with Poisson noise
# reproduces panel A's observed matrix (asserted below).
# Baseline mu = library_fraction * W H. Noise models:
#   Poisson: ApplyNBNoise(dispersion = 0, library_size_fraction), as in panel A; E[V] = mu.
#   Proportional: mu * Gamma(shape 1/phi, rate 1/phi), Var = phi mu^2 (continuous); E[V] = mu.
#   Normal: max(mu + N(0, sigma^2), 0). mu is the pre-floor baseline; flooring raises
#     E[V] above mu and lowers the variance below sigma^2.
#   phi = 1/median(mu_A), sigma = sqrt(median(mu_A)) from panel A's signal: the three
#   models have equal relative noise at that median count BEFORE flooring only.
# Quantity: realized squared perturbation, not a variance. In each replicate and scaling,
# the scaling is fitted on the observed V (zero genes removed); the same fitted weights
# transform V - mu: N = D_l (V - mu) D_t, l = r/sqrt(a), t = c/sqrt(b) (the noise part of
# Z = D_a^-1/2 V~ D_b^-1/2). Gene share = row sum of N^2 / total, in percent. For the
# floored normal model V - mu includes the clipping bias.
# Output: x = rank by observed total within each replicate; mean, min and max over the
# replicates of the share of the i-th ranked gene. Ranks condition on the noise.
# Discussion: artifact/20261026_fig1C-narrative-options.md. Illustrative, not a benchmark.
library(GeneralDualSimplex)
here <- "figure/fig1/panelC"
pkg <- "/workspace/dual_simplex_functional/general_dual_simplex"
writeLines(c(
  paste("commit", system2("git", c("-C", pkg, "rev-parse", "HEAD"), stdout = TRUE)),
  paste("installed_version", packageVersion("GeneralDualSimplex")),
  "uncommitted_R_src:", system2("git", c("-C", pkg, "status", "--porcelain", "R", "src"), stdout = TRUE)),
  file.path(here, "package_commit.txt"))
A <- readRDS("figure/fig1/panelA/simulation.rds"); pa <- A$parameters
frac <- pa$library_fraction; R <- 5
med <- median(frac * A$signal); phi <- 1 / med; sigma <- sqrt(med)
noise <- list(
  Poisson = function(sim, mu) ApplyNBNoise(sim, dispersion = 0, library_size_fraction = frac)$Observed,
  Proportional = function(sim, mu) mu * matrix(rgamma(length(mu), shape = 1 / phi, rate = 1 / phi), nrow(mu)),
  `Normal, floored at 0` = function(sim, mu) pmax(mu + matrix(rnorm(length(mu), 0, sigma), nrow(mu)), 0))
replicate_shares <- function(r, model) {
  set.seed(r)
  sim <- GenerateMixture(pa$n_feature, pa$n_sample, pa$k, n_marker = pa$n_marker,
                         marker_fold = pa$marker_fold, profile_spread_sd = pa$profile_spread_sd)
  mu <- frac * sim$W %*% sim$H
  V <- noise[[model]](sim, mu)
  if (r == 1 && model == "Poisson") stopifnot(identical(V, A$observed))
  keep <- rowSums(V) > 0; V <- V[keep, , drop = FALSE]; mu <- mu[keep, , drop = FALSE]
  res <- list(total = rowSums(V), kept = sum(keep))
  for (sc in c("Uniform", "Expression")) {
    s <- (CreateDSO(V) |> ScaleDSO(type = tolower(sc)))@scaling
    if (sc == "Uniform") res$converged <- isTRUE(s$sinkhorn$converged)
    q <- rowSums((s$r / sqrt(s$a) * sweep(V - mu, 2, s$c / sqrt(s$b), "*"))^2)
    res[[sc]] <- 100 * q / sum(q)
  }
  res
}
rows <- list(); runlog <- list()
for (model in names(noise)) {
  runs <- lapply(seq_len(R), replicate_shares, model = model)
  kept <- sapply(runs, `[[`, "kept"); m <- min(kept)
  runlog[[model]] <- data.frame(model, genes_kept = paste(kept, collapse = "/"),
                                uniform_converged = sum(sapply(runs, `[[`, "converged")))
  for (sc in c("Uniform", "Expression")) {
    mat <- sapply(runs, function(z) z[[sc]][order(z$total)][seq_len(m)])
    rows[[length(rows) + 1]] <- data.frame(model, scaling = sc, rank = seq_len(m), mean = rowMeans(mat),
      lo = apply(mat, 1, min), hi = apply(mat, 1, max))
  }
}
d <- do.call(rbind, rows)
write.csv(d, file.path(here, "noise_share_by_rank.csv"), row.names = FALSE)
print(do.call(rbind, runlog), row.names = FALSE)
for (k in split(d, list(d$model, d$scaling), drop = TRUE))
  cat(sprintf("%-21s %-10s mean %.3g-%.3g%%  lowest quarter %.1f%%  median (max-min)/mean %.2f\n",
              k$model[1], k$scaling[1], min(k$mean), max(k$mean),
              100 * sum(k$mean[k$rank <= max(k$rank) / 4]) / sum(k$mean), median((k$hi - k$lo) / k$mean)))
cat(sprintf("noise parameters: median expected count %.4g, phi %.4g, sigma %.4g\n", med, phi, sigma))

