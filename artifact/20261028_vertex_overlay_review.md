# Review: add_true_vertices() and vertex-overlay note

Reviewer: Claude (fresh, independent). Date: 2026-10-28.
Scope: `artifact/20261028_simulation_helpers.R:89-113` (uncommitted diff on
manuscript commit d270e7485cf2518b6c04c4b9126c27a4878ce8d2) and
`artifact/20261028_vertex_overlay.md`. Package GeneralDualSimplex 0.29.0,
commit bfd5ce69987c17e5a1253a477e9b73e965afc1aa, clean `R/` and `src/`
(checked). ggplot2 4.0.3, patchwork 1.3.2.

## Verdict

Accept. No blocking findings. Three minor findings, all optional: two
clarifications to the note and one error message.

## Checks

The checks are in `check.R` and `check_mutation.R` (this directory). They use
`pdf(NULL)`; no root `Rplots.pdf` was created.

- Panel mapping matches the package. `DualPlot` puts Psi on the left and Phi on
  the right (`R/dso-visualization.R:93-100`). The GSVD solution vertices are
  `sol$X[, dims]` for Psi and `t(sol$Omega[dims, ])` for Phi
  (`R/dso-visualization.R:357-361`). The helper does the same at
  `helpers.R:110-111`.
- Orientation: x is `dims[1]` and y is `dims[2]` in both, so reversed dims
  `c(3, 2)` match the package's axis labels (`R/dso-visualization.R:387-388`).
- Indexing: the helper selects by name `"dimN"`. In all 8 fixture runs,
  `X` has columns and `Omega` has rows named `dim1..dim3`, which come from
  `Psi`/`Phi` row names. Name-based selection is correct even when the truth
  was saved with a subset of dims. Both panels have k = 3 and choose(3, 2) = 3
  segments. The segment endpoints match the true vertex coordinates within
  1e-12, for dims 2:3 and c(3, 2).
- Input plot: the layer count stays at 1/1 and the layer-1 data are identical
  after the call. The serialized bytes do change, but a plain control
  `y <- p; y[[1]] <- y[[1]] + geom_blank()` changes them too, and
  `all.equal` against the old copy is TRUE. This comes from
  ggplot2/patchwork internals, not from the helper.
- Style and legend: the built layer is dashed, black, linewidth 0.4, with
  `inherit.aes = FALSE` and `show.legend = FALSE`. With `solution = TRUE`, the
  number of layers that can create a legend is the same with and without the
  overlay (2 vs 2). In the rendered `overlay_sol.png`, which I opened, there is
  one `component` legend, no fill, and no added points or labels.
- History-trimmed archive (`packed_trimmed_xz.rds`, 0 history rows):
  `history = FALSE` with the overlay builds without error.

## Findings (minor, non-blocking)

1. `artifact/20261028_vertex_overlay.md:20-21`: the note says
   `history = FALSE` works with trimmed archives. It does not say that the
   default fails. `DualPlot(d, dims = 2:3)` with `history = NULL` on the trimmed
   fixture errors with "dim(X) must have a positive length". Suggest: "Trimmed
   archives need `history = FALSE`; the default errors."
2. `artifact/20261028_vertex_overlay.md:10-11`: the line
   `RunReduction(dso, gsvd_dims = 2:3)` runs every time the block is pasted,
   although the comment says it is conditional. On the fixtures it would replace
   an existing dims-1:3 reduction. That is harmless here, but it is not a no-op.
   Suggest commenting the line out or wrapping it in
   `if (is.null(dso@reduction$gsvd))`.
3. `artifact/20261028_simulation_helpers.R:93,110-111`: if dims are missing
   from the saved truth, or the matrices have no dimnames, R stops with the bare
   message "subscript out of bounds". Optional: add a `stopifnot()` that names
   the available dims. The helper also cannot check `scaling_id`/`projection_id`
   against the plotted object, because it does not receive the DSO. The note
   covers this at line 31-32, which is adequate.

## Out of scope / not checked

I did not review `artifact/20261028_vertex_overlay_validation.R` or the lead's
`preview.png`. I did not check the scientific meaning of the fixture triangles,
k < 2 (`combn` errors), or UMAP.
