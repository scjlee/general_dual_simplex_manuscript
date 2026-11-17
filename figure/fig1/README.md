# Figure 1 working draft

Open **figure1.svg** in Inkscape. It is the editable single-page master;
figure1.pdf is the PDF preview and figure1.png is the 600 dpi raster preview.
The page is 180 × 200 mm. Display panels a–h contain only the panels selected in the
supplied outline. The long slide captions and definitions are kept separately
in reference/outline-text.txt, not packed into the artwork.

## Files and editing

- figure1_components.Rmd: common theme/geom settings at the top; panel-specific
  labels and styling in each plot chunk. It also exports the optional log-SNR plot.
- render.R, export_helpers.R, simulation_helpers.R: report runner, file export/
  provenance only, and the unchanged simulation-reader functions. The export
  helper does not alter plot labels, themes, layers or geometry.
- panelB/generated/ through panelG/generated/: individual editable SVG plots.
- panelB/input_data.rds through panelG/input_data.rds: compact plotted inputs.
- panelA/fig1A.svg and panelB/fig1B_schematic.svg: existing schematic masters;
  these have not been edited. The copy in figure1.svg is editable independently.
- package_commit.txt in panels C–G, results_package_commit.txt in panel B:
  installed package version, current package commit, and source-tree status.
  The older panel B package_commit.txt continues to describe its schematic.
- reference/: preserved outline PDF, original Rmd, artwork guide and inspection
  previews. Source simulations remain at data/figure1/ to avoid duplicating the
  large supplied archive. The originals in data/ are unchanged.
- render/: logs, intermediate R/Markdown and verification results.
- review.md: independent scientific/panel-selection review, when completed.

Rerun from the repository root in its renv:

```sh
Rscript figure/fig1/render.R
python figure/fig1/assemble.py
inkscape figure/fig1/figure1.svg --export-type=pdf
inkscape figure/fig1/figure1.svg --export-type=png --export-dpi=600
```

Rerendering overwrites the generated individual SVGs. The assembler replaces
only groups named data-panelB-… through data-panelG-… in the master. It preserves
page geometry, panel placement, schematic edits and surrounding annotations.
Edits inside those generated groups will be replaced; save a numbered backup
before regenerating after hand edits. Edit the outer groups to move panels.

## Content and limits

The selected examples, data filters, formulas, metrics and seeds follow the
original Rmd. The feature-simplex examples use seed 17 and noise level 1/2,
with the noiseless baseline. D and the share plots in E use noise level 1/4.
Sample-simplex plots, correlation-error alternatives, variance-ratio and
spectral-gap alternatives, error-scatter alternatives, disabled blocks and the
installation/sanity-check block were removed. F uses the singular-value ratio,
as shown in the outline, not the unused gap plot.

Plots export directly through svglite with real text. Point layers in B's
feature simplices and D's rank plot are embedded rasters at 1200 dpi, following
the Rmd changes in commit ce1218e54d983fa0f63ff2c5d52ffc4c741414ac. Axes, labels,
triangles, ribbons and the remaining plots stay vector. The existing
schematics and their matrix/cloud values are illustrative; experimental plots
use the supplied saved simulations. No new simulations were run. Caption
claims in the supplied outline have not been established by this artwork task.
The archive records package version 0.38.0 but not its generating commit.

The supplied artwork guide recommends 180 mm width, 5–7 pt sans-serif text,
RGB and editable vector output. Its maximum two-column height is 225 mm
for a caption under 50 words; rows e and f were shortened by 20% and
30% on 2026-11-13 (45 → 36 mm and 44 → 30.8 mm), and rows c/d were set to
38.7 mm, giving the 200 mm page. This is a working layout; submission height must
be revisited with the final caption length. Definitions and detailed legends
remain in the companion reference text. Figure schematics use the existing
Liberation Sans font, which is metrically compatible with Arial.

The B schematic shows the original matrix titles: W (profiles), H (proportions),
V* (true signal), ε (noise) and V (observed data). The axis labels in A read
"scaled sample₁" and "scaled feature₁" (and ₂); they denote the scaled
expression coordinates. The B feature simplices are exported at 17.9 × 21.5 mm.
Their seed and noise level are given in caption_notes.md, not in the artwork.

Panel titles are not in the artwork; they go in the legend. Each panel label
sits beside its content, at the top of the row, and is drawn last in its layer
so the plots' white backgrounds do not cover it. Rows are separated by 2.5 mm.

On 2026-11-13, panels a and b were re-laid out in figure1.svg only, following the
user's spec: A is compacted horizontally and B is wider. Later that day the
panel titles were removed and every row moved up and grew into the freed space.
The previous masters are backups/figure1-005.svg and figure1-006.svg. A fresh
assembly from the schematic sources would not reproduce the rescaled planes, the
moved pipeline row and axis labels, or the moved B matrices.
The noiseless model is labelled “∅”, including the narrow strips in C, F and G;
B's pure-signal example title reads “∅ (none)”. Noise-level ticks still read “0”. Liberation Sans lacks ∅, so the
symbol alone uses DejaVu Sans through ggtext; other labels use Liberation Sans.
C and G share RMSE limits separately for W and H, calculated from the combined
plotted values and zero. E's left, middle and right plots are 92, 43 and 35 mm
wide, respectively, with 3 mm gaps.

## Editable typography and optional plot

The setup chunk in figure1_components.Rmd contains the shared theme and geom
defaults. All plot-specific text, tick angles, line widths and point sizes are
specified in the corresponding plot chunks, before export_plot(). The helpers
only save the plot and record its data/provenance.

F's ratio labels use ggtext::element_markdown(), 6.5 pt main text, and an explicit
5 pt span inside each subscript. The exported SVG contains separate editable
text elements for the sigma and each subscript. The ggtext dependency was
approved by the user and recorded in renv.lock. This approach follows the
package's [documented HTML/CSS support](https://wilkelab.org/ggtext/articles/introduction.html).

panelF/generated/log-snr-ratio.svg is exported and shown in the HTML gallery,
but excluded from assemble.py's placements and from the Inkscape master.
D's bins and E's total-share barplots omit the x title and tick marks; their
noise-model names remain, rotated by 60 degrees.

## Display letters a–h (2026-11-16)

The Inkscape master uses a–h. Panel f contains the spectrum, singular-value
ratio and SNR/ratio plots; g contains the two projection RMSE plots; h is the
final RMSE ratio plot. Plot paths retain their original panelF/panelG names.
The assembler records all eight display letters and the renamed h group
(`data-panelH`). Existing label positions and layer edits are preserved.
Labels are drawn above plot backgrounds.
The spectrum title is “Rank 3 signal” and its noiseless legend entry is “∅ (none)”.

## Simplified copy

`simplified/figure1-simplified.svg` is a separate 180 × 168 mm master with
panels a–g. It omits f's rightmost SNR/ratio scatter and all of h, following
the user's clarification. The remaining f and g plots share the bottom row:
spectrum 40 mm, singular-value ratio 41 mm, and projection W/H 43 mm each,
with 3 mm gaps. Plot heights are 40.4 mm. These are fresh exports at the new
sizes, preserving text size and plotted values. Only the compact spectrum
legend drops “(none)” after ∅. Input RDS and provenance remain in the original
panelF/panelG folders; the compact artwork uses exactly those data.

After running `render.R` and assembling the full figure, run:

```sh
python figure/fig1/assemble_simplified.py
inkscape figure/fig1/simplified/figure1-simplified.svg --export-type=pdf
inkscape figure/fig1/simplified/figure1-simplified.svg --export-type=png --export-dpi=600
inkscape figure/fig1/simplified/figure1-simplified.svg --query-all > figure/fig1/render/object-boxes-simplified.csv
python figure/fig1/verify.py --simplified
```

The first simplified assembly copies the full master, then removes and
repositions the selected groups. Later runs replace the four compact plot
groups while preserving edits to the simplified master. The full master
remains independent.

## Simplified version 2 (2026-11-17)

`simplified-v2/figure1-simplified-v2.svg` keeps the current simplified layout
and adds h as a 27 mm bottom row, making the page 180 × 197.5 mm. W and H
ratios are side by side, with a two-line y title on W and no y title on H.
The values come directly from `panelG/input_data.rds`, entry `fraction`;
no ratios are recomputed. Original input and provenance files remain in panelG.
The current simplified master is retained. All three masters show the refreshed
E-left x tick labels and title. The full assembly script is unchanged.

To export just these layouts from saved plotted inputs, run from the root:

```sh
Rscript figure/fig1/render_layout.R
python figure/fig1/assemble_simplified_v2.py
inkscape figure/fig1/simplified-v2/figure1-simplified-v2.svg --export-type=pdf
inkscape figure/fig1/simplified-v2/figure1-simplified-v2.svg --export-type=png --export-dpi=600
inkscape figure/fig1/simplified-v2/figure1-simplified-v2.svg --query-all > figure/fig1/render/object-boxes-simplified-v2.csv
python figure/fig1/verify.py --simplified-v2
```

`render_layout.R` exports E-left and the new h SVGs; it does not replace E in
an existing master. The E replacements for this update were made directly in
its named data group after saving backups 018 (full) and 002 (simplified).
The verifier follows the saved hand placement of f's ratio in the simplified
masters and the full master's combined g/h display label g.
