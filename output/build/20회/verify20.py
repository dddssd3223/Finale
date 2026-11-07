import sympy as sp, numpy as np
x,a,b,h,t,k=sp.symbols('x a b h t k',real=True)
R={}
R[1]=sp.limit((x**2+3*x+2)/(x**2-1),x,-1)
f=(x**2-1)*(x**2+a*x+4); R[2]=sp.solve(sp.diff(f,x).subs(x,2)-55,a)
R[3]=sp.solve((3+a)**2-(7+a)**2,a)
F=sp.sqrt((t+1)**2+4*t**2); R[4]=(F.subs(t,2),sp.limit((F-5)/(t-2),t,2))
f=x**2+3*x; R[5]=sp.limit((f.subs(x,1+2*h)-f.subs(x,1-h))/h,h,0)
av=sp.solve(4-2*a+2,a)[0]; R[6]=(av, sp.limit((x**2-av*x+2)/(x-2),x,2)+av)
R[7]=3*1-(2+1*(-1))
R[8]=7*2
# 9
m=sp.symbols('m'); 
def lim9(fx,aa):
    e=fx.subs(x,x+1)/((x-1)*(fx+2)); L=sp.limit(e,x,aa,'+'); Lm=sp.limit(e,x,aa,'-'); return L.is_finite and Lm.is_finite and sp.simplify(L-Lm)==0
sols=[]
for mm in range(-6,7):
  for cc in range(-10,11):
    if mm==0: continue
    fx=mm*x+cc
    if lim9(fx,1) and not lim9(fx,4): sols.append((mm,cc,fx.subs(x,-2)))
R[9]=sols
s=sp.solve([3-(-1+a+b),-1-(-1-a+b)],[a,b]); R[10]=s[a]+s[b]
# 11
def f11(X): return -X+2 if X<1 else 2*X
e=1e-7
kk=1.5
cand=[]
for A in np.arange(-3,4,0.25):
  L=f11(A-e)/abs(f11(A-e)-kk); Rr=f11(A+e)/abs(f11(A+e)-kk)
  if abs(L-Rr)>1e-3 or abs(L)>1e5: cand.append(A)
R[11]=(cand,sum(cand), abs(f11(1-e)-kk)-abs(f11(1+e)-kk))
R[12]=( (3+3)*(3+1) )
# 13
def cnt(T):
    if T<0: return 0
    r=0
    for c in [8+T,8-T]:
        D=4+4*c
        if D>1e-12: r+=2
        elif abs(D)<1e-12: r+=1
    return r
g=lambda T:T*(T-9)
R[13]=(cnt(5)+g(5), [cnt(v) for v in (-1,0,4,9,10)])
# 14
f=x**2+a*x+b; G2=f.subs(x,x+1)-f
s=sp.solve([f.subs(x,2)-G2.subs(x,2), sp.diff(f,x).subs(x,2)-sp.diff(G2,x).subs(x,2)],[a,b]); R[14]=f.subs(s).subs(x,4)
# 15
def ok15(K):
    fx=x**2+2*x+9; den=sp.expand(fx**2-K*(x+2)*fx)
    for r in sp.Poly(den,x).real_roots():
        if not sp.limit((x-1)**2/den,x,r).is_finite: return False
    return True
ks=[K for K in range(-15,10) if ok15(K)]; R[15]=(len(ks),ks)
# 17
fx=(x+1)*(x-2); gx=sp.expand(fx*(fx+3))
ok=True
for A in sp.Poly(gx*fx,x).real_roots():
    for e1 in (gx*sp.Abs(fx)/fx, sp.Abs(gx-3*fx)/gx):
        L1=sp.limit(e1,x,A,'+'); L2=sp.limit(e1,x,A,'-')
        if not (L1.is_finite and sp.simplify(L1-L2)==0): ok=False
R[17]=(ok,gx.subs(x,3),sp.Poly(fx+3,x).real_roots())
# 18 brute
vals=[]
for A in range(-12,13):
  for B in range(-15,25):
    P=sp.Poly(x**3+A*x**2+B*x+6,x); fx=P.as_expr(); good=True
    for r in P.real_roots():
        if abs(sp.N(fx.subs(x,3*r+2)))>1e-9: good=False;break
        # multiplicity check
        mr=sp.roots(P).get(r,1) if r.is_rational else 1
        num=sp.Poly(fx.subs(x,3*x+2),x)
        mm=0; q=num
        while q.eval(r)==0: q=sp.Poly(sp.quo(q.as_expr(),x-r),x); mm+=1
        if mm<mr: good=False;break
    if good: vals.append((A,B,fx.subs(x,1)))
R[18]=(max(v[2] for v in vals), len(vals))
# S1
R['S1']=(6,8,6+2*8)
for kk in R: print(kk,R[kk])
