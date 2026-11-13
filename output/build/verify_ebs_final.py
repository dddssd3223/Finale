from sympy import *
x,t,p,q,r,c,a,b,k=symbols('x t p q r c a b k')
R={}
# 1회14
f=x**2*(x-Rational(9,2)); fp=diff(f,x)
assert fp.subs(x,1)==-6 and sorted(solve(fp,x))==[0,3]
kk=limit(f/fp**2,x,0); R['1-14']=kk+(f/fp**2).subs(x,5)
# brute: generic monic cubic with f'(1)=-6, require continuity at one f' root
# 1회20
f=x*(x-6)**2; fp=diff(f,x); R['1-20']=sum(m for m in range(-20,20) if fp.subs(x,m)*fp.subs(x,m+2)<0)
# 2회
f=2*x**2-3*x+4; R['2-02']=solve(diff(f,x)-5,x)
x1=t**3-2*t**2+4*t; x2=t**2+t; tt=solve(diff(x1-x2,t),t); R['2-11']=[abs((x1-x2).subs(t,s)) for s in tt]
for cc in [1,Rational(-3,2)]:
    f=(x-1)**2*(x-cc); g=expand(f*diff(f,x))
    assert g.subs(x,0)==-3 and g.subs(x,1)==0 and diff(g,x).subs(x,1)==0
    R['2-21 c=%s'%cc]=(g.subs(x,2), 'monotone' if len(real_roots(diff(g,x)))==0 or all(diff(g,x).subs(x,z)>=0 for z in [Rational(i,10) for i in range(-50,50)]) else 'not monotone')
# 3회
R['3-02']=diff(x**3-x+1,x).subs(x,2)
R['3-07']=[(diff(t**3-3*t**2,t,2)+diff(-t**2+15*t,t,2)).subs(t,s) for s in solve(diff(t**3-3*t**2+t**2-15*t,t),t) if s>0]
g=x**2+k*x-2; al,be=symbols('al be'); 
fa=expand(x**3-2*x+2*k); rem=rem_=Poly(fa,x).rem(Poly(g,x)); R['3-15 f mod g']=rem_.as_expr()
# 4회
R['4-02']=diff(2*x**3-x**2+9,x).subs(x,2); R['4-03']=solve(-2*a+1-(a**2-6*a+5),a)
f=Rational(1,3)*(x-1)**2+2; R['4-09']=(f.subs(x,4), limit((f-f.subs(x,-1))/(x-3),x,3), limit(f.subs(x,x+2)/f.subs(x,x-4),x,2))
X=t**3-12*t**2+36*t; R['4-13']=(X.subs(t,1), solve(diff(X,t),t), abs(X.subs(t,6)-X.subs(t,2)))
R['4-16']=diff((x**3-x)*(x**2+2*x),x).subs(x,1)
f=x*(x-1)**2; assert diff(f,x).subs(x,0)+diff(f,x).subs(x,1)==1; R['4-22']=2*f.subs(x,4)
# 5회
R['5-02']=diff(5*x**2-6*x,x).subs(x,1)
f=x**2-2*x-2; R['5-08']=(expand((x-1)*f), f.subs(x,-1), f.subs(x,3), f.subs(x,1))
y=a*x**4+x**2-a*x-1; sa=diff(y,x).subs(x,1); sb=diff(y,x).subs(x,0)
for av in solve(sa*sb+1,a):
    X0=solve((sa*(x-1)-(sb*x-1)).subs(a,av),x)[0]; Y0=(sb*x-1).subs({a:av,x:X0}); R['5-11 a=%s'%av]=(X0,Y0)
f=x**4-3*x**2+4*x; R['5-20']=(limit((f-x**4)/(1-x**2),x,oo), limit(f/x,x,0), f.subs(x,2))
# 6회
R['6-02']=limit((x+1)/(sqrt(x+5)-2),x,-1); R['6-04']=solve(10-(1+a+2),a); R['6-05']=diff((3*x-1)*(x**2+x+2),x).subs(x,1)
sols=[]
for rr in range(-10,11):
    F=expand((x-3)*(x-4)*(x-rr)); A,B,C=[F.coeff(x,i) for i in (2,1,0)]
    G=C*x**3+B*x**2+A*x+1
    ok=True
    for root in set([3,4,rr]):
        if root==4: continue
        L=limit(G/F,x,root)
        if not L.is_finite: ok=False
    if not ok: continue
    if limit(G/F,x,4).is_finite: continue
    sols.append((rr,limit(G/F,x,3)))
# also non-integer third root: solve generally
F=(x-3)*(x-4)*(x-r); A,B,C=[expand(F).coeff(x,i) for i in (2,1,0)]
G=C*x**3+B*x**2+A*x+1
R['6-21 g(3)=0 roots r']=solve(G.subs(x,3),r)
R['6-21 int sols']=sols
# 7회
R['7-02']=diff(x**3+2*x-3,x).subs(x,2)
R['7-05']=solve(a-diff(x**2+2*a-3,x).subs(x,2),a)
f=x**3-8*x; R['7-08']=(limit(f/x**4,x,oo),limit((f-x*f.subs(x,2))/x**2,x,0),f.subs(x,3))
f=x**3-2*x**2+8; m=symbols('m')
def nroots(mv): return len(set(real_roots(Poly(f-mv*x,x))))
R['7-13']=(solve(diff(f,t*0+x)*x-f,x), [nroots(v) for v in (3,4,5)], solve(3*t**2-4*t-4,t))
f=(x-1)**3+1; R['7-15']=(diff(f,x).subs(x,0), solve([f-x, diff(f,x)-3],x), f.subs(x,2))
for kk,v in R.items(): print(kk,':',v)
