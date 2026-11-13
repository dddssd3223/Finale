import sympy as sp
x=sp.symbols('x')
vals=[]
for A in range(-40,41):
  for B in range(-80,81):
    f=sp.Poly(x**3+A*x**2+B*x-5,x)
    rs=sp.roots(f,multiple=False) if False else None
    fx=f.as_expr(); num=sp.Poly(fx.subs(x,-2*x+3),x)
    ok=True
    for r,m in sp.polys.polyroots.roots(f).items() if False else []: pass
    # real roots with multiplicity via factor
    for fac,m in sp.factor_list(fx)[1]:
        P=sp.Poly(fac,x)
        if P.degree()==1:
            r=sp.solve(fac,x)[0]
            # multiplicity of r in numerator
            mm=0; g=num
            while g.eval(r)==0: g=sp.Poly(sp.quo(g.as_expr(),x-r),x); mm+=1
            if mm<m: ok=False;break
        elif P.degree()>=2:
            disc=sp.discriminant(P) if P.degree()==2 else None
            if P.degree()==2 and disc>=0: ok=None  # irrational real roots: check numerically
            if P.degree()==3: ok=None
    if ok is None:
        for r in sp.Poly(fx,x).real_roots():
            if abs(sp.N(fx.subs(x,-2*r+3)))>1e-9: ok=False;break
        else: ok='?'
    if ok: vals.append((A,B,fx.subs(x,2),ok))
print(vals); f2=[v[2] for v in vals]; print(max(f2),min(f2),max(f2)+min(f2))
