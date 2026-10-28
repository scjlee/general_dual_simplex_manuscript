# Source from the manuscript root. Base R only.
# Noise parameters matched on mean per-entry noise variance in units of
# V* = W H. See 20261028_noise_grid.md for the derivation.

# `simulations` is a list of list(W, H), e.g. base_runs$simulation for one
# setup. Moments are pooled over all entries of all simulations.
signal_moments <- function(simulations) {
  sums <- sapply(simulations, function(sim) {
    V_star <- sim$W %*% sim$H
    c(n = length(V_star), mu = sum(V_star), mu2 = sum(V_star^2))
  })
  totals <- rowSums(sums)
  c(mean_mu = totals[["mu"]] / totals[["n"]], mean_mu2 = totals[["mu2"]] / totals[["n"]])
}

# Mean of (Observed / scale - V*)^2 with Normal clipping at zero:
# sigma^2 (Phi(a) - a phi(a)) + mu^2 Phi(-a), with a = mu / sigma.
clipped_normal_mse <- function(simulations, normal_sd) {
  sapply(normal_sd, function(sigma) {
    sums <- sapply(simulations, function(sim) {
      V_star <- sim$W %*% sim$H
      a <- V_star / sigma
      c(length(V_star), sum(sigma^2 * (pnorm(a) - a * dnorm(a)) + V_star^2 * pnorm(-a)))
    })
    sum(sums[2, ]) / sum(sums[1, ])
  })
}

# Expected mean noise variance of each model at given parameters.
# Poisson and NB counts are divided by the fraction f; multiplicative noise by
# its mean multiplier exp(s^2 / 2). Normal is before clipping.
noise_variance <- function(moments, fraction, normal_sd, mul_sd, dispersion) {
  nb <- outer(moments[["mean_mu"]] / fraction, dispersion * moments[["mean_mu2"]], "+")
  colnames(nb) <- paste0("nb_", dispersion)
  cbind(
    poisson = moments[["mean_mu"]] / fraction,
    normal = normal_sd^2,
    mul = moments[["mean_mu2"]] * (exp(mul_sd^2) - 1),
    nb
  )
}

# Round x to the coarsest mantissa step (1, 0.5, 0.1, 0.05, 0.01 of its decade)
# whose implied variance is within `tolerance` of the target.
nice_value <- function(x, target, implied_variance, tolerance) {
  decade <- 10^floor(log10(x))
  for (step in c(1, 0.5, 0.1, 0.05, 0.01)) {
    candidate <- signif(round(x / (step * decade)) * step * decade, 6)
    if (abs(implied_variance(candidate) / target - 1) <= tolerance) return(candidate)
  }
  candidate
}

# NB reuses the Poisson fractions, so each NB run pairs with a Poisson run.
find_grid_points <- function(simulations, target = 100 * 2^(0:6),
                             dispersion = c(0.01, 0.1), tolerance = 0.03) {
  moments <- signal_moments(simulations)
  nice <- function(exact, implied_variance) {
    mapply(nice_value, exact, target, MoreArgs = list(implied_variance, tolerance))
  }
  fraction <- nice(moments[["mean_mu"]] / target, function(f) moments[["mean_mu"]] / f)
  normal_sd <- nice(sqrt(target), function(s) s^2)
  mul_sd <- nice(sqrt(log1p(target / moments[["mean_mu2"]])),
                 function(s) moments[["mean_mu2"]] * (exp(s^2) - 1))

  details <- data.frame(
    target, fraction, normal_sd, mul_sd,
    noise_variance(moments, fraction, normal_sd, mul_sd, dispersion),
    normal_clipped = clipped_normal_mse(simulations, normal_sd),
    check.names = FALSE
  )
  structure(
    list(fraction = fraction, normal_sd = normal_sd, mul_sd = mul_sd, dispersion = dispersion),
    moments = moments,
    details = details
  )
}
