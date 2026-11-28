import sympy as sp, numpy as np
from fractions import Fraction as Fr
x,t=sp.symbols('x t',real=True)
A={}
# 1 점 (0,6)에서 y=x^3-2x+4에 그은 접선의 x절편
s=sp.symbols('s',real=True); f=x**3-2*x+4
ts=[r for r in sp.solve(sp.Eq(6,f.subs(x,s)+sp.diff(f,x).subs(x,s)*(0-s)),s) if r.is_real]
A[1]=[sp.solve(sp.Eq(0,f.subs(x,T)+sp.diff(f,x).subs(x,T)*(x-T)),x)[0] for T in ts]
# 2 [1,5], f=x^3-3x^2+a, M+m=50
a=sp.symbols('a'); f=x**3-3*x**2+a
vals=[f.subs(x,v) for v in [1,2,5]]
A[2]=sp.solve(sp.Eq(sp.Max(*[v.subs(a,0) for v in vals])+sp.Min(*[v.subs(a,0) for v in vals])+2*a,50),a)
# 3
A[3]=[r for r in sp.solve(sp.integrate(3*x**2-2*x-6,(x,0,a)),a) if r>0]
# 4
A[4]=sp.integrate(3*x**2-x**3,(x,0,3)); assert sp.solve(x**3-3*x**2,x)==[0,3]
# 5 f=-x^3+ax^2+bx, (−2,0) 증가, (0,∞) 감소, f(-2) 최댓값 → b=0, a<=-3 (수치 확인)
best=-1e9
for av in np.linspace(-10,5,3001):
  for bv in [0.0]:
    fp=lambda X:-3*X**2+2*av*X+bv
    X1=np.linspace(-2,0,401)[1:-1];X2=np.linspace(0,20,401)[1:]
    if (fp(X1)>=-1e-12).all() and (fp(X2)<=1e-12).all(): best=max(best,8+4*av-2*bv)
A[5]=best
# b≠0 불가 확인: f'(0)=b, (−2,0)에서 f'≥0, (0,∞)에서 f'≤0 → 연속성으로 b=0
# 6 x^3+5x^2-9x-8=2x^2+a 세 실근, 곱 양수, 정수 a 최대+최소
ok=[]
for av in range(-60,60):
  r=np.roots([1,3,-9,-8-av]); rr=r[abs(r.imag)<1e-9].real
  if len(rr)==3 and len(set(np.round(rr,7)))==3 and np.prod(rr)>0: ok.append(av)
A[6]=(min(ok)+max(ok),ok[:3],ok[-3:])
# 7
aa,bb=sp.symbols('aa bb'); sol=sp.solve([aa+bb+2,4*aa+2*bb],[aa,bb])
fx=sp.cancel((4*sol[aa]*x**3+2*sol[bb]*x)/(x-1)); A[7]=(fx, sp.minimum(fx,x))
# 8
assert sp.diff(x**3-5*x**2+4*x,x).subs(x,0)==4
A[8]=sp.integrate((-x**2+4*x)-(x**3-5*x**2+4*x),(x,0,4))
# 9 f=x^3-3ax^2-9a^2x+2, y=7 접선 → f(2)
av=sp.symbols('av',positive=True); f=x**3-3*av*x**2-9*av**2*x+2
crit=sp.solve(sp.diff(f,x),x); sols=[]
for c in crit:
  for r in sp.solve(sp.Eq(f.subs(x,c),7),av): sols.append((r,f.subs(av,r).subs(x,2)))
A[9]=sols
# 10 3x^3-9x+a=0, -2<=x<=1 서로 다른 두 실근 정수 a 개수
cnt=[]
for av in range(-40,40):
  r=np.roots([3,0,-9,av]); rr=sorted(set(np.round(r[abs(r.imag)<1e-7].real,6)))
  rr=[q for q in rr if -2-1e-9<=q<=1+1e-9]
  if len(rr)==2: cnt.append(av)
A[10]=(len(cnt),cnt)
# 11
C=sp.symbols('C'); fa=3*x**2-4*x+C
eqs=[sp.Eq(x*fa,2*x**3+a*x**2+2*a+sp.integrate(fa.subs(x,t),(t,1,x)))]
s11=sp.solve(sp.Poly(sp.expand(x*fa-(2*x**3+a*x**2+2*a+sp.integrate(fa.subs(x,t),(t,1,x)))),x).coeffs(),[a,C],dict=True)
# 일반해: f'=6x+2a 이므로 f=3x^2+2ax+C 로 다시
fa=3*x**2+2*a*x+C
co=sp.Poly(sp.expand(x*fa-(2*x**3+a*x**2+2*a+sp.integrate(fa.subs(x,t),(t,1,x)))),x).coeffs()
for so in sp.solve(co+[fa.subs(x,1)-sp.integrate(fa,(x,0,1))],[a,C],dict=True):
  A[11]=(so, so[a]+fa.subs(so).subs(x,3))
# 12
top=-x**3+x; bot=x**3-x**2
assert sorted(sp.solve(top-bot,x))==[-sp.Rational(1,2),0,1]
tot=sp.integrate(top-bot,(x,0,1)); A[12]=sp.solve(sp.Eq(sp.integrate(a*x*(1-x)-bot,(x,0,1)),tot/2),a)
# 13
A[13]=sp.Rational(1)-9+2*sp.Rational(81,8)
xs=np.linspace(1e-6,30,20001)
assert all(xs**2-9*xs+81/4>=-1e-9)
# 14
ms=[]
for m in range(-20,40):
  r=np.roots([2,0,-8,10-m]); pos=sorted(q.real for q in r if abs(q.imag)<1e-9 and q.real>1e-9)
  # 부호 변화(단순근) 개수
  vv=lambda T:2*T**3-8*T+10-m
  ch=sum(1 for p in pos if vv(p-1e-5)*vv(p+1e-5)<0)
  if ch==2: ms.append(m)
A[14]=(sum(ms),ms)
# 15
fx=x**2+x+C; A[15]=(fx.subs(C,sp.solve(sp.integrate(fx,(x,2,3)),C)[0]).subs(x,2))
# 16
v=3*t**2-12*t+9; X=sp.integrate(v,(t,0,x))
d04=sp.integrate(sp.Abs(v),(t,0,4))
A[16]=('x(1)=',X.subs(x,1),'dist0-4=',d04)
# 17 수치: 교점 개수
def g17(tv,av,bv):
  n=0
  r=np.roots([1,0,-3,4-tv]); rr=set(np.round(r[abs(r.imag)<1e-6].real,5)); n+=sum(1 for q in rr if q<=2+1e-9)
  r=np.roots([av,-av*(2+bv),2*av*bv+10-tv]); rr=set(np.round(r[abs(r.imag)<1e-6].real,5)); n+=sum(1 for q in rr if q>2+1e-9)
  return n
best=None
for av in range(1,70):
  for bv in range(1,40):
    m=10-av*(bv-2)**2/4 if bv>2 else None
    crit=sorted(set([6,2,10]+([m] if m is not None else [])))
    grid=np.concatenate([np.linspace(-30,40,1401),np.array(crit)])
    ks=[c for c in crit if g17(c,av,bv)+g17(c-1e-4,av,bv)+g17(c+1e-4,av,bv)==9]
    mids=[(crit[i]+crit[i+1])/2 for i in range(len(crit)-1)]+[crit[0]-1,crit[-1]+1]
    inf=any(g17(q,av,bv)==3 for q in mids)
    if len(ks)==1 and not inf and (best is None or av+bv>best[0]): best=(av+bv,av,bv,ks)
A[17]=best
# 18
def hprime(xv,av):
  fv=-xv**2 if xv<0 else xv**2-2*xv
  gv=av*xv+av if xv<-1 else (0 if xv<2 else av*xv-2*av)
  return gv-fv
def nextrema(av):
  xs=np.linspace(-30,30,120001); hv=np.array([hprime(q,av) for q in xs])
  sg=np.sign(np.where(abs(hv)<1e-12,0,hv)); nz=sg[sg!=0]
  return int(np.sum(nz[1:]!=nz[:-1]))
kk=max(av for av in np.round(np.arange(0.05,8.0,0.05),2) if nextrema(av)==1)
fP=sp.Piecewise((-x**2,x<0),(x**2-2*x,True)); gP=sp.Piecewise((4*x+4,x<-1),(0,x<2),(4*x-8,True))
A[18]=(kk, 4+sp.integrate(gP-fP,(x,0,5)))
# 서답형 1: 우함수, 주기 3, ∫_{-3}^{6} f = 18 → ∫_0^3 f, ∫_0^{21/2} f  (예: f=1+cos(2πx/3) 꼴로 수치 확인)
c=sp.symbols('c'); fe=c*(1+sp.cos(2*sp.pi*x/3))+sp.cos(4*sp.pi*x/3)
cv=sp.solve(sp.integrate(fe,(x,-3,6))-18,c)[0]
A['S1']=(sp.simplify(sp.integrate(fe.subs(c,cv),(x,0,3))), sp.simplify(sp.integrate(fe.subs(c,cv),(x,0,sp.Rational(21,2)))))
# 서답형 2
fS=x**3+4*x**2-11*x+5; sS=sp.diff(fS,x).subs(x,t)-5*t**2+2
loc=sp.solve(sp.diff(fS,x),x); mn=fS.subs(x,1)
A['S2']=(loc, '극솟값',mn, 's(t) 최대', sp.maximum(sS,t), '꼭짓점', sp.solve(sp.diff(sS,t),t), 'f(0)',fS.subs(x,0),'f(2)',fS.subs(x,2))
for k,v in A.items(): print(k,v)
