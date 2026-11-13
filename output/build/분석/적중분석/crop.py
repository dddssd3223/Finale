import pymupdf, re, numpy as np
from PIL import Image
def labels(doc):
    out=[]
    for pi,p in enumerate(doc):
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']:
                    t=s['text'].strip()
                    m=re.fullmatch(r'(\d{1,2})\.',t)
                    if m and s['size']>=8.5:
                        out.append((pi,int(m.group(1)),s['bbox'],s['size']))
                    if t.startswith('단답형 1') or t.startswith('서술형 1') or t.startswith('서답형 1') or t.startswith('서답형 2'):
                        out.append((pi,t[:5],s['bbox'],s['size']))
    return out
def crop(path,key,out,ybot=780,zoom=3,colsplit=300,xl=(36,296),xr=(299,560),pad=4):
    d=pymupdf.open(path); L=labels(d)
    cand=[x for x in L if x[1]==key]
    if not cand: return None
    pi,_,bb,_=cand[0]; left=bb[0]<colsplit
    x0,x1=(xl if left else xr)
    ys=[x[2][1] for x in L if x[0]==pi and ((x[2][0]<colsplit)==left) and x[2][1]>bb[1]+5]
    y1=min(ys)-pad if ys else ybot
    R=pymupdf.Rect(x0,bb[1]-pad,x1,y1)
    pm=d[pi].get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),clip=R); pm.save(out)
    im=Image.open(out).convert('L'); a=np.array(im)
    rows=np.where((a<200).sum(1)>0)[0]
    if len(rows): 
        im2=Image.open(out).crop((0,0,im.width,min(im.height,rows.max()+12))); im2.save(out)
    return (pi,R)
