# g = f+2x (f>=0), 3f (f<0); f monic cubic. count discontinuities ==1, nondiff ==2.
import numpy as np, itertools
def analyze(cf):
    f=np.poly1d(cf); fp=f.deriv()
    g=lambda t: f(t)+2*t if f(t)>=0 else 3*f(t)
    rts=sorted(set(np.round([r.real for r in f.r if abs(r.imag)<1e-5],5)))
    disc=0; nd=0; e=1e-6
    for r in rts:
        gl,g0,gr=g(r-e),g(r),g(r+e)
        if abs(gl-g0)>1e-4 or abs(gr-g0)>1e-4: disc+=1; nd+=1; continue
        dl=(g0-gl)/e; dr=(gr-g0)/e
        if abs(dl-dr)>1e-3: nd+=1
    return disc,nd
sols=[]
grid=np.arange(-7,7.01,0.5)
for p,q,s in itertools.combinations_with_replacement(grid,3):
    cf=np.poly([p,q,s])
    if analyze(cf)==(1,2): sols.append((p,q,s))
for p in grid:
  for b in np.arange(-6,6.01,1):
    for c in np.arange(0.5,10,1):
      if b*b-4*c<0:
        cf=np.polymul([1,-p],[1,b,c])
        if analyze(cf)==(1,2): sols.append(('cplx',p,b,c))
print(len(sols)); print(sols[:60])
