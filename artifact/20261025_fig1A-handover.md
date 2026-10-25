# Figure 1 panel A: handover to `general_dual_simplex_manuscript`

Copied 2026-10-25 from the package repository, `.ai/20261025_fig1A-handover.md` at commit
c8fba150b2a8df6092fe8c2854b0f19914940f89. Links and paths below
refer to the package repository. In this repository the panel lives in `figure/fig1/panelA/`; `points.R`
now uses the installed package from this renv and reproduces `tiles.csv` and `points_frac0.1_seed1.csv`
byte for byte.

Written 2026-10-25 by the package thinking partner (Claude). Figure work moves to the manuscript repository
([decision](decisions.md#2026-10-25--figure-work-moves-to-the-manuscript-repo-with-its-own-renv-package-ai-is-read-only-there)).
Copy this note into the manuscript `artifact/` and cite the package commit that contains it.

## State

- Prototype: `.ai/figures/fig1A/` in the package repo, first committed at e3d15c66812d1d8ae1bd3e5cc16aff59c648770c.
  This copy is frozen; continue in the manuscript repo.
- Files: `fig1A.svg` (master), `make_fig1A.py` (generator, Python stdlib), `points.R` (data),
  `tiles.csv`, `points_frac0.1_seed1.csv`, `fig1A.pdf` / `fig1A.png` (previews, made before the user's edit).
- Layout model: panel A of the user's mock `/data/figure1_mock.png` ("One mixture, two projection geometries").
- User edit (Inkscape, 2026-10-25): `label_X` "X = WH" → "V* = WH"; `label_Y` "Y" → "V". Nothing else moved.
  The new V and V* are bold upright; only "WH" kept italics. Ask whether V/V* should be italic.

## Data provenance

- `points.R` ran from the package root with `devtools::load_all()` on package 0.28.0 at
  e73fef4620adf03da7c46cbf2101724194adc329 (no uncommitted changes in `R/` or `src/`).
- Setting copied from `.ai/bench/20261022_space-distortion.R`: `GenerateMixture(500, 200, 3, n_marker = 20,
  marker_fold = 5, profile_spread_sd = 0.2)`, `ApplyNBNoise(dispersion = 0, library_size_fraction = 0.1)`, seed 1,
  `ScaleDSO(type = "uniform" | "expression")`, `FindProjection(k = 3, method = "svd")`.
- Scatter: oracle projection of the true H onto the estimated H space, span(Psi D_b D_c^-1). Axes:
  contrast 1 = (h2 − h3)/√2, contrast 2 = (2h1 − h2 − h3)/√6. Oracle columns do not sum to 1 (max |colsum − 1|
  0.096 uniform, 0.073 expression), so contrasts are used rather than renormalised barycentric coordinates.
- Oracle RMSE, seed 1: uniform 0.0815, expression 0.0634. Benchmark medians over 10 seeds: 0.084 and 0.063.
  At library fraction 0.02: 0.2170 and 0.1529 (seed 1, not kept).
- Heatmaps: real W, H, X = WH and the same Poisson Y used for the projection. Genes: marker1.1–3.2 (2 per
  component) plus the first 2 background rows; 8 samples (3, 3, 2 per dominant component). Each matrix is
  log1p-rescaled to [0, 1] on its own; grey ramp #F4F4F4 → #333333.
- These are illustrative figure data. A number cited as evidence in the text needs an experiment-repo commit.

## SVG conventions

- 134 × 67 mm canvas, `viewBox` in mm (1 user unit = 1 mm). Text 5–8 pt (pt × 0.3528 = px in the file),
  Liberation Sans → Arial → Helvetica. Lines 0.4–0.6 pt.
- Inkscape layers: Heatmaps, Boxes, Arrows, Scatter, Labels, Title. Every object has a readable id
  (`box_noise`, `arrow_X_to_exposure`, `points_oracle_uniform`, `label_rmse_expression`, ...).
- Colours: uniform #E07B28 (fill #FBE3CF, text #B85A12); expression #2A7BBF (fill #D6E6F4, text #1B5C93);
  truth points #B8B8B8; lines #4D4D4D.
- Multi-line text uses `<tspan sodipodi:role="line">`. The `<text>` element must also carry `x`/`y`;
  otherwise Inkscape stacks every line at the origin.
- After the first hand edit the SVG is the master. `make_fig1A.py` still rebuilds the whole file and would
  erase it. Change the generator to replace only the data groups (`heatmap_*`, `scatter_*`) by id inside the
  existing SVG before using it again.

## Tooling (container)

- Inkscape 1.4.4 runs headless. The GTK warnings ("Failed to wrap object of type 'PangoFT2FontMap'") are harmless.
  - Preview: `inkscape fig.svg --export-type=png --export-dpi=600 -o fig.png`, and `--export-type=pdf`.
  - Crop: `--export-area=x0:y0:x1:y1` (user units).
  - Fit check: `inkscape --query-all fig.svg` gives id,x,y,w,h in px at 96 dpi (× 25.4/96 → mm). Check every
    text item is inside the canvas and box labels are inside their `_rect` (≥ 1.1 mm margin at present).
- Fonts installed: `fonts-liberation2`. No other renderer (rsvg, cairosvg, magick, ghostscript) is installed.
- Inkscape re-saves the file pretty-printed (thousands of diff lines). Diff the meaning instead: compare
  `--query-all` boxes and `<text>` contents by id between `git show HEAD:<file>` and the working copy.

## Editing loop with the user

- The user edits on the host in Inkscape and saves as **Inkscape SVG**; the agent edits the same file from
  the container. Turn-taking: user saves → agent edits → user uses File → Revert. Inkscape does not reload.
- Keep a numbered copy before each agent edit. Refer to objects by id.
- No Inkscape MCP: the container has no display, and the community servers are unvetted dependencies.
  Revisit only if the user wants live, selection-based edits on the host.

## Open questions for the user

- Library fraction for the scatters: 0.1 (benchmark setting, modest visual gap 0.082 vs 0.063) or 0.02
  (wider gap 0.217 vs 0.153, but both clouds spread). Or let panel B carry the comparison.
- Italic V and V*?
- Panel width: 134 mm assumes panel A takes about two thirds of a 180 mm double-column figure.
