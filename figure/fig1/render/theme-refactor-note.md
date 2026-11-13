# Transparent Rmd styling and subscript rendering

Baseline manuscript commit: a8fbb2ddfea43a8d91957a4563d94010afb6dfaf.

The common ggplot theme and geom defaults are now in the setup chunk at the
top of figure/fig1/figure1_components.Rmd. Panel-specific labels, rotations,
legend sizes and geom arguments are in their individual Rmd chunks.
export_helpers.R now only saves files and records the plotted inputs and
package provenance; it does not mutate plots.

D/bins and E/total omit the Noise x-axis title and x tick marks. Model names
remain and rotate 60 degrees. Sigma ratio labels in F use element_markdown with
6.5 pt main text and explicit 5 pt spans inside the subscripts. These sizes
were checked directly in all three generated F ratio SVG files, including the
optional log-snr-ratio plot. No superscript label was required by these plots.

The user approved installing ggtext. ggtext 0.1.2, gridtext 0.1.6 and the
required dependencies were installed and recorded in renv.lock. renv::status()
reported a consistent state. Usage follows the package's documented support:
https://wilkelab.org/ggtext/articles/introduction.html

Rscript figure/fig1/render.R completed. The optional log-snr-ratio SVG and PNG
were rendered and the SVG was included in the HTML gallery. It is absent
from assemble.py's placements and the master SVG. Its log10 coordinate
transform and limits are unchanged from the user's baseline commit.

Existing B/C/D/E/G input RDS checksums are unchanged. Existing F entries
spectrum, ratio and snr-ratio are identical after deserialization; F gains
only log-snr-ratio. Details: theme-refactor-results.json and
theme-data-comparison.log. No new simulations or evaluations were run.

The prior master is backups/figure1-004.svg. The assembled master outside the
generated groups is unchanged. The one-page PDF and 600 dpi PNG were exported;
the PNG and optional log-SNR PNG were opened. All assembled text objects
fit the page and plot slots; there are no duplicate IDs. The existing ten
inline 1200 dpi raster point layers remain. See verification.json.

The spectrum retains its plain 5.5 pt axis title. The tracked extracted R script was regenerated from the final Rmd with knitr::purl().
