import sympy as sp
p,c,x=sp.symbols('p c x',real=True)
K=2; A,B=0,2
f=c*(x+1)*(x-3)*(x-p)
def g(xv,t): 
    # t numeric or p
    return f.subs(x,xv) if sp.simplify(xv - t)>=0 else -f.subs(x,xv)
cases=[(-1,(2,3),{1,2}),(3,(4,5),{3,4}),(3,(-sp.oo,1),{1,2})]
for t,(lo,hi),S in cases:
    a,b=sorted(S)
    for X,Y in [(a,b),(b,a)]:
        eqs=[sp.Eq(g(A,t),X),sp.Eq(K*g(B,t),Y)]
        sol=sp.solve(eqs,[p,c],dict=True)
        for s in sol:
            pv,cv=s[p],s[c]
            ok=(pv>lo) and (pv<=hi) and cv>0
            print(t,(lo,hi),X,Y,pv,cv,ok)
