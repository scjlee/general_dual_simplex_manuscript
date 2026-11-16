# Figure 1 three-bin regeneration and legend review

Baseline manuscript commit: bcc2af21e19a90e43cb4d791d1896e23ec49b691.
Reviewed working outputs use the three-bin settings from ac60e9c8c2f90c8c7246e026019e149da5b7a2a4 and the two guide-order edits in figure/fig1/figure1_components.Rmd. Saved package provenance is unchanged. Reviewer: Claude, profile=Advisor - Claude, Paseo agent 1f7de98a-7fec-4a0f-b356-25b415291c7b.

## Lead disposition

- Approved. Green Before is above orange After, each high/mid/low. The final SVG, PDF and 600 dpi PNG were opened/checked; Inkscape measured no text outside the page or plot slots, and no duplicate ids.
- The reviewer observed intermediate panel B output while the final master was being prepared. The final master preserves every section except D/E from backups/figure1-013.svg; the generated B SVG is also restored byte-for-byte. This resolves the title-layout finding without changing the user's saved artwork.
- The pooled ntile binning is the user's committed setting and is already described in caption_notes.md. The reviewer flags boundary-rank consistency as an optional scientific follow-up. It was not changed in this legend/layout task.
- Corrected the handoff's mistaken description of the prior bin count: five, not four.
- Proposed house rule, 2026-11-16: Read the saved bin levels before describing the previous bin count in a handoff.
- The pre-existing untracked render/panelF/generated/log-snr-ratio.svg was preserved.

## Reviewer response (observed intermediate B artwork)

Showing 2 of 52 activities (limited to 2)

[Thought] The images have rendered, and the E values line up with what I expected. The x-axis bins on E are unlabelled now, and the legend is gone, so its colors are explained by the middle legend instead. With the by-bin legend removed, the Source legend on the total plot covers it. B's titles look fine visually, so I'm checking the centering next.

I'm checking the figure's provenance and noting that the B titles are centered. Several smaller items remain: the handoff's "four bins" count is off by one, the `figure1_components.html` change looks fine, and an older untracked SVG predates this work. The E image looks clean with no leftover space after the legend removal, so I'm moving on to composing the verdict.
**Role:** Reviewer, read-only. I edited no files.

## Verdict: approve

Panels D and E now use the user's three-bin calculation from commit `ac60e9c8c2f90c8c7246e026019e149da5b7a2a4`. Bin 1 is labelled high, bin 2 mid and bin 3 low. The legend fix changes only the legend order, not any plotted value. There is one small data issue, which existed before your edit. There is also one layout side effect in panel B.

## Checks that passed

- **Generator diff:** the only uncommitted change in `figure/fig1/figure1_components.Rmd` is `guide = guide_legend(order = 1)` on the green Before scale (line 385) and `order = 2` on the orange After scale (line 402).
- **Data unchanged apart from bins:** in both D tables and all three E tables (by-bin, total, snr), every column except `bin` is identical to `out/20261116_fig1_legend/panel{D,E}-before.rds`.
- **Totals preserved:** each of the 10 model × scaling totals in D is 100 both before and after (largest difference 1.4e-14). The 320 per-seed totals in E (model × scaling × type) match exactly. Recomputing D's bars as rows ÷ 20 seeds reproduces the saved values exactly.
- **Label alignment:** bin 1 covers ranks 1–717 and bin 3 covers ranks 1434–2150. Rank 1 is the highest expression, which agrees with the old label "1 (high)". Every old bin maps into the expected new bins: 1→1, 2→1 or 2, 3→2, 4→2 or 3, 5→3.
- **Images inspected:** `out/20261116_fig1_legend/panelD-bins.png` and crops of `figure/fig1/figure1.png`.
  - In D, the green legend is on top and the orange legend below, each ordered high, mid, low.
  - The bars match the data, for example noiseless Before: high 96.3, mid 3.4, low 0.25; Normal After: low 92.2.
  - E's bars match the data (Normal Before, bin 1: noise 8.1, signal 76.8) and E has no bottom legend. E's x-axis has no tick labels, so "high/mid/low" appears only in D.
- **Other panels:** the input data, package commit files and generated SVGs of C, F and G, and of B except one SVG, match `before.json`. `verification.json` reports no text-box findings. The text count fell from 393 to 383, which fits fewer legend labels in D and the removed legend in E.

## Findings

1. **Minor, existed before your edit: two ranks fall into different bins in different runs.**
   - **Where:** `figure/fig1/figure1_components.Rmd:277`, where `dplyr::ntile(rank, 3)` runs over all experiments pooled together.
   - **Cause:** there are 2150 genes, which 3 does not divide evenly (5 did). So rank 717 is in bin 1 for 136 rows and bin 2 for 64 rows. Rank 1434 is split the same way between bins 2 and 3. The old five-bin data had no split ranks.
   - **Effect:** binning each gene by rank alone, the same way in every run (`ceiling(3 * rank / max(rank))`), moves any bar by at most 0.017 percentage points (Mul, After, high). That is not visible.
   - **Wording:** "Bins use the source's pooled rank binning" in `figure/fig1/caption_notes.md:28` already describes this. Whether to change the binning is the user's call.
2. **Layout: the full re-render overwrote hand edits to panel B's titles in the master SVG.** Before, `figure1.svg` had single, centred text objects with `y=4.78`:
   - "∅ (none)" kept its tspan `panelB-feature-none-title-explanation`.
   - "Neg. Binom." was one object.

   Now each title is split into separate objects positioned by ggtext: "∅" + "(none)" at `y=5.01`, and "Neg." + "Binom.". The tracked file `figure/fig1/panelB/generated/feature-none.svg` also changed; it is not identical to the copy in `before.json`. In the PNG the titles still look centred and correct. No data is involved, but it goes against the "SVG is the master" rule and the ids from commit 9bce22f. Either restore those title objects from the HEAD copy of the master, or record that the change is accepted.
3. **Wording in the handoff:** it says the old outputs had four bins. The old RDS files and commit ac60e9c show five bins.

## Open questions

- Should the binning become per gene (fixed sizes 717/717/716), or stay pooled as the caption note describes?
- Should B's hand-edited title objects be restored, or is the regenerated layout acceptable?
- The untracked `figure/fig1/render/panelF/generated/log-snr-ratio.svg` is dated 13 November, so it is not part of this change. Leave it untracked.
