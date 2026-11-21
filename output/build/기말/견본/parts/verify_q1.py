# -*- coding: utf-8 -*-
"""q1.py (3·5·6·7번) 정답 검증"""
import os, sympy as sp, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'q1.py'), encoding='utf-8').read(), ns); IT = ns['ITEMS']
x, t, a, b = sp.symbols('x t a b', real=True)
EXPECT_POS = {3: 1, 5: 4, 6: 2, 7: 5}

def chk(no, val):
    it = IT[no]
    ch = [sp.nsimplify(c.replace(r'\dfrac', '')) for c in it['choices']]
    assert ch == sorted(ch), (no, '선지 정렬')
    assert len(set(ch)) == 5, (no, '선지 중복')
    assert it['ans'] == EXPECT_POS[no], (no, '지정 정답 위치')
    assert sp.simplify(ch[it['ans'] - 1] - val) == 0, (no, ch, val)
    print(f'{no}번 OK: 정답 {val} = 선지 {it["ans"]}')

# 3번: t>0에서 만나는 시각 전수, p-q
x1 = 2*t**3 - 3*t**2; x2 = t**2 + 6*t
meet = [r for r in sp.solve(x1 - x2, t) if r.is_real and r > 0]
assert meet == [3], meet
p = sp.diff(x1, t).subs(t, 3); q = sp.diff(x2, t).subs(t, 3)
assert (p, q) == (36, 12)
chk(3, p - q)
assert p in [sp.nsimplify(c) for c in IT[3]['choices']] and p + q in [sp.nsimplify(c) for c in IT[3]['choices']]  # 함정 값 포함

# 5번: 0<a<=4 전 범위에서 구간 [-a/2,a/2]의 최솟값이 2인 a를 전수(수치) + 기호 확인
f5 = -x**4 + 4*x**3 + 20*x**2 + a
def ext(av):
    av = sp.nsimplify(av); g = f5.subs(a, av)
    cands = [-av/2, av/2] + [r for r in sp.solve(sp.diff(g, x), x) if -av/2 <= r <= av/2]
    vals = [g.subs(x, c) for c in cands]
    return min(vals), max(vals)
# 최솟값이 항상 f(0)=a 인지 격자 확인
fl = sp.lambdify((x, a), f5)
for av in np.linspace(0.01, 4, 400):
    xs = np.linspace(-av/2, av/2, 4001)
    assert abs(fl(xs, av).min() - av) < 1e-9
sols = [s for s in sp.solve(sp.Eq(a, 2), a) if 0 < s <= 4]
assert sols == [2]
m5, M5 = ext(2)
assert (m5, M5) == (2, 25)
chk(5, M5 + 2)

# 6번: a 결정(극소 확인), B, D 전수
f6 = 2*x**3 - sp.Symbol('A')*x**2 + 8*x + 1
As = sp.solve(sp.diff(f6, x).subs(x, 2), sp.Symbol('A'))
assert As == [8]
f6 = f6.subs(sp.Symbol('A'), 8)
assert sp.diff(f6, x, 2).subs(x, 2) > 0          # 극소
A_ = (2, f6.subs(x, 2))
tA = f6.subs(x, 2) + sp.diff(f6, x).subs(x, 2)*(x - 2)
Bx = [r for r in sp.solve(f6 - tA, x) if r != 2]; assert Bx == [0]
B_ = (0, f6.subs(x, 0))
tB = B_[1] + sp.diff(f6, x).subs(x, 0)*x
Dx = [r for r in sp.solve(f6 - tB, x) if r != 0]; assert Dx == [4]
D_ = (4, f6.subs(x, 4)); assert D_ == (4, 33)
area = sp.Abs(sp.Matrix([[A_[0]-B_[0], A_[1]-B_[1]], [D_[0]-B_[0], D_[1]-B_[1]]]).det())/2
chk(6, area)

# 7번: 극한 존재 + 극한값 → (a,b) 유일, 수치 극한 확인
F7 = sp.integrate(t*(a*t**2 + b), (t, 1, x))
sol = sp.solve([F7.subs(x, 2), sp.diff(F7, x).subs(x, 2) - 12], [a, b], dict=True)
assert sol == [{a: 4, b: -10}], sol
F7n = F7.subs(sol[0])
assert sp.limit(F7n/(x - 2), x, 2) == 12
f7 = (a*x**2 + b).subs(sol[0])
# 함정: 아래끝 0
F0 = sp.integrate(t*(a*t**2 + b), (t, 0, x))
s0 = sp.solve([F0.subs(x, 2), sp.diff(F0, x).subs(x, 2) - 12], [a, b], dict=True)[0]
assert (a*9 + b).subs(s0) == 21
chk(7, f7.subs(x, 3))
print('전체 통과')
