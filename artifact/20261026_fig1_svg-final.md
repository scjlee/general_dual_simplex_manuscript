# Figure 1 A/D/S/E/F: SVG revision for review and commit

Date: 2026-10-26. Current rendering/caption note; supersedes the layout
descriptions in the earlier D/E, E/F and D/sample notes. The data and
derivations in `20261026_fig1D-samples-and-EF-svg.md` and
`20261026_fig1EF-oracle-png.md` remain applicable. Illustrative simulation
only: no benchmark or general recovery claim relies on these draws.

## Final output

- A: gene projections, W-side oracle labels. Existing master changed only
  at the two RMSE text contents; its original H diagnostic remains in CSV.
- D: `figure/fig1/panelD/fig1D.svg` and PNG, 119 × 107 mm. Representative
  gene simplices; W oracle RMSE for one prespecified draw per noise model.
  The “Draw 1…” footer is removed. Legend and separate-scales note remain.
- S: `figure/fig1/panelD_samples/sample_simplices.svg` and PNG, same size
  and layout. Representative observed samples with H oracle RMSE from the
  same draw. “S” is provisional for supplementary placement. Its “Draw 1…”
  footer is removed too.
- E: `figure/fig1/panelE/fig1E.svg` and PNG, W oracle RMSE, 100 × 54 mm.
- F: `figure/fig1/panelF/fig1F.svg` and PNG, H oracle RMSE, same size.
  E/F's three bottom explanatory notes are removed; axis labels remain.

The removed information belongs in captions, not inside the panels. E/F
still show five dots per scaling/model, paired grey lines, mean bars and
mean values above the plots, without highlighting D/S's particular draw.
A/D match one E point; S matches one F point. Representative values need
not equal the displayed five-draw means. W and H errors have different units.

New D/S SVG generator: `figure/fig1/panelD/make_fig1DS.py`.
E/F SVG generator: `figure/fig1/panelE/make_fig1EF.py`.
Both create a master once, then replace only named data groups; all other
bytes and hand edits are retained. D/S's projection groups include data,
known triangles and their RMSE labels. E/F's data groups include paired
lines, dots, mean bars and mean values. Real Liberation Sans text, 5–8 pt;
mm viewBoxes, readable ids, Inkscape layers, 0.4–0.6 pt strokes.

`panelD/make_mock_panels.R` renders each standalone PNG from its SVG master
when present. Combined PNGs remain R/grid layout drafts and are refreshed
without the removed notes. Final own-file backup before this revision:
`out/20261026_fig1_final/001/`; A's pre-W-label backup remains
`out/20261026_fig1A_Wlabels/001/`.

## Current caption text

**A, oracle amendment.** The labels report W oracle RMSE for the illustrated
draw, in units of simulated W before the 0.04 library fraction, from
projecting the known W onto the
retained feature subspace. They do not measure gene-to-triangle distances.
Other existing current A caption conventions remain.

**D. Representative gene simplices.** All observed genes from one
prespecified illustrative signal/noise draw per noise model, shared by the
two scalings. Markers enriched for components 1/2/3 are green/pink/gold;
background genes are grey. Dashed: known H rows, normalized after sample
scaling and mapped into the same estimated space, not fitted vertices.
Each label is that draw's W oracle RMSE in units of simulated W before
the 0.04 library fraction. Separate display scales
and equal aspect. These values match individual points in E, not E's means.

**S. Representative sample simplices.** All observed samples from D's
same matrices. Grey: samples. Coloured vertices: known pure W profiles
normalized after gene scaling and projected into the same estimated
feature coordinates; dashed lines join
them. Labels: H oracle RMSE for that draw, in fraction units, matching
individual points in F. Separate display scales, equal aspect, no fitted
vertices. Illustrative simulation for possible supplementary placement.

**E–F. Oracle errors across five paired draws.** E reports the known W's
oracle RMSE; F reports the known H's oracle RMSE. Five independent draws
vary both signal and noise, at C's single settings. Within a draw, the
signal is shared across noise models and the observed matrix is shared
across scalings; weights are refitted per matrix. Dots: draws; grey lines:
paired scalings; short bars and numbers: arithmetic mean RMSE across five
draws. Oracles are unconstrained least-squares projections, with no clipping
or factor normalization and no vertex estimation. W is in units of the
simulated W before the 0.04 library fraction, H in fractions; their
y-ranges differ. These are illustrative simulations
for figure development, not benchmarks or general rankings.

## Provenance and validation

GeneralDualSimplex 0.28.0, package full commit
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, clean `R/` and `src/`.
Manuscript base full commit `c29f61dd9936840883af47cbea1fbd4521eee36d`.
This note describes the user-requested revision approved for commit after
fresh review. Numerical sources are the A/D/S/E/F input CSVs and generators
identified in the earlier derivation notes, in this working state.

All input CSVs are byte-identical to the pre-footer-removal backup. All
four final SVGs were rendered by Inkscape at 600 dpi and their PNGs opened.
Query bounds put all labels inside their canvases: D/S have 22 text objects
each; E has 24 and F 23. Every D/S point and coloured vertex lies within
its frame. All object ids are unique, no SVG embeds a raster, and the
required footers are absent. Running both data-refresh generators a
second time leaves all four SVG masters byte-identical. Diagnostics:
`out/20261026_fig1_final/`. `git diff --check` passes.

This review also covers the previously unreviewed W oracle, the sample
geometry, and A's label change across this session. Existing unrelated
C/discussion/AGENTS edits are outside this task's commit scope.

## Fresh review result

Advisor - Claude, agent `68d49e3c-ce86-4116-b3a8-9564f054013c`, workspace
`wks_eae2eb8dafb28fa0`: **approve for commit, no blocking findings**.
Handoff: `artifact/handoff/20261026-0603_claude_fig1-ADS-EF-final-review.md`;
report: `out/20261026_fig1_final_review/review.md`. The final message was
read through `get_agent_activity` and the reviewer was archived.

The review independently rebuilt original-unit rank-3 factor spaces for
12 noise/draw/scaling cases, checked package QP reconstructions against
both spans, recomputed all 60 saved RMSEs, checked every representative
label and five-draw mean, and reproduced both SVG refreshes and all five
standalone PNGs. It opened all five images and checked text/point bounds.
It did not rerun generators that overwrite task files; the independent
span check covers draws 1 and 4, and the other draws were checked against
their saved oracle entries. Package version/full commit are given above.

Optional wording fixes applied after review: explicitly state that W uses
the simulated scale before the library fraction, describe known vertices
after scaling/normalization, and update the stale data-generator header.
No data or SVG changed after approval. A's explicit “W oracle RMSE” and
D's shorter “oracle RMSE” labels are deliberate user choices. The current
SVG helper import via panel C works with the committed helper definitions;
moving helpers into a shared module is deferred. D/S's right-side label
fits its canvas; check its margin when assembling a multi-panel figure.

## Reproduction

```sh
python3 figure/fig1/panelD/make_fig1DS.py
python3 figure/fig1/panelE/make_fig1EF.py
RENV_CONFIG_SANDBOX_ENABLED=FALSE Rscript figure/fig1/panelD/make_mock_panels.R
```

Use File → Revert for figures already open in Inkscape.
