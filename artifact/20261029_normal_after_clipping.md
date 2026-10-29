# Targeting Normal noise after clipping: feasibility and open convention

Date: 2026-10-29. Status: design explanation; independent review accepted. No change to
the grid helper, package generator or recovery experiments. No replacement
grid is selected. Pre-clipping matching remains the baseline.

## User decisions carried forward

Keep the current parameter grid for now. The proposed noise-level calibration
is intended for the next round, whose numerical targets are not yet chosen.
Keep NB at the same Poisson exposure, accept its additional variance and report
its higher noise level. The user explicitly chose reporting the excess rather
than imposing a cap; the rounding preference is separate from overdispersion.
The user asks whether Normal can be calibrated after clipping, without yet
adopting that convention.

## Reviewed starting point and provenance

`artifact/20261028_noise_grid.md`, "Matched quantity" and "Clipped Normal",
and `artifact/20261028_noise_grid.R`, `clipped_normal_mse()`, already give the
clipped mean and MSE below. These files are at manuscript commit
`29cb5265b0ad7795666f17ab26fbd317c39ff21b`. The independent accepted formulation
review is `artifact/20261029_noise_formulation_review.md`, "Algebra checked"
and "Final verdict (after revision)"; its comparison is a working-tree
analysis based on that manuscript commit.

GeneralDualSimplex 0.29.0, package commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`, `R/simulation.R:340`, implements
`Observed <- pmax(mu + rnorm(length(mu), mean = 0, sd = sd), 0)`.
The package repository is read-only
here. No supplied ground-truth archive or recovery output is used for this
derivation.

## Two after-clipping targets

For each fixed nonnegative signal entry mu and sigma > 0, let

    Z ~ N(0,1), Y = max(mu + sigma Z, 0), a = mu/sigma.

Write Phi and phi for the standard Normal CDF and density. The reviewed mean
and MSE are

    h = E[Y | mu] = mu Phi(a) + sigma phi(a),
    b = h - mu = sigma phi(a) - mu Phi(-a),
    d = E[(Y-mu)^2 | mu]
      = sigma^2 [Phi(a) - a phi(a)] + mu^2 Phi(-a).

Since mu is fixed, the conditional variance follows from bias decomposition:

    g = Var(Y | mu) = d - b^2.

The current calibration equates mean conditional variance and mean squared
error about mu because the models being matched are conditionally unbiased.
Clipped Normal separates these quantities. For the chosen positive
signal-variance denominator S and target level L, there are two calibrations:

1. Keep the variance reading: solve mean_ij(g) = L S for sigma.
2. Keep the squared-error reading: solve mean_ij(d) = L S for sigma.

The first matches conditional noise variance after clipping. The second
matches total squared perturbation, the helper's written matched quantity;
its ratio would be described as an MSE ratio. Neither choice retains both
readings, restores conditional unbiasedness or restores the reviewed identity
that joint variance over entries and noise is (1 + L) S. Under variance
matching, mean MSE exceeds L S by mean_ij(b^2). Under MSE matching, mean
variance is below L S by mean_ij(b^2) evaluated at that calibration's own SD.
The decomposition uses mean_ij(b^2),
not the square of mean_ij(b). Neither target is the variance across the
entries of one observed matrix.

For multiple ground truths, average g or d across entries and replicates with
the same entry weighting used for S. S remains the average of the individual
matrices' population signal variances, not variance after pooling and centring.
These equations target expectations for the chosen calibration set, not the
realized error of each noise draw or an identical level for every seed.

## Inversion exists and needs no recovery runs

Both targets are continuous and strictly increasing with sigma for finite
mu >= 0. For d, differentiating gives

    d' = 2 sigma [Phi(a) - a phi(a)] > 0.

The bracket is the positive integral of z^2 phi(z) from -a to infinity.
Using h' = phi(a), the variance derivative is

    g' = 2 sigma [Phi(a)(1 - a phi(a)) - phi(a)^2] > 0.

For a >= 0, Phi(a) >= 1/2, a phi(a) <= 1/sqrt(2 pi e), and
2 phi(a)^2 <= 1/pi. Combining the last bound with Phi(a) >= 1/2 gives
phi(a)^2 <= Phi(a)/pi. Therefore the variance derivative's bracket is at least
Phi(a)[1 - 1/sqrt(2 pi e) - 1/pi], which is positive.

Both targets tend to zero as sigma tends to zero. At large sigma with mu
fixed, d/sigma^2 tends to 1/2 and g/sigma^2 tends to
1/2 - 1/(2 pi) > 0. Thus each positive target has a unique solution, also
after averaging over a finite calibration set.

Use a scalar root solver such as base R's `uniroot()`. A fixed SD bracket is
sqrt(L S) to sqrt(L S / c), where c = 1/2 for MSE or
c = 1/2 - 1/(2 pi) for variance. To see these bounds, write d/sigma^2 and
g/sigma^2 as functions of a. Their derivatives in a are respectively
2 a Phi(-a) and 2 Phi(-a)[a Phi(a) + phi(a)], both nonnegative for a >= 0.
Their values at a = 0 are the respective c, and their limits at large a are
1. The bounds survive averaging across entries and make
mean(target quantity) - L S nonpositive at the lower end and nonnegative at
the upper end. Both ends have positive SD,
avoiding direct evaluation of mu/sigma at sigma = 0.

Apply any rounding preference against the selected after-clipping quantity.
This needs signal values and Normal moments, not noise draws or recovery
experiments. It is a prospective calibration recipe, not an implemented
helper change.

For finite nonnegative mu and positive sigma, there is positive probability
of clipping. Clipping strictly reduces expected squared error, so
d < sigma^2; its positive bias gives g < d. Consequently an after-clipping
target requires a larger SD than pre-clipping matching, with variance matching
requiring a larger SD than MSE matching at the same target. The adjustment
depends on the signal values and target level; there is no single constant
correction valid for all signals and levels.

## Scientific choice still open

If the next round is intended to target actual after-clipping conditional
variance while retaining the variance reading of L, use variance matching
and report mean squared clipping bias and MSE alongside it. This changes the
calibration, while retaining the package's clipped Normal generator. It does
not remove entry-dependent bias. One global multiplier cannot align every
entry's clipped mean to its original mu.

If total perturbation about mu is the desired quantity, choose MSE matching
explicitly instead. Neither choice is adopted by this feasibility explanation.
Mean-scale corrections for Poisson/NB and multiplicative noise remain as
already reviewed. Equal noise levels do not imply equal recovery difficulty.

## Verification and review

Base R numerical integration of the first moment, second moment and squared
error agrees with the entry formulas for test signals including zero. Toy
root checks for variance and MSE recover their requested targets and give the
expected SD ordering. These are mathematical consistency checks, not a
calibration on the supplied archive. Outputs:
`out/20261029_normal_after_clipping/moment_checks.csv` and
`out/20261029_normal_after_clipping/toy_root_checks.csv`, produced from this
working tree based on manuscript commit
`29cb5265b0ad7795666f17ab26fbd317c39ff21b`.

Fresh Advisor - Claude independently checked the moments by numerical
integration, derivatives by finite differences and the analytic inversion
argument. Initial verdict: accept with minor changes. Findings F1-F6 were
addressed by distinguishing both readings of the prior calibration, retaining
the bias warning, using the fixed positive SD bracket, making the positivity
step explicit, correcting the package source line and clarifying the
signal/target dependence. The same reviewer checked the revised note and
returned final verdict: accept. Two optional wording clarifications were
then applied: each bias gap is evaluated at its own calibration's SD, and
the root bracket allows equality at an endpoint. Its final activity was read
and the agent archived. Report:
`artifact/20261029_normal_after_clipping_review.md`. Handoff:
`artifact/handoff/20261029-0433_claude_normal-after-clipping-review.md`.
No candidate grid or recovery study is being generated.
