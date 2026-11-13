import numpy as np
from fractions import Fraction as Fr
# Q16: f={-x^2+2x+3 (x<2), x+k (x>=2)}, k>-2; g(t)=max on [t,t+2]; continuity
def gmax(t,kv):
    xs=np.linspace(t,t+2,4001)
    v=np.where(xs<2,-xs**2+2*xs+3,xs+kv)
    return v.max()
ok=[]
for kv in np.round(np.arange(-1.95,4.0001,0.05),3):
    ts=np.arange(-3,5,0.0005)
    gs=np.array([gmax(t,kv) for t in ts[::1]]) if False else None
    # check jumps near critical t = 0 and t = 2 (and general scan coarse)
    bad=False
    for t0 in [0.0,2.0,-1.0,1.0]:
        l=gmax(t0-1e-6,kv); r=gmax(t0,kv); r2=gmax(t0+1e-6,kv)
        if abs(l-r)>1e-3 or abs(r2-r)>1e-3: bad=True
    if not bad: ok.append(kv)
print('Q16 k range', min(ok), max(ok), len(ok))
print('g(3) at ends', gmax(3,min(ok)), gmax(3,max(ok)), gmax(3,-1)+gmax(3,2))
# coarse full scan for k=-1,2 and a bad one
for kv in [-1,2,-1.05,2.05,0.5]:
    ts=np.arange(-3,5,0.001); g=np.array([gmax(t,kv) for t in ts]); print(kv, np.abs(np.diff(g)).max())
# Q18: f=x^2+ax+b ; g={|f|-x^2 (x<=0), f^2+2x^3 (x>0)}
def chk(av,bv):
    f=lambda t:t*t+av*t+bv
    g=lambda t:(abs(f(t))-t*t) if t<=0 else f(t)**2+2*t**3
    e=1e-6
    nd=[]
    for t0 in sorted(set([0.0]+[r.real for r in np.roots([1,av,bv]) if abs(r.imag)<1e-12])):
        if abs(g(t0-e)-g(t0))>1e-4 or abs(g(t0+e)-g(t0))>1e-4: nd.append(t0); continue
        dl=(g(t0)-g(t0-e))/e; dr=(g(t0+e)-g(t0))/e
        if abs(dl-dr)>1e-3: nd.append(t0)
    # nondiff only at x=b
    if not (len(nd)==1 and abs(nd[0]-bv)<1e-9): return False
    xs=np.linspace(-20,-1e-6,200001); vals=[g(t) for t in xs[::50]]
    v=np.array(vals); return bool(np.any(np.sign(v[:-1])!=np.sign(v[1:])) or np.any(v==0))
sols=[(av,bv) for av in np.round(np.arange(-6,6.001,0.25),2) for bv in [-2,-1,-0.5,0,0.5,1,2] if chk(av,bv)]
print('Q18', sols)
f=lambda t:t*t-1; g=lambda t:(abs(f(t))-t*t) if t<=0 else f(t)**2+2*t**3
print('ans', g(-0.5)+g(2))
