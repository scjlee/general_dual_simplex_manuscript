# Figure 1C diagnostic: how much of the variation in Z (beyond the trivial pair) is signal.
# Run from the manuscript root: Rscript figure/fig1/panelC/signal_noise_split.R
# Same replicates, noise models and fitted scalings as noise_share.R.
# With u = sqrt(a), v = sqrt(b), P = I - u u^T, Q = I - v v^T, fitted weights
# l = r/sqrt(a), t = c/sqrt(b), signal S = D_l mu D_t and perturbation N = D_l (V - mu) D_t:
#   E = Z - u v^T = P S Q + P N Q, so ||E||^2 = ||PSQ||^2 + ||PNQ||^2 + 2 <PSQ, PNQ>.
# Reports each term as a percentage of ||E||^2. Decomposition from the Advisor - Codex
# review (artifact/20261026_fig1C-noise-share.md, Review). For floored normal noise, N is
# relative to the pre-floor mu and so includes the flooring bias. Illustrative.
library(GeneralDualSimplex)
here <- "figure/fig1/panelC"
A <- readRDS("figure/fig1/panelA/simulation.rds"); pa <- A$parameters
frac <- pa$library_fraction; R <- 5
med <- median(frac * A$signal); phi <- 1 / med; sigma <- sqrt(med)
noise <- list(
  Poisson = function(sim, mu) ApplyNBNoise(sim, dispersion = 0, library_size_fraction = frac)$Observed,
  Proportional = function(sim, mu) mu * matrix(rgamma(length(mu), shape = 1 / phi, rate = 1 / phi), nrow(mu)),
  `Normal, floored at 0` = function(sim, mu) pmax(mu + matrix(rnorm(length(mu), 0, sigma), nrow(mu)), 0))
project <- function(X, u, v) {  # P X Q
  X <- X - u %o% as.vector(crossprod(u, X))
  X - as.vector(X %*% v) %o% v
}
rows <- list()
for (model in names(noise)) for (r in seq_len(R)) {
  set.seed(r)  # same seeds and order as noise_share.R
  sim <- GenerateMixture(pa$n_feature, pa$n_sample, pa$k, n_marker = pa$n_marker,
                         marker_fold = pa$marker_fold, profile_spread_sd = pa$profile_spread_sd)
  mu <- frac * sim$W %*% sim$H
  V <- noise[[model]](sim, mu)
  keep <- rowSums(V) > 0; V <- V[keep, , drop = FALSE]; mu <- mu[keep, , drop = FALSE]
  for (sc in c("Uniform", "Expression")) {
    s <- (CreateDSO(V) |> ScaleDSO(type = tolower(sc)))@scaling
    l <- s$r / sqrt(s$a); t <- s$c / sqrt(s$b); u <- sqrt(s$a); v <- sqrt(s$b)
    Z <- l * sweep(V, 2, t, "*"); S <- l * sweep(mu, 2, t, "*")
    E <- Z - u %o% v; S0 <- project(S, u, v); N0 <- project(Z - S, u, v)
    stopifnot(max(abs(E - S0 - N0)) < 1e-10)
    total <- sum(E^2)
    rows[[length(rows) + 1]] <- data.frame(model, replicate = r, scaling = sc,
      signal_pct = 100 * sum(S0^2) / total, noise_pct = 100 * sum(N0^2) / total,
      cross_pct = 200 * sum(S0 * N0) / total)
  }
}
d <- do.call(rbind, rows)
write.csv(d, file.path(here, "signal_noise_split.csv"), row.names = FALSE)
for (k in split(d, list(d$model, d$scaling), drop = TRUE))
  cat(sprintf("%-21s %-10s signal %.2f-%.2f%%  noise %.2f-%.2f%%  cross %.2f-%.2f%%\n",
              k$model[1], k$scaling[1], min(k$signal_pct), max(k$signal_pct),
              min(k$noise_pct), max(k$noise_pct), min(k$cross_pct), max(k$cross_pct)))
