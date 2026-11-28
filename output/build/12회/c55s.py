from c55 import *
import itertools
for d in [3]:
  for cc in [Rational(n,2) for n in range(-12,13) if n!=0]+[Rational(n,3) for n in (-10,-8,-7,-5,-4,-2,-1,1,2,4,5,7)]:
    r=solve_case(d,cc)
    if len(r)==1:
        tch,pv,k,S=list(r)[0]
        F=k*x*(x-d)*(x-pv); t={'0':0,'d':d,'p':pv}[tch]
        gv=lambda xx: (-F if xx<t else F).subs(x,xx)
        print(d,cc,r,[gv(v) for v in (-5,-4,-3,-2,4,5,6)],flush=True)
    else: print(d,cc,len(r),flush=True)
