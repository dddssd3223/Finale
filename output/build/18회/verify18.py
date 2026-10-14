import sympy as sp, numpy as np, math, itertools
x,h,a,b,c,k=sp.symbols('x h a b c k',real=True)
R={}
R[1]=sp.limit((x+3)*(x**2-x-6)/(x**2+2*x),x,-2)
F=sp.Function('f')
R[2]=2*2*3+4*5
R[3]=sp.limit((x**2-x-6)/(sp.sqrt(x+1)-2),x,3)
R[4]=sum(sp.solve(2+a**2-3*a,a))
f=x**3-2*x**2+3*x; R[5]=sp.limit((f.subs(x,1+h)-f.subs(x,1-3*h))/h,h,0)
f=x**3-3*x**2+2; m=sp.diff(f,x).subs(x,-1); R[6]=f.subs(x,-1)-m*(-1)
s=sp.solve([1+a+b-(b+6),3+a-b],[a,b]); R[7]=s[a]+s[b]
s=sp.solve([1+a+b, sp.limit((x**2+a*x+b)/(x**2-4*x+3),x,1).subs(b,-1-a)-3],[a,b],dict=True); R[8]=[d[b]-d[a] for d in s]
# 9: monic quad f, a>0, lim_{x->1} f(x)f(x-a)/(x-1)^2=-4  -> f(4); brute over f=(x-p)(x-q)
p,q=sp.symbols('p q')
sols=[]
for cand in [ (1,1-a) ]:
    ff=(x-1)*(x-(1-a)); L=sp.limit(ff*ff.subs(x,x-a)/(x-1)**2,x,1); av=[v for v in sp.solve(L+4,a) if v>0]
    sols+= [ff.subs(a,v).subs(x,4) for v in av]
R[9]=sols
# 10
def f10(t): return -2*t*(t-1) if t<2 else (t-3)*(t-6)
def cont10(av):
    e=1e-7; H=lambda X: f10(X-1)*f10(X-av)
    return abs(H(3-e)-H(3))<1e-4 and abs(H(3+e)-H(3))<1e-4
cands=[v/2 for v in range(-20,21)]
R[10]=[v for v in cands if cont10(v)], sum(v for v in cands if cont10(v))
# 11
def f11(X): return 2 if abs(X)>=2 else abs(X)
R[11]=f11(-2.5)+f11(0)+f11(1.5)
# check equation holds
assert all(abs(f11(X)**3-2*f11(X)**2-X*X*f11(X)+2*X*X)<1e-9 for X in np.linspace(-5,5,101))
# 12
kk=sp.symbols('kk'); ff=kk*(x-1)*(x-3)+2
A1=sp.limit((ff-2*x)/(x**2-1),x,1); A2=sp.limit((ff-ff.subs(x,x-2))/(x-3),x,3)
kv=sp.solve(A2-2*A1,kk); R[12]=(kv,A1.subs(kk,kv[0]),ff.subs(kk,kv[0]).subs(x,9))
# 13
av=2; ff=lambda X: abs(X*(X-av))
R[13]=(ff(1e-5)*ff(-1e-5)/1e-10, ff(2-1e-7)*ff(-(2-1e-7))/(-1e-7))
# 14: f=x(x^2+px+4)
P=-3; f14=lambda X: X*(X*X+P*X+4)
R[14]=(5/f14(5), 'disc', P*P-16, 'roots x^2-3x+1', np.roots([1,P,1]))
# 15
av=sp.sqrt(sp.Rational(10,3)); f=-x**3+av**2*x**2+3*x
A=(av,f.subs(x,av)); mA=sp.diff(f,x).subs(x,av); Bx=sp.simplify(av - A[1]/mA)
OA=sp.sqrt(A[0]**2+A[1]**2); AB=sp.sqrt((A[0]-Bx)**2+A[1]**2)
R[15]=(sp.simplify(OA*AB), sp.simplify(2*mA), 'tan at O slope', sp.diff(f,x).subs(x,0))
# 17
f=(x+1)*(x-1)*(x-3)*(x-5); g=sp.expand(f.subs(x,x-(-2))); R[17]=(g, )
# 18: quintic monic; enumerate multiplicity patterns
res=[]
for m0 in range(0,6):
  for m2 in range(0,6-m0):
    rest=5-m0-m2
    # A: lim x^3(x-2)/f at 0 exists -> m0<=3 ; at 2 doesn't exist -> m2>=2
    # B: lim f/(x^2(x-2)^4) at 0 exists -> m0>=2 ; at 2 doesn't exist -> m2<4
    if not (m0<=3 and m0>=2 and m2>=2 and m2<4): continue
    cc=sp.symbols('cc')
    if rest==0: ff=x**m0*(x-2)**m2; 
    elif rest==1: ff=x**m0*(x-2)**m2*(x-cc)
    else: continue
    eq=sp.Eq(ff.subs(x,3),18)
    if rest==0:
        if ff.subs(x,3)==18: res.append((m0,m2,ff.subs(x,4)))
    else:
        for cv in sp.solve(eq,cc):
            if cv in (0,2): continue
            res.append((m0,m2,cv,ff.subs(cc,cv).subs(x,4)))
R[18]=res
# S1
f=2*x**3-3*x**2+b*x+c; s=sp.solve([f.subs(x,1),sp.diff(f,x).subs(x,1)-4],[b,c]); f=f.subs(s)
R['S1']=(sp.limit((f-2*x**3)/x**2,x,sp.oo),f.subs(x,1),f.subs(x,0),sp.diff(f,x).subs(x,2))
for key in R: print(key,R[key])
