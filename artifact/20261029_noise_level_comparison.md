# Proposed noise level relative to signal variance: formulation and grid comparison

Status: independent review accepted the revised note and checked numbers.
No replacement grid is adopted and
there is no change to `artifact/20261028_noise_grid.R`. This note records a proposed experimental
calibration and descriptive calculations on supplied ground truths. It does not
report new recovery experiments or predict changes in recovery error.

## Request and scientific question

The user wants to compare the effect of marginal choices across noise models,
with a dimensionless noise-level axis. They proposed level 1 for additional
noise variance equal to Var_ij(mu), level 2 for twice that variance and level
0.5 for half. They requested an independent Claude review and a quantitative
comparison with the current settings.

Earlier discussion distinguished three requirements: calibration fixed across
preprocessing choices, invariance under a common global rescaling, and
invariance under arbitrary positive row/column rescaling of the same signal and
observation. Entrywise relative MSE satisfies the third requirement but divides
by individual squared signal entries. Relative Frobenius error and the proposed
variance ratio satisfy the first two when evaluated in a fixed original
representation, but not the third. None of these metrics is a universally
neutral weighting of noise.

The main experimental control is pairing: every marginal choice receives the
same ground truth and the same noisy observation. Recovery losses should use a
common target and definition across methods. A transformed-space noise measure
can explain differences, but calibrating separately after each marginal choice
would change the experimental input along with the treatment.
Pairing supports any calibration fixed before preprocessing; it does not select
this denominator over the alternatives. The reason to use L is its stated
interpretation relative to total entrywise signal variance, if that matches the
scientific question. There is no proof of general superiority here.

## Formulation and assumptions

For a fixed ground-truth matrix mu = W H containing N = mn entries, define

    S_mu = mean_ij[(mu_ij - mean(mu))^2].

This is the population variance across the flattened matrix (denominator N),
not the mean within-gene across-sample variance. Require S_mu > 0.

Let X be the observation expressed at the expected scale of mu, using known
generating parameters rather than a multiplier estimated from a realization:

| Model | X used for the comparison |
|---|---|
| Poisson/NB with scalar library fraction f | V / f |
| Multiplicative V = mu exp(Z), Z ~ Normal(0, s^2) | V / exp(s^2/2) |
| Additive Normal before clipping | V |

For these conditionally unbiased models, define

    v = mean_ij Var_noise(X_ij | mu)
      = mean_ij E_noise[(X_ij - mu_ij)^2 | mu],
    L = v / S_mu.

Suggested descriptive name: "noise-to-total-signal variance ratio", with
"total signal variance" explicitly defined as variance across all entries.
L is a variance ratio; sqrt(L) is RMS noise divided by the signal's standard
deviation across entries. It is not the fraction of total observed variance.
For a uniformly chosen entry I and a noise draw, conditional on the fixed mu,

    Var_{I,noise}(X_I | mu)
      = Var_I(E_noise[X_I | I,mu]) + E_I Var_noise(X_I | I,mu)
      = S_mu + v = (1 + L) S_mu.

This is a population statement over entries and noise draws. For an individual
noisy matrix, the cross term need not vanish. The expected empirical population
variance around that matrix's own sample mean is S_mu + v - Var_noise(mean(X));
under independent entrywise errors the last term is v/N. Thus even its
expectation is not exactly S_mu + v. Conditional unbiasedness is essential to
the stated decomposition.

Both numerator and denominator scale by c^2 when the same global c multiplies
mu and X. Arbitrary row/column rescaling generally changes L. Regenerating
noise after rescaling mu is a different experiment and requires recalibration.

For several simulations in one setup, this note uses the entry-weighted mean
of each matrix's S_mu as S, and the correspondingly pooled v. This defines
L = average(v_r) / average(S_r), not average(v_r/S_r) and not an exact level
for every replicate. All supplied matrices have equal size, so entry weighting
and equal replicate weighting coincide. Pooling before centering would also
include variation between replicate grand means; that is deliberately excluded.

## Mapping to the current helper

The current helper already uses the known mean multipliers above and calibrates
Poisson, multiplicative and pre-clipping Normal on v. The proposed axis changes
the denominator and target interpretation, not the mean correction.

For a setup denominator S, requested levels map to `target = levels * S`.
Write M1 = mean(mu) and M2 = mean(mu^2), pooled as in the current helper.
For exact level L:

| Model | Exact parameter before rounding |
|---|---|
| Poisson | f = M1 / (L S) |
| Normal before clipping | sigma = sqrt(L S) |
| Mean-aligned multiplicative | s = sqrt(log(1 + L S / M2)) |
| NB with scalar dispersion phi | f = M1 / (L S - phi M2), only if L S > phi M2 |

The NB floor in these level units is phi M2/S. It is not phi, which was the
floor under the relative Frobenius and entrywise-relative definitions.
Reusing Poisson fractions, as the current helper does, gives NB the Poisson
level plus phi M2/S. Equal-noise NB matching is a separate design change.

The existing rounding preference is retained in the numerical comparisons:
coarse decimal values are preferred when their implied v is within 3% of the
target, with a fallback that is not a hard guarantee. The tables distinguish
exact targets from achieved levels after parameter rounding.

## Input, implementation and calculation provenance

- Ground truths: `/data/simulation_ground_truth_k3.rds`, SHA-256
  `78c62b71a6f6969df3e43404e65096dcd014f41e31c0d82db00563235423c522`.
  It contains 120 W,H pairs: K=3; marker folds 2,5,10,100; 30 seeds per fold;
  each mu is 3000 by 500. The generating commit is not established.
- Comparison calculation: `artifact/20261029_noise_level_comparison.R`, a new
  working-tree script based on manuscript commit
  `29cb5265b0ad7795666f17ab26fbd317c39ff21b`. Script SHA-256:
  `81e5d9c6fb0348b40cf6a72ea6dac1ac7311a75f2854a6b0a817efde2aedc5d9`.
  The script uses base R and the unchanged existing helper, not package noise
  simulation functions. Results are therefore descriptive calculations on the
  supplied matrices, with exact conditional noise moments, not new draws.
- Existing helper: `artifact/20261028_noise_grid.R`, at the full manuscript
  commit above. Original design: `artifact/20261028_noise_grid.md`, "Matched
  quantity" and "Rounding".
- Implementation conventions: GeneralDualSimplex 0.29.0, source commit
  `bfd5ce69987c17e5a1253a477e9b73e965afc1aa`, `R/simulation.R:281`, `:317`
  and `:338`. R/src worktree clean at the check. This is verified implementation
  context, not proof that this commit generated the supplied archive.
- Run from the repository root with its renv:
  `Rscript artifact/20261029_noise_level_comparison.R`.
  The run exited successfully. Startup emitted the existing renv out-of-sync
  notice and a read-only cache-lock warning; no dependency changes were made.
- Output directory: `out/20261029_noise_level_comparison/`; console log:
  `out/20261029_noise_level_comparison.log`; runtime details: `sessionInfo.txt`.
  CSV files retain unrounded values. Displayed values below are rounded from
  those values. The directory is ignored scratch output, reproducible by script.

## Pilot signal variance and existing levels

For K=3, marker fold 5, seeds 1-10 (the same subset as the current helper's
pilot validation), M1 = 39.59060642, M2 = 2268.418812 and
S = 700.8332627. These come from `setup_summary.csv`, row
`pilot_fold5_seeds1to10`.

The old target v values therefore have the following nominal labels:

| Current target v | New label L = v/S |
|---:|---:|
| 100 | 0.142687 |
| 200 | 0.285375 |
| 400 | 0.570749 |
| 800 | 1.141498 |
| 1600 | 2.282997 |
| 3200 | 4.565993 |
| 6400 | 9.131987 |

Source: `current_grid_levels.csv`, `target` and `target_level`.
Merely applying these labels changes no parameters, observations or recovery
outcomes. Rounded parameters have slightly different
achieved levels, also reported in that CSV. NB and clipped Normal must retain
their distinct actual diagnostic levels.

Within this fixed setup, v, L and relative Frobenius error are exactly constant
multiples of one another: q_F = (S/M2) L = 0.3089523236 L. Across marker folds
this factor changes slightly; it is not one exact constant for the whole
archive when denominators are recomputed by fold. Any fixed alternative
denominator can relabel existing targets without changing the experiment.
Reusing the same numeric levels with a different denominator instead changes
the target noise variance and may change it substantially.

## Illustrative replacement levels and parameter changes

The user has not selected a full replacement grid. To quantify a concrete
alternative, the calculation uses seven doubling levels
0.125, 0.25, 0.5, 1, 2, 4, 8. This is an illustration, not an adopted default.

Compared by position against the old seven targets, the new exact target
variance is always S/800 = 0.8760415784 times the old target: 12.3958% lower.
Before rounding, Poisson fraction increases 14.1498%, and Normal SD decreases
6.4029%. Multiplicative log-SD changes nonlinearly with the target.

| New illustrative L | Old v | New v | Poisson f, old -> new | Normal SD, old -> new | Multiplicative log-SD, old -> new |
|---:|---:|---:|---:|---:|---:|
| 0.125 | 100 | 87.6042 | 0.4 -> 0.45 | 10 -> 9.4 | 0.21 -> 0.195 |
| 0.25 | 200 | 175.2083 | 0.2 -> 0.23 | 14 -> 13.2 | 0.29 -> 0.27 |
| 0.5 | 400 | 350.4166 | 0.1 -> 0.11 | 20 -> 18.5 | 0.4 -> 0.38 |
| 1 | 800 | 700.8333 | 0.05 -> 0.055 | 28 -> 26.5 | 0.55 -> 0.52 |
| 2 | 1600 | 1401.6665 | 0.025 -> 0.028 | 40 -> 37 | 0.73 -> 0.7 |
| 4 | 3200 | 2803.3331 | 0.0125 -> 0.014 | 57 -> 53 | 0.94 -> 0.9 |
| 8 | 6400 | 5606.6661 | 0.0062 -> 0.007 | 80 -> 75 | 1.15 -> 1.12 |

Source: `illustrative_grid_comparison.csv`. After current rounding, Poisson
fractions increase 10-15%, Normal SD decreases 5.3571-7.5%, and multiplicative
log-SD decreases 2.6087-7.1429%. These are parameter changes, not estimates of
recovery-error changes. The exact 12.3958% variance reduction refers to the
targets; rounding produces model-dependent achieved reductions.

The actual expected perturbation changes after rounding are:

| Model / quantity | Reduction from the corresponding current grid position |
|---|---:|
| Poisson variance | 9.09-13.05% |
| Normal variance before clipping | 10.42-14.44% |
| Mean-aligned multiplicative variance | 8.97-14.04% |
| Clipped Normal MSE | 9.24-13.10% |

These range endpoints are rounded outward to two decimal places. Each ratio
is 1 minus the new achieved level divided by the old achieved level, using
`illustrative_grid_comparison.csv` and `current_grid_levels.csv`. The constant
S cancels. At L=0.5 the variance reductions are 9.09% (Poisson), 14.44%
(pre-clipping Normal) and 10.47% (multiplicative). At L=1 they are 9.09%,
10.43% and 12.10%, respectively. At L=2 they are 10.71%, 14.44% and 10.17%.

## Separate NB and clipping consequences

For the pilot, the NB level floors are 0.03236745 at phi=0.01 and 0.32367454
at phi=0.1. The floor is approached as f tends to infinity and is not attained
at finite f. Thus L=0.125 and 0.25 cannot be matched at phi=0.1, even without
imposing f<=1. Source: `setup_summary.csv`, `nb_floor_phi001` and
`nb_floor_phi01`, and `matched_nb_grid.csv`.

At L=1, the exact matched NB fractions are 0.05838039 (phi=0.01) and
0.08352600 (phi=0.1). Current rounding gives 0.06 and 0.08, respectively,
with achieved L of 0.973880 and 1.029809. These would replace the use of the
same Poisson fraction for both dispersions only if equal-noise NB matching is
adopted. Pure relabelling preserves the existing NB design.

Normal remains calibrated before clipping. With the rounded parameters in
the illustrative grid:

| Nominal L | Normal SD | Pre-clipping achieved L | Clipped MSE / S |
|---:|---:|---:|---:|
| 0.5 | 18.5 | 0.488347 | 0.423825 |
| 1 | 26.5 | 1.002022 | 0.804665 |
| 2 | 37 | 1.953389 | 1.441873 |

Source: `illustrative_grid_comparison.csv`. The last column includes squared
bias and is not a conditional variance. The label change does not correct
the mismatch between pre-clipping variance and actual clipped perturbation.

## Denominator interpretation and stability

Source: `setup_summary.csv` and `per_simulation_moments.csv`.

- Across all 30 seeds at each marker fold, mean within-matrix S is 693.0383480
  (fold 2), 696.2665462 (fold 5), 698.2496240 (fold 10) and 700.4221417
  (fold 100). The largest is 1.0654% above the smallest. The denominator
  changes little across these supplied setups; this says nothing by itself
  about similarity of recovery difficulty or informative singular values.
- Within the ten pilot seeds, S ranges from 666.8641639 to 718.7731433.
  If the same target v=S_average is used for Normal before clipping, its
  individual levels range from 0.975041 to 1.050939. Poisson and multiplicative
  levels also depend on their seed-specific first/second signal moments.
- Pooling all pilot entries before centering gives variance 701.0026950,
  0.02418% above the mean within-matrix S. The numerical difference is small
  here, but the conventions are conceptually different.
- Decomposition by gene: S = 684.0332061 between-gene variance + 16.80005661
  mean within-gene variance. Thus 97.6028% of this denominator comes from
  differences in gene means. It should not be described as purely
  across-sample mixture variation. The largest decomposition residual in the
  120 supplied simulations is below 1e-13 (rounded upward).

Consequently, at nominal L=1, the target noise variance is 41.7161 times the
mean within-gene variance for the pilot. This is a statement about the chosen
denominator, not a recovery threshold. Replacing S with within-gene variance
while keeping the same numeric L would reduce these targets by that factor;
it would not merely relabel them.

An additional design option is to compute one parameter grid from M1, M2 and
S pooled over all 120 ground truths, then reuse that same grid across marker
folds. The archive-wide average within-matrix S is 696.9941650. Sharing only
S while recomputing M1 and M2 by fold would not ensure identical parameters.
Alternatively, fold-specific calibrations can deliberately target each
fold's own ratio. Small moment changes can cross the rounding thresholds and
produce larger discrete parameter differences. The reviewer documents this
in its F3 finding. Neither option has been adopted here.

For presentation, two significant figures are sufficient for level labels;
the extra digits in this record support reproducibility, not per-replicate
precision. Conditional expected per-seed levels vary around setup targets.

## Limits and review

These calculations quantify changes in target levels and generator parameters.
They cannot quantify how W/H recovery changes without new paired recovery runs.
The same noise energy can have different effects under different variance
patterns, dependence structures, tails and signal geometries.

Independent review handoff:
`artifact/handoff/20261029-0204_claude_noise-formulation-review.md`.
Review report: `artifact/20261029_noise_formulation_review.md`, initial verdict
"accept with changes". It independently recomputed the supplied moments,
parameter grids and clipped-Normal diagnostics. Its substantive requests were
to explain fixed-setup relabelling, name total entrywise variance precisely,
report achieved variance changes, clarify pairing does not select a
denominator, and distinguish shared from fold-specific calibration. Those
explanations are now included. The same fresh reviewer rechecked the revised
note, reproduced the added numbers and returned final verdict "accept".
Its final message was read with get_agent_activity and the agent archived.
No helper change or full replacement grid has been adopted. No inference about
the size, sign or qualitative stability of recovery differences is made.

Proposed house rule (not applied to AGENTS.md):
2026-10-29: Pairing justifies holding calibration fixed across methods; it does
not establish a preferred noise-normalization denominator.
