import sys,xml.etree.ElementTree as ET
NS='{http://www.w3.org/2000/svg}'
def t(p):
    r=ET.parse(p).getroot(); o=[]
    for e in r.iter(NS+'text'):
        o.append((''.join(e.itertext()), e.get('style'), e.get('transform')))
    return o
a,b=t(sys.argv[1]),t(sys.argv[2])
from collections import Counter
ka=Counter((x[0],x[1]) for x in a); kb=Counter((x[0],x[1]) for x in b)
print('texts',len(a),len(b))
for k in (ka-kb).elements(): print(' -',k)
for k in (kb-ka).elements(): print(' +',k)
