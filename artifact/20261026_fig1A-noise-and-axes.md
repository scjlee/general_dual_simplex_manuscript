# Figure 1A: stronger observation noise and axes 2/3

The user requested more visible separation between weighting methods and
axis labels Projection 2 and Projection 3, with no further reviewer.
This note supersedes the observation depth and axis naming in
`artifact/20261026_fig1A-gene-simplex.md`; its projection derivation, heatmap
selection, and metric definition continue to apply.

Starting manuscript commit: `326c9046c476ecc3f67fd99f2295fabeadb77cb2`.
GeneralDualSimplex 0.28.0 at package checkout
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, with no uncommitted R/src changes
(`figure/fig1/panelA/package_commit.txt`). The installed package code is
unchanged from the previous figure revision. The package repository was
read only.

## Choice and numerical record

`points.R` now defaults to library_size_fraction = 0.04 instead of 0.1.
GenerateMixture parameters, the latent W and H, true signal WH, seed 1,
Poisson observation model (dispersion = 0), projections and shared display
scale rule are unchanged. Lower expected counts increase relative sampling
noise. No artificial displacement of projected points is used.

Three candidate depths were tried at the same seed. The 0.02 trial made
outliers dominate the shared display range and nearly erased the triangle.
The 0.05 trial preserved the geometry; 0.04 gave a clearer visual difference
while retaining readable triangles, so it was selected for illustration.
This selection is recorded rather than treated as a new test of a general
advantage for one weighting method.

Table: oracle H RMSE by sampling fraction, rounded from the stored values.

| Sampling fraction | Uniform | Expression |
|:---|---:|---:|
| 0.10 | 0.081547 | 0.063356 |
| 0.05 | 0.129208 | 0.090295 |
| 0.04 | 0.151065 | 0.104678 |
| 0.02 | 0.216967 | 0.152904 |

Table sources: the 0.10 row is
`figure/fig1/panelA/projection_metrics.csv` at manuscript commit
`326c9046c476ecc3f67fd99f2295fabeadb77cb2`; the selected row is the updated
file at that same path. Trial outputs and logs are in
`out/20261026_fig1A_more-noise/fraction_<fraction>/` (ignored scratch).
All new rows were computed with `points.R` from the starting manuscript
revision and the package version/full commit above. The default depth and
one diagnostic field are the only changes to the R generator.

The selected values round to H oracle RMSE = 0.151 and 0.105 on the figure.
They are the H projection residuals defined in the original derivation,
not errors between the gene cloud and the dashed triangle.

## Axis labels and caption addition

The first coordinate is constant and is not displayed. The axes now read
Projection 2 and Projection 3, naming the two nonconstant dimensions used
in the plot. The previous rigid orientation is retained: each displayed
axis is a rotated coordinate within that plane, rather than an unrotated
singular vector. The rotation is applied to both the genes and triangle.

Caption addition to the original draft: “The nonconstant projection plane
(dimensions 2 and 3) is shown after rigid orientation. Observation noise is
increased to make the two weighting choices easier to compare visually.
These data are illustrative; the display was selected for clarity.” No
noise-model parameters are printed on the figure.

## Verification

- RDS comparison confirms W, H, true signal and seed are identical to the
  previous revision. Only observation depth changes the noisy data.
- `projection_metrics.csv` reports that the first coordinate differs from
  one by less than 3.3e-15, and the coordinate identity residual is less than
  6.2e-15 (bounds rounded up). Both panels retain all 500 genes, including
  60 markers and 440 background genes.
- The data generator preserves every byte outside the six data-group
  contents. The separate SVG edit changes only the four axis labels and
  two RMSE labels. Other text subtrees, attributes and positions match the
  numbered pre-edit master backup in `out/20261026_fig1A_more-noise/`.
- PNG and PDF previews were regenerated with Inkscape; the final 600 dpi
  PNG was opened and visually inspected. Query checks keep all 27 text
  objects inside the canvas, five box labels inside their boxes, and all
  1,000 gene circles inside their frames. Outliers are retained.
- A second data-generator run leaves the entire SVG byte-identical.
- No new reviewer was launched, as the user explicitly requested.

Reproduce from the repository root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelA/points.R
python3 figure/fig1/panelA/make_fig1A.py
inkscape figure/fig1/panelA/fig1A.svg --export-type=png --export-dpi=600 -o figure/fig1/panelA/fig1A.png
inkscape figure/fig1/panelA/fig1A.svg --export-type=pdf -o figure/fig1/panelA/fig1A.pdf
inkscape --query-all figure/fig1/panelA/fig1A.svg
```

As before, labels are separate master objects. If data change again, use
the printed RMSE values to update them before rendering.
