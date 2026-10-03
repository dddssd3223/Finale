import sys, json, zipfile
sys.argv=['build.py']
import build
from lxml import etree
from hwpx.layout.pages import estimate_pages
build.FIGS.update(build.figs_info())
NS={'hp':'http://www.hancom.co.kr/hwpml/2011/paragraph'}
fill={}
try:
    fill={tuple(map(int,k.split(','))):v for k,v in json.load(open('fill.json')).items()}
except Exception: pass
for it in range(4):
    xml=build.write_exam('x', fill=fill)
    build.pack(xml,'tune.hwpx',[('image21','fig8.png'),('image22','fig17.png')],'x')
    e=estimate_pages('tune.hwpx')
    ps=etree.fromstring(xml.encode()).findall('hp:p',NS)
    pos={}
    for p,ls in zip(ps,e.lines):
        i=int(p.get('id'))
        if 880000<=i<890000 and ls:
            ci,j=divmod(i-880000,10); pos[(ci,j)]=(ls[0].page,ls[0].column,ls[0].vertpos)
    lastcol={}
    for p,ls in zip(ps,e.lines):
        for l in ls: lastcol[(l.page,l.column)]=max(lastcol.get((l.page,l.column),0),l.vertpos)
    changed=False
    print('iter',it,'pages',e.pages)
    for ci,col in enumerate(build.COLS):
        for j,(key,top) in enumerate(col):
            pg,cc,v=pos[(ci,j)]
            exp=(ci//2,ci%2)
            flag='' if (pg,cc)==exp else ' !!WRONG COLUMN'
            print(f'  C{ci} {key:4s} p{pg}c{cc} start={v:6d} target={top:6d} diff={v-top:6d}{flag}')
            if j>0:
                d=round((top-v)/1352)
                if d!=0:
                    fill[(ci,j)]=max(0,fill[(ci,j)]+d); changed=True
    if not changed: break
print('col bottoms', {k:v for k,v in sorted(lastcol.items())})
json.dump({f'{k[0]},{k[1]}':v for k,v in fill.items()},open('fill.json','w'))
