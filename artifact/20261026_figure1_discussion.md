# Figure 1 discussion: scaling, noise, and the variation the SVD sees

Date: 2026-10-26, rewritten at the end of the day to focus on the current
panel designs. Status: layout drafts for discussion. All data are
illustrative simulations, not benchmarks; the user plans to rerun the
analyses at the end. Package: GeneralDualSimplex 0.28.0 at commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`.
Manuscript base: `c29f61dd9936840883af47cbea1fbd4521eee36d`. Notation
([README](../README.md), Mathematical Notation): signal `V* = WH`, observed
`V`, scaled `Ṽ = D_r V D_c` with row sums `a` and column sums `b`,
bi-whitened `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`, which goes to the SVD. Equations
go in the figure legend, not in the panels (user decision).

## Message and panel sequence

Figure 1 introduces the elements of panel A one at a time and primes one
point: **both the scaling and the noise model decide where the variation sits
in `Z`, and so what the SVD works with.** Under Poisson noise, uniform
scaling gives low-count genes a larger share; under proportional noise the
pattern reverses.

| Panel | Element of A | Reader question | Status |
| --- | --- | --- | --- |
| A | Whole pipeline | What is compared? | Drawn; bi-whitening step added |
| B | Scaling | What weight does each scaling give each gene and sample? | Drawn |
| C | Bi-whitening | Where does the variation sit in `Z`, for each noise model? | Layout draft |
| D | Projection | What mixture structure survives? | Proposed |
| E | Error label | Does the difference hold across draws and noise levels? | Proposed |

D may become insets in E for a four-panel figure (open).

## A: pipeline

`figure/fig1/panelA/fig1A.svg`. One mixture `W, H` → `V* = WH` → Noise →
observed `V` → {uniform, expression} scaling → **Bi-whitening** → rank-k
projection → projected genes, with an H oracle RMSE label above each
projection (0.151 uniform, 0.105 expression;
`figure/fig1/panelA/projection_metrics.csv`). The bi-whitening box was added
on 2026-10-26 so that C can show `Z`; it is per branch because `a` and `b`
depend on the scaling. Plot scales are separate, so cloud sizes are not
compared. One fixed-seed example (500 genes, 200 samples, k = 3, Poisson at
library-size fraction 0.04), chosen for readability; its labels are not a
general ranking. In the 10-draw check below, the exposure-0.04 means were
0.153 and 0.106, so A's draw is typical for that signal.

## B: what scaling does

`figure/fig1/panelB/`; record `artifact/20261026_fig1B-rank-log-share.md`.
Each gene (500) and sample (200) of A's matrix, ranked by observed total; y
is its share of `Ṽ` (that is, `a` or `b`), log scale, separate y-ranges.
Uniform scaling is a flat line (1/500 = 0.2% per gene, 1/200 = 0.5% per
sample). Expression scaling equals the raw count share: genes 0.021–0.645%
(31-fold), samples 1.2-fold. B defines the scalings; it does not show that
either improves projection. The earlier cumulative version is archived in
`figure/fig1/panelB/archive/20261026_cumulative/`.

## C: where the variation sits after bi-whitening

`figure/fig1/panelC/`; record and caption draft
`artifact/20261026_fig1C-noise-share.md`.

**Quantity.** For each gene, its variation in `Z` beyond the trivial
singular pair: `q_g = Σ_i (Z_gi − √(a_g b_i))²`. Bi-whitening makes
`√a √bᵀ` the leading singular pair with singular value 1, the same for every
sample. Summed over genes, `Σ_g q_g = Σ_{j≥2} σ_j²`: the squared singular
values the truncated SVD ranks beyond the first. This is the bridge to D,
since the truncated SVD minimizes squared (Frobenius) reconstruction error.
`q_g` is weighted variation (correspondence-analysis inertia), not the
ordinary across-sample variance of a row; the legend must say so. It needs
only the observed `V`, so it also applies to real data.

**Display.** Three plots side by side (Poisson, proportional, normal floored
at 0), each with its own log y-scale; x = gene rank by observed total; y =
gene share of variance in `Z` (%). Five independent replicates with A's
settings (replicate r: `set.seed(r)`, then signal, then noise; replicate 1
with Poisson noise is A's matrix). Dot: mean share of the i-th ranked gene;
band: range. Uniform in orange, expression in blue.

**Noise models** on baseline `μ = 0.04 · WH`: Poisson (`ApplyNBNoise`,
dispersion 0, as in A); proportional `μ · Gamma(1/φ, 1/φ)`; normal
`max(μ + N(0, σ²), 0)`. `φ = 1/m̃`, `σ = √m̃`, with m̃ = 1.093 the median
of A's `μ`, so all three have equal relative noise at m̃ before flooring.
Flooring raises the normal model's mean above `μ`.

**Results** (`noise_share_by_rank.csv`; lowest quarter = 125 lowest-ranked
genes; an even spread gives 25%):

| Noise | Uniform | Expression |
| --- | --- | --- |
| Poisson | 51.0% | 25.0% |
| Proportional | 25.9% | 8.4% |
| Normal, floored | 47.5% | 31.7% |

At these counts 97–98% of the variation is noise: with a consistent
projected split, the signal term is 1.60–4.02% across all models, scalings
and replicates (`signal_noise_split.R`). That does not mean noise dominates
the leading singular directions.

**Why `Z` and not a simpler matrix.** Binned noise-variance shares, computed
on a wider design (3,000 genes, 400 samples, background range 1–1000,
expected variances, weights fitted on the noise-free matrix;
`out/20261026_fig1C_noise/binned_variance.R`, ignored, exploratory), lowest to
highest abundance quartile:

| Noise, scaling | Raw `V` | Scaled `Ṽ` | `Z` |
| --- | --- | --- | --- |
| Poisson, uniform | 0.4 / 2.5 / 16.9 / 80.2 | 83.1 / 14.2 / 2.3 / 0.4 | 83.1 / 14.2 / 2.3 / 0.4 |
| Poisson, expression | 0.4 / 2.5 / 16.9 / 80.2 | 0.4 / 2.5 / 16.9 / 80.2 | 25.0 / 25.0 / 25.0 / 25.0 |

Raw `V` cannot show a scaling effect (identical for both scalings).
Expression-scaled `Ṽ` equals raw and would suggest that expression scaling
is the bad choice under Poisson noise, the opposite of the outcome. Only
`Z` shows the pattern, which is why bi-whitening was added to A.

**Reviews.** Two Advisor - Codex reviews (handoffs
`20261026-0440_codex_fig1ABC-review.md`, `20261026-0510_codex_fig1C-gene-variance-review.md`):
both approve with fixes; fixes applied. The second confirmed `σ₁ = 1` is
the largest singular value and the sum identity in all 30 matrices, and
reproduced the data, SVG and PNG byte for byte.

## D (proposed): what survives projection

2×2 or 3×2 grid, noise model × scaling, in panel A's style but on H: true H
in grey and oracle-projected H in colour, on identical fixed contrasts of
the original H coordinates, paired observations within a row. The H oracle
RMSE is then literally the grey-to-colour gap, which links C (what the SVD
sees) to E (the error). "Oracle" means the projection of the known H; no
simplex vertices are estimated. Suggested by the first independent review;
close to panel B of the user's conceptual mock (`/data/figure1_mock.png`).

## E (proposed): does it hold?

Paired H oracle RMSE, both scalings on the same observed matrix: Poisson
against exposure; proportional against φ (exposure would be flat by
construction, since both scalings ignore a constant factor and the noise is
relative); normal against σ. Noiseless reference. Suggested minimum: 10
independent signals × 5 paired draws, at least three levels per model;
include designs with low- versus high-abundance distinctive genes and
unequal sample depths. Weights refitted per draw.

**Evidence so far (one signal, exploratory).** Panel A's signal, 10 paired
draws per setting (`out/20261026_fig1C_explore/noise_models.R`, ignored):
expression had lower RMSE in all 40 Poisson draws (exposures 0.01–4); uniform
had lower RMSE in all 30 proportional draws (φ 0.05–0.5). Normal noise is
untested. This is consistent with the reversal in C but is one signal, not
a result.

## Open decisions

1. Axis wording in C: keep "variance" with the weighted definition in the
   legend, or use "variation".
2. D as its own panel or as insets in E (five versus four panels).
3. Whether normal noise stays in C, D and E, and whether proportional noise
   is an equal partner or a labelled control (its levels are matched to
   Poisson only at the median count).
4. Final simulation design for the user's rerun (A's settings or a wider
   background range), applied to all panels.
5. Run and review the replicated D/E experiment before any claim about
   projection quality.

## History

Earlier directions are kept in Git (this file at `c29f61d` and before) and
in `artifact/20261026_fig1C-narrative-options.md`: a cumulative B; `Z`-free
C options (per-gene reliability against B's weights, relative noise against
expected count, displacement of projected gene points); noise-share bars in
`Z`; and noise variance rather than total variation. They were replaced
because they either avoided the matrix the SVD sees or measured noise alone.
The decision log (`artifact/decisions.md`, 2026-10-26 Figure 1 entries)
records each change.
