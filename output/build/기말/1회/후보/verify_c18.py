# -*- coding: utf-8 -*-
"""18번: 연결 조건, 모든 이동 구간의 근, 적분상수 유일성, 넓이·조건 제거."""
from pathlib import Path
import re
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

it = runpy.run_path(str(HERE / 'c18.py'))['ITEMS'][18]
x, a, c = s.symbols('x a c', real=True)
third = s.Rational(1, 3)
delta = s.integrate(81*x*x-a, (x, -1, 1))
assert s.solve(delta-36, a) == [9]
base = 27*x**3-9*x+c
assert s.diff(base, x) == 81*x*x-9
assert s.simplify(base.subs(x, 1)-base.subs(x, -1)) == 36
assert s.diff(base, x).subs(x, 1) == s.diff(base, x).subs(x, -1) == 72
# 함수값 차36, 도함수 일치: 모든 정수 n에 대해 base(x-2n)+36n으로
# 이어 붙이면 전역 미분가능 함수가 존재하고 유일하다.
crit = s.solve(s.diff(base, x), x)
assert crit == [-third, third]
values = {r: s.expand(base.subs(x, r)) for r in [-1, -third, third, 1]}
assert values == {-1: c-18, -third: c+2, third: c-2, 1: c+18}
assert all(s.simplify(v-(c-18)) >= 0 and s.simplify(c+18-v) >= 0 for v in values.values())
# 0<c<4에서 n>=1인 구간은 최솟값 c-18+36n>0,
# n<=-1인 구간은 최댓값 c+18+36n<0. 무한히 많은 이동 구간을 소진.
k = s.symbols('k', integer=True, nonnegative=True)
assert s.expand(c-18+36*(k+1)) == c+18+36*k
assert s.expand(c+18+36*(-k-1)) == c-18-36*k
assert s.reduce_inequalities([c > 0, c < 4, c+18 <= 0], c) is s.false
assert s.reduce_inequalities([c > 0, c < 4, c-18 >= 0], c) is s.false

# 세 단조 구간에서 끝값 부호로 0<c<2 / c=2 / 2<c<4의 근을 센다.
assert s.reduce_inequalities([c > 0, c < 4, c+2 <= 0], c) is s.false
assert s.reduce_inequalities([c > 0, c < 4, c-18 >= 0], c) is s.false
assert s.discriminant(base, x) == 19683*(4-c*c)
for cv, wanted in [(1, 3), (2, 2), (3, 1)]:
    rr = set(s.real_roots(base.subs(c, cv)))
    assert len(rr) == wanted and all(-1 < r < 1 for r in rr)
candidate_c = s.solve(s.discriminant(base, x), c)
assert candidate_c == [-2, 2]
assert [r for r in candidate_c if 0 < r < 4] == [2]
f = base.subs(c, 2)
assert s.factor(f) == (3*x-1)**2*(3*x+2)
assert set(s.real_roots(f)) == {-s.Rational(2, 3), third}
print('a=9 유일; 전역 영점은 기본 구간에만 존재')
print('c 전수: (0,2) -> 3근, c=2 -> 2근, (2,4) -> 1근; c=2 유일')

# 0<=x<=1에서 인수분해식은 비음수, [1,2]는 기본 구간의 값을36만큼 올려 양수.
assert s.reduce_inequalities([x >= 0, x <= 1, 3*x+2 < 0], x) is s.false
assert f.subs(x, -1)+36 == 20 > 0
area1 = s.integrate(f, (x, 0, 1))
area2 = s.integrate(f.subs(x, x-2)+36, (x, 1, 2))
assert (area1, area2) == (s.Rational(17, 4), s.Rational(143, 4))
answer = area1+area2
assert answer == s.integrate(f, (x, -1, 1))+36 == 40
assert 36+2 == 38  # 기록한 오답: 상수항 적분을 c로 처리
print('미분가능 확장 및 비음수 확인; 넓이 17/4+143/4=40')

# ABLATION (가): 같은 형태의 다른 삼차함수 조각. 이동량36, 실근2개,
# 0<f(0)<4를 모두 유지하지만 넓이가 달라진다.
# p(x)=L*x³-L*r²*3*x+c0, r=1/4, c0=2Lr³.
r = s.Rational(1, 4)
coef = s.Rational(288, 13)
c0 = 2*coef*r**3
other = coef*x**3-3*coef*r*r*x+c0
assert c0 == s.Rational(9, 13) and 0 < c0 < 4
assert s.expand(other.subs(x, 1)-other.subs(x, -1)) == 36
assert s.diff(other, x).subs(x, 1) == s.diff(other, x).subs(x, -1)
assert set(s.real_roots(other)) == {-2*r, r}
other_values = [other.subs(x, z) for z in [-1, -r, r, 1]]
assert min(other_values) == c0-18 and max(other_values) == c0+18
assert c0-18+36 > 0 and c0+18-36 < 0
assert s.expand(other-coef*(x-r)**2*(x+2*r)) == 0
assert s.integrate(other, (x, -1, 1))+36 == s.Rational(486, 13) != answer

# ABLATION (나): 한 삼차다항식을 실수 전체에 그대로 사용.
# (가)는 a=9로, (다)는 근 -2/3,1/3과 f(0)=2로 만족한다.
assert s.integrate(f, (x, 0, 2)) == 94 != answer
# ABLATION (다): c=3, 같은 이동 확장. 양수인 [0,2]의 넓이는42.
assert s.integrate(base.subs(c, 3), (x, -1, 1))+36 == 42 != answer
# 세부: 실근 개수만 제거하면 c=3, 수치 범위만 제거하면 c=38.
# c=38인 함수는 최종 f를 x방향으로2 옮긴 함수이므로 전역 실근 수2를 보존.
assert s.expand(base.subs(c, 38)-(f+36)) == 0
assert s.integrate(base.subs(c, 38), (x, -1, 1))+36 == 112 != answer
print('ABLATION: (가) 제거 -> 486/13; (나) 제거 -> 94; (다) 제거 -> 42')
print('ABLATION 세부: 실근 수 제거 -> 42; f(0) 범위 제거 -> 112; 모두 필요')

choices = list(map(s.Rational, it['choices']))
assert len(set(choices)) == 5 and {choices[i+1]-choices[i] for i in range(4)} == {1}
assert it['ans'] == 4 and choices[3] == answer
assert choices[1] == 38 and '②' in it['wrong']
assert it['author'] == 'codex' and it['cand'] == 'codex18'
assert it['core']['axis'] == '②' and not it['bunseok'] and len(it['cond']) == 3

# 원문 J33: 경계 연속으로 계수, 평행이동으로 세 구간의 적분.
original = -x*x+a*x
oa = s.solve(original.subs(x, 1)-(original.subs(x, -1)+4), a)
assert oa == [2]
obase = original.subs(a, oa[0])
opieces = [(-2, -1, s.expand(obase.subs(x, x+2)-4)),
           (-1, 0, obase), (0, 1, obase),
           (1, 3, s.expand(obase.subs(x, x-2)+4))]
orig_A = orig_B = 0
for lo, hi, p in opieces:
    assert not any(lo < z < hi for z in s.solve(p, x))
    sign = s.sign(p.subs(x, s.Rational(lo+hi, 2)))
    area = sign*s.integrate(p, (x, lo, hi))
    if hi <= 0:
        orig_A += area
    else:
        orig_B += area
assert (orig_A, orig_B) == (s.Rational(14, 3), 8)
index = '①②③④⑤'.index(F.I['J33'][2])
frac = re.fullmatch(r'\\dfrac\{(\d+)\}(\d+)', F.I['J33'][1][index])
assert frac and s.Rational(frac[1], frac[2]) == orig_A+orig_B == s.Rational(38, 3)
print('원문 J33: 계수 2, A=14/3, B=8, 정답 ② 38/3')

newlen = len(DC.norm(SC.body(it)))
oldlen = len(DC.norm(F.I['J33'][0]))
assert newlen >= oldlen and SC.odist(it) <= 0.25
print(f'본문 정규화 길이 {oldlen}->{newlen}, 원문 골격 {SC.odist(it):.4f}')
print('선지 등차·정답 ④·오답 근거·유일성·조건 제거 확인')
print('ALL OK')
