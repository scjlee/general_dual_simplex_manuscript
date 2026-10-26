# Figure 1 R Markdown consolidation review

Recipient: Advisor - Claude (fresh reviewer, other provider).
Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`.
Workspace ID: `wks_eae2eb8dafb28fa0`.

Review only; do not change tracked files or original figure inputs/outputs.
You may create a report and scratch checks in `out/fig1_playground_review/`.
Read README.md and AGENTS.md first; state the reviewer role once.

The user asked to collect all R data/visualization code for `figure/fig1`
into one editable R Markdown file. Exact SVG styling is unnecessary.
Review `figure/fig1/fig1_playground.Rmd`, currently a new untracked file.
It is self-contained simulation/plotting code with the original defaults;
it does not source panel scripts or overwrite existing panel data/masters.
It covers A, current and archived B, C and its Vtilde alternative, C's
signal/perturbation decomposition, D/sample companion, E/F and noiseless
oracle controls. W/H error definitions and assumptions should be unchanged.
All figures explicitly remain illustrative, supporting no manuscript claim.

Check numerical/mathematical equivalence to the source R scripts, sensible
parameter editing and captions/labels. Return a verdict, findings with
file/line, and open questions. A concise report is sufficient. Do not browse
or install dependencies. No commit is requested.

Sources: `panelA/points.R`, `panelB/mass.R` and its archived version,
`panelC/{noise_share,signal_noise_split}.R`,
`panelC_vtilde/variance_share.R`, `panelD/{projections,make_mock_panels}.R`,
all under `figure/fig1/`. The notebook also redraws the plot content of
the Python SVG renderers using ggplot2 and patchwork.

Evidence already collected by the lead:

- `Rscript out/fig1_playground/verify.R` renders HTML, retains its environment,
  and compares default data to existing saved RDS/CSVs across all panels.
- It passed: `out/fig1_playground/verification.log`. Every difference is
  below 1e-9; the largest is about 5e-13 in W oracle factor entries.
- Render: `out/fig1_playground/fig1_playground.html`.
- R plot previews: `out/fig1_playground/preview_{A,BC,DS,EF}.png`.
- `out/fig1_playground/validation_data.rds` has metrics/checks/decomposition.
- Rscript startup emits a renv cache-lock warning due to restricted writes
  in the home cache; the normal renv session still exposes rmarkdown from
  the existing system library. Do not use RENV_CONFIG_SANDBOX_ENABLED=FALSE
  for rendering: it hides the installed system rmarkdown. No new package
  has been installed or added.

Source snapshot: manuscript `85af3ab076de2a0fe9c4e9c71fc6ec88036b37b3`;
GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`.

The lead will separately test a changed-parameter run. No existing tracked
file has changed.

## Outcome

Advisor - Claude, agent `856c5695-6c78-4a8d-b2c4-b3a2c1cce7c3`, approved the
final notebook after a correction check. All findings were resolved. It
independently rendered the final version and reran the comparisons,
including the complete B summary. Report:
`out/fig1_playground_review/review.md`. The lead's changed-parameter run
also passes. The final reviewer message was read and the agent archived.
