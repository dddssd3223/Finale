from sympy import *
x,t,a,b,c,p,q,k,r=symbols('x t a b c p q k r')
R={}
# 1 C5 variant
R[1]=limit((x**2+2*x-8)/(sqrt(x+2)-2),x,2)
# 2 L51 variant: f-2 ~ 3(x-1)
f=2+3*(x-1)+7*(x-1)**2
R[2]=limit((x**2-1)/(f**2-4),x,1)
# 3 product
f=(x**2-2)*(x**2+a*x+1); R[3]=solve(diff(f,x).subs(x,1)-10,a)
# 4 graph: f = -x+1 (x<0), x-1 (0<=x<1) ,2 at x=1, -x+3 (x>1)  -> lim0- f + lim1+ f(x)f(-x)
R[4]=1+2*(-(-1)+1)
# 5 L26
R[5]=solve([1+a+b,(2+a)/4-2],[a,b])
# 6 C39 : f={-x+6 (x<a), 3x-a (x>=a)}
R[6]=solve((6-a)**2-(2*a)**2,a)
# 7 T4
R[7]=solve([3+a-5, 1+a+3-(5+b)],[a,b])
# 8 L25
f=x*(x-2)*(p*x+q); R[8]=solve([limit(f/x,x,0)+2, limit(f/(x-2),x,2)-10],[p,q]); R['8f']=f.subs(R[8]).subs(x,3)
# 9 C14: f={-x+4 (x<1),2x+a}, g=-x^2+3x+a
R[9]=[s for s in [-2,1]]
assert (-1+3-2)==0 or True
# 10 L28
aa=solve(sqrt(1+a)-3,a)[0]; R[10]=(aa, limit((sqrt(x**2+aa*x)-3)/(x**2-1),x,1))
# 11 C44: f=p(x-1)(x-3), lim f/(x-3)=4 at 3
f=p*(x-1)*(x-3); pp=solve(limit(f/(x-3),x,3)-4,p)[0]; R[11]=f.subs(p,pp).subs(x,5)
# 12 L47 variant
A,B,C,K=symbols('A B C K'); f=A*x**2+B*x+C
s1=[f.subs(x,2)-4]
num=f-2*x
# lim_{x->2} (f-2x)/(x^2-4)=K : (f'(2)-2)/4 = K
eqs=[f.subs(x,2)-4, (diff(f,x).subs(x,2)-2)/4-K, ]
# lim_{x->4}(f(x)-f(x-2))/(x-4) = 2K: need f(4)=f(2) then derivative f'(4)-f'(2)
eqs+= [f.subs(x,4)-f.subs(x,2), diff(f,x).subs(x,4)-diff(f,x).subs(x,2)-2*K]
sol=solve(eqs,[A,B,C,K],dict=True); R[12]=[(s,f.subs(s).subs(x,10)) for s in sol]
# 13 |x^2-4x|
R[13]=2+5*(5-4)
# 14 L35 variant
f=k*(x+2)*(x-1)*(x-3)+3; kk=solve(f.subs(x,2)+1,k)[0]; R[14]=(kk,f.subs(k,kk).subs(x,4))
# 15 C35 general: f=(x-2)^2-4
R[15]=((x-2)**2-4).subs(x,5)
# 16 L30 general
R[16]=solve(a**2-a-6,a)
# 17 C51 general
best=[]
for n in range(1,60):
    bmax=ceiling(2*sqrt(n))-1
    for bb in range(-n,bmax+1):
        if bb**2<4*n and 1+bb+n>=1:
            best.append((Rational(n+2,n+4+2*bb),n,bb))
best.sort(); R[17]=best[:3]; n0,b0=best[0][1],best[0][2]; R['17f']=(x*(x**2+b0*x+n0)).subs(x,2)
# 19 F-28 staged
f=(x-3)*(x-4)*(x-Rational(1,3)); fe=expand(f); R[19]=(fe.subs(x,0), fe.coeff(x,2), limit((fe.coeff(x,0)*x**3+fe.coeff(x,1)*x**2+fe.coeff(x,2)*x+1)/fe,x,3))
# 20 C24 variant
pr=[pv for pv in range(-10,10) if pv**2<20 and 6+pv>=1 and (1+pv+2)<0]
R[20]=(pr, (x*(x**2-4*x+5)).subs(x,3))
for k_,v in R.items(): print(k_,v)
