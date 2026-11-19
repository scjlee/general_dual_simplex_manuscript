# Figure 2 working draft

Panels a and b are separate editable SVG masters, drawn from the user's draft
of 2026-11-19 (`261119_figure2_draft.pdf`, pages 3–4). Panel c is not drawn yet.

| Panel | Master | Generator | Size |
|---|---|---|---|
| a, pipeline | `panelA/fig2A.svg` | `panelA/make_fig2A.py` | 176 × 29.2 mm |
| b, factorization of Ṽ | `panelB/fig2B.svg` | `panelB/make_fig2B.py` | 176 × 34.4 mm |

`fig2A.pdf`/`.png` and `fig2B.pdf`/`.png` are previews (PNG at 600 dpi).
Each panel folder holds `input_data.json` (all illustrative matrices) and
`package_commit.txt`. The shared matrices and drawing helpers are in
`schematic.py`; b's Ṽ is the same matrix as a's Ṽ.

Run from the repository root, once, before any hand edit:

```sh
python3 -B figure/fig2/panelA/make_fig2A.py
python3 -B figure/fig2/panelB/make_fig2B.py
```

The generators open the SVG with mode `x` and stop if it exists: after the
first hand edit the SVG is the master.

## Style

Follows Figure 1a/b: Liberation Sans, 6 pt text, bold symbols with plain
words, 8 pt operator; grey rounded step boxes (`#f2f2f2`, `#404040` outline);
black 0.5 pt matrix frames, 0.4 pt white cell lines, 0.6 pt arrows; dashed
outline around the generative model W H = V as in Figure 1b. Colours: W and
W̃ `#D55E00`, H and H̃ `#0072B2` (as Figure 1b), V, Ṽ and Z on Figure 1b's
`#56B4E9`–`#009E73`–`#E69F00` scale, M `#CC79A7`. Panel letters are left to
the assembly, as in Figure 1. Every object has a readable id prefixed `A_`
or `B_`, grouped in Inkscape layers.

## Choices made while drawing (open for the user)

- Step headers read "Prescribed marginal scaling" and "Bi-marginal whitening";
  the draft's circled numbers 1 and 2 are omitted.
- In b, symbols sit above the matrices (Figure 1 style) rather than on top
  of them as in the page-4 example; "Column marginal = **b**" sits above Ṽ's
  label and "Row marginal = **a**" runs along Ṽ's left side.
- The page-4 example reads "Row marginal = b"; the handwritten draft and
  README.md define the row marginal as **a** = Ṽ**1**, so b uses **a**.
- "Columns of W̃ sum to 1s" is written "Columns of W̃ sum to 1" (same for H̃).
- Not drawn yet, as requested: the dashed box around b's factorization and
  the zoom lines from a's Ṽ. Space is left for them around b's matrices.
- The note on page 4 (any common value c for sum(M), sum(Ṽ), sum(a), sum(b);
  c = 1 is used) is not in the artwork; it may belong in the legend or text.
