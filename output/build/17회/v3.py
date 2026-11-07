import numpy as np
def make(a,b,q,m):
    def G(x):
        return b*x/(x+a) if x<2 else (x-q)**2+m
    return G
def h(G,a,t):
    # count solutions of |G(x)|=t via sign changes on fine grid + tangency approx
    xs=np.concatenate([np.linspace(-60,-a-1e-6,300001),np.linspace(-a+1e-6,2-1e-12,300001),np.linspace(2,60,300001)])
    v=np.array([abs(G(x)) for x in xs])-t
    cnt=0
    for seg in (slice(0,300001),slice(300001,600002),slice(600002,900003)):
        s=v[seg]; z=np.sum(s==0); ch=np.sum(np.sign(s[:-1])*np.sign(s[1:])<0); cnt+=z+ch
    return cnt
a,b,q,m=2,6,5,-6
G=make(a,b,q,m)
print('f(2)',G(2),'= 2b/(2+a)',2*b/(2+a))
for t in [0,0.5,1,2.9,3,3.1,4,5.9,6,6.1,8,20]:
    print(t,h(G,a,t))
print('f(ab)',(a*b-q)**2+m)
