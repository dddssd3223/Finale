# -*- coding: utf-8 -*-
"""18번: 도함수의 실근 유형을 전수 분류하고 모든 조건에 반례를 만든다."""
from pathlib import Path
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
IT = runpy.run_path(str(HERE / 'c3.py'))['ITEMS']
assert set(IT) == {18}
it = IT[18]
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F
x, y, t, a, b, c, u, v = s.symbols('x y t a b c u v', real=True)

def kink_count(poly, variable=x):
    """절댓값이 미분불가능한 점 = 다항식의 단순 실근. 중복도까지 정확히 계산."""
    return sum(m == 1 for _, m in s.Poly(poly, variable).real_roots(multiple=False))

def integral(poly):
    return s.simplify(15*s.integrate(poly, (x, -1, 1)))

# 전수 분류 근거: f'는 실계수 삼차식이다.
# (A) 단순 실근 하나/삼중 실근 하나: 유일한 최소 높이에서 g=0.
# (B) 이중 실근과 단순 실근: 최소 높이에서 g=0, 정지변곡 높이에서 g=1.
# (C) 서로 다른 실근 셋: 두 극솟값이 다르면 불연속 높이 3개.
#     두 극솟값이 같으면 그 높이에서 g=0, 극댓값 높이에서 g=2.
# 따라서 (가)(나)는 (C)의 같은 두 극솟값=0을 강제한다.
single_min = x**4+x*x+1
flat_min = x**4+1
assert kink_count(single_min-1) == kink_count(flat_min-1) == 0
assert s.discriminant(s.diff(single_min, x), x) < 0
assert s.factor(s.diff(flat_min, x)) == 4*x**3
unequal_minima = x**4-2*x*x+x+1
assert s.discriminant(s.diff(unequal_minima, x), x) > 0
critical_values = s.Poly(s.resultant(unequal_minima-t, s.diff(unequal_minima, x), x), t)
assert critical_values.degree() == 3 and s.discriminant(critical_values.as_expr(), t) != 0

# 모든 (B)형: 삼차항이 없으므로 f'=4(x-r)^2(x+2r), r!=0.
r = s.symbols('r', real=True, nonzero=True)
degenerate = x**4-6*r*r*x*x+8*r**3*x+1
assert s.expand(s.diff(degenerate, x)-4*(x-r)**2*(x+2*r)) == 0
minimum = degenerate.subs(x, -2*r)
shoulder = degenerate.subs(x, r)
assert s.simplify(minimum) == 1-24*r**4
assert s.simplify(shoulder) == 1+3*r**4
assert s.factor(degenerate-shoulder) == (x-r)**3*(x+3*r)
assert s.factor(degenerate-minimum) == (x+2*r)**2*(x*x-4*r*x+6*r*r)
assert s.discriminant(x*x-4*r*x+6*r*r, x) == -8*r*r
# 위 두 인수분해가 (B)형 전체에서 g(최소)=0, g(정지변곡)=1임을 보인다.

# (C)형에서 같은 두 최소 높이가 0이면 f는 두 제곱인수의 곱이다.
sq = s.Poly((x-u)**2*(x-v)**2, x)
assert sq.coeff_monomial(x**3) == -2*(u+v)
assert s.factor(sq.coeff_monomial(1)) == u*u*v*v
possible_u = s.solve(u**4-1, u)
assert possible_u == [-1, 1]  # u는 실수로 선언되어 있다.
candidates = {s.expand((x-uu)**2*(x+uu)**2) for uu in possible_u}
assert len(candidates) == 1
f = candidates.pop()
assert f == x**4-2*x*x+1
critical = s.solve(s.diff(f, x), x)
assert critical == [-1, 0, 1]
levels = sorted({f.subs(x, rr) for rr in critical})
assert levels == [0, 1]
table = {tt: kink_count(f-tt) for tt in [-1, 0, s.Rational(1, 2), 1, 2]}
assert list(table.values()) == [0, 0, 4, 2, 2]
# 정지점 높이 사이에서는 단순 실근 수가 불변이다. 모든 높이 구간과 경계를 확인했다.
print('EXHAUSTIVE 18: derivative cases A(simple/triple), B(double+simple), C(unequal/equal minima): OK')
print('18 g(t) table:', table, '; unique (a,b,p)=(-2,0,1)')

answer = integral(f)
choices = list(map(s.sympify, it['choices']))
assert it['author'] == 'codex' and it['ans'] == 1
assert len(set(choices)) == len(choices) == 5
assert len({choices[j+1]-choices[j] for j in range(4)}) == 1
assert choices[0] == answer == 16 and choices.count(answer) == 1
wrong = [integral(x**4+aa*x*x+1) for aa in [-1, 0, 1, 2]]
assert wrong == [26, 36, 46, 56] == choices[1:]
assert kink_count((x*x+1)**2-1) == 0  # 마지막 오답에는 서로 다른 두 극소점이 없다.
print(f'18: answer={answer}, position=1, AP={choices}, all distractors={wrong}: OK')

# (가) 삭제: f=x^4+1, p=2는 (나)를 만족시키나 적분값은 36.
without_a = x**4+1
assert kink_count(without_a-2) == 2 and integral(without_a) == 36 != answer
print('ABLATION 18 (가): 필요(f=x⁴+1, p=2이면 (나) 성립, 답 36)')

# (나) 삭제: r=24^(-1/4), f(r*y)=(y^4-6y²+8y+24)/24.
# 극소 높이=0, 정지변곡 높이=9/8의 두 높이에서만 불연속이다.
scaled = (y**4-6*y*y+8*y+24)/24
assert s.factor(s.diff(scaled, y)) == (y-1)**2*(y+2)/6
ablation_levels = sorted({scaled.subs(y, q) for q in [-2, 1]})
assert ablation_levels == [0, s.Rational(9, 8)]
table_b = {tt: kink_count(scaled-tt, y) for tt in [-1, 0, 1, s.Rational(9, 8), 2]}
assert list(table_b.values()) == [0, 0, 2, 1, 2]
rr = 24**(-s.Rational(1, 4))
without_b = degenerate.subs(r, rr)
ablation_answer = integral(without_b)
assert s.simplify(ablation_answer-(36-5*s.sqrt(6))) == 0
assert ablation_answer != answer
print(f'ABLATION 18 (나): 필요(정지변곡 반례 g={table_b}, 답 {ablation_answer})')

# 본문에서 함수의 각 고정 계수 조건도 실제로 일하는지 확인한다.
# 최고차항 1을 삭제하면 2(x²-1/√2)²: 상수항1, 삼차항0, (가)(나) 모두 성립.
without_leading = 2*(x*x-1/s.sqrt(2))**2
assert s.expand(without_leading).subs(x, 0) == 1
assert set(s.solve(s.diff(without_leading, x), x)) == {-2**(-s.Rational(1, 4)), s.Integer(0), 2**(-s.Rational(1, 4))}
assert s.simplify(integral(without_leading)-(42-20*s.sqrt(2))) == 0
assert integral(without_leading) != answer
print('ABLATION 18 최고차항 계수: 필요(2(x²-1/√2)²이면 답 42-20√2)')

# 삼차항0을 삭제하면 (x-2)²(x-1/2)²: 상수항1, 같은 두 최소0, 다른 높이 g=2.
without_cubic = (x-2)**2*(x-s.Rational(1, 2))**2
middle = s.Rational(5, 4)
p_shift = without_cubic.subs(x, middle)
assert p_shift == s.Rational(81, 256)
assert kink_count(without_cubic-p_shift) == 2
assert integral(without_cubic) == s.Rational(237, 2) != answer
print('ABLATION 18 삼차항 계수: 필요((x-2)²(x-1/2)²이면 답 237/2)')

# 상수항1을 삭제하면 (x²-2)²: 같은 두 최소0, 극대4에서 g=2.
without_constant = (x*x-2)**2
assert kink_count(without_constant-4) == 2 and integral(without_constant) == 86 != answer
print('ABLATION 18 상수항: 필요((x²-2)²이면 답 86)')

# 원문을 직접 풀기: 적분 대칭 → 이차항, 주어진 정지점 → 일차항,
# 두 불연속 높이 중 작은 값0 → 상수항. 원문 문장을 복사하지 않는다.
original = x**3+a*x*x+b*x+c
z = s.symbols('z', real=True)
symmetry = s.Poly(s.expand(original.subs(x, -z)+original.subs(x, z+2)-2*original.subs(x, 1)), z)
coeff_a = s.solve(symmetry.all_coeffs(), a)
assert coeff_a == {a: -3}
ob = s.solve(s.diff(original.subs(coeff_a), x).subs(x, -1), b)
assert ob == [-9]
original = original.subs({a: -3, b: ob[0]})
crit_o = s.solve(s.diff(original, x), x)
assert crit_o == [-1, 3]
co = s.solve(original.subs(x, 3), c)
assert co == [27]
original = original.subs(c, co[0])
assert original.subs(x, -1) > 0
assert s.integrate(original, (x, -1, 1)) == 52 and F.I['I44'][2] == '④'
print('ORIGINAL I44: integral=52, stored answer ④: OK')
print('ALL OK')
