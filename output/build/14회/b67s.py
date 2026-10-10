from b67 import *
r=solve_b67()
cands={}
for t,c,fv in r:
    cands[tuple(fv[i] for i in range(1,7))]=fv
import itertools
ops={'<=':lambda a,b:a<=b,'>=':lambda a,b:a>=b,'<':lambda a,b:a<b,'>':lambda a,b:a>b}
for ns in [(1,2),(2,3),(3,4),(1,3),(1,4),(2,4)]:
  for step in (1,2):
    for op in ops:
        ok=[k for k,fv in cands.items() if all(ops[op](fv[n+step] if n+step<=6 else None, fv[n]) for n in ns if n+step<=6)]
        if len(ok)==1:
            fv=cands[ok[0]]
            # interpolate quartic
            pts=[(i,fv[i]) for i in range(1,6)]
            P=interpolate(pts,x)
            print(ns,step,op,ok[0], 'f(5/2)*128=',P.subs(x,Rational(5,2))*128, 'f(0)=',P.subs(x,0),'f(7/2)=',P.subs(x,Rational(7,2)), 'lead',Poly(P,x).LC())
