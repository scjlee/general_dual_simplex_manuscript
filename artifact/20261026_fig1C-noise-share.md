# Figure 1C: where the noise sits after bi-whitening (layout draft)

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
- Quantity: **realized squared perturbation**, not a variance. In each
  replicate and scaling, the scaling is fitted on the observed `V`; the
  same fitted weights transform `V − μ`:
  `N = D_l (V − μ) D_t`, `l = r/√a`, `t = c/√b` (the noise part of
  `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`). A gene's share is its row sum of `N²`
  over the total. For floored normal noise `V − μ` includes clipping bias.
- x: gene rank by observed total within each replicate (ranks condition on
  the noise). Dot: mean over replicates of the share of the i-th ranked
  gene. Band: min–max over replicates.

## Values (from `make_fig1C.py` output on `noise_share_by_rank.csv`)

| Noise | Scaling | Mean share range | Lowest quarter of ranks |
|---|---|---|---|
| Poisson | Uniform | 0.034–1.0% | 51.3% |
| Poisson | Expression | 0.169–0.228% | 25.1% |
| Proportional | Uniform | 0.157–0.266% | 25.3% |
| Proportional | Expression | 0.0247–0.725% | 8.2% |
| Normal, floored | Uniform | 0.015–0.672% | 49.6% |
| Normal, floored | Expression | 0.0702–0.32% | 33.8% |

All 15 runs kept 500 genes; uniform balancing converged in all 15.

## Caption draft

**C, Where the noise sits after bi-whitening.** Each gene's share of the
squared noise in the bi-whitened matrix `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`, against
its rank by observed total, for three noise models. Squared noise is
`‖D_l (V − μ) D_t‖²` per gene, with `l = r/√a` and `t = c/√b` fitted on the
observed matrix. Dots: mean over five independent simulated replicates of
the i-th ranked gene; bands: range. Noise levels are matched at the median
expected count before flooring. Illustrative simulation, not a benchmark.
Under Poisson noise, uniform scaling places more squared noise on low-count
genes; expression scaling spreads it evenly. The pattern reverses under
proportional noise. The panel shows allocation within each scaling; it does
not show that one scaling has less total noise or recovers H better.

## Review

Advisor - Codex, 2026-10-26 (`artifact/handoff/20261026-0440_codex_fig1ABC-review.md`,
findings in ignored `out/20261026_fig1ABC_review_codex/review.md`): approve
with fixes. Applied: y-axis "Gene share of squared noise (%)" and the
definition above; matching stated as before flooring with `μ` as the
pre-floor baseline. Data reproduced byte for byte by the reviewer. The
Inkscape renderer was written after the review; it draws the reviewed CSV
unchanged.

Open (user): keep the realized squared-perturbation share, or estimate
conditional variance from repeated draws of one fixed signal (a different
target).
