# Dashed true-vertex overlay for DualPlot

Source `artifact/20261028_simulation_helpers.R`, which now provides
`add_true_vertices(plot, vertices, dims = 2:3, colour = "black",
linetype = "dashed", linewidth = 0.4)`.

```r
source("artifact/20261028_simulation_helpers.R")

# Uncomment if the fitted object has no GSVD reduction yet.
# dso <- RunReduction(dso, gsvd_dims = 2:3)

p <- DualPlot(dso, dims = 2:3, history = FALSE, solution = FALSE)
p <- add_true_vertices(p, dso@misc$true_vertices)
p
```

This adds dashed edges with no fill, vertex points, labels or additional legend.
The observed data points remain. Set `solution = TRUE` in `DualPlot` if fitted
vertex points should also remain visible. `history = FALSE` works with the
history-trimmed archives from the existing helper. For those archives, explicitly
set `history = FALSE`: the DualPlot default otherwise tries to draw the removed
trajectory.

Style and dimension changes use ordinary arguments:

```r
p <- DualPlot(dso, dims = c(3, 2), history = FALSE, solution = FALSE)
add_true_vertices(p, dso@misc$true_vertices, dims = c(3, 2),
                  colour = "firebrick", linewidth = 0.5)
```

Use the same dimensions for both functions, and coordinates saved from that
DSO's projection. This helper applies to the ordinary GSVD DualPlot. UMAP plots
require transformation into their embedding and are outside this helper.

The helper connects every pair of component vertices: with three components,
the edges form the requested triangle. It uses X rows in the left feature/Psi
panel and Omega columns, transposed, in the right sample/Phi panel. It adds
coordinates directly without recomputing or rescaling them. For more than three
components it draws all projected simplex edges, including interior edges in
the two-dimensional projection.

Implementation source: GeneralDualSimplex 0.29.0, package commit
`bfd5ce69987c17e5a1253a477e9b73e965afc1aa`, clean `R/` and `src/`.
Relevant source: package `R/dso-visualization.R`, `DualPlot` panel ordering and
`build_proj_panel` GSVD solution vertices. Plot layers follow the primary
[ggplot2 segment documentation](https://ggplot2.tidyverse.org/reference/geom_segment.html)
and panel modification follows the primary
[patchwork assembly documentation](https://patchwork.data-imaginist.com/articles/guides/assembly.html).

Verification: `artifact/20261028_vertex_overlay_validation.R` passed against the
temporary GeneralDualSimplex 0.29.0 installation, with ggplot2 4.0.3 and patchwork
1.3.2. It checks correct panel coordinates and edges, unchanged base plots and
colour scales, fixed style without an added legend, reversed dimensions, all
edges for four vertices, and a history-trimmed DSO. Run from the manuscript root:

```sh
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript artifact/20261028_vertex_overlay_validation.R /tmp/20261028_pipeline_library
```

The temporary library argument can be omitted when the current package is
installed in the repository's renv. Output:
`out/20261028_vertex_overlay_validation.log`; session:
`out/20261028_vertex_overlay/sessionInfo.txt`. The input is the earlier
illustrative fixture `out/20261028_simulation_validation/full_gzip.rds`, generated
by `artifact/20261028_simulation_validation.R` at the package commit above.
Manuscript base commit: `d270e7485cf2518b6c04c4b9126c27a4878ce8d2`;
the overlay and this validation are new changes after that base.

The preview `out/20261028_vertex_overlay/preview.png` was rendered at 600 dpi and
opened for visual inspection. It shows dashed unfilled triangles on the two
panels without added vertex points, labels or legends. Caption draft:
"Illustrative simulation fixture: precomputed true vertices overlaid on GSVD
coordinates; no scientific result is claimed."

Independent review: Claude, profile `Advisor - Claude`, **accept**. Record:
`artifact/20261028_vertex_overlay_review.md`. The reviewer independently checked
panel mapping, dimensions, endpoints, plot preservation, style/legend behavior
and history-trimmed plotting, and opened a preview with fitted vertices visible.
Optional documentation suggestions were applied: the preparation line is now
commented out, and history-trimmed objects explicitly require `history = FALSE`.
The original named-matrix contract is retained; requesting an unsaved dimension
produces R's ordinary indexing error.
