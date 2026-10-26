# Handoff: Figure 1 narrative after panel B (independent suggestions)

- Recipient: Advisor - Codex (reviewer role; independent second opinion)
- Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
- Paseo workspace: `wks_eae2eb8dafb28fa0`
- Lead: Claude (Opus 5.5), 2026-10-26 03:35

## Task

Suggest how Figure 1 should convey its message **from panel C onward**, or
propose a different narrative. This is a thinking-partner task, not an
approval review. Read-only: do not edit, stage or commit any file. You may
run R or Python to explore, writing only into
`out/20261026_fig1_narrative_codex/` (ignored). Package
`/workspace/dual_simplex_functional/general_dual_simplex` is read-only.

## Work in this order, to keep your view independent

1. Read `AGENTS.md`, then `README.md` (Mathematical Notation), and look at
   the figures by opening the images: `figure/fig1/panelA/fig1A.png`,
   `figure/fig1/panelB/fig1B.png`, and the user's conceptual mock
   `/data/figure1_mock.png` (invented values).
2. Read the user's constraints below and form **your own** proposal before
   reading the lead's.
3. Then read the lead's record `artifact/20261026_fig1C-narrative-options.md`
   and the background `artifact/20261026_figure1_discussion.md`. Check the
   lead's derivations (sections 3.2–3.4) and exploratory scripts in
   `out/20261026_fig1C_explore/` (`noise_models.R`, `reliability.R`,
   `displacement.R`).

## User constraints (stated 2026-10-26)

- No metric in `Z = D_a^(-1/2) Ṽ D_b^(-1/2)` or in the reduced space: the
  figure never introduces that step, and such metrics complicate the story.
  The word "energy" was found unclear.
- Introduce panel A's elements step by step. Panel B now explains scaling
  visually. The next panel should prime why a scaling is bad or good, and
  bridge to projection and the final RMSE.
- Figure 1 should also prime that **both the scaling and the noise model
  matter**: with proportional noise the effect is expected to reverse.

## Please return

1. Your proposed panel sequence from C onward: per panel, the reader
   question, the display (axes, marks), and the one-sentence take-home.
2. Your critique of the lead's options 1–3: what works, what misleads, and
   which you would choose.
3. Mathematical or evidence errors in the lead's record, with file and
   line.
4. The minimum experiments needed before any panel's claim is supportable
   (signals, draws, noise levels), and any primary literature that should
   be checked (do not cite from memory; give what to look for).
5. Open questions for the user.

Keep it compact; the user reads on a phone. Result first.
