from sympy import *
x,P=symbols('x p',real=True)
def solve_case(d,cc,show=False):
    # f=k x(x-d)(x-p), k>0 ; denominator x(x-d)
    out=[]
    F=x*(x-d)*(x-P)
    for tch in ['0','d','p']:
        # region partition points for p
        pts=sorted(set([Rational(n,1) for n in range(-12,25)]+[Rational(2*n+1,2) for n in range(-12,25)]))
        cands=set()
        # sample p values between integers & at integers
        samples=[Rational(n,1) for n in range(-10,22)]+[Rational(2*n+1,2) for n in range(-10,22)]
        for pv in samples:
            t={'0':0,'d':d,'p':pv}[tch]
            f=F.subs(P,pv)
            def g(xx,side=0):
                return -f.subs(x,xx) if xx<t or (xx==t and side<0) else f.subs(x,xx)
            S=[]
            for m in range(1,40):
                # right limit of g/(x(x-d)) at m
                gm=f if m>=t else -f
                L=limit(gm/(x*(x-d)),x,m,'+')
                if L.is_number and L<0: S.append(m)
            if len(S)!=2: continue
            # g(-1), g(1) as functions of p (symbolic) in same configuration
            gsym=lambda xx: (-F if xx< {'0':0,'d':d,'p':P}[tch] else F).subs(x,xx)
            # careful: comparison with symbolic p ; use pv for branch
            A=(-F if -1<t else F).subs(x,-1)
            B=cc*((-F if 1<t else F).subs(x,1))
            cands.add((tuple(S),A,B,pv))
        # for each S, solve k*A=s_i, k*B=s_j with p in the region giving same S and branch
        for S,A,B,pv in cands:
            for s1,s2 in [(S[0],S[1]),(S[1],S[0])]:
                for sol in solve(Eq(A*s2,B*s1),P):
                    if not sol.is_real: continue
                    # check sol gives same S and branch
                    out.append((tch,S,sol,s1,s2,A,B))
    # verify each solution fully
    res=set()
    for tch,S,pv,s1,s2,A,B in out:
        t={'0':0,'d':d,'p':pv}[tch]
        Av=A.subs(P,pv); 
        if Av==0: continue
        k=s1/Av
        if k<=0: continue
        f=k*F.subs(P,pv)
        gm=lambda xx: (-f if xx<t else f)
        Sv=[m for m in range(1,60) if (lambda L: L.is_number and L<0)(limit(gm(m)/(x*(x-d)),x,m,'+'))]
        g_1=gm(-1).subs(x,-1); g1=gm(1).subs(x,1)
        if sorted([g_1,cc*g1])==Sv and g_1!=cc*g1:
            res.add((tch,pv,k,tuple(Sv)))
    return res
if __name__=='__main__':
    print(solve_case(2,Rational(-7,2)))
