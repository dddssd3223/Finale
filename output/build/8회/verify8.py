from sympy import *
x,a,b,c,k,p,q,t=symbols('x a b c k p q t',real=True)
R={}
# Q1 L24v
A=symbols('A',positive=True)
F=lambda z: Abs(z*(z-A))
e=simplify((F(x)*F(-x)/x**2).subs(x,Rational(1,1000)))
aa=sqrt(3)
fx=lambda z: abs(z*(z-aa))
R[1]=(limit(x**2*Abs(x**2-3)/x**2,x,0), limit((x*(aa-x))*(x*(x+aa))/(x-aa),x,aa,'-'))
# Q2 C15v
fq=(x-3)*(x+1); gp=x-2*x+3; gn=x+2*x+3   # x>=0: -x+3, x<0: 3x+3
R[2]=(limit(fq/gn,x,-1), limit(fq/gp,x,3), limit(fq/gn,x,-1)*limit(fq/gp,x,3))
# Q3 C9v
def f3(z): return z+2 if z<=0 else -Rational(1,2)*z+6
def lim3(av,side):
    e=Rational(1,10**8)*(1 if side>0 else -1); z=av+e
    return f3(z)*f3(z-av)
sols=[av for av in [Rational(i,2) for i in range(-60,61)] if abs(lim3(av,1)-lim3(av,-1))<1e-5 and abs(lim3(av,1)-f3(av)*f3(0))<1e-5]
R[3]=(sols,sum(sols))
# Q4 L36v
kk=symbols('kk'); g4=kk*(x+2)**2; f4=expand(g4-kk*(x+1)*(x-3)); R[4]=(f4, simplify(f4.subs(x,2)/g4.subs(x,0)))
# Q5 L60v
d=symbols('d'); R[5]=solve((d-2)/(d+1)-Rational(1,4),d)
# Q6 C25v
s=solve([(a+b)/3-5,(4*a+b)/6-7],[a,b]); R[6]=(s,((a*x+b)/(x+2)).subs(s).subs(x,2))
# Q7 C45v
R[7]=(solve(a**2-3*a-4,a), solve(a-(3*a+8),a))
# Q8 L37v
cc=symbols('cc'); g8=cc*(x-1); f8=3*x**3-x**2*g8-3*x
cv=solve(limit(g8/(f8+g8),x,1)+Rational(1,2),cc); R[8]=(cv, g8.subs(cc,cv[0]).subs(x,-2), expand(f8.subs(cc,cv[0])))
# Q9 C54v
f9=(x-2)*(x-3)*(x-4); g9=f9.subs(x,x+2)*(f9+1)/f9
R[9]=(limit(g9,x,2), g9.subs(x,5))
# Q10 C17v: f=|x| (|x|<=2), 2 otherwise
fv=lambda z: min(abs(z),2); R[10]=fv(-3)+fv(1)+fv(Rational(-1,2))
# Q11 L67v: f=x^2+4x+8, (x+2)
cnt=[]
for kv in range(-30,31):
    h=expand((x**2+4*x+8)*((x**2+4*x+8)-kv*(x+2)))
    num,den=fraction(cancel(x**2/h))
    ok=len(Poly(den,x).real_roots())==0
    if ok: cnt.append(kv)
R[11]=(cnt,len(cnt))
# Q12 A14v
s12=solve([4-(-8+b), -50+5*b+c, 4+a-(-8+2*b+c)],[a,b,c]); R[12]=(s12, s12[a]*s12[b]*s12[c], factor(-2*x**2+s12[b]*x+s12[c]))
# Q13 A16v count
def diffable(av,bv):
    fx=(x-2)*(x-5)*Abs((x-av)*(x-bv)**2)
    for r in {av,bv}:
        l=limit((fx-fx.subs(x,r))/(x-r),x,r,'-'); rr=limit((fx-fx.subs(x,r))/(x-r),x,r,'+')
        if l!=rr: return False
    return True
R[13]=sum(1 for av in range(1,10) for bv in range(1,10) if (av in (2,5) or av==bv))
# Q14 T1v
av=sqrt(Rational(10,3)); f14=-x**3+av*x**2+3*x
xa=av; ya=f14.subs(x,xa); sl=diff(f14,x).subs(x,xa); xb=xa-ya/sl
R[14]=(simplify(sl*3), simplify(sqrt(xa**2+ya**2)*sqrt((xb-xa)**2+ya**2)))
# Q15 L66 원본 확인, g(6)
f15=(x-1)**2*(x-2); g15=(x-1)*(x**2-7*x+13)
R[15]=([limit(f15/g15,x,n) for n in (1,2,3,4)], g15.subs(x,6))
# Q16 L68v: brute integer a,b with f=x^3+ax^2+bx-9, lim f(3x-2)/f(x) exists everywhere
best=None; sols=[]
for av_ in range(-20,21):
    for bv in range(-40,41):
        f=x**3+av_*x**2+bv*x-9
        num,den=fraction(cancel(f.subs(x,3*x-2)/f))
        ok=len(Poly(den,x).real_roots())==0
        if ok: sols.append((av_,bv,f.subs(x,2)))
R[16]=(len(sols), max(s_[2] for s_ in sols), [s_ for s_ in sols if s_[2]==max(t_[2] for t_ in sols)])
# Q17 B63v
P,Q,Rr=symbols('P Q Rr'); f17=x**3+P*x**2+Q*x+Rr
D=expand((f17.subs(x,x+2)-f17)/2); s17=solve([D.coeff(x,1)+6, D.coeff(x,0)-2],[P,Q])
ok=all((3*k_-4)<=(3*k_**2-6*k_+2)<=(4*k_**2-9*k_+4) for k_ in range(-50,50))
R[17]=(s17, ok, diff(f17,x).subs(s17).subs(x,5))
# Q19 F-19v: f=x(x-k)^2, f'(0)+f'(2)=4
K=symbols('K'); f19=x*(x-K)**2; R[19]=(solve(diff(f19,x).subs(x,0)+diff(f19,x).subs(x,2)-4,K), f19.subs(K,2).subs(x,1), 2*f19.subs(K,2).subs(x,8))
# Q20 L65v
h=(x-1)*(x-3)+2; g20=(x-1)*(x-3)*h; R[20]=(discriminant(h,x), g20.subs(x,-1))
for kk_,v in R.items(): print(kk_,v)
