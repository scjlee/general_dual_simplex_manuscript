# Illustrative alternative of panel C, before bi-marginal whitening.
# Run from the manuscript root in its renv:
# Rscript figure/fig1/panelC_vtilde/variance_share.R
# Same signal, noise, seeds and fitted scalings as panelC/noise_share.R.
# Gene g: v_g = sum_i (Vtilde_gi - mean_i Vtilde_gi)^2 / (n - 1).
# y = 100 v_g / sum_h v_h. The common n - 1 cancels in the share.
# This is ordinary within-gene variance across samples, signal and noise
# together. The denominator is the sum of gene variances, not variance of
# all matrix entries about one grand mean, and not inertia in Z.
# No manuscript claim relies on these illustrative data.
library(GeneralDualSimplex)
here <- "figure/fig1/panelC_vtilde"
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
rows <- list(); per_gene <- list()
for (model in names(noise)) {
  runs <- lapply(seq_len(R), function(r) {
    set.seed(r)
    sim <- GenerateMixture(pa$n_feature, pa$n_sample, pa$k, n_marker = pa$n_marker,
                          marker_fold = pa$marker_fold, profile_spread_sd = pa$profile_spread_sd)
    mu <- frac * sim$W %*% sim$H
    V <- noise[[model]](sim, mu)
    if (r == 1 && model == "Poisson")
      cat("Poisson replicate 1 identical to panel A:", identical(V, A$observed), "\n")
    keep <- rowSums(V) > 0; V <- V[keep, , drop = FALSE]
    total <- rowSums(V); ordering <- order(total)
    res <- list(kept = nrow(V))
    for (sc in c("Uniform", "Expression")) {
      s <- (CreateDSO(V) |> ScaleDSO(type = tolower(sc)))@scaling
      Vtilde <- s$r * sweep(V, 2, s$c, "*")
      variance <- rowSums((Vtilde - rowMeans(Vtilde))^2) / (ncol(Vtilde) - 1)
      share <- 100 * variance / sum(variance)
      res[[sc]] <- share[ordering]
      per_gene[[length(per_gene) + 1]] <<- data.frame(
        model, replicate = r, scaling = sc, gene = which(keep)[ordering],
        rank = seq_len(nrow(V)), observed_total = total[ordering],
        variance = variance[ordering], share = share[ordering])
      cat(sprintf("%s replicate %d %s: genes %d; mass %.12f; share sum %.12f%%; variance discrepancy %.3g\n",
                  model, r, sc, nrow(V), sum(Vtilde), sum(share),
                  max(abs(variance - apply(Vtilde, 1, var)))))
    }
    res
  })
  m <- min(vapply(runs, `[[`, 0L, "kept"))
  for (sc in c("Uniform", "Expression")) {
    mat <- sapply(runs, function(z) z[[sc]][seq_len(m)])
    rows[[length(rows) + 1]] <- data.frame(model, scaling = sc, rank = seq_len(m),
      mean = rowMeans(mat), lo = apply(mat, 1, min), hi = apply(mat, 1, max))
  }
}
d <- do.call(rbind, rows)
write.csv(d, file.path(here, "variance_share_by_rank.csv"), row.names = FALSE)
write.csv(do.call(rbind, per_gene), file.path(here, "variance_by_gene.csv"), row.names = FALSE)
for (z in split(d, list(d$model, d$scaling), drop = TRUE))
  cat(sprintf("%-21s %-10s mean %.4g-%.4g%%; band %.4g-%.4g%%; lowest quarter %.2f%%\n",
              z$model[1], z$scaling[1], min(z$mean), max(z$mean), min(z$lo), max(z$hi),
              sum(z$mean[z$rank <= max(z$rank) / 4])))
cat(sprintf("noise parameters: median expected count %.12g, phi %.12g, sigma %.12g\n", med, phi, sigma))
