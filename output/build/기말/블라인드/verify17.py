# -*- coding: utf-8 -*-
"""17번 검증 (원문 L42 변형).
f: 원문 그래프 그대로 (x<0: (x+3)(x-3)/9, 0<=x<1: 삼차 조각(f(0)=1, x->1- 에서 0, [0,1)에서 양수), x>=1: -x+3)
g: 최고차항의 계수가 -1인 이차함수 g(x) = -(x-p)^2 + M,  h(x) = f(g(x))
(가) h(x)가 불연속인 실수 x의 개수는 3   (나) h(1) = 0   ->  g(3)의 최댓값 = 1
"""
import sympy as sp
from fractions import Fraction

x, t, p, M = sp.symbols('x t p M', real=True)

# ---- 원문 L42 확인 (정답 12) ---------------------------------------------
cub0 = x**3 - 2*x**2 + 1          # 그림과 맞는 삼차 조각 하나: (x-1)(x^2-x-1), f(0)=1, f(1)=0
# 원문: g/f 극한 존재 -> g(0)=0 (x=0 점프), g(1)=0 이고 (x-1)^2 인수 (x=1- 에서 f->0, 우극한 0)
gL = x*(x-1)**2
assert sp.limit(gL/((x**2-9)/9), x, 0, '-') == sp.limit(gL/cub0, x, 0, '+')
assert sp.limit(gL/cub0, x, 1, '-') == sp.limit(gL/(-x+3), x, 1, '+') == 0
assert gL.subs(x, 3) == 12
print('원문 L42: g(x)=x(x-1)^2, g(3)=12 확인')

# ---- 변형 문항의 f (삼차 조각 두 가지로 확인: 답이 조각 모양에 무관함) ------------
def make_f(cub):
    def f(u):
        return sp.Piecewise(((u**2 - 9)/9, u < 0), (cub.subs(x, u), u < 1), (-u + 3, True))
    return f

cubics = [cub0, sp.expand((x-1)*(x**2 - sp.Rational(1, 2)*x - 1))]
for cub in cubics:   # 두 삼차 모두 [0,1)에서 양수, f(0)=1, f(1-)=0
    assert cub.subs(x, 0) == 1 and cub.subs(x, 1) == 0
    assert all(cub.subs(x, sp.Rational(k, 100)) > 0 for k in range(100))

def disc_points(f, pv, Mv):
    """h=f(g)의 불연속점: g=0, g=1 인 점만 후보 (f는 0, 1에서만 불연속, 나머지 연속)."""
    g = -(x - pv)**2 + Mv
    cand = set()
    for c in (0, 1):
        for r in sp.solve(sp.Eq(g, c), x):
            if r.is_real:
                cand.add(sp.nsimplify(r))
    out = []
    eps = sp.Rational(1, 10**6)
    for r in sorted(cand, key=lambda v: float(v)):
        h = lambda xv: f(g.subs(x, xv))
        hl = sp.N(h(r - eps)); hr = sp.N(h(r + eps)); hv = sp.N(h(r))
        if abs(hl - hv) > 1e-3 or abs(hr - hv) > 1e-3:
            out.append(r)
    return out

# ---- (가) 경우 분기: 최댓값 M에 따른 불연속점 개수 ---------------------------
cases = [(-1, 'M<0'), (0, 'M=0 (꼭짓점이 y=0에 아래에서 접함)'), (sp.Rational(1, 2), '0<M<1'),
         (1, 'M=1 (꼭짓점이 y=1에 아래에서 접함)'), (2, 'M>1')]
table = {}
for cub in cubics:
    f = make_f(cub)
    for pv in (0, sp.Rational(3, 2), 3, -1):
        for Mv, name in cases:
            n = len(disc_points(f, pv, Mv))
            table.setdefault(name, set()).add(n)
for name, s in table.items():
    print(f'  {name:32s} -> 불연속점 개수 {sorted(s)}')
assert [sorted(table[n])[0] for _, n in cases] == [0, 1, 2, 3, 4]
assert all(len(s) == 1 for s in table.values())
# 개수 3은 M=1에서만 (조밀 표본으로도 확인)
f = make_f(cub0)
for k in range(-20, 41):
    Mv = sp.Rational(k, 10)
    n = len(disc_points(f, 0, Mv))
    assert (n == 3) == (Mv == 1), (Mv, n)
print('(가) 불연속점 3개 <=> M=1 (5가지 경우: 0,1,2,3,4개)')

# M=1 꼭짓점의 경계 함정: 극한은 존재(0)하지만 함숫값 2와 다름 -> 불연속
pv = 3; g1 = -(x - pv)**2 + 1
assert sp.N(f(g1.subs(x, pv + sp.Rational(1, 10**6)))) < 1e-3 and f(g1.subs(x, pv)) == 2

# ---- (나) h(1)=0 -> g(1)=-3 ------------------------------------------------
# f(t)=0 의 해: x<0 조각 t=-3, x>=1 조각 t=3, 삼차 조각은 [0,1)에서 양수 -> 해 없음, (1,0)은 빈 점
sol_t = []
for cub in cubics:
    s = set(sp.solve(sp.Eq((t**2 - 9)/9, 0), t)) & {r for r in sp.solve(sp.Eq((t**2-9)/9, 0), t) if r < 0}
    s |= {r for r in sp.solve(sp.Eq(-t + 3, 0), t) if r >= 1}
    s |= {r for r in sp.solve(sp.Eq(cub.subs(x, t), 0), t) if r.is_real and 0 <= r < 1}
    sol_t.append(s)
assert sol_t[0] == sol_t[1] == {-3, 3}
# M=1 이므로 g(1) <= 1 -> g(1) = -3  (t=3 불가)
ps = sp.solve(sp.Eq(-(1 - p)**2 + 1, -3), p)
assert set(ps) == {-1, 3}
vals = {}
for pv in ps:
    g = -(x - pv)**2 + 1
    for cub in cubics:
        fc = make_f(cub)
        assert len(disc_points(fc, pv, 1)) == 3
        assert fc(g.subs(x, 1)) == 0
    vals[pv] = g.subs(x, 3)
print('(나) 후보 g(x)=-(x-3)^2+1, -(x+1)^2+1 ->  g(3) =', vals)
ans = max(vals.values()); assert ans == 1

# ---- 오답 근거 ---------------------------------------------------------------
wrong = {}
# 빈 점 (1,0)을 그래프 위 점으로 읽음: g(1)=1 -> p=1
pw = sp.solve(sp.Eq(-(1 - p)**2 + 1, 1), p); assert pw == [1]
gw = -(x - 1)**2 + 1
wrong['빈 점 (1,0)을 f(1)=0으로 읽음 (실제 h(1)=f(1)=2)'] = gw.subs(x, 3)
assert f(gw.subs(x, 1)) == 2
# 최댓값 대신 다른 후보(최솟값)
wrong['p=-1 후보 (최솟값)'] = vals[-1]
# 경계 함정: 꼭짓점(y=1에 접함)을 연속으로 보면 M=1에서 2개 -> 3개가 되는 M 없음 (막힘), M을 0으로 오인시 무리수
print('오답 근거:', wrong)

choices = [-15, -11, -7, -3, 1]
d = [choices[i+1] - choices[i] for i in range(4)]
assert len(set(d)) == 1, '선지 등차 아님'
assert choices.count(ans) == 1
assert all(v in choices for v in wrong.values())
print('선지', choices, '공차', d[0], '정답 번호', choices.index(ans) + 1)
print('ALL PASS')
