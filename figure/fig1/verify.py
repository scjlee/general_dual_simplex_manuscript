#!/usr/bin/env python3
"""Check Inkscape's measured text boxes against the page and plot slots."""
import csv
import json
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
SVG='{http://www.w3.org/2000/svg}'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--simplified', action='store_true')
args=parser.parse_args()
root=ET.parse(HERE/('simplified/figure1-simplified.svg' if args.simplified else 'figure1.svg')).getroot()
page=tuple(map(float,root.get('viewBox').split()))
boxes={}
query='render/object-boxes-simplified.csv' if args.simplified else 'render/object-boxes.csv'
for row in csv.reader((HERE/query).open()):
    if len(row)==5:
        try: boxes[row[0]]=tuple(float(v)*25.4/96 for v in row[1:])
        except ValueError: pass
slots={
 'panelB-feature-none':(86,19.33,17.9,21.5),'panelB-feature-Normal':(104.5,19.33,17.9,21.5),
 'panelB-feature-Poisson':(123,19.33,17.9,21.5),'panelB-feature-Mul':(141.5,19.33,17.9,21.5),
 'panelB-feature-NB':(160,19.33,17.9,21.5),
 'panelC-rmse-W':(2,45.45,43,38.7),'panelC-rmse-H':(47,45.45,43,38.7),
 'panelD-rank':(95,45.45,47,38.7),'panelD-bins':(144,45.45,34,38.7),
 'panelE-by-bin':(2,86.65,92,36),'panelE-total':(97,86.65,43,36),'panelE-snr':(143,86.65,35,36),
 'panelF-spectrum':(2,125.15,52,30.8),'panelF-ratio':(57,125.15,65,30.8),'panelF-snr-ratio':(125,125.15,53,30.8),
 'panelG-projection-W':(2,158.45,50,40.4),'panelG-projection-H':(54,158.45,50,40.4),'panelG-fraction':(106,158.45,72,40.4)
}
if args.simplified:
    slots.pop('panelF-snr-ratio')
    slots.pop('panelG-fraction')
    slots.update({
      'panelF-spectrum':(2,125.15,40,40.4), 'panelF-ratio':(45,125.15,41,40.4),
      'panelG-projection-W':(89,125.15,43,40.4), 'panelG-projection-H':(135,125.15,43,40.4)
    })
def contained(b,c,tol=.15):
    x,y,w,h=b; a,z,v,j=c
    return x>=a-tol and y>=z-tol and x+w<=a+v+tol and y+h<=z+j+tol
fail=[]; texts=[]
for e in root.iter(SVG+'text'):
    id_=e.get('id'); b=boxes.get(id_)
    texts.append(id_)
    if b is None:
        fail.append((id_,'no query box'));continue
    if not contained(b,page): fail.append((id_,'outside page',b))
    for prefix,slot in slots.items():
        if id_.startswith(prefix+'-') and not contained(b,slot):
            fail.append((id_,'outside plot slot',b,slot))
    for step in ['sinkhorn','subspace','solution']:
        if id_=='schematicA-step_'+step+'_text':
            box=boxes['schematicA-step_'+step+'_box']
            if not contained(b,box): fail.append((id_,'outside pipeline box',b,box))
ids=[e.get('id') for e in root.iter() if e.get('id')]
labels=[''.join(e.itertext()).strip() for e in root.iter(SVG+'text') if (e.get('id') or '').startswith('panel-label-')]
expected=list('abcdefg' if args.simplified else 'abcdefgh')
if labels!=expected: fail.append(('panel labels',labels,expected))
report={'page_mm':list(page[2:]), 'text_objects':len(texts),'duplicate_ids':len(ids)-len(set(ids)),
 'raster_images':len(list(root.iter(SVG+'image'))),'text_box_findings':fail}
output='simplified/verification.json' if args.simplified else 'render/verification.json'
(HERE/output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
