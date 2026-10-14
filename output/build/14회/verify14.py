from sympy import *
import numpy as np
x,a,b,c,k,p,m=symbols('x a b c k p m',real=True); R={}
R[1]=solve((2+a)*(3*a-2)-16,a)
f=Function('f')
R[2]=Rational(12,4)*Rational(1,3)*Rational(1,2)
R[3]=solve(2*sqrt(a+3)-8,a)
F=x**3+6*x-5; R[4]=(limit((F-x**3)/(2*x),x,oo),F.subs(x,0),F.subs(x,2))
R[5]=(6/2, 12/3/ (2*1+6))
R[6]=6*2-(1+2*4)
F=x**4+a*x+2; sv=solve([diff(F,x).subs(x,1)+3],[a]); R[7]=(sv, F.subs(sv).subs(x,1)+3, sv[a]+F.subs(sv).subs(x,1)+3)
R[8]=solve(a*1-3,a)  # g=ax-3, g(1)=0
d=symbols('d'); R[9]=solve((d+2)/(d-1)-4,d)
R[10]=(5*3+5)
R[11]=solve([a+b-6,(2*a+b)-Rational(4,5)*(a+2*b)],[a,b])
# 12
def F12(t): return -2*t*(t-1) if t<2 else (t-4)*(t-6)
def ok12(av):
    h=lambda t:F12(t-1)*F12(t-av); e=1e-7
    return abs(h(3-e)-h(3))<1e-4 and abs(h(3+e)-h(3))<1e-4
R[12]=[av for av in np.round(np.arange(-10,10.001,0.5),2) if ok12(av)]
# 13 f=2x-4
F=2*x-4
R[13]=(limit(F.subs(x,x+1)/((x-1)*(F-4)),x,1), limit(F.subs(x,x+1)/((x-1)*(F-4)),x,4,'+'), F.subs(x,7))
# 14
g=k*(x-2)**2; F=g-k*(x+1)*(x-3); R[14]=(expand(F), simplify(F.subs(x,1)/g.subs(x,0)))
# 15 f={x+1 (x<1), -2x+6 (x>=1)}, k=3
def F15(t): return t+1 if t<1 else -2*t+6
def ex15(av):
    h=lambda t: F15(t)/abs(F15(t)-3); e=1e-7
    try:
        l=h(av-e); r=h(av+e)
    except ZeroDivisionError: return False
    return abs(l-r)<1e-3 and abs(l)<1e5
R[15]=[av for av in np.round(np.arange(-6,6.001,0.25),3) if not ex15(av)]
# 16: f=(x-3)^2 Q + R, Q(3)=R(3); lim (f+x^2)/(f-R)
Rx=(x-3)**2-x**2; q3=Rx.subs(x,3); Q=q3+5*(x-3)  # sample Q with Q(3)=R(3)
F=(x-3)**2*Q+Rx; R[16]=(Rx, q3, limit((F+x**2)/(F-Rx),x,3))
# 18
F=x*(x+5)**2; R[18]=(F.subs(x,-3), F.subs(x,2))
# 서술
def F20(t): return t*t-2*t if (t<3 and t!=2) else (5 if t==2 else t*t-t)
G=p*x**2+6*x
R['S2']=(limit(G/(((x+2)**2-2*(x+2))),x,0), solve(3*G.subs(x,-1)-6*G.subs(x,1),p))
# 단답
F=x**3+a*x**2+2
R['S1']=(expand(x*F+9*x**2-2*x), (F.subs(x,3)).subs(a,6)+(F.subs(x,3)).subs(a,-6), F.subs({x:1,a:6}))
for kk,v in R.items(): print(kk,v)
