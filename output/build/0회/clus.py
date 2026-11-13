import numpy as np, pymupdf, sys
import align; z=align.z=4
pg=int(sys.argv[1]); x0,y0,x1,y1=map(float,sys.argv[2:6]); gap=float(sys.argv[6]) if len(sys.argv)>6 else 3
def clusters(M):
    reg=M[int(y0*z):int(y1*z), int(x0*z):int(x1*z)]
    cols=reg.sum(0)>0; out=[]; s=None; last=None
    for i,c in enumerate(cols):
        if c:
            if s is None: s=i
            elif i-last>gap*z: out.append((s,last)); s=i
            last=i
    if s is not None: out.append((s,last))
    res=[]
    for a,b in out:
        rows=np.nonzero(reg[:,a:b+1].sum(1))[0]
        res.append((round(x0+a/z,1),round(x0+b/z,1),round(y0+rows[0]/z,1),round(y0+rows[-1]/z,1)))
    return res
print('scan'); [print(' ',c) for c in clusters(align.scan_ink(pg))]
print('ours'); [print(' ',c) for c in clusters(align.our_ink(pymupdf.open('exam.pdf'),pg))]
