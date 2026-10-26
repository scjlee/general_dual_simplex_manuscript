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

## 2026-10-26 — Define which changes skip second-provider review; exempt illustrative figure data

Context: AGENTS.md required review for "substantive" mathematical,
evidence or figure-data changes but did not define "substantive". The
user asked whether any rule lets an agent skip review for small changes.

Options: keep the undefined term; define exemptions by size; define them
by what the change can affect; also exempt illustrative figure data or not.

Decision (user, 2026-10-26): exemptions depend on what a change can
affect, not on its size. A change skips review only if it cannot alter a
formula, a claim or a cited number. Exempt: wording, typos, layout, colour,
fonts, label position, file moves, README or AGENTS.md edits, and
illustrative figure data that no claim relies on and whose caption draft
says it is illustrative. Any other change to a generator's data or
parameters needs review. A skipped review is recorded as
"No review: <reason>" at the end of the commit message. If unsure, review.
A house rule was added.

Evidence: AGENTS.md, Agents section and House rules (this edit).

Revisit if: an exempt change later turns out to alter a result or claim,
or illustrative figure data becomes backed by a cited result.

## 2026-10-26 — Figure 1 after B: raw noise (C), true vs projected H (D), replicated RMSE (E)

Context: the user rejected panel C measures in `Z` or the reduced space
(bi-whitening is not introduced in the figure; "energy" was unclear), asked
that panels introduce panel A's elements step by step, and asked Figure 1 to
prime that both scaling and noise model matter (proportional noise expected
to reverse the ranking). An independent Advisor - Codex review was obtained.

Options: lead's Option 1 (C overlays per-gene reliability on B's weights),
Option 2 (weight × relative variance table), Option 3 (negative binomial
bridge), or the reviewer's revised Option 1.

Decision (user): adopt the reviewer's sequence as the working direction.
C: typical noise ÷ expected count against expected count, per noise model.
D: true H against oracle-projected H, noise model × scaling. E: paired,
replicated H oracle RMSE against exposure (Poisson) or noise level
(proportional). Work on C first. Add a normal noise model centred at 0,
with the observed matrix floored at 0. Use a wider background range so
low-count genes are present. The reviewer's proposed house rule is dropped.

Evidence: `artifact/20261026_fig1C-narrative-options.md` (sections 3, 6),
exploratory scripts in ignored `out/20261026_fig1C_explore/` and
`out/20261026_fig1C_noise/`, GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. The ranking reversal was seen
on one signal (10 paired draws per setting) and is not yet a result.

Revisit if: the replicated experiment does not show the reversal, or C's
mock fails to carry the "why" without the weights overlay.

## 2026-10-26 — Figure 1 introduces bi-whitening (A) and shows per-gene squared-noise shares in Z (C)

Context: computing gene noise variance in raw `V` or scaled `Ṽ` cannot show
the scaling effect (raw is identical for both scalings; `Ṽ` under expression
scaling equals raw and points the wrong way). Only `Z` shows it. This
supersedes the previous entry's panel C (raw relative noise against
expected count).

Options: keep `Z` out of the figure, or introduce bi-whitening in A and show
noise in `Z` in C; quartile bars or per-gene rank plots; fixed or independent
replicates; panel A's settings or a wider background range.

Decision (user): add a Bi-whitening step between scaling and projection in
panel A. Panel C: per gene, share of squared noise in `Z` against gene rank by
observed total, as in B; Poisson, proportional and floored normal noise; each
plot its own log y-scale; five independent replicates (signal and noise from
seeds 1–5) with panel A's settings; dots = mean of the i-th ranked gene,
bands = range. Equations go in the figure legend, not the panels. Panel C is a
layout draft; the user will rerun analyses at the end.

Evidence: `artifact/20261026_fig1C-noise-share.md`; `figure/fig1/panelC/`.
GeneralDualSimplex 0.28.0 at `af56ff97da8e38af7c304513c5d26f1c2ff0c910`.
Reviewed by Advisor - Codex (approve with fixes; fixes applied). A and B data
reproduce byte for byte.

Revisit if: the user chooses conditional variance instead of realized
squared perturbations, or a different simulation design for the final run.

## 2026-10-26 — Figure 1C plots each gene's variation in Z (signal and noise), not noise

Context: panel D will bridge C to the projection, and the truncated SVD
minimizes squared reconstruction error, so the user asked for the variance
of genes in `Z` rather than noise. The previous C plotted one draw's squared
noise; a noise-variance version was briefly drafted and withdrawn.

Options: realized squared noise; noise variance `l_g² Σ_i t_i² Var(V_gi)`;
each gene's total variation in `Z`.

Decision (user): y = gene share of `q_g = Σ_i (Z_gi − √(a_g b_i))²`, which sums
to `Σ_{j≥2} σ_j²`. It is weighted variation (inertia), defined in the legend.
Title "Where the variance sits after bi-whitening". Bands and dots share a
colour; dots larger. The discussion note was rewritten around the current
designs (A–E).

Evidence: `artifact/20261026_fig1C-noise-share.md`,
`artifact/20261026_figure1_discussion.md`, `figure/fig1/panelC/`
(`noise_share.R`, `signal_noise_split.R`). Advisor - Codex review approved with
two fixes, both applied. GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`.

Revisit if: the label "variance" misleads readers (use "variation"), or D
shows that the allocation in C does not track the projection error.

## 2026-10-26 — Prototype D with gene simplices and E with five paired oracle errors, PNG only

Context: the user asked to generate D and E from the Figure 1 discussion,
specifying a representative gene simplex for every noise/scaling pair in
D and five draws per pair for E. Output is PNG for layout prototyping.

Options: the discussion's true-versus-oracle H overlays in D and larger
noise-level experiment in E, or the user's simpler layout request.

Decision: follow the user's request. D uses draw 1, selected in advance,
with three noise columns and two scaling rows, in A's gene projection
style. E shows five paired H oracle RMSEs and their arithmetic means per
noise model. Use C's settings and seeds 1–5: each draw has a fresh signal
and noise; both scalings share its observed matrix. This pairing convention
is the lead's implementation choice, stated to the user. D and E remain
illustrative layout prototypes; no benchmark or general ranking is claimed.
Keep equations in the caption note and create no SVGs.

Evidence: `artifact/20261026_fig1DE-png-mock.md`, caption drafts and
“Values and verification”; `figure/fig1/panelD/`, `figure/fig1/panelE/`,
`figure/fig1/fig1DE_mock.png`. GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. The Poisson draw-1 matrix and
gene coordinates reproduce A; H RMSEs were recalculated from saved H
entries. Existing A–C content is preserved.

Advisor - Claude approved the mathematics, data and plotting; minor
caption and figure-text clarifications were applied without changing data
(`artifact/handoff/20261026-0526_claude_fig1DE-png-review.md`).

Revisit if: the user wants noise-only repeats of one fixed signal, a
different representative draw, D insets, or the full final experiment.

## 2026-10-26 — Narrow E, put W oracle error in E and H oracle error in F, skip review at user request

Context: the user approved the paired-draw plot, then requested no
highlighting of D's draws, a narrower panel, W-side oracle RMSE in E,
H-side RMSE in F, and y-axis text “oracle RMSE”.

Options: keep H in E, combine both factors on one scale, or split them.

Decision: follow the requested split. E and F are 100 mm wide instead of
134 mm, retain five paired draws per noise model, and have no draw-1 rings.
Use the original known W in expression units and H in fraction units,
with separate y-ranges. Both are unconstrained Euclidean oracle
projections into the corresponding recovered subspaces. D is unchanged.
The new note records the W derivation and current captions.

Evidence: `artifact/20261026_fig1EF-oracle-png.md`, “Oracle W derivation”
and “Values and checks”; `figure/fig1/panelE/`, `figure/fig1/panelF/`,
`figure/fig1/fig1EF_mock.png`. GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. H data and D PNG/data are
byte-identical to their prior versions; saved W entries reproduce its
RMSEs. All outputs remain illustrative PNG layout drafts.

Review: the user explicitly said “Skip the review; finish the fixes”.
The fresh Claude review was cancelled before a verdict and archived;
local checks were completed. This overrides review for this revision only.

Revisit if: the user requests another width or normalization of W, or
these illustrative values are used for a manuscript claim.

## 2026-10-26 — Match gene labels to W and sample labels to H; make representative D and E/F SVGs

Context: the user approved D's layout after requesting shorter error
labels, rotated scaling labels closer to the plots, “Representative” in
the title, a companion sample simplex, and E/F SVGs. They then asked why
D's values differed from E and requested matching gene plots to W error,
sample plots to H error, including A.

Options: retain the original ambient-profile-space assignment, or assign
oracle targets by the plotted entities for consistency with E/F.

Decision: gene projections A/D report W oracle RMSE; the sample companion
reports H oracle RMSE. Preserve each representative draw and all plotted
coordinates. A/D values match one E point, whereas E's labels are means;
the sample companion similarly matches one F point. Simplify D's labels
to “oracle RMSE: <value>”, rotate scaling text 90°, and move the first
plot column left. Keep D/sample as PNG drafts. Create E/F SVG masters
with editable text/layers and data-only refresh groups. All data remain
illustrative, with no manuscript claim relying on them.

Evidence: `artifact/20261026_fig1D-samples-and-EF-svg.md`, “Provenance and
checks”; `figure/fig1/panelA/`, `panelD/`, `panelD_samples/`, `panelE/`,
`panelF/`. GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. A's SVG differs only in the
two error labels. Its simulation and point/triangle data are unchanged,
as are D coordinates and all E/F data. Sample projection identities and
text bounds were checked, and final PNGs opened. No fresh review under
the illustrative-data/layout exemption and the user's skip-review request.

Revisit if: the user wants normalized rather than native-unit W error,
estimated rather than known vertices, or these drafts support a claim.

## 2026-10-26 — Finalize D/S SVGs, remove panel footers and obtain fresh review before commit

Context: the user asked to remove the “Draw 1…” footer from D and S,
generate their SVGs, remove bottom notes from E/F, and send the completed
work to a reviewer before committing.

Options: retain PNG-only D/S drafts, or make all four projections/error
panels editable SVG masters with the requested text reduction.

Decision: create D/S masters at 119 × 107 mm, keep their legends and
separate-scale note, and remove the draw footer. Remove all three
explanatory bottom notes from E/F and trim their canvases to 100 × 54 mm.
Preserve axes, data and W/H assignments. Put replicate, pairing and
illustrative-data information in the captions. Generators update named
data groups only; preview rendering uses the masters. The latest review
request supersedes the earlier skip-review instruction.

Evidence: `artifact/20261026_fig1_svg-final.md`, current captions and
validation; handoff
`artifact/handoff/20261026-0603_claude_fig1-ADS-EF-final-review.md`.
GeneralDualSimplex 0.28.0 at
`af56ff97da8e38af7c304513c5d26f1c2ff0c910`. Input CSVs are unchanged;
all four PNGs were opened, all text/point bounds fit, and SVG data refresh
leaves the masters byte-identical.

Revisit if: supplementary placement changes, the user edits SVG layout,
or the final analyses replace the illustrative data.

Fresh review outcome: Advisor - Claude approved for commit with no
blocking findings (`out/20261026_fig1_final_review/review.md`). It checked
the W/H oracle spaces independently, all saved RMSEs and displayed values,
SVG refresh preservation, renders and bounds. Optional caption unit/vertex
clarifications and a stale generator header were fixed; data and SVGs did
not change after review. The reviewer's final message was read and the
agent archived before committing.
