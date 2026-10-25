# Figure 1A: preserve the SVG master when refreshing data

Starting manuscript commit: `cfe53929a7c2a5f891dbcdcd2145af6bb0a062a7`.
The data CSVs, `points.R`, package provenance and rendered previews are unchanged.
The numbered pre-edit master is `out/20261025_fig1A_update/backup_001.svg`
(ignored scratch output).

## Change

`figure/fig1/panelA/make_fig1A.py` reads the existing master and locates
`heatmap_W`, `heatmap_H`, `heatmap_X`, `heatmap_Y`, `scatter_uniform` and
`scatter_expression` by XML id. It replaces only their contents. It preserves
the groups' opening and closing tags, including transforms, and every byte
outside their contents. It never creates a new SVG document. Generated tiles
and points now have readable, deterministic ids. Missing, repeated or nested
data groups, invalid XML and duplicate output ids are rejected before writing.

All label-generation and document-generation code was removed. RMSE values
are printed for checking the separate master labels when data change; the
script does not update those labels. The historical CSV keys X/Y remain
independent of displayed matrix symbols.

The user confirmed `V* = WH` for true signal and `V` for observed data.
The SVG already uses those labels. README now records the same convention
and makes explicit that its existing noiseless formulas use `V = V*`.

## Verification

Run from the repository root:

```sh
inkscape figure/fig1/panelA/fig1A.svg --export-type=png --export-dpi=600 -o out/20261025_fig1A_update/before.png
inkscape --query-all figure/fig1/panelA/fig1A.svg > out/20261025_fig1A_update/before_query.csv
python3 figure/fig1/panelA/make_fig1A.py
inkscape figure/fig1/panelA/fig1A.svg --export-type=png --export-dpi=600 -o out/20261025_fig1A_update/after_data.png
inkscape --query-all figure/fig1/panelA/fig1A.svg > out/20261025_fig1A_update/after_data_query.csv
```

- All 28 `<text>` elements, including their contents and attributes, match
  the backup by id. All 67 text/tspan query rows match exactly by id.
- Masking the six data-group contents gives byte-identical before/after SVGs.
- Before/after 600 dpi PNG files are byte-identical. Both were opened and
  visually inspected. The tracked `fig1A.png` also matches the new render.
  PNG SHA256: `a53088bab9a40ab6cca529f1043b4ad95a32db5964798b358ff93baa25b7b3c8`.
- All text bounding boxes lie inside the canvas. The six box labels lie
  inside their rectangles, with minimum margin greater than 1.07 mm.
- A second actual generator run leaves the SVG byte-identical.
- An in-memory changed payload preserves an added group transform and all
  bytes outside data contents. A missing target id raises an error.

Raw query outputs and short verification summaries are in the ignored
`out/20261025_fig1A_update/` folder. The large SVG line diff comes from
replacing Inkscape-formatted data contents with compact generated elements;
labels and other document content retain their original bytes.
