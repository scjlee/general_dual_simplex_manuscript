"""Render saved scaled-matrix variance shares. Run from the manuscript root.
Existing SVGs are masters: refresh only named curve/band groups after first creation.
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / 'panelA'))
from make_fig1A import replace_data

PT = 25.4 / 72
W, H = 180, 166
PLOT_W, PLOT_H = 65, 37
YMIN, YMAX = 0.0005, 1
TICKS = (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1)
COLOURS = ('#440154', '#443983', '#31688e', '#21918c', '#35b779', '#90d743', '#B79D12')
PANELS = {
    'Poisson': ('Poisson', 17, 20, 'FRACTION', 'Library fraction'),
    'NB': ('Negative binomial', 108, 20, 'FRACTION', 'Library fraction'),
    'Mul': ('Multiplicative lognormal', 17, 98, 'MUL_SD', 'Log SD'),
    'Normal': ('Normal, floored at 0', 108, 98, 'NORMAL_SD', 'Additive SD'),
}


def txt(id_, x, y, content, size=6, anchor='start', weight='normal', transform=''):
    tr = f' transform="{transform}"' if transform else ''
    return (f'<text id="{id_}" x="{x:g}" y="{y:g}"{tr} '
            f'style="font-family:Liberation Sans,Arial,sans-serif;font-size:{size*PT:.4f}px;'
            f'font-weight:{weight};text-anchor:{anchor};fill:#222222">{content}</text>')


def line(id_, x1, y1, x2, y2, colour='#666666', width=0.5, dash=''):
    d = f';stroke-dasharray:{dash}' if dash else ''
    return (f'<path id="{id_}" d="M{x1:g},{y1:g} L{x2:g},{y2:g}" '
            f'style="fill:none;stroke:{colour};stroke-width:{width*PT:.4f}{d}"/>')


def layer(id_, label, body):
    return f'<g id="{id_}" inkscape:groupmode="layer" inkscape:label="{label}">{body}</g>'


def key(value):
    return f'{value:g}'.replace('.', 'p')


def main():
    tables = defaultdict(list)
    with (HERE / 'variance_by_rank_bins.csv').open() as stream:
        for row in csv.DictReader(stream):
            model = row['NOISE']
            parameter = float(row[PANELS[model][3]])
            dispersion = float(row['DISPERSION']) if model == 'NB' else 0
            tables[model, parameter, dispersion].append(row)
    groups, axes, labels = {}, '', ''
    for model, (title, left, top, field, legend_title) in PANELS.items():
        bottom = top + PLOT_H
        parameters = sorted({p for m, p, _ in tables if m == model})
        colours = {p: COLOURS[round(i*6/(len(parameters)-1))] for i, p in enumerate(parameters)}
        n = max(int(r['rank_last']) for (m, _, _), rows in tables.items() if m == model for r in rows)
        px = lambda rank: left + PLOT_W * (rank - 1) / (n - 1)
        py = lambda value: bottom - PLOT_H * math.log10(value/YMIN) / math.log10(YMAX/YMIN)
        for value in TICKS:
            y = py(value)
            axes += line(f'grid_{model}_y_{key(value)}', left, y, left+PLOT_W, y, '#E4E4E4', 0.4)
            axes += txt(f'tick_{model}_y_{key(value)}', left-1.5, y+0.65, f'{value:g}%', 5.5, 'end')
        for rank in (1, 1000, 2000, 3000):
            x = px(rank)
            axes += line(f'grid_{model}_x_{rank}', x, top, x, bottom, '#EEEEEE', 0.4)
            axes += line(f'tickmark_{model}_x_{rank}', x, bottom, x, bottom+0.8)
            axes += txt(f'tick_{model}_x_{rank}', x, bottom+3.8, str(rank), 5.5, 'middle')
        axes += line(f'axis_{model}_x', left, bottom, left+PLOT_W, bottom)
        axes += line(f'axis_{model}_y', left, bottom, left, top)
        labels += txt(f'title_{model}', left, top-3, title, 7.5, weight='bold')
        labels += txt(f'legend_title_{model}', left, bottom+8, legend_title, 6, weight='bold')
        for i, parameter in enumerate(parameters):
            x, y = left + (i % 4)*16, bottom+13+(i//4)*5
            labels += line(f'legend_line_{model}_{key(parameter)}', x, y-0.6, x+3, y-0.6, colours[parameter], 0.6)
            labels += txt(f'legend_value_{model}_{key(parameter)}', x+4, y, f'{parameter:g}', 6)
        if model == 'NB':
            for i, dispersion in enumerate(sorted({d for m, _, d in tables if m == model})):
                x, y = left+i*31, bottom+23
                labels += line(f'legend_disp_line_{key(dispersion)}', x, y-0.6, x+5, y-0.6,
                               '#555555', 0.5, '' if dispersion == 0.01 else '1.2,0.7')
                labels += txt(f'legend_disp_text_{key(dispersion)}', x+6.5, y, f'Dispersion {dispersion:g}', 6)
        for (m, parameter, dispersion), rows in sorted(tables.items()):
            if m != model:
                continue
            rows.sort(key=lambda r: float(r['rank']))
            id_ = f'{model}_{key(parameter)}_{key(dispersion)}'
            points = lambda col, rr: ' L'.join(f'{px(float(r["rank"])):.3f},{py(float(r[col])):.3f}' for r in rr)
            colour = colours[parameter]
            band = f'<path id="range_{id_}" d="M{points("hi_pct", rows)} L{points("lo_pct", rows[::-1])} Z" style="fill:{colour};fill-opacity:0.15;stroke:none"/>'
            dash = ';stroke-dasharray:1.2,0.7' if model == 'NB' and dispersion == 0.1 else ''
            curve = f'<path id="mean_{id_}" d="M{points("mean_pct", rows)}" style="fill:none;stroke:{colour};stroke-width:{0.45*PT:.4f}{dash}"/>'
            groups[f'band_{id_}'] = band
            groups[f'curve_{id_}'] = curve
        lo = min(float(r['lo_pct']) for (m, _, _), rows in tables.items() if m == model for r in rows)
        hi = max(float(r['hi_pct']) for (m, _, _), rows in tables.items() if m == model for r in rows)
        print(f'{model}: {n} ranks; {len(parameters)} colour levels; band range {lo:.8g}–{hi:.8g}%; axes {YMIN}–{YMAX}%.')
    labels += txt('shared_axis_x', 95, 163, 'Gene rank by observed total (low to high)', 7, 'middle')
    labels += txt('shared_axis_y', -79, 3.5, 'Gene share of variance in scaled matrix (%)', 7, 'middle', transform='rotate(-90)')
    title = txt('panel_letter', 1.2, 5, 'C', 10, weight='bold')
    title += txt('panel_title', 8, 5, 'Gene variance across noise levels', 8, weight='bold')
    title += txt('panel_subtitle', 8, 9, 'Uniform scaling; 30-gene rank bins; mean and range of 10 seeds', 6)
    master = HERE / 'fig1C_sweep.svg'
    if master.exists():
        original = master.read_bytes()
        updated = replace_data(original, groups)
        if updated != original:
            master.write_bytes(updated)
        print('Refreshed data groups only; axes and labels remain the master.')
        return
    data_layer = lambda prefix: ''.join(f'<g id="{id_}">{body}</g>' for id_, body in groups.items() if id_.startswith(prefix))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" id="fig1C_sweep">'
           + layer('layer_axes', 'Axes', axes)
           + layer('layer_ranges', 'Seed ranges', data_layer('band_'))
           + layer('layer_curves', 'Mean variance shares', data_layer('curve_'))
           + layer('layer_labels', 'Labels and legends', labels)
           + layer('layer_title', 'Panel title', title) + '</svg>\n')
    master.write_text(svg)
    print('Created', master)


if __name__ == '__main__':
    main()
