from sympy import *
x,h,a,b,c,k,p,q,C=symbols('x h a b c k p q C',real=True)
R={}
f=x**3-x; R[1]=[s for s in solve(Eq(diff(f,x),(f.subs(x,3)-f.subs(x,0))/3),x) if s>0]
fp=6*x**2-2*x+1; F=integrate(fp,x); R[2]=limit((F.subs(x,1+3*h)-F.subs(x,1-h))/h,h,0)
f=1+3*(x-2)+x*(x-2)**2; g=x**2*f-3*x; assert f.subs(x,2)==1 and diff(f,x).subs(x,2)==3; R[3]=diff(g,x).subs(x,2)
s=solve([Eq(1+a+b,b+2),Eq(3+2*a,b)],[a,b]); R[4]=(s,(5*x+2).subs(x,2)+(x**3+s[a]*x**2+s[b]).subs(x,-1))
f=x+5*x**2; g=2*x-x**2  # f'(0)=1,g'(0)=2
R[5]=(limit((f+g)/x,x,0),limit((f.subs(x,2*x)+x)/(g-x),x,0))
f=x**3+a*x**2+2; s=solve(Eq(diff(f,x).subs(x,-1),5),a)[0]; bb=f.subs(a,s).subs(x,-1)+5; R[6]=(s,bb,s+bb)
f=Rational(3,2)*x**2+2*x+1; R[10]=diff(f,x).subs(x,-2)
f=a*x**2+b*x+c; s=solve(Poly(expand(diff(f,x)**2-(4*f+8*x**2+4*x-7)),x).all_coeffs(),[a,b,c],dict=True); R[9]=[(t,f.subs(t).subs(x,2)) for t in s]
f=x*(x-1)*(x-k); kk=solve(Eq(limit(f/((x-1)*diff(f,x)**2),x,1),Rational(-1,2)),k); R[12]=(kk,[f.subs(k,v).subs(x,4) for v in kk])
f=p*x*(x-2); pp=solve(Eq(limit((2-x)*f/x,x,0),8),p)[0]; f=f.subs(p,pp); R[13]=(pp,Abs(3-2)*f.subs(x,3))
f=(x-2)**2; g1=f; g2=f.subs(x,x+1)+f
R[14]=(g1.subs(x,1),g2.subs(x,1),diff(g1,x).subs(x,1),diff(g2,x).subs(x,1),g2.subs(x,3))
f=-(x-2)**3+C; Cv=solve(Eq(f.subs(x,0),3),C)[0]; f=f.subs(C,Cv); R[15]=(limit((f-3)/x,x,0),diff(f,x),f.subs(x,3))
g=x*(x+2); hp=symbols('hp',positive=True)
L=(x+2)*g; Rr=(2-3*x)*g
R[16]=('at0',limit((L.subs(x,-hp)-L.subs(x,0))/(-hp),hp,0),limit((Rr.subs(x,hp)-Rr.subs(x,0))/hp,hp,0),'at-2',limit((-(x+2)*g).subs(x,-2-hp)/(-hp),hp,0),limit(((x+2)*g).subs(x,-2+hp)/hp,hp,0),g.subs(x,4))
f=x**4-4*x**3-2*x**2+16*x; ps=solve(Eq(diff(f,x),4),x); v=[]
for P in ps:
  for Q in ps:
    if Q>P: A=P-Q; B=f.subs(x,P)-f.subs(x,Q); v.append((P,Q,A,B,A-B))
R[18]=(v,max(t[4] for t in v)+min(t[4] for t in v))
f=x**3+a*x**2+b*x+2; sa=solve(Eq(diff(f,x).subs(x,-1),diff(f,x).subs(x,3)),a)[0]; f=f.subs(a,sa)
m=diff(f,x).subs(x,-1); l1=m*(x+1)+f.subs(x,-1); l2=m*(x-3)+f.subs(x,3)
R[19]=(sa,simplify(l1.subs(x,0)),simplify(l2.subs(x,0)),solve(Eq((32/m)**2,64),b))
for kk in R: print(kk,R[kk])
