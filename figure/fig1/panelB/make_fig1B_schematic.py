#!/usr/bin/env python3
"""Draw the simulation-study schematic for Figure 1B.

Run once from the repository root. Matrix values are illustrative. The SVG is
created with mode "x" because it becomes the master after the first hand edit.
"""
import random
import re
import subprocess
from pathlib import Path
from statistics import mean, pstdev

HERE = Path(__file__).parent
PACKAGE = Path("../general_dual_simplex")

# Slide placeholder measured at 893.5 x 202.5 px (ratio 4.41); width matches Fig 1A.
WIDTH, HEIGHT = 134, 30.4
PT = 25.4 / 72
FONT = 8 * PT
OPERATOR_FONT = 14 * PT
CAP_HEIGHT = 0.716 * FONT
MATH_AXIS = 0.34 * OPERATOR_FONT
CELL = 3.1
TOP = 10.3
ROW_CENTRE = TOP + 3 * CELL
DARK = "#404040"

rng = random.Random(20261109)
m, k, n = 6, 3, 5
noise_fraction = 0.3


def dirichlet(alpha, size):
    draws = [rng.gammavariate(alpha, 1) for _ in range(size)]
    return [draw / sum(draws) for draw in draws]


W = [[rng.gammavariate(8 if j == i // 2 else 1.5, 1) for j in range(k)] for i in range(m)]
H_columns = [dirichlet(0.8, k) for _ in range(n)]
H = [[H_columns[j][i] for j in range(n)] for i in range(k)]
Vstar = [[sum(W[i][c] * H[c][j] for c in range(k)) for j in range(n)] for i in range(m)]
noise_sd = noise_fraction * pstdev(x for row in Vstar for x in row)
V = [[max(0, x + rng.gauss(0, noise_sd)) for x in row] for row in Vstar]
epsilon = [[V[i][j] - Vstar[i][j] for j in range(n)] for i in range(m)]


def blend(low, high, t):
    channels = [(int(low[i:i + 2], 16), int(high[i:i + 2], 16)) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a + (b - a) * t):02x}" for a, b in channels)


def pale(colour):
    return blend("#ffffff", colour, 0.12)


def entries(values):
    return [v for row in values for v in row]


def rect(id_, x, y, width, height, style, rx=0):
    corner = f' rx="{rx}"' if rx else ""
    return (f'<rect id="{id_}" x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" '
            f'height="{height:.3f}"{corner} style="{style}"/>')


def text(id_, x, y, content, weight="normal", anchor="middle", size=FONT):
    style = (f"font-family:'Liberation Sans',Arial,sans-serif;font-size:{size:.4f}px;"
             f"font-weight:{weight};text-anchor:{anchor};fill:#000000")
    return (f'<text id="{id_}" x="{x:.3f}" y="{y:.3f}" xml:space="preserve" style="{style}">'
            f'<tspan id="{id_}_line" sodipodi:role="line" x="{x:.3f}" y="{y:.3f}">{content}</tspan></text>')


def layer(id_, label, items):
    body = "\n".join(items)
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">\n{body}\n</g>'


def group(id_, items):
    return f'<g id="{id_}">\n' + "\n".join(items) + "\n</g>"


def matrix(name, values, low, high, x, pool):
    ranked = sorted(pool)
    cells = []
    for i, row in enumerate(values, 1):
        for j, value in enumerate(row, 1):
            fill = blend(low, high, ranked.index(value) / (len(ranked) - 1))
            cells.append(rect(f"{name}_r{i}_c{j}", x + (j - 1) * CELL, TOP + (i - 1) * CELL, CELL, CELL,
                              f"fill:{fill};stroke:#ffffff;stroke-width:{0.4 * PT:.4f}"))
    frame = rect(f"{name}_frame", x, TOP, len(values[0]) * CELL, len(values) * CELL,
                 f"fill:none;stroke:#000000;stroke-width:{0.5 * PT:.4f}")
    return layer(f"layer_matrix_{name}", f"matrix {name}", [group(f"{name}_cells", cells), frame])


def header(name, title, x0, x1):
    box = rect(f"header_{name}_box", x0, 0.4, x1 - x0, 4.6,
               f"fill:#f2f2f2;stroke:{DARK};stroke-width:{0.5 * PT:.4f}", rx=0.8)
    label = text(f"header_{name}_text", (x0 + x1) / 2, 2.7 + CAP_HEIGHT / 2, title, "bold")
    return group(f"header_{name}", [box, label])


def annotation(name, symbol, word, x_centre):
    content = f'<tspan id="label_{name}_symbol" style="font-weight:bold">{symbol}</tspan> ({word})'
    return text(f"label_{name}", x_centre, TOP - 0.9, content)


def right_brace(id_, x0, x1, y0, y1):
    mid_x, mid_y, curl = (x0 + x1) / 2, (y0 + y1) / 2, 1.3
    path = (f"M {x0},{y0} Q {mid_x},{y0} {mid_x},{y0 + curl} L {mid_x},{mid_y - curl} "
            f"Q {mid_x},{mid_y} {x1},{mid_y} Q {mid_x},{mid_y} {mid_x},{mid_y + curl} "
            f"L {mid_x},{y1 - curl} Q {mid_x},{y1} {x0},{y1}")
    return (f'<path id="{id_}" d="{path}" style="fill:none;stroke:#000000;'
            f'stroke-width:{0.6 * PT:.4f};stroke-linecap:round;stroke-linejoin:round"/>')


signal_pool = entries(Vstar) + entries(V)
matrices = [("W", "W", "profile", W, pale("#D55E00"), "#D55E00", 4.2, entries(W)),
            ("H", "H", "proportions", H, pale("#0072B2"), "#0072B2", 23.0, entries(H)),
            ("Vstar", "V*", "true signal", Vstar, "#56B4E9", "#E69F00", 51.0, signal_pool),
            ("epsilon", "ε", "noise", epsilon, pale(DARK), DARK, 81.5, entries(epsilon)),
            ("V", "V", "observed data", V, "#56B4E9", "#E69F00", 112.0, signal_pool)]
headers = [("signal_generation", "Signal generation", 0.4, 69.6),
           ("perturbation", "Perturbation", 71.2, 133.6)]
operators = [("times", "×", 18.25), ("plus", "+", 74.0), ("equals", "=", 104.5)]

layers = [
    layer("layer_headers", "headers", [header(*h) for h in headers]),
    layer("layer_signal_outline", "W times H outline",
          [rect("signal_outline", 0.4, 6.4, 42.0, 23.6,
                f"fill:none;stroke:{DARK};stroke-width:{0.5 * PT:.4f};stroke-dasharray:1.2,0.8", rx=0.8)]),
    layer("layer_brace", "brace", [right_brace("brace_factors_to_signal", 43.8, 46.4, TOP, TOP + 6 * CELL)]),
    *[matrix(name, values, low, high, x, pool) for name, _, _, values, low, high, x, pool in matrices],
    layer("layer_labels", "matrix annotations",
          [annotation(name, symbol, word, x + len(values[0]) * CELL / 2)
           for name, symbol, word, values, _, _, x, _ in matrices]),
    layer("layer_operators", "operators",
          [text(f"operator_{name}", x, ROW_CENTRE + MATH_AXIS, symbol, "bold", size=OPERATOR_FONT)
           for name, symbol, x in operators]),
]

svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg id="fig1B_schematic" version="1.1" width="{WIDTH}mm" height="{HEIGHT}mm" viewBox="0 0 {WIDTH} {HEIGHT}"
   sodipodi:docname="fig1B_schematic.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
<title id="fig1B_schematic_title">Figure 1B schematic of the simulation study</title>
<sodipodi:namedview id="namedview_fig1B_schematic" inkscape:document-units="mm" pagecolor="#ffffff"
   inkscape:pageopacity="1" inkscape:current-layer="layer_headers"/>
{chr(10).join(layers)}
</svg>
"""
with open(HERE / "fig1B_schematic.svg", "x", encoding="utf-8") as output:
    output.write(svg)


def package_git(*args):
    return subprocess.run(["git", "-C", str(PACKAGE), *args], capture_output=True, text=True).stdout


version = re.search(r"^Version: (.+)$", (PACKAGE / "DESCRIPTION").read_text(), re.M)[1]
(HERE / "package_commit.txt").write_text(
    "This schematic uses no package code; values are illustrative.\n"
    f"commit {package_git('rev-parse', 'HEAD')}version {version}\n"
    f"git status --porcelain R src:\n{package_git('status', '--porcelain', 'R', 'src')}"
)

entries = [x for row in Vstar for x in row]
noise = [x for row in epsilon for x in row]
print(f"m={m} k={k} n={n} seed=20261109 canvas={WIDTH}x{HEIGHT} mm ratio={WIDTH / HEIGHT:.3f}")
print(f"V* mean={mean(entries):.3f} sd={pstdev(entries):.3f}; noise sd before clipping={noise_sd:.3f}")
print(f"epsilon = V - V*: min={min(noise):.3f} max={max(noise):.3f}")
print("cell colour: rank within each matrix; V* and V ranked together on one #56B4E9 to #E69F00 ramp")
print(f"entries clipped at zero: {sum(x == 0 for row in V for x in row)}")
