# Handoff: review Figure 1 panels A (bi-whitening edit), B and C (draft)

- Recipient: Advisor - Codex (reviewer role)
- Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
- Paseo workspace: `wks_eae2eb8dafb28fa0`
- Lead: Claude (Opus 5.5), 2026-10-26 04:40
- Package: GeneralDualSimplex 0.28.0 at
  `af56ff97da8e38af7c304513c5d26f1c2ff0c910` (no uncommitted `R/`/`src/`),
  `/workspace/dual_simplex_functional/general_dual_simplex`, read-only.

## Task

Review before commit. Read-only: do not edit, stage or commit. Exploratory
outputs only under `out/20261026_fig1ABC_review_codex/`. Read `AGENTS.md`
first. Return a verdict (approve / approve with fixes / reject), findings with
file and line, and open questions. Result first; compact.

## Scope

1. **Panel A edit** (`git diff figure/fig1/panelA/fig1A.svg`; backup before
   the edit: `out/20261026_fig1_backups/fig1A_01.svg`; one-off edit script
   `out/20261026_fig1_backups/edit_fig1A_biwhitening.py`). A "Bi-whitening"
   box was added between scaling and rank-k projection in both branches. The
   Noise box was narrowed; heatmap V, its labels and the fork moved 6 mm left.
   Check: the step order matches the package pipeline (README notation
   `Z = D_a^(-1/2) Ṽ D_b^(-1/2)`; `FindProjection`); nothing else changed
   (data groups, RMSE labels); the generator `make_fig1A.py` still refreshes
   data groups correctly (heatmap_Y group now has `transform`); text inside
   boxes and canvas (`inkscape --query-all`); open `fig1A.png`.
   Data files were regenerated with `points.R` and are byte-identical to the
   committed ones.
2. **Panel B** (`figure/fig1/panelB/`, never reviewed, untracked): `mass.R`,
   `make_fig1B.py`, CSVs, `fig1B.svg/png`, record
   `artifact/20261026_fig1B-rank-log-share.md`; archived cumulative version
   in `archive/20261026_cumulative/` and
   `artifact/20261026_fig1B-cumulative-mass.md`. Check formulas, data,
   claims in the record and labels against the code.
3. **Panel C draft** (`figure/fig1/panelC/`, new): `noise_share.R`,
   `noise_share_by_rank.csv`, `fig1C_draft.png/svg`. Check the noise-in-Z
   formula `N = D_l (V − μ) D_t`, `l = r/√a`, `t = c/√b`, against the package
   scaling code (`R/dso-scaling.R`) and README; the three noise generators
   and their matching rule; the claim that replicate 1 with Poisson noise
   reproduces panel A's observed matrix (the script asserts it); the
   rank-wise averaging across independent replicates; and whether the plot,
   title ("Where the noise sits after bi-whitening") and caption say only
   what the data support. Rerun the script and compare the CSV.
4. **Records**: `artifact/20261026_fig1C-narrative-options.md` (sections 3,
   6), the 2026-10-26 Figure 1 entry at the end of `artifact/decisions.md`,
   `artifact/20261026_figure1_discussion.md`. Flag statements the evidence
   does not support. Note that section 4's Option 1 and the bar/`Z`
   discussion were superseded by the user's later choice (panel C in `Z`,
   per-gene rank plot).

## Context

The user chose to introduce `Z` (bi-whitening) in panel A so that panel C
can show noise in `Z`. Panel C is a layout draft for discussion; the user
will rerun the analyses at the end. Equations will go in the figure legend,
not the panels. All data are illustrative simulations.
