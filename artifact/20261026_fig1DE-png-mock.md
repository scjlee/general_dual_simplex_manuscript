# Figure 1D–E: PNG layout prototypes

Historical first D/E prototype. E is superseded by W-side E and H-side F
in `artifact/20261026_fig1EF-oracle-png.md`; that note describes the current
files. The original own files are backed up in `out/20261026_fig1EF_v1/`.

Date: 2026-10-26. Illustrative simulations for layout discussion, not
benchmarks. No manuscript claim or general ranking relies on these draws.
The user asked for gene simplices in D and five draws per noise/scaling pair
in E, with PNG output only. This replaces the proposed H overlays in D;
the broader E experiment in `20261026_figure1_discussion.md` remains a
proposal for the final rerun. Existing A–C files are unchanged by this task.

## Files and provenance

- `figure/fig1/panelD/fig1D.png`: representative gene projections, three
  noise columns × two scaling rows; draw 1 for every cell.
- `figure/fig1/panelE/fig1E.png`: five paired draws per model; shared y-axis.
- `figure/fig1/fig1DE_mock.png`: combined layout, with matching noise columns.
- `figure/fig1/panelD/projections.R`: produces both panels' data.
- `figure/fig1/panelD/make_mock_panels.R`: draws PNGs directly with R/grid,
  600 dpi, Liberation Sans. No SVG, including temporary SVGs, is generated.
- D input tables: `gene_points.csv`, `simplex_vertices.csv`; E input tables:
  `projection_metrics.csv`, `oracle_H.csv`, `noiseless_metrics.csv`,
  `noise_parameters.csv`. The plots can be redrawn from the CSVs alone.

Manuscript starting commit: `c29f61dd9936840883af47cbea1fbd4521eee36d`;
these prototypes are uncommitted work on top of that base and the existing
uncommitted C discussion. Package: GeneralDualSimplex 0.28.0, commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`.
Both panel directories contain `package_commit.txt`.

The simulation/noise settings are copied from
`figure/fig1/panelC/noise_share.R`; gene geometry and H oracle metric are
copied from `figure/fig1/panelA/points.R`. The latter's original source is
package `.ai/bench/20261022_space-distortion.R` at the package commit above,
as documented in `artifact/20261026_fig1A-gene-simplex.md`, sections
“Projection derivation” and “Oracle metric and heatmap selection”. The
package reconstruction map is `R/dso-projection.R`,
`DSProjection$reconstruct_H_tilde`, at the same package commit.

## Design and calculation

As in C, draw r calls `set.seed(r)`, simulates a fresh W and H, then noise.
The signal is regenerated from the same seed for every noise model. Both
scalings within a draw use the identical observed matrix, with weights
refitted to it. Thus the five draws vary both signal and noise; they are
not five noise draws conditional on one signal. There are 15 observed
matrices, each projected with both scalings, giving 30 RMSE values.

Inputs: A's `simulation.rds` parameters: 500 genes, 200 samples, k = 3,
20 markers per component, marker fold 5, profile spread 0.2, and library
fraction 0.04. Other GenerateMixture defaults are unchanged: marker and
background ranges 10–100, cell sizes 1, alpha 1, marker spread 0.2.
Baseline μ = 0.04 WH. Models, as in C:

- Poisson: `ApplyNBNoise(dispersion = 0, library_size_fraction = 0.04)`.
- Proportional: μ × Gamma(shape = 1/φ, rate = 1/φ), φ = 1/median(μ_A).
- Normal, floored: max(μ + N(0, σ²), 0), σ = sqrt(median(μ_A)).

Exact parameters are saved in `panelE/noise_parameters.csv`; the rounded
values are median μ_A = 1.092664, φ = 0.9151943, σ = 1.045306. Noise levels
match at that count before flooring only. Flooring shifts the normal
model's expectation above μ. E compares the single settings used in C;
it does not sweep exposure or noise level.

For D, fit scaling and rank-3 SVD to observed V. Normalized observed gene
profiles F = rowNormalize(V D_c) and true pure component profiles
T = rowNormalize(H D_c) are mapped by the same Ψᵀ. Display dimensions 2–3
of F Ψᵀ and T Ψᵀ after translating the triangle centroid and applying the
same rigid rotation/reflection as A. Each plot fits all points and vertices
with equal aspect and an independent display range. No simplex vertices
are fitted, and no genes are selected for visual appearance. Draw 1 is
chosen in advance, not selected on error. Marker colours match A.

For E, the package's scaled H reconstruction map is X Ψ D_b. Undoing
sample scaling D_c makes its row space span(Ψ D_b D_c⁻¹). In unscaled H
coordinates, let A = D_b D_c⁻¹ Ψᵀ (n × k), Q = orth(A), and
H_oracle = H Q Qᵀ (k × n). The reported quantity is

`RMSE_H = sqrt(mean((H − H_oracle)^2)) = ||H − H_oracle||_F / sqrt(k n)`.

This is the existing metric from A. It is the unconstrained least-squares
projection of the known H, with no nonnegativity clipping or fraction
renormalization. It measures retained sample subspace, not distances from
gene dots to D's triangle. D is a qualitative view; E supplies the H error.

## Caption drafts

**D. Gene simplex after projection.** Representative illustrative draw 1
under each noise model and scaling, with the same signal across models
and the same observed matrix across the two scalings. Dots: all observed
genes; component-enriched markers in green, pink and gold, background in
grey. Dashed: known pure component profiles mapped into the same estimated
space, not an estimated simplex. Display scales are separate, with equal
aspect. Labels report draw-1 H oracle RMSE (ringed in E), which measures
sample-subspace error and is not a gene-to-triangle distance. The Poisson
pair reproduces A.

**E. H oracle error across five paired draws.** Five independent signal
and noise draws at C's single noise settings. Each draw's signal is shared
across all three noise models; its observed matrix is shared by both scalings.
Dots: individual H oracle RMSEs; grey lines connect the same draw's two
scalings. Short bars and numbers above each plot: arithmetic mean RMSE
over the five draws. Dark rings mark draw 1, shown in D. Shared y-axis.
The noise-free RMSE is below 5 × 10⁻¹⁶ in every draw (not drawn). This
noise-free check is shared by the models because their baseline μ is shared.
The oracle is an unconstrained least-squares projection of known H into
the recovered sample subspace. Its entries may be negative and its columns
need not sum to one; no vertices are estimated. These are illustrative
simulations for layout, not benchmarks or uncertainty estimates for a
general ranking.

## Values and verification

Source for the table: `figure/fig1/panelE/projection_metrics.csv`, generated
by `panelD/projections.R` in this uncommitted manuscript working state,
base `c29f61dd9936840883af47cbea1fbd4521eee36d`, using GeneralDualSimplex
0.28.0 at `af56ff97da8e38af7c304513c5d26f1c2ff0c910`.

| Noise | Mean uniform H RMSE | Mean expression H RMSE |
| --- | --- | --- |
| Poisson | 0.15350435 | 0.10341627 |
| Proportional | 0.10231862 | 0.16368048 |
| Normal, floored at 0 | 0.14640282 | 0.09947461 |

Independent arithmetic recalculation in Python from the saved 600 true and
oracle H entries per projection agrees with all 30 stored RMSEs to within
5.3 × 10⁻¹⁶. Draw-1 Poisson V matches A with zero difference; its D gene
coordinates and vertices match A's CSVs with zero difference. Every D cell
has all 500 genes, and all 15 uniform balancing runs converged. Maximum
oracle residual orthogonality error is below 2.0 × 10⁻¹⁵, and agreement with
a direct least-squares solve is within 6.7 × 10⁻¹⁶. The maximum noiseless
RMSE in `panelE/noiseless_metrics.csv` is below 4.7 × 10⁻¹⁶. Bounds are
rounded up. These are numerical checks of the illustrative calculations.

The combined PNG was opened and inspected. A first rendering incorrectly
combined models because a loop variable and a data column shared the name
`model` inside R's `subset()`. The filter was replaced with explicit
data-frame indexing before final rendering; correct model counts and
draw-specific RMSEs were checked in the render log.

R/grid text bounds also place all 23 D labels and all 26 E labels inside
their canvases (`out/20261026_fig1DE_checks/text_bounds_D.csv` and
`text_bounds_E.csv`). `git diff --check` passes.

Proposed house rule, 2026-10-26: use explicit data-frame indexing when a
plot loop variable shares a column name; check group counts before reading
the figure.

## Independent review

Advisor - Claude, agent `a8cdf866-0a3e-494a-8015-c61c0c2bddc4`, workspace
`wks_eae2eb8dafb28fa0`, approved the mathematics, data and plotting, with
minor caption/text fixes. Handoff:
`artifact/handoff/20261026-0526_claude_fig1DE-png-review.md`; full review:
`out/20261026_fig1DE_review/review.md`. The reviewer independently
regenerated non-Poisson cells via the package reconstruction map and a
different solver; checked seeds, pairing, all saved H errors and means;
compared Poisson draw 1 with A; and opened the combined PNG.

Applied wording fixes: label D's errors as draw 1 and link them to E's rings;
name their sample-subspace meaning on D; say E's signal is also shared
across models; state that the oracle is unconstrained; replace the undrawn
noise-free-reference wording with its bound in the caption; and label the
triangle “True components, projected”. D keeps its RMSE labels to match A,
with the explicit distinction from gene distances. Panel letters remain
10 pt to match A/C in these PNG prototypes; reduce to the repository's
5–8 pt range at the SVG stage. No data changed after review. The reviewer's
last message was read with `get_agent_activity`, and the agent was archived.

Reproduce from the manuscript root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/projections.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/make_mock_panels.R
```
