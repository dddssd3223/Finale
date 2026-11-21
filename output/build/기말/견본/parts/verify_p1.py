# -*- coding: utf-8 -*-
# p1.py (1–4번) 정답 검증
import os
from sympy import symbols, Rational, diff, integrate, solve, factor, Poly, real_roots, sympify, nsimplify
x, t, a = symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']

def chosen(no):
    c = IT[no]['choices'][IT[no]['ans'] - 1]
    return nsimplify(c.replace(r'\dfrac', '').replace('{', '').replace('}', ''))

def sorted_ok(no):
    v = [sympify(c) for c in IT[no]['choices']]
    return v == sorted(v) and len(set(v)) == 5

ok = True
def check(no, val, note=''):
    global ok
    good = (sympify(val) == chosen(no)) and sorted_ok(no)
    ok &= good
    print(f'{no}번: 계산 {val}, 선지 {chosen(no)} (위치 {IT[no]["ans"]}) {"OK" if good else "FAIL"} {note}')

# 1번: f'(x)>=0 for all x  (전수: 정수 a를 넓게 훑어 f'의 최솟값 >= 0 확인, 등호 경계 포함)
cnt = []
for A in range(-50, 51):
    fp = 3*x**2 + 2*A*x + A + Rational(10, 3)
    xm = -Rational(A, 3)
    if fp.subs(x, xm) >= 0:
        cnt.append(A)
print('  1번 정수 a:', cnt, ' D/4 =', factor(a**2 - 3*(a + Rational(10, 3))))
# 경계 a=-2, 5에서 f'는 완전제곱 → 증가(한 점에서만 0)
for A in (-2, 5):
    print('   a=', A, "f' =", factor(3*x**2 + 2*A*x + A + Rational(10, 3)))
check(1, len(cnt))

# 2번
v2 = integrate(3*x**2 + x, (x, -1, 1)) + integrate(3*x - 1, (x, 1, -1)) + integrate(3*x**2 - 2*x + 1, (x, 1, 2))
wrong2 = integrate(3*x**2 + x, (x, -1, 1)) + integrate(3*x - 1, (x, -1, 1)) + integrate(3*x**2 - 2*x + 1, (x, 1, 2))
check(2, v2, f'(부호 누락 오답 {wrong2})')

# 3번: v의 t>0 부호 변화 근 전수
X = 2*t**3 - 3*t**2 - 36*t
V = diff(X, t); Acc = diff(V, t)
rts = [r for r in solve(V, t) if r > 0]
turn = [r for r in rts if V.subs(t, r - Rational(1, 100)) * V.subs(t, r + Rational(1, 100)) < 0]
assert len(turn) == 1 and V.subs(t, 0) != 0
check(3, Acc.subs(t, turn[0]), f'(전환 시각 {turn}, v={factor(V)})')

# 4번
f = x**3 - 4*x**2 + 5*x; g = 2*x**2 - 3*x
h = f - g
pts = sorted(solve(h, x))
area = sum(abs(integrate(h, (x, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))
# 수치 교차 검증
import numpy as np
xs = np.linspace(float(pts[0]), float(pts[-1]), 400001)
hn = np.abs(xs**3 - 6*xs**2 + 8*xs)
num = float(np.sum((hn[1:] + hn[:-1]) / 2 * np.diff(xs)))
check(4, area, f'(교점 {pts}, 수치 {num:.6f}, 전구간 ∫ {integrate(h, (x, pts[0], pts[-1]))})')

print('정답 위치:', [IT[k]['ans'] for k in sorted(IT)])
print('전체', '통과' if ok else '실패')
assert ok
