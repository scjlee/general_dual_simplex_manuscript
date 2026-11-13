# Figure 1 working draft

Open **figure1.svg** in Inkscape. It is the editable single-page master;
figure1.pdf is the vector preview and figure1.png is the 600 dpi raster preview.
The page is 180 × 225 mm. Layers A–G contain only the panels selected in the
supplied outline. The long slide captions and definitions are kept separately
in reference/outline-text.txt, not packed into the artwork.

## Files and editing

- figure1_components.Rmd: cleaned, local-path Rmd; only the selected panels.
- render.R, export_helpers.R, simulation_helpers.R: report runner, styling/SVG
  export and the unchanged simulation-reader functions.
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

Plots export directly through svglite with real text. B's raster point layer
is replaced with vector circles at the same coordinates. The existing
schematics and their matrix/cloud values are illustrative; experimental plots
use the supplied saved simulations. No new simulations were run. Caption
claims in the supplied outline have not been established by this artwork task.
The archive records package version 0.38.0 but not its generating commit.

The supplied artwork guide recommends 180 mm width, 5–7 pt sans-serif text,
RGB and editable vector output. The 225 mm height is its maximum two-column
height for a short caption. This is a working layout; submission height must
be revisited with the final caption length. Definitions and detailed legends
remain in the companion reference text. Figure schematics use the existing
Liberation Sans font, which is metrically compatible with Arial.

In the compact schematic, W denotes feature profiles, H proportions, V* the
true signal, ε noise and V observed data, as in the source outline. Shortened
axis labels in A still denote the scaled sample/feature expression coordinates.
The narrow noiseless facet strips in C, F and G are labelled “0” (noise level
zero) so that the text fits; the data and facet widths are unchanged.
