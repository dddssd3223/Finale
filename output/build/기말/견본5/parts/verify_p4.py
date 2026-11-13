# -*- coding: utf-8 -*-
# p4.py (견본5 서답형1, 자체 출제 · 유형 I53) 검증: 원문 풀이 · (1)(2) 답 · 유일성 · 오답 값 · 조건 빼 보기
import os
import sympy as sp
from sympy import symbols, integrate, diff, expand, solve, Poly, Rational
x, t, C = symbols('x t C', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py')).read(), ns)
S = ns['SITEMS']['S1']
assert S['author'] == 'claude' and S['key'] == 'I53' and S['src'] == '학교 자체 출제'
assert [q[1] for q in S['subs']] == ['4점, 풀이과정을 상세히 쓰시오.', '6점, 풀이과정을 상세히 쓰시오.']

# ===== 원문 I53: ∫_0^x f = 3x^3+2x → f(1)=11 (③)
fo = diff(3*x**3 + 2*x, x)
assert fo.subs(x, 1) == 11
print('원문 풀이 OK (I53=11)')

RHS = lambda f: x*f - 2*x**3 + 3*x**2 - 4
LOW = 1

# ===== 유일성: 차수 n 이하 일반 다항식으로 전수 (n=0..6), 항등식 계수 비교 =====
sols_all = []
for n in range(0, 7):
    cs = symbols(f'c0:{n + 1}')
    f = sum(cs[i] * x**i for i in range(n + 1))
    eq = expand(integrate(f.subs(x, t), (t, LOW, x)) - RHS(f))
    sol = solve(Poly(eq, x).all_coeffs(), cs, dict=True)
    for so in sol:
        sols_all.append(sp.expand(f.subs(so)))
sols_all = {sp.expand(s_) for s_ in sols_all}
assert sols_all == {3*x**2 - 6*x + 6}, sols_all
f = 3*x**2 - 6*x + 6
assert expand(integrate(f.subs(x, t), (t, 1, x)) - RHS(f)) == 0      # 원식 성립
print('유일성 OK: 차수 0~6 전수에서 f(x)=3x^2-6x+6 하나')

# ===== (1) f'(x)
fp = diff(f, x)
# 풀이 경로: 양변 미분 → x f'(x) = 6x^2 - 6x
F = sp.Function('F')
lhs_d = F(x)                               # d/dx ∫_1^x f = f(x)
rhs_d = diff(x*F(x) - 2*x**3 + 3*x**2 - 4, x)
assert expand(rhs_d - lhs_d - (x*diff(F(x), x) - 6*x**2 + 6*x)) == 0
assert expand(x*fp - (6*x**2 - 6*x)) == 0 and fp == 6*x - 6
print(f"(1) f'(x) = {fp}  OK  (답란: {S['ans'][0]})")
assert '6x-6' in S['ans'][0].replace(' ', '')

# ===== (2) f(x): 적분 + 아래끝 대입
Fc = integrate(6*x - 6, x) + C
f1 = solve(RHS(sp.Symbol('y')).subs(x, 1), sp.Symbol('y'))     # 0 = f(1) - 2 + 3 - 4
assert f1 == [3]
Cv = solve(Fc.subs(x, 1) - 3, C)
assert Cv == [6]
assert expand(Fc.subs(C, 6) - f) == 0
print(f"(2) f(x) = {sp.expand(f)}  OK  (답란: {S['ans'][1]})")
assert '3x^2-6x+6' in S['ans'][1].replace(' ', '')

# ===== 오답 확인 (wrong에 적은 값)
w_noC = 3*x**2 - 6*x                                   # 적분상수 누락
assert expand(integrate(w_noC.subs(x, t), (t, 1, x)) - RHS(w_noC)) != 0
assert integrate(f.subs(x, t), (t, 1, 0)) == -4         # x=0 대입은 ∫_1^0 f = -4 (0이 아님) → 0=-4 모순 오답
w_sign = solve((3*x**2 - 6*x + C).subs(x, 1) - (2 - 3 - 4), C)[0]   # 이항 부호 실수 f(1)=-5
assert w_sign == -2
print('오답 OK: 3x^2-6x, x=0 대입 모순, 3x^2-6x-2')

# ===== 조건 빼 보기
print('--- 조건 빼 보기 ---')
# 상수항 -4: 빼면 f(1)=-1, C=2로 답 바뀜
fA = 3*x**2 - 6*x + solve((3*x**2 - 6*x + C).subs(x, 1) - (2 - 3), C)[0]
assert expand(integrate(fA.subs(x, t), (t, 1, x)) - (x*fA - 2*x**3 + 3*x**2)) == 0 and fA != f
print(f'ABLATION S1 우변 상수 -4: 필요(답 바뀜 {f} → {fA})')
# 아래끝 1: 아래끝을 0으로 바꾸면 x=0 대입에서 0=-4 모순 → 만족하는 f 없음
n0 = []
for n in range(0, 7):
    cs = symbols(f'c0:{n + 1}'); g = sum(cs[i] * x**i for i in range(n + 1))
    eq = expand(integrate(g.subs(x, t), (t, 0, x)) - RHS(g))
    n0 += solve(Poly(eq, x).all_coeffs(), cs, dict=True)
assert n0 == []
print('ABLATION S1 아래끝 1: 필요(아래끝 0이면 만족하는 다항함수 없음, 아래끝이 적분상수를 정함)')
# xf(x) 항: 빼면 x=1 대입에서 0=-3 모순 → 만족하는 f 없음
assert (-2*x**3 + 3*x**2 - 4).subs(x, 1) != 0
print('ABLATION S1 xf(x) 항: 필요(빼면 x=1 대입에서 0=-3 모순, 만족하는 다항함수 없음)')
print('ALL OK')
