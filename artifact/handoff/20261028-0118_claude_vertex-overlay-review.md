# Recipient: Advisor - Claude; independent review

Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
Workspace ID: `wks_f1fc0452fbbda285`
Role: fresh reviewer, read-only except report/checks under
`out/20261028_vertex_overlay_review/`. Do not start other agents.

The user asks for a helper to overlay precalculated vertices on DualPlot as a
dashed triangle outline. I interpret the unfinished phrase "without for the
structure" as no fill, vertex points or labels. Existing observed data remains.

Review the new add_true_vertices() appended to
`artifact/20261028_simulation_helpers.R` and the usage/mapping note
`artifact/20261028_vertex_overlay.md`. Earlier helpers are unchanged and were
independently accepted in the prior review. This function takes an existing
DualPlot patchwork, a true_vertices list (Omega, X), and matching GSVD dims.
It adds all vertex-pair segments to each appropriate panel, with no inherited
aesthetics or legend. Three vertices produce a triangle. Known inputs are the
simulation helper's stored matrices; UMAP is explicitly outside scope.

Check panel mapping and coordinate orientation; plot/indexing behavior; no
changes to input plot/data; style/legend independence; and whether examples work
with history-trimmed DSOs. Return accept or findings with file:line. Keep this
bounded; no broad package re-review or scientific inference from fixtures.

Package source (read-only): `../general_dual_simplex`, 0.29.0, full commit
bfd5ce69987c17e5a1253a477e9b73e965afc1aa, clean R/src. Repository renv still
has 0.28.0. Temp 0.29.0 installation is already available; from manuscript root:
`RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript ...`, and prepend
`.libPaths(c('/tmp/20261028_pipeline_library', .libPaths()))` before loading
GeneralDualSimplex. ggplot2 4.0.3 and patchwork 1.3.2 are installed in the renv.

Existing illustrative fixtures with true_vertices:
`out/20261028_simulation_validation/full_gzip.rds` (base data.frame with `result`
DSOs and `run` labels). Preview/check script will be under
`out/20261028_vertex_overlay/`. Use `pdf(NULL)` for plot-build checks to avoid
creating a root Rplots.pdf. Do not edit the helper or note. You may write your
report under out/20261028_vertex_overlay_review/review.md.
