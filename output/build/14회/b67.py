from sympy import *
import itertools
x=symbols('x')
F=symbols('f1:7')
def solve_b67(sumN=5, cond=lambda f:[f[5]<=f[3], f[6]<=f[4]], extra=0):
    # f(n) values f1..f6 ; quartic: 5th difference 0, 4th diff != 0
    eqs=[sum((-1)**k*binomial(5,k)*F[5-k] for k in range(6))]
    res=[]
    # n=1: f1 = f1 f2 + extra? ; general: S_n = f(n) f(n+1)
    # branch on each n: f(n)=0 or recurrence
    branches=[]
    for choice in itertools.product([0,1],repeat=sumN):
        E=list(eqs)
        # n=1
        if choice[0]==0: E.append(F[0])
        else: E.append(F[1]-1)
        for n in range(2,sumN+1):
            if choice[n-1]==0: E.append(F[n-1])
            else: E.append(F[n]-F[n-2]-1)
        sols=solve(E,F,dict=True)
        for s in sols:
            fv={i+1:F[i].subs(s) for i in range(6)}
            if any(not v.is_number for v in fv.values()): 
                # free parameters
                res.append(('free',choice,fv)); continue
            # verify original sum conditions
            ok=all(sum(fv[k] for k in range(1,n+1))==fv[n]*fv[n+1] for n in range(1,sumN+1))
            d4=sum((-1)**k*binomial(4,k)*fv[5-k] for k in range(5))
            if ok and d4!=0:
                res.append(('fix',choice,fv))
    return res
r=solve_b67()
seen=set()
for t,c,fv in r:
    key=tuple(fv[i] for i in range(1,7))
    if key in seen: continue
    seen.add(key)
    print(t,key)
