import numpy as np, sympy as sp
from fractions import Fraction as Fr
# ---- 17: f = x(x-3)^2 (x<=3), a(x-3)(x-b) (x>3); g(t)=#{f(x)=tx}
def g17(a,b,t):
    x=sp.symbols('x'); n=0; sols=set()
    for r in sp.Poly(x*(x-3)**2-t*x,x).all_roots():
        if r.is_real and r<=3: sols.add(sp.nsimplify(r))
    for r in sp.Poly(a*(x-3)*(x-b)-t*x,x).all_roots():
        if r.is_real and r>3: sols.add(sp.nsimplify(r))
    return len(sols)
def g17n(a,b,t):  # numeric
    s=set()
    for r in np.roots([1,-6,9-t,0]):
        if abs(r.imag)<1e-9 and r.real<=3+1e-12: s.add(round(r.real,7))
    for r in np.roots([a,-a*(3+b)-t,3*a*b]):
        if abs(r.imag)<1e-9 and r.real>3+1e-9: s.add(round(r.real,7))
    return len(s)
ok=[]
for a in range(1,60):
    for b in range(1,200):
        e=1e-6
        if g17n(a,b,-12+e)-g17n(a,b,-12-e)==2: ok.append((a,b))
print('17 pairs',ok,'sum a+b',sum(a+b for a,b in ok))
print('17 g profile (4,12):',[ (t,g17n(4,12,t)) for t in (-20,-12,-11,-5,0,3,9,10)])
# ---- 18: f=-x^2 (x<0), x^2-x (x>=0); g=a(x+1) (x<-1), 0 (x>=-1); h=int_0^x (g-f)
x,a=sp.symbols('x a',real=True)
def k(xx,aa):
    if xx<-1: return aa*(xx+1)+xx**2
    if xx<0: return xx**2
    return -(xx**2-xx)
def h(X,aa):
    if X>=0: return sp.integrate(x-x**2,(x,0,X)) if X<=0 else sp.Rational(X**2,2)-sp.Rational(X**3,3) if False else (sp.Rational(1,2)*X**2-sp.Rational(1,3)*X**3)
    if X>=-1: return -sp.integrate(x**2,(x,X,0))
    return -(sp.integrate(x**2+aa*x+aa,(x,X,-1))+sp.Rational(1,3))
def nroots(aa):

    def H(X):
        if X>=0: return X**2/2-X**3/3
        if X>=-1: return X**3/3
        return -((-1/3+aa/2-aa)-(X**3/3+aa*X**2/2+aa*X)+1/3)
    xs=np.linspace(-30,10,400001); v=np.array([H(t) for t in xs])
    cnt=0
    for i in range(len(xs)-1):
        if v[i]==0 or v[i]*v[i+1]<0: cnt+=1
    return cnt, min(abs(v[(xs>-3.01)&(xs<-2.99)]))
for aa in (3,4,4.4,4.5,4.6,6):
    print('18 a=',aa,nroots(aa))
A=sp.Rational(9,2)
print('h(-3)=',h(-3,A),'h(-3/2)=',h(sp.Rational(-3,2),A),'h(1)=',h(1,A),'h(3/2)=',h(sp.Rational(3,2),A))
print('roots of h=0:', sp.solve(sp.Rational(1,2)*x**2-sp.Rational(1,3)*x**3,x))
r=sp.symbols('r'); print('elim:',sp.factor(sp.expand(2*r**3+3*(-r**2/(r+1))*(r+1)**2)))
