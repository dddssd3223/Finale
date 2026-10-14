from sympy import *
import numpy as np
x,a,b,c,t,h=symbols('x a b c t h',real=True); R={}
F=Abs(x-1)*Abs(x+1)*(x+a)/((x-1)*(x+1))
R[1]=solve(limit(F.subs(a,a),x,1,'+')+limit(F,x,-1,'-')-8,a)
F=a*x**2+3*x; R[2]=(solve(F.subs(x,-1)+1,a), F.subs(a,2).subs(x,1))
av=8; R[3]=(limit((sqrt(x**2+av)-3)/((x-1)*(x**2+1)),x,1), av/limit((sqrt(x**2+av)-3)/((x-1)*(x**2+1)),x,1))
R[4]=Rational(1,1+4*6)
fp=2*x**2-x+3; R[5]=4*fp.subs(x,2)
R[6]=solve(2*3*a/3-4,a)
F=x**3-x; m=diff(F,x).subs(x,-1); R[7]=solve(F-(m*(x+1)),x)
R[8]=(solve(Abs(-2+a)-2,a), solve(2*b+1-2,b), solve(2*b+1+2,b))
sv=solve([(2-a)*(2-b)-(2*a-b), 4-a-b-a],[a,b],dict=True); R[9]=(sv,[d[a]+d[b] for d in sv])
R[10]=((9-1)/(3+1), expand((x**2-4*x+7)-(-x**2+4*x-1)))
f=1/(x-3); bv=Rational(-3,4); g=sqrt(x+bv)-Rational(3,2)
R[11]=(limit(f*g,x,1), limit(f*g,x,3), g.subs(x,3))
fq=x**2-3*x+a; sv=solve(fq.subs(x,2)**2-fq.subs(x,-1)**2,a); R[12]=(sv, [fq.subs(a,s_).subs(x,1)+fq.subs(a,s_).subs(x,0) for s_ in sv])
# 13 numeric
def f13(x): return -2 if abs(x)>=1 else 1
def g13(x): return 1 if abs(x)>=1 else -2*x
e=1e-7
R[13]=( (f13(1-e)*g13(1-e), f13(1+e)*g13(1+e)), (f13(-1-e)*g13(-1-e), f13(-1+e)*g13(-1+e)), (f13(-1-e)*g13(-1-e+1), f13(-1+e)*g13(-1+e+1), f13(-1)*g13(0)) )
OA=sqrt(a**2+(2*a+1)**2); R[14]=(OA.subs(a,1), sqrt(1+9), simplify(diff(OA,a).subs(a,1)))
R[15]=(3*2**2-2*2+4)
# 16 count
def f16(x):
    if x==-1 or x==3: return 1.0
    return 1/(x+1)
def okint(a_):
    lo,hi=a_-1,a_+1
    if lo<=-1<=hi: return False
    return True
R[16]=sum(1 for a_ in range(-9,10) if okint(a_))
# 17
P=(t,t**2); Q=(2/t,2); PQ=sqrt((Q[0]-P[0])**2+(Q[1]-P[1])**2)
R[17]=simplify(limit(PQ/(sqrt(2)-t),t,sqrt(2),'-'))
# check P is closest point: tangent slope 2t matches line slope 2t
# 서술
fa=Abs(x*(x-a)); 
R['S2']=(solve(limit((Abs(x*(x-a))*Abs(-x*(-x-a))/x**2).subs(a,2),x,0)-4,a) , limit(Abs(x*(x-2))*Abs(x*(x+2))/(x-2),x,2,'+'), limit(Abs(x*(x-2))*Abs(x*(x+2))/(x-2),x,2,'-'))
for k_,v in R.items(): print(k_,v)
