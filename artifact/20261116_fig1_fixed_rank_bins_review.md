# Fixed Figure 1 rank bins — independent review

Reviewer: fresh Claude, profile=Advisor - Claude, Paseo agent 5445cf11-548e-4f26-afaa-f6cf20fb0c4d. Verdict: approve.

Source baseline: manuscript commit bcc2af21e19a90e43cb4d791d1896e23ec49b691, plus the working legend-order fix reviewed separately in artifact/20261116_fig1_three_bins_legend_review.md. This report describes the corrected outputs committed alongside it. Numerical evidence: figure/fig1/panelD/input_data.rds, rank and bins tables; figure/fig1/panelE/input_data.rds, by-bin, total and snr tables. Caption source: figure/fig1/caption_notes.md, D. Before-fix pooled-three-bin inputs were saved in out/20261116_fig1_fixed_bins/panelD-before.rds and panelE-before.rds. No package parameters or package provenance files changed.

Lead disposition: approved; no blocking findings. This generator is specific to the supplied rank set, not a general binning utility. Existing axis label choices remain as requested. No caption percentage claims require updates. Fixed boundaries and bin sizes were checked independently as well as by out/20261116_fig1_fixed_bins/check.R. Final PNG was opened and Inkscape bounds checked. All master artwork outside D/E was preserved from backups/figure1-014.svg.

## Reviewer response

Showing 1 of 32 activities (limited to 1)

**Verdict: approve.** Every rank now falls in the bin it should, in every run. The only values that changed are the bin summaries in panel D's stacked bars and panel E's by-bin bars. I edited no files; my scratch scripts are only in `/tmp`.

**What I checked** (my own R scripts, run from the repo root, plus the PNG image itself):

- **Source.** `figure/fig1/figure1_components.Rmd:277` now computes `ceiling(rank / ceiling(max(rank)/3))`. In the saved panel D data, every noise model and scaling has ranks 1–2150, each appearing once per seed across 20 seeds. So the bins are 1–717, 718–1434 and 1435–2150, holding 717, 717 and 716 ranks. All 430,000 panel D rows match these ranges.
- **The old problem is fixed.** In the old pooled data, ranks 717 and 1434 were split between two bins. Those are the only two ranks whose bin changed: 196 rows in panel D and 316 rows in panel E.
- **Panel E bins.** Panel E's data has no rank column. Its rows follow the same order as panel D's (the same genes in the same runs), and I confirmed that for all four scaling and signal/noise combinations its bin sequence is identical to panel D's. Every noise model, seed, scaling and type has 717, 717 and 716 genes per bin.
- **Nothing else moved.**
  - Panel D: every column except `bin` is identical to the old data.
  - Panel E: every column except `bin` is identical in by-bin and total, and the SNR table is identical.
  - The panel D bar values recompute exactly from the rank data (largest difference 0). They differ from the old values by at most 0.033 percentage points (Mul, After, high bin).
  - Panel E per-seed bin sums changed by a median of 0.00016 and at most 0.46 percentage points.
- **SVG master.** Only `data-panelD-bins` and `data-panelE-by-bin` differ from `backups/figure1-014.svg`. All other layers and groups are byte-identical, including the D rank plot, E total, E SNR and the panel labels. `verification.json` reports no text-box problems and no duplicate ids.
- **Image.** I opened crops of panels D and E from `figure/fig1/figure1.png`. D's legend reads high/mid/low in the same order for before and after, and the bar heights match the recomputed values (for example, none/Before/high is 96.3%). Panel E renders normally.
- **Caption.** `figure/fig1/caption_notes.md:28-31` matches the code and data (1–717, 718–1434, 1435–2150; width rounded up; the last bin takes the rest).

**Findings** (none block the commit):

1. Low: the formula only gives three bins when there are more than four ranks; with four ranks it gives two. That cannot happen with 2150 ranks, so it needs no change; it only matters if the code is reused elsewhere.
2. Pre-existing, not part of this change: panel E's bin axis has no tick labels (`axis.text.x = element_blank()`, around Rmd:477). Readers infer high, mid and low only from bar order and the axis title "(high -> low)". The same is true at HEAD.

**Open questions:**

1. Should the caption state that rank 1 is the most highly expressed gene? The axis title implies it, but I did not check how the package defines `rank`.
2. Panel D's bars changed by up to 0.033 points and panel E's per-seed sums by up to 0.46 points. If any manuscript text quotes these bin percentages, it needs updating. I found no such numbers in `caption_notes.md`.
