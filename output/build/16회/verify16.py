from sympy import *
import numpy as np
x,a,b,c,p,q,r,k,t=symbols('x a b c p q r k t',real=True); R={}
R[1]=2-1
R[2]=8-(2+3)
R[3]=solve((1+a)**2-(4+a)**2,a)
f=sqrt((2*t+1)**2+(t+3)**2); R[4]=(f.subs(t,1),limit((f-5)/(t-1),t,1))
F=x**3-2*x; R[5]=3*diff(F,x).subs(x,2)
s6=solve((x**2+a*x-6).subs(x,2),a); R[6]=(s6, limit((x**2+s6[0]*x-6)/(x-2),x,2))
R[7]=12+(-1)+2*4
F=x**2+p*x+q; s8=solve([limit((F-x**2)/x,x,oo)-limit(x*(F.subs(x,1+2/x)-F.subs(x,1)),x,oo),F.subs(x,3)-2],[p,q]); R[8]=(s8,F.subs(s8).subs(x,5))
F=-2*x+6; R[9]=(limit(F.subs(x,x+3)/(x*(F-2)),x,0), limit(F.subs(x,x+3)/(x*(F-2)),x,2,'+'), F.subs(x,-1))
fe=cancel(((x-4)*(x**2+10*x-24)+(x-2)*(x**2-10*x+24))/((x-2)*(x-4))); R[10]=(fe, fe.subs(x,2)+fe.subs(x,4))
def F11(x): return x/2+0.5 if x<1 else -x+4
bad=[]
for av in np.round(np.arange(-8,8.001,0.25),3):
    e=1e-7
    try:
        l=F11(av-e)/abs(F11(av-e)-2); rr=F11(av+e)/abs(F11(av+e)-2)
        if abs(l-rr)>1e-3 or abs(l)>1e5: bad.append(av)
    except ZeroDivisionError: bad.append(av)
R[11]=(bad,sum(bad))
# 12: f={|x+3| (x<=0), 2x+3 (x>0)}, g=x(x+3)
g=x*(x+3)
def h12(v): return (abs(v+3) if v<=0 else 2*v+3)*float(g.subs(x,v))
e=1e-6
R[12]=([( (h12(t0)-h12(t0-e))/e, (h12(t0+e)-h12(t0))/e) for t0 in (-3,0)], g.subs(x,2))
# 13: f=x^2-4x+a, |f|=t roots count discontinuities
av=-2
def cnt(tv):
    rts=set()
    for s in (tv,-tv):
        for rt in np.roots([1,-4,av-s]):
            if abs(rt.imag)<1e-9: rts.add(round(rt.real,7))
    return len(rts)
disc=[tv for tv in np.round(np.arange(-3,10,0.5),2) if cnt(tv)!=cnt(tv+1e-4) or cnt(tv)!=cnt(tv-1e-4)]
R[13]=(disc, av**2-4*av+av)
# 14
F=x**3+p*x**2+q*x+r
eqs=[diff(F,x).subs(x,0)+1-(-diff(F,x).subs(x,0)), (-diff(F,x)+2*x).subs(x,1)-(diff(F,x)+3).subs(x,1), F.subs(x,1)-4]
s14=solve(eqs,[p,q,r]); Fv=F.subs(s14); av=2*Fv.subs(x,0)
bv=solve((-Fv+x**2+av).subs(x,1)-(Fv+3*x+b).subs(x,1),b)[0]
R[14]=(s14,av,bv,(Fv+x).subs(x,-1)+(Fv+3*x+bv).subs(x,2))
# 15
F=x**3+p*x**2+q*x+r; Dk=expand((F.subs(x,k+2)-F.subs(x,k))/2)
s15=solve([Dk.subs(k,0)-(4*0-6),Dk.subs(k,1)-(4*1-6)],[p,q]); Dv=Dk.subs(s15)
okb=all((Dv.subs(k,kk)>=4*kk-6) and (Dv.subs(k,kk)<=4*kk**2-6) for kk in range(-30,30))
R[15]=(s15,expand(Dv),okb,diff(F.subs(s15),x).subs(x,4))
# 16 boki numeric
def f16(v): return v+2 if v<=0 else (v if v<=1 else 3*v-2)
def chk(P,sq=False):
    hh=lambda v:P(v)*(f16(v)**2 if sq else f16(v)); e=1e-7; out=[]
    for t0 in (0,1):
        cont=abs(hh(t0-e)-hh(t0))<1e-5 and abs(hh(t0+e)-hh(t0))<1e-5
        d=abs((hh(t0)-hh(t0-e))/e-(hh(t0+e)-hh(t0))/e)<1e-4
        out.append((cont,d))
    return out
R[16]=( chk(lambda v:v), chk(lambda v:v*v*(v-1)), chk(lambda v:v*(v-1)), chk(lambda v:v*v*(v-1),True), chk(lambda v:v*(v-1),True), chk(lambda v:v*v,True))
# 17
h=(x-1)*(x-3)+3; G=(x-1)*(x-3)*h; R[17]=(expand(h), discriminant(h,x), G.subs(x,-1))
# 18: g={(x+2)f(x) x<0, (x+a)f(x-b) x>=0}, f=(x+2)^2, b=6
f=(x+2)**2; bv=6; av=solve(2*f.subs(x,0)-a*f.subs(x,-bv),a)[0]
R[18]=(av, (x+av).subs(x,2)*f.subs(x,2-bv))
# 단답
R['S1']=(solve(a-(2*a+5),a), solve(a+4-(a**2-2*a),a))
# 서술
av=symbols('av')
g=(x-1)*(x-3)*(x-av)
h1=limit(g/(x**2-5*x+4),x,1); ha=limit(g/(-x**2+av*x),x,av)
sv=solve(h1-ha,av); R['S2']=(h1,ha,sv,[ (h1+ (g/(x**2-5*x+4)).subs(x,2)).subs(av,s_) for s_ in sv])
for kk,v in R.items(): print(kk,v)
