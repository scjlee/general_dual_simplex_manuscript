# Session handoff: formulation and variance-based noise levels

Date: 2026-10-29. This summarizes the discussion and the final independent
Claude review. It introduces no new calculations, scientific claims or adopted
defaults. The grid helper remains unchanged. The purpose of the next session
is to settle the experimental design before implementation.

## Aim and experimental control

Study how different marginal choices affect recovery under Poisson,
negative-binomial (NB), multiplicative lognormal and additive Normal noise.
The user wants an interpretable dimensionless noise level for selecting the
simulation grid.

For each ground truth and noise draw, give every marginal method the same
observed matrix. Compare recovery using a common target and loss definition.
Choose calibration before marginal preprocessing. Matching separately after
each marginal choice would change the input as well as the method.

Claude's correction to the lead's initial rationale is important: this paired
design supports any fixed input calibration. It does not establish that a
particular denominator is scientifically superior.

## Three meanings of scaling independence

1. Calibration is fixed independently of which marginal method is tested.
2. Its value is unchanged when the same global factor multiplies signal and
   observation.
3. Its value is unchanged under arbitrary positive row/column rescaling of
   the same signal and observation.

The first is the experimental control needed for comparing marginal methods.
The third is a stronger mathematical requirement. Metric invariance on an
existing pair does not mean noise can be regenerated after rescaling the
signal while leaving its scalar generating parameters unchanged.

## Metrics considered

Let mu = W H. In this discussion, X denotes an observation aligned to the
expected scale of mu. This is temporary discussion notation, distinct from
the simplex-vertex matrix X in the repository README.

| Metric | Definition | Interpretation and limitations |
|---|---|---|
| Current helper's absolute level v | mean_ij E[(X_ij-mu_ij)^2 | mu] | Mean squared absolute perturbation; equals mean conditional noise variance for unbiased models; has squared signal units. |
| Entrywise relative MSE q_entry | mean_ij E[((X_ij-mu_ij)/mu_ij)^2 | mu] | Equal weighting of fractional errors; invariant to common positive row/column factors; undefined at zero signal and can be dominated by weak entries. |
| Relative Frobenius error q_F | E[||X-mu||_F^2 | mu] / ||mu||_F^2 | Total noise energy relative to total signal energy; globally scale invariant; handles zeros if total signal energy is positive; not diagonally invariant. |
| Proposed variance-based level L | v / Var_ij(mu) | Noise variance relative to total variance across noiseless matrix entries; globally scale invariant; not diagonally invariant. |

No scalar makes noise geometry or recovery difficulty identical across models.
q_F and L weight fractional squared errors in proportion to mu_ij^2, whereas
q_entry weights them equally. This alone does not say which entries dominate
absolute noise energy: the variance pattern is constant for additive Normal,
proportional to mu for Poisson, and proportional to mu^2 for mean-aligned
multiplicative noise. NB adds a term proportional to mu^2.

Spectral perturbation measures and recovery errors can be secondary outcomes.
A single spectral calibration in a fixed reference can also preserve pairing;
it is incorrect to say spectral calibration necessarily breaks pairing.

## User's proposed variance-based formulation

The user proposed that level 1 means additional noise variance equals
Var_ij(mu), level 2 means twice it, and level 0.5 means half it.

For a fixed signal with N = mn entries, use the population variance:

    S_mu = mean_ij[(mu_ij - mean(mu))^2], with S_mu > 0.
    v = mean_ij Var_noise(X_ij | mu).
    L = v / S_mu.

Var_ij means variance across the flattened matrix around its grand mean, with
denominator N. It is not the mean within-gene across-sample variance.
L is a variance ratio; sqrt(L) is the RMS noise divided by signal SD.
It is not the noise fraction of the total observed variance.

Under conditional unbiasedness, E_noise[X_ij | mu] = mu_ij, v also equals
mean squared perturbation. For a uniformly chosen entry I and a noise draw,

    Var_{I,noise}(X_I | mu) = S_mu + v = (1 + L) S_mu.

This is not an exact identity for the empirical variance of each noisy
matrix. Its expected empirical population variance around its own mean is
S_mu + v - Var_noise(mean(X)); independent errors give Var_noise(mean(X))=v/N.
Clipping generally invalidates the conditional-unbiasedness assumption.

Suggested descriptive name: "noise-to-total-signal variance ratio", defining
"total signal variance" explicitly as variance across all noiseless entries.

## What aligning expected scales means

Remove only the known global multiplier introduced by the generating model:

| Model | Mean-aligned observation X |
|---|---|
| Poisson/NB, scalar library fraction f | V/f |
| Multiplicative V = mu exp(Z), Z ~ Normal(0,s^2) | V/exp(s^2/2) |
| Additive Normal before clipping | V |

The multiplier comes from the known model parameters, never from fitting each
noisy realization. This prevents intentional exposure changes or a lognormal
mean shift from being counted as random perturbation. It does not remove noise:
for example Var(V_ij/f | mu) = mu_ij/f for Poisson.

This correction is already included in the current helper's theoretical
calibration. It is separate from the marginal preprocessing being compared.
Clipped Normal has entry-dependent bias; no global factor removes all of it.

## Existing helper and proposed parameter inverses

Current file: `artifact/20261028_noise_grid.R`, function `find_grid_points()`.

- Matches v, with targets `100 * 2^(0:6)`.
- Pools M1 = mean(mu) and M2 = mean(mu^2) across the supplied simulations.
- Matches Poisson, multiplicative and Normal BEFORE clipping.
- NB reuses Poisson fractions at dispersions 0.01 and 0.1; it is not matched
  to the same noise level.
- Uses a 3% rounding preference with a fallback, not a strict tolerance bound.
- Reports clipped-Normal MSE separately; this includes squared bias.

For proposed level L and a chosen setup denominator S, set v = L S:

| Model | Exact parameter before rounding |
|---|---|
| Poisson | f = M1/(L S) |
| Normal before clipping | sigma = sqrt(L S) |
| Multiplicative | s = sqrt(log(1 + L S/M2)) |
| NB, scalar dispersion phi | f = M1/(L S - phi M2), requiring L S > phi M2 |

The NB level floor is phi M2/S, approached as f tends to infinity. It is not
phi under this variance-based definition. Matching NB is a separate design
change from expressing the existing settings using L.

The comparison used the mean of each matrix's population signal variance,
weighted by entry count if matrix sizes differ. Its ratio of average noise
variance to average signal variance is not the mean of per-seed ratios, nor
an exact level for every seed. Pooling entries before centering would also
include differences between simulation grand means.

## Quantitative comparison already completed

All values below summarize `artifact/20261029_noise_level_comparison.md`,
sections "Pilot signal variance and existing levels", "Illustrative replacement
levels and parameter changes", "Separate NB and clipping consequences" and
"Denominator interpretation and stability". Claude independently reproduced
the checked results. Provenance is given below.

For K=3, marker fold 5, seeds 1-10:

- Mean within-matrix signal variance S = 700.8332627.
- Existing targets 100, 200, 400, 800, 1600, 3200, 6400 correspond to nominal
  L of approximately 0.14, 0.29, 0.57, 1.1, 2.3, 4.6, 9.1.
- Relabelling those targets changes no parameters, observations or outcomes.
  Within a fixed setup, v, L and q_F differ only by constant factors.
- The seven levels 0.125, 0.25, 0.5, 1, 2, 4, 8 were an ILLUSTRATIVE alternative,
  not user-approved defaults. Compared by position with the old targets, their
  exact target variances are 12.3958% lower.
- After existing parameter rounding, achieved variance reductions range from
  9.09-13.05% for Poisson, 10.42-14.44% for pre-clipping Normal, and
  8.97-14.04% for multiplicative noise (range endpoints rounded outward).
- Example: illustrative L=1 uses target variance 700.83, compared with old
  target 800. Rounded Poisson f changes 0.05 -> 0.055; Normal SD 28 -> 26.5;
  multiplicative log-SD 0.55 -> 0.52.
- With phi=0.1, the NB floor is about 0.324: illustrative L=0.125 and 0.25
  cannot be matched. At L=1, independently matched NB fractions round to
  0.06 for phi=0.01 and 0.08 for phi=0.1.
- Normal's actual clipped MSE/S at nominal L=0.5, 1, 2 is approximately
  0.424, 0.805, 1.442. Those are MSE ratios, not pure conditional variances.
- About 97.6% of S comes from differences in gene means. At L=1, target
  noise variance is about 41.7 times the mean within-gene variance. This
  does not establish a recovery threshold or isolate mixture information.

Across the four marker folds, mean S ranges from about 693.04 to 700.42.
The mean over all 120 saved ground truths is 696.9941650. Small moment changes
can cross rounding thresholds and produce discrete parameter differences.
If identical parameters across folds are desired, compute one grid from
pooled M1, M2 and S, then reuse it. Sharing S alone is insufficient.

No recovery study was rerun. These calculations quantify targets and generator
parameters; they do not predict the magnitude, sign or qualitative stability
of differences in recovery or in paired contrasts between marginal methods.

## Claude's review and conclusions to carry forward

A fresh Advisor - Claude reviewed the formulation, code and numerical results.
Initial verdict: accept with explanatory changes. After revision and a second
check, final verdict: ACCEPT. The reviewer independently recomputed results,
its final activity was read, and the agent was archived.

Carry forward the corrected conclusions:

- Pairing does not select a denominator; scientific interpretation must do so.
- Equal noise level does not mean equal recovery difficulty.
- Total entrywise variance includes gene abundance differences. Describe it
  precisely; do not call it purely informative mixture variation.
- Relabelling and choosing different numerical targets are different actions.
- Shared calibration and fold-specific calibration answer different design
  needs. Rounding can amplify small differences in moments.
- Conditional expected per-seed levels are not realized noisy-draw errors.
- For multiplicative noise, relative variance is constant across entries;
  it is incorrect to call its relative-abundance relationship the reverse
  of Poisson's.
- Observed differences in noise patterns do not establish the cause of
  recovery differences.
- No stability prediction or bracket for finite Monte Carlo recovery
  estimates has been established.

The review accepted the formulation and comparison, not an implemented
replacement grid or a claim of universal superiority for this metric.

## Decisions still open

1. Final denominator: total entrywise signal variance as proposed, or another
   scientific target such as mean within-gene variance or signal energy.
2. Relabel the existing grid, or choose new L targets and rerun.
3. One shared grid across marker folds, or a separate grid per setup.
4. NB at matched noise levels, at matched Poisson exposure, or both as distinct
   experiments.
5. Retain the approved pre-clipping Normal convention, or explicitly change
   the target to post-clipping MSE/variance with bias handled separately.

The current helper is unchanged. A full replacement grid has not been adopted.
The mean-scale corrections already existed. Do not treat illustrative levels
or conditional recommendations as settled user decisions.

## Files and provenance

Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`.

Read in this order:

1. `README.md`, `AGENTS.md` and the recent decision record, following the
   repository's Lead startup instructions.
2. This handoff.
3. `artifact/20261029_noise_level_comparison.md`.
4. `artifact/20261029_noise_formulation_review.md`, including final verdict
   and re-review; historical findings are retained there.
5. `artifact/20261028_noise_grid.R` and `.md`.

Calculations: `artifact/20261029_noise_level_comparison.R`.
Outputs: `out/20261029_noise_level_comparison/`.
Independent verification: `out/20261029_noise_formulation_review/`.
Original review task: `artifact/handoff/20261029-0204_claude_noise-formulation-review.md`.
Decision record: `artifact/decisions.md`, entry dated 2026-10-29 about reviewing
the proposed formulation before changing the grid.

Analysis base and existing helper commit:
`29cb5265b0ad7795666f17ab26fbd317c39ff21b` in the manuscript repository.
The new calculation and review artifacts are working-tree files, not committed
at this handoff. Calculation-script SHA-256:
`81e5d9c6fb0348b40cf6a72ea6dac1ac7311a75f2854a6b0a817efde2aedc5d9`.

Ground truths: `/data/simulation_ground_truth_k3.rds`, containing K=3;
marker folds 2,5,10,100; 30 seeds per fold; 3000 by 500 matrices.
SHA-256: `78c62b71a6f6969df3e43404e65096dcd014f41e31c0d82db00563235423c522`.
The archive's generating commit is not established.

Implementation context: GeneralDualSimplex 0.29.0, package source commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`; `R/simulation.R` defines the models.
This is not proof of the supplied archive's generation provenance. The package
repository is read-only from this manuscript session.

Preserve all existing modifications and untracked files. In particular, there
are unrelated edits in AGENTS.md, the simulation helpers and other artifacts.
Current AGENTS.md also includes a file-link/formula rendering house rule;
follow it rather than repeating earlier guesses about unsupported link formats.

## Copyable starting prompt

```text
I want to continue designing a simulation study of how marginal choices affect
recovery under different noise models, with an interpretable noise-level grid.

Work as Lead in:
/workspace/dual_simplex_functional/general_dual_simplex_manuscript

Follow README.md and AGENTS.md, including the Lead startup instructions. Read:
- artifact/20261029_noise_level_session_handoff.md
- artifact/20261029_noise_level_comparison.md
- artifact/20261029_noise_formulation_review.md (final verdict and re-review)
- artifact/20261028_noise_grid.R and its .md note

The proposed level is L = mean_ij Var_noise(X_ij | mu) / S,
where mu = W H and S is the population variance across all entries of mu.
X removes only the known global mean multiplier: V/f for Poisson/NB,
V/exp(s^2/2) for multiplicative noise, and V for Normal before clipping.
For several ground truths, the reviewed comparison uses a ratio of average
noise variance to average within-matrix signal variance.

The intended interpretation is L=1 for equal noise and total entrywise signal
variance, L=2 for twice the noise variance, and L=0.5 for half. Calibrate before
preprocessing and give every marginal method the same noisy draws. Pairing
does not determine the denominator, and equal L is not equal recovery difficulty.
This metric is globally scale invariant, not invariant to arbitrary row/column
rescaling. Entrywise relative MSE was a separate option for the stronger
invariance requirement.

Claude independently reviewed the formulation and numerical comparison;
the final verdict was accept after clarifications. The existing helper remains
unchanged: it matches absolute mean noise variance, matches Normal before
clipping, and reuses Poisson fractions for NB rather than matching NB levels.
The grid 0.125,0.25,0.5,1,2,4,8 was illustrative and is NOT an approved default.
Mean-scale correction is already included in the existing calibration.

Help me settle the remaining choices: denominator, target levels versus pure
relabelling, one shared grid versus setup-specific grids, NB matching versus
shared exposure, and the Normal clipping convention. Retain the existing
pre-clipping convention as the baseline unless we explicitly change it.

Start with a concise recommendation and rationale using the reviewed evidence.
Separate settled facts from choices requiring my decision. Do not change the
helper or launch recovery experiments until we agree on the design. Preserve
existing work and cite the recorded provenance; do not infer recovery changes
from parameter changes alone.
```
