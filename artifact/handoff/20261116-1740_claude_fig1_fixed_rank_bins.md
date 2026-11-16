# Review fixed Figure 1 rank bins

Recipient: fresh Claude Reviewer, profile=Advisor - Claude.
Repository: /workspace/dual_simplex_functional/general_dual_simplex_manuscript
Workspace ID: wks_eae2eb8dafb28fa0
Role: Reviewer, read-only. Read README.md and AGENTS.md. Do not edit files or rerender the full figure.

User explicitly requests fixing the pooled bin issue: all rank 717 must be in bin 1 and all rank 1434 in bin 2; commit after completion.

Change: figure/fig1/figure1_components.Rmd:277 replaces pooled ntile(rank,3) with factor(ceiling(rank / ceiling(max(rank) / 3))). For 2150 ranks, this gives bins 1–717, 718–1434, 1435–2150 in every run. Caption_notes.md now describes these fixed ranges. The earlier uncommitted guide_legend ordering change is also being included in this final commit and was independently approved in artifact/20261116_fig1_three_bins_legend_review.md. A proposed formula ceiling(3*rank/max(rank)) from that earlier review would fail the requested boundary conditions; this implementation instead uses a bin width rounded up.

Full render is complete. Saved D/E inputs and bin SVGs regenerated; SVG/PDF/PNG exports ready. Every master section outside D/E was preserved from backups/figure1-014.svg. Ignore the pre-existing untracked render/panelF/generated/log-snr-ratio.svg. Only D/E data are expected to change; package provenance unchanged.

Check the source, caption, saved D/E RDS data, and actual figure image. Verify every rank maps consistently to the requested bin; no numerical values other than regrouped bin summaries change. Prior (pooled three-bin) inputs are out/20261116_fig1_fixed_bins/panelD-before.rds and panelE-before.rds. My validation script/log are out/20261116_fig1_fixed_bins/check.R and check.log. Verify independently, using R from repo root. No full simulation rerun or package edits required.

Return a compact verdict, findings with paths/lines, and open questions in your final message; do not write a report file.
