# Review — transparent Rmd styling and mathematical labels

Reviewer: fresh Advisor - Claude (read-only; wrote only this file and scratch
files in `render/review_scratch/`). Date: 2026-11-13.
Baseline: HEAD `a8fbb2ddfea43a8d91957a4563d94010afb6dfaf`; working tree as it stood
at 17:50 UTC.

## Verdict

**Accept with minor changes.** The refactor reproduces HEAD in every panel
except the intended changes. No data, metric or panel geometry changed. All
five requested outcomes are met. Two items need action before commit: the
unrequested change of the D/bins tick angle from 90° to 60° (finding 1) and a
stale tracked file (finding 2). Findings 3–5 are for the user to decide.

## Findings

| # | Severity | Location | Finding | Suggestion |
|---|---|---|---|---|
| 1 | Medium | `figure1_components.Rmd:403`; HEAD `export_helpers.R:37` | HEAD rotated the D/bins tick labels by **90°**. The Rmd and `README.md:92` now use **60°**. The request asked only to keep the names rotated. At 60°, the five labels 1.71 mm apart nearly touch in the 600 dpi PNG ("none"/"Normal"/"Poisson"/"Mul"/"NB"); no ink overlaps. `review.md` row 8 records that crowding in these labels was fixed by rotation. The refactor otherwise aimed to reproduce HEAD, so this is a visible style change that was not asked for. | Restore `angle = 90`, or ask the user to approve 60°. E/total was already 60° at HEAD, so it is unchanged. |
| 2 | Medium-low | `render/figure1_components.R` (tracked, modified) | This file is stale. Its timestamp is 17:44:54, but the Rmd was last saved at 17:45:56. It still has `bquote(σ[k+1] / σ[k] ~ "(lower is better)")` at lines 610, 675 and 732, and no `library(ggtext)` or `element_markdown`. HEAD's helper used to override those labels; it no longer does. Someone running this script would get the old labels. | Re-purl it from the final Rmd or restore it to HEAD. Do not commit it as it stands. |
| 3 | Low (user decision) | `figure1_components.Rmd:618, 643, 710, 768`; `README.md:83` | The F y-axis titles are **6.5 pt**. Every other axis title in the figure is 5.5 pt, and the difference is visible in the full-page PNG. This meets the request (subscripts at 5 pt, smaller than the main text), but it makes row F inconsistent with the rest. | Ask the user whether to keep 6.5/5 pt or use 5.5/5 pt, which matches the other titles but makes the subscripts only slightly smaller. |
| 4 | Low (user decision) | `figure1_components.Rmd:612`; HEAD `export_helpers.R:49` | The F/spectrum y title changed from "Normalized singular value" to "Normalized singular value σ<sub>k</sub>". Request item 4 names only the σ ratio labels. The new title brings back the σ<sub>k</sub> from the user's original `bquote`, which HEAD's helper had removed. ggtext also writes "Normalized", "singular" and "value" as three separate `<text>` objects, so the title is edited word by word in Inkscape. | Confirm with the user. If accepted, mention the word split in `README.md`. |
| 5 | Low (optional plot, not assembled) | `figure1_components.Rmd:754–758` | The log-SNR plot has two readability problems, both from the user's transform, which is copied unchanged from HEAD. (a) The x axis is labelled only at 2, 4 and 6. All non-Mul points (SNR 0.011 to about 1) lie left of the first label, so their x positions cannot be read. (b) `expand = FALSE` cuts **23 of 400** markers at the panel edges, and the y axis has no 1.00 label. No points are lost: 400 marks are drawn, the same as in the linear plot, and no SNR is ≤ 0. | Flag to the user only. Possible fixes are explicit log breaks (for example 0.01, 0.1, 1, 10) and a small expansion. |
| 6 | Note (outside task) | F/snr-ratio and log legend | The legend title "NOISE" is in capitals, unlike "Noise level" and "Noise" in F/spectrum. This was already so at HEAD. | Flag only. |
| 7 | Nit | `figure1_components.Rmd:311, 455, 601, 871` | Sizes such as `size = 0.05 / 3` and `2 / 3` keep the old effective values exactly (the helper divided sizes by 3). They are transparent but read oddly. | Optional: write the final value with a short comment. |

## What I verified

- **Requirement 1 (common theme at top).** The setup chunk holds the full
  former helper theme, the geom defaults and `noise_strip_labels` (Rmd lines
  28–56). Met.
- **Requirement 2 (helper only writes files).** `export_helpers.R` now only
  sets the path, records the inputs, calls `ggsave` and writes provenance. It
  changes no theme, layer, label, guide or facet. Nothing in `render.R`,
  `simulation_helpers.R` or `assemble.py` changes plots either. Met.
- **Fidelity to HEAD.** All SVGs were regenerated at 17:47. Every panel without
  an intended change is byte-identical to HEAD: B (5 files), C (2), D/rank,
  E/by-bin, E/snr and G (3). I compared the changed SVGs with HEAD after scaling
  each element to its panel's clip box:
  - F/spectrum and F/ratio: in-panel geometry identical.
  - F/snr-ratio: marker centres within 0.00026 of the panel width; marker sizes
    within 0.01 px (rounding); styles identical.
  - D/bins and E/total: bar rectangles within 0.001 (rounding). Only the 10 tick
    marks are gone.
  The text changes are exactly the expected ones: "Noise" removed from D/E, and
  the σ titles replaced.
- **Requirement 3.** D/bins and E/total have no x title and no x tick marks.
  Their model names remain, rotated by 60° (see finding 1). Met.
- **Requirement 4.** F/ratio, F/snr-ratio and the log plot draw σ at 6.5 px and
  "k+1"/"k" at 5.00 px as separate `<text>` elements. In the master the import
  scale is 0.35278 = 25.4/72, so these print at 6.5 pt and 5 pt. `pdffonts`
  lists only Liberation Sans (regular and bold), with no Standard Symbols. In
  the PNG the subscripts are lowered and legible. Met.
- **Requirement 5.** `panelF/generated/log-snr-ratio.svg` exists and appears in
  the HTML gallery. Neither `assemble.py` nor `figure1.svg` mentions it. The
  `coord_transform(x = "log10", xlim = …, expand = FALSE)` block matches HEAD
  line for line. The other changes in that chunk are labels and legend sizes,
  now the same as F/snr-ratio, plus the removal of `print(p)`. Met.
- **Master SVG.** Of the 80 ids (top level and two levels down), 67 are
  unchanged. Only the five changed data groups and their parent layers differ.
  All `translate`/`scale` placements are identical to HEAD, so the backgrounds,
  layout and annotations are preserved. Page size: 180 × 225 mm.
- **Data.** The B, C, D, E and G `input_data.rds` files are unchanged against
  HEAD by `git diff`. In F, the entries `spectrum`, `ratio` and `snr-ratio` are
  `identical()` to HEAD. The new `log-snr-ratio` entry is identical to
  `snr-ratio`.
- **Visual check.** I opened crops of the full-page 600 dpi PNG (rows D, E and
  F) and the standalone `log-snr-ratio.png`. I saw no clipped text in the
  assembled figure; the D/bins labels are crowded (finding 1).
- **Dependencies.** `renv.lock` adds commonmark, curl, ggtext, gridtext, jpeg,
  litedown, markdown and xml2. `ggtext` is listed as approved in `README.md`.

## Limits

- I did not re-run the Rmd, `assemble.py` or `verify.py`, and I did not run
  `inkscape --query-all`. I relied on the parent's `verification.json`
  (395 text objects, 0 duplicate ids, no text-box findings) together with my
  own PNG inspection.
- I did not run `renv::status()`. Every R start prints "project is
  out-of-sync"; this warning was already present at HEAD, and
  `render/ggtext-environment.log` ends with "No issues found".
- The SVG comparison covers in-panel marks, text strings and text styles. It
  does not compare the positions of axis or legend text, apart from the
  rotations I checked by hand in D and E.
- I made no scientific judgement. Existing caveats in `caption_notes.md` and
  `review.md` were not re-checked.
- Scratch files: `render/review_scratch/` (HEAD copies, comparison scripts,
  crops). The parent may delete them.
