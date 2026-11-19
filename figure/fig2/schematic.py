"""Illustrative matrices and SVG primitives shared by the Figure 2a and 2b schematics.

All values are illustrative. W and H repeat the draws of
figure/fig1/panelB/make_fig1B_schematic.py (same seed, same order), so they match
Figure 1b. V = WH is noiseless. The prescribed marginals are drawn after W and H.
Notation follows README.md: Vtilde = D_r V D_c, Z = D_a^(-1/2) Vtilde D_b^(-1/2),
Wtilde = D_r W D_w^(-1), Htilde = D_h^(-1) H D_c, M = D_w D_h.
"""
import json
import random
import re
import subprocess
from math import log
from pathlib import Path
from xml.sax.saxutils import escape

PACKAGE = Path("../general_dual_simplex")

PT = 25.4 / 72
FONT = 6 * PT
OPERATOR_FONT = 8 * PT
CAP_HEIGHT = 0.716 * FONT
FRAME_LINE = 0.5 * PT
CELL_LINE = 0.4 * PT
ARROW_LINE = 0.6 * PT
DARK = "#404040"
BOX_FILL = "#f2f2f2"
TILDE = "̃"
FONT_STYLE = "font-family:'Liberation Sans',Arial,sans-serif"

SIGNAL_STOPS = ["#56B4E9", "#009E73", "#E69F00"]
W_COLOUR, H_COLOUR, M_COLOUR = "#D55E00", "#0072B2", "#CC79A7"

# ---------------------------------------------------------------- matrices
SEED = 20261109
rng = random.Random(SEED)
m, k, n = 6, 3, 5


def dirichlet(alpha, size):
    draws = [rng.gammavariate(alpha, 1) for _ in range(size)]
    return [draw / sum(draws) for draw in draws]


def matmul(A, B):
    return [[sum(A[i][c] * B[c][j] for c in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


W = [[rng.gammavariate(8 if j == i // 2 else 1.5, 1) for j in range(k)] for i in range(m)]
H_columns = [dirichlet(0.8, k) for _ in range(n)]
H = [[H_columns[j][i] for j in range(n)] for i in range(k)]
V = matmul(W, H)

MARGINAL_ALPHA = 4
a_target = dirichlet(MARGINAL_ALPHA, m)
b_target = dirichlet(MARGINAL_ALPHA, n)

SINKHORN_TOLERANCE = 1e-13
r, c = [1.0] * m, [1.0] * n
row_error = 1.0
while row_error > SINKHORN_TOLERANCE:
    r = [a_target[i] / sum(V[i][j] * c[j] for j in range(n)) for i in range(m)]
    c = [b_target[j] / sum(V[i][j] * r[i] for i in range(m)) for j in range(n)]
    row_error = max(abs(r[i] * sum(V[i][j] * c[j] for j in range(n)) - a_target[i]) / a_target[i]
                    for i in range(m))

Vtilde = [[r[i] * V[i][j] * c[j] for j in range(n)] for i in range(m)]
a = [sum(row) for row in Vtilde]
b = [sum(Vtilde[i][j] for i in range(m)) for j in range(n)]
Z = [[Vtilde[i][j] / (a[i] * b[j]) ** 0.5 for j in range(n)] for i in range(m)]

w = [sum(r[i] * W[i][j] for i in range(m)) for j in range(k)]
h = [sum(H[j][s] * c[s] for s in range(n)) for j in range(k)]
Wtilde = [[r[i] * W[i][j] / w[j] for j in range(k)] for i in range(m)]
Htilde = [[H[j][s] * c[s] / h[j] for s in range(n)] for j in range(k)]
M = [[w[i] * h[j] if i == j else 0.0 for j in range(k)] for i in range(k)]


def entries(values):
    return [x for row in values for x in row]


def write_input_data(path):
    data = {name: globals()[name] for name in
            ["SEED", "MARGINAL_ALPHA", "SINKHORN_TOLERANCE", "W", "H", "V", "a_target", "b_target",
             "r", "c", "Vtilde", "a", "b", "Z", "w", "h", "Wtilde", "M", "Htilde"]}
    path.write_text(json.dumps(data, indent=1) + "\n")


def write_package_commit(path):
    def package_git(*args):
        return subprocess.run(["git", "-C", str(PACKAGE), *args], capture_output=True, text=True).stdout

    version = re.search(r"^Version: (.+)$", (PACKAGE / "DESCRIPTION").read_text(), re.M)[1]
    path.write_text(
        "This schematic uses no package code; values are illustrative.\n"
        f"commit {package_git('rev-parse', 'HEAD')}version {version}\n"
        f"git status --porcelain R src:\n{package_git('status', '--porcelain', 'R', 'src')}"
    )


def print_properties():
    product = matmul(matmul(Wtilde, M), Htilde)
    print(f"m={m} k={k} n={n} seed={SEED}; V = WH (noiseless); W and H repeat the Figure 1b draws")
    print(f"prescribed marginals drawn from Dirichlet({MARGINAL_ALPHA}): "
          f"a={[round(x, 4) for x in a_target]} b={[round(x, 4) for x in b_target]}")
    print(f"Sinkhorn max relative row-marginal error {row_error:.2e}; "
          f"max |a - target| {max(abs(x - y) for x, y in zip(a, a_target)):.2e}, "
          f"max |b - target| {max(abs(x - y) for x, y in zip(b, b_target)):.2e}")
    print(f"sum(Vtilde)={sum(entries(Vtilde)):.15f} sum(a)={sum(a):.15f} sum(b)={sum(b):.15f}")
    print(f"column sums of Wtilde: {[sum(Wtilde[i][j] for i in range(m)) for j in range(k)]}")
    print(f"row sums of Htilde: {[sum(row) for row in Htilde]}")
    print(f"diag(M)={[M[j][j] for j in range(k)]} sum={sum(M[j][j] for j in range(k)):.15f}")
    print(f"max |Vtilde - Wtilde M Htilde| = "
          f"{max(abs(x - y) for x, y in zip(entries(Vtilde), entries(product))):.2e}")
    print("cell colour: V, Vtilde and Z are linear in log(value) between each matrix's own min and max "
          f"on {'-'.join(SIGNAL_STOPS)}; W, Wtilde ({W_COLOUR}) and H, Htilde ({H_COLOUR}) show rank "
          f"within each matrix; diag(M) ({M_COLOUR}) is linear in value / max from a 30% tint to full colour; zeros are white")


# ---------------------------------------------------------------- colours
def blend(low, high, t):
    channels = [(int(low[i:i + 2], 16), int(high[i:i + 2], 16)) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in channels)


def gradient(stops, t):
    position = t * (len(stops) - 1)
    segment = min(int(position), len(stops) - 2)
    return blend(stops[segment], stops[segment + 1], position - segment)


def log_colours(values):
    low, high = log(min(entries(values))), log(max(entries(values)))
    return [[gradient(SIGNAL_STOPS, (log(x) - low) / (high - low)) for x in row] for row in values]


def rank_colours(values, colour):
    ranked = sorted(entries(values))
    stops = [blend("#ffffff", colour, 0.12), colour]
    return [[gradient(stops, ranked.index(x) / (len(ranked) - 1)) for x in row] for row in values]


def diagonal_colours(values, colour):
    largest = max(values[j][j] for j in range(len(values)))
    stops = [blend("#ffffff", colour, 0.3), colour]
    return [[gradient(stops, x / largest) if x else "#ffffff" for x in row] for row in values]


# ---------------------------------------------------------------- SVG
def rect(id_, x, y, width, height, style, rx=0):
    corner = f' rx="{rx}"' if rx else ""
    return (f'<rect id="{id_}" x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" '
            f'height="{height:.3f}"{corner} style="{style}"/>')


def text(id_, x, y, lines, size=FONT, anchor="middle", line_height=1.2, transform=None):
    """lines: list of lines; each line is a list of (string, bold) runs."""
    style = f"{FONT_STYLE};font-size:{size:.4f}px;line-height:{line_height};text-anchor:{anchor};fill:#000000"
    spans = []
    for number, line in enumerate(lines, 1):
        y_line = y + (number - 1) * line_height * size
        runs = "".join(f'<tspan id="{id_}_line{number}_run{run}" style="font-weight:{"bold" if bold else "normal"}">'
                       f'{escape(content)}</tspan>' for run, (content, bold) in enumerate(line, 1))
        spans.append(f'<tspan id="{id_}_line{number}" sodipodi:role="line" x="{x:.3f}" y="{y_line:.3f}">{runs}</tspan>')
    placement = f' transform="{transform}"' if transform else ""
    return (f'<text id="{id_}" x="{x:.3f}" y="{y:.3f}"{placement} xml:space="preserve" style="{style}">'
            + "".join(spans) + "</text>")


def layer(id_, label, items):
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">\n' + "\n".join(items) + "\n</g>"


def group(id_, items):
    return f'<g id="{id_}">\n' + "\n".join(items) + "\n</g>"


def matrix(prefix, name, colours, x, y, cell):
    cells = [rect(f"{prefix}_{name}_r{i}_c{j}", x + (j - 1) * cell, y + (i - 1) * cell, cell, cell,
                  f"fill:{fill};stroke:#ffffff;stroke-width:{CELL_LINE:.4f}")
             for i, row in enumerate(colours, 1) for j, fill in enumerate(row, 1)]
    frame = rect(f"{prefix}_{name}_frame", x, y, len(colours[0]) * cell, len(colours) * cell,
                 f"fill:none;stroke:#000000;stroke-width:{FRAME_LINE:.4f}")
    return layer(f"{prefix}_layer_matrix_{name}", f"matrix {name}", [group(f"{prefix}_{name}_cells", cells), frame])


def box(id_, x, y, width, height, lines, line_height=1.2):
    """Grey rounded box with bold, centred text, as in Figure 1a and 1b."""
    outline = rect(f"{id_}_box", x, y, width, height,
                   f"fill:{BOX_FILL};stroke:{DARK};stroke-width:{FRAME_LINE:.4f}", rx=0.8)
    block = (len(lines) - 1) * line_height * FONT
    first_baseline = y + height / 2 - block / 2 + CAP_HEIGHT / 2
    label = text(f"{id_}_text", x + width / 2, first_baseline, [[(line, True)] for line in lines],
                 line_height=line_height)
    return group(id_, [outline, label])


def arrow(id_, x0, x1, y, marker):
    return (f'<path id="{id_}" d="M {x0:.3f},{y:.3f} H {x1:.3f}" style="fill:none;stroke:#000000;'
            f'stroke-width:{ARROW_LINE:.4f};marker-end:url(#{marker})"/>')


def operator(id_, x, y_centre, symbol):
    return text(id_, x, y_centre + 0.34 * OPERATOR_FONT, [[(symbol, True)]], size=OPERATOR_FONT)


def document(id_, title, width, height, layers, marker, current_layer):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg id="{id_}" version="1.1" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}"
   sodipodi:docname="{id_}.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
<title id="{id_}_title">{title}</title>
<sodipodi:namedview id="{id_}_namedview" inkscape:document-units="mm" pagecolor="#ffffff"
   inkscape:pageopacity="1" inkscape:current-layer="{current_layer}"/>
<defs id="{id_}_defs">
<marker id="{marker}" orient="auto" markerUnits="strokeWidth" markerWidth="9" markerHeight="9"
   viewBox="0 0 9 9" refX="8.5" refY="4.5" style="overflow:visible">
<path id="{marker}_shape" d="M 0,0.5 L 9,4.5 L 0,8.5 Z" style="fill:#000000;stroke:none"/>
</marker>
</defs>
{chr(10).join(layers)}
</svg>
"""
