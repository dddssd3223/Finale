# -*- coding: utf-8 -*-
# 서답형1 (q4.py S1) 검증: 구간별 도함수 적분, 연속 조건으로 a 결정, x=1 미분가능성 판정
import os, sympy as sp

x, h, a, C1, C2 = sp.symbols('x h a C1 C2')
fpL = 3*x**2 - 6*x + a          # x<1
fpR = 2*x - 4                   # x>1

# 구간별 부정적분 (적분상수 따로)
fL = sp.integrate(fpL, x) + C1
fR = sp.integrate(fpR, x) + C2
assert sp.expand(sp.diff(fL, x) - fpL) == 0 and sp.expand(sp.diff(fR, x) - fpR) == 0

# 조건: f(0)=0 (0<1 → 왼쪽 식), f(3)=0 (3>1 → 오른쪽 식), x=1 연속
eqs = [sp.Eq(fL.subs(x, 0), 0), sp.Eq(fR.subs(x, 3), 0), sp.Eq(fL.subs(x, 1), fR.subs(x, 1))]
sol = sp.solve(eqs, [a, C1, C2], dict=True)
assert len(sol) == 1, sol                       # 선형계 → 해 유일
s = sol[0]
assert s == {a: 2, C1: 0, C2: 3}, s
# 계수행렬 랭크 3 (유일성 재확인)
M, _ = sp.linear_eq_to_matrix([e.lhs - e.rhs for e in eqs], [a, C1, C2])
assert M.rank() == 3

FL = sp.expand(fL.subs(s)); FR = sp.expand(fR.subs(s))
assert FL == x**3 - 3*x**2 + 2*x and FR == x**2 - 4*x + 3
f1 = FR.subs(x, 1)
assert f1 == 0 and FL.subs(x, 1) == 0
print('(1) a =', s[a], ', f(1) =', f1)

# (2) 미분계수의 정의: 좌우 차분몫
qL = sp.simplify((FL.subs(x, 1 + h) - f1) / h)
qR = sp.simplify((FR.subs(x, 1 + h) - f1) / h)
assert sp.expand(qL - (h**2 - 1)) == 0 and sp.expand(qR - (h - 2)) == 0
dL = sp.limit(qL, h, 0, '-'); dR = sp.limit(qR, h, 0, '+')
assert dL == -1 and dR == -2 and dL != dR
print('(2) 좌미분계수', dL, ', 우미분계수', dR, '→ x=1에서 미분가능하지 않다')

# 수치 확인 (조각 함수 직접 정의)
def f(t):
    return float(FL.subs(x, t)) if t < 1 else float(FR.subs(x, t))
for hh in (1e-3, 1e-5):
    assert abs((f(1 - hh) - f(1)) / (-hh) - (-1)) < 1e-2
    assert abs((f(1 + hh) - f(1)) / hh - (-2)) < 1e-2
assert abs(f(0)) < 1e-12 and abs(f(3)) < 1e-12
# x≠1에서 도함수 일치 확인
for t in (-2, 0.3, 0.9, 1.1, 2, 5):
    expr = (fpL if t < 1 else fpR).subs(a, 2)
    g = FL if t < 1 else FR
    assert sp.diff(g, x).subs(x, t) == expr.subs(x, t)

# 오답 설계 확인: 기울기 식을 같게 놓으면 a=1 → 연속 조건 위반
a_wrong = sp.solve(sp.Eq(fpL.subs(x, 1), fpR.subs(x, 1)), a)
assert a_wrong == [1]
fLw = fL.subs({a: 1, C1: 0}); fRw = fR.subs(C2, 3)
assert fLw.subs(x, 1) != fRw.subs(x, 1)        # -1 ≠ 0: 불연속
print('오답 a=1: 왼쪽 극한', fLw.subs(x, 1), '≠ 오른쪽 극한', fRw.subs(x, 1))
# 적분상수 하나로 통일한 오답: f(0)=0, f(3)=0 모두 왼쪽식이라 보면 27-27+3a=0 → a=0
a_wrong2 = sp.solve(sp.Eq(fL.subs({C1: 0, x: 3}), 0), a)
assert a_wrong2 == [0]

# 배점 합 확인
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q4.py'), encoding='utf-8').read(), ns)
import re
S1 = ns['SITEMS']['S1']
pts = [sum(int(p) for p in re.findall(r'\[(\d)점\]', r.split('(정의식 없이')[0].split('(적분상수를')[0])) for r in S1['rubric']]
assert pts == [4, 6], pts
assert [int(p[1][0]) for p in S1['subs']] == [4, 6]
print('배점', pts, '— 모든 검증 통과')
