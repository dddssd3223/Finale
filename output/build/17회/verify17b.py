import sympy as sp, numpy as np
x,h,a,b,c,k,t,p,q=sp.symbols('x h a b c k t p q',real=True)
R={}
# 1 L5': f={2x+a (x<-1), x^2-x+a (x>=-1)}, left*right=12, a>0
s=sp.solve(sp.Eq((-2+a)*(2+a),12),a); R[1]=[v for v in s if v>0]
# 2 B50': f=(x^2+3)(x^2+ax-2), f'(1)=12
f=(x**2+3)*(x**2+a*x-2); R[2]=sp.solve(sp.diff(f,x).subs(x,1)-12,a)
# 3 C1': |f| cont, f={x+a (x<-2), x (-2<=x<3), bx-1 (x>=3)}, a,b>0
sa=[v for v in sp.solve(sp.Abs(-2+a)-2,a) if v>0]; sb=[v for v in sp.solve(sp.Abs(3*b-1)-3,b) if v>0]; R[3]=(sa,sb,[i+j for i in sa for j in sb])
# 4 A20': (f(x+h)-f(x-h))/h -> 2f' = 12x^2-6x+4 ; g=lim (f(x+3h)-f(x-2h))/(2h) = 5/2 f'
fp=(12*x**2-6*x+4)/2; g=sp.Rational(5,2)*fp; R[4]=g.subs(x,-1)+g.subs(x,1)
# check with a concrete f
F=sp.integrate(fp,x); chk=sp.limit((F.subs(x,x+3*h)-F.subs(x,x-2*h))/(2*h),h,0); assert sp.simplify(chk-g)==0
# 5 lim x(sqrt(x^2+4)-x)
R[5]=sp.limit(x*(sp.sqrt(x**2+4)-x),x,sp.oo)
# 6 f={x^2+ax+b (x<2), 3x-1}: diff at 2 -> a-b
s=sp.solve([4+2*a+b-5,4+a-3],[a,b]); R[6]=s[a]-s[b]
# 7 A28': lim_{inf} x f'/f =4, lim_0 f/(x f') = 1/3, monic, f(1)=f'(1) -> f(2)
f=x**4+b*x**3; bb=sp.solve(f.subs(x,1)-sp.diff(f,x).subs(x,1),b)[0]; f=f.subs(b,bb)
R[7]=(bb,f.subs(x,2),sp.limit(x*sp.diff(f,x)/f,x,sp.oo),sp.limit(f/(x*sp.diff(f,x)),x,0))
# 8 L45': lim_{x->0+} x^2 f(1/x)=3, lim (f-2g)/x=4, f(0)=1,f(1)=6,g(0)=2 -> g(4)
f=3*x**2+p*x+1; pp=sp.solve(f.subs(x,1)-6,p)[0]; f=f.subs(p,pp)
G=sp.Rational(3,2)*x**2+q*x+2; qq=sp.solve(sp.limit((f-2*G-0)/x,x,sp.oo)-4,q)
R[8]=(f,qq,[G.subs(q,v).subs(x,4) for v in qq], sp.limit(x**2*f.subs(x,1/x),x,0,'+'))
# 9 A25': lim (f+g)/x=2, lim (f+2)/(x g)=3 -> h'(0)
f0,g0,f1,g1=sp.symbols('f0 g0 f1 g1'); s=sp.solve([f0+g0,f1+g1-2,f0+2,f1/g0-3],[f0,g0,f1,g1],dict=True)[0]
R[9]=s[f1]*s[g0]+s[f0]*s[g1]
# 10 C14': f={-x+5 (x<2), 3x+a}, g=x^2-5x+a ; fg continuous -> sum of a
R[10]=sp.solve(sp.Eq(3*(4-10+a),(6+a)*(4-10+a)),a)
# 11 A14': f={x^2+a (x<1), -x^2+bx+c}, cont, |f| nondiff only at 4, a>0
s=sp.solve([1+a-(-1+b+c), 2-(-2+b), -16+4*b+c],[a,b,c]); R[11]=(s, s[a]+s[b]+s[c])
# 12 B47': axis 3, sum_{k=1}^{8} 2f'(k-2) = -f(0)
f=(x-3)**2+c; ssum=sum(2*sp.diff(f,x).subs(x,kk-2) for kk in range(1,9)); cc=sp.solve(ssum+f.subs(x,0),c)[0]; R[12]=(cc,f.subs(c,cc).subs(x,-1))
# 13 C54': g={f(x+1)(f+2)/f, 5}, lim_{x->1} g = g(1)-9 -> f=x(x-1)(x-2), g(3)
f=(x-1)*(x-2)*(x-p); L=sp.limit((f.subs(x,x+1)/f).subs(p,0),x,1)
pp=sp.solve(sp.Eq(2*(-(2-p)/(1-p)),5-9),p); f=f.subs(p,pp[0]); gx=f.subs(x,x+1)*(f+2)/f
R[13]=(pp,sp.limit(gx,x,1),gx.subs(x,3))
# 15 L67': f=x^2-6x+12, lim x^2/(f^2-k(x-2)f) exists for all a
def ok15(kk):
    den=sp.expand(((x**2-6*x+12)**2-kk*(x-2)*(x**2-6*x+12)))
    for r in sp.Poly(den,x).all_roots():
        if not r.is_real: continue
        L=sp.limit(x**2/den,x,r)
        if not L.is_finite: return False
    return True
ks=[kk for kk in range(-20,21) if ok15(kk)]; R[15]=(ks,sum(ks))
for kk in sorted(R): print(kk,R[kk])
