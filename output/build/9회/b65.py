from sympy import *
x=symbols('x',real=True)
def analyze(f1,f2,xk,A,B,lo=-10,hi=10):
    # f = f1 (x<xk), f2 (x>=xk); g=min(dA^2,dB^2)
    pts=set()
    for fx,(L,R) in [(f1,(lo,xk)),(f2,(xk,hi))]:
        dA=(x-A[0])**2+(fx-A[1])**2; dB=(x-B[0])**2+(fx-B[1])**2
        for r in solve(Eq(dA,dB),x):
            if r.is_real and L<r<R and diff(dA-dB,x).subs(x,r)!=0: pts.add(r)
    # kink at xk
    def comp(fx):
        dA=(x-A[0])**2+(fx-A[1])**2; dB=(x-B[0])**2+(fx-B[1])**2
        return dA,dB
    a1,b1=comp(f1); a2,b2=comp(f2)
    v1=min(a1.subs(x,xk),b1.subs(x,xk))
    act1 = a1 if a1.subs(x,xk)<=b1.subs(x,xk) else b1
    act2 = a2 if a2.subs(x,xk)<=b2.subs(x,xk) else b2
    if a1.subs(x,xk)==b1.subs(x,xk):
        # left derivative of min = min slope? handle generally numerically
        pass
    eps=Rational(1,10**6)
    g=lambda t: min(((t-A[0])**2+((f1 if t<xk else f2).subs(x,t)-A[1])**2),((t-B[0])**2+((f1 if t<xk else f2).subs(x,t)-B[1])**2))
    ld=(g(xk)-g(xk-eps))/eps; rd=(g(xk+eps)-g(xk))/eps
    if abs(float(ld-rd))>1e-3: pts.add(xk)
    return sorted(pts)
# 원본 확인
p=analyze(x+1,-2*x+4,1,(-1,-1),(1,2)); print('orig',p,80*sum(p))
for A,B,f1,f2,xk in [((-1,-2),(2,1),2*x+1,-x+4,1),((-2,-1),(1,3),x+2,-2*x+5,1),((0,-2),(2,2),x,-x+4,2),((-1,0),(2,3),x+1,-x+5,2)]:
    p=analyze(f1,f2,xk,A,B); print(A,B,f1,f2,xk,p,sum(p))
