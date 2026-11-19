# Review: Figure 2a and 2b schematics

Recipient: Codex reviewer (profile Advisor - Codex). Role: Reviewer, read-only.
Repository: `/workspace/dual_simplex_functional/general_dual_simplex_manuscript`
(Paseo workspace `wks_abf130d2b9ce4603`). Read `AGENTS.md` and the
"Mathematical Notation" section of `README.md` first.

## Files to review (all new, uncommitted)

- `figure/fig2/schematic.py`: illustrative matrices and SVG helpers.
- `figure/fig2/panelA/make_fig2A.py`, `panelA/fig2A.svg` (+ `.png`, `.pdf`).
- `figure/fig2/panelB/make_fig2B.py`, `panelB/fig2B.svg` (+ `.png`, `.pdf`).
- `figure/fig2/README.md`, `figure/fig2/caption_notes.md`.
- The user's draft: `/home/paseo/.paseo/uploads/upload_424174b8-3bbd-4c7f-8651-978ffb648ac1/261119_figure2_draft.pdf`
  (page 3: hand sketch of a and b; page 4: example schema of b).

Write your review only to `out/20261119_fig2_ab/review.md`. Edit nothing
else. Do not regenerate the SVGs (the generators refuse to overwrite them);
to rerun, copy the generators to a scratch directory under `out/`.

## Purpose

The user asked for panels a and b as two editable SVGs following the draft,
in Figure 1's style (`figure/fig1/figure1.png`, `figure/fig1/panelB/make_fig1B_schematic.py`).
Matrix values are illustrative; the caption notes say so.

## Check

1. Mathematics. The "Key properties" box in b states: columns of W̃ sum to 1;
   rows of H̃ sum to 1; diagonal of M sums to 1; sum(a) = sum(b) = 1, with
   sum(Ṽ) = 1. Check each against README.md's definitions. Check that
   `schematic.py` computes Ṽ = D_r V D_c (Sinkhorn to prescribed a, b),
   Z = D_a^(-1/2) Ṽ D_b^(-1/2), W̃, H̃ and M as README.md defines them, and
   that Ṽ = W̃ M H̃ holds for V = WH. Check the printed numbers in
   `out/20261119_fig2_ab/panelA.log` against `caption_notes.md`.
2. Labels. "Row marginal = a" (the page-4 example says b; README.md defines
   a = Ṽ1 as the row marginal) and "Column marginal = b". Are the labels,
   symbols and step names faithful to the draft? List any deviation.
3. Statements. Anything in `README.md` or `caption_notes.md` of fig2 that the
   code or evidence does not support (for example "W and H repeat the Figure 1b
   draws", the tolerance numbers, the colour-mapping description).
4. Figure rules from AGENTS.md: text 5–8 pt real text, lines 0.4–0.6 pt,
   mm viewBox, layers, readable unique ids, `x`/`y` on line tspans. Open the
   PNGs and confirm text lies inside its box.
5. Style: README.md "Coding style guides".

## Return

Verdict (approve / approve with changes / reject), findings with file and
line, severity, and open questions. Put the full review in the file above
and a short summary in your last message.
