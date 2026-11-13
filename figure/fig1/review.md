# Figure 1 review — SVG export and panel selection

Reviewer: Advisor - Claude (fresh). Date: 2026-11-13. Read-only review; my only
outputs are this file and scratch previews in `figure/fig1/review_previews/`
(safe to delete).

State reviewed: `figure1_components.Rmd` (03:31), generated SVGs (03:32),
`export_helpers.R` and `assemble.py` (03:34:41), `figure1.svg/.png/.pdf`
(03:35). The lead edited files during the review. The 03:34 changes to
`export_helpers.R` (strip labeller, tick angles) are **not yet in the
generated SVGs**, because the Rmd was not re-rendered. Package checkout:
`09dd30edfd7a65715e6ec0261d3ea12b0cd0ee71` (GeneralDualSimplex 0.38.0).

## Verdict

**Changes requested.** The computations, filters, seeds and plotted quantities
match the original Rmd. Three things block approval: (1) two labels rename
deconvolution error as "reconstruction", (2) panel F's σ labels and several
other text items do not render correctly, and (3) two pieces of information
on the panels were removed without being moved to the caption.

## 1. Analysis fidelity (checked; no change found)

- I diffed the original and new Rmd after stripping whitespace and comments.
  The only added code lines are `p <-`, `export_plot(...)`, chunk headers,
  setup/theme lines and B's `geom_point(size = 0.08)` (replacing
  `ggrastr::geom_point_rast(size = 0.5)`). No filter, metric, formula, seed or
  aggregation changed. Retained: `NOISE_LEVEL != "1/3"`, `EXAMPLE_L = "1/2"`,
  `EXAMPLE_SEED = 17`, D at levels `0`/`1/4`, E at `1/4`, `set.seed(1993)`,
  jitter `seed = 1`, `n_seed` divisor, the `oracle_rmse / rmse` ratio, and the
  SNR as ratio of summed post-scaling shares.
- `simulation_helpers.R` reader functions are identical to
  `artifact/20261028_simulation_helpers.R` (diff shows only removed writer and
  overlay functions).
- Run facts printed in `figure1_components.html`: 340 retained runs, 20 seeds,
  example seed 17 at level 1/2. 340 = 20 × (1 noiseless + 4 models × 4
  levels). So "none" has only level 0, and `sum(...)/n_seed` is a true mean
  in D and E. This matches the outline's "20 simulations" (F caption).
- Sanity check that could have failed: E "total", Before, gives a signal share
  of about 80 % for every model at level 1/4, as 1/(1 + 0.25) predicts. Read
  from the plot, not computed.
- Panel selection matches the outline (`reference/outline-*.png`): B shows
  feature simplices only; C rmse W/H; D rank and bins; E by-bin, total and SNR;
  F spectrum, ratio and SNR-versus-ratio; G oracle RMSE W/H and fraction.
  Unused plots, `eval=F` blocks and the install block are gone.
- Originals are unchanged: `reference/original_components.Rmd` and
  `reference/outline.pdf` are byte-identical to `data/figure1/`; Git shows no
  change to `panelA/fig1A.svg` or `panelB/fig1B_schematic.svg`.

## 2. Findings

| # | Sev. | Where | Finding | Suggestion |
|---|---|---|---|---|
| 1 | High | `export_helpers.R:45,48`; `assemble.py:81` (heading "Reconstruction"; the existing master keeps it) | C titles "W/H reconstruction", the G axis "Projection / reconstruction RMSE" and the C heading rename the metric. Package `R/benchmark.R` defines `rmse` as the RMSE between the processed **estimate and the true factor**, i.e. deconvolution error. The original Rmd and the outline say "Deconvolution error of W" and "Projection-to-deconvolution RMSE ratios". "Reconstruction" usually means ‖V − WH‖, a different quantity. This breaks the brief's "without changing quantities". | Use "W deconvolution", "Projection / deconvolution RMSE", heading "Deconvolution". Edit the heading text in the master by hand, because regeneration does not touch it. |
| 2 | High | `export_helpers.R:50–51`; `panelF/generated/ratio.svg`, `snr-ratio.svg` | The F y-labels render as a garbled "q" glyph overlapping the subscript (`review_previews/zoom-F-ratio-ylabel.png`). The SVG draws σ and "+" in font `"Standard Symbols PS"` with fixed `textLength`; plotmath `sigma` sends them to the symbol font. The original used the literal `σ` name. The subscripts are 3.85 pt, below the 5 pt minimum. Also seen in `figure1.png`. | Use a plain label such as `"σ(k+1) / σ(k)"` or `"σₖ₊₁ / σₖ"` in Liberation Sans, or map svglite's symbol font to Liberation Sans. Confirm by opening the PNG. |
| 3 | Med | `export_helpers.R:49`; F spectrum | Removing the title "Rank-3 signal (noise level = 0.25)" leaves the filter `NOISE_LEVEL %in% c("0","1/4")` stated nowhere on the panel. The outline caption does say "at noise level 0.25". | Keep it in the caption draft, or add a 5 pt note on the panel. |
| 4 | Med | `export_helpers.R:52`; E SNR, F scatter x-axis | "SNR" is the **post-scaling** ratio (`scaled_signal_var_share / scaled_noise_var_share`). The outline F caption says "post-scaling SNR"; the E caption does not. | Label it "Post-scaling SNR", or state this in the E caption. |
| 5 | Med | `export_helpers.R:11` vs Rmd `B-features` theme | B lost its blank axes. `export_plot` adds `axis.text`, `axis.title` and `axis.ticks` after the plot's own `element_blank()`, so ticks, numbers and "dim2/dim3" reappear. Tick labels overlap ("-0.40.0 0.4 0.8"), and "Multiplicative" is clipped to "Multiplicativ". The original and the outline show bare simplices. | Skip the axis overrides for `panelB`, or reapply `element_blank()` after them. Shrink or wrap the B titles. |
| 6 | Med | A schematic, `assemble.py:42–48` (`clamp_text`) | The pipeline-box text is fixed in the 03:35 master (whitespace step). Remaining problem: at scale 0.64, the 5 pt minimum enlarges the axis labels by 1.56×. "scaled sample₁ expr." now collides with "scaled sample₂ expr." under both planes. | Move or shorten these four labels in the master, or give A more width. Check with `inkscape --query-all`. |
| 7 | Med | Every generated SVG → master | svglite writes `<rect width='100%' height='100%' fill='#FFFFFF'>`. Nested in the master, each one resolves to the page size × PT, a white rectangle 63.5 × 79.4 mm at each plot's origin (`review_previews/query-all.csv`: e.g. `panelB-feature-Poisson-rect-0004` spans 127–190.5 mm; the page bounding box reaches 224.5 mm). Draw order hides this now, but in Inkscape these rectangles catch clicks and will cover any panel moved under them. | Drop or size these rectangles in `import_art`, e.g. replace 100% with the source viewBox size. |
| 8 | Low | C, G, F-ratio strips; D bins, E SNR x-axis | Text is clipped or overlaps: the strip "none" shows as "on"/"one", "1/41/2" collides in E SNR, and the D bin x labels overlap. The 03:34 helper edits (labeller, 60–90° ticks) aim at this but are not rendered yet. Renaming the strip "none" to "0" makes it identical to its x tick and drops the model name. | Re-render, then inspect. "None" may fit if the strip text is 5 pt. |
| 9 | Low | `assemble.py` (`schematicB` short labels) | B labels are shortened to W, H, V*, ε, V. The words "profiles, proportions, true signal, noise, observed data" now appear only in the outline caption text. | Put these definitions in the caption draft. |
| 10 | Low | `assemble.py:74`, README | The 225 mm height is the guide's maximum only for captions under 50 words (`reference/artwork-guide-1.png`). The outline captions for A–G total several hundred words, which allows about 185 mm. The README already notes this. | Plan for about 185 mm, or a shorter caption. |
| 11 | Low | `figure1_components.html` | Pandoc could not fetch the 17 embedded `generated/*.svg` (render.log: "Could not fetch resource"), because it resolves paths from `render/`. The HTML has no previews. | Use absolute paths or `knitr::include_graphics(normalizePath(...))`. |
| 12 | Low | `export_helpers.R` `write_provenance` | Provenance names the input RDS but gives no checksum, and its generating commit is unknown. | Record `sha256sum data/figure1/k3_simulation_balanced-population.rds`. |

## 3. Pre-existing issues (flagged, not fixed; author decision)

- **F spectrum normalisation.** Rmd lines 515–531:
  `normalized_spectral = σ_k / (‖biwhitened‖_F² − 1)`. If σ₁ = 1, the
  denominator is Σ_{j≥2} σ_j². Values of about 4.2 at k = 2 (noiseless)
  show that this is not a share; a share would be ≤ 1. So the plotted value
  scales as 1/σ and is not scale-free, and "normalized singular value" does
  not say what it is. Consider σ_k² / Σσ² (share of inertia) or
  σ_k / √Σσ². This would change plotted numbers, so it needs the author.
- **D rank y-axis is truncated** at the 99.9 % quantile of noiseless shares
  (Rmd lines 288–289). The note on omitted features was commented out in the
  original. The caption should say so.
- **F scatter legend.** The grey "Noise level" fill legend does not match what
  is drawn: shapes 15/16/17/3 ignore `fill`, and level is shown by the
  per-model colour gradient, whose guide is hidden. The shape legend title is
  the raw column name "NOISE".
- **D bins** use `dplyr::ntile(rank, 5)` over the pooled table, not per run
  (Rmd line 242). If every run ranks the same m features 1..m, this equals
  per-run binning. I did not check that.
- **Metric definitions** are read from the package at the current commit. The
  archive does not record the commit that generated it, so the definitions
  are assumed unchanged.
- **Outline caption claims** (e.g. C "maintaining accuracy near the noiseless
  baseline", G "ratios approach one in some cases"): the plots are visually
  consistent with them. I did not test them numerically.

## Limits

- I did not re-run the Rmd or load the 1.9 GB archive. Fidelity rests on the
  code diff, the printed run facts and the rendered plots.
- I inspected the PNG previews (400 dpi per plot; the 600 dpi master at
  03:35). The final state after the lead's pending re-render is not reviewed.
  Re-check findings 2, 5 and 8 after it.
- The finding 6 test (stripping whitespace on a scratch copy restored the
  boxes) supports the lead's fix. Text overlap was not checked by bounding
  boxes for every label.

---

## Addendum — final-state check (2026-11-13, artifacts 03:38–03:41)

**Revised verdict: approved as a user-editable draft.** All blocking and
medium findings above are resolved in the rendered output. The low-priority
notes below need no regeneration. This is not approval of the scientific
captions, and the pre-existing issues in section 3 remain open for the author.

State checked: Rmd and helpers 03:38:03; generated SVGs 03:38:25;
`assemble.py` 03:40:51; `figure1.svg` 03:40:52; `figure1.png` (600 dpi)
03:40:55; `figure1.pdf` 03:40:59. I read `review_response.md` and
`caption_notes.md`, and I opened the final PNG and four 600 dpi crops
(`review_previews/final-*.png`).

### Re-check of the original findings

| # | Status | Evidence |
|---|---|---|
| 1 | Fixed | The C titles read "W/H deconvolution", the heading reads "Deconvolution", the G axis reads "Projection / deconvolution RMSE" (`export_helpers.R:45,48`; PNG). |
| 2 | Fixed | The F labels read "σ(k+1) / σ(k)" in Liberation Sans and are legible in the 600 dpi crop. `figure1.svg` contains no "Standard Symbols" font. |
| 3 | Fixed | The spectrum title reads "Rank 3; noise level 0.25". |
| 4 | Fixed | The E y-axis and the F scatter x-axis read "Post-scaling SNR". |
| 5 | Fixed | The B simplices have no ticks or tick text. "Multiplicative" fits. The example settings appear as "Feature simplices: seed 17; noise level 0.5". |
| 6 | Fixed | The pipeline boxes show two-line labels. The axis labels under the planes no longer collide (now "sample₁ expr.", etc.). |
| 7 | Fixed | `figure1.svg` contains no `width='100%'` rect. |
| 8 | Fixed | The strips show "0", "Normal", …; the D, E and F tick labels are rotated and do not overlap. |
| 9 | Addressed | The B definitions are in `caption_notes.md`. |
| 10 | Documented | `caption_notes.md` and `review_response.md` state that 225 mm depends on a caption under 50 words. |
| 11 | Fixed | The HTML has 19 SVG/data-image matches (18 panels plus a header match). Not opened in a browser. |
| 12 | Fixed | `reference/input-manifest.tsv`. I recomputed the RDS SHA-256 (`ad5c1ccc…44a4`), and it matches. |

### Fidelity re-check

- I repeated the whitespace- and comment-insensitive diff of the original and
  the 03:38 Rmd. The added lines are again only setup, export, chunk headers,
  `geom_point(size = 0.08)` and the printed facts. No filter, metric, seed or
  formula changed. All label edits are in `export_helpers.R` and change text
  only.
- Text size: I walked the `scale()` transforms in `figure1.svg` and found no
  `text`/`tspan` below 4.95 pt at final size. Most plot text is 5.0–6.0 pt.
  This check reads `scale()` only, not `matrix()` transforms.
- `render/verification.json` reports no text outside the page or its plot
  slot. `verify.py` checks containment, not text-to-text overlap. I checked
  overlap by eye on the PNG and found none.

### Remaining low-priority notes (no regeneration needed)

1. The noiseless condition has three names: "Noiseless" (B), "0" (C, F-ratio
   and G strips), "none" (D facets and ticks, F spectrum legend). Pick one, or
   define them in the caption.
2. Noise levels mix fractions and decimals: tick labels use "1/4, 1/2", while
   the titles say "noise level 0.5" and "0.25". This is harmless, but uniform
   notation would read better.
3. The A axis labels dropped "scaled". `caption_notes.md` says they denote
   scaled expression coordinates, so keep that sentence in the caption.
4. The F scatter legend title is still the raw column name "NOISE"
   (pre-existing). `caption_notes.md` covers the grey shade proxy but not
   this title; consider renaming it "Noise" in the master.
5. In B, the true simplices for the Normal and Poisson examples are barely
   visible or invisible at this size, because outlying points set the axis
   range (pre-existing; the outline shows the same). The outline caption
   "Colored triangles indicate the true simplex" is therefore not visible
   for those two examples.

### Open (author decision, unchanged)

The section 3 items remain open: the spectrum normalisation (values about 4.2;
not a share), the truncated D y-axis, the shade legend, pooled binning, metric
definitions taken from the current package commit, and untested caption
claims. `caption_notes.md` records most of them accurately and claims nothing
beyond the evidence.

### Limits

I did not re-run the Rmd or `assemble.py`, and I did not open the PDF itself.
The PDF was exported 4 s after the PNG from the same SVG and is assumed
equivalent. I did not check the regeneration path, in which an existing
master's groups are replaced, against a hand-edited master.
