#!/usr/bin/env python3
"""Check Inkscape's measured text boxes against the page and plot slots."""
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
SVG='{http://www.w3.org/2000/svg}'
root=ET.parse(HERE/'figure1.svg').getroot()
boxes={}
for row in csv.reader((HERE/'render/object-boxes.csv').open()):
    if len(row)==5:
        try: boxes[row[0]]=tuple(float(v)*25.4/96 for v in row[1:])
        except ValueError: pass
slots={
 'panelB-feature-none':(93,25,16.4,18),'panelB-feature-Normal':(110,25,16.4,18),
 'panelB-feature-Poisson':(127,25,16.4,18),'panelB-feature-Mul':(144,25,16.4,18),
 'panelB-feature-NB':(161,25,16.4,18),
 'panelC-rmse-W':(2,53,43,37),'panelC-rmse-H':(47,53,43,37),
 'panelD-rank':(95,53,47,37),'panelD-bins':(144,53,34,37),
 'panelE-by-bin':(2,96,77,40),'panelE-total':(82,96,43,40),'panelE-snr':(128,96,50,40),
 'panelF-spectrum':(2,142,52,39),'panelF-ratio':(57,142,65,39),'panelF-snr-ratio':(125,142,53,39),
 'panelG-projection-W':(2,188,54,36),'panelG-projection-H':(59,188,54,36),'panelG-fraction':(116,188,62,36)
}
def contained(b,c,tol=.15):
    x,y,w,h=b; a,z,v,j=c
    return x>=a-tol and y>=z-tol and x+w<=a+v+tol and y+h<=z+j+tol
fail=[]; texts=[]
for e in root.iter(SVG+'text'):
    id_=e.get('id'); b=boxes.get(id_)
    texts.append(id_)
    if b is None:
        fail.append((id_,'no query box'));continue
    if not contained(b,(0,0,180,225)): fail.append((id_,'outside page',b))
    for prefix,slot in slots.items():
        if id_.startswith(prefix+'-') and not contained(b,slot):
            fail.append((id_,'outside plot slot',b,slot))
    for step in ['sinkhorn','subspace','solution']:
        if id_=='schematicA-step_'+step+'_text':
            box=boxes['schematicA-step_'+step+'_box']
            if not contained(b,box): fail.append((id_,'outside pipeline box',b,box))
ids=[e.get('id') for e in root.iter() if e.get('id')]
report={'page_mm':[180,225], 'text_objects':len(texts),'duplicate_ids':len(ids)-len(set(ids)),
 'raster_images':len(list(root.iter(SVG+'image'))),'text_box_findings':fail}
(HERE/'render/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
