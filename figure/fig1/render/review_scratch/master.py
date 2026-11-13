import sys,xml.etree.ElementTree as ET,hashlib
NS='{http://www.w3.org/2000/svg}'
def top(p):
    r=ET.parse(p).getroot(); d={}
    print(p, r.get('viewBox'), r.get('width'), r.get('height'))
    def walk(e,depth,path):
        for c in e:
            i=c.get('id')
            if i is None: continue
            s=ET.tostring(c)
            d[i]=(path,c.get('transform'),hashlib.md5(s).hexdigest()[:8],len(s))
            if depth<2: walk(c,depth+1,path+'/'+i)
    walk(r,0,'')
    return d
a,b=top(sys.argv[1]),top(sys.argv[2])
for k in sorted(set(a)|set(b)):
    if a.get(k)!=b.get(k):
        x,y=a.get(k),b.get(k)
        print(k, 'HEAD',x and (x[0],x[1],x[2]), 'NEW',y and (y[0],y[1],y[2]))
print('unchanged ids',sum(1 for k in a if a[k]==b.get(k)),'of',len(a))
