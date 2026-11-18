#!/usr/bin/env python3
"""Assemble the separate compact master with f and g on one bottom row."""
import xml.etree.ElementTree as ET
from assemble import HERE, PT, tag, import_art, placements as full_placements

FOLDER = HERE / 'simplified'
MASTER = FOLDER / 'figure1-simplified.svg'
placements = [
    ('data-panelF-spectrum', 'panelF-spectrum', 2),
    ('data-panelF-ratio', 'panelF-ratio', 45),
    ('data-panelG-projection-W', 'panelG-projection-W', 89),
    ('data-panelG-projection-H', 'panelG-projection-H', 135),
]


def refresh_simplified_plots(root):
    groups = {e.get('id'): e for e in root.iter()}
    for name, _, _ in full_placements:
        panel, stem = name.split('/')
        if panel in ('panelB', 'panelC', 'panelD', 'panelE'):
            prefix = f'{panel}-{stem}'
            group = groups['data-' + prefix]
            group[:] = [import_art(HERE / panel / 'generated' / (stem + '.svg'), prefix)]
    for ident, stem, _ in placements:
        group = groups[ident]
        group[:] = [import_art(FOLDER / 'generated' / (stem + '.svg'), stem)]


if __name__ == '__main__':
    tree = ET.parse(MASTER if MASTER.exists() else HERE / 'figure1.svg')
    root = tree.getroot()
    if not MASTER.exists():
        root.set('height', '168mm')
        root.set('viewBox', '0 0 180 168')
        root.find(tag('title')).text = 'Figure 1 simplified: panels a–g'
        next(e for e in root.iter() if e.get('id') == 'page-white').set('height', '168')
        for parent in root.iter():
            for child in list(parent):
                if child.get('id') in ['data-panelF-snr-ratio-0', 'layer2',
                                       'data-panelH', 'data-panelG-error-scatter']:
                    parent.remove(child)
        label = next(e for e in root.iter() if e.get('id') == 'panel-label-g')
        label.set('x', '89')
        label.set('y', '126.95')
        for ident, _, x in placements:
            group = next(e for e in root.iter() if e.get('id') == ident)
            group.set('transform', f'translate({x},125.15) scale({PT})')

    refresh_simplified_plots(root)
    FOLDER.mkdir(exist_ok=True)
    tree.write(MASTER, encoding='utf-8', xml_declaration=True)
    print(MASTER)
