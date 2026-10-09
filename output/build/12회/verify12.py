from sympy import *
import numpy as np, itertools
x,a,b,c,p,q,r,s,al,be,ga=symbols('x a b c p q r s al be ga',real=True); R={}
# 1
R[1]=solve(Eq(4+2*a,6*a-2),a)
R[2]=limit(sqrt(x**2+6*x)-x,x,oo)
R[3]=solve(diff((x**2+2)*(x**2+a*x+1),x).subs(x,1)-20,a)
R[4]=limit((x**2-9)/(sqrt(x+1)-2),x,3)
f=Function('f'); R[5]=2*2*3+(4-1)*(-1)
F=x**3+2*x**2; R[6]=limit((F.subs(x,1+3*x)-F.subs(x,1-x))/x,x,0)
F=x**3-3*x+2; m=diff(F,x).subs(x,2); R[7]=(F.subs(x,2)-m*2)
s8=solve([1+a+b-4,2+a-4],[a,b]); R[8]=(s8,s8[a]+s8[b])
cv=solve(limit(((x-1)*(x+c))/(sqrt(x+3)-2),x,1)-12,c)[0]; N=expand((x-1)*(x+cv)); av,bv=N.coeff(x,1),N.coeff(x,0); R[9]=(N,av,bv,av**2+bv**2,limit((x**2+av*x+bv)/(sqrt(x+3)-2),x,1))
# 10
F=x**2+p*x+q
L1=limit((F-x**2)/x,x,oo); L2=limit(x*(F.subs(x,2+3/x)-F.subs(x,2)),x,oo)
sv=solve([L1-L2,F.subs(x,1)-2],[p,q]); R[10]=(sv,F.subs(sv).subs(x,4))
# 11
Fl=p*x+q; G=x**2+2*x+5-Fl
sv=solve([G.subs(x,1)-Fl.subs(x,1),diff(G,x).subs(x,1)-diff(Fl,x)],[p,q]); Fv=Fl.subs(sv)
R[11]=(Fv, limit((Fv-G.subs(sv))/(x-1),x,1), Fv.subs(x,3)*diff(Fv,x))
# 12
R[12]=solve((a+1)*(a+2)-(a+1)*(a**2-4),a)
# 13
F=x**3+p*x**2+q*x+r
eqs=[F.subs(x,0)-(-F.subs(x,0)+a), diff(F,x).subs(x,0)+4-(-diff(F,x).subs(x,0)),
     (-F+a).subs(x,2)-(F+x**2+b).subs(x,2), diff(-F,x).subs(x,2)-diff(F+x**2,x).subs(x,2), F.subs(x,2)+5]
sv=solve(eqs,[p,q,r,a,b],dict=True)
R[13]=[(d,(-F+a).subs(d).subs(x,1)+(F+x**2+b).subs(d).subs(x,3)) for d in sv]
# 14
e0,e1,e2,e3,e4=symbols('e0:5'); Fq=x**4+e3*x**3+e2*x**2+e1*x+e0
qq=al*x**2+be*x+ga; Fq=(x**2-1)*qq
# g=q off ±1; g(±1)=2(±1)+a must equal q(±1) for continuity/differentiability
sv=solve([qq.subs(x,1)-(2+a),qq.subs(x,-1)-(-2+a),qq.subs(x,1)-4, diff(qq,x).subs(x,1)/(2*4)-Rational(1,2)],[al,be,ga,a],dict=True)
R[14]=[(d,limit((qq.subs(d)-4)/Fq.subs(d),x,1),Fq.subs(d).subs(x,d[a])) for d in sv]
# 15 check with p=x-2 and p=x^2(x-2)
fx=Piecewise((-x+1,x<=0),(x-1,x<=2),(3*x-5,True))
def ld(h,x0,side): return limit((h-h.subs(x,x0))/(x-x0),x,x0,side)
for P in [x-2,x**2*(x-2),x*(x-2)]:
    h=P*fx; h2=P*fx**2
    R['15_'+str(P)]=([(ld(h,t,'-'),ld(h,t,'+')) for t in (0,2)],[ (limit(h2,x,t,'-'),limit(h2,x,t,'+'),h2.subs(x,t)) for t in (0,2)],[(ld(h2,t,'-'),ld(h2,t,'+')) for t in (0,2)])
# 16: f=x(x^2+px+4); brute p over grid + boundary candidates
sols=[]
for pv in [Rational(n,100) for n in range(-400,401)]+[-2*sqrt(2)]:
    if pv**2>=16: continue
    qx=x**2+pv*x+2
    rts=[rr for rr in solve(qx,x) if rr.is_real and 0<rr<2]
    if len(set(rts))==1 and (5+pv).is_integer and 5+pv>0: sols.append(pv)
R[16]=(sols,[1/(16+4*pv+4) for pv in sols])
for k_,v in R.items(): print(k_,v)
# ---- 단답형 1 (D19 변형)
h=x**3-8*x**2+16*x
ts=solve(Eq(h.subs(x,s),diff(h,x).subs(x,s)*(s+2)),s); print('S1 h tangents',ts,[diff(h,x).subs(x,t_) for t_ in ts])
cc=symbols('cc'); Fc=cc*(x-4)**2*(x-14)
ts2=solve(Eq(Fc.subs(x,s),diff(Fc,x).subs(x,s)*(s+2)),s); print('S1 f tangents',ts2)
cv=solve(diff(Fc,x).subs(x,10)-3,cc)[0]; Fv=Fc.subs(cc,cv)
print('c',cv,'f(10)',Fv.subs(x,10),'f(13)',Fv.subs(x,13), 'diff at 4',diff(Fv,x).subs(x,4), Fv.subs(x,14))
# ---- 서술형 1 (C30 변형): f monic quadratic, roots 1 and s
for sv in [Rational(n,2) for n in range(-16,4)]+[1]:
    Fq=(x-1)*(x-sv)
    zg=set(solve(Fq.subs(x,x**2+1),x)); zg={z for z in zg if z.is_real}
    zh={z for z in solve(Fq.subs(x,x**2),x) if z.is_real}
    if len(zg)==1 and len(zh)==2:
        bb=min(zh); L=limit(Fq.subs(x,x-3)/Fq.subs(x,x**2),x,bb)
        print('S2 s=',sv,'a',zg,'b,c',sorted(zh),'lim',L, 'f(3)*lim' , Fq.subs(x,3)*L if L.is_finite else None)
