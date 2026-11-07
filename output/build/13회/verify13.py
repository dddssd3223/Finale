from sympy import *
import numpy as np, itertools
x,a,b,c,p,q,k,s=symbols('x a b c p q k s',real=True); R={}
R[1]=solve(2+a**2-3*a,a)
R[2]=limit((x**3+1)/(x**2-x-2),x,-1)
F=Function('F'); R[3]=diff(x**3+4*x**2+7*x,x).subs(x,0)
R[4]=solve([4+2*b-10,1+a-(1+b)],[a,b])
R[5]=-2*4
R[6]=(6, 2*3, 6+6)
f1=2; fp=(5-f1)/2; R[7]=(f1,fp, f1-fp*1)
R[8]=solve([2+3+1-(a+b),4+3-a],[a,b])
F=x**3+a*x**2+x+b; sv=solve([F.subs(x,1)-12, 2*diff(F,x).subs(x,1)-12],[a,b]); R[9]=(sv,sv[a]+sv[b], limit(x*(F.subs(sv).subs(x,1+2/x)-12),x,oo))
# 10: example f with lim (f-2)/x=3, g(f-2)=x^2(f+4): f=3x+2 -> g=x^2(3x+6)/(3x)=x(x+2)
f=3*x+2; g=x*(x+2); R[10]=(simplify(g*(f-2)-x**2*(f+4)), limit((4*x*g+f*g)/(x+g),x,0))
# 11
g=c*(x+1); f=3*x**3-x**2*g-3*x; cv=solve(limit(g/(f+g),x,-1)-Rational(1,3),c); R[11]=(cv, g.subs(c,cv[0]).subs(x,2))
# 12 numeric check of all a
def F12(t): return t+2 if t<=0 else 2*t-4
def cont(av):
    e=1e-7
    h=lambda t: F12(t)*F12(t-av)
    for t0 in set([0,av]):
        if abs(h(t0-e)-h(t0))>1e-4 or abs(h(t0+e)-h(t0))>1e-4: return False
    return True
R[12]=[av for av in np.round(np.arange(-10,10.0001,0.25),2) if cont(av)]
# 13
f=x*(x-2)*(p*x+q); sv=solve([diff(f,x).subs(x,2)-4, limit(f.subs(x,x+1)/f.subs(x,x-1),x,1)+2],[p,q],dict=True)
R[13]=[(d,f.subs(d).subs(x,4)) for d in sv]
# 14 example
f=-x**2/4+3*x; g=3+x**2+4*x
R[14]=(limit((f+g-3)/x,x,0), expand((f+x)*(g-3)-x**2*(f+16)), limit(f*g*(g-3)/x**2,x,0))
# 15
f=(x-2)*(x-3)*(x-4); G=lambda t:(f.subs(x,t+2)*(f.subs(x,t)+1)/f.subs(x,t))
R[15]=(limit(f.subs(x,x+2)*(f+1)/f,x,2), G(5))
# 17
fa=x*(x-2)**2*(x-4); gg=expand(fa.subs(x,x+1)); kk=sqrt(2)
R[17]=(expand(gg-gg.subs(x,1+kk)), factor(gg-gg.subs(x,1+kk)), -1+10*kk**2)
for kk_,v in R.items(): print(kk_,v)
