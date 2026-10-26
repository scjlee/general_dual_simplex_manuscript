"""Write or refresh the Figure 1B SVG: cumulative scaled versus observed share.

Archived 2026-10-26 (replaced by the rank plot in figure/fig1/panelB/).
Usage (repo root): python3 figure/fig1/panelB/archive/20261026_cumulative/make_fig1B.py
Input: mass_by_gene.csv, mass_by_sample.csv and mass_summary.csv from mass.R.
Each point is one gene (left) or sample (right), ordered by observed total:
x = cumulative share of the observed matrix total, y = cumulative share of
the scaled matrix total. If fig1B.svg is absent, a first draft with all
labels is written. Once it exists it is the master: only the contents of the
data groups points_<margin>_<scaling> (margin = genes, samples; scaling =
uniform, expression) are replaced by id (panel A's replace_data); labels are
left alone and the values they need are printed.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "panelA"))  # figure/fig1/panelA
from make_fig1A import replace_data  # noqa: E402

PT = 0.3528  # mm per point
FONT = "font-family:Liberation Sans, Arial, Helvetica, sans-serif;line-height:1.15"
UNIFORM, EXPRESSION = "#E07B28", "#2A7BBF"  # panel A branch colours
INK, MUTED, AXIS, GRID = "#1A1A1A", "#555555", "#666666", "#E3E3E3"
W, H = 134.0, 67.0
Y0, Y1 = 12.5, 50.5  # plot area top and bottom
PLOT_W = 45.0
MARGINS = {  # margin key: (plot left edge, CSV, title, singular noun, point radius)
    "genes": (15.0, "mass_by_gene.csv", "Genes", "gene", 0.1),
    "samples": (82.0, "mass_by_sample.csv", "Samples", "sample", 0.16),
}
SCALINGS = (("expression", EXPRESSION), ("uniform", UNIFORM))  # uniform drawn on top


class Plot:
    def __init__(self, x0):
        self.x0 = x0

    def px(self, percent):
        return self.x0 + PLOT_W * percent / 100

    @staticmethod
    def py(percent):
        return Y1 - (Y1 - Y0) * percent / 100


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


def points(p, margin, scaling, rows, item, radius):
    return "".join(f'<circle id="pt_{margin}_{scaling}_{r[item]}" '
                   f'cx="{p.px(float(r["raw_cumulative_percent"])):.3f}" '
                   f'cy="{p.py(float(r[f"{scaling}_cumulative_percent"])):.3f}" r="{radius}"/>'
                   for r in rows)


def data_groups(margin, rows):
    x0, _, _, item, radius = MARGINS[margin]
    return {f"points_{margin}_{scaling}": points(Plot(x0), margin, scaling, rows, item, radius)
            for scaling, _ in SCALINGS}


def layer(id_, label, body):
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">{body}</g>\n'


def axes(margin):
    p, s = Plot(MARGINS[margin][0]), margin
    out = "".join(line(f"grid_{s}_x_{v}", p.px(v), p.py(0), p.px(v), p.py(100), GRID, 0.4)
                  + line(f"grid_{s}_y_{v}", p.px(0), p.py(v), p.px(100), p.py(v), GRID, 0.4)
                  for v in (25, 50, 75, 100))
    # Dashed line at 50% of the observed total, spanning the whole y-axis.
    out += line(f"half_line_{s}", p.px(50), p.py(0), p.px(50), p.py(100), AXIS, 0.4, "0.6,0.4")
    out += line(f"axis_{s}_x", p.px(0), p.py(0), p.px(100), p.py(0), AXIS, 0.5)
    out += line(f"axis_{s}_y", p.px(0), p.py(0), p.px(0), p.py(100), AXIS, 0.5)
    for v in (0, 25, 50, 75, 100):
        out += line(f"tick_{s}_x_{v}", p.px(v), p.py(0), p.px(v), p.py(0) + 0.8, AXIS, 0.5)
        out += line(f"tick_{s}_y_{v}", p.px(0), p.py(v), p.px(0) - 0.8, p.py(v), AXIS, 0.5)
        out += text(f"ticklabel_{s}_x_{v}", p.px(v), p.py(0) + 3.0, f"{v}%", 5, "middle", MUTED)
        out += text(f"ticklabel_{s}_y_{v}", p.px(0) - 1.3, p.py(v) + 0.6, f"{v}%", 5, "end", MUTED)
    return out


def labels(margin, u_half, e_half):
    x0, _, title, noun, _ = MARGINS[margin]
    p, s = Plot(x0), margin
    ymid = (Y0 + Y1) / 2
    return (text(f"plot_title_{s}", p.px(0), Y0 - 2.0, title, 7, weight="bold")
            + text(f"axis_title_x_{s}", p.px(50), p.py(0) + 6.2,
                   f"Cumulative {noun} share of observed matrix total (%)", 6, "middle")
            + text(f"axis_title_y_{s}", -ymid, p.x0 - 11.4,
                   [f"Cumulative {noun} share of", "scaled matrix total (%)"], 6, "middle",
                   transform="rotate(-90)")
            + text(f"label_half_{s}_uniform", p.px(50) - 1.0, p.py(u_half) - 1.0,
                   f"{u_half:.1f}%", 6, "end", UNIFORM, "bold")
            + text(f"label_half_{s}_expression", p.px(50) + 1.2, p.py(e_half) + 2.6,
                   f"{e_half:.1f}%", 6, "start", EXPRESSION, "bold"))


def draft(tables, halves):
    groups = {}
    for margin in MARGINS:
        groups.update(data_groups(margin, tables[margin]))
    colour = dict(SCALINGS)
    style = {id_: (f' style="fill:{colour[id_.rsplit("_", 1)[1]]};fill-opacity:0.75;stroke:none"'
                   if id_.startswith("points_") else "") for id_ in groups}
    data = "".join(f'<g id="{id_}" inkscape:label="{id_.replace("_", " ")}"{style[id_]}>{body}</g>'
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
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            f'<svg width="{W:g}mm" height="{H:g}mm" viewBox="0 0 {W:g} {H:g}" version="1.1" id="fig1B" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">\n'
            '<sodipodi:namedview id="namedview1" inkscape:document-units="mm" pagecolor="#ffffff"/>\n'
            + layer("layer_axes", "Axes", "".join(axes(m) for m in MARGINS))
            + layer("layer_data", "Data", data)
            + layer("layer_labels", "Labels", "".join(labels(m, *halves[m]) for m in MARGINS) + legend)
            + layer("layer_title", "Title", title)
            + "</svg>\n")


def main():
    tables = {}
    for margin, (_, path, _, _, _) in MARGINS.items():
        with (HERE / path).open() as f:
            tables[margin] = list(csv.DictReader(f))
    with (HERE / "mass_summary.csv").open() as f:
        summary = {r["quantity"]: float(r["value"]) for r in csv.DictReader(f)}
    halves = {}
    for margin in MARGINS:
        u = summary[f"{margin}_uniform_cumulative_percent_at_observed_half"]
        e = summary[f"{margin}_expression_cumulative_percent_at_observed_half"]
        halves[margin] = (u, e)
        print(f"{margin}: at 50% of observed total, scaled share uniform {u:.6f}% (label {u:.1f}%), "
              f"expression {e:.6f}% (label {e:.1f}%); max |raw - expression| "
              f"{summary[f'{margin}_max_abs_raw_minus_expression_cumulative_percent']:.3g}")
    print(f"genes {summary['genes_count']:.0f}, samples {summary['samples_count']:.0f}; "
          f"uniform converged {summary['uniform_converged']:.0f}, "
          f"max relative marginal error {summary['uniform_max_relative_marginal_error']:.3g}")

    master = HERE / "fig1B.svg"
    if not master.exists():
        master.write_text(draft(tables, halves))
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
