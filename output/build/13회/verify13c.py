from sympy import *
import numpy as np
x,A,B,C,D=symbols('x A B C D',real=True)
# 단답: g={-f (x<0), |f|-|x^2-4| (x>=0)}, f cubic; brute: f(0)=2, f'(0)=0, f(2)=0, f'(2)=±4
cands=[]
for s in (4,-4):
    f=A*x**3+B*x**2+2
    sv=solve([f.subs(x,2), diff(f,x).subs(x,2)-s],[A,B],dict=True)[0]
    cands.append((s,factor(f.subs(sv))))
print(cands)
def gfun(fx):
    fl=lambdify(x,fx)
    return lambda t: -fl(t) if t<0 else abs(fl(t))-abs(t*t-4)
for s,fx in cands:
    g=gfun(fx); e=1e-6; bad=[]
    for t0 in np.round(np.arange(-5,8,0.001),3):
        dl=(g(t0)-g(t0-e))/e; dr=(g(t0+e)-g(t0))/e
        if abs(dl-dr)>1e-2: bad.append(t0)
    print(s, 'nondiff pts', sorted(set(np.round(bad,2)))[:10], 'f(-5)', fx.subs(x,-5), 'f(0)',fx.subs(x,0))
# 서술 C26 var: f=(k a_k+1)x+2k(k+1) on [k,k+1), a_6=6
a={6:Rational(6)}
for kk in range(5,0,-1):
    # continuity at x=kk+1: (kk*a_kk+1)(kk+1)+2kk(kk+1) = ((kk+1)a_{kk+1}+1)(kk+1)+2(kk+1)(kk+2)
    ak=symbols('ak'); a[kk]=solve((kk*ak+1)*(kk+1)+2*kk*(kk+1)-(((kk+1)*a[kk+1]+1)*(kk+1)+2*(kk+1)*(kk+2)),ak)[0]
print({k_:a[k_] for k_ in sorted(a)}, sum(a[k_] for k_ in range(1,6)))
