# -*- coding: utf-8 -*-
"""서답형1: f(x)=x^4-4x^3+ax^2+b, x=1에서 극값 3 → a, b와 극댓값·극솟값. 유일성, 조건 빼 보기, 배점, D18 원문."""
from pathlib import Path
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'output/build/부교재_기말'))
import items_final as F

it = runpy.run_path(str(HERE / 'p4.py'))['SITEMS']['S1']
x, a, b = s.symbols('x a b', real=True)
f = x**4-4*x**3+a*x**2+b
df = s.diff(f, x)
assert s.expand(df-(4*x**3-12*x**2+2*a*x)) == 0

# (1) f'(1)=0, f(1)=3 → 해가 하나뿐
sols = s.solve([df.subs(x, 1), f.subs(x, 1)-3], [a, b], dict=True)
assert sols == [{a: 4, b: 2}], sols
A, B = 4, 2
g = f.subs({a: A, b: B})
assert s.expand(g-(x**2*(x-2)**2+2)) == 0
print('S1(1): a=4, b=2 (유일)')

# (2) 증가·감소와 극값
dg = s.diff(g, x)
assert s.factor(dg) == 4*x*(x-1)*(x-2)
crit = sorted(s.solve(dg, x))
assert crit == [0, 1, 2]
sign = lambda t: s.sign(dg.subs(x, t))
assert [sign(t) for t in (-1, s.Rational(1, 2), s.Rational(3, 2), 3)] == [-1, 1, -1, 1]
assert s.solve_univariate_inequality(dg < 0, x, relational=False) == s.Union(s.Interval.open(-s.oo, 0), s.Interval.open(1, 2))
assert s.solve_univariate_inequality(dg > 0, x, relational=False) == s.Union(s.Interval.open(0, 1), s.Interval.open(2, s.oo))
maxima = [c for c in crit if sign(c-s.Rational(1, 10)) > 0 > sign(c+s.Rational(1, 10))]
minima = [c for c in crit if sign(c-s.Rational(1, 10)) < 0 < sign(c+s.Rational(1, 10))]
assert maxima == [1] and minima == [0, 2]
maxv = {g.subs(x, c) for c in maxima}; minv = {g.subs(x, c) for c in minima}
assert maxv == {3} and minv == {2}
# 이계도함수로도 확인
d2 = s.diff(g, x, 2)
assert d2.subs(x, 1) < 0 and d2.subs(x, 0) > 0 and d2.subs(x, 2) > 0
print('S1(2): x<=0 감소, 0<=x<=1 증가, 1<=x<=2 감소, x>=2 증가 / 극댓값 3 (x=1), 극솟값 2 (x=0, 2)')

# 조건 빼 보기
# 'x=1에서 극값'(f'(1)=0)을 빼고 f(1)=3만 두면 a, b가 하나로 정해지지 않는다
only_val = s.solve([f.subs(x, 1)-3], [a, b], dict=True)
assert len(only_val) == 1 and len(only_val[0]) == 1   # b=-a+6 꼴, 한 문자 남음
print('ABLATION S1 f(1)=3(극값 3의 값): 필요(빼면 b 미정)')
only_crit = s.solve([df.subs(x, 1)], [a, b], dict=True)
assert only_crit == [{a: 4}]
print("ABLATION S1 x=1에서 극값(f'(1)=0): 필요(빼면 a 미정, 극값도 a에 따라 바뀜)")
# a가 다르면 x=1이 극점이 아님(예: a=3이면 f'(1)=-2)
assert df.subs({a: 3, x: 1}) != 0
# 극값 3을 극솟값이라고 가정하면 해가 없음(주어진 극값은 극댓값이어야 함) → 판정이 실제로 일함
assert d2.subs(x, 1) < 0
print('판정: x=1에서 이계도함수 -4<0, 주어진 극값 3은 극댓값(극솟값 아님)')

# 오답 근거
wa = s.solve(4-12+a, a)[0]; wb = s.solve(1-4+wa+b-3, b)[0]
assert (wa, wb) == (8, -2)
print('오답: ax^2을 ax로 미분하면 a=8, b=-2')

# 배점
def pts_of(t):
    return sum(int(m) for m in re.findall(r'\[(\d+)점\]', t))
assert pts_of(it['rubric'][0]) == 4, pts_of(it['rubric'][0])
assert pts_of(it['rubric'][1]) == 6, pts_of(it['rubric'][1])
assert pts_of(it['rubric'][2]) == 0
print('배점: (1) 4점, (2) 6점')

# 기록 필드
assert it['author'] == 'claude' and it['key'] == 'D18'
assert it['src'] == '학교 자체 출제' and it['bunseok'] is False
assert '함정 추가' not in it['vtype'] and it['effect'] in ('같음', '쉬워짐', '어려워짐')
for k in ('subs', 'ans', 'rubric', 'sol', 'fast', 'wrong', 'note', 'var', 'vtype', 'effect', 'bunseok', 'precedent', 'level'):
    assert k in it, k
assert len(it['subs']) == len(it['ans']) == len(it['sol']) == 2
assert it['subs'][0][1] == '4점, 풀이과정을 상세히 쓰시오.'
assert it['subs'][1][1] == '6점, 풀이과정을 상세히 쓰시오.'
assert r'a=4' in it['ans'][0] and r'b=2' in it['ans'][0]
assert r'\(3\)' in it['ans'][1] and r'\(2\)' in it['ans'][1]
assert 'x^4-4x^3+ax^2+b' in it['body']
assert not it.get('choices')

# 원문 D18: f(x)=x^4-2x^2+ax+b, x=0에서 극대, 극솟값이 모두 3 → a+b=4
of = x**4-2*x**2+a*x+b
oa = s.solve(s.diff(of, x).subs(x, 0), a)[0]
assert oa == 0
og = of.subs(a, oa)
ocrit = sorted(s.solve(s.diff(og, x), x))
assert ocrit == [-1, 0, 1]
ob = s.solve(og.subs(x, 1)-3, b)[0]
assert og.subs({b: ob, x: -1}) == 3 and s.diff(og, x, 2).subs(x, 0) < 0
orig_answer = oa+ob
assert orig_answer == 4
idx = '①②③④⑤'.index(F.I['D18'][2])
assert int(F.I['D18'][1][idx]) == orig_answer
print('원문 D18: a=0, b=4, a+b=4 (정답 ④)')
print('ALL OK')
