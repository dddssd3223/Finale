from fractions import Fraction as Fr
def F(x,a): return x+4 if x<4 else abs(2*x-a)
def h(x,a,b): return F(x,a)*(x-4)*(x-b)
def diffable(a,b):
    pts=[4]+([Fr(a,2)] if Fr(a,2)>=4 else [])
    e=Fr(1,10**7)
    for p in pts:
        l=(h(p,a,b)-h(p-e,a,b))/e; r=(h(p+e,a,b)-h(p,a,b))/e
        if abs(l-r)>Fr(1,1000): return False
    return True
pairs=[(a,b) for a in range(1,200) for b in range(1,200) if diffable(a,b)]
print(len(pairs)); print([p for p in pairs if p[1]!=4]); print(sorted(set(a for a,b in pairs if b==4)))
