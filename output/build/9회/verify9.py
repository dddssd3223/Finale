from sympy import *
import itertools
x=symbols('x',real=True); R={}
R[1]=limit((x**3-1)/(x**2+x-2),x,1)
R[2]=diff((2*x+1)*(x**2-3),x).subs(x,1)
R[3]=limit(sqrt(4*x**2+3*x)-2*x,x,oo)
a=symbols('a'); av=solve(4+2*a-6,a)[0]; R[4]=(av, limit((x**2+av*x-6)/(x-2),x,2))
f=x**3-x; h=symbols('h'); R[5]=limit((f.subs(x,2+3*h)-f.subs(x,2-h))/h,h,0)
f=x**3-3*x**2+2; R[6]=f.subs(x,1)-diff(f,x).subs(x,1)*1
R[7]=2*2*5+4*4
# 8 C29v: x<2 fg=x^2-3x-10, x>2 g/f=x+1, f>0
F=symbols('F',positive=True); R[8]=(solve(3*F**2-12,F), (2+1)*2)   # f(2)=2, g(2+)=3*2=6 → f(2)*g(2+)=12
# 9 L59v: fg=2x^4+cx^3+4x^2, fg(2)=0, (fg)'(2)=8
c=symbols('c'); P=2*x**4+c*x**3+4*x**2; cv=solve(P.subs(x,2),c)[0]; P=P.subs(c,cv)
facs=[2,x,x,x-1,x-2]; best=-oo
for mask in itertools.product([0,1],repeat=5):
    ff=sympify(prod([facs[i] for i in range(5) if mask[i]] or [1]))
    for sg in (1,-1): best=max(best,sg*ff.subs(x,2))
R[9]=(factor(P), diff(P,x).subs(x,2), best)
# 10 L39v: f quintic monic, A={a|lim x^3(x-2)/f exists}, B={b|lim f/(x^2(x-2)^4) not exist}; 0∈A-B, 2∈B-A, f(4)=320
cands=[]
for m in (2,3):
    for n in (2,3):
        if m+n==5: cands.append(x**m*(x-2)**n)
cv=symbols('cv'); cands.append(x**2*(x-2)**2*(x-cv))
out=[]
for f in cands:
    if f.has(cv):
        s=solve(f.subs(x,4)-320,cv); out.append((s, f.subs(cv,s[0]).subs(x,3)))
    else: out.append(f.subs(x,4))
R[10]=out
# 11 L64v
best=[]
for n in range(1,8):
    # f - 2x^4 + 5x^3 has degree n+1, lead 3 (if n+1>=1), lowest term of f is 6x^n
    # try general f of degree<=8 with unknown coeffs and solve
    cs=symbols('c0:9'); f=sum(cs[i]*x**i for i in range(9))
    eqs=[]
    G=expand(f-2*x**4+5*x**3)
    for i in range(9):
        if i>n+1: eqs.append(G.coeff(x,i))
    eqs.append(G.coeff(x,n+1)-3)
    for i in range(n): eqs.append(f.coeff(x,i))
    eqs.append(f.coeff(x,n)-6)
    s=solve(eqs,cs,dict=True)
    for sol in s:
        fs=f.subs(sol)
        if fs.free_symbols: best.append((n,'free',fs))
        else: best.append((n,fs.subs(x,1)))
R[11]=best
# 12 B43v: f=3x-1, g=f+(x-1)^2(x-4)^2
f=3*x-1; g=f+(x-1)**2*(x-4)**2; R[12]=(g.subs(x,0)+f.subs(x,5))
# 13 A41v: f'(x)/3 * (-g'(x)/4) = -2(x^3+x+10) → f'g'=24(x+2)(x^2-2x+5)
tot=0; lst=[]
for A_ in [d for d in divisors(24)]:
    B_=24//A_
    if A_%3==0 and B_%2==0:
        m=A_*4; lst.append((A_,B_,B_*(m+2))); tot+=B_*(m+2)
R[13]=(lst,tot)
# 14 B64v: g lead 3, slopes ∓18
al=symbols('al'); be=al+6; ga=al+9; hh=(x-al)**2*(x-ga)
R[14]=(simplify(-hh.subs(x,be+2)), simplify(diff(hh,x).subs(x,be)))
# 16 B65v
R[16]='19/7 -> 14p=38'
# 17 C56v: f=(x+2)^2, b=6, a=1/2
f=lambda z:(z+2)**2; b_=6; a_=Rational(2*f(0),f(-b_)); R[17]=(a_, (8+a_)*f(8-b_))
# 18 ext 2회21: f=(x-1)^2(x+3/2), g=ff'
f=(x-1)**2*(x+Rational(3,2)); R[18]=(f*diff(f,x)).subs(x,3)
# S1 1회14v: f=(x-1)^2(x-4)
f=(x-1)**2*(x-4); fp=diff(f,x); k=limit(f/fp**2,x,1); g5=(f/fp**2).subs(x,5); R['S1']=(solve(fp,x),diff(f,x).subs(x,2),k,g5,72*(g5-k))
# S2 C30v
f=(x-1)*(x+4); hh=f.subs(x,x-3)/f.subs(x,x**2); R['S2']=(limit(hh,x,-1), f.subs(x,5)*limit(hh,x,-1), limit(hh,x,1,'+'))
for k_,v in R.items(): print(k_,v)
