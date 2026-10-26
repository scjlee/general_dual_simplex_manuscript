"""Create E/F SVG masters from their existing oracle RMSE CSVs.

Run from the manuscript root: python3 figure/fig1/panelE/make_fig1EF.py
After creation, update only named data groups, preserving edited axes and text.
No simulation or RMSE calculation is performed here. Current axes: W 0–10,
H 0–0.2. Means in the data groups update from unrounded input values.
"""
import csv
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "panelC"))
from make_fig1C import text, line, layer  # noqa: E402
from make_fig1A import replace_data  # imported by make_fig1C  # noqa: E402

PT = 25.4 / 72
MODELS = (("poisson", "Poisson", 15), ("proportional", "Proportional", 44),
          ("normal", "Normal, floored at 0", 73))
COLOURS = {"uniform": "#E07B28", "expression": "#2A7BBF"}
INK, MUTED = "#1A1A1A", "#555555"


def point(id_, x, y, colour):
    return (f'<circle id="{id_}" cx="{x:.5f}" cy="{y:.5f}" r="0.43" '
            f'style="fill:{colour};stroke:none"/>')


def data_groups(rows, side, ymax):
    value = f"oracle_{side}_rmse"
    py = lambda v: 47 - 29 * v / ymax
    groups = {}
    for key, model, x0 in MODELS:
        by_draw = {(int(r["draw"]), r["scaling"]): float(r[value])
                   for r in rows if r["model"] == model}
        pairs = []
        for draw in range(1, 6):
            shift = -1.2 + .6 * (draw - 1)
            pairs.append(line(f"pair_{key}_draw{draw}", x0 + 5 + shift,
                py(by_draw[draw, "uniform"]), x0 + 18 + shift,
                py(by_draw[draw, "expression"]), "#B8B8B8", .4))
        groups[f"pairs_{key}"] = "".join(pairs)
        for sc, dx in (("uniform", 5), ("expression", 18)):
            values = [by_draw[r, sc] for r in range(1, 6)]
            avg = statistics.mean(values)
            body = "".join(point(f"dot_{key}_{sc}_draw{draw}", x0 + dx - 1.2 + .6 * (draw - 1),
                                 py(v), COLOURS[sc]) for draw, v in enumerate(values, 1))
            body += line(f"mean_bar_{key}_{sc}", x0 + dx - 2.1, py(avg),
                         x0 + dx + 2.1, py(avg), COLOURS[sc], .6)
            body += text(f"mean_label_{key}_{sc}", x0 + dx, 16.7, f"{avg:.3f}", 5.5,
                         "middle", COLOURS[sc], "bold")
            groups[f"values_{key}_{sc}"] = body
            print(f"{side} {model} {sc}: n={len(values)}, mean={avg:.9g}, "
                  f"range={min(values):.9g}–{max(values):.9g}; axis 0–{ymax:g}")
    return groups


def draft(letter, side, ymax, ticks, groups):
    axes, labels = "", ""
    py = lambda v: 47 - 29 * v / ymax
    for key, model, x0 in MODELS:
        labels += text(f"noise_title_{key}", x0 + 11.5, 13.3, model, 6.5,
                       "middle", weight="bold")
        for i, y in enumerate(ticks):
            axes += line(f"grid_{key}_y{i}", x0, py(y), x0 + 23, py(y), "#E3E3E3", .4)
            if key == "poisson":
                labels += text(f"ytick_{i}", x0 - 1.4, py(y) + .65,
                               f"{y:g}", 5.5, "end", MUTED)
        axes += line(f"axis_{key}_x", x0, 47, x0 + 23, 47, "#777777", .5)
        axes += line(f"axis_{key}_y", x0, 18, x0, 47, "#777777", .5)
        for sc, dx in (("uniform", 5), ("expression", 18)):
            labels += text(f"xlabel_{key}_{sc}", x0 + dx, 51.2,
                           sc.capitalize(), 5.8, "middle", COLOURS[sc])
    labels += text("axis_title_y", -32.5, 3.95, "oracle RMSE", 6,
                   "middle", transform="rotate(-90)")
    title = text("panel_letter", 1.2, 5.8, letter, 8, weight="bold")
    title += text("panel_title", 7, 5.8, f"{side} oracle error", 8, weight="bold")
    data = "".join(f'<g id="{id_}">{body}</g>' for id_, body in groups.items())
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg id="fig1{letter}" width="100mm" height="54mm" viewBox="0 0 100 54" '
            'xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">\n'
            '<sodipodi:namedview id="namedview" inkscape:document-units="mm" pagecolor="#ffffff"/>\n'
            + layer("layer_axes", "Axes", axes)
            + layer("layer_data", "Paired oracle errors and means", data)
            + layer("layer_labels", "Labels", labels)
            + layer("layer_title", "Title", title) + '</svg>\n')


def main():
    for letter, side, ymax, ticks in (("E", "W", 10, (0, 2, 4, 6, 8, 10)),
                                      ("F", "H", .2, (0, .05, .1, .15, .2))):
        directory = HERE.parent / f"panel{letter}"
        with (directory / "projection_metrics.csv").open() as f:
            rows = list(csv.DictReader(f))
        groups = data_groups(rows, side, ymax)
        path = directory / f"fig1{letter}.svg"
        if path.exists():
            old = path.read_bytes()
            updated = replace_data(old, groups)
            if updated != old:
                path.write_bytes(updated)
            print("Updated data groups only:", path)
        else:
            path.write_text(draft(letter, side, ymax, ticks, groups))
            print("Created SVG master:", path)


if __name__ == "__main__":
    main()
