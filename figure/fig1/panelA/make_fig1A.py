"""Refresh only the data inside the hand-edited Figure 1A SVG master.

Usage (repo root): python3 figure/fig1/panelA/make_fig1A.py
Inputs: tiles.csv and points_frac0.1_seed1.csv from points.R; existing fig1A.svg.
The six heatmap_* / scatter_* groups are found by id. Their opening tags
(including hand-edited transforms) and all bytes outside their contents stay
untouched. Labels, including RMSE labels, are edited separately in the master;
this script prints the current RMSE values for checking them.
"""
import csv
import math
from pathlib import Path
from xml.parsers import expat

HERE = Path(__file__).parent
POINTS = HERE / "points_frac0.1_seed1.csv"
PT = 0.3528  # mm per point
CELL = 1.8
GREY_TRUTH = "#B8B8B8"
SVG_NS = "http://www.w3.org/2000/svg"


def group_contents(svg, wanted):
    """Find byte ranges with an XML parser, without reserializing the master."""
    parser = expat.ParserCreate(namespace_separator=" ")
    stack, ranges = [], {}

    def start(name, attrs):
        id_ = attrs.get("id")
        target = id_ if id_ in wanted else None
        if target:
            if name != f"{SVG_NS} g" or target in ranges:
                raise ValueError(f"Expected one SVG group with id {target!r}")
            # Expat points at '<'. Locate '>' while respecting quoted attributes.
            pos, quote = parser.CurrentByteIndex, None
            while pos < len(svg):
                char = svg[pos:pos + 1]
                if quote:
                    if char == quote:
                        quote = None
                elif char in (b'"', b"'"):
                    quote = char
                elif char == b">":
                    break
                pos += 1
            if svg[pos - 1:pos] == b"/":
                raise ValueError(f"Data group {target!r} must have a closing tag")
            if any(parent for parent in stack):
                raise ValueError("Data groups must not be nested")
            ranges[target] = [pos + 1, None]
        stack.append(target)

    def end(name):
        target = stack.pop()
        if target:
            ranges[target][1] = parser.CurrentByteIndex

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.Parse(svg, True)
    missing = wanted - ranges.keys()
    if missing:
        raise ValueError(f"Missing data groups: {', '.join(sorted(missing))}")
    return ranges


def replace_data(svg, replacements):
    ranges = group_contents(svg, set(replacements))
    for id_, (start, end) in sorted(ranges.items(), key=lambda item: item[1][0], reverse=True):
        svg = svg[:start] + replacements[id_].encode("utf-8") + svg[end:]
    # Check the complete result before writing anything to the master.
    parser = expat.ParserCreate(namespace_separator=" ")
    ids = set()

    def check_id(name, attrs):
        id_ = attrs.get("id")
        if id_ is not None:
            if id_ in ids:
                raise ValueError(f"Duplicate SVG id: {id_}")
            ids.add(id_)

    parser.StartElementHandler = check_id
    parser.Parse(svg, True)
    return svg


def grey(value):
    g = round(0xF4 + (0x33 - 0xF4) * value)
    return f"#{g:02X}{g:02X}{g:02X}"


def heatmap(name, x, y, cells):
    nr, nc = max(c[0] for c in cells), max(c[1] for c in cells)
    rects = "".join(
        f'<rect id="tile_{name}_{r}_{c}" x="{x + (c - 1) * CELL:.2f}" y="{y + (r - 1) * CELL:.2f}" '
        f'width="{CELL}" height="{CELL}" style="fill:{grey(v)};stroke:#FFFFFF;stroke-width:0.1"/>'
        for r, c, v in cells)
    frame = (f'<rect id="heatmap_frame_{name}" x="{x:.2f}" y="{y:.2f}" '
             f'width="{nc * CELL:.2f}" height="{nr * CELL:.2f}" '
             f'style="fill:none;stroke:#666666;stroke-width:{0.4 * PT:.3f}"/>')
    return rects + frame


def scatter(key, colour, yc, pts, span, c2_lo, c2_hi):
    sx, sw = 115.6, 15.0
    fy, inner = yc - sw / 2, sw - 1.6

    def to_xy(p):
        return (sx + 0.8 + (p[0] + span / 2) / span * inner,
                fy + 0.8 + (c2_hi - p[1]) / span * inner + (inner - (c2_hi - c2_lo) / span * inner) / 2)

    verts = [to_xy(p) for p in [(0, 2 / math.sqrt(6)), (1 / math.sqrt(2), -1 / math.sqrt(6)),
                              (-1 / math.sqrt(2), -1 / math.sqrt(6))]]
    simplex = (f'<path id="simplex_{key}" d="M {verts[0][0]:.2f},{verts[0][1]:.2f} L {verts[1][0]:.2f},{verts[1][1]:.2f} '
               f'L {verts[2][0]:.2f},{verts[2][1]:.2f} Z" '
               f'style="fill:none;stroke:#999999;stroke-width:{0.4 * PT:.3f};stroke-dasharray:0.6,0.4"/>')

    def circles(set_):
        return "".join(f'<circle id="point_{key}_{set_}_{i}" cx="{x:.2f}" cy="{y:.2f}" r="0.28"/>'
                       for i, (x, y) in enumerate(map(to_xy, pts[set_]), 1))

    frame = (f'<rect id="frame_{key}" x="{sx}" y="{fy:.2f}" width="{sw}" height="{sw}" '
             f'style="fill:#FFFFFF;stroke:{colour};stroke-width:{0.6 * PT:.3f}"/>')
    return (f'{frame}{simplex}<g id="points_truth_{key}" style="fill:{GREY_TRUTH}">{circles("truth")}</g>'
            f'<g id="points_oracle_{key}" style="fill:{colour};fill-opacity:0.85">{circles(key)}</g>')


def main():
    tiles = {}
    with (HERE / "tiles.csv").open() as f:
        for row in csv.DictReader(f):
            tiles.setdefault(row["matrix"], []).append((int(row["row"]), int(row["col"]), float(row["value"])))

    pts, hs = {}, {}
    with POINTS.open() as f:
        for row in csv.DictReader(f):
            h1, h2, h3 = (float(row[c]) for c in ("h1", "h2", "h3"))
            pts.setdefault(row["set"], []).append(((h2 - h3) / math.sqrt(2), (2 * h1 - h2 - h3) / math.sqrt(6)))
            hs.setdefault(row["set"], []).extend((h1, h2, h3))

    allp = [p for points in pts.values() for p in points]
    c1_max = max(abs(p[0]) for p in allp) * 1.06
    c2_lo, c2_hi = min(p[1] for p in allp), max(p[1] for p in allp)
    pad = 0.06 * (c2_hi - c2_lo)
    c2_lo, c2_hi = c2_lo - pad, c2_hi + pad
    span = max(2 * c1_max, c2_hi - c2_lo)

    # CSV names X/Y are historical data keys, independent of displayed notation.
    replacements = {f"heatmap_{name}": heatmap(name, x, y, tiles[name])
                    for name, x, y in [("W", 7.5, 19.5), ("H", 3.0, 41.5),
                                       ("X", 26.0, 26.0), ("Y", 62.8, 26.0)]}
    for key, colour, yc in [("uniform", "#E07B28", 18.0), ("expression", "#2A7BBF", 48.4)]:
        replacements[f"scatter_{key}"] = scatter(key, colour, yc, pts, span, c2_lo, c2_hi)
        error = math.sqrt(sum((x - y) ** 2 for x, y in zip(hs[key], hs["truth"])) / len(hs[key]))
        print(f"{key}: oracle RMSE {error:.6f} (label {error:.3f}); check the master label separately")

    master = HERE / "fig1A.svg"
    original = master.read_bytes()
    updated = replace_data(original, replacements)
    if updated != original:
        master.write_bytes(updated)
    print("Updated only data-group contents in", master)


if __name__ == "__main__":
    main()
