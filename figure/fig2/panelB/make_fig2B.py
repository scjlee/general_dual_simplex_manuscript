#!/usr/bin/env python3
"""Draw the Figure 2b schematic: the linked dual simplex factorization Vtilde = Wtilde M Htilde.

Run once from the repository root. Matrix values are illustrative (see ../schematic.py);
Vtilde is the same matrix as in Figure 2a. The SVG is created with mode "x" because it
becomes the master after the first hand edit.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import schematic as sc  # noqa: E402

P = "B"
WIDTH, HEIGHT = 176, 34.4
CELL = 4.0
MARGINAL_BASELINE = 3.4
LABEL_BASELINE = 8.3
TOP = 9.8
ROW_CENTRE = TOP + 3 * CELL
MARKER = f"{P}_marker_arrow_head"

VTILDE_X, EQUALS_X = 18.6, 48.6
WTILDE_X, M_X, HTILDE_X = 58.6, 73.6, 88.6
KEY_X, KEY_WIDTH, KEY_TITLE_HEIGHT = 136.7, 39.0, 4.6
KEY_BOTTOM = TOP + 6 * CELL

matrices = [("Vtilde", "V" + sc.TILDE, sc.log_colours(sc.Vtilde), VTILDE_X),
            ("Wtilde", "W" + sc.TILDE, sc.rank_colours(sc.Wtilde, sc.W_COLOUR), WTILDE_X),
            ("M", "M", sc.diagonal_colours(sc.M, sc.M_COLOUR), M_X),
            ("Htilde", "H" + sc.TILDE, sc.rank_colours(sc.Htilde, sc.H_COLOUR), HTILDE_X)]
vtilde_centre = VTILDE_X + 5 * CELL / 2

marginals = [
    sc.text(f"{P}_column_marginal", vtilde_centre, MARGINAL_BASELINE,
            [[("Column marginal = ", False), ("b", True)]]),
    sc.text(f"{P}_row_marginal", VTILDE_X - 1.6, ROW_CENTRE,
            [[("Row marginal = ", False), ("a", True)]],
            transform=f"rotate(-90,{VTILDE_X - 1.6:.3f},{ROW_CENTRE:.3f})"),
]

properties = [("bullet", [("Columns of W" + sc.TILDE + " sum to 1", False)]),
              ("bullet", [("Rows of H" + sc.TILDE + " sum to 1", False)]),
              ("bullet", [("Diagonal of M sums to 1", False)]),
              ("bullet", [("sum(", False), ("a", True), (") = sum(", False), ("b", True), (") = 1", False)]),
              ("sub", [("sum(V" + sc.TILDE + ") = 1", False)])]
steps = [4.4, 4.4, 4.4, 3.4]
list_centre = (KEY_TITLE_HEIGHT + 0.5 + KEY_BOTTOM) / 2
first_baseline = list_centre - (sum(steps) + sc.CAP_HEIGHT) / 2 + sc.CAP_HEIGHT
baselines = [first_baseline + sum(steps[:i]) for i in range(len(properties))]


def key_property(number, kind, runs, baseline):
    indent = 0 if kind == "bullet" else 4.5
    marker = "•" if kind == "bullet" else "–"
    return sc.group(f"{P}_key_property_{number}", [
        sc.text(f"{P}_key_property_{number}_marker", KEY_X + 2.5 + indent, baseline, [[(marker, False)]],
                anchor="start"),
        sc.text(f"{P}_key_property_{number}_text", KEY_X + 5.0 + indent, baseline, [runs], anchor="start")])


key = [sc.rect(f"{P}_key_frame", KEY_X, 0.5, KEY_WIDTH, KEY_BOTTOM - 0.5,
               f"fill:#ffffff;stroke:{sc.DARK};stroke-width:{sc.FRAME_LINE:.4f}", rx=0.8),
       sc.box(f"{P}_key_title", KEY_X, 0.5, KEY_WIDTH, KEY_TITLE_HEIGHT, ["Key properties"]),
       *[key_property(number, kind, runs, y)
         for number, ((kind, runs), y) in enumerate(zip(properties, baselines), 1)]]

layers = [
    *[sc.matrix(P, name, colours, x, TOP, CELL) for name, _, colours, x in matrices],
    sc.layer(f"{P}_layer_labels", "matrix labels",
             [sc.text(f"{P}_label_{name}", x + len(colours[0]) * CELL / 2, LABEL_BASELINE, [[(symbol, True)]])
              for name, symbol, colours, x in matrices]),
    sc.layer(f"{P}_layer_marginals", "marginal labels", marginals),
    sc.layer(f"{P}_layer_operators", "operators", [sc.operator(f"{P}_operator_equals", EQUALS_X, ROW_CENTRE, "=")]),
    sc.layer(f"{P}_layer_key_properties", "key properties", key),
]

svg = sc.document("fig2B", "Figure 2b linked dual simplex factorization of the scaled matrix", WIDTH, HEIGHT,
                  layers, MARKER, f"{P}_layer_labels")
with open(HERE / "fig2B.svg", "x", encoding="utf-8") as output:
    output.write(svg)
sc.write_input_data(HERE / "input_data.json")
sc.write_package_commit(HERE / "package_commit.txt")

print(f"canvas={WIDTH}x{HEIGHT} mm; cell={CELL} mm; text {sc.FONT / sc.PT:g} pt, operator {sc.OPERATOR_FONT / sc.PT:g} pt")
sc.print_properties()
