# Noise grid matched on mean noise variance

Helper: `artifact/20261028_noise_grid.R` (base R only).
Checks: `artifact/20261028_noise_grid_validation.R`.

## Usage

```r
source("artifact/20261028_noise_grid.R")
base_runs <- readRDS("/data/simulation_ground_truth_k3.rds")
grid <- find_grid_points(base_runs[K == 3 & MARKER_FOLD == 5, simulation],
                         target = 100 * 2^(0:6), dispersion = c(0.01, 0.1))
grid$fraction; grid$normal_sd; grid$mul_sd; grid$dispersion
attr(grid, "details")   # expected mean noise variance at the rounded values; normal_clipped is MSE
```

Call it once per simulation setup. NB uses `grid$fraction` crossed with
`grid$dispersion`, so each NB run pairs with a Poisson run at the same
fraction.

## Matched quantity

The grid matches Poisson, multiplicative and **unclipped** additive Normal
noise. The package clips Normal observations at zero; that model is not
matched (see Clipped Normal below).

The scaling step does not depend on a global factor of the data: uniform
Sinkhorn absorbs constant row and column factors, and expression scaling
divides by the total. For Poisson, NB, multiplicative and unclipped Normal
noise, dividing the observation by a constant makes its mean $V^*_{ij}$
(written $\mu$). The matched quantity is the mean over all entries of
$E[(V_{ij}/\text{scale} - \mu)^2]$.

| model (package 0.29.0) | scale | entry variance | mean over entries |
|---|---|---|---|
| `ApplyNBNoise(dispersion = 0, library_size_fraction = f)`: $V \sim \text{Poisson}(f\mu)$ | $f$ | $\mu / f$ | $\bar\mu / f$ |
| `ApplyNBNoise(dispersion = φ, library_size_fraction = f)`: mean $f\mu$, size $1/φ$ | $f$ | $\mu / f + φ\mu^2$ | $\bar\mu / f + φ\overline{\mu^2}$ |
| `ApplyNormalNoise(sd = σ)` before clipping | 1 | $σ^2$ | $σ^2$ |
| `ApplyMultiplicativeNoise(sd = s)`: $V = \mu e^Z$, $Z \sim N(0, s^2)$ | $e^{s^2/2}$ | $\mu^2(e^{s^2} - 1)$ | $\overline{\mu^2}(e^{s^2} - 1)$ |

$\bar\mu$ and $\overline{\mu^2}$ are pooled over all entries of all
simulations passed in. The library-size form follows the code: target
library size $f \cdot$ `colSums(mu)`, so each mean is scaled by exactly $f$.

Inverses for target $v$: $f = \bar\mu / v$, $σ = \sqrt v$,
$s = \sqrt{\log(1 + v / \overline{\mu^2})}$. NB has a floor
$φ\overline{\mu^2}$ and is not matched; it reuses the Poisson fractions.

Clipped Normal. With $a = \mu/σ$ and $Y = \max(\mu + ε, 0)$,
$E[(Y - \mu)^2] = σ^2(\Phi(a) - aφ(a)) + \mu^2\Phi(-a)$, from
$E[Z^2 1\{Z > c\}] = 1 - \Phi(c) + cφ(c)$ with $c = -a$, plus $\mu^2$ when
the draw is clipped. This is a mean squared error, not a variance: it
includes the squared bias $(E[Y] - \mu)^2$, with
$E[Y] = \mu\Phi(a) + σφ(a)$. The bias depends on $\mu/σ$, so no global
divisor removes it. Reported in `details$normal_clipped`; it is not used to
pick σ. For fold 5, seeds 1–10, it is 342 at target 400 and 3847 at target
6400, about 15% and 40% below the target.

## Rounding

Each exact value is rounded to the coarsest mantissa step of its decade,
in the order 1, 0.5, 0.1, 0.05, 0.01, whose implied mean variance is within
`tolerance` (default 3%) of the target. The 0.01 step is the fallback.
A value near a tolerance edge can flip with small changes in the moments:
fold 5 gives 0.0125 with seeds 1–10 and 0.012 with seeds 1–30.

## Validation (GeneralDualSimplex 0.29.0, commit bfd5ce69987c17e5a1253a477e9b73e965afc1aa)

Output of the validation script, base `/data/simulation_ground_truth_k3.rds`:

- K = 3, fold 5, seeds 1–10: fraction 0.4, 0.2, 0.1, 0.05, 0.025, 0.0125,
  0.0062; normal_sd 10, 14, 20, 28, 40, 57, 80; mul_sd 0.21, 0.29, 0.4,
  0.55, 0.73, 0.94, 1.15. Largest implied error (rounded up): Poisson 1.1%,
  Normal 2.0%, Mul 2.5%.
- Folds 2, 5, 10, 100 (30 seeds each) give the same grid up to one rounding
  step; $\bar\mu$ is 39.4–39.7 and $\overline{\mu^2}$ 2253–2266.
- One Monte Carlo draw with the package noise functions (fold 5, seed 1):
  measured over expected minus one is within ±0.5% for every model and level,
  except multiplicative at the two highest levels (+1.1%, −2.7%; heavy tail).
  The clipped-Normal formula agrees within 0.2%.

Limits: the match is on mean variance only. Variance relative to each
gene's squared level differs by model: at target 400 (fold 5, seeds 1–10),
the background-gene mean is 0.39 for Poisson, 0.88 for Normal and 0.17
for multiplicative noise. Equal mean variance does not give equal recovery
error. In the 10-seed pilot (`/data/simulation_runs_k3.rds`; package version
0.29.0 recorded, generating commit not available), medians of 1−r for W and
H were:

| setting | mean noise variance | 1−r W | 1−r H |
|---|---|---|---|
| Poisson, fraction 0.1 | 400 | 0.023 | 0.022 |
| Normal, SD 20 | 400 | 0.042 | 0.032 |
| Normal, SD 25 | 620 | 0.061 | 0.048 |
| Multiplicative, SD 0.5 | 650 | 0.019 | 0.011 |
| Poisson, fraction 0.05 | 790 | 0.060 | 0.052 |

Produced by the ignored scratch script `out/20261028_normal_noise/sweep_check.R`
(Normal variance before clipping).
