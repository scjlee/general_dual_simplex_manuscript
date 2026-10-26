# Figure 1A: fit each projection separately; remove k beside H

The user requested a larger expression triangle and removal of k to the
left of H. The previous renderer used a single shared display scale for
both complete clouds. It did not explicitly force equal triangle sizes.

Starting manuscript commit: `e37dac1b8714c0d87d7a9148f0ac8f4ede5dd72e`.

## Display decision

`make_fig1A.py` now fits the range separately for each projection using
all its observed genes and pure vertices. Each plot retains equal aspect
and the existing padding. Points and triangle receive the same translation
and uniform magnification within each plot. All outliers remain visible.
This enlarges the expression projection because its full cloud has a
smaller coordinate range in the stored simulation.

Both branches use the same noisy observed matrix. This revision changes
display magnification; the input data, coordinates and H oracle RMSE values
are unchanged. The projected triangle's size on the page therefore cannot
be compared directly between panels as an absolute size or error measure.

Caption amendment, superseding the earlier shared-scale description:
“Each projection is fitted independently to all its genes and pure vertices,
with equal aspect. The panels use separate scales; compare the dispersion
of points relative to each triangle rather than absolute sizes on the page.”
The figure legend now explicitly states “Separate plot scales.”

The SVG object `label_H_rows` was removed. The H heatmap and its other labels
are preserved. The SVG remains the master and numbered backups are in
`out/20261026_fig1A_separate-scales/`.

## Verification

SHA256 comparisons confirm that all six simulation/data files match the
starting revision, including gene coordinates, vertices, metrics, selected
samples, tiles and the simulation RDS. All remaining text subtrees and
attributes match the master backup except for the legend addition.

The final SVG was exported to PNG at 600 dpi and to PDF. The PNG was opened
and inspected. Inkscape query checks put all 26 remaining text objects
inside the canvas, five box labels inside their rectangles, and all 1,000
gene circles inside their plot frames including their radii. A second
generator run leaves the entire edited master byte-identical. No reviewer
was launched for this display change, consistent with the user's instruction
for these minor revisions.
