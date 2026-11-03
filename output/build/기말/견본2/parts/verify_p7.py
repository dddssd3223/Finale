# 서답형2 난도 조정판 검증
import sympy as sp, numpy as np, os
x, a = sp.symbols('x alpha', real=True)
f = (x - 3) * (x - a) ** 2
sols = sp.solve(sp.integrate(f, (x, 0, 4)), a); assert set(sols) == {0, sp.Rational(4, 3)}
vals = {al: sp.integrate(sp.Abs(f.subs(a, al)), (x, 0, 4)) for al in sols}
assert vals[0] == sp.Rational(27, 2) and vals[sp.Rational(4, 3)] == sp.Rational(11, 2)
for al in (0, 4 / 3):                       # (가): 범위가 정확히 0<p<3
    for P in np.linspace(-3, 6, 361):
        xs = np.linspace(P, P + 3, 4001); y = (xs - 3) * (xs - al) ** 2
        ne = abs(np.trapezoid(np.abs(y), xs) - abs(np.trapezoid(y, xs))) > 1e-7
        assert ne == (0 < P < 3) or abs(P) < 1e-9 or abs(P - 3) < 1e-9
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
assert len(ns['SITEMS']['S2']['subs']) == 3
print('ALL OK')
