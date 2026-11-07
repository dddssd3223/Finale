from sympy import *
import numpy as np
x,a,b,p,q,k,c=symbols('x a b p q k c',real=True); R={}
R[1]=limit((x**2-9)/(x**2-2*x-3),x,3)
R[2]=diff((x**2+2)*(3*x-1),x).subs(x,1)
R[3]=limit(sqrt(x**2+5*x)-x,x,oo)
s=solve([2*a-4,a+1-(4+b)],[a,b]); R[4]=s[a]*s[b]
R[5]=2+3
R[6]=Rational(6,2)/2
f=x**3-4*x; R[7]=f.subs(x,2)-2*diff(f,x).subs(x,2)
R[8]=min(n for n in range(1,30) if 36-4*n<0)
av=solve(3*a*(2+2*a)-2*(3*a+2*a),a); av=[v for v in av if v>0][0]
F=lambda z: -z+3*av if z<=0 else z+2
R[9]=(av, F(1)*(F(-1)+2*av))
f=2*x**3+p*x**2+q*x-1; s=solve([f.subs(x,1)-4,f.subs(x,-1)+4],[p,q]); f=f.subs(s)
cc=symbols('cc'); g=x**3+0*x**2+cc*x+3; cv=solve(g.subs(x,1)-6,cc)[0]; g=g.subs(cc,cv)
R[10]=(f, limit(x**3*f.subs(x,1/x),x,0,'+'), limit((f-2*g)/x**2,x,oo), g.subs(x,2))
f=(x-2)*(x**2+p*x-1-2*p); R[11]=(limit(f/(x-2),x,2), f.subs(x,0), expand(f.subs(x,3)))
A=symbols('A'); f=A*x**2*(x-2); gg=Abs(x-2)*f; Av=solve(limit((Abs(x-2)*f)/x**2,x,0)-6,A)[0]
R[12]=(Av, (Abs(x-2)*f).subs({A:Av,x:4}))
f=(x**2-a**2)*(x-3*a)+2; av=solve(diff(f,x).subs(x,1)+4,a); R[13]=[(v,f.subs(a,v).subs(x,0),f.subs(a,v).subs(x,4)) for v in av]
# 14
A=symbols('A',positive=True)
c1=4*A**2-12*(4*A+4); c2=4*A**2-12*(4-4*A)
R[14]=(solve(c2,A), [N(v) for v in solve(c2,A)])
# 15
av=4; kk=symbols('kk'); f=x/2+kk*x*(x-av)*(x-2*av); sl=diff(f,x).subs(x,av); C=av-(av/2)/sl
kv=solve(C-5,kk); f=f.subs(kk,kv[0])
R[15]=(kv, f.subs(x,12), sqrt(5**2), sqrt((8-5)**2+4**2))
# 16 numeric N(k) for |x^2-4| and line kx+t
def ncount(kv,t):
    xs=set()
    for s in (1,-1):
        r=np.roots([1,-kv,-4-t]) if s==1 else np.roots([-1,-kv,4-t])
        for z in r:
            if abs(z.imag)<1e-9:
                z=z.real
                if (s==1 and abs(z)>=2-1e-12) or (s==-1 and abs(z)<=2+1e-12): xs.add(round(z,6))
    return len(xs)
def Nk(kv):
    ts=np.linspace(-60,60,240001); vals=[ncount(kv,t) for t in ts]
    cnt=0; disc=[]
    for i in range(1,len(ts)-1):
        if vals[i]!=vals[i-1] or vals[i]!=vals[i+1]:
            disc.append(round(ts[i],2))
    # cluster
    cl=[]
    for d in disc:
        if not cl or abs(d-cl[-1])>0.01: cl.append(d)
    return cl
tot=0; det={}
for kv in range(1,9):
    cl=Nk(kv); det[kv]=cl; tot+=len(cl)
R[16]=(tot,det)
# 17 C32v checked numerically elsewhere: a=-4,b=4,c=3 -> f(7)
f=(-4*x+4)/(x-3); R[17]=(f.subs(x,4), f.subs(x,7))
# 18 D20v
f=(x-2)**2*(x+Rational(8,3)); R[18]=(f.subs(x,-2)-f.subs(x,0), -f.subs(x,-1))
# S1 C06v
cv=Rational(3,2); gx=x/3+Rational(1,3); fg=cv*(x-2)*(x+1)
R['S1']=(gx.subs(x,2), gx.subs(x,-1), -fg.subs(x,0), 2*gx.subs(x,5)+fg.subs(x,5))
# S2 C8v
P=symbols('P',positive=True); f=P*(x-1)*(x-4)+2*x+1
R['S2']=(f.subs(x,1),f.subs(x,4), solve(9*P**2-24*P+4,P), f.subs(x,0), [n for n in range(1,20) if Rational(n-1,4)<(4+2*sqrt(3))/3][-1])
for k_,v in R.items(): print(k_,v)
