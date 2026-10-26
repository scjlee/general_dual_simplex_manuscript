# Figure 1A: noisy gene simplex and mixed-sample heatmaps

This revision follows the user's 2026-10-26 instructions. The SVG remains the
master; editorial changes were made by object id, without rebuilding the
whole document. Numbered backups are in `out/20261026_fig1A/`.

## Caption draft

**A. One mixture, two projection geometries.** Illustrative simulated linear
mixtures share the same true signal V* = WH and observed counts V. A generic
noise step represents the observation process. The heatmaps show selected
mixed samples; all three components contribute to each sample. W shades show
relative profiles within each gene; H shades show fractions on a linear
zero-to-one scale. Signal and observed heatmaps share a per-gene shade scale
after adjusting the observed values for the known sampling depth, so shades
do not represent absolute counts.

Each projection shows only noisy observed gene profiles, with markers for
components 1, 2 and 3 in green, pink and gold, and background genes in grey.
The dashed triangle joins pure component profiles projected into the same
estimated space, using scaling weights estimated from the noisy matrix.
Markers are enriched rather than perfectly component-specific. The pure
vertices represent ideal profiles; no simulated gene has a pure profile. Rigid rotation/reflection and
translation orient the components consistently; both plots have equal aspect
and share one display scale. The H oracle RMSE above each plot measures
how far the true H lies from the estimated sample subspace. It is not a distance between
the plotted genes and the triangle. These illustrative projections do not
establish a general ranking of weighting methods.

## Data and implementation provenance

Starting manuscript commit: `b009b90b0ef6ec4092fc8af9c59b88bbcd0581f3`.

Package: GeneralDualSimplex 0.28.0; checkout
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no uncommitted `R/` or `src/`
changes. Those directories are unchanged since
`156152b445d9e511e3bcf0080d8344b38fd2122b`, the commit recorded when the
package was installed. The installed GenerateMixture and ApplyNBNoise
function bodies (deparsed) match the current source. The package repository
was read only.

Source model: package `.ai/bench/20261022_space-distortion.R` and
`.ai/decisions.md`, entry “2026-10-22 — Marginal-distortion benchmark:
principal angles and oracle RMSE lead; target is RNA fractions after depth
normalisation”, at package commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. These inform the simulation and
retained metric, not an experimental claim for the new gene plots.

`figure/fig1/panelA/points.R` runs the installed package from the manuscript
root. It retains GenerateMixture(500, 200, 3, n_marker = 20, marker_fold = 5,
profile_spread_sd = 0.2), seed 1, and ApplyNBNoise(dispersion = 0,
library_size_fraction = 0.1). The other GenerateMixture defaults are those
in the cited package source: alpha = 1, marker_range = c(10,100),
background_range = c(10,100), cell_size = rep(1,3), and
marker_spread_sd = profile_spread_sd. This particular observation model has
E[V] = 0.1 V*. The figure keeps the label generic to allow discussion of
other observation models; no new model has been evaluated.

Outputs and roles:

- `simulation.rds`: W, H, V*, observed V and explicit non-default parameters.
- `gene_points.csv`: all nonzero observed genes projected under each scaling.
- `simplex_vertices.csv`: the projected true pure component profiles.
- `projection_metrics.csv`: oracle H errors, coordinate identity errors,
  noiseless convex identity errors and gene counts.
- `heatmap_samples.csv`: selected sample ids and their actual fractions.
- `tiles.csv`: displayed tile intensities and original raw values. Historical
  X/Y keys mean the signal/observation heatmaps, independent of README's X.
- `package_commit.txt`: package checkout, installed version and dirty status.

The earlier `points_frac0.1_seed1.csv` is retained as historical data for the
previous H-oracle plot; the new generator does not read it.

## Projection derivation

Use README's notation, with scaling fitted to the noisy observed V:

Ṽ = D_r V D_c,  a = Ṽ 1,  b = Ṽᵀ 1,
Z = D_a^(-1/2) Ṽ D_b^(-1/2) = Sᵀ Σ R,
Ψ = R_(1..k,*) D_b^(-1/2),  Φ = S_(1..k,*) D_a^(-1/2).

The normalized noisy gene profiles are V_ss = D_a^(-1) Ṽ. Row scaling
cancels, giving rowNormalize(V D_c). Their retained coordinates are

C = V_ss Ψᵀ = Φᵀ Σ_(1..k,1..k).

Indeed, V_ss Ψᵀ = D_a^(-1/2) Sᵀ Σ R R_(1..k,*)ᵀ;
orthonormality selects the first k singular dimensions. The first coordinate
is one; dimensions 2 and 3 give the plotted plane before rigid orientation.

Let h = H c and H̃ = D_h^(-1) H D_c. These pure profiles give the vertices
X = H̃ Ψᵀ. With V* = WH, its row-normalized scaled profiles satisfy

rowNormalize(V* D_c) = B* H̃,
B* = D_(W h)^(-1) W D_h.

B* is nonnegative and has row sums one. Thus noiseless genes are convex
combinations of the same pure vertices after projection. The scalar sampling
depth cancels in row normalization. This establishes the interpretation of
the dashed triangle; noisy genes need not remain inside it. No points are
removed for being outside.

Each triangle's centroid is subtracted from its vertices and gene points.
An orthogonal Procrustes transform (reflection allowed) aligns the true
component identities to a fixed reference orientation. No anisotropic
stretch, shear, or point-cloud fit is used. Both panels then use one shared
range, including every point and vertex, with equal coordinate scales on
both axes. The axes are labelled Projection 1/2 because rotation mixes the
original two GSVD dimensions. The two weighting methods define different
coordinate metrics; the shared display scale does not make their distances
an absolute measure of estimation error.

## Oracle metric and heatmap selection

The existing oracle H metric is retained, from the same observed data:

Q = orth(D_b D_c^(-1) Ψᵀ),  P = Q Qᵀ,
H_oracle = H P,
RMSE_H = ||H - H_oracle||_F / sqrt(k n).

D_b D_c^(-1) Ψᵀ has dimensions n by k. This multiplication order corrects
a transposition error in the planning handoff; the executable code always
used the dimensionally correct form. The label explicitly names H to avoid
confusing this sample-side metric with gene-point dispersion.

Heatmaps use two marker rows per component and two background rows. The
eight sample columns are closest available matches to fixed interior targets
listed in `points.R`, among samples with every fraction at least 0.1. This
selection applies only to the heatmaps. H uses untransformed fractions;
W is divided by each row maximum. V* and V/0.1 share the maximum within each
displayed gene across both heatmaps. No per-row minimum is subtracted, so
low-variation background is not expanded to fill the grayscale range.

## Verification and review

Numerical source: `figure/fig1/panelA/projection_metrics.csv` and
`heatmap_samples.csv`, generated by `points.R` using the package provenance
above. These are illustrative calculations, not benchmark measurements.
Each panel contains all 500 observed genes (60 markers and 440 background).
Oracle H RMSE rounds to 0.082 (uniform) and 0.063 (expression). The coordinate
identity residual is below 2.1e-14 and the noiseless convex identity residual
is below 5.3e-18 (upper bounds rounded up). The displayed H fractions range
from about 0.123 to 0.652 and each sample's fractions sum to one.

Commands (from the repository root):

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelA/points.R
python3 figure/fig1/panelA/make_fig1A.py
inkscape figure/fig1/panelA/fig1A.svg --export-type=png --export-dpi=600 -o figure/fig1/panelA/fig1A.png
inkscape figure/fig1/panelA/fig1A.svg --export-type=pdf -o figure/fig1/panelA/fig1A.pdf
inkscape --query-all figure/fig1/panelA/fig1A.svg
```

The renv sandbox setting avoids a read-only cache warning; R still runs in
this repository's renv with the installed package. A second R run reproduced
all seven data/provenance files byte-for-byte. A second generator run left
the entire edited SVG byte-identical. Query checks place all 27 text objects
inside the canvas and all five box labels inside their boxes. Both H oracle
RMSE labels sit above their plots. All 1,000 plotted gene circles fit inside
their frames, including their radii; no clipping or outlier suppression is
used. PNG and PDF previews were refreshed, and the PNG was opened and
visually inspected. Raw checks are in `out/20261026_fig1A/`.

Independent review: Advisor - Claude, profile unchanged from Paseo,
agent `4a39974b-1fcb-40c2-80c1-8d439afd61cf`, workspace
`wks_fac28d65ea0e3234`, approved the implementation after checking the
formulas, data, and opened PNG. The final review found no mathematical,
evidence, or data errors and no unresolved scientific choice. Its minor
wording and legibility findings were addressed: the caption now names the
pink marker colour, uses “grey” consistently, defines the metric as a
projection residual, and the legend uses darker numerals and calls the
outline a pure component triangle. Point colours and data are unchanged.
The review was read via `get_agent_activity` and the agent was archived.

Proposed house rule, 2026-10-26: dimension-check every matrix product copied
into a handoff or caption against its executable form before sending it.
