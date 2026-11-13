#!/usr/bin/env python3
"""Assemble the editable figure; later runs replace named generated groups only."""
from pathlib import Path
from copy import deepcopy
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SVG = 'http://www.w3.org/2000/svg'
INK = 'http://www.inkscape.org/namespaces/inkscape'
SOD = 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
XLINK = 'http://www.w3.org/1999/xlink'
for prefix, ns in [('',SVG),('inkscape',INK),('sodipodi',SOD),('xlink',XLINK)]:
    ET.register_namespace(prefix,ns)
def tag(x): return '{'+SVG+'}'+x
PT = 25.4/72

def text(parent, id_, x, y, value, size=5.5, weight='normal', anchor='start'):
    e=ET.SubElement(parent,tag('text'),{'id':id_,'x':str(x),'y':str(y),
      'style':f'font-family:Liberation Sans,Arial,sans-serif;font-size:{size*PT:.5f}px;font-weight:{weight};text-anchor:{anchor};fill:#000000'})
    e.text=value
    return e

def import_art(path,prefix,scale=1,clamp_text=False):
    src=ET.parse(path).getroot()
    g=ET.Element(tag('g'),{'id':prefix+'-content'})
    if src.get('class'): g.set('class',src.get('class'))
    for c in src:
        if c.tag in ('{'+SOD+'}namedview',tag('metadata'),tag('title')): continue
        g.append(deepcopy(c))
    # Percent backgrounds would resolve against the entire assembled page.
    for parent in g.iter():
        for child in list(parent):
            if child.tag == tag('rect') and child.get('width') == '100%': parent.remove(child)
    ids={e.get('id'):prefix+'-'+e.get('id') for e in g.iter() if e.get('id')}
    for i,e in enumerate(g.iter()):
        if e.get('id') in ids: e.set('id',ids[e.get('id')])
        elif not e.get('id'): e.set('id',f'{prefix}-{e.tag.split("}")[-1]}-{i:04d}')
        for key,value in list(e.attrib.items()):
            if key=='id': continue
            for old,new in ids.items():
                value=value.replace('url(#'+old+')','url(#'+new+')')
                if value=='#'+old: value='#'+new
            e.set(key,value)
        # Original schematics use mm units; enlarge their small labels at final size.
        if clamp_text and e.tag==tag('text'):
            style=e.get('style','')
            m=re.search(r'font-size:([0-9.]+)px',style)
            if m:
                size=float(m[1]); size=max(5*PT/scale,min(7*PT/scale,size))
                style=re.sub(r'font-size:[0-9.]+px',f'font-size:{size:.5f}px',style)
                e.set('style',style)
    if prefix == 'schematicA':
        labels={'feature_axis_downleft_label':'sample₁ expr.','feature_axis_downright_label':'sample₂ expr.',
                'sample_axis_downleft_label':'feature₁ expr.','sample_axis_downright_label':'feature₂ expr.'}
        for e in g.iter(tag('text')):
            key=e.get('id','').removeprefix('schematicA-')
            if key in labels:
                for child in list(e): e.remove(child)
                e.text=labels[key]
    if prefix == 'schematicB':
        for e in g.iter(tag('text')):
            short={'label_W':'W','label_H':'H','label_Vstar':'V*','label_epsilon':'ε','label_V':'V'}
            key=e.get('id','').removeprefix('schematicB-')
            if key in short:
                for child in list(e): e.remove(child)
                e.text=short[key]
    return g

def layer(parent,id_,label):
    return ET.SubElement(parent,tag('g'),{'id':id_,'{'+INK+'}groupmode':'layer','{'+INK+'}label':label})

placements=[
 ('panelB/feature-none',93,25),('panelB/feature-Normal',110,25),
 ('panelB/feature-Poisson',127,25),('panelB/feature-Mul',144,25),('panelB/feature-NB',161,25),
 ('panelC/rmse-W',2,53),('panelC/rmse-H',47,53),
 ('panelD/rank',95,53),('panelD/bins',144,53),
 ('panelE/by-bin',2,96),('panelE/total',82,96),('panelE/snr',128,96),
 ('panelF/spectrum',2,142),('panelF/ratio',57,142),('panelF/snr-ratio',125,142),
 ('panelG/projection-W',2,188),('panelG/projection-H',59,188),('panelG/fraction',116,188)
]
master=HERE/'figure1.svg'
if master.exists():
    tree=ET.parse(master); root=tree.getroot()
else:
    root=ET.Element(tag('svg'),{'id':'figure1','width':'180mm','height':'225mm','viewBox':'0 0 180 225','version':'1.1','{'+INK+'}version':'1.4.4'})
    tree=ET.ElementTree(root)
    ET.SubElement(root,tag('title'),{'id':'figure1-title'}).text='Figure 1 draft: selected panels A–G'
    ET.SubElement(root,'{'+SOD+'}namedview',{'id':'figure1-view','{'+INK+'}document-units':'mm','pagecolor':'#ffffff','{'+INK+'}pageopacity':'1'})
    bg=layer(root,'layer-background','Page')
    bg.set('{'+SOD+'}insensitive','true')
    ET.SubElement(bg,tag('rect'),{'id':'page-white','x':'0','y':'0','width':'180','height':'225','fill':'white'})
    layers={letter:layer(root,'layer-panel'+letter,'Panel '+letter) for letter in 'ABCDEFG'}
    for letter,x,y,heading in [('a',2,2.7,''),('b',93,2.7,''),('c',2,51,'Deconvolution'),('d',95,51,'Variance share'),('e',2,94,'Signal and noise'),('f',2,140,'Spectral separation'),('g',2,186,'Projection')]:
        text(layers[letter.upper()],'panel-label-'+letter,x,y,letter,7,'bold')
        if heading: text(layers[letter.upper()],'panel-heading-'+letter,x+4,y,heading,6)
    for letter,path,x,y,scale in [('A','panelA/fig1A.svg',2,4,0.64),('B','panelB/fig1B_schematic.svg',93,4,62.5/134)]:
        g=ET.SubElement(layers[letter],tag('g'),{'id':'schematic-panel'+letter,'transform':f'translate({x},{y}) scale({scale})'})
        g.append(import_art(HERE/path,'schematic'+letter,scale,True))
    text(layers['B'],'panelB-example-note',93,22.5,'Feature simplices: seed 17; noise level 0.5')
    table=ET.SubElement(layers['B'],tag('g'),{'id':'noise-variance-table'})
    rows=[('Noise','Variance'),('Normal','constant‡'),('Poisson','linear (L)'),('Mul','quadratic (Q)'),('NB','L + Q')]
    for row,(a,b) in enumerate(rows):
        y=4+row*3.2
        ET.SubElement(table,tag('rect'),{'id':f'noise-table-row-{row}','x':'157','y':str(y),'width':'21','height':'3.2','fill':'#f2f2f2' if row==0 else 'white','stroke':'#666666','stroke-width':'0.15'})
        text(table,f'noise-table-name-{row}',157.5,y+2.2,a,5,'bold' if row==0 else 'normal')
        text(table,f'noise-table-variance-{row}',165,y+2.2,b,5,'bold' if row==0 else 'normal')
    for name,x,y in placements:
        letter=name[5]
        ident=name.replace('/','-')
        ET.SubElement(layers[letter],tag('g'),{'id':'data-'+ident,'transform':f'translate({x},{y}) scale({PT})'})
# Replace only generated plot content, preserving the master document and placement.
by_id={e.get('id'):e for e in root.iter()}
for name,x,y in placements:
    ident=name.replace('/','-')
    target=by_id['data-'+ident]
    for child in list(target): target.remove(child)
    target.append(import_art(HERE/name.split('/')[0]/'generated'/(name.split('/')[1]+'.svg'),ident))
# Preserve SVG text whitespace: pretty-printing inside xml:space=preserve text
# inserts visible spaces and breaks multiline labels in Inkscape.
for e in root.iter(tag('text')):
    if e.text and '\n' in e.text and not e.text.strip(): e.text=None
    for child in e.iter():
        if child.text and '\n' in child.text and not child.text.strip(): child.text=None
        if child.tail and '\n' in child.tail and not child.tail.strip(): child.tail=None
tree.write(master,encoding='utf-8',xml_declaration=True)
print(master)
