"""Write or refresh the Figure 1C SVG: per-gene share of the variance in Z after bi-whitening.

Usage (repo root): python3 figure/fig1/panelC/make_fig1C.py
Input: noise_share_by_rank.csv from noise_share.R. One plot per noise model, each with
its own log y-range. x = gene rank by observed total within each replicate; dot = mean
share of the i-th ranked gene over the replicates; band = min-max over the replicates.
If fig1C.svg is absent, a first draft with all labels is written. Once it exists it is
the master: only the contents of the data groups band_<model>_<scaling> and
points_<model>_<scaling> are replaced by id (panel A's replace_data); labels are left
alone and the values they need are printed.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "panelA"))
from make_fig1A import replace_data  # noqa: E402

PT = 0.3528  # mm per point
FONT = "font-family:Liberation Sans, Arial, Helvetica, sans-serif;line-height:1.15"
UNIFORM, EXPRESSION = "#E07B28", "#2A7BBF"  # panel A branch colours
DOT = {"uniform": "#B85A12", "expression": "#1B5C93"}  # darker dots over light bands (panel A label colours)
INK, MUTED, AXIS, GRID = "#1A1A1A", "#555555", "#666666", "#E3E3E3"
W, H = 134.0, 67.0
Y0, Y1 = 12.5, 48.5  # plot area top and bottom
PLOT_W = 33.0
X_TICKS = (1, 100, 200, 300, 400, 500)
# model key: (CSV name, plot title, plot left edge, log y-range in %, y ticks)
MODELS = {
    "poisson": ("Poisson", "Poisson", 13.0, (0.02, 2.0), (0.03, 0.1, 0.3, 1)),
    "proportional": ("Proportional", "Proportional", 55.5, (0.01, 1.0), (0.01, 0.03, 0.1, 0.3, 1)),
    "normal": ("Normal, floored at 0", "Normal, floored at 0", 98.0, (0.01, 1.0), (0.01, 0.03, 0.1, 0.3, 1)),
}
SCALINGS = (("expression", "Expression", EXPRESSION), ("uniform", "Uniform", UNIFORM))  # uniform on top


class Plot:
    def __init__(self, x0, n, y_range):
        self.x0, self.n = x0, n
        self.y_min, self.y_max = y_range

    def px(self, rank):
        return self.x0 + PLOT_W * (rank - 1) / (self.n - 1)

    def py(self, percent):
        frac = math.log10(percent / self.y_min) / math.log10(self.y_max / self.y_min)
        return Y1 - (Y1 - Y0) * frac


def text(id_, x, y, lines, size, anchor="start", fill=INK, weight="normal", transform=None):
    """Text with one sodipodi line tspan per entry of lines, each with its own x/y."""
    lines = [lines] if isinstance(lines, str) else lines
    tr = f' transform="{transform}"' if transform else ""
    step = size * PT * 1.15
    spans = "".join(f'<tspan sodipodi:role="line" id="{id_}_line{i + 1}" x="{x:.2f}" y="{y + i * step:.2f}">'
                    f'{content}</tspan>' for i, content in enumerate(lines))
    return (f'<text id="{id_}" xml:space="preserve" x="{x:.2f}" y="{y:.2f}"{tr} '
            f'style="{FONT};font-size:{size * PT:.3f}px;font-weight:{weight};text-anchor:{anchor};fill:{fill}">'
            f'{spans}</text>')


def line(id_, x1, y1, x2, y2, colour, width):
    return (f'<path id="{id_}" d="M {x1:.2f},{y1:.2f} L {x2:.2f},{y2:.2f}" '
            f'style="fill:none;stroke:{colour};stroke-width:{width * PT:.3f}"/>')


def plot_for(model, n):
    _, _, x0, y_range, _ = MODELS[model]
    return Plot(x0, n, y_range)


def data_groups(model, rows):
    p = plot_for(model, len(rows[SCALINGS[0][1]]))
    groups = {}
    for key, name, _ in SCALINGS:
        r = rows[name]
        upper = " L ".join(f"{p.px(int(x['rank'])):.3f},{p.py(float(x['hi'])):.3f}" for x in r)
        lower = " L ".join(f"{p.px(int(x['rank'])):.3f},{p.py(float(x['lo'])):.3f}" for x in reversed(r))
        groups[f"band_{model}_{key}"] = f'<path id="band_{model}_{key}_area" d="M {upper} L {lower} Z"/>'
        groups[f"points_{model}_{key}"] = "".join(
            f'<circle id="pt_{model}_{key}_{x["rank"]}" cx="{p.px(int(x["rank"])):.3f}" '
            f'cy="{p.py(float(x["mean"])):.3f}" r="0.14"/>' for x in r)
    return groups


def layer(id_, label, body):
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">{body}</g>\n'


def axes(model, n):
    p, s, y_ticks = plot_for(model, n), model, MODELS[model][4]
    left, right, bottom, top = p.px(1), p.px(n), p.py(p.y_min), p.py(p.y_max)
    out = "".join(line(f"grid_{s}_y_{v:g}", left, p.py(v), right, p.py(v), GRID, 0.4) for v in y_ticks)
    out += "".join(line(f"grid_{s}_x_{v}", p.px(v), bottom, p.px(v), top, GRID, 0.4) for v in X_TICKS[1:])
    out += line(f"axis_{s}_x", left, bottom, right, bottom, AXIS, 0.5)
    out += line(f"axis_{s}_y", left, bottom, left, top, AXIS, 0.5)
    for v in X_TICKS:
        out += line(f"tick_{s}_x_{v}", p.px(v), bottom, p.px(v), bottom + 0.8, AXIS, 0.5)
        out += text(f"ticklabel_{s}_x_{v}", p.px(v), bottom + 3.0, str(v), 5, "middle", MUTED)
    for v in y_ticks:
        out += line(f"tick_{s}_y_{v:g}", left, p.py(v), left - 0.8, p.py(v), AXIS, 0.5)
        out += text(f"ticklabel_{s}_y_{v:g}", left - 1.3, p.py(v) + 0.6, f"{v:g}%", 5, "end", MUTED)
    return out


def draft(tables):
    groups = {}
    for model in MODELS:
        groups.update(data_groups(model, tables[model]))
    colour = {key: c for key, _, c in SCALINGS}
    bands = "".join(f'<g id="{id_}" inkscape:label="{id_.replace("_", " ")}" '
                    f'style="fill:{DOT[id_.rsplit("_", 1)[1]]};fill-opacity:0.15;stroke:none">{body}</g>'
                    for id_, body in groups.items() if id_.startswith("band_"))
    points = "".join(f'<g id="{id_}" inkscape:label="{id_.replace("_", " ")}" '
                     f'style="fill:{DOT[id_.rsplit("_", 1)[1]]};fill-opacity:0.9;stroke:none">{body}</g>'
                     for id_, body in groups.items() if id_.startswith("points_"))
    n = len(tables["poisson"]["Uniform"])
    labels = ""
    for model, (_, title, x0, _, _) in MODELS.items():
        labels += text(f"plot_title_{model}", x0, Y0 - 2.0, title, 7, weight="bold")
    mid = plot_for("proportional", n)
    labels += text("axis_title_x", mid.px((n + 1) / 2), Y1 + 6.2, "Gene rank by observed total", 6, "middle")
    labels += text("axis_title_y", -(Y0 + Y1) / 2, 3.6, "Gene share of variance in Z (%)", 6, "middle",
                   transform="rotate(-90)")
    legend, y = "", 61.3
    for key, label, c, x in [("uniform", "Uniform scaling", DOT["uniform"], 44.0),
                             ("expression", "Expression scaling", DOT["expression"], 70.0)]:
        legend += (f'<circle id="legend_dot_{key}" cx="{x:.2f}" cy="{y - 0.6:.2f}" r="0.55" style="fill:{c}"/>'
                   + text(f"legend_{key}", x + 1.4, y, label, 6))
    legend += text("replicate_note", W / 2, 65.4,
                   f"Dots: mean of the i-th ranked gene over {REPLICATES} simulated replicates; bands: range.",
                   6, "middle", MUTED)
    title = (text("panel_letter", 1.2, 5.2, "C", 10, weight="bold")
             + text("panel_title", 7.0, 5.0, "Where the variance sits after bi-whitening", 8, weight="bold"))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            f'<svg width="{W:g}mm" height="{H:g}mm" viewBox="0 0 {W:g} {H:g}" version="1.1" id="fig1C" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">\n'
            '<sodipodi:namedview id="namedview1" inkscape:document-units="mm" pagecolor="#ffffff"/>\n'
            + layer("layer_axes", "Axes", "".join(axes(m, n) for m in MODELS))
            + layer("layer_bands", "Bands", bands)
            + layer("layer_points", "Points", points)
            + layer("layer_labels", "Labels", labels + legend)
            + layer("layer_title", "Title", title)
            + "</svg>\n")


REPLICATES = 5  # must match R in noise_share.R (the CSV does not record it); used only in the draft note


def main():
    tables = {m: {name: [] for _, name, _ in SCALINGS} for m in MODELS}
    by_name = {v[0]: k for k, v in MODELS.items()}
    with (HERE / "noise_share_by_rank.csv").open() as f:
        for r in csv.DictReader(f):
            tables[by_name[r["model"]]][r["scaling"]].append(r)
    for model, (name, _, _, (y_min, y_max), _) in MODELS.items():
        for _, scaling, _ in SCALINGS:
            rows = sorted(tables[model][scaling], key=lambda r: int(r["rank"]))
            tables[model][scaling] = rows
            means = [float(r["mean"]) for r in rows]
            lo, hi = min(float(r["lo"]) for r in rows), max(float(r["hi"]) for r in rows)
            quarter = sum(means[: len(means) // 4]) / sum(means) * 100
            print(f"{name:21s} {scaling:10s} genes {len(rows)}; mean {min(means):.3g}-{max(means):.3g}%; "
                  f"band {lo:.3g}-{hi:.3g}%; lowest quarter {quarter:.1f}%")
            if lo < y_min or hi > y_max:
                print(f"  NOTE: values fall outside the y-range {y_min}-{y_max}%")
    master = HERE / "fig1C.svg"
    if not master.exists():
        master.write_text(draft(tables))
        print("Wrote first draft", master)
        return
    replacements = {}
    for model in MODELS:
        replacements.update(data_groups(model, tables[model]))
    original = master.read_bytes()
    updated = replace_data(original, replacements)
    if updated != original:
        master.write_bytes(updated)
    print("Updated only data-group contents in", master, "; check labels against the values above")


if __name__ == "__main__":
    main()
