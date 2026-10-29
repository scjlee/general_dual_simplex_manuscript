# Review: noise level relative to signal variance

Reviewer: Claude (fresh, independent). Role: Reviewer. Date: 2026-10-29.
Handoff: `artifact/handoff/20261029-0204_claude_noise-formulation-review.md`.
Reviewed: `artifact/20261029_noise_level_comparison.md` (working tree),
`artifact/20261029_noise_level_comparison.R` (SHA-256
`81e5d9c6fb0348b40cf6a72ea6dac1ac7311a75f2854a6b0a817efde2aedc5d9`, matches the
note), its CSVs in `out/20261029_noise_level_comparison/`,
`artifact/20261028_noise_grid.R` and `.md` at manuscript commit
`29cb5265b0ad7795666f17ab26fbd317c39ff21b`. Package conventions:
GeneralDualSimplex 0.29.0, commit `bfd5ce69987c17e5a1253a477e9b73e965afc1aa`,
`R/simulation.R:281-345`, R/src clean.
Input: `/data/simulation_ground_truth_k3.rds`, SHA-256 verified as
`78c62b71…c522`.
Independent recomputation: `out/20261029_noise_formulation_review/recompute.R`,
log `recompute.log` and CSVs in the same directory. It is my own code. It
reuses only the helper's `find_grid_points` and `nice_value`.

## Final verdict (after revision)

**Accept.** The revised note (re-review below) resolves F1–F5, F7 bullet 1
and F8 bullet 1, and its new numbers reproduce. Nothing remains that blocks
acceptance. The user still owns the open scientific choices listed below.

## Initial verdict

**Accept with changes.** The algebra is correct and every number I checked
reproduces. The note keeps its claims within its evidence. My main criticisms
are about interpretation and design, not about errors:

1. Relabelling the existing v targets changes nothing physical. Within one
   setup, L is an exact constant multiple of v and of q_F (pilot:
   L = v/700.83, q_F = 0.309 L). Across folds the factors are close but not
   equal (F1). Physical change comes only from recalibrating to new numeric
   levels. With the illustrative 1/8…8 grid, every target falls 12.4%, which
   is 0.19 of one doubling step. Recalibrating the *same* numeric L under a
   different denominator would differ far more: about 3.2 times for M2 and
   about 42 times for within-gene variance.
2. The name "level 1 = noise variance equals signal variance" misleads.
   Gene abundance differences make up 97.6% of S. Measured against mean
   within-gene variance, L = 1 is a noise variance about 42 times larger.
3. Fitting a separate S to each marker fold creates parameter splits between
   folds that the old absolute-v grid did not have, including for Normal noise.
   One archive-wide parameter grid, reused for every fold, would avoid them.
4. The pairing argument is sound, but it does not choose a denominator. It
   supports any calibration done in the original representation.

The lead is right that recovery changes cannot be predicted without new runs.
Under a monotonicity assumption, the population performance curves can be
bracketed. Finite Monte Carlo estimates cannot (finding F6).

## How much difference the modification makes (answer for the user)

| Change | Generator parameters | Observations / recovery |
|---|---|---|
| Relabel the current grid only (L = v/S) | none | none |
| Adopt round levels 1/8…8 in place of 100·2^k | exact target v × S/800 = 0.876 (−12.4%) at every position; achieved v after rounding × 0.856–0.910 (8.97–14.44% lower, by model and position) | new runs needed; not predictable from these calculations |
| Also match NB to L | at φ = 0.1, f rises from 0.11 to 0.30 at L = 0.5; L = 1/8 and 1/4 cannot be matched | new NB design; with reused fractions, NB at φ = 0.1 is 1.6–3.6 times the Poisson level at L ≤ 0.5 |
| Normal stays calibrated before clipping | unchanged convention | actual clipped MSE/S is 0.42, 0.80 and 1.44 at nominal L = 0.5, 1 and 2 |

Sources: `out/20261029_noise_formulation_review/grid_comparison.csv` and
`nb_matched.csv`. Pilot setup: fold 5, seeds 1–10, S = 700.833.

## Verified numbers

My recomputation reproduces each of the following:

- Pilot M1 = 39.5906, M2 = 2268.42, S = 700.833 (note lines 139–141).
- The old labels 0.142687–9.131987 (line 148ff).
- S/800 = 0.876042; the Poisson fraction rises 14.15% and the Normal SD falls
  6.40% before rounding (lines 169–172).
- Every rounded parameter in the table at lines 174–182.
- The rounded-parameter change ranges at lines 184–186 (Poisson +10% to +15%,
  Normal −5.36% to −7.5%, log-SD −2.61% to −7.14%).
- The NB floors 0.032367 and 0.323675, and the L = 1 matched fractions
  0.05838 and 0.08353, rounding to 0.06 and 0.08 with achieved L 0.9739 and
  1.0298.
- Clipped MSE/S of 0.4238, 0.8047 and 1.4419.
- Fold S of 693.04–700.42 (1.07% spread).
- The pilot per-seed S range of 666.86–718.77, the pooled-before-centering
  difference of +0.024%, and the decomposition 684.03 + 16.80 (97.60%
  between genes) with a residual below 1e-13.

Algebra checked:

- The total-variance identity (line 59–61) holds.
- The expected empirical variance S + v − Var(mean X) (line 65–66) holds:
  E[mean(X−m)²] = S + v and E[(X̄−m)²] = Var(X̄).
- Monte Carlo check (pilot seed 1, exact L = 1): the empirical var(X)/S is
  2.0003 for Poisson and 2.0017 for unclipped Normal. For clipped Normal it
  is 1.653, and the clipped MSE/S is 0.798. The decomposition therefore
  fails for clipped Normal, as the note states.
- The NB floor φM2/S, and the statement that φ is the floor under q_F and
  q_entry (line 98–99), are correct. The package NB variance f·mu + φf²mu²
  divided by f² gives mu/f + φmu².
- The mean corrections match the package code: library size `f*colSums(mu)`,
  multiplier not mean-corrected, clipping at zero.

## Findings

**F1. Relabelling and recalibration are different changes (severity:
interpretation).**

- *Within one fixed setup and denominator,* L, q_F and v are exact constant
  multiples. For the pilot, L = v/700.833 and q_F = (S/M2)·L = 0.3090 L.
- *Across folds* the factors are only approximately equal: S/M2 is
  0.306–0.311 and S is 693–700 (`setup.csv`).
- *If the existing v targets are kept and only relabelled,* the choice of
  denominator changes labels only. Here that holds for total S, M2 (q_F) or
  within-gene variance alike.
- *If the same numeric L values are recalibrated* under a different
  denominator, the targets change by the ratio of the denominators. M2/S is
  3.24 for the pilot. Within-gene variance is 16.80 against S = 700.83, a
  ratio of about 42. So "L = 1" under the within-gene variance would be a
  target about 42 times smaller than "L = 1" under the total variance.
- The note implies the relabelling point at lines 221–225 but never says it
  outright. It should, together with the recalibration contrast, because
  this is the direct answer to "how much difference".

**F2. The label overstates signal (severity: wording/claim risk).**

- The note defines S correctly (lines 35–38, 233–237). However, the phrase
  "noise variance equal to signal variance" (line 11–13) will be read as an
  SNR of 1 for the mixture.
- Gene means make up 97.6% of S. Between-sample variance makes up 8e-6. The
  within-gene (row-centred) part is 2.4%: 16.8 for the pilot, essentially all
  of it gene-by-sample interaction.
- At L = 1, the noise variance is 41.7 times the mean within-gene variance.
  At L = 1/8 it is still 5.2 times.
- Uniform Sinkhorn scaling removes row scale. Most of S is therefore a
  quantity that one of the compared treatments discards.
- This does not bias the paired contrasts, because calibration happens
  before treatment. It does affect how a reader understands "level 1".
- Suggestion: name it "noise-to-total-signal variance ratio", and report
  S_within/S (0.024) in the methods so readers can convert.

**F3. A separate S per fold creates fold-specific parameters (severity:
design).**

- Under the old grid the target v is the same for every fold. Normal SD is
  then identical across all five setups, and Poisson and multiplicative noise
  split at only 2 and 1 positions.
- Under target = L·S_fold, the target itself differs by fold (86.6–87.6 at
  L = 1/8). The rounded parameters split at 3 Poisson positions, 3 Normal
  positions and 2 multiplicative positions. Examples: f 0.055 vs 0.057 at
  L = 1; Normal SD 26 vs 26.5; SD 13.0 vs 13.2.
- These splits are as large as 4.5% in achieved v. That exceeds the 1.07%
  difference in S between folds that they are meant to track.
- If marker folds will be compared, compute ONE parameter grid from moments
  pooled over all 120 matrices: M1 = 39.5045, M2 = 2257.90 and S = 696.994
  (`setup.csv`, row `all120`). Then reuse that one set of f, σ and s for every
  fold. Sharing S alone while recomputing M1 and M2 by fold would leave
  splits: f at 2 positions and s at 1. Under the one shared grid, each fold's
  own conditional expected level is 0.973–1.034 times nominal, rounding
  included (`archive_grid_check.R`). The alternative is to state that
  fold-specific rounding is accepted.

**F4. Report achieved variance changes, not only parameter changes
(severity: completeness).**

- Lines 184–188 give parameter ratios and say the achieved reductions are
  "model-dependent", but give no numbers.
- In the pilot, achieved new/old v is 0.870–0.909 for Poisson, 0.856–0.896
  for Normal, 0.860–0.910 for multiplicative and 0.869–0.908 for clipped
  MSE. This is the number the user asked for.
- The ratios are not monotone in grid position. At L = 0.5, Poisson falls
  9.1% and Normal 14.4%. The models' relative positions therefore shift by
  up to 6.3% between grids (0.9091/0.8556 at L = 0.5).

**F5. Per-seed level spread exceeds the rounding tolerance (severity:
precision of reporting).**

- With one setup-level parameter set (fold 5, 30 seeds), the conditional
  expected per-seed level at nominal 1 ranges 0.956–1.032 (Poisson), 0.941–1.018 (Normal)
  and 0.968–1.051 (multiplicative). Each value is the seed's own v at the
  rounded parameters divided by its own S. It is computed from exact moments;
  no noisy draws enter. Seed S spans 0.954–1.032 of the setup S.
- This ±5% exceeds the 3% rounding tolerance. Six-digit labels such as
  0.142687 are therefore setup-level definitions, not per-run levels.
- Ratio of averages vs mean of ratios: 0.99536 vs 0.99571 (Poisson, fold 5,
  L = 1). The choice is immaterial here.
- Suggestion: report levels to two significant figures, with the seed range
  in a supplement.

**F6. Recovery change: not predictable from these calculations (severity:
the lead's limit statement is correct).**

- Lines 241–242 are right that the calculations cannot quantify the change
  in recovery.
- The new exact targets are the old ones shifted by −0.19 doubling steps.
  After rounding, every achieved new v lies strictly between the achieved
  values at old positions k−1 and k, or below old position 0.
- Suppose the population (infinite-replicate) error curve for each model and
  marginal choice is non-decreasing in v. Then the population value at each
  new point lies between the population values at the adjacent old points.
- This brackets population curves only. It does not bracket finite-sample
  Monte Carlo estimates such as 30-seed medians, which can violate the
  ordering. Monotonicity itself is an assumption: the 10-seed pilot table in
  `20261028_noise_grid.md` is consistent with it but does not test it.
- These calculations give no expectation for the paired contrast between
  marginal choices. That needs the rerun.

**F7. Criticism of the primary recommendation (q_F / L in the fixed original
representation; pairing).**

- *The pairing argument is necessary but does not discriminate.* Any
  denominator calibrated before treatment preserves pairing: q_F, L, q_entry
  or raw v. Pairing argues against calibrating after each marginal choice. It
  does not argue for L or q_F over q_entry. Lines 25–29 are correct as
  written. The decision log should not record pairing as the reason for
  picking q_F/L.
- *Equal L is a nominal dose, not equal difficulty.* The lead says this. But
  the study compares marginal choices *across* noise models, so the risk is
  in the inference. The pilot shows a counterexample: at v = 400, Normal
  gave about twice the W error of Poisson (0.042 vs 0.023), per the
  `20261028_noise_grid.md` table, whose generating commit is unavailable.
  Statements of the form "marginal A beats B more under model X than Y at
  the same level" depend on the μ²-weighted choice. Keep such statements
  descriptive, or add an equal-difficulty secondary axis. An example would
  be the level at which a fixed reference pipeline reaches a set error. That
  axis is calibrated on outcomes, so it must be labelled as such.
- *q_F/L weighting.* Both weight fractional squared errors by mu_ij².
  Neither says by itself which entries dominate: that depends on how the
  noise variance scales with mu. Per-entry variance Var(X_ij) is constant
  (σ²) for Normal before clipping, proportional to mu_ij (mu_ij/f) for
  Poisson, and proportional to mu_ij² (mu_ij²(exp(s²) − 1)) for mean-aligned
  multiplicative noise. NB adds φ·mu_ij² to the Poisson term. So the same
  mean variance is spread over entries in very different ways. The relative
  variance Var(X_ij)/mu_ij² is:
  - Poisson: 1/(f·mu_ij), largest for low-abundance entries;
  - Normal before clipping: σ²/mu_ij², steeper still;
  - mean-aligned multiplicative: exp(s²) − 1, the same for every entry.

  At equal L, the models therefore put different relative noise on the
  low-abundance genes that row scaling amplifies (`20261028_noise_grid.md`,
  Limits: background-gene means 0.39, 0.88 and 0.17 at target 400). This is
  a descriptive difference in noise patterns. These calculations do not
  establish that it causes the pilot's recovery differences.

**F8. Minor.**

- Lines 157–159: "reconstructs the original targets with zero floating point
  difference" checks (v/S)·S = v. That is tautological and tests nothing.
  Drop it or say so.
- The handoff/note wording "NB reuses Poisson fractions … not equal-noise
  matched" is correct. Add the size of the mismatch: with reused fractions,
  NB at φ = 0.1 reaches L = 0.45, 0.57 and 0.84 where Poisson is at 0.125,
  0.25 and 0.5 (`nb_matched.csv`).
- The comparison script first failed with a syntax error at line 28 (an extra
  `)`). The lead fixed it before the final run, and the reviewed version
  parses.

## Unresolved scientific choices (the user's)

1. Denominator: total S (as proposed; 97.6% gene abundance), within-gene
   variance, or M2 (q_F). If the existing v targets are kept and relabelled,
   this choice changes labels only. If the same numeric L values are
   recalibrated, it changes the targets by the ratio of the denominators:
   about 3.2 times for M2 and about 42 times for within-gene variance (F1).
2. Relabel only (no reruns; labels 0.14…9.1), or adopt round levels and
   rerun (targets −12.4%).
3. One parameter grid from pooled M1, M2 and S over all 120 matrices,
   reused for every fold, or a separate grid per marker fold (F3).
4. NB matched to L, paired with Poisson fractions, or both (both is
   possible: they are separate run sets).
5. Normal calibrated before clipping (current), or on clipped MSE. The
   clipped MSE falls 4–39% below nominal across L = 1/8…8.
6. Whether comparisons across noise models at equal L are claimed as equal
   difficulty (I advise not; F7).

## Re-review of the revised comparison note

Checked: `artifact/20261029_noise_level_comparison.md`, revised working tree,
2026-10-29. The script SHA-256 is unchanged (`81e5d9c6…d9`).

Numbers reproduced against my CSVs:

- q_F = 0.3089523236 L (line 170).
- Achieved reductions after rounding (lines 208–211): Poisson 9.09–13.05%,
  Normal 10.42–14.44%, multiplicative 8.97–14.04%, clipped MSE 9.24–13.10%.
  My unrounded ratios give 9.091–13.043%, 10.43–14.44%, 8.97–14.04% and
  9.24–13.09%, so the bounds are rounded outward correctly.
- The point values at L = 0.5, 1 and 2 (lines 216–218).
- S/S_within = 41.7161 (line 269).
- Archive S = 696.9941650 (line 277).
- Sharing S alone does not give identical parameters (line 278): it leaves
  splits in f at 2 positions and in s at 1.

Resolved:

- F1: lines 169–175 and 269–273.
- F2: lines 60–61.
- F3: lines 275–282.
- F4: lines 204–218.
- F5: lines 284–286.
- F7, pairing: lines 31–34.
- F8, tautological check: removed from the prose.
- The note no longer infers recovery stability (lines 304–305).

Remaining, none blocking:

- The note does not mention that per-fold calibration also splits the Normal
  SD (26 vs 26.5 at L = 1). The old grid never splits it. One clause at line
  280 would cover it.
- The proposed house rule (lines 307–309) is sound. Adopting it is the
  user's decision.

## Limits of this review

- I did not rerun any recovery and drew no noise with the package
  functions. My only draws were one base-R Monte Carlo check.
- The archive's generating commit is still unknown.
- I did not read the package decision record.
