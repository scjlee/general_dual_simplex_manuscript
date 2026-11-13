import sys,re,xml.etree.ElementTree as ET
sys.path.insert(0,'render/review_scratch')
NS='{http://www.w3.org/2000/svg}'
def nums(s): return [float(v) for v in re.findall(r'-?\d+\.?\d*',s)]
def get(p):
    root=ET.parse(p).getroot(); cl={}
    for cp in root.iter(NS+'clipPath'):
        r=cp.find(NS+'rect'); cl[cp.get('id')]=[float(r.get(k)) for k in 'x y width height'.split()]
    for g in root.iter(NS+'g'):
        m=re.search(r'#([^)]+)',g.get('clip-path','') or '')
        if not m: continue
        x0,y0,w,h=cl[m.group(1)]
        if w>100 and x0<1: continue
        out=[];sizes=[]
        for e in g:
            t=e.tag[len(NS):]
            if t in('polygon','polyline'):
                v=nums(e.get('points')); xs=v[0::2]; ys=v[1::2]
                out.append((t,e.get('style'),(sum(xs)/len(xs)-x0)/w,(sum(ys)/len(ys)-y0)/h)); sizes.append((round(max(xs)-min(xs),2),round(max(ys)-min(ys),2)))
            elif t=='circle':
                out.append((t,e.get('style'),(float(e.get('cx'))-x0)/w,(float(e.get('cy'))-y0)/h)); sizes.append(e.get('r'))
            elif t=='line':
                out.append((t,e.get('style'),(float(e.get('x1'))-x0)/w,(float(e.get('y1'))-y0)/h)); sizes.append(None)
        return out,sizes,(x0,y0,w,h)
(a,sa,ca),(b,sb,cb)=get(sys.argv[1]),get(sys.argv[2])
print('clip',ca,cb)
md=max(max(abs(u[2]-v[2]),abs(u[3]-v[3])) for u,v in zip(a,b))
print('n',len(a),len(b),'styles equal',[u[1] for u in a]==[v[1] for v in b],'max centroid diff (panel fraction)',round(md,5),'absolute marker sizes equal',sa==sb)
d=[(i,u,v) for i,(u,v) in enumerate(zip(sa,sb)) if u!=v]
print(len(d)); print(d[:8])
import collections
print(collections.Counter((u,v) for _,u,v in d).most_common(5))
