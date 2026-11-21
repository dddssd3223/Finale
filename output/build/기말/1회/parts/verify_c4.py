# -*- coding: utf-8 -*-
"""서답형1: f(x)=x^3+x-4|x|의 두 한쪽 미분계수, 감소하는 범위, 조건 빼 보기, 배점, D15 원문."""
from pathlib import Path
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'output/build/부교재_기말'))
import items_final as F

it = runpy.run_path(str(HERE / 'c4.py'))['SITEMS']['S1']
x, h = s.symbols('x h', real=True)
f = x**3+x-4*s.Abs(x)
left = x**3+5*x    # x<0
right = x**3-3*x   # x>=0
neg, pos = s.symbols('neg', negative=True), s.symbols('pos', positive=True)
assert s.simplify(f.subs(x, neg)-left.subs(x, neg)) == 0
assert s.simplify(f.subs(x, pos)-right.subs(x, pos)) == 0
assert f.subs(x, 0) == 0

# (1) 정의 그대로(절댓값 포함) 두 한쪽 극한
q = (f.subs(x, h)-f.subs(x, 0))/h
L = s.limit(q, h, 0, dir='-')
R = s.limit(q, h, 0, dir='+')
assert (L, R) == (5, -3)
assert s.expand(left.subs(x, h)/h) == h**2+5 and s.expand(right.subs(x, h)/h) == h**2-3
print('S1(1): 좌 5, 우 -3')

# (2) 감소하는 범위: 두 조각의 f'<0 집합 → (0,1), 연속성으로 끝값 포함 [0,1]
dl, dr = s.diff(left, x), s.diff(right, x)
assert s.expand(dl-(3*x**2+5)) == 0 and s.expand(dr-3*(x-1)*(x+1)) == 0
negL = s.solve_univariate_inequality(dl < 0, x, relational=False).intersect(s.Interval.open(-s.oo, 0))
negR = s.solve_univariate_inequality(dr < 0, x, relational=False).intersect(s.Interval.open(0, s.oo))
assert negL is s.EmptySet and negR == s.Interval.open(0, 1)
posR = s.solve_univariate_inequality(dr > 0, x, relational=False).intersect(s.Interval.open(0, s.oo))
assert posR == s.Interval.open(1, s.oo)
assert s.limit(f, x, 0, '-') == s.limit(f, x, 0, '+') == f.subs(x, 0)  # 0에서 연속
# 유일성: 감소 구간은 [0,1] 하나뿐(밖의 어느 점을 넣어도 감소가 깨짐), 끝값 포함 확인
assert f.subs(x, 0) > f.subs(x, s.Rational(1, 2)) > f.subs(x, 1)
assert f.subs(x, -s.Rational(1, 10)) < f.subs(x, 0)      # 0 왼쪽으로 넓히면 감소 아님
assert f.subs(x, 1) < f.subs(x, s.Rational(11, 10))      # 1 오른쪽으로 넓히면 감소 아님
assert (f.subs(x, 0), f.subs(x, 1)) == (0, -2)           # 극댓값 0, 극솟값 -2
# 촘촘한 격자 수치 확인: 감소하는 이웃 구간이 정확히 [0,1]
pts = [s.Rational(k, 100) for k in range(-300, 301)]
vals = [f.subs(x, p) for p in pts]
dec = [pts[i] for i in range(len(pts)-1) if vals[i+1] < vals[i]]
assert dec[0] == 0 and dec[-1] == s.Rational(99, 100) and len(dec) == 100
print('S1(2): 감소하는 범위 0<=x<=1 (x<0 증가, x>1 증가)')

# 조건 빼 보기: 절댓값의 양쪽 부호를 모두 써야 답이 [0,1]이 된다
only_plus = x**3+x-4*x    # |x|를 x로만 봄 → 감소 [-1,1]
only_minus = x**3+x+4*x   # |x|를 -x로만 봄 → 항상 증가
assert s.solve_univariate_inequality(s.diff(only_plus, x) < 0, x, relational=False) == s.Interval.open(-1, 1)
assert s.solve_univariate_inequality(s.diff(only_minus, x) < 0, x, relational=False) is s.EmptySet
no_abs = x**3+x           # 절댓값 항을 빼면 감소 구간이 없음
assert s.solve_univariate_inequality(s.diff(no_abs, x) < 0, x, relational=False) is s.EmptySet
# (1)에서 h<0에도 |h|=h로 계산하는 오답 → 두 극한 모두 -3
assert s.limit(right.subs(x, h)/h, h, 0, dir='-') == -3
print('빼 보기: |x|=x만 → [-1,1], |x|=-x만 → 감소 없음, 절댓값 항 없음 → 감소 없음')

# 배점: 소문항별 [n점] 합이 4, 6
def pts_of(t):
    return sum(int(m) for m in re.findall(r'\[(\d+)점\]', t))
assert pts_of(it['rubric'][0]) == 4, pts_of(it['rubric'][0])
assert pts_of(it['rubric'][1]) == 6, pts_of(it['rubric'][1])
assert pts_of(it['rubric'][2]) == 0
assert '각' not in ''.join(re.findall(r'\[[^\]]*점\]', ''.join(it['rubric'])))
print('배점: (1) 4점, (2) 6점')

# 기록 필드
assert it['author'] == 'codex' and it['key'] == 'D15'
assert it['src'] == '학교 자체 출제' and not it['bunseok'] and it['effect'] == '쉬워짐'
assert '측정 후 Claude 수정' in it['var'] and '함정 추가' not in it['vtype']
assert len(it['subs']) == len(it['ans']) == len(it['sol']) == 2
assert it['subs'][0][1] == '4점, 풀이과정을 상세히 쓰시오.'
assert it['subs'][1][1] == '6점, 풀이과정을 상세히 쓰시오.'
assert r'\(5\)' in it['ans'][0] and r'\(-3\)' in it['ans'][0]
assert r'0\le x\le1' in it['ans'][1]
assert 'x^3+x-4|x|' in it['body']
assert not it.get('choices')  # 서답형이므로 선지 검사는 비대상.

# 원문 D15: 왼쪽 도함수의 음수 구간을 x<a가 만나지 않아야 한다.
a = s.symbols('a', real=True)
r = s.symbols('r', positive=True)
original_left = x**3+x*x+(a-x)+2
original_right = x**3+x*x+(x-a)+2
odl = s.diff(original_left, x)
odr = s.diff(original_right, x)
assert s.factor(odl) == (x+1)*(3*x-1)
assert s.solve_univariate_inequality(odl < 0, x, relational=False) == s.Interval.open(-1, s.Rational(1, 3))
assert s.expand(odr-(3*(x+s.Rational(1, 3))**2+s.Rational(2, 3))) == 0
assert s.simplify((original_left-original_right).subs(x, a)) == 0
assert s.solve_univariate_inequality(odl.subs(x, -1-r) > 0, r) is s.true
assert odr.subs(x, -1) == 2
orig_answer = -1
idx = '①②③④⑤'.index(F.I['D15'][2])
assert int(F.I['D15'][1][idx]) == orig_answer
print('원문 D15: 왼쪽 도함수 음수 구간 (-1,1/3), a<=-1, 정답 ② -1')
print('ALL OK')
