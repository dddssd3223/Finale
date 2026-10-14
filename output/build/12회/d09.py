import itertools, numpy as np
from fractions import Fraction as Fr
def run(R,A,show=True):
    res=[]
    for w2 in range(-60,61):
        w=w2/4
        f=lambda x: x + x*x*(x-R)*(x-w)
        roots=sorted(set([0,R,w]))
        nint=len(roots)+1
        for asg in itertools.product([0,1],repeat=nint):
            def g(x):
                i=sum(1 for r in roots if x>r)  # interval index (x on root -> lower interval; values agree there)
                return f(x) if asg[i] else x
            # (가): non-differentiable at R
            e=1e-6
            dl=(g(R)-g(R-e))/e; dr=(g(R+e)-g(R))/e
            if abs(dl-dr)<1e-3: continue
            xs=np.arange(0,12.0001,0.005)
            bad=[x for x in xs if abs(g(-x)+g(x))>1e-9]
            # also need oddness for all large x (beyond 12): asg of last and first intervals both 'x'
            if not (asg[0]==0 and asg[-1]==0): continue
            amin=max(bad) if bad else -1
            if abs(amin-(A-0.005))<1e-9 and abs(g(-A)+g(A))<1e-9:
                res.append((w,asg,g(-2),g(2),g(-3),g(3),g(-1),g(4) if True else 0))
    return res
if __name__=='__main__':
    for r in run(2,4): print(r)
    print('---')
    for r in run(1,3): print(r)
