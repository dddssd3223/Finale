from sympy import *
x,h,a,b,c,p,q,r,k=symbols('x h a b c p q r k',real=True)
hp=symbols('hp',positive=True)
R={}
def lr(Fl,Fr,x0):  # one-sided derivatives with explicit pieces
    return (limit((Fl.subs(x,x0-hp)-Fl.subs(x,x0))/(-hp),hp,0), limit((Fr.subs(x,x0+hp)-Fr.subs(x,x0))/hp,hp,0))
# 1
f=x**3+a*x**2+b*x
s=solve([Eq((f.subs(x,3)-f.subs(x,-1))/4,2*diff(f,x).subs(x,1)), Eq(limit((f-f.subs(x,1))/(x**2-1),x,1),f.subs(x,1)-2)],[a,b],dict=True)
R[1]=(s,[v[a]*v[b] for v in s])
# 2
F=Function('F')
fp1=symbols('fp1'); # g=x^2 f, g'(1)=2f(1)+f'(1); 4g'(1)=20
fp=solve(Eq(4*(2*2+fp1),20),fp1)[0]; R[2]=(fp, Rational(1,2)*fp+Rational(1,3)*fp)
# check with explicit f
ff=2+fp*(x-1)+7*(x-1)**2; g=x**2*ff
assert limit((g.subs(x,1+3*h)-g.subs(x,1-h))/h,h,0)==20
R[2]=R[2]+(limit((ff.subs(x,1+h/2)-ff.subs(x,1-h/3))/h,h,0),)
# 3
ff=3*x-4+5*(x-2)**2; g=(x**3-2*x)*ff
gp=diff(g,x).subs(x,2); R[3]=(g.subs(x,2),gp,expand(gp*(0-2)+g.subs(x,2)))
# 4
L=x**2+a*x+b; Rr=x**3+c*x
s=solve([Eq(diff(Rr,x).subs(x,1),1),Eq(L.subs(x,-1),Rr.subs(x,-1)),Eq(diff(L,x).subs(x,-1),diff(Rr,x).subs(x,-1))],[a,b,c],dict=True)[0]
R[4]=(s,L.subs(s).subs(x,-2)+Rr.subs(s).subs(x,2))
# 5
f1=x**2+2*x-1; f2=-x**3+2*x-1; f3=2*x**2-4*x+2
R[5]=('cont0',f1.subs(x,0),f2.subs(x,0),'cont1',f2.subs(x,1),f3.subs(x,1),
      'ga',limit((f1+1)/x,x,0,'-'),limit((f2+1)/x,x,0,'+'),'nu',lr(f2,f3,1),'da',lr(f2**2,f3**2,1))
# 6
f=x**3+a*x**2+b*x
s=solve([Eq(b,-1),Eq(3*diff(f,x).subs(x,2),a)],[a,b],dict=True)[0]; ff=f.subs(s)
R[6]=(ff,limit(ff/x,x,0),limit(x*(ff.subs(x,2+3/x)-ff.subs(x,2)),x,oo),limit((ff-x**3)/x**2,x,oo),ff.subs(x,3))
# 7  (x^2-4)g = f-3x, f'(2)=7, h'(2)=10, f'(-2)=-1
g2,gp2,gm2=symbols('g2 gp2 gm2')
f2v=6; s=solve([Eq(4*g2,7-3),Eq(7*g2+f2v*gp2,10),Eq(-4*gm2,-1-3)],[g2,gp2,gm2])
R[7]=(s,s[g2]+s[gp2]+s[gm2])
# 9
f1=x**2-2*x+10; f2=-x**2+2*x+8
R[9]=(f1.subs(x,1),f2.subs(x,1),lr(f1,f2,1),solve(f2,x),f1.subs(x,-1)+f2.subs(x,3))
# 10
ff=x*(x-2)*(x+1)
R[10]=(limit(Abs(x-2)*ff/x,x,0), lr((2-x)*ff,(x-2)*ff,2), Abs(3-2)*ff.subs(x,3))
# 11
f=x**3+p*x**2+q*x; G=f.subs(x,x+1)-f
s=solve([Eq(f.subs(x,1),G.subs(x,1)),Eq(diff(f,x).subs(x,1),diff(G,x).subs(x,1))],[p,q],dict=True)[0]
R[11]=(s,G.subs(s).subs(x,3))
# 12
res=[]
for rr,ss in [(2,6),(-2,-6),(2*sqrt(2),3*sqrt(2)),(-2*sqrt(2),-3*sqrt(2))]:
    av=-(rr+ss); assert simplify(rr*ss-12)==0
    ff=x**3+av*x**2+12*x+2; res.append((av,ff.subs(x,1)))
R[12]=(res,max(r1 for _,r1 in res))
# 13
al,be,ga=symbols('al be ga'); qq=al*x**2+be*x+ga
s=solve([Eq(qq.subs(x,0),a),Eq(qq.subs(x,2),4+a),Eq(qq.subs(x,2),6),Eq(diff(qq,x).subs(x,2)/12,Rational(1,2))],[al,be,ga,a],dict=True)[0]
fq=expand((x**2-2*x)*qq.subs(s)); gq=qq.subs(s)
R[13]=(s,fq,limit((gq-6)/fq,x,2),gq.subs(x,s[a]+1))
# 14
ff=2*x**2+2*x+1; assert simplify((ff.subs(x,x+1)-ff.subs(x,x-1))/2-(4*x+2))==0
gg=ff+(x-1)**2*(x-3); R[14]=(ff.subs(x,1),gg.subs(x,1),ff.subs(x,2)+gg.subs(x,2))
# 15
gg=x*(x+2)*(x-c); FL=x+2; FR=2-3*x
cv=solve(Eq(diff(FR*gg,x).subs(x,1),10),c)[0]; gg=gg.subs(c,cv)
R[15]=(cv,lr(-(x+2)*gg,(x+2)*gg,-2),lr(FL*gg,FR*gg,0),gg.subs(x,4))
# 16
f=x**3+p*x**2+q*x+r; A_,B_=symbols('A_ B_')
G1=f+4*x; G2=-f+A_; G3=f-2*x+B_
s=solve([Eq(G1.subs(x,0),G2.subs(x,0)),Eq(diff(G1,x).subs(x,0),diff(G2,x).subs(x,0)),Eq(G2.subs(x,3),G3.subs(x,3)),Eq(diff(G2,x).subs(x,3),diff(G3,x).subs(x,3)),Eq(f.subs(x,1),2)],[p,q,r,A_,B_],dict=True)[0]
R[16]=(s,G2.subs(s).subs(x,1)+G3.subs(s).subs(x,4))
# 18
f=x**4-4*x**3-2*x**2+16*x
ps=solve(Eq(diff(f,x),4),x); vals=[]
for P in ps:
  for Q in ps:
    if P!=Q: A=Q-P; B=f.subs(x,P)-f.subs(x,Q); vals.append((P,Q,A,B,A*B))
abv=[v[4] for v in vals]; R[18]=(ps,vals,max(abv)+min(abv))
# 19
qv=symbols('qv',positive=True)
ff=x**2*(x**2-2*x+qv)
R[19]=(limit(diff(ff,x)**2/(x**2*ff),x,oo), limit(ff/diff(ff,x),x,1), factor(2*ff-diff(ff,x)), [ (qq_, 4*qq_) for qq_ in [Rational(9,4),2]], Rational(9,4)*4+8)
# 20
f=x**4-4*x**3+2*x**2+4*x
cr=solve(diff(f,x),x); R[20]=[(cc,simplify(f.subs(x,cc))) for cc in cr]
g=f.subs(x,x+1); R['20b']=(expand(g),factor(g-g.subs(x,sqrt(2))))
for kk in R: print(kk,R[kk])
