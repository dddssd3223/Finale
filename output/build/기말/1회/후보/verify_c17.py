# -*- coding: utf-8 -*-
"""17번: 전체 계수 영역, 경계 달성, 조건 제거, 선지, 원문 직접 풀이."""
from pathlib import Path
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(ROOT / 'template/db/parts'),
               str(HERE.parent.parent / '지침'),
               str(ROOT / 'output/build/부교재_기말')]
import items_final as F
import schoolcheck as SC
import dupcheck as DC

it = runpy.run_path(str(HERE / 'c17.py'))['ITEMS'][17]
x, a, b, t = s.symbols('x a b t', real=True)
f = x**3 + a*x**2 + b*x
odd = s.expand(f - f.subs(x, -x))
assert s.factor(odd) == 2*x*(x**2+b)

# b<0: 0과 ±sqrt(-b)가 서로 다름. b=0: 0 하나.
# b>0: x²+b>0이므로 0 하나. 이것으로 실수 b 전 범위를 소진한다.
v = s.symbols('v', positive=True)
assert set(s.solve(odd.subs(b, -v**2), x)) == {-v, s.S.Zero, v}
assert s.real_roots(odd.subs(b, 0)) == [0, 0, 0]
assert (x*x+v).is_positive
print('실근 개수 전수 분기: b<0 -> 3, b=0 -> 1, b>0 -> 1; b>=0')

q = x*x+(a+2)*x+b+2*a+4
assert s.expand((x-2)*(f-f.subs(x, 2))-(x-2)**2*q) == 0
qmin = s.simplify(q.subs(x, -(a+2)/2))
assert qmin == -a*a/4+a+b+3
assert s.expand(q-(x+(a+2)/2)**2-qmin) == 0
# (x-2)^2을 나누지 못하는 한 점은 q의 연속성으로 포함한다.
print('전구간 부호 조건 <=> q>=0 <=> b>=a²/4-a-3')

target = f.subs(x, 1)
# a>=-2, b>=0에서는 target+1=(a+2)+b>=0.
assert s.expand(target+1-((a+2)+b)) == 0
# a<-2에서는 q의 하한을 대입하면 target>=a²/4-2>-1.
lower = s.simplify(target.subs(b, a*a/4-a-3))
assert lower == a*a/4-2
assert s.reduce_inequalities([a < -2, lower <= -1], a) is s.false
fstar = f.subs({a: -2, b: 0})
assert fstar.subs(x, 1) == -1
assert s.factor((x-2)*(fstar-fstar.subs(x, 2))) == x*x*(x-2)**2
assert s.solve(fstar-fstar.subs(x, -x), x) == [0]
# 등호는 a>=-2인 경우에만 가능하다. a+2와 b가 모두 0이므로 유일하다.
assert s.solve([a+2, b], [a, b]) == {a: -2, b: 0}
# 연속적인 허용 함수족: a=-2+t, b=0, 0<=t<=8. 최소점은 그 경계이다.
assert s.factor(s.discriminant(q.subs({a: -2+t, b: 0}), x)) == t*(t-8)
assert s.simplify(target.subs({a: -2+t, b: 0})) == t-1
print('최솟값 -1, 등호 함수 x³-2x² 유일; 허용 연속족 t∈[0,8]의 경계 t=0')

# ABLATION: 각 조건 및 (나)의 수치/개수 조건을 따로 제거한다.
without_ga = x**3-3*x*x  # (나)는 만족, f(1)=-2; a를 더 낮추면 하한 없음.
assert s.solve(without_ga-without_ga.subs(x, -x), x) == [0]
assert without_ga.subs(x, 0) == 0 and without_ga.subs(x, 1) == -2
assert ((x-2)*(without_ga-without_ga.subs(x, 2))).subs(x, 1) < 0
without_count = x**3-3*x
assert s.factor((x-2)*(without_count-without_count.subs(x, 2))) == (x-2)**2*(x+1)**2
assert len(s.solve(without_count-without_count.subs(x, -x), x)) == 3
assert without_count.subs(x, 1) == -2
without_zero = fstar-1
assert s.expand((without_zero-without_zero.subs(x, 2))-(fstar-fstar.subs(x, 2))) == 0
assert s.solve(without_zero-without_zero.subs(x, -x), x) == [0]
assert without_zero.subs(x, 1) == -2
print('ABLATION: (가) 제거 -> 하한 없음; (나) 제거 -> 상수 이동으로 하한 없음')
print('ABLATION 세부: f(0)=0 제거 -> 상수 이동, 실근 개수 제거 -> 최솟값 -2')

choices = list(map(s.Rational, it['choices']))
assert len(set(choices)) == 5 and {choices[i+1]-choices[i] for i in range(4)} == {1}
assert it['ans'] == 3 and choices[2] == -1
assert -2 in choices and -2 != choices[2] and '②' in it['wrong']
assert s.simplify(lower.subs(a, 0)) == -2  # 기록한 오답의 실제 최소
assert it['author'] == 'codex' and it['cand'] == 'codex17'
assert it['core']['axis'] == '①' and not it['bunseok']
assert len(it['cond']) == 2

# 원문 M32. 부호 조건에서 (x-4)로 나눈 이차식은 비음수이고
# f(0)=0이므로 그 이차식은 x²이다.
k, m = s.symbols('k m', real=True)
original = x*x*(x-4)
poly = s.factor(original-m*x)
assert poly == x*(x*x-4*x-m)
# 고정근 0과 이차식의 근이 겹치거나, 이차식의 두 근이 같아야 2근.
slopes = s.solve((x*x-4*x-m).subs(x, 0), m) + s.solve(s.discriminant(x*x-4*x-m, x), m)
assert set(slopes) == {0, -4}
ks = set()
for slope in slopes:
    assert len(set(s.real_roots(poly.subs(m, slope)))) == 2
    ks.update(s.solve(s.diff(original, x).subs(x, k)-slope, k))
assert ks == {s.S.Zero, s.Rational(2, 3), s.Integer(2), s.Rational(8, 3)}
total = sum(ks)
assert total == s.Rational(16, 3)
assert total.p+total.q == int(F.I['M32'][2]) == 19
print('원문 M32: k 전수 {0, 2/3, 2, 8/3}, 합 16/3, 정답 19')

newlen = len(DC.norm(SC.body(it)))
oldlen = len(DC.norm(F.I['M32'][0]))
assert newlen >= oldlen and SC.odist(it) <= 0.25
print(f'본문 정규화 길이 {oldlen}->{newlen}, 원문 골격 {SC.odist(it):.4f}')
print('선지 등차·정답 ③·오답 근거·유일성·조건 제거 확인')
print('ALL OK')
