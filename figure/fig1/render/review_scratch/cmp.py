import sys,re,xml.etree.ElementTree as ET
def load(p):
    t=ET.parse(p).getroot()
    out=[]
    for e in t.iter():
        tag=e.tag.split('}')[1]
        if tag in('text','tspan','g','svg','defs','style','clipPath'): continue
        a={k.split('}')[-1]:v for k,v in e.attrib.items() if k not in('id',) and not k.endswith('href') or tag!='image'}
        out.append((tag,tuple(sorted(a.items()))))
    return out
def texts(p):
    t=ET.parse(p).getroot(); r=[]
    for e in t.iter():
        if e.tag.endswith('}text'):
            s=''.join(e.itertext())
            r.append((s,e.get('style'),e.get('transform'),e.get('x'),e.get('y')))
    return r
a,b=sys.argv[1],sys.argv[2]
la,lb=load(a),load(b)
print('nontext elements',len(la),len(lb),'identical' if la==lb else 'DIFFER')
if la!=lb:
    from collections import Counter
    ca,cb=Counter(la),Counter(lb)
    print(' only HEAD:',sum((ca-cb).values()),' only new:',sum((cb-ca).values()))
    for x in list((ca-cb).elements())[:6]: print('  -',str(x)[:300])
    for x in list((cb-ca).elements())[:6]: print('  +',str(x)[:300])
ta,tb=texts(a),texts(b)
sa,sb=set(ta),set(tb)
for x in ta:
    if x not in sb: print('  T-',x)
for x in tb:
    if x not in sa: print('  T+',x)
