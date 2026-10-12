import sympy as sp, numpy as np
x,a,b,c,h=sp.symbols('x a b c h',real=True)
print(1,sp.limit((x+2)*(x**2+2*x-3)/(x**2-x),x,1))
print(2,2*1*3+2*5)
print(3,sp.limit((x**2+x-6)/(sp.sqrt(x+7)-3),x,2))
print(4,sp.solve(4+a**2-(6*a-2),a),sum(sp.solve(4+a**2-(6*a-2),a)))
f=x**3-4*x+1; m=sp.diff(f,x).subs(x,-1); print(6,f.subs(x,-1)+m)  # y-int = f(-1)-m*(-1)
print(7,sp.solve([1+a+b-(b+8),3+a-b],[a,b]))
# 10
def f10(t): return t*(t-3) if t<2 else (t-3)*(t-4)
H=lambda X,av: f10(X-1)*f10(X-av)
ok=[av/2 for av in range(-30,31) if abs(H(3-1e-8,av/2)-H(3,av/2))<1e-5 and abs(H(3+1e-8,av/2)-H(3,av/2))<1e-5]
print(10,ok,sum(ok))
# check non-grid a: solve analytically -> f(3-a)=0 or a=1
# 12
k=sp.symbols('k'); ff=k*(x-2)*(x-4)+6
A1=sp.limit((ff-3*x)/(x**2-4),x,2); A2=sp.limit((ff-ff.subs(x,x-2))/(x-4),x,4)
kv=sp.solve(A2+2*A1,k); print(12,kv,A1.subs(k,kv[0]),ff.subs(k,kv[0]).subs(x,8))
# 14 f=x(x^2+px+7), g(0)=1/7, g=1/4 one root in (0,1), f(1) natural
for P in np.arange(-5.29,5.3,0.01):
    pass
P=-5; print(14,'disc',P*P-28,'roots',np.roots([1,P,3]),'f(1)',8+P,'g(6)',sp.Rational(6,6*(36+6*P+7)))
# 15
av=sp.sqrt(sp.Rational(17,4)); f=-x**3+av*x**2+4*x; Ay=f.subs(x,av); m=sp.diff(f,x).subs(x,av); Bx=av-Ay/m
print(15,sp.simplify((Ay/av)*m),sp.simplify(sp.sqrt(av**2+Ay**2)*sp.sqrt((av-Bx)**2+Ay**2)), av>2)
# 18: A={a| lim x^3(x+1)/f exists}, B={b| lim f/(x^2(x+1)^4) DNE}, 0 in A-B, -1 in B-A, f(1)=12
res=[]
cc=sp.symbols('cc')
for m0 in (2,3):
  for m1 in (2,3):
    r=5-m0-m1
    if r<0: continue
    ff=x**m0*(x+1)**m1*((x-cc) if r==1 else 1)
    if r==0:
        if ff.subs(x,1)==12: res.append((m0,m1,ff.subs(x,2)))
    else:
        for cv in sp.solve(ff.subs(x,1)-12,cc):
            if cv not in (0,-1): res.append((m0,m1,cv,ff.subs(cc,cv).subs(x,2)))
print(18,res)
# S1
f=3*x**3+2*x**2+b*x+c; s=sp.solve([f.subs(x,-1),sp.diff(f,x).subs(x,-1)-5],[b,c]); f=f.subs(s)
print('S1',f,sp.limit((f-3*x**3)/x**2,x,sp.oo),f.subs(x,0),sp.limit((f.subs(x,1+2*h)-f.subs(x,1))/h,h,0))
