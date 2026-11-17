#!/usr/bin/env python3
"""Add a short h row to a separate copy of the current simplified master."""
import xml.etree.ElementTree as ET
from assemble import HERE, PT, tag, import_art, layer, text

folder = HERE / 'simplified-v2'
master = folder / 'figure1-simplified-v2.svg'
tree = ET.parse(master if master.exists() else HERE / 'simplified/figure1-simplified.svg')
root = tree.getroot()
if not master.exists():
    root.set('height', '197.5mm')
    root.set('viewBox', '0 0 180 197.5')
    root.find(tag('title')).text = 'Figure 1 simplified version 2: panels a–h'
    next(e for e in root.iter() if e.get('id') == 'page-white').set('height', '197.5')
    parent = layer(root, 'layer-panelH', 'Panel H')
    for side, x in [('W', 2), ('H', 91.5)]:
        ET.SubElement(parent, tag('g'), {
            'id': 'data-panelH-ratio-' + side,
            'transform': f'translate({x},168.05) scale({PT})'})
    text(parent, 'panel-label-h', 2, 169.85, 'h', 7, 'bold')
for side in ['W', 'H']:
    stem = 'panelH-ratio-' + side
    group = next(e for e in root.iter() if e.get('id') == 'data-' + stem)
    for child in list(group):
        group.remove(child)
    group.append(import_art(folder / 'generated' / (stem + '.svg'), stem))
tree.write(master, encoding='utf-8', xml_declaration=True)
print(master)
