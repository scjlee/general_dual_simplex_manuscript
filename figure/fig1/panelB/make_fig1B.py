"""Write or refresh the Figure 1B SVG: per-item scaled share against rank.

Usage (repo root): python3 figure/fig1/panelB/make_fig1B.py
Input: mass_by_gene.csv, mass_by_sample.csv and mass_summary.csv from mass.R.
Each point is one gene (left) or sample (right): x = rank by observed total,
y = its share of the scaled matrix total, log scale. Each plot has its own
y-range (not for comparison between plots). The archived cumulative version
is in archive/20261026_cumulative/.
If fig1B.svg is absent, a first draft with all labels is written. Once it
exists it is the master: only the contents of the data groups
points_<margin>_<scaling> (margin = genes, samples; scaling = uniform,
expression) are replaced by id (panel A's replace_data); labels are left
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
INK, MUTED, AXIS, GRID = "#1A1A1A", "#555555", "#666666", "#E3E3E3"
W, H = 134.0, 67.0
Y0, Y1 = 12.5, 50.5  # plot area top and bottom
PLOT_W = 45.0
# margin key: (plot left edge, CSV, title, singular noun, point radius, x ticks,
#              log y-range of shares in %, y ticks); each plot has its own y-range.
MARGINS = {
    "genes": (15.0, "mass_by_gene.csv", "Genes", "gene", 0.18, (1, 100, 200, 300, 400, 500),
              (0.01, 1.0), (0.01, 0.03, 0.1, 0.3, 1)),
    "samples": (82.0, "mass_by_sample.csv", "Samples", "sample", 0.25, (1, 50, 100, 150, 200),
                (0.4, 0.6), (0.4, 0.45, 0.5, 0.55, 0.6)),
}
SCALINGS = (("expression", EXPRESSION), ("uniform", UNIFORM))  # uniform drawn on top


class Plot:
    def __init__(self, x0, n, y_range):
        self.x0, self.n = x0, n
        self.y_min, self.y_max = y_range

    def px(self, rank):
        return self.x0 + PLOT_W * rank / self.n

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


def line(id_, x1, y1, x2, y2, colour, width, dash=None):
    d = f";stroke-dasharray:{dash}" if dash else ""
    return (f'<path id="{id_}" d="M {x1:.2f},{y1:.2f} L {x2:.2f},{y2:.2f}" '
            f'style="fill:none;stroke:{colour};stroke-width:{width * PT:.3f}{d}"/>')


def plot_for(margin, n):
    return Plot(MARGINS[margin][0], n, MARGINS[margin][6])


def points(p, margin, scaling, rows, item, radius):
    return "".join(f'<circle id="pt_{margin}_{scaling}_{r[item]}" '
                   f'cx="{p.px(int(r["rank"])):.3f}" '
                   f'cy="{p.py(float(r[f"{scaling}_share_percent"])):.3f}" r="{radius}"/>'
                   for r in rows)


def data_groups(margin, rows):
    _, _, _, item, radius, *_ = MARGINS[margin]
    p = plot_for(margin, len(rows))
    return {f"points_{margin}_{scaling}": points(p, margin, scaling, rows, item, radius)
            for scaling, _ in SCALINGS}


def layer(id_, label, body):
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">{body}</g>\n'


def axes(margin, n):
    p, s, x_ticks, y_ticks = plot_for(margin, n), margin, MARGINS[margin][5], MARGINS[margin][7]
    y_min, y_max = p.y_min, p.y_max
    left, right = p.px(0), p.px(n)
    out = "".join(line(f"grid_{s}_y_{v:g}", left, p.py(v), right, p.py(v), GRID, 0.4) for v in y_ticks)
    out += "".join(line(f"grid_{s}_x_{v}", p.px(v), p.py(y_min), p.px(v), p.py(y_max), GRID, 0.4)
                   for v in x_ticks[1:])
    out += line(f"axis_{s}_x", left, p.py(y_min), right, p.py(y_min), AXIS, 0.5)
    out += line(f"axis_{s}_y", left, p.py(y_min), left, p.py(y_max), AXIS, 0.5)
    for v in x_ticks:
        out += line(f"tick_{s}_x_{v}", p.px(v), p.py(y_min), p.px(v), p.py(y_min) + 0.8, AXIS, 0.5)
        out += text(f"ticklabel_{s}_x_{v}", p.px(v), p.py(y_min) + 3.0, str(v), 5, "middle", MUTED)
    for v in y_ticks:
        out += line(f"tick_{s}_y_{v:g}", left, p.py(v), left - 0.8, p.py(v), AXIS, 0.5)
        out += text(f"ticklabel_{s}_y_{v:g}", left - 1.3, p.py(v) + 0.6, f"{v:g}%", 5, "end", MUTED)
    return out


def labels(margin, n, uniform_share):
    x0, _, title, noun, *_ = MARGINS[margin]
    p, s = plot_for(margin, n), margin
    y_min = p.y_min
    ymid = (Y0 + Y1) / 2
    return (text(f"plot_title_{s}", p.px(0), Y0 - 2.0, title, 7, weight="bold")
            + text(f"axis_title_x_{s}", p.px(n / 2), p.py(y_min) + 6.2, f"{noun.capitalize()} rank", 6, "middle")
            + text(f"axis_title_y_{s}", -ymid, x0 - 10.4, f"{noun.capitalize()} share of scaled matrix total (%)",
                   6, "middle", transform="rotate(-90)")
            + text(f"label_uniform_{s}", p.px(n * 0.03), p.py(uniform_share) - 1.0,
                   f"Uniform: 1/{n} = {uniform_share:.2g}% each", 5, "start", UNIFORM))


def draft(tables, uniform_shares):
    groups = {}
    for margin in MARGINS:
        groups.update(data_groups(margin, tables[margin]))
    colour = dict(SCALINGS)
    data = "".join(f'<g id="{id_}" inkscape:label="{id_.replace("_", " ")}" '
                   f'style="fill:{colour[id_.rsplit("_", 1)[1]]};fill-opacity:0.75;stroke:none">{body}</g>'
                   for id_, body in groups.items())
    # One-line colour legend, centred below both plots.
    legend, y = "", 61.3
    for key, label, c, x in [("uniform", "Uniform scaling (equal mass)", UNIFORM, 33.3),
                             ("expression", "Expression scaling = raw count share", EXPRESSION, 66.0)]:
        legend += (f'<circle id="legend_dot_{key}" cx="{x:.2f}" cy="{y - 0.6:.2f}" r="0.55" style="fill:{c}"/>'
                   + text(f"legend_{key}", x + 1.4, y, label, 6))
    legend += text("ordering_note", W / 2, 65.4,
                   "Genes and samples are ordered by observed expression total.", 6, "middle", MUTED)
    title = (text("panel_letter", 1.2, 5.2, "B", 10, weight="bold")
             + text("panel_title", 7.0, 5.0, "How each scaling allocates gene and sample mass", 8, weight="bold"))
    body = "".join(labels(m, len(tables[m]), uniform_shares[m]) for m in MARGINS) + legend
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            f'<svg width="{W:g}mm" height="{H:g}mm" viewBox="0 0 {W:g} {H:g}" version="1.1" id="fig1B" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">\n'
            '<sodipodi:namedview id="namedview1" inkscape:document-units="mm" pagecolor="#ffffff"/>\n'
            + layer("layer_axes", "Axes", "".join(axes(m, len(tables[m])) for m in MARGINS))
            + layer("layer_data", "Data", data)
            + layer("layer_labels", "Labels", body)
            + layer("layer_title", "Title", title)
            + "</svg>\n")


def main():
    tables = {}
    for margin, (_, path, *_rest) in MARGINS.items():
        with (HERE / path).open() as f:
            tables[margin] = list(csv.DictReader(f))
    with (HERE / "mass_summary.csv").open() as f:
        summary = {r["quantity"]: float(r["value"]) for r in csv.DictReader(f)}
    uniform_shares = {}
    for margin in MARGINS:
        def q(name):
            return summary[f"{margin}_{name}"]
        uniform_shares[margin] = 100 / q("count")
        print(f"{margin}: uniform share {q('uniform_share_percent_min'):.6g}-{q('uniform_share_percent_max'):.6g}% "
              f"(label 1/{q('count'):.0f} = {uniform_shares[margin]:.2g}%); expression share "
              f"{q('expression_share_percent_min'):.6g}-{q('expression_share_percent_max'):.6g}% "
              f"({q('expression_share_max_over_min'):.4g}-fold); "
              f"{q('items_percent_expression_above_uniform'):.1f}% of items above uniform")
        values = [float(r[f"{s}_share_percent"]) for r in tables[margin] for s, _ in SCALINGS]
        y_min, y_max = MARGINS[margin][6]
        if min(values) < y_min or max(values) > y_max:
            print(f"  NOTE: {margin} shares fall outside the y-range {y_min}-{y_max}%")
    print(f"uniform converged {summary['uniform_converged']:.0f}, "
          f"max relative marginal error {summary['uniform_max_relative_marginal_error']:.3g}")

    master = HERE / "fig1B.svg"
    if not master.exists():
        master.write_text(draft(tables, uniform_shares))
        print("Wrote first draft", master)
        return
    replacements = {}
    for margin in MARGINS:
        replacements.update(data_groups(margin, tables[margin]))
    original = master.read_bytes()
    updated = replace_data(original, replacements)
    if updated != original:
        master.write_bytes(updated)
    print("Updated only data-group contents in", master, "; check labels against the values above")


if __name__ == "__main__":
    main()
