# C55 variant design: zeros r1<r2 of denominator, f=c(x-r1)(x-r2)(x-p), t in {r1,r2,p}
from fractions import Fraction as F
import itertools
r1,r2=-1,3
def negset(t,p,M=30):
    S=set()
    for m in range(1,M):
        if (m>=t and m<p) or (m<t and m>p): S.add(m)
    return S
def gval(x,t,p,c):
    f=c*(x-r1)*(x-r2)*(x-p)
    return f if x>=t else -f
# search over rational p and c>0, k for set {g(A), k g(B)}
A,B=0,2
sols=[]
ps=[F(n,d) for d in (1,2,3,4,5,6) for n in range(-40,60)]
ps=sorted(set(ps))
for K in [F(k,2) for k in range(-12,13) if k!=0]:
  found=[]
  for p in ps:
    for t in {r1,r2,p}:
      S=negset(t,p)
      if len(S)!=2: continue
      a,b=sorted(S)
      # g(A)=u*c, k g(B)=v*c with c>0 unknown
      u=gval(A,t,p,1); v=K*gval(B,t,p,1)
      for x,y in [(a,b),(b,a)]:
        # u c = x, v c = y
        if u==0 or v==0: continue
        c=F(x)/u
        if c>0 and v*c==y and u*c!=v*c:
          found.append((p,t,c,x,y))
  if len(found)==1: sols.append((K,found[0]))
for s in sols: print(s)
