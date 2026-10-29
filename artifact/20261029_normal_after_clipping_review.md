# Review: Normal noise calibrated after clipping

Reviewer: fresh Advisor - Claude (read-only except this file).
Target: `artifact/20261029_normal_after_clipping.md` (working tree, read
2026-10-29 after its "Verification and review" section was updated).
Manuscript commit: `29cb5265b0ad7795666f17ab26fbd317c39ff21b`;
`artifact/20261028_noise_grid.md` and `.R` are unmodified relative to it.
Package: GeneralDualSimplex 0.29.0, commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa` (read with `git show`, unchanged).
Scratch: `out/20261029_normal_after_clipping_review/check*.R` and `.txt`
(ignored; base R only; no grid, noise draw or recovery run).

## Verdict

**Accept with minor changes.** Every formula is correct and every derivative,
limit and bound I checked holds. The note can say all four points in the
handoff:

1. Yes: one can solve the expected clipped conditional variance for sigma.
2. MSE matching is also possible, but it targets a different quantity.
3. Clipping bias remains under either target.
4. No universal fixed correction multiplier exists.

My main point (F1) is about framing. Both targets extend the current
definition, and neither keeps all of its properties. The other findings
tighten wording and simplify the recipe.

## What I checked

All checks are base R, in the scratch outputs above.

- Mean h, bias b, MSE d and variance g (lines 42–49) against numerical
  integration split at the clipping point, for mu in {0, 0.1, 1, 5, 30} and
  sigma in {0.3, 1, 10, 100} with mu/sigma ≤ 20. Maximum relative error
  5.6e-16 (`check3.txt`).
- d' and g' (lines 73, 78) against central finite differences. Maximum
  relative error 1.9e-11 (`check.txt`). I also derived both by hand. For d',
  the terms from a = mu/sigma cancel, leaving 2 sigma[Phi(a) − a phi(a)]. For
  g', g' = d' − 2 b h' with h' = phi(a), and the bracket simplifies to
  Phi(a)(1 − a phi(a)) − phi(a)^2.
- The positivity bound (lines 80–82). The constant
  1 − 1/sqrt(2 pi e) − 1/pi equals 0.4397 > 0. On a ∈ [0, 12] the bracket
  divided by Phi(a) is at least 0.6446. The bracket itself is smallest at
  a = 0, where it equals 0.3408 = 1/2 − 1/(2 pi).
- The limits (lines 84–86). As sigma grows, d/sigma^2 tends to 1/2 and
  g/sigma^2 tends to 1/2 − 1/(2 pi) = 0.340845.
- The lead's outputs `out/20261029_normal_after_clipping/moment_checks.csv`
  and `toy_root_checks.csv` agree with my formulas. For example, mu = 0 and
  sigma = 3 give d = 4.5 and g = 3.0676 = 9 × 0.340845.
- Toy roots on my own mixture signal (300 zeros, 700 Exp(mean 30) entries) at
  targets T = 50, 700 and 5600. The SD ratio to sqrt(T) is 1.186, 1.358 and
  1.550 for variance matching, and 1.139, 1.259 and 1.367 for MSE matching.
  This is illustrative only and does not use the supplied archive.

## Findings

**F1 (moderate; framing) — lines 54, 57–58, 104–106.** The current definition
states v twice: as mean variance and as mean squared error about mu. See
`artifact/20261029_noise_level_comparison.md` lines 54–57, and
`artifact/20261028_noise_grid.md` lines 30–32, where "the matched quantity is
the mean over all entries of E[(V/scale − μ)^2]". The two statements agree
only because Poisson, NB, multiplicative and pre-clipping Normal noise are
conditionally unbiased. Clipped Normal splits them:

- Variance matching keeps the name "variance ratio".
- MSE matching keeps the helper's written matched quantity, and so remains
  "total squared perturbation about mu" for every model.

So line 54 ("Preserve the variance-based definition") and line 58 ("would need
an MSE-based name") favour one reading. Each option keeps one half of the
current definition and gives up the other.

Neither option restores the decomposition Var(X) = (1 + L) S. The comparison
note says this decomposition requires conditional unbiasedness (lines 64–75).
Under clipping, the entry means h(mu) replace mu. Also h is nondecreasing in
mu with slope Phi(a) in [1/2, 1), so Var_I(h) ≤ S. Under variance matching,
the expected spread across entries is therefore Var_I(h) + L S, at most
(1 + L) S, not equal to it.

Suggested wording for lines 54–58: "The current definition equates mean
variance and mean squared error about mu, because the other models are
conditionally unbiased. Clipped Normal is biased, so a choice is needed.
Variance matching keeps the variance reading; MSE matching keeps the
squared-error reading used by the helper. Neither restores
Var(X) = (1 + L) S." At line 105, "retaining the proposed definition of L"
should become "retaining the variance reading of L".

**F2 (minor; claim stated weaker than shown) — lines 95–100.** "Generally" and
"at least as large" can be made strict, and the multiplier can be bounded.
For every finite mu ≥ 0 and sigma > 0:

- Phi(−a) > 0, so d < sigma^2 strictly.
- b = E[max(−(mu + sigma Z), 0)] > 0, so g < d strictly.

Hence the after-clipping SD is always strictly larger than the pre-clipping
SD, and the variance-matched SD is always strictly larger than the
MSE-matched SD.

Bounds: d/sigma^2 = Phi(a) − a phi(a) + a^2 Phi(−a) has a-derivative
2a Phi(−a) ≥ 0, so it lies in [1/2, 1). g/sigma^2 has a-derivative
2 Phi(−a)(a Phi(a) + phi(a)) > 0, so it lies in [1/2 − 1/(2 pi), 1). Both
derivatives were checked by finite differences (`check2.txt`). Therefore the
ratio of the after-clipping SD to the pre-clipping SD sqrt(L S) is:

- in (1, 1/sqrt(1/2 − 1/(2 pi))] = (1, 1.7129] for variance matching;
- in (1, sqrt(2)] = (1, 1.4143] for MSE matching.

The upper ends are approached only when every mu is negligible relative to
sigma. Lines 99–100 remain correct: the multiplier is not constant (in the
toy check it rises from 1.19 to 1.55 across targets for one signal set), but
it is bounded.

**F3 (minor; recipe) — lines 89–90.** No expansion of the upper bound is
needed. By F2, the root lies in [sqrt(L S), sqrt(L S / c)], with
c = 1/2 − 1/(2 pi) for variance and c = 1/2 for MSE. The target minus L S is
≤ 0 at the lower end and ≥ 0 at the upper end. In my toy roots `uniroot()`
converged on this bracket with the expected signs (`check.txt`). The bracket
also keeps sigma away from 0. There, a = mu/sigma is infinite and, for
mu = 0, 0/0, so a direct evaluation returns NaN. Keep computing Phi(−a) with
`pnorm(-a)`, as the helper does, not as 1 − Phi(a).

**F4 (minor; provenance) — lines 28–29.** At the cited package commit,
`R/simulation.R:338` is the line `ApplyNormalNoise <- function(simulation, sd = 0.1) {`.
The clipping is on line 340:
`Observed <- pmax(mu + rnorm(length(mu), mean = 0, sd = sd), 0)`. Cite
`R/simulation.R:338–340`, and either mark the quoted expression as a
paraphrase or copy it exactly.

**F5 (minor; derivation step) — lines 80–82.** The step from
"2 phi(a)^2 ≤ 1/pi" to the stated lower bound uses
phi(a)^2 ≤ 1/(2 pi) ≤ Phi(a)/pi, which needs Phi(a) ≥ 1/2. Say this
explicitly. Optionally add that the bound is loose: the bracket's true
minimum is 1/2 − 1/(2 pi), at a = 0.

**F6 (minor; wording) — line 99.** "Depends on the distribution of mu/sigma":
sigma is the unknown being solved for. Suggest "depends on the signal values
relative to the solved SD, and hence on the target level."

## Points that need no change

- Line 59: the identity uses mean(b^2), not mean(b)^2. This is correct.
- Line 60: neither target is the variance across one observed matrix. This is
  correct and matches the accepted review's Monte Carlo result
  (`artifact/20261029_noise_formulation_review.md`, "Algebra checked": clipped
  var(X)/S 1.653 versus clipped MSE/S 0.798 at nominal L = 1).
- Lines 62–66: the weighting of entries and replicates matches the comparison
  note (lines 81–86) and the helper's pooling in `signal_moments()` and
  `clipped_normal_mse()`.
- Lines 108–109: one multiplier cannot remove the bias. A one-line proof:
  h(0) = sigma phi(0) > 0, so no c > 0 gives c h(0) = 0; and h(mu)/mu varies
  with a.
- Lines 9–15 and 102–114: the user's decisions are carried forward
  correctly. These are NB at the shared Poisson exposure with its higher
  level reported and no cap; the current grid kept; pre-clipping as baseline;
  no convention adopted.

## Open scientific questions (the user's)

1. Which reading of v should define L for clipped Normal: variance (keeps the
   name) or MSE about mu (keeps the helper's matched quantity and the "total
   perturbation" meaning shared with the unbiased models)? See F1.
2. Under variance matching, clipped Normal's total squared perturbation is
   larger than that of the unbiased models at the same L, by mean(b^2).
   Should figures report mean(b^2)/S and MSE/S next to L, as line 106
   proposes?
3. Which calibration set: pooled over all 120 matrices or per marker fold?
   This is still open from the accepted review (item 3) and applies here
   unchanged.

## Limits

I did not compute any value on the supplied ground-truth archive, generate
noise or run recovery. The toy signal is mine and illustrative. My checks
cover the formulas for a ∈ [0, 12] numerically and for all a ≥ 0 by the
analytic derivatives above.

## Re-review of the revised note

Read 2026-10-29 (156 lines). **Final verdict: accept.** F1–F6 are resolved.
Nothing blocks acceptance.

- F1: resolved at lines 52–68 and 124. Both readings are separated. The note
  states that neither restores unbiasedness or the (1 + L) S identity, and it
  states the bias and MSE gaps by direction.
- F2: resolved at lines 113–117. The SD orderings are now strict.
- F3: resolved at lines 98–106. The bracket, the a-derivatives, the values at
  a = 0 and the limits all match my checks (`check2.txt`).
- F4: resolved at lines 28–29. The line number and the code are exact.
- F5: resolved at lines 88–91.
- F6: resolved at lines 118–119.

Two optional wording points; neither changes a claim:

- Lines 65–66, "by the same amount": the gap is mean_ij(b^2) evaluated at each
  calibration's own SD. The two SDs differ, so the two amounts differ.
  Suggest "by mean_ij(b^2) at its own SD".
- Lines 104–105, "opposite signs": if every mu is 0, the variance or MSE
  target is met exactly at the upper end. The difference there is then zero,
  not of opposite sign. Base R's `uniroot()` accepts a zero at an end, but
  rounding error could give a small wrong-sign value. "Opposite signs, or zero
  at the upper end" is exact.

The open scientific questions above are unchanged and remain the user's.
