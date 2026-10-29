# Recipient: Advisor - Claude; fresh panel C noise sweep review

Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
Workspace ID: `wks_f1fc0452fbbda285`
Role: Reviewer. Read-only except your own report or validation under
`out/panelC_sweep_review/`. Do not start other agents.

User asks to plot a panel like the existing C from
`/data/simulation_runs_k3.rds` (reproduces `/data/261027_experiment_script_check.html`),
with colors for different noise parameters in each model. They then supplied
the code saving `metadata$row$scaled_var = matrixStats::rowVars(Vtilde)` and
`scaled_total = rowSums(Vtilde)`, where Vtilde = GetData(dso, "scaled").
The user was told that this differs from old C's Z metric and that the
new draft uses their saved variance, normalized across genes, with an
explicitly different axis label. Only uniform scaling is present in the
archive. They were also told that display bins 30 neighboring observed-total
ranks for readability while preserving unbinned summaries.

Review completed artifacts only in `figure/fig1/panelC_sweep/` and note
`artifact/20261028_panelC_noise_sweep.md`. Do not edit existing helpers or
other agents' files. Check saved-stat extraction and alignment, normalization,
ascending observed rank, per-seed binning followed by mean/min/max across
seeds, model/parameter mapping, negative-binomial line styles, caption,
provenance limits, SVG bounds/render, and master preservation. Final figures
are `fig1C_sweep.svg`, `.png`, `.pdf`. Unbinned rank summaries and actual
plotted bin summaries are saved as CSVs. Per-gene scratch data are at
`out/panelC_sweep/gene_shares.csv`. Run checks are in checks.csv and log
`out/panelC_sweep_summary.log`. All text bounds fit the canvas locally.

The RDS is a packed data.table with 320 rows and plain `result[[i]]$state`;
no R6 reconstruction needed. Saved package version 0.29.0; renv has 0.28.0.
The source's current commit is bfd5ce69987c17e5a1253a477e9b73e965afc1aa, clean
R/src. **Generating commit is not embedded or verified**, and the note says
so explicitly. No simulation or optimization is rerun. No new dependencies.
R runs from this repo root with RENV_CONFIG_SANDBOX_ENABLED=FALSE. Avoid
loading the full 1.6GB source unless necessary; all 320 saved variances were
already checked against matrix recomputation. Bounded independent checks
of summary math and visual inspection may suffice.

Return accept or findings with file:line, open questions, and write your
review to `out/panelC_sweep_review/review.md`. User did not request a commit
or push. The existing figure C is untouched.
