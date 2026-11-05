# -*- coding: utf-8 -*-
"""M31 후보: 임계 높이 전수 분류, 합성 극한, 최솟값·오답·빼 보기."""
from pathlib import Path
import runpy
import sympy as s

x, t, u, m, c = s.symbols('x t u m c', real=True)
R = s.Rational
it = runpy.run_path(str(Path(__file__).with_name('c17.py')))['ITEMS'][17]
assert it['key'] == 'M31' and it['author'] == 'codex'


def distinct_real(poly):
    return set(s.Poly(poly, x).real_roots(radicals=False))


def count_abs(poly, height):
    if height < 0:
        return 0
    if height == 0:
        return len(distinct_real(poly))
    return len(distinct_real(poly-height)) + len(distinct_real(poly+height))


# 원문: 도함수의 근으로 임계 높이를 완전히 구한다.
original = x**3-3*x**2-9*x+10
critical = s.solve(s.diff(original, x), x)
assert critical == [-1, 3]
assert [original.subs(x, v) for v in critical] == [15, -17]
levels_original = [0, 15, 17]
eps = R(1, 100)
original_h = lambda z: count_abs(original, z)-count_abs(original, z-2)
candidates = sorted(set(levels_original + [v+2 for v in levels_original]))
discontinuous = []
for z in candidates:
    triple = [original_h(z-eps), original_h(z), original_h(z+eps)]
    if len(set(triple)) > 1:
        discontinuous.append(z)
assert discontinuous == [0, 2, 15, 19]
assert sum(discontinuous) == 36
assert [original_h(17-eps), original_h(17), original_h(17+eps)] == [-2]*3
print('원문 M31: 불연속점 [0, 2, 15, 19], 합 36 OK')

# 후보: 각 단조 구간의 끝점 높이가 유일한 임계 높이이다.
f = x**3-3*x+7
assert s.expand(s.diff(f, x)-3*(x-1)*(x+1)) == 0
assert [f.subs(x, z) for z in [-1, 1]] == [9, 5]
levels = [0, 5, 9]
heights = [-1, 0, 1, 5, 6, 9, 10]
assert [count_abs(f, z) for z in heights] == [0, 1, 2, 3, 4, 3, 2]
side_counts = {z: (count_abs(f, z-eps), count_abs(f, z+eps)) for z in levels}
assert side_counts == {0: (0, 2), 5: (2, 4), 9: (4, 2)}


def bad_points(q):
    """각 점의 국소 전개: 홀수 차수로 높이를 통과할 때만 양쪽 극한이 다르다."""
    result = set()
    for height in levels:
        for root, mult in s.roots(q-height, x).items():
            if root.is_real and mult % 2 and side_counts[height][0] != side_counts[height][1]:
                result.add(root)
    return result


# 전 실수 m의 분류를 결정하는 판별식: 양수면 두 단순근, 0이면 접촉점.
q = (x-u)**2+m
assert s.discriminant(q-c, x) == 4*(c-m)
assert s.expand(q.subs(m, c)-c) == s.expand((x-u)**2)
# 임계점 사이에서 개수는 불변. 0,5,9 각각의 경계도 별도 확인한다.
cells = [(-1, 6), (0, 4), (1, 4), (5, 2), (7, 2), (9, 0), (10, 0)]
for height, expected in cells:
    assert len(bad_points(q.subs({u: 2, m: height}))) == expected
assert s.reduce_inequalities([m >= 5, m < 9], m).as_set() == s.Interval.Ropen(5, 9)
# (가)에서 m in [5,9), 두 근은 q=9의 근. 근의 곱은 u²+m-9.
assert s.Poly(q-9, x).TC() == u**2+m-9
m_value = s.solve(u**2+m-9, m)[0]
assert m_value == 9-u**2
domain = s.reduce_inequalities([m_value >= 5, m_value < 9], u)
expected_domain = s.Union(s.Interval.Ropen(-2, 0), s.Interval.Lopen(0, 2))
assert domain.as_set() == expected_domain
target = s.expand(q.subs({x: 1, m: m_value}))
assert target == 10-2*u and s.diff(target, u) == -2
answer = target.subs(u, 2)
assert answer == 6
attainer = s.expand(q.subs({u: 2, m: 5}))
assert bad_points(attainer) == {s.Integer(0), s.Integer(4)}
# 꼭짓점 x=2에서는 g의 함숫값은 3, 양쪽 극한은 4: 극한은 존재한다.
assert count_abs(f, 5) == 3 and side_counts[5][1] == 4
print('17: m 전체 분류 6/4/2/0, 허용 u=[-2,0)∪(0,2], 최솟값 6 OK')

choices = list(map(s.sympify, it['choices']))
assert len(choices) == len(set(choices)) == 5
assert {choices[i+1]-choices[i] for i in range(4)} == {1}
assert it['ans'] == 5 and choices[it['ans']-1] == answer
wrong_drop_level = ((x-3)**2).subs(x, 1)
wrong_drop_term = (attainer-x**2).subs(x, 1)
assert [wrong_drop_level, wrong_drop_term] == [4, 5]
assert it['wrongs'] == [str(wrong_drop_level), str(wrong_drop_term)]
assert all(s.sympify(v) in choices and s.sympify(v) != answer for v in it['wrongs'])

# 조건 삭제는 숫자 교체가 아니라 나머지 조건을 만족하는 반례로 확인한다.
# (가)를 없애면 α,β는 (나)만 만족하면 되므로 임의 q가 가능하다.
# 더 강한 증인: α=0,β=6 둘 다 실제 극한 부재점이지만 추가 부재점도 있다.
without_count = (x-3)**2
assert {s.Integer(0), s.Integer(6)} <= bad_points(without_count)
assert len(bad_points(without_count)) == 4
assert without_count.subs(x, 1) == 4 < answer
print('ABLATION 17 (가) 두 점뿐: 필요(q=(x-3)^2, 부재점 네 개, q(1)=4)')
without_product = (x-1)**2+5
assert bad_points(without_product) == {-1, 3}
assert without_product.subs(x, 1) == 5 < answer
print('ABLATION 17 (나) 두 점의 곱 0: 필요(q=(x-1)^2+5, q(1)=5)')
without_monic = 4*(x-1)**2+5
assert bad_points(without_monic) == {0, 2}
assert without_monic.subs(x, 1) == 5 < answer
print('ABLATION 17 최고차항 계수 1: 필요(q=4(x-1)^2+5, q(1)=5)')
print('선지·정답 위치 ⑤·오답 4,5 OK')
print('ALL OK')
