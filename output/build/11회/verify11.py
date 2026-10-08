from sympy import *
import numpy as np
x,a,b,c,p,q=symbols('x a b c p q',real=True); R={}
R[1]=limit((x**3-8)/(x**2-4),x,2)
R[2]=diff((x**3+1)*(2*x-3),x).subs(x,1)
R[3]=limit(x*(sqrt(x**2+4)-x),x,oo)
R[4]=limit((sqrt(x+7)-3)/(x-2),x,2)
R[5]=-1+3
f=x**3+x; R[6]=2*diff(f,x).subs(x,2)
R[7]=2*1*2+2*3
f=x**3-2*x+1; m=diff(f,x).subs(x,-1); R[8]=(-1)-f.subs(x,-1)/m
# 9
f=2*x**3-3*x**2+p*x+q; s=solve([f.subs(x,2),diff(f,x).subs(x,2)-4],[p,q]); f=f.subs(s)
R[9]=(f, limit((f-2*x**3)/x**2,x,oo), limit(f/(x-2),x,2), limit(x*(f.subs(x,1/x)-f.subs(x,0)),x,oo))
# 10 B46v
g=x*(x+2); F=Piecewise((Abs(x+2),x<=0),(2*x+2,True))
h=F*g
R[10]=( [ (limit((h-h.subs(x,r))/(x-r),x,r,'-'), limit((h-h.subs(x,r))/(x-r),x,r,'+')) for r in (-2,0)], g.subs(x,4))
# 11 L58v
f=2*x**3+3*x**2+p*x+q; s=solve([f.subs(x,2),diff(f,x).subs(x,2)-6],[p,q]); f=f.subs(s)
R[11]=(f, limit((x**3*f.subs(x,1/x)-2)/(x**3+x),x,0,'+'), limit(f/(x**2-x-2),x,2), f.subs(x,1))
# 12 C33v
s=solve([1+a+b,9-3*a-b],[a,b]); fe=cancel(((x-3)*(x**2+a*x+b)+(x-1)*(x**2-a*x-b)).subs(s)/((x-1)*(x-3)))
R[12]=(s,fe,fe.subs(x,1)+fe.subs(x,3))
# 13 B47v
cc=symbols('cc'); f=(x-5)**2+cc; S_=sum(3*diff(f,x).subs(x,k) for k in range(1,9)); cv=solve(S_-f.subs(x,0),cc)[0]
R[13]=(cv,f.subs(cc,cv).subs(x,1))
# 14 A31v
r=symbols('r'); g=-3*x**2+18*x+symbols('g0'); h=(x-2)**2*(x-r); fx=g+h
rv=solve(diff(fx,x).subs(x,0)-7,r)[0]; R[14]=(rv, h.subs(r,rv).subs(x,3), diff(g,x).subs(x,2), diff(g,x).subs(x,4))
# 15 L43v
sols=[]
for av,bv in [(4,Rational(1,4))]+[(t,0) for t in [Rational(1,4),-Rational(1,4),0,1,-1,2]]:
    # check (가)
    L=limit((x-2)/(x**2-av),x,2)
    if L!=bv: continue
    ok=False
    for k in range(1,6):
        v=limit(Abs((x**4+av*x**3+bv*x**2)/x**k),x,0)
        if v==Rational(1,4): ok=True
    if ok: sols.append((av,bv))
R[15]=(sols, sum(s_[0]+s_[1] for s_ in sols))
# 16 C27v numeric
def fcount(m_,r_):
    d=abs(4*m_-3)/np.sqrt(m_*m_+1)
    return 2 if d<r_-1e-12 else (1 if abs(d-r_)<1e-12 else 0)
def disc(r_):
    ms=np.linspace(-200,200,800001); d=np.abs(4*ms-3)/np.sqrt(ms*ms+1)
    s=np.sign(d-r_); idx=np.where(s[:-1]!=s[1:])[0]
    return len(idx)
R[16]=( {r_:disc(r_) for r_ in [0.5,1,3,3.99,4,4.5,5,5.0000001,6]}, 3/np.sqrt(1)*0+abs(4-3)/np.sqrt(2))
# 17 C53v numeric check: b=-0.5 → a=2b-2, c=2-2b
def G(y): return abs(y+2)-abs(y-2)-y
for bv in [-1,-0.5,-0.2]:
    av=2*bv-2; cv=2-2*bv
    F_=lambda t: t+av if t<-2 else (bv*t if t<2 else t+cv)
    xs=np.linspace(-20,20,400001); ys=np.array([G(F_(t)) for t in xs])
    R['17_'+str(bv)]=(bool(np.all(np.diff(ys)<0)), av+2*bv+2*cv, ys.min(), ys.max())
# 18 C24v: a=2, m=1 → g(x)= ax-a (x<=2), x-a+1 (x>2) → m+g(a^2+1)
R[18]=1+(5-2+1)
for k_,v in R.items(): print(k_,v)
