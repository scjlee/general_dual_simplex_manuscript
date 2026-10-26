# Figure 1C: where the variance sits after bi-whitening (layout draft)

Date: 2026-10-26. Status: layout draft for discussion; illustrative
simulations, not a benchmark. The user plans to rerun the analyses at the
end. Equations go in the figure legend, not in the panels.

## Files

`figure/fig1/panelC/`: `noise_share.R` (data) → `noise_share_by_rank.csv`;
`make_fig1C.py` (SVG master `fig1C.svg`, preview `fig1C.png`);
`package_commit.txt`. GeneralDualSimplex 0.28.0 at package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`.
After the first hand edit, `fig1C.svg` is the master; the generator replaces
only the groups `band_<model>_<scaling>` and `points_<model>_<scaling>`.

## What is plotted

- Five independent replicates with panel A's simulation parameters (500
  genes, 200 samples, k = 3, 20 markers per component, marker fold 5,
  profile spread 0.2, default level ranges). Replicate r calls
  `set.seed(r)`, simulates the signal, then the noise. Replicate 1 with
  Poisson noise equals panel A's observed matrix (asserted in the script).
- Baseline `μ = 0.04 · WH`. Noise models: Poisson (`ApplyNBNoise`,
  dispersion 0, as in panel A); proportional, `μ · Gamma(1/φ, 1/φ)`;
  normal, `max(μ + N(0, σ²), 0)`. `φ = 1/m̃`, `σ = √m̃`, where
  m̃ = 1.093 is the median of panel A's `μ`. The three models have equal
  relative noise at m̃ **before flooring only**. Flooring raises the normal
  model's mean above `μ` (1.172 at m̃) and lowers its variance (0.837 vs
  1.093), per the reviewer's calculation.
- Quantity (user, 2026-10-26: "variance of genes, not noise", to link with
  the SVD's L2 objective in panel D): **each gene's variance in `Z`**, signal
  and noise together, as the SVD sees it. In each replicate and scaling the
  scaling is fitted on the observed `V`. `Z = D_a^(-1/2) Ṽ D_b^(-1/2)` has the
  trivial leading singular pair `√a √bᵀ` with singular value 1 (asserted in
  the script for replicate 1). Gene g's variance is
  `Σ_i (Z_gi − √(a_g b_i))²`; summed over genes it equals `Σ_{j≥2} σ_j²`,
  the L2 budget left for the non-trivial SVD dimensions. A gene's share is
  its variance over that total. It needs only the observed `V`.
  History: the first draft plotted one draw's squared noise
  `Σ_i (l_g (V_gi − μ_gi) t_i)²`; a second, unreviewed version plotted the
  noise variance `l_g² Σ_i t_i² Var(V_gi)`. Both were replaced.
- "Variance" is weighted variation (correspondence-analysis inertia; Greenacre,
  *Tying up the loose ends in simple correspondence analysis*, sections 2
  and 4, flagged by the reviewer): `q_g = a_g Σ_i (p_gi − b_i)²/b_i` with
  `p_gi = Ṽ_gi/a_g`, the b-weighted variance of `Z_gi/√b_i` about `√a_g`. It
  equals the ordinary across-sample variance of a row only when `b` is
  uniform.
- At these settings the variation is mostly noise. With `P = I − uuᵀ`,
  `Q = I − vvᵀ`, `u = √a`, `v = √b`, signal `S = D_l μ D_t` and perturbation
  `N = D_l (V − μ) D_t`: `‖Z − uvᵀ‖² = ‖PSQ‖² + ‖PNQ‖² + 2⟨PSQ, PNQ⟩`. Over all
  three models, both scalings and five replicates the signal term is
  1.60–4.02%, the perturbation term 96.92–98.45% and the cross term −1.04 to
  +0.16% (`figure/fig1/panelC/signal_noise_split.R` →
  `signal_noise_split.csv`; matches the reviewer's diagnostic exactly). For
  floored normal noise the perturbation includes the flooring bias. Noise
  dominating the total does not mean it dominates the leading singular
  directions.
- x: gene rank by observed total within each replicate (ranks condition on
  the noise). Dot: mean over replicates of the share of the i-th ranked
  gene. Band: min–max over replicates.

## Values (from `make_fig1C.py` output on `noise_share_by_rank.csv`)

| Noise | Scaling | Mean share range | Lowest quarter of ranks |
|---|---|---|---|
| Poisson | Uniform | 0.0344–0.99% | 51.0% |
| Poisson | Expression | 0.167–0.235% | 25.0% |
| Proportional | Uniform | 0.152–0.295% | 25.9% |
| Proportional | Expression | 0.0289–0.706% | 8.4% |
| Normal, floored | Uniform | 0.0176–0.631% | 47.5% |
| Normal, floored | Expression | 0.0781–0.291% | 31.7% |

All 15 runs kept 500 genes; uniform balancing converged in all 15.

## Caption draft

**C, Where the variance sits after bi-whitening.** Each gene's share of the
variance in the bi-whitened matrix `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`, against its
rank by observed total, for three noise models. Gene g's variance is its
weighted variation (inertia) `Σ_i (Z_gi − √(a_g b_i))²`, the squared size of
its row after removing the trivial singular pair; it is not the ordinary
variance across samples. The genes' variances add up to `Σ_{j≥2} σ_j²`, the
squared singular values beyond the first that the truncated SVD ranks. Dots: mean over five independent
simulated replicates of the i-th ranked gene; bands: range. Noise levels are
matched at the median expected count before flooring. Illustrative
simulation, not a benchmark. Under Poisson noise, uniform scaling gives
low-count genes a larger share of the variance; expression scaling spreads
it evenly. The pattern reverses under proportional noise. At these counts
97–98% of the variation is noise. The panel shows allocation within each
scaling; it does not show that one scaling recovers H better.

## Review

Advisor - Codex, 2026-10-26 (`artifact/handoff/20261026-0440_codex_fig1ABC-review.md`,
findings in ignored `out/20261026_fig1ABC_review_codex/review.md`): approve
with fixes. Applied: the realized quantity was relabelled "squared noise" (later
replaced by the variance above, which needs its own review); matching stated as before flooring with `μ` as the
pre-floor baseline. Data reproduced byte for byte by the reviewer. The
Inkscape renderer was written after the review; it draws the reviewed CSV
unchanged.

Resolved (user, 2026-10-26): plot each gene's variance in `Z` (signal and
noise), to link with the SVD's L2 objective in panel D.

Second review, Advisor - Codex, 2026-10-26
(`artifact/handoff/20261026-0510_codex_fig1C-gene-variance-review.md`; report in
ignored `out/20261026_fig1C_gene_variance_review/review.md`): approve with two
fixes, both applied: define "variance" as weighted variation (inertia), and
replace the mixed-definition 2.4%/98% ratios with the consistent split above.
It confirmed `σ₁ = 1` is the largest singular value (Cauchy–Schwarz) and the
identity `Σ_g q_g = Σ_{j≥2} σ_j²` in all 30 matrices; CSV, SVG and PNG
reproduce byte for byte. Allowed bridge to D: the truncated SVD minimizes the
squared Frobenius reconstruction error; `q_g` splits the variation beyond the
trivial pair among genes. It is not a measure of recovery accuracy.
Open (user): keep "variance" with this definition, or label "variation".
