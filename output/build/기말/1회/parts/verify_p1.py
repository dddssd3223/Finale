# -*- coding: utf-8 -*-
# p1.py (1회 Claude 1·3·5·7번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·오름차순·서로 다름 · 오답 값이 선지에 있음 · 조건 빼 보기
import os
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Function, Poly, real_roots
x, t, a, C = symbols('x t a C', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 3: 1, 5: 2, 7: 3}
assert sorted(IT) == [1, 3, 5, 7] and all(IT[n]['author'] == 'claude' for n in IT)
assert [IT[n]['key'] for n in (1, 3, 5, 7)] == ['I18', 'I4', 'I17', 'M29']
for n in IT:
    assert IT[n]['bunseok'] is False and IT[n]['effect'] in ('같음', '쉬워짐') and IT[n]['precedent']
    assert '함정 추가' not in IT[n]['vtype'] and 1 <= len(IT[n]['vtype']) <= 3

def cv(c):
    c = str(c).replace(r'\dfrac{11}2', '11/2').replace(r'\dfrac{13}2', '13/2')
    return nsimplify(c)

def arith_up(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] > 0

def chk(no, val, wrongs=()):
    ch = [cv(c) for c in IT[no]['choices']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith_up(no)
            and all(nsimplify(w) in ch and nsimplify(w) != nsimplify(val) for w in wrongs))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {list(wrongs)} {"OK" if good else "FAIL"}')
    assert good

def tangent_count(curve, s, av):
    """점 (s, av)에서 곡선 y=curve(x)에 그은 서로 다른 접선의 개수 (접점 t의 서로 다른 실근 수; 삼차곡선은 접점이 다르면 접선이 다름)"""
    h = expand(curve.subs(x, t) + diff(curve, x).subs(x, t) * (s - t))
    roots = set(real_roots(Poly(h - av, t)))
    # 접점이 다르면 접선이 다름을 직접 확인 (기울기·절편 쌍이 서로 다름)
    lines = {(diff(curve, x).subs(x, r), expand(curve.subs(x, r) - diff(curve, x).subs(x, r) * r)) for r in roots}
    assert len(lines) == len(roots)
    return len(roots), h

def discont_points(curve, s, lo=-20, hi=20):
    """개수 함수가 불연속인 a: 후보(극값)에서 좌·우와 값이 다르고, 그 밖의 유리수 격자에서는 이웃과 같음을 전수 확인"""
    _, h = tangent_count(curve, s, 0)
    crit = [r for r in solve(diff(h, t), t) if r.is_real]
    cand = sorted({h.subs(t, r) for r in crit})
    eps = Rational(1, 1000)
    disc = [c for c in cand if not (tangent_count(curve, s, c - eps)[0] == tangent_count(curve, s, c)[0] == tangent_count(curve, s, c + eps)[0])]
    # 격자 전수: 후보가 아닌 점에서는 개수가 일정한 구간 안에 있음
    grid = [Rational(k, 4) for k in range(4 * lo, 4 * hi + 1)]
    vals = {g: tangent_count(curve, s, g)[0] for g in grid}
    for g1, g2 in zip(grid, grid[1:]):
        if vals[g1] != vals[g2]:
            assert any(g1 <= c <= g2 for c in cand), (g1, g2)
    return disc

# ===== 원문 풀이 =====
# I18: ∫_0^1(x^2-x)+∫_1^0(x+1)+∫_1^3(x^2-2x-1) = -3 (③)
o18 = integrate(x**2 - x, (x, 0, 1)) + integrate(x + 1, (x, 1, 0)) + integrate(x**2 - 2*x - 1, (x, 1, 3))
assert o18 == -3
# I4: F=xf-3x^4+x^2, F(1)=5 → f(-1)=3 (③)
fp4 = solve(sp.Eq(x * symbols('q'), -diff(-3*x**4 + x**2, x)), symbols('q'))[0]   # x f' = -P'
f4 = integrate(expand(fp4), x) + C
C4 = solve((x * f4 - 3*x**4 + x**2).subs(x, 1) - 5, C)[0]
assert f4.subs(C, C4).subs(x, -1) == 3
# I17: f(0)=0, f(1)=1, ∫f=1/6, g=-f(x+1)+1 (-1<x<0), f (0≤x≤1), 주기 2 → ∫_{-3}^2 g = 17/6 (②). 구체적 f로 확인
# f(0)=0, f(1)=1, ∫f=1/6 인 삼차다항식을 계수로 구함
p, q = symbols('p q')
fg = p*x**3 + q*x**2 + (1 - p - q)*x
sol17 = solve([integrate(fg, (x, 0, 1)) - Rational(1, 6), p - 1], [p, q])
f17 = fg.subs(sol17)
assert f17.subs(x, 0) == 0 and f17.subs(x, 1) == 1 and integrate(f17, (x, 0, 1)) == Rational(1, 6)
def g17_int(lo, hi):
    # 주기 2, 기본 구간 (-1,1]
    tot = 0
    for k in range(-5, 5):
        tot += integrate(-f17.subs(x, x - 2*k + 1) + 1, (x, sp.Max(lo, 2*k - 1), sp.Min(hi, 2*k))) if max(lo, 2*k - 1) < min(hi, 2*k) else 0
        tot += integrate(f17.subs(x, x - 2*k), (x, sp.Max(lo, 2*k), sp.Min(hi, 2*k + 1))) if max(lo, 2*k) < min(hi, 2*k + 1) else 0
    return sp.nsimplify(tot)
assert g17_int(-3, 2) == Rational(17, 6)
# M29: 점 (1,a), y=x^3-x → 불연속 a=-1, 0, 합 -1 (②)
d29 = discont_points(x**3 - x, 1)
assert sorted(d29) == [-1, 0] and sum(d29) == -1
print('원문 풀이 OK (I18=-3, I4=3, I17=17/6, M29=-1)')

# ===== 1번 =====
A1, B1, C1 = x**2 - 2*x + 2, 2*x - 2, x**2 - 4*x + 4
assert expand(A1 - B1 - C1) == 0 and expand(C1 - (x - 2)**2) == 0       # 합치기 짜임 유지
p1 = [integrate(A1, (x, 1, 2)), integrate(B1, (x, 2, 1)), integrate(C1, (x, 2, 4))]
assert p1 == [Rational(4, 3), -1, Rational(8, 3)]
v1 = sum(p1)
assert v1 == integrate((x - 2)**2, (x, 1, 4))
w1_sign = p1[0] - p1[1] + p1[2]        # 위끝·아래끝 교환 부호 실수
w1_drop = p1[0] + p1[2]                # 둘째 정적분 누락
chk(1, v1, wrongs=(w1_sign, w1_drop))

# ===== 3번 =====
P3 = -3*x**4 + 2*x**3
fx = Function('f')
# F = x f + P 를 미분: f = f + x f' + P'  →  x f' = -P'  (다항식이므로 f' = -P'/x, 유일)
fp3 = sp.cancel(-diff(P3, x) / x)
assert fp3.is_polynomial(x) and expand(fp3 - (12*x**2 - 6*x)) == 0
f3 = integrate(fp3, x) + C
F3 = expand(x * f3 + P3)
assert expand(diff(F3, x) - f3) == 0                       # F'=f 확인 (어떤 C에서도)
Cs = solve(F3.subs(x, 2) - 10, C)
assert len(Cs) == 1 and Cs[0] == 1                         # 적분상수 유일
v3 = F3.subs(C, Cs[0]).subs(x, 1)
w3 = f3.subs(C, Cs[0]).subs(x, 1)                          # F(1) 대신 f(1)
chk(3, v3, wrongs=(w3,))

# ===== 5번 =====
# 답이 f에 무관함: ∫f=1/2인 서로 다른 연속함수 여러 개로 확인
def g5_int(f, lo, hi):
    tot = 0
    for k in range(-4, 4):   # 주기 2, 기본 구간 [0,2): [0,1] f, (1,2) 2-f(x-1)
        a0, a1, a2 = 2*k, 2*k + 1, 2*k + 2
        if max(lo, a0) < min(hi, a1): tot += integrate(f.subs(x, x - 2*k), (x, max(lo, a0), min(hi, a1)))
        if max(lo, a1) < min(hi, a2): tot += integrate(2 - f.subs(x, x - 2*k - 1), (x, max(lo, a1), min(hi, a2)))
    return sp.nsimplify(tot)
fams = [Rational(1, 2) + 0*x, x, 2*x**3, Rational(3, 2)*x**2, 4*x**3 - 3*x**2 + Rational(1, 2), 1 - x]
for f in fams:
    assert integrate(f, (x, 0, 1)) == Rational(1, 2)
vals5 = {g5_int(f, -1, 4) for f in fams}
assert vals5 == {Rational(11, 2)}
v5 = vals5.pop()
w5 = Rational(5, 2) * g5_int(x, 0, 2)                        # 2.5주기 × 한 주기 정적분
assert g5_int(x, 0, 2) == 2
chk(5, v5, wrongs=(w5,))

# ===== 7번 =====
cur7 = -x**3 + 3*x
_, h7 = tangent_count(cur7, 2, 0)
assert expand(h7 - (2*t**3 - 6*t**2 + 6)) == 0
d7 = discont_points(cur7, 2)
assert sorted(d7) == [-2, 6]
# 개수 함수 값 확인
assert [tangent_count(cur7, 2, v)[0] for v in (-3, -2, 0, 6, 7)] == [1, 2, 3, 2, 1]
v7 = sum(d7)
w7_t = sum(r for r in solve(diff(h7, t), t))                 # 극값을 갖는 t의 합
w7_max = max(d7)                                             # a=-2(점이 곡선 위) 누락
assert cur7.subs(x, 2) == -2
chk(7, v7, wrongs=(w7_t, w7_max))

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
print(f'ABLATION 1 둘째 정적분의 위끝·아래끝 교환(∫_2^1): 필요(∫_1^2로 바꾸면 답 바뀜 {v1} → {w1_sign})')
v1_noC = p1[0] + p1[1]
print(f'ABLATION 1 셋째 정적분: 필요(빼면 답 바뀜 {v1} → {v1_noC})')
f3free = f3.subs(x, 1) + P3.subs(x, 1)
print(f'ABLATION 3 F(2)=10: 필요(정해지지 않음: F(1)={f3free} (C는 임의))')
assert f3free.has(C)
# 3번: 우변 2x^3 항을 빼면(원문형 -3x^4만) 답 바뀜
P3b = -3*x**4; f3b = integrate(sp.cancel(-diff(P3b, x) / x), x) + C; F3b = expand(x * f3b + P3b)
Cb = solve(F3b.subs(x, 2) - 10, C)[0]
print(f'ABLATION 3 2x^3 항: 필요(답 바뀜 {v3} → {F3b.subs(C, Cb).subs(x, 1)})')
assert F3b.subs(C, Cb).subs(x, 1) != v3
# 5번: ∫f=1/2 조건을 빼면 답이 f에 따라 달라짐
vals5b = {g5_int(f, -1, 4) for f in (x, 2*x, x**2)}
print(f'ABLATION 5 ∫f=1/2: 필요(정해지지 않음: f에 따라 {sorted(vals5b)})')
assert len(vals5b) > 1
# 5번: 주기 조건을 빼면 [-1,0], [2,4]에서 g가 정해지지 않음
print('ABLATION 5 g(x+2)=g(x): 필요(정해지지 않음: [0,2) 밖에서 g가 정의되지 않음)')
# 5번: 둘째 조각의 상수 2 → 0이면 답 바뀜
def g5_int_c(f, lo, hi, c):
    tot = 0
    for k in range(-4, 4):
        a0, a1, a2 = 2*k, 2*k + 1, 2*k + 2
        if max(lo, a0) < min(hi, a1): tot += integrate(f.subs(x, x - 2*k), (x, max(lo, a0), min(hi, a1)))
        if max(lo, a1) < min(hi, a2): tot += integrate(c - f.subs(x, x - 2*k - 1), (x, max(lo, a1), min(hi, a2)))
    return sp.nsimplify(tot)
print(f'ABLATION 5 조각 상수 2: 필요(0으로 바꾸면 답 바뀜 {v5} → {g5_int_c(x, -1, 4, 0)})')
# 7번: 점의 x좌표 2 → 원문 1이면 답 바뀜, 곡선 바꾸면 답 바뀜
d7b = discont_points(cur7, 1)
print(f'ABLATION 7 점의 x좌표 2: 필요(1로 바꾸면 답 바뀜 {v7} → {sum(d7b)})')
assert sum(d7b) != v7
d7c = discont_points(-x**3 + 2*x, 2)
print(f'ABLATION 7 곡선의 계수 3x: 필요(-x^3+2x이면 답 바뀜 {v7} → {sum(d7c)})')
assert sum(d7c) != v7

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
