# Figure 1: representative simplices, matching oracle targets, E/F SVGs

Date: 2026-10-26. Current layout/caption note, superseding the D metric
assignment in the earlier D/E and E/F prototype notes. All simulations
remain illustrative; no manuscript recovery claim relies on these draws.

## Changes requested and files

- D title: “Representative gene simplices”. Above each projection, only
  “oracle RMSE: <value>”. Scaling labels are single lines rotated 90°,
  adjacent to the first plot column. The first column moves from x = 25 mm
  to x = 10 mm, with the label at x = 6.5 mm. Plot size stays 29.5 mm square;
  the standalone panel is now 119 × 111 mm.
- D's companion: `figure/fig1/panelD_samples/sample_simplices.png`, same
  layout and same observed draw 1, with every observed sample and known
  pure W profiles mapped into the estimated feature projection. “S” is a
  provisional supplementary panel label, not an assigned figure number.
- Following the user's correction, A and D report **W** oracle RMSE for
  gene plots; the sample companion reports **H** oracle RMSE.
- E and F now have editable SVG masters:
  `figure/fig1/panelE/fig1E.svg`, `figure/fig1/panelF/fig1F.svg`, with
  matching PNG previews. E remains W-side, F H-side, both 100 × 69 mm.
- A's existing SVG master has only its two RMSE text contents changed;
  PNG and PDF refreshed. Its layout, points, triangles and heatmaps are
  unchanged. Numbered backup: `out/20261026_fig1A_Wlabels/001/`.

Generators: `panelA/points.R` now also saves the W oracle diagnostic;
`panelA/make_fig1A.py` prints W values for checking the edited labels.
`panelD/projections.R` adds the companion sample coordinates and checks.
`panelD/make_mock_panels.R` draws D/sample PNGs and combined layout drafts;
when E/F SVG masters exist it renders their PNGs from those masters.
`panelE/make_fig1EF.py` creates E/F SVGs once, then replaces only named
data groups. Other edited objects are preserved; check axes if data change.
Combined PNGs remain R layout drafts; standalone E/F PNGs render the SVGs.

## Which errors should match?

The initial choice used the ambient profile space to assign metrics. The
user preferred assigning them to recovery of the plotted entities; this
note records that convention explicitly. Neither metric is a distance
from noisy dots to a triangle.

| Display | Oracle target | Draws represented |
| --- | --- | --- |
| A, gene projections | Original W, expression units | Poisson draw 1 |
| D, gene projections | Original W, expression units | Draw 1 in each model |
| E | Original W, expression units | Five dots; number = mean of five RMSEs |
| Sample companion | Original H, fraction units | Draw 1 in each model |
| F | Original H, fraction units | Five dots; number = mean of five RMSEs |

Thus D matches one dot in each E group, not its mean. The sample companion
matches one dot in each F group. A and D's Poisson pair match each other.
W and H errors have different units and should not be compared in magnitude.

The formulas are unchanged from
`artifact/20261026_fig1EF-oracle-png.md`, “Oracle W derivation”:
Q_W = orth(D_r⁻¹ D_a Φᵀ), W_oracle = Q_W Q_Wᵀ W;
Q_H = orth(D_b D_c⁻¹ Ψᵀ), H_oracle = H Q_H Q_Hᵀ.
RMSE is the Frobenius residual divided by the square root of the number
of true factor entries. These are unconstrained projections in original
factor units, with no clipping or normalization of the oracle.

## Companion sample geometry

Source: `figure/fig1/panelD/projections.R` →
`panelD_samples/sample_points.csv`, `simplex_vertices.csv`,
`projection_checks.csv`, `package_commit.txt`. The source model, seeds and
noise levels are unchanged from the current E/F note.

Column-normalized scaled observed samples are
F_s = colNormalize(D_r V); known pure profiles are
T_s = colNormalize(D_r W). Sample coordinates are Φ F_s and component
vertices are Φ T_s. Their first coordinate is one, so dimensions 2–3
are displayed. This is the dual construction to D's gene plot. For
noiseless signal, F_s* = T_s B_s*, where
B_s* = colNormalize(D_colSums(D_r W) H), a nonnegative column-stochastic
matrix. Thus noiseless samples are convex mixtures of the known vertices.
No vertices are estimated. Noise can put observed samples outside them.

Each cell includes all 200 samples, with an independent display range and
equal aspect. A translation and rigid rotation/reflection align component
identities; no stretching or sample selection is used. Grey: observed
samples. Green/pink/gold vertices: known pure components 1/2/3. The
legend's component colours refer to vertices, not observed sample classes.

## Caption drafts

**A, amendment.** Labels report the W oracle RMSE in native expression
units for this one illustrative draw: the error from projecting known W
into the recovered feature subspace. It is not a gene-to-triangle distance.
Replace earlier H-oracle wording; other current caption conventions remain.

**D. Representative gene simplices.** One prespecified illustrative draw
per noise model, shared across scalings. All observed genes are shown,
with component-enriched markers in green, pink and gold and background
genes in grey. Dashed: known pure component profiles projected into the
same estimated space. Labels: draw-1 W oracle RMSE, corresponding to one
dot in E; E's top numbers are five-draw means. Separate display scales,
equal aspect, no fitted vertices. Illustrative simulation, not a benchmark.

**Sample companion. Representative sample simplices.** All observed
samples from D's same matrices and scalings, mapped into the feature
projection. Grey: samples; coloured vertices: known pure W profiles
projected by the same map. Dashed lines join those vertices. Labels:
draw-1 H oracle RMSE, corresponding to one dot in F. Separate display
scales and equal aspect; no fitted vertices. Illustrative simulation for
possible supplementary placement, not a benchmark.

E/F caption drafts in `20261026_fig1EF-oracle-png.md` remain applicable;
their data and numerical summaries are unchanged. The SVG footer now says
“Illustrative simulation” and panel letters are 8 pt.

## Provenance and checks

GeneralDualSimplex 0.28.0, full package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`.
Manuscript base: `c29f61dd9936840883af47cbea1fbd4521eee36d`; this revision
is uncommitted. Source for the following numerical checks is the current
`panelA/projection_metrics.csv`, `panelD_samples/projection_checks.csv`
and E/F CSVs generated in that working state with the cited package.

- A's W values are 6.335 (uniform) and 5.777 (expression), rounded from
  its new `oracle_W_rmse` column; they equal E's Poisson draw-1 values.
  A's H diagnostic remains saved. Its simulation, coordinate, vertex,
  heatmap and provenance files reproduce byte for byte. SVG comparison
  differs only at the two RMSE text contents.
- All previous D coordinates and E/F metric/oracle/noiseless/parameter
  CSVs reproduce byte for byte. Switching labels did not change the sample
  point or vertex CSVs.
- Sample first-coordinate error is below 6.7 × 10⁻¹⁶; agreement with
  Σ Ψ is within 7.8 × 10⁻¹⁵; noiseless convex-identity error is below
  3.5 × 10⁻¹⁸. Bounds rounded up. All six companion cells have 200 samples.
- D and companion PNGs were opened after the final metric swap. Their
  text bounds fit the canvas. A's final PNG was opened, and Inkscape query
  bounds place its text within the canvas.
- Both SVG previews were rendered at 600 dpi and opened. Inkscape
  `--query-all` places all 27 E and 26 F text objects inside the canvas;
  each SVG contains 30 data dots, unique object ids and no raster images.
  Fonts are Liberation Sans, 5–8 pt; strokes 0.4–0.6 pt. Re-running the
  SVG data refresh leaves both masters byte-identical.

Backups/diagnostics: `out/20261026_fig1D_samples_v1/` and
`out/20261026_fig1A_Wlabels/`. No new reviewer was launched: these are
layout changes, the user's requested choice between existing illustrative
metrics, and illustrative sample data with no claim relying on them.
Captions label the simulations illustrative; the user previously requested
skipping review for these fixes.

Proposed house rule, 2026-10-26: name the factor targeted by every oracle
metric in the caption, and distinguish representative-draw values from
replicate summaries before comparing panels.

## Reproduction

From the repository root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelA/points.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/projections.R
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/make_mock_panels.R
python3 figure/fig1/panelE/make_fig1EF.py
inkscape figure/fig1/panelE/fig1E.svg --export-type=png --export-dpi=600 -o figure/fig1/panelE/fig1E.png
inkscape figure/fig1/panelF/fig1F.svg --export-type=png --export-dpi=600 -o figure/fig1/panelF/fig1F.png
```

A's master labels are edited by id, not overwritten by its data generator.
If A is already open in Inkscape, use File → Revert to load the changed labels.
