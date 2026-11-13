import numpy as np, math
# 14 C7': f={-x^2+4x (x<3), 2x+k}, g(t)=max on [t,t+2], continuous for all t
def f(x,k): return -x*x+4*x if x<3 else 2*x+k
def g(t,k):
    xs=np.linspace(t,t+2,4001); xs=np.append(xs,[3.0] if t<=3<=t+2 else [])
    return max(f(v,k) for v in xs)
def cont(k):
    for t0 in np.arange(-3,7,0.25):
        for d in (1e-6,):
            if abs(g(t0-d,k)-g(t0,k))>1e-3 or abs(g(t0+d,k)-g(t0,k))>1e-3: return False
    return True
ks=[kk for kk in range(-12,4) if cont(kk)]
print('14 ints',ks,len(ks),'g(4)max',max(g(4,kk) for kk in ks), 'real range check', [ (kk,cont(kk)) for kk in (-7.2,-6.9,-2.1,-1.9)])
# 16
def F(x): return x-1 if x<0 else (1.5 if x==0 else x-2)
G=lambda x: F(x)+abs(F(x)); H=lambda x: F(x)+F(-x)
e=1e-9
print('16 ㄱ lim g',G(e),G(-e),'| |h| cont', abs(H(e)),abs(H(-e)),abs(H(0)),'| h cont',H(e),H(0),'| g(h-3) at0',G(e)*(H(e)-3),G(0)*(H(0)-3))
# check |h| continuity everywhere and g(h-3) everywhere
xs=np.linspace(-5,5,20001)
print('16 h const away 0', set(round(H(v),6) for v in xs if abs(v)>1e-6))
# 18
c,pp=0.25,8/3
fx=lambda x: c*(x+1)*(x-3)*(x-pp)
gx=lambda x: fx(x) if x>=-1 else -fx(x)
neg=[m for m in range(1,20) if (gx(m+1e-7)/((m+1e-7+1)*(m+1e-7-3)))<0]
print('18 negset',neg,'g(0)',gx(0),'2g(2)',2*gx(2),'g(-3)',gx(-3))
# danap L62': y=2tx-4, P=(t,t^2), Q=(4/t,4)
def PQ(t): return math.hypot(4/t-t,4-t*t)
print('S1 (1) dist t=1', abs(2*1-1-4)/math.sqrt(5), 3/math.sqrt(5),'(2) PQ t=1',PQ(1),3*math.sqrt(2),'(3)',PQ(2-1e-7)/1e-7, 2*math.sqrt(5))
# check P is min distance point: numeric
for tt in (0.5,1,1.7):
    xs=np.linspace(-5,5,200001); d=np.abs(2*tt*xs-xs**2-4)/math.sqrt(4*tt*tt+1); print(' argmin',tt,xs[d.argmin()])
