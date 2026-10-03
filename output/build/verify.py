from sympy import *
x,h,a,b,c,k,t,y,p=symbols('x h a b c k t y p',real=True)
R={}
# 1
f=x**3-x; avg=(f.subs(x,3)-f.subs(x,0))/3
R[1]=[s for s in solve(Eq(diff(f,x),avg),x) if 0<s<3]
# 2: f'(2)=3 any poly e.g. f=3x+ (x-2)^2
f=3*x+(x-2)**2
assert limit((f.subs(x,2+3*h)-f.subs(x,2-h))/h,h,0)==12
R[2]=limit((x**2-4)/(f-f.subs(x,2)),x,2)
# 3
f=2+3*(x-1)+(x-1)**2; assert limit((f-2)/(x-1),x,1)==3
R[3]=diff((x**2+1)*f,x).subs(x,1)
# 4
sol=solve([Eq(1+a,b+3),Eq(3+a,2*b)],[a,b]); R[4]=(sol, 4*sol[b]+3)
# 5
F=Function('F'); fp=(6*x**2-12*x+9)/3; f=integrate(fp,x)
assert simplify(limit((f.subs(x,x+2*h)-f.subs(x,x-h))/h,h,0)-(6*x**2-12*x+9))==0
g=limit((f.subs(x,x+h)-f.subs(x,x-3*h))/(2*h),h,0); R[5]=g.subs(x,1)+g.subs(x,-1)
# 6
f=x**3-3*x+a; ts=solve(Eq(diff(f,x),9),x)
lines=[expand(9*(x-x0)+f.subs(x,x0)) for x0 in ts]
big=max(lines,key=lambda L:L.subs({x:0,a:0}))
R[6]=(lines,solve(Eq(big.subs(x,1),3),a))
# 7
f=3+2*(x-1); gv=symbols('gv'); gp=symbols('gp')
R[7]=solve([Eq(3*gv,6),Eq(2*gv+3*gp,10)],[gv,gp])
# 8
f=Piecewise((x**2+2*x,x<1),(3*x,True))
R[8]=(limit((f.subs(x,1+h)-f.subs(x,1-h))/h,h,0,'+'),limit((f.subs(x,1+h)-3)/h,h,0,'+'),limit((f.subs(x,1+h)-3)/h,h,0,'-'),
 limit(((h)*f.subs(x,1+h))/h,h,0,'+'),limit(((h)*f.subs(x,1+h))/h,h,0,'-'))
# 9
A,B,C=symbols('A B C'); f=A*x**2+B*x+C
eqs=Poly(expand(diff(f,x)**2-(4*f+8*x**2+4*x-7)),x).all_coeffs()
R[9]=[(s,(f.subs(s)).subs(x,2)) for s in solve(eqs,[A,B,C],dict=True)]
# 10
f=Rational(3,2)*x**2+2*x+1
assert simplify(f.subs(x,x+y)-(f+f.subs(x,y)+3*x*y-1))==0 and diff(f,x).subs(x,1)==5
R[10]=diff(f,x).subs(x,-2)
# 11
f1=x**2-2*x+10; f2=-x**2+2*x+8
assert f1.subs(x,1)==f2.subs(x,1) and diff(f1,x).subs(x,1)==diff(f2,x).subs(x,1)
R[11]=(solve(f1,x),solve(f2,x),f1.subs(x,-1)+f2.subs(x,3))
# 12
f=x**3+a*x**2+b*x
s=solve([Eq(diff(f,x).subs(x,2),(f.subs(x,3)-f.subs(x,0))/3),Eq(diff(f,x).subs(x,3),6)],[a,b])
ff=f.subs(s); R[12]=(s,solve(Eq(diff(ff,x),(ff.subs(x,3))/3),x),ff.subs(x,1))
# 13
f=x**3-3*x**2-x
R[13]=(limit(f/x,x,0),limit(x*(f.subs(x,2+3/x)-f.subs(x,2)),x,oo),limit((f-x**3)/x**2,x,oo),f.subs(x,3))
# 14
f=Piecewise((x+1,x<1),(3-x,True))
def lr(G):
  return (limit((G.subs(x,1+h)-G.subs(x,1))/h,h,0,'+'),limit((G.subs(x,1+h)-G.subs(x,1))/h,h,0,'-'))
R[14]=(lr((x-1)*f),lr(f*f.subs(x,2-x)),lr((f-2)*Abs(x-1)))
# 15
f=x*(x-2)*(x+1); g=Abs(x-2)*f
R[15]=(limit(g/x,x,0),lr2:=None)
gl=limit((g.subs(x,2+h)-g.subs(x,2))/h,h,0,'-'); gr=limit((g.subs(x,2+h)-g.subs(x,2))/h,h,0,'+')
R[15]=(limit(g/x,x,0),gl,gr,g.subs(x,3))
# 16
f=2*x**3+a*x**2+b*x
s=solve([Eq(diff(f,x).subs(x,3),diff(f,x).subs(x,0)),Eq(diff(f,x).subs(x,1),0)],[a,b]); ff=f.subs(s)
def F(v):  # extend
  n=floor(Rational(v)/3); r=v-3*n; return ff.subs(x,r)+n*ff.subs(x,3)
R[16]=(s,ff.subs(x,3),F(7),F(-2))
# 17
res=[]
for case in [(x-a)**2*(x-2*a),(x-a)*(x-2*a)**2]:
  f=case+2*x+1
  for av in solve(Eq(diff(f,x).subs(x,0),22),a):
    if av!=0 and f.subs({a:av,x:0})>1: res.append((case,av,f.subs({a:av,x:1})))
R[17]=res
# 18
f=x**3+a*x**2+b*x+2
sa=solve(Eq(diff(f,x).subs(x,-1),diff(f,x).subs(x,3)),a)[0]; f=f.subs(a,sa)
s=diff(f,x).subs(x,-1)
l1=s*(x+1)+f.subs(x,-1); l2=s*(x-3)+f.subs(x,3)
T=solve(l1,x)[0]; Sx=solve(l2,x)[0]
bs=solve(Eq((T-Sx)**2,64),b)
R[18]=(sa,simplify(l1.subs(x,0)),simplify(l2.subs(x,0)),bs,sum(bs))
# 19
f=x**3+p*x**2-x+2
assert f.subs(x,0)==2 and diff(f,x).subs(x,0)==-1
A_=symbols('A',positive=True)
pp=solve(Eq(diff(f,x).subs(x,-A_),-1),p); 
fA=f.subs(p,pp[0]); bb=simplify(2-fA.subs(x,-A_))
tang=expand(-1*(x-A_)+2+bb)
Av=solve(Eq(tang.subs(x,0),-2),A_)
f2=fA.subs(A_,Av[0]); b2=bb.subs(A_,Av[0])
g=Piecewise((f2,x<=0),(f2.subs(x,x-Av[0])+b2,True))
R[19]=(pp,bb,tang,Av,b2,expand(f2),g.subs(x,4),
 limit((g.subs(x,h)-g.subs(x,0))/h,h,0,'+'),limit((g.subs(x,h)-g.subs(x,0))/h,h,0,'-'),limit(g,x,0,'+'))
# 20
al=symbols('alpha')
for alv in [0,1,-2]:
  gq=-(x-alv)**2+6*(x-alv)+5; hh=(x-alv)**2*(x-alv-6); f=gq+hh
  assert diff(f,x).subs(x,alv)==6==diff(gq,x).subs(x,alv) and f.subs(x,alv)==gq.subs(x,alv)
  be=solve(Eq(diff(gq,x),-2),x)[0]; assert diff(f,x).subs(x,be)==-2
  P=(alv,gq.subs(x,alv)); Q=(alv+6,gq.subs(x,alv+6)); Rr=(be,f.subs(x,be))
  area=Abs((Q[0]-P[0])*(Rr[1]-P[1])-(Rr[0]-P[0])*(Q[1]-P[1]))/2
  R.setdefault(20,[]).append((be-alv,solve(f-gq,x),P,Q,Rr,area))
for kk in sorted(R): print(kk,R[kk])
