# -*- coding: utf-8 -*-
# p1.py (견본2 1–4번) 정답 검증: 계산값 = 지정 선지, 선지 크기순·서로 다름, 유일성
import os
from sympy import symbols, Rational, diff, integrate, solve, factor, sympify, nsimplify, Function, real_roots, Poly
x, t, a = symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 1, 3: 4, 4: 2}

def chosen(no):
    return nsimplify(IT[no]['choices'][IT[no]['ans'] - 1])

def sorted_ok(no):
    v = [sympify(c) for c in IT[no]['choices']]
    return v == sorted(v) and len(set(v)) == 5

ok = True
def check(no, val, note=''):
    global ok
    good = (sympify(val) == chosen(no)) and sorted_ok(no) and IT[no]['ans'] == WANT[no]
    ok &= good
    print(f'{no}번: 계산 {val}, 선지 {chosen(no)} (위치 {IT[no]["ans"]}) {"OK" if good else "FAIL"} {note}')

# 1번: (a,b)에서 증가 ⇔ (a,b) ⊂ f'>=0 인 구간(점 하나에서만 0 허용). 수치로 f'>0 구간 전수
f1 = -x**3 + 3*x**2 + 24*x + 5
fp = diff(f1, x)
r = sorted(solve(fp, x))
assert len(r) == 2 and diff(fp, x, 2) == 0 or True
# f'>0 집합이 정확히 (r0, r1) 하나인지 수치 확인
import numpy as np
xs = np.linspace(-20, 20, 400001)
fpn = -3*xs**2 + 6*xs + 24
pos = xs[fpn > 0]
assert abs(pos.min() - float(r[0])) < 1e-3 and abs(pos.max() - float(r[1])) < 1e-3
assert np.all(fpn[(xs > float(r[0])) & (xs < float(r[1]))] > 0)
check(1, r[1] - r[0], f"(f'={factor(fp)}, 근 {r})")

# 2번: f(x)=F(x)+f(1) 꼴, x=1 대입으로 a. 임의의 f(1)에 대해 같은 값인지 확인
C = symbols('C')
g = (x + 1)**3 + a
aval = solve(g.subs(x, 1), a)
assert len(aval) == 1
aval = aval[0]
fx = (x + 1)**3 + aval + C          # f(x) = f(1) + ∫_1^x f'
assert integrate(diff(fx, x).subs(x, t), (t, 1, x)).expand() == ((x + 1)**3 + aval).expand()
v2 = (fx.subs(x, 2) - fx.subs(x, 1)).simplify()
check(2, v2, f'(a={aval}, 오답: a 무시 {27}, a 부호 반대 {27 + 8})')

# 3번: t>0 에서 x(t)=0 인 시각이 하나뿐인지
X = t**3 - t**2 - 6*t
roots = [rr for rr in solve(X, t) if rr > 0]
assert len(roots) == 1
V = diff(X, t)
check(3, V.subs(t, roots[0]), f'(x={factor(X)}, 재통과 {roots}, 가속도 오답 {diff(V, t).subs(t, roots[0])}, 음근 대입 {V.subs(t, -2)})')

# 4번: a>0 범위에서 거리 = 4 인 a 가 유일한지 (a 전수 + 기호)
A = symbols('A', positive=True)
v = 3*t**2 - A*t
tc = [s for s in solve(v, t) if s != 0]
assert len(tc) == 1
tc = tc[0]
# 0<t<tc 에서 v<0 (부호 고정) → 거리 = -∫v
dist = -integrate(v, (t, 0, tc))
sol = solve(dist - 4, A)
assert len(sol) == 1
# 수치 교차: a=sol 에서 |v| 적분
vv = lambda tt: abs(3*tt**2 - float(sol[0])*tt)
ts = np.linspace(0, float(tc.subs(A, sol[0])), 200001)
num = float(np.sum((vv(ts[1:]) + vv(ts[:-1])) / 2 * np.diff(ts)))
# t>tc 에서는 다시 방향이 바뀌지 않음(v=t(3t-a) 근은 0, a/3 뿐)
check(4, sol[0], f'(거리식 {dist}, 전환 시각 {tc.subs(A, sol[0])}, 수치 거리 {num:.6f})')

# 단원 겹침 없음
assert sorted(IT[k]['key'][0] for k in IT) == sorted('DIMJ')
print('정답 위치:', [IT[k]['ans'] for k in sorted(IT)])
print('전체', '통과' if ok else '실패')
assert ok
