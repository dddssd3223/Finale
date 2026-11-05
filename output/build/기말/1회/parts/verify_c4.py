# -*- coding: utf-8 -*-
"""서답형1: 두 한쪽 미분계수, 전체 매개변수 범위, 끝값, D15 원문."""
from pathlib import Path
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'output/build/부교재_기말'))
import items_final as F

it = runpy.run_path(str(HERE / 'c4.py'))['SITEMS']['S1']
x, h, a = s.symbols('x h a', real=True)
left = x**3+(1-a)*x
right = x**3+(1+a)*x
assert left.subs(x, 0) == right.subs(x, 0) == 0
L = s.limit(left.subs(x, h)/h, h, 0, dir='-')
R = s.limit(right.subs(x, h)/h, h, 0, dir='+')
assert (L, R) == (1-a, 1+a)
allowed = s.reduce_inequalities([L >= 0, R >= 0], a)
assert allowed.as_set() == s.Interval(-1, 1)
assert s.diff(left, x) == 3*x*x+1-a
assert s.diff(right, x) == 3*x*x+1+a
# |a|<=1이면 양쪽 열린 반직선에서 도함수가 양수이다. 0에서 연속으로 이어진다.
r = s.symbols('r', positive=True)
assert (3*r*r).is_positive
assert s.limit(left, x, -s.oo) == -s.oo
assert s.limit(right, x, s.oo) == s.oo
# a>1이면 음의 영점과 0에서 함숫값이 같다.
# a<-1이면 양의 영점과 0에서 함숫값이 같다.
assert s.simplify(left.subs(a, 1+r*r).subs(x, -r)) == 0
assert s.simplify(right.subs(a, -1-r*r).subs(x, r)) == 0
# 끝값에서 한쪽 미분계수가 0이어도 각 열린 반직선에서 도함수는 양수이다.
assert s.diff(left.subs(a, 1), x) == 3*x*x
assert s.diff(right.subs(a, -1), x) == 3*x*x
assert s.solve(L-R, a) == [0]  # wrong에 기록한 '미분가능성' 오답
print('S1(1): 좌 1-a, 우 1+a')
print('S1(2): [-1,1] 전체에서 일대일대응; 범위 밖은 서로 다른 두 영점으로 배제')
print('오답 검증: 끝값 ±1 포함, 미분가능성만 요구하면 a=0')
assert it['author'] == 'codex' and it['key'] == 'D15'
assert it['src'] == '학교 자체 출제' and not it['bunseok']
assert len(it['subs']) == len(it['ans']) == len(it['sol']) == 2
assert it['subs'][0][1].startswith('4점') and it['subs'][1][1].startswith('6점')
assert '1-a' in it['ans'][0] and '1+a' in it['ans'][0]
assert r'-1\le a\le1' in it['ans'][1]
assert not it.get('choices')  # 서답형이므로 선지 등차·선지 오답 포함 검사는 비대상.

# 원문 D15: 왼쪽 도함수의 음수 구간을 x<a가 만나지 않아야 한다.
original_left = x**3+x*x+(a-x)+2
original_right = x**3+x*x+(x-a)+2
dl = s.diff(original_left, x)
dr = s.diff(original_right, x)
assert s.factor(dl) == (x+1)*(3*x-1)
assert s.solve_univariate_inequality(dl < 0, x, relational=False) == s.Interval.open(-1, s.Rational(1, 3))
assert s.expand(dr-(3*(x+s.Rational(1, 3))**2+s.Rational(2, 3))) == 0
assert s.simplify((original_left-original_right).subs(x, a)) == 0
# x<a 전체에서 dl>=0 <=> a<=-1. a=-1에서는 양쪽 열린 구간에서 증가.
assert s.solve_univariate_inequality(dl.subs(x, -1-r) > 0, r) is s.true
assert s.diff(original_right, x).subs(x, -1) == 2
orig_answer = -1
idx = '①②③④⑤'.index(F.I['D15'][2])
assert int(F.I['D15'][1][idx]) == orig_answer
print('원문 D15: 왼쪽 도함수 음수 구간 (-1,1/3), a<=-1, 정답 ② -1')
print('채점 배점 4+6·답안·필요충분성·끝값 확인')
print('ALL OK')
