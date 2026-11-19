#!/usr/bin/env python3
"""Draw the Figure 2a pipeline schematic: WH = V, scaling to Vtilde, whitening to Z, then the solver steps.

Run once from the repository root. Matrix values are illustrative (see ../schematic.py).
The SVG is created with mode "x" because it becomes the master after the first hand edit.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import schematic as sc  # noqa: E402

P = "A"
WIDTH, HEIGHT = 176, 29.2
CELL = 3.0
HEADER_TOP, HEADER_HEIGHT = 0.5, 3.8
LABEL_BASELINE = 8.0
TOP = 9.4
ROW_CENTRE = TOP + 3 * CELL
MARKER = f"{P}_marker_arrow_head"

# Left edges (mm). Each header spans its arrow and the matrix that the step produces.
W_X, H_X, V_X = 1.8, 12.6, 34.8
VTILDE_X, Z_X = 69.3, 103.3
SUBSPACE_X, SOLUTION_X, BOX_WIDTH = 128.1, 156.2, 19.5

matrices = [("W", "W", sc.rank_colours(sc.W, sc.W_COLOUR), W_X),
            ("H", "H", sc.rank_colours(sc.H, sc.H_COLOUR), H_X),
            ("V", "V", sc.log_colours(sc.V), V_X),
            ("Vtilde", "V" + sc.TILDE, sc.log_colours(sc.Vtilde), VTILDE_X),
            ("Z", "Z", sc.log_colours(sc.Z), Z_X)]


def centre(x, colours):
    return x + len(colours[0]) * CELL / 2


def label(name, symbol, colours, x):
    runs = [(symbol, True)] + ([(" (data)", False)] if name == "V" else [])
    return sc.text(f"{P}_label_{name}", centre(x, colours), LABEL_BASELINE, [runs])


v_right = V_X + 5 * CELL
outline_right = v_right + 1.5
vtilde_right, z_right = VTILDE_X + 5 * CELL, Z_X + 5 * CELL
headers = [(f"{P}_header_scaling", outline_right + 1.0, vtilde_right + 1.0, "Prescribed marginal scaling"),
           (f"{P}_header_whitening", vtilde_right + 2.0, z_right + 1.0, "Bi-marginal whitening")]
arrows = [("V_to_Vtilde", outline_right + 1.5, VTILDE_X - 1.0),
          ("Vtilde_to_Z", vtilde_right + 2.5, Z_X - 1.0),
          ("Z_to_subspace", z_right + 0.8, SUBSPACE_X - 1.0),
          ("subspace_to_solution", SUBSPACE_X + BOX_WIDTH + 0.8, SOLUTION_X - 1.0)]

layers = [
    sc.layer(f"{P}_layer_headers", "step headers",
             [sc.box(id_, x0, HEADER_TOP, x1 - x0, HEADER_HEIGHT, [title]) for id_, x0, x1, title in headers]),
    sc.layer(f"{P}_layer_model_outline", "WH = V outline",
             [sc.rect(f"{P}_model_outline", 0.3, 5.3, outline_right - 0.3, TOP + 6 * CELL + 1.2 - 5.3,
                      f"fill:none;stroke:{sc.DARK};stroke-width:{sc.FRAME_LINE:.4f};stroke-dasharray:1.2,0.8",
                      rx=0.8)]),
    *[sc.matrix(P, name, colours, x, TOP, CELL) for name, _, colours, x in matrices],
    sc.layer(f"{P}_layer_labels", "matrix labels",
             [label(name, symbol, colours, x) for name, symbol, colours, x in matrices]),
    sc.layer(f"{P}_layer_operators", "operators",
             [sc.operator(f"{P}_operator_equals", (H_X + 5 * CELL + V_X) / 2, ROW_CENTRE, "=")]),
    sc.layer(f"{P}_layer_arrows", "arrows",
             [sc.arrow(f"{P}_arrow_{name}", x0, x1, ROW_CENTRE, MARKER) for name, x0, x1 in arrows]),
    sc.layer(f"{P}_layer_steps", "solver steps",
             [sc.box(f"{P}_step_subspace", SUBSPACE_X, TOP, BOX_WIDTH, 6 * CELL, ["Subspace", "estimation"]),
              sc.box(f"{P}_step_solution", SOLUTION_X, TOP, BOX_WIDTH, 6 * CELL, ["Find", "solution"])]),
]

svg = sc.document("fig2A", "Figure 2a generalized DualSimplex pipeline", WIDTH, HEIGHT, layers, MARKER,
                  f"{P}_layer_headers")
with open(HERE / "fig2A.svg", "x", encoding="utf-8") as output:
    output.write(svg)
sc.write_input_data(HERE / "input_data.json")
sc.write_package_commit(HERE / "package_commit.txt")

print(f"canvas={WIDTH}x{HEIGHT} mm; cell={CELL} mm; text {sc.FONT / sc.PT:g} pt, operator {sc.OPERATOR_FONT / sc.PT:g} pt")
sc.print_properties()
