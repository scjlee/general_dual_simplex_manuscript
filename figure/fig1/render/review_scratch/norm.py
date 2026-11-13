import sys,re,xml.etree.ElementTree as ET
NS='{http://www.w3.org/2000/svg}'
def clips(root):
    d={}
    for cp in root.iter(NS+'clipPath'):
        r=cp.find(NS+'rect')
        if r is not None: d[cp.get('id')]=tuple(float(r.get(k)) for k in 'x y width height'.split())
    return d
def nums(s): return [float(v) for v in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?',s)]
def norm(e,c):
    x0,y0,w,h=c; tag=e.tag[len(NS):]
    st=e.get('style','')
    def nx(v):return round((v-x0)/w,3)
    def ny(v):return round((v-y0)/h,3)
    if tag in('polyline','polygon'):
        v=nums(e.get('points')); pts=tuple((nx(v[i]),ny(v[i+1])) for i in range(0,len(v),2))
    elif tag=='circle': pts=(nx(float(e.get('cx'))),ny(float(e.get('cy'))),e.get('r'))
    elif tag=='line': pts=(nx(float(e.get('x1'))),ny(float(e.get('y1'))),nx(float(e.get('x2'))),ny(float(e.get('y2'))))
    elif tag=='rect': pts=(nx(float(e.get('x'))),ny(float(e.get('y'))),round(float(e.get('width'))/w,3),round(float(e.get('height'))/h,3))
    elif tag=='path': pts=('path',len(e.get('d','')))
    elif tag=='image': pts=('image',round(float(e.get('width'))/w,3),round(float(e.get('height'))/h,3), hash(e.get('{http://www.w3.org/1999/xlink}href') or e.get('href')))
    else: pts=None
    return (tag,st,pts)
def panels(p):
    root=ET.parse(p).getroot(); cl=clips(root); out=[]
    for g in root.iter(NS+'g'):
        cpid=re.search(r'#([^)]+)',g.get('clip-path','') or '')
        if not cpid: continue
        c=cl[cpid.group(1)]
        if c[2]>100 and c[0]<1: continue  # whole-device clip
        items=[norm(e,c) for e in g if not e.tag.endswith('text')]
        out.append(items)
    return out
a,b=panels(sys.argv[1]),panels(sys.argv[2])
print('panel groups',len(a),len(b))
for i,(x,y) in enumerate(zip(a,b)):
    same=x==y
    if not same:
        diff=[(u,v) for u,v in zip(x,y) if u!=v]
        print(' group',i,'n',len(x),len(y),'mismatches',len(diff))
        for u,v in diff[:3]: print('   H',str(u)[:200]); print('   N',str(v)[:200])
print('all in-panel groups identical after normalization:', a==b)
