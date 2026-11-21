# -*- coding: utf-8 -*-
"""p2.py (5–8번) 정답 검증"""
import os, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p2.py'), encoding='utf-8').read(), ns); IT = ns['ITEMS']
x, t, y = sp.symbols('x t y', real=True)

def chk(no, val):
    it = IT[no]
    ch = [sp.nsimplify(c.replace(r'\dfrac', '')) for c in it['choices']]
    assert ch == sorted(ch), (no, '선지 정렬')
    assert len(set(ch)) == 5, (no, '선지 중복')
    assert sp.simplify(ch[it['ans'] - 1] - val) == 0, (no, ch, val)
    print(f'{no}번 OK: 정답 {val} = 선지 {it["ans"]}')

# 5번: 0<=t<=4에서 |x1-x2|의 최댓값
x1 = 2*t**3 - t**2 - 5*t; x2 = 2*t**2 + 7*t; D = sp.expand(x1 - x2)
crit = [r for r in sp.solve(sp.diff(D, t), t) if 0 <= r <= 4]
assert crit == [2]
cands = {c: abs(D.subs(t, c)) for c in [0, 4] + crit}
M5 = max(cands.values())
import numpy as np
grid = np.linspace(0, 4, 400001); fD = sp.lambdify(t, D)
assert abs(np.max(np.abs(fD(grid))) - float(M5)) < 1e-6
assert abs(D.subs(t, 2)) == 20 and D.subs(t, -1) == 7   # 함정 값 확인
chk(5, M5)

# 6번: f를 일반 5차 다항식으로 두고 항등식으로 결정 → F가 x축에 접하는 모든 경우
cs = sp.symbols('c0:6'); K = sp.Symbol('K')
f = sum(cs[i] * x**i for i in range(6))
F = sp.integrate(f, x) + K
eqs = sp.Poly(sp.expand(F - (x*f - 2*x**3 + 4*x**2)), x).coeffs()
sol = sp.solve(eqs, list(cs[1:]) + [K], dict=True)
assert len(sol) == 1
fS = f.subs(sol[0]); FS = sp.expand(F.subs(sol[0]))
C = cs[0]
assert sp.expand(fS - (3*x**2 - 8*x + C)) == 0
assert sp.expand(FS - x*(x**2 - 4*x + C)) == 0
# 접함 ⇔ F와 F'의 공통 실근 존재: 종결식 = 0
res = sp.resultant(FS, sp.diff(FS, x), x)
Cs = sorted(set(sp.solve(res, C)))
assert all(c.is_real for c in Cs)
ok = []
for c in Cs:
    Fc = FS.subs(C, c)
    common = [r for r in sp.solve(sp.gcd(Fc, sp.diff(Fc, x)), x) if r.is_real]
    if common: ok.append(c)
assert ok == [0, 4], ok
chk(6, sum(fS.subs({C: c, x: 1}) for c in ok))

# 7번: 평균값 정리 상·하한 + 등호 달성 함수(미분가능, f'<=3) 확인
lo = 14 - 3*(7 - 4); hi = 2 + 3*(4 - 1)
pw_max = sp.Piecewise((3*x - 1, x <= 4), (11 + 3*(x - 4) - sp.Rational(2, 3)*(x - 4)**2, True))
pw_min = sp.Piecewise((5 + 3*(x - 4) + sp.Rational(2, 3)*(x - 4)**2, x <= 4), (3*x - 7, True))
for g, v in [(pw_max, hi), (pw_min, lo)]:
    L, R = g.args[0][0], g.args[1][0]
    assert L.subs(x, 4) == R.subs(x, 4) and sp.diff(L, x).subs(x, 4) == sp.diff(R, x).subs(x, 4)  # 이음점 미분가능
    assert g.subs(x, 1) == 2 and g.subs(x, 7) == 14 and g.subs(x, 4) == v
    for seg, a, b in [(L, 1, 4), (R, 4, 7)]:
        d = sp.diff(seg, x)
        assert sp.maximum(d, x, sp.Interval(a, b)) <= 3
chk(7, hi + lo)

# 8번: g 넓이 = 12*2 - ∫_0^2 f, 수치 적분(g를 수치로 구해 직접 적분)으로 대조
f8 = x**3 + 2*x
assert sp.solve(sp.Eq(f8, 12), x) and [r for r in sp.solve(f8 - 12, x) if r.is_real] == [2]
assert sp.solveset(sp.diff(f8, x) <= 0, x, sp.S.Reals) == sp.S.EmptySet  # 증가함수
A = 12*2 - sp.integrate(f8, (x, 0, 2))
X = np.linspace(0, 12, 200001); a_, b_ = np.zeros_like(X), np.full_like(X, 3.0)
for _ in range(80):  # 이분법으로 g(X) 수치 계산
    m_ = (a_ + b_) / 2; big = m_**3 + 2*m_ > X; b_ = np.where(big, m_, b_); a_ = np.where(big, a_, m_)
G = (a_ + b_) / 2
An = np.sum((G[1:] + G[:-1]) / 2 * np.diff(X))
assert abs(An - float(A)) < 1e-6, An
chk(8, A)
print('검증 통과')
