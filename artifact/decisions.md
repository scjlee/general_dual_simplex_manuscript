# Decisions

## 2026-10-09 — Start the manuscript repository with setup only and a new history

Context: the user split `scjlee/dual_simplex_functional` into three
independent repositories: experiments (full history kept), the
`GeneralDualSimplex` R package, and this manuscript repository. The
decisions behind the split are in the experiment repository's
`artifact/decisions.md`, entries from 2026-10-05 and 2026-10-09.

Options: start the manuscript from the old tracked TeX file, or start
empty. The old TeX file is a slide deck, not a paper draft.

Decision (user, 2026-10-05): setup only. This repository starts a new
history with a README, agent rules, this record and local tools. It does
not inherit the slide deck. No manuscript format or scientific content is
chosen yet.

Evidence: at setup, the experiment transition branch is at
`fe436483d4f394d3312d4bf02cd9938ab534fe3b`, and GeneralDualSimplex 0.1.0
is at `aa2717e59b098bcc31995d3dde5ab021aca6d087`. Its 13 standalone
reports were rendered at that experiment commit; the old and new reports
agree on every verdict.

Revisit if: the user chooses a manuscript format, or the experiment
repository is renamed on GitHub (README names it
`scjlee/dual_simplex_functional`).

## 2026-10-25 — One AGENTS.md for Claude and Codex; lead and reviewer roles; package .ai is read-only

Context: the user will not implement code here and now plans to use only
Claude and Codex, for figures, writing discussion and language checks.
Figure work moved here from the package repository (package
`.ai/decisions.md`, entry of 2026-10-25; handover
`.ai/20261025_fig1A-handover.md`). The user may retire the experiment
repository, so the rules do not name it.

Options: keep per-agent files (CLAUDE.md, CODEX.md, GEMINI.md); merge
them into one AGENTS.md.

Decision (user, 2026-10-25): one AGENTS.md. CLAUDE.md only imports it;
CODEX.md and GEMINI.md are deleted. Roles are lead (usually Claude) and
reviewer (usually Codex, read-only). Package `.ai/` is read-only and is
cited by note path and package commit. New Figures and Language-check
sections. Pushes only when the user asks. Second-provider review for
mathematical, evidence or figure-data changes, not for language checks.
Changes were written by the package thinking partner at the user's request.

Evidence: proposal in the package repository,
`.ai/20261025_manuscript-agents-md-proposal.md` (commit
21e061c1affa137fae3abb067ef968e2d3d6fb59), with the experiment-repository mentions removed as the user
asked. README "Working here" now points to AGENTS.md and says the figure R
environment is not set up yet.

Revisit if: the renv for figures is set up (update README), the
experiment repository is retired or kept (README still records it as setup
history and as the source of `script/`), or another agent type joins.

## 2026-10-25 — Manuscript renv with GeneralDualSimplex and legacy DualSimplex; experiment repo marked legacy pilot study

Context: the user asked to clean up this repository, approved the proposed
figure packages, asked to add the legacy DSO package
(`artyomovlab/dualsimplex`), and has not decided whether to retire the
experiment repository.

Options for the experiment repository: drop it from the rules, keep it as
the evidence source, or mark it as a legacy pilot study.

Decision (user, 2026-10-25): mark it as a legacy pilot study, read only, cited
by full commit, not developed further. The renv holds GeneralDualSimplex (local
install), DualSimplex (GitHub), ggplot2, patchwork, scales and svglite. Panel A
moved here as `figure/fig1/panelA/`; the handover note is
`artifact/20261025_fig1A-handover.md`. README rewritten (related repositories,
layout, R environment, tools); AGENTS.md lists the legacy sources.
Written by the package thinking partner at the user's request.

Evidence: R 4.5.3, Bioconductor 3.22, 90 packages in `renv.lock`.
GeneralDualSimplex 0.28.0 is `Source: Local` with no commit, so figure scripts
write `package_commit.txt` (package checkout at
156152b445d9e511e3bcf0080d8344b38fd2122b, no uncommitted `R/` or `src/`
changes; package code unchanged since e73fef4620adf03da7c46cbf2101724194adc329).
DualSimplex 1.2 is pinned at 089c982f8ea41e60365675c8e8013d095c3e5eaf; limma
3.66.0 and Biobase 2.70.0 come from Bioconductor. Rerunning `points.R` here
reproduced `tiles.csv` and `points_frac0.1_seed1.csv` byte for byte (oracle RMSE
uniform 0.0815, expression 0.0634). `fig1A.svg` is the user-edited master
(V* = WH, V); previews re-rendered from it and inspected. The ignored scratch
folder `out/step5c/` (2026-10-09 setup push record) was left in place: its
deletion was blocked by a permission check.

Revisit if: the user retires or revives the pilot study, package commits are
pushed routinely (pin GeneralDualSimplex by GitHub commit), or `make_fig1A.py`
is changed to update data groups by id (needed before it runs again).

## 2026-10-25 — Preserve Figure 1A labels during data refresh; use V* for signal and V for observations

Context: the user requested a generator that updates data groups inside the
hand-edited master and notation aligned between Figure 1A and README.
README used V for ground truth, while the figure used V* for signal and V
for observed data.

Options: change the figure's symbols to README's convention, or retain the
figure's symbols and update README. For SVG updates, serialize the complete
document or replace only the named data-group contents.

Decision (user): retain V* = WH for the true signal and V for observed data.
README now uses that convention and explicitly limits its existing noiseless
formulas to V = V*. The generator replaces only contents of the four heatmap
and two scatter groups by id, preserving their attributes and every byte
outside them. Labels remain part of the hand-edited master; the generator
prints RMSE for separate label checks.

Evidence: `artifact/20261025_fig1A-update-verification.md` records checks
against manuscript commit `cfe53929a7c2a5f891dbcdcd2145af6bb0a062a7`.
All text contents and query boxes are unchanged; the before/after PNGs are
byte-identical and were opened. Figure data and theoretical formulas did not
change.

Revisit if: data change (check the RMSE labels separately), the target group
ids change, or a noisy theoretical model is introduced.

## 2026-10-26 — Figure 1A shows noisy genes, mixed-sample heatmaps and a generic noise step

Context: the user requested upright matrix letters, one Noise box without
model parameters, RMSE labels above the plots, noisy gene projections with
colored markers and grey background, dashed pure simplex outlines, and
heatmaps that show linear mixtures rather than nearly pure samples.

Options: keep the H-oracle point clouds or plot observed gene profiles;
select nearly pure or interior mixture samples for the heatmaps; show a
model-specific or generic observation step.

Decision (user): show noisy gene profiles and a generic Noise step. The
existing illustrative simulation is retained. Each scaling projects every
nonzero observed gene into its estimated GSVD plane; the true component
profiles define the dashed triangle in that same plane. Marker components
use green, pink and gold. Interior samples replace the nearly pure heatmap
selection. Matrix letters are upright. The retained metric is labelled
H oracle RMSE and moved above each plot; the caption explicitly defines its
sample-side target. The SVG is edited by id and remains master.

Evidence: `artifact/20261026_fig1A-gene-simplex.md` gives the derivation,
caption draft, source paths, data roles and validation. Data were generated
with GeneralDualSimplex 0.28.0 at package checkout
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`, no dirty `R/` or `src/`
changes; those directories are unchanged since the installed-package commit
`156152b445d9e511e3bcf0080d8344b38fd2122b`. Data reproduce byte-for-byte,
the generator preserves the edited master on rerun, and refreshed PNG and
PDF previews pass the layout checks. A fresh Advisor - Claude reviewer
approved the math, evidence, data and opened PNG; minor caption and legend
legibility fixes were then applied. These remain illustrative data, not a
benchmark conclusion about scaling methods.

Revisit if: a different observation model is chosen, a gene-side error
metric replaces the H metric, or new data require updated labels.

## 2026-10-26 — Increase illustrative Figure 1A noise and label the nonconstant plane 2/3

Context: the user liked the revised figure and requested more noise to make
the weighting difference clearer, axis numbering 2/3 because dimension 1
is constant, and no further reviewer.

Options: retain the existing sampling fraction 0.1, or lower it to increase
relative sampling noise. Fixed-seed trials used 0.05, 0.04 and 0.02.

Decision: use 0.04 as the generator default. This preserves readable
triangles with more visibly scattered points under uniform weighting; the
0.02 trial nearly erased the geometry. Keep the latent mixture and seed,
all genes, the shared scale rule, and the rigid orientation. Rename the
axes Projection 2 and Projection 3 and update both H oracle RMSE labels.
The labels name the nonconstant plane; the caption records its rotation.
No fresh reviewer was launched, following the user's explicit instruction.

Evidence: `artifact/20261026_fig1A-noise-and-axes.md` records the trial
selection, values, package provenance, current caption addition, and
validation. Sources are the generated `projection_metrics.csv` and RDS
under `figure/fig1/panelA/`, produced by GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910` with no dirty R/src changes.
This is an appearance-selected illustrative example, not a new benchmark
conclusion. The final PNG was opened; text and point extents pass the
Inkscape checks.

Revisit if: the user wants unrotated singular axes, a different noise model,
or a representative multi-seed performance comparison.

## 2026-10-26 — Fit Figure 1A projections independently and remove k beside H

Context: the user asked whether triangle sizes were deliberately similar,
wanted the expression projection enlarged to make the comparison clearer,
and requested removal of k to the left of H.

Options: retain one shared display scale or fit each full cloud and its
triangle separately. The earlier renderer did not normalize triangle sizes;
it used one common coordinate range.

Decision: fit each projection independently, retaining equal aspect and all
points. Magnify the entire gene cloud and its triangle together. Add
“Separate plot scales” to the legend and update the caption interpretation.
Remove SVG text object label_H_rows. Data and metric values are unchanged.

Evidence: `artifact/20261026_fig1A-separate-scales.md` records the scope,
caption amendment and checks against manuscript commit
`e37dac1b8714c0d87d7a9148f0ac8f4ede5dd72e`. The six data files retain their
hashes; text and point extents fit. The final PNG was opened and inspected.
No new reviewer was launched for this minor display change.

Revisit if: absolute coordinate sizes need to be compared across panels,
or the user requests shared scales again.
