# -*- coding: utf-8 -*-
"""D45 후보: 사차의 근 지수 전수 분류·두 후보 배제·조건별 반례."""
from pathlib import Path
import runpy
import sympy as s

x, a, b, c, d, r = s.symbols('x a b c d r', real=True)
R = s.Rational
it = runpy.run_path(str(Path(__file__).with_name('c18.py')))['ITEMS'][18]
assert it['key'] == 'D45' and it['author'] == 'codex'

# 원문을 직접 푼다: 유한 극한의 두 소거 조건 + 내부 극소점.
original = x**3+a*x**2+b*x+c
osol = s.solve([original.subs(x, -2)-2, s.diff(original, x).subs(x, -2),
               s.diff(original, x).subs(x, 4)], (a, b, c), dict=True)
assert len(osol) == 1
original = original.subs(osol[0])
assert s.expand(s.diff(original, x)-3*(x-4)*(x+2)) == 0
assert s.diff(original, x, 2).subs(x, 4) > 0
assert s.limit((original-2)/(x+2)**2, x, -2) == -9
assert original.subs(x, 8) == 102
print('원문 D45: 유일한 삼차함수, f(8)=102 OK')

general = x**4+a*x**3+b*x**2+c*x+d
finite = s.solve([general.subs(x, 0)-1, s.diff(general, x).subs(x, 0)], (c, d))
assert finite == {c: 0, d: 1}
assert s.limit((general.subs(finite)-1)/x**2, x, 0) == b
# 두 실근 모두 짝수 지수여야 전 구간에서 부호가 바뀌지 않는다.
# 차수 4의 모든 양의 지수 분배를 전수 조사하면 (2,2)뿐이다.
partitions = [(i, 4-i) for i in range(1, 4)]
assert [(i, j) for i, j in partitions if i % 2 == j % 2 == 0] == [(2, 2)]
family = x**2*(x-r)**2+1
assert s.Poly(family, x).LC() == 1
k = s.limit((family-1)/x**2, x, 0)
assert k == r**2
derivative = s.factor(s.diff(family, x))
assert s.expand(derivative-2*x*(x-r)*(2*x-r)) == 0
candidates = s.solve(derivative.subs(x, 1), r)
assert candidates == [1, 2]
survivors = [rr for rr in candidates if s.diff(family, x, 2).subs({x: 1, r: rr}) > 0]
assert survivors == [1]
solution = family.subs(r, survivors[0])
assert s.factor(solution-1) == x**2*(x-1)**2
assert s.solve(solution-1, x) == [0, 1]
assert s.expand(solution-solution.subs(x, 1)) == s.expand(x**2*(x-1)**2)
answer = k.subs(r, survivors[0])
assert answer == 1
print('18: 짝수 지수 배분 (2,2), r=1 또는 2 중 r=1만 극소, k=1 OK')

choices = list(map(s.sympify, it['choices']))
assert len(choices) == len(set(choices)) == 5
assert {choices[i+1]-choices[i] for i in range(4)} == {1}
assert it['ans'] == 2 and choices[it['ans']-1] == answer
wrong_second_derivative = s.diff(solution, x, 2).subs(x, 0)
wrong_maximum = k.subs(r, 2)
assert [wrong_second_derivative, wrong_maximum] == [2, 4]
assert it['wrongs'] == [str(wrong_second_derivative), str(wrong_maximum)]
assert all(s.sympify(v) in choices and s.sympify(v) != answer for v in it['wrongs'])

# 모든 명시 조건을 개별 삭제한다. (나)의 두 절도 따로 검사한다.
without_limit = (x-1)**2*(x-2)**2+1
assert s.solve(without_limit-1, x) == [1, 2]
assert s.diff(without_limit, x).subs(x, 1) == 0
assert without_limit.subs(x, 1) == 1
assert s.limit((without_limit-1)/x**2, x, 0) == s.oo
print('ABLATION 18 (가) 유한 극한: 필요(f=(x-1)^2(x-2)^2+1 허용, k 미정)')
without_lower = x**4-R(4, 3)*x**3+1
assert s.solve(without_lower-1, x) == [0, R(4, 3)]
assert s.limit((without_lower-1)/x**2, x, 0) == 0
assert s.expand(s.diff(without_lower, x)-4*x**2*(x-1)) == 0
assert s.expand(without_lower-without_lower.subs(x, 1)-(x-1)**2*(3*x**2+2*x+1)/3) == 0
assert s.discriminant(3*x**2+2*x+1, x) < 0
print('ABLATION 18 (나) 전 구간 하한: 필요(f=x^4-4x^3/3+1, k=0)')
# (다)는 작은 근방만 아니라 주어진 열린구간 전체에서 확인한다.
without_two = x**4-R(11, 5)*x**3+R(13, 10)*x**2+1
assert s.solve(without_two-1, x) == [0]
assert s.discriminant(x**2-R(11, 5)*x+R(13, 10), x) < 0
assert s.limit((without_two-1)/x**2, x, 0) == R(13, 10)
assert s.expand(without_two-without_two.subs(x, 1)-(x-1)**2*(10*x**2-2*x-1)/10) == 0
assert (10*x**2-2*x-1).subs(x, R(1, 2)) == R(1, 2)
assert s.diff(10*x**2-2*x-1, x).subs(x, R(1, 2)) > 0
print('ABLATION 18 (나) 서로 다른 두 근: 필요(f=x^4-11x^3/5+13x^2/10+1, k=13/10)')
without_local_min = family.subs(r, 2)
assert s.solve(without_local_min-1, x) == [0, 2]
assert s.limit((without_local_min-1)/x**2, x, 0) == 4
assert s.diff(without_local_min, x, 2).subs(x, 1) < 0
print('ABLATION 18 (다) 구간 하한: 필요(f=x^2(x-2)^2+1, k=4)')
without_monic = 2*x**2*(x-1)**2+1
assert s.limit((without_monic-1)/x**2, x, 0) == 2
print('ABLATION 18 최고차항 계수 1: 필요(f=2x^2(x-1)^2+1, k=2)')
print('선지·정답 위치 ②·오답 2,4 OK')
print('ALL OK')
