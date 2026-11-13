# Review request — transparent Rmd styling and mathematical labels

Recipient: fresh Advisor - Claude reviewer.
Repository: /workspace/dual_simplex_functional/general_dual_simplex_manuscript
Workspace: wks_eae2eb8dafb28fa0

Read README.md and AGENTS.md. Read-only review except write findings to
figure/fig1/theme_review.md; keep any scratch files under figure/fig1/render/.
No agents, no installing dependencies, no changes to the figure or sources.

The user requested (1) all common ggplot theme settings visible at the top of
figure1_components.Rmd; (2) all plot labels/style directly specified in the Rmd,
with export_helpers.R only writing files/provenance, no plot mutations;
(3) stacked bars D/bins and E/total: remove x-axis Noise title and tick marks,
retain model names rotated; (4) sigma ratio labels with real subscripts >= 5 pt,
using ggtext approved by user; (5) render the user's new log-snr-ratio option,
but do not assemble it. The baseline HEAD is a8fbb2ddfea43a8d91957a4563d94010afb6dfaf.

All changes are in the working tree. Final figure SVG/PDF/600dpi PNG and HTML
are ready; please open the PNG and the standalone log-snr-ratio.png if helpful.
The Rmd completed. verify.py reports 395 text objects, no duplicate ids and no
out-of-page/plot text bounds. Inspect the ratio SVG text nodes: main sigma
6.50 px (pt in source viewBox), subscripts 5.00 px. Main master imports at
25.4/72 scale in mm, so these are 6.5/5 pt at print size. No Standard Symbols
font used. Backgrounds, layout and annotations outside generated groups should
be preserved. The helper had hidden point-size/linewidth changes; these have
been moved into explicit geom arguments / top geom defaults to preserve style.

Check correctness/fidelity against git HEAD, transparency, all five requested
outcomes, numerical/metric preservation and visual clipping. Existing per-panel
input RDS hashes are unchanged for B,C,D,E,G. F gains only a log-snr-ratio entry;
previous F data entries are being checked in render/theme-data-comparison.log.
The new log coordinate transform is copied from the user's HEAD unchanged.
Existing science caveats in caption_notes.md/review.md are outside this task;
flag rather than change them. No fresh scientific claims are intended.

Write verdict, findings with file/line, and verification limits. Do not re-run
the large simulation archive unnecessarily. Please inspect code and artifacts
as they stand; the parent will keep them stable during review.
