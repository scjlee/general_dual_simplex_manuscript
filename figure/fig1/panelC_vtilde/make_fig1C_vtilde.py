"""Illustrative panel C alternative: ordinary variance shares in Vtilde.

Run from the repository root after variance_share.R:
python3 figure/fig1/panelC_vtilde/make_fig1C_vtilde.py
Reuses panel C's layout. After creation the SVG is the master; refreshes
replace only named data-group contents. Axes have fixed log ranges printed
below so that hand-edited labels can be checked against the input data.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "panelC"))
import make_fig1C as base

base.MODELS = {
    "poisson": ("Poisson", "Poisson", 13.0, (0.01, 2.0), (0.01, 0.03, 0.1, 0.3, 1)),
    "proportional": ("Proportional", "Proportional", 55.5, (0.001, 3.0), (0.001, 0.01, 0.1, 1)),
    "normal": ("Normal, floored at 0", "Normal, floored at 0", 98.0, (0.01, 1.0), (0.01, 0.03, 0.1, 0.3, 1)),
}


def main():
    tables = {m: {name: [] for _, name, _ in base.SCALINGS} for m in base.MODELS}
    by_name = {v[0]: k for k, v in base.MODELS.items()}
    with (HERE / "variance_share_by_rank.csv").open() as f:
        for row in csv.DictReader(f):
            tables[by_name[row["model"]]][row["scaling"]].append(row)
    for model, (name, _, _, limits, _) in base.MODELS.items():
        for _, scaling, _ in base.SCALINGS:
            rows = sorted(tables[model][scaling], key=lambda r: int(r["rank"]))
            tables[model][scaling] = rows
            means = [float(r["mean"]) for r in rows]
            print(f"{name}, {scaling}: mean sum {sum(means):.12g}%; "
                  f"band {min(float(r['lo']) for r in rows):.6g}-"
                  f"{max(float(r['hi']) for r in rows):.6g}%; axis {limits}%; "
                  f"lowest quarter {sum(means[:len(means) // 4]):.6g}%")
    master = HERE / "fig1C_vtilde.svg"
    if master.exists():
        groups = {}
        for model in base.MODELS:
            groups.update(base.data_groups(model, tables[model]))
        original = master.read_bytes()
        updated = base.replace_data(original, groups)
        if updated != original:
            master.write_bytes(updated)
        print("Refreshed data groups in", master)
    else:
        svg = base.draft(tables)
        svg = svg.replace('id="fig1C"', 'id="fig1C_vtilde"')
        svg = svg.replace("Where the variance sits after bi-marginal whitening",
                          "Where the variance sits before bi-marginal whitening")
        svg = svg.replace("Gene share of variance in Z (%)", "Gene share of total variance in Ṽ (%)")
        master.write_text(svg)
        print("Created", master)


if __name__ == "__main__":
    main()
