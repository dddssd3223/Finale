# -*- coding: utf-8 -*-
# p5 (15·16번) 검증: sympy 기호 계산 + 수치 전수 스캔
import os, sys, importlib.util
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p5', os.path.join(HERE, 'p5.py'))
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
IT = P.ITEMS
R = sp.Rational
x, s, A, B = sp.symbols('x s A B', real=True)

# =====================================================================
# 15번 (I64): (가) [0,1] f=x^2+x+2, (나) f(x+1)-(x-1)f(x)=ax+b on [0,inf), f 미분가능
#   답 4*int_1^2 f = 23 (⑤)
# =====================================================================
print('=== 15번 ===')
g = x**2 + x + 2
# [1,2] 조각: f(x) = (x-2) f(x-1) + A(x-1) + B  (x-1 in [0,1])
f12 = sp.expand(((x - 1) - 1) * g.subs(x, x - 1) + A * (x - 1) + B)
# 연속(x=1)과 미분가능(x=1)으로 A, B 결정 -> 유일
sol = sp.solve([sp.Eq(f12.subs(x, 1), g.subs(x, 1)),
                sp.Eq(sp.diff(f12, x).subs(x, 1), sp.diff(g, x).subs(x, 1))], [A, B], dict=True)
assert len(sol) == 1, sol
a, b = sol[0][A], sol[0][B]
print('a, b =', a, b)
assert (a, b) == (2, 6)
f12 = sp.expand(f12.subs({A: a, B: b}))
print('[1,2]에서 f =', sp.factor(f12), '=', sp.expand(f12.subs(x, s + 1)), '(s=x-1)')
# 다음 조각 [2,3]도 만들어 x=2에서 미분가능(자동 연쇄) 확인
f23 = sp.expand((x - 2) * f12.subs(x, x - 1) + a * (x - 1) + b)
assert sp.simplify(f23.subs(x, 2) - f12.subs(x, 2)) == 0
assert sp.simplify(sp.diff(f23, x).subs(x, 2) - sp.diff(f12, x).subs(x, 2)) == 0
# 관계식 점검 (각 조각에서 항등식)
assert sp.expand(f12.subs(x, x + 1) - (x - 1) * g - (a * x + b)) == 0
assert sp.expand(f23.subs(x, x + 1) - (x - 1) * f12 - (a * x + b)) == 0
I = sp.integrate(f12, (x, 1, 2))
print('int_1^2 f =', I, ' -> 4*I =', 4 * I)
assert 4 * I == 23
# 공식 확인: b=f(1)+f(0), a=f'(1)-f(0)+f'(0)
g0, g1 = g.subs(x, 0), g.subs(x, 1)
d0, d1 = sp.diff(g, x).subs(x, 0), sp.diff(g, x).subs(x, 1)
assert b == g1 + g0 and a == d1 - g0 + d0
Iint = sp.integrate((x - 1) * g, (x, 0, 1))
val = lambda aa, bb: 4 * (Iint + R(aa, 2) + bb)
traps = {'원본공식 b=f(1),a=f\'(1)': val(d1, g1), "a=f'(1)-f(0) (f'(0) 누락)": val(d1 - g0, b),
         'b=f(1) (f(0) 누락)': val(a, g1), '곱의 미분 부호 실수 a=f\'(1)-f(0)-f\'(0)': val(d1 - g0 - d0, b)}
print('오답 값:', traps)
# 15번은 질문을 60×∫_1^3 으로 바꾼 수정본(답 1077)으로 교체됨 → 선지·정답 대조는 verify_p5_15.py
print('15번 정답 ⑤ = 23 확인')

# =====================================================================
# 16번 (J70): v=t(t-1)(at+b), a!=0, int_0^1|v|=2, x(0)=0
#   ㄱ |x(1)|<2 거짓, ㄴ x(1)=0 -> max-min=1 참, ㄷ exists t1 in (0,1), |x(t1)|>=2/3 참  -> ④
# =====================================================================
print('=== 16번 ===')
t = sp.symbols('t', real=True)
a_, b_ = sp.symbols('a b', real=True)
v = t * (t - 1) * (a_ * t + b_)
X = sp.integrate(v, (t, 0, t))
assert sp.simplify(X.subs(t, 1) - (-a_ / 12 - b_ / 6)) == 0

def dist_exact(av, bv):
    vv = v.subs({a_: av, b_: bv})
    pts = sorted({0, 1} | {r for r in sp.solve(vv, t) if r.is_real and 0 < r < 1})
    return sum(abs(sp.integrate(vv, (t, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))

# ㄱ 반례: b=0, a=24
assert dist_exact(24, 0) == 2
x1 = X.subs({a_: 24, b_: 0, t: 1})
print('ㄱ 반례 a=24,b=0: 거리', dist_exact(24, 0), ', x(1) =', x1)
assert abs(x1) == 2
# ㄴ: x(1)=0 <=> b=-a/2, 거리 2 <=> |a|=64, 이때 x=(a/4)(t(t-1))^2
for av in [64, -64]:
    bv = -R(av, 2)
    assert dist_exact(av, bv) == 2
    xx = sp.expand(X.subs({a_: av, b_: bv}))
    assert sp.expand(xx - R(av, 4) * (t * (t - 1))**2) == 0
    vals = [xx.subs(t, 0), xx.subs(t, R(1, 2)), xx.subs(t, 1)]
    print('ㄴ a=%d: x(0),x(1/2),x(1) =' % av, vals, ' max-min =', max(vals) - min(vals))
    assert max(vals) - min(vals) == 1
# x(1)=0 이면 b=-a/2 뿐 (유일)
assert sp.solve(sp.Eq(-a_ / 12 - b_ / 6, 0), b_) == [-a_ / 2]

# 수치 전수 스캔: (a,b) 방향을 각도로 훑고 거리 2가 되게 크기 조정 (거리는 (a,b)에 대해 1차 동차)
tt = np.linspace(0, 1, 20001)
def scan(theta):
    ca, cb = np.cos(theta), np.sin(theta)
    if abs(ca) < 1e-12:
        return None
    vv = tt * (tt - 1) * (ca * tt + cb)
    # 누적 적분 (사다리꼴)
    xx = np.concatenate([[0], np.cumsum((vv[1:] + vv[:-1]) / 2 * np.diff(tt))])
    D = np.sum((np.abs(vv[1:]) + np.abs(vv[:-1])) / 2 * np.diff(tt))
    k = 2 / D
    xx = xx * k
    turns = np.sum(np.diff(np.sign(vv[1:-1])) != 0)
    return xx, turns
min_max = 9; worst = None; max_turns = 0; ok_g = False
for th in np.linspace(0, 2 * np.pi, 7201, endpoint=False):
    r = scan(th)
    if r is None:
        continue
    xx, turns = r
    max_turns = max(max_turns, turns)
    m = np.max(np.abs(xx[1:-1]))
    if m < min_max:
        min_max, worst = m, th
    assert abs(xx[-1]) <= 2 + 1e-6
    if abs(abs(xx[-1]) - 2) < 1e-6:
        ok_g = True
print('방향 전환 최대 횟수:', max_turns)
assert max_turns <= 1
print('ㄱ: |x(1)|=2 인 경우 수치로도 존재:', ok_g)
assert ok_g
print('ㄷ: 모든 (a,b)에서 max_(0,1)|x| 의 최솟값 ≈ %.6f (2/3=%.6f)' % (min_max, 2 / 3))
assert min_max >= 2 / 3 - 1e-3 and min_max < 2 / 3 + 5e-3   # 2/3 이 최솟값(등호 가능)
# 판정 → ㄴ, ㄷ = ④
truth = {'ㄱ': False, 'ㄴ': True, 'ㄷ': True}
pick = 'T:' + ', '.join(k for k in 'ㄱㄴㄷ' if truth[k])
assert IT[16]['choices'].index(pick) + 1 == IT[16]['ans'] == 4
print('16번 정답 ④ (ㄴ, ㄷ) 확인')
print('ALL OK')
