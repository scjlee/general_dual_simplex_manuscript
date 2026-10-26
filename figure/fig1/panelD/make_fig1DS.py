"""Create D and supplementary sample-simplex SVG masters from saved CSVs.

After initial creation, replace only named projection data groups. Axes,
frames, labels, legend and hand edits outside those groups are preserved.
Run: python3 figure/fig1/panelD/make_fig1DS.py
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "panelE"))
from make_fig1EF import text, line, layer, replace_data  # noqa: E402

PT = 25.4 / 72
MODELS = (("poisson", "Poisson", 10), ("proportional", "Proportional", 47),
          ("normal", "Normal, floored at 0", 84))
SCALINGS = (("uniform", 21, "#E07B28"), ("expression", 59, "#2A7BBF"))
COLOURS = {"background": "#B8B8B8", "marker1": "#009E73",
           "marker2": "#CC79A7", "marker3": "#D69B00"}
SIDE = 29.5


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def circle(id_, x, y, radius, colour, opacity=1):
    return (f'<circle id="{id_}" cx="{x:.5f}" cy="{y:.5f}" r="{radius}" '
            f'style="fill:{colour};fill-opacity:{opacity};stroke:none"/>')


def groups_for(points, vertices, metrics, sample_side):
    groups = {}
    field = "oracle_H_rmse" if sample_side else "oracle_W_rmse"
    for key, model, x0 in MODELS:
        for sc, y0, _ in SCALINGS:
            p = [r for r in points if r["model"] == model and r["scaling"] == sc]
            v = sorted((r for r in vertices if r["model"] == model and r["scaling"] == sc),
                       key=lambda r: int(r["component"]))
            xs = [float(r["x"]) for r in p + v]
            ys = [float(r["y"]) for r in p + v]
            midx, midy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            span = max(max(xs) - min(xs), max(ys) - min(ys))
            px = lambda r: x0 + SIDE / 2 + (float(r["x"]) - midx) / span * (SIDE - 4)
            py = lambda r: y0 + SIDE / 2 - (float(r["y"]) - midy) / span * (SIDE - 4)
            prefix = f"{key}_{sc}"
            body = ""
            for r in sorted(p, key=lambda r: r.get("group", "")):
                name = r["sample"] if sample_side else r["gene"]
                id_ = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
                colour = "#929292" if sample_side else COLOURS[r["group"]]
                radius = .23 if sample_side else (.18 if r["group"] == "background" else .26)
                body += circle(f"point_{prefix}_{id_}", px(r), py(r), radius, colour,
                               1 if sample_side else .85)
            path = " L ".join(f"{px(r):.5f},{py(r):.5f}" for r in v)
            body += (f'<path id="triangle_{prefix}" d="M {path} Z" '
                     f'style="fill:none;stroke:#666666;stroke-width:{.5 * PT:.5f};stroke-dasharray:0.6,0.4"/>')
            if sample_side:
                body += "".join(circle(f"vertex_{prefix}_{r['component']}", px(r), py(r), .4,
                                       COLOURS[f"marker{r['component']}"]) for r in v)
            error = next(float(r[field]) for r in metrics
                         if r["model"] == model and r["scaling"] == sc and int(r["draw"]) == 1)
            body += text(f"rmse_{prefix}", x0 + SIDE / 2, y0 - 1.7,
                         f"oracle RMSE: {error:.3f}", 5.5, "middle", "#555555")
            groups[f"projection_{prefix}"] = body
            print(f"{'S' if sample_side else 'D'} {model} {sc}: {len(p)} points, "
                  f"{len(v)} vertices; {field}={error:.9g}; equal-aspect span={span:.9g}")
    return groups


def draft(sample_side, groups):
    letter = "S" if sample_side else "D"
    title = "Representative sample simplices" if sample_side else "Representative gene simplices"
    labels = text("panel_letter", 1.2, 5.8, letter, 8, weight="bold")
    labels += text("panel_title", 7, 5.8, title, 8, weight="bold")
    frames = ""
    for key, model, x0 in MODELS:
        labels += text(f"noise_title_{key}", x0 + SIDE / 2, 13.8, model,
                       6.5, "middle", weight="bold")
        for sc, y0, colour in SCALINGS:
            frames += (f'<rect id="frame_{key}_{sc}" x="{x0}" y="{y0}" '
                       f'width="{SIDE}" height="{SIDE}" '
                       f'style="fill:none;stroke:{colour};stroke-width:{.6 * PT:.5f}"/>')
    for sc, y0, colour in SCALINGS:
        labels += text(f"scaling_label_{sc}", -(y0 + SIDE / 2), 7.2,
                       sc.capitalize() + " scaling", 6.5, "middle", colour,
                       "bold", transform="rotate(-90)")
    labels += text("axis_title_x", 61.75, 93.4, "Projection 2", 6, "middle")
    labels += text("axis_title_y", 117, 54.75, "Projection 3", 6, "middle",
                   transform="rotate(90 117 54.75)")
    legend = text("legend_components", 10, 98.7, "Components:" if sample_side else "Markers:",
                  5.8, fill="#555555")
    for i in range(1, 4):
        legend += circle(f"legend_component_dot_{i}", 25 + 6 * (i - 1), 98,
                         .35, COLOURS[f"marker{i}"])
        legend += text(f"legend_component_number_{i}", 26 + 6 * (i - 1), 98.7,
                       str(i), 5.8, fill=COLOURS[f"marker{i}"])
    legend += circle("legend_grey_dot", 45, 98, .35, "#929292" if sample_side else COLOURS["background"])
    legend += text("legend_grey_label", 46.5, 98.7, "Samples" if sample_side else "Background",
                   5.8, fill="#555555")
    legend += (f'<path id="legend_triangle_line" d="M 67,98 L 72,98" '
               f'style="fill:none;stroke:#666666;stroke-width:{.5 * PT:.5f};stroke-dasharray:0.6,0.4"/>')
    legend += text("legend_triangle_label", 73.5, 98.7, "True components, projected", 5.8, fill="#555555")
    legend += text("separate_scales_note", 60, 103.7, "Separate plot scales; equal aspect.",
                   5.8, "middle", "#555555")
    data = "".join(f'<g id="{id_}">{body}</g>' for id_, body in groups.items())
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg id="fig1{letter}" width="119mm" height="107mm" viewBox="0 0 119 107" '
            'xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">\n'
            '<sodipodi:namedview id="namedview" inkscape:document-units="mm" pagecolor="#ffffff"/>\n'
            + layer("layer_frames", "Frames", frames)
            + layer("layer_data", "Projections and oracle labels", data)
            + layer("layer_labels", "Titles and axes", labels)
            + layer("layer_legend", "Legend", legend) + '</svg>\n')


def main():
    for sample_side in (False, True):
        directory = HERE.parent / "panelD_samples" if sample_side else HERE
        points = read(directory / ("sample_points.csv" if sample_side else "gene_points.csv"))
        vertices = read(directory / "simplex_vertices.csv")
        metrics = read(HERE.parent / ("panelF" if sample_side else "panelE") / "projection_metrics.csv")
        groups = groups_for(points, vertices, metrics, sample_side)
        path = directory / ("sample_simplices.svg" if sample_side else "fig1D.svg")
        if path.exists():
            old = path.read_bytes()
            updated = replace_data(old, groups)
            if updated != old:
                path.write_bytes(updated)
            print("Updated projection groups only:", path)
        else:
            path.write_text(draft(sample_side, groups))
            print("Created SVG master:", path)


if __name__ == "__main__":
    main()
