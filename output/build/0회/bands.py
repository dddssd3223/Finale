import pymupdf, numpy as np, sys
from align import scan_ink, our_ink, z
doc=pymupdf.open('exam.pdf')
def bands(M,x,y0,y1,w=250):
    xa,xb=int(x*z),int((x+w)*z)
    r=M[int(y0*z):int(y1*z),xa:xb].sum(1)
    rows=np.nonzero(r>3)[0]; out=[];s=None;prev=None
    for i in rows:
        if s is None: s=i
        elif i-prev>2: out.append((s,prev)); s=i
        prev=i
    if s is not None: out.append((s,prev))
    return [(round(y0+a/z,1),round(y0+b/z,1)) for a,b in out if b-a>5]
if __name__=='__main__':
    pi,x,y0,y1=int(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
    w=float(sys.argv[5]) if len(sys.argv)>5 else 250
    print('scan',bands(scan_ink(pi),x,y0,y1,w)); print('ours',bands(our_ink(doc,pi),x,y0,y1,w))
