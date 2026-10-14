from fractions import Fraction as Fr
import itertools
def make(p1,c,p3,a,b):
    def f(x):
        if x<a: return abs(x+p1[0])+p1[1]
        if x<b: return x+c
        return abs(x-p3[0])+p3[1]
    return f
def run(p1,c,p3,maxb=8,show=False):
    out=[]
    e=Fr(1,10**6)
    for a in range(1,maxb):
        for b in range(a+1,maxb):
            f=make(p1,c,p3,a,b)
            # candidate k: grid of quarters up to 20
            for k4 in range(1,80):
                k=Fr(k4,4)
                if not f(k)<0: continue
                h=lambda x: f(x)*f(x+k)
                ok=True
                for t in [a,b,a-k,b-k]:
                    if abs(h(t-e)-h(t))>Fr(1,1000) or abs(h(t+e)-h(t))>Fr(1,1000): ok=False;break
                if ok: out.append((a,b,k,f(a)*f(b)*f(k)))
    return out
print('orig',run((3,-1),-10,(9,-1)))
for p1 in [(2,-2),(2,-1),(3,-2),(4,-1)]:
    for c in [-8,-9,-10,-11]:
        for p3 in [(8,-2),(8,-1),(9,-2),(10,-1),(9,-1)]:
            r=run(p1,c,p3)
            if len(r)==1: print(p1,c,p3,r)
