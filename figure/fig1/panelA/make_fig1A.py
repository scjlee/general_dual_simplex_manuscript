"""Panel A schematic as an Inkscape-editable SVG (1 user unit = 1 mm).

Usage (repo root): python3 figure/fig1/panelA/make_fig1A.py
Inputs: tiles.csv and points_frac0.1_seed1.csv from points.R. Output: fig1A.svg.
It rewrites the whole file, so running it now would erase the user's hand edits to fig1A.svg.
Change it to replace only the heatmap_* and scatter_* groups by id before running it again.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent
POINTS = HERE / "points_frac0.1_seed1.csv"
PT = 0.3528  # mm per point
W_MM, H_MM = 134, 67
FONT = "Liberation Sans, Arial, Helvetica, sans-serif"

ORANGE, ORANGE_LIGHT, ORANGE_DARK = "#E07B28", "#FBE3CF", "#B85A12"
BLUE, BLUE_LIGHT, BLUE_DARK = "#2A7BBF", "#D6E6F4", "#1B5C93"
GREY_TRUTH, LINE, BOX_FILL, INK = "#B8B8B8", "#4D4D4D", "#F2F2F2", "#1A1A1A"
CELL = 1.8
CY = 33.2  # pipeline centre line
Y_TOP, Y_BOT = CY - 15.2, CY + 15.2  # branch rows

layers = {name: [] for name in ["Heatmaps", "Boxes", "Arrows", "Scatter", "Labels", "Title"]}


def text(layer, id_, x, y, lines, size=6, weight="normal", anchor="middle", fill=INK, rotate=None, style=""):
    lines = [lines] if isinstance(lines, str) else lines
    fs = size * PT
    y0 = y - (len(lines) - 1) * fs * 1.15 / 2
    tspans = "".join(
        f'<tspan sodipodi:role="line" x="{x:.2f}" y="{y0 + i * fs * 1.15:.2f}">{s}</tspan>' for i, s in enumerate(lines))
    rot = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate else ""
    layers[layer].append(
        f'<text id="{id_}" xml:space="preserve" x="{x:.2f}" y="{y0:.2f}" style="font-family:{FONT};font-size:{fs:.3f}px;'
        f'line-height:1.15;font-weight:{weight};text-anchor:{anchor};fill:{fill};{style}"{rot}>{tspans}</text>')


def arrow(id_, d):
    layers["Arrows"].append(
        f'<path id="{id_}" d="{d}" style="fill:none;stroke:{LINE};stroke-width:{0.6 * PT:.3f};marker-end:url(#arrowhead)"/>')


def box(id_, x, y, w, h, lines, fill=BOX_FILL, stroke="#808080", color=INK, weight="normal"):
    layers["Boxes"].append(
        f'<g id="{id_}" inkscape:label="{id_}"><rect id="{id_}_rect" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'rx="0.8" style="fill:{fill};stroke:{stroke};stroke-width:{0.5 * PT:.3f}"/></g>')
    text("Labels", f"{id_}_label", x + w / 2, y + h / 2 + 0.55, lines, weight=weight, fill=color)


def grey(v):
    lo, hi = 0xF4, 0x33
    g = round(lo + (hi - lo) * v)
    return f"#{g:02X}{g:02X}{g:02X}"


tiles = {}
with open(HERE / "tiles.csv") as f:
    for r in csv.DictReader(f):
        tiles.setdefault(r["matrix"], []).append((int(r["row"]), int(r["col"]), float(r["value"])))


def heatmap(name, x, y):
    cells = tiles[name]
    nr, nc = max(c[0] for c in cells), max(c[1] for c in cells)
    rects = "".join(
        f'<rect x="{x + (c - 1) * CELL:.2f}" y="{y + (r - 1) * CELL:.2f}" width="{CELL}" height="{CELL}" '
        f'style="fill:{grey(v)};stroke:#FFFFFF;stroke-width:0.1"/>' for r, c, v in cells)
    frame = (f'<rect x="{x:.2f}" y="{y:.2f}" width="{nc * CELL:.2f}" height="{nr * CELL:.2f}" '
             f'style="fill:none;stroke:#666666;stroke-width:{0.4 * PT:.3f}"/>')
    layers["Heatmaps"].append(f'<g id="heatmap_{name}" inkscape:label="heatmap {name}">{rects}{frame}</g>')
    return nc * CELL, nr * CELL


# --- truth: W (genes x k) over H (k x samples), joined by a brace -------------------------------
hx = 3.0
wx = hx + 4 * CELL - 1.5 * CELL
w_w, w_h = heatmap("W", wx, 19.5)
text("Labels", "label_W", wx + w_w / 2, 18.4, "<tspan style='font-style:italic;font-weight:bold'>W</tspan> (profiles)", size=6.5)
text("Labels", "label_W_rows", wx - 1.0, 19.5 + w_h / 2, "Genes", size=5.5, rotate=-90)
text("Labels", "label_W_cols", wx + w_w / 2, 19.5 + w_h + 2.3, "Components", size=5.5)
h_y = 41.5
h_w, h_h = heatmap("H", hx, h_y)
text("Labels", "label_H", hx + h_w / 2, h_y - 1.1, "<tspan style='font-style:italic;font-weight:bold'>H</tspan> (proportions)", size=6.5)
text("Labels", "label_H_cols", hx + h_w / 2, h_y + h_h + 2.3, "Samples", size=5.5)
text("Labels", "label_H_rows", hx - 1.0, h_y + h_h / 2, "k", size=5.5, rotate=-90, style="font-style:italic;")

bx, by0, by1, d = 19.6, 19.5, h_y + h_h, 1.1
ym = (by0 + by1) / 2
layers["Arrows"].append(
    f'<path id="brace_truth" d="M {bx},{by0} q {d},0 {d},{d} V {ym - d} q 0,{d} {d},{d} q {-d},0 {-d},{d} '
    f'V {by1 - d} q 0,{d} {-d},{d}" style="fill:none;stroke:{LINE};stroke-width:{0.5 * PT:.3f}"/>')
arrow("arrow_truth_to_X", f"M {bx + 2 * d + 0.4},{CY} H 25.4")

# --- expected counts X, exposure/noise, observed Y ---------------------------------------------
xx, top = 26.0, CY - 4 * CELL
x_w, x_h = heatmap("X", xx, top)
text("Labels", "label_X", xx + x_w / 2, top - 1.3, "<tspan style='font-style:italic'>X</tspan> = <tspan style='font-style:italic'>WH</tspan>", size=7, weight="bold")
text("Labels", "label_X_desc", xx + x_w / 2, top - 4.2, "Expected counts", size=6)
text("Labels", "label_X_cols", xx + x_w / 2, top + x_h + 2.3, "Samples", size=5.5)

ex, ew, eh = 44.4, 15.0, 4.4
y_exp, y_noise = CY - 3.6, CY + 3.6
arrow("arrow_X_to_exposure", f"M {xx + x_w + 0.6},{y_exp} H {ex - 0.4}")
box("box_exposure", ex, y_exp - eh / 2, ew, eh, "Exposure")
arrow("arrow_exposure_to_noise", f"M {ex + ew / 2},{y_exp + eh / 2} V {y_noise - eh / 2 - 0.3}")
box("box_noise", ex, y_noise - eh / 2, ew, eh, "Poisson noise")

yx = 62.8
arrow("arrow_noise_to_Y", f"M {ex + ew},{y_noise} H {yx - 0.4}")
y_w, y_h = heatmap("Y", yx, top)
text("Labels", "label_Y", yx + y_w / 2, top - 1.3, "<tspan style='font-style:italic'>Y</tspan>", size=7, weight="bold")
text("Labels", "label_Y_desc", yx + y_w / 2, top - 4.2, "Observed counts", size=6)
text("Labels", "label_Y_cols", yx + y_w / 2, top + y_h + 2.3, "Samples", size=5.5)

# --- branch: scaling -> rank-k projection -> oracle simplex ------------------------------------
fork = 80.0
layers["Arrows"].append(
    f'<path id="fork" d="M {yx + y_w + 0.6},{CY} H {fork} M {fork},{Y_TOP} V {Y_BOT}" '
    f'style="fill:none;stroke:{LINE};stroke-width:{0.6 * PT:.3f}"/>')

pts = {}
with open(POINTS) as f:
    for r in csv.DictReader(f):
        h1, h2, h3 = float(r["h1"]), float(r["h2"]), float(r["h3"])
        pts.setdefault(r["set"], []).append(((h2 - h3) / math.sqrt(2), (2 * h1 - h2 - h3) / math.sqrt(6)))


def rmse(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))


hs = {}
with open(POINTS) as f:
    for r in csv.DictReader(f):
        hs.setdefault(r["set"], []).extend(float(r[c]) for c in ("h1", "h2", "h3"))

allp = [p for v in pts.values() for p in v]
c1_max = max(abs(p[0]) for p in allp) * 1.06
c2_lo, c2_hi = min(p[1] for p in allp), max(p[1] for p in allp)
pad = 0.06 * (c2_hi - c2_lo)
c2_lo, c2_hi = c2_lo - pad, c2_hi + pad
span = max(2 * c1_max, c2_hi - c2_lo)  # equal aspect ratio

sx, sw = 115.6, 15.0
for key, label, light, dark, colour, yc in [
        ("uniform", "Uniform", ORANGE_LIGHT, ORANGE_DARK, ORANGE, Y_TOP),
        ("expression", "Expression", BLUE_LIGHT, BLUE_DARK, BLUE, Y_BOT)]:
    arrow(f"arrow_fork_to_{key}", f"M {fork},{yc} H 82.6")
    box(f"box_scaling_{key}", 83.0, yc - 3.2, 13.6, 6.4, [label, "scaling"], fill=light, stroke=colour, color=dark, weight="bold")
    arrow(f"arrow_{key}_to_projection", f"M 96.6,{yc} H 99.2")
    box(f"box_projection_{key}", 99.6, yc - 3.2, 12.5, 6.4, ["Rank-<tspan style='font-style:italic'>k</tspan>", "projection"])
    text("Labels", f"label_rmse_{key}", 105.85, yc + 5.6, f"oracle RMSE {rmse(hs[key], hs['truth']):.3f}", size=5, fill="#555555")
    arrow(f"arrow_projection_to_scatter_{key}", f"M 112.1,{yc} H {sx - 0.4}")

    fy = yc - sw / 2
    inner = sw - 1.6

    def to_xy(p):
        return (sx + 0.8 + (p[0] + span / 2) / span * inner,
                fy + 0.8 + (c2_hi - p[1]) / span * inner + (inner - (c2_hi - c2_lo) / span * inner) / 2)

    verts = [to_xy(p) for p in [(0, 2 / math.sqrt(6)), (1 / math.sqrt(2), -1 / math.sqrt(6)), (-1 / math.sqrt(2), -1 / math.sqrt(6))]]
    simplex = (f'<path id="simplex_{key}" d="M {verts[0][0]:.2f},{verts[0][1]:.2f} L {verts[1][0]:.2f},{verts[1][1]:.2f} '
               f'L {verts[2][0]:.2f},{verts[2][1]:.2f} Z" style="fill:none;stroke:#999999;stroke-width:{0.4 * PT:.3f};stroke-dasharray:0.6,0.4"/>')
    truth = "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.28"/>' for x, y in map(to_xy, pts["truth"]))
    oracle = "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.28"/>' for x, y in map(to_xy, pts[key]))
    frame = (f'<rect id="frame_{key}" x="{sx}" y="{fy:.2f}" width="{sw}" height="{sw}" '
             f'style="fill:#FFFFFF;stroke:{colour};stroke-width:{0.6 * PT:.3f}"/>')
    layers["Scatter"].append(
        f'<g id="scatter_{key}" inkscape:label="scatter {key}">{frame}{simplex}'
        f'<g id="points_truth_{key}" inkscape:label="truth points" style="fill:{GREY_TRUTH}">{truth}</g>'
        f'<g id="points_oracle_{key}" inkscape:label="oracle points" style="fill:{colour};fill-opacity:0.85">{oracle}</g></g>')
    text("Labels", f"label_c1_{key}", sx + sw / 2, fy + sw + 2.2, "Contrast 1", size=5)
    text("Labels", f"label_c2_{key}", sx + sw + 1.6, yc, "Contrast 2", size=5, rotate=90)

# --- title and caption -------------------------------------------------------------------------
text("Title", "panel_letter", 1.2, 5.2, "A", size=10, weight="bold", anchor="start")
text("Title", "panel_title", 7.0, 5.0, "One mixture, two projection geometries", size=8, weight="bold", anchor="start")
text("Title", "caption", 67.0, 62.6, "Same latent signal. Same observed matrix. Different weighting.", size=6.5, weight="bold")
text("Title", "legend_note", 67.0, 65.4,
     f"Grey: true <tspan style='font-style:italic'>H</tspan>; colour: oracle projection of <tspan style='font-style:italic'>H</tspan> onto the rank-3 space "
     f"(Poisson, library fraction 0.1, seed 1).", size=5, fill="#555555")

defs = (f'<defs><marker id="arrowhead" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto" '
        f'markerUnits="strokeWidth"><path d="M 0,0 L 5,2.5 L 0,5 Z" style="fill:{LINE};stroke:none"/></marker></defs>')
body = "".join(
    f'<g id="layer_{n.lower()}" inkscape:groupmode="layer" inkscape:label="{n}">{"".join(items)}</g>' for n, items in layers.items())
svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
       f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
       f'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
       f'width="{W_MM}mm" height="{H_MM}mm" viewBox="0 0 {W_MM} {H_MM}">'
       f'<sodipodi:namedview inkscape:document-units="mm"/>{defs}{body}</svg>\n')
(HERE / "fig1A.svg").write_text(svg)
print("wrote", HERE / "fig1A.svg")
