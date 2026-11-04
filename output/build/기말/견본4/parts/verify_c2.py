# -*- coding: utf-8 -*-
"""10·12·14·16: 정답, 경우 분기, 오답, 원문 및 16번 조건 빼 보기."""
from pathlib import Path
import runpy
import re
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
IT = runpy.run_path(str(HERE / 'c2.py'))['ITEMS']
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F
x, t, a, b, c = s.symbols('x t a b c', real=True)
assert set(IT) == {10, 12, 14, 16}

def check(n, value, pos, wrong):
    it = IT[n]
    choices = list(map(s.sympify, it['choices']))
    assert it['author'] == 'codex' and it['ans'] == pos
    assert len(set(choices)) == len(choices) == 5
    assert len({choices[j+1]-choices[j] for j in range(4)}) == 1
    assert choices[pos-1] == value and choices.count(value) == 1
    assert set(wrong) == set(choices)-{value}
    listed = re.findall(r'([①②③④⑤]) \\\((.*?)\\\)', it['wrong'])
    assert len(listed) == 4
    for label, number in listed:
        assert s.sympify(number) == choices['①②③④⑤'.index(label)]
    assert {s.sympify(number) for _, number in listed} == set(wrong)
    print(f'{n}: answer={value}, position={pos}, AP={choices}, all distractors={wrong}: OK')

def original(key, value, expected, label):
    assert s.simplify(value-expected) == 0 and F.I[key][2] == label
    print(f'ORIGINAL {key}: {value}, stored answer {label}: OK')

# 10: 가속도를 적분하고 속도 연속으로 상수를 유일하게 결정한다.
v1 = 6*t*(t-1)
primitive = s.integrate(6*t-12, t)+c
cs = s.solve(primitive.subs(t, 1)-v1.subs(t, 1), c)
assert cs == [9]
v2 = s.factor(primitive.subs(c, cs[0]))
assert s.expand(v2-3*(t-1)*(t-3)) == 0
assert v1.subs(t, 1) == v2.subs(t, 1) == 0
assert s.diff(v1, t).subs(t, 1) != s.diff(v2, t).subs(t, 1)
assert [s.sign(v1.subs(t, s.Rational(1, 2))), s.sign(v2.subs(t, 2)), s.sign(v2.subs(t, 4))] == [-1, -1, 1]
pieces = [-s.integrate(v1, (t, 0, 1)), -s.integrate(v2, (t, 1, 3)), s.integrate(v2, (t, 3, 4))]
assert pieces == [1, 4, 4]
check(10, sum(pieces), 3, [abs(-pieces[0]-pieces[1]+pieces[2]), pieces[0]+pieces[1], pieces[0]+2*pieces[1]+pieces[2], pieces[0]+2*sum(pieces[1:])])
vo1 = 2*t**3-8*t
vo2 = s.integrate(6*t+4, t)+c
co = s.solve(vo2.subs(t, 2)-vo1.subs(t, 2), c)
assert co == [-20]
vo2 = vo2.subs(c, co[0])
assert s.diff(vo1, t).subs(t, 2) == s.diff(vo2, t).subs(t, 2)
original('J69', -s.integrate(vo1, (t, 0, 2))+s.integrate(vo2, (t, 2, 3)), s.Integer(17), '17')

# 12: 조각별 원시함수의 연속·좌우미분계수로 a=b²-2b.
# b<=2에서는 감소 구간 또는 상수 구간이 생긴다. b>2가 필요충분.
q = x*x-2*x
right = s.integrate(q, (x, b, x)) + a*b
left = a*x
assert s.simplify(right.subs(x, b)-left.subs(x, b)) == 0
assert s.diff(right, x).subs(x, b) == b*b-2*b
assert s.solve_univariate_inequality(q < 0, x, relational=False) == s.Interval.open(0, 2)
assert q.subs(x, 2) == 0  # b=2이면 a=0: 왼쪽 상수 구간, 역함수 없음
inside = s.simplify(b*(b*b-2*b)+s.integrate(q, (x, b, 3)))
assert s.expand(inside-(2*b**3/3-b*b)) == 0
assert s.expand(s.diff(inside, b)-2*b*(b-1)) == 0
assert inside.subs(b, 3) == 9 < 24  # (2,3] 전체를 배제
aval = s.solve(3*a-24, a)
bvals = s.solve(b*b-2*b-aval[0], b)
assert aval == [8] and bvals == [-2, 4]
valid = [bb for bb in bvals if bb > 3]
assert valid == [4]
assert s.integrate(s.Piecewise((8, x < 4), (q, True)), (x, 0, 3)) == 24
wrong_b6 = s.solve(2*(b-2)-8, b)[0]
check(12, aval[0]+valid[0], 2, [8+wrong_b6, 8+2, 8, 8+bvals[0]])
# 원문도 연결점의 세 위치를 확인한다.
qo = -3*x*x+x
ao = qo.subs(x, b)
io = s.factor(b*ao+s.integrate(qo, (x, b, 2))+s.Rational(15, 2))
assert s.expand(io+(b-1)*(4*b*b+3*b+3)/2) == 0
assert s.discriminant(4*b*b+3*b+3, b) == -39
outside_roots = s.solve(2*ao+s.Rational(15, 2), b)
assert all(bb <= 2 for bb in outside_roots)
assert qo.subs(x, s.Rational(1, 3)) == 0
original('I40', ao.subs(b, 1)+1, s.Integer(-1), '②')

# 14: 직사각형 [0,4]×[0,2]. 곡선과 윗변의 교점에 따라 실제 넓이를 분기한다.
y, u = s.symbols('y u', positive=True)
ap = s.symbols('ap', positive=True)
# 두 곡선의 원점 이외 교점은 (a,a), a>2이면 내부에서 겹치지 않는다.
assert s.factor((x*x/ap)**2/ap-x) == x*(x-ap)*(x*x+ap*x+ap*ap)/ap**3
assert s.discriminant(x*x+ap*x+ap*ap, x) == -3*ap**2
assert s.simplify((y*y/ap)**2/ap-y) == y**4/ap**3-y
# 0<y<=2<a이면 y^4/a^3<y: 왼쪽 부분은 아래쪽 부분과 겹치지 않는다.
S1 = s.integrate(y*y/ap, (y, 0, 2))
S2_inside = s.simplify(s.integrate(x*x/ap, (x, 0, s.sqrt(2*ap))) + 2*(4-s.sqrt(2*ap)))
S2_outside = s.integrate(x*x/ap, (x, 0, 4))
assert S1 == 8/(3*ap)
assert s.simplify(S2_inside-(8-4*s.sqrt(2*ap)/3)) == 0
assert S2_inside.subs(ap, 8) == S2_outside.subs(ap, 8) == s.Rational(8, 3)
# 2<a<=8 ⇔ 2<u=sqrt(2a)<=4. 목표값과의 차이를 양수인 식으로 정리한다.
excess = s.simplify((S1+S2_inside-s.Rational(8, 3)).subs(ap, u*u/2))
certificate = 4*(4-u)/3+16/(3*u*u)
assert s.simplify(excess-certificate) == 0  # 2<u<=4에서 첫 항>=0, 둘째 항>0
# a>8에서는 일차방정식으로 귀결되고 유일한 후보 9가 범위를 만족한다.
S3 = 8-S1-S2_outside
aa = s.solve(8-3*(S1+S2_outside), ap)
assert aa == [9] and aa[0] > 8
actual = [q.subs(ap, 9) for q in [S1, S2_outside, S3]]
assert actual == [s.Rational(8, 27), s.Rational(64, 27), s.Rational(16, 3)]
assert sum(actual) == 8 and actual[2] == 2*sum(actual[:2])
assert (HERE / 'fig_c_14.svg').is_file()
# ①계수 3을 2로, ②적분을 끝값으로, ③S1 누락, ⑤S1 중복 합산.
wrong = [s.solve(S3-S1-S2_outside, ap)[0],
         s.solve(S1+16/ap-s.Rational(8, 3), ap)[0],
         s.solve(S2_outside-s.Rational(8, 3), ap)[0],
         s.solve(2*S1+S2_outside-s.Rational(8, 3), ap)[0]]
assert wrong == [6, 7, 8, 10]
check(14, aa[0], 4, wrong)
print('CASES 14: 2<a<=8 excluded by positive excess; a>8 gives unique a=9')
o1 = s.Rational(9, 2)/a
o2 = 9/a
o3 = 9-o1-o2
roots = s.solve(o2**2-o1*o3, a)
assert roots == [s.Rational(7, 2)] and roots[0] > 3
original('J15', 12*roots[0], s.Integer(42), '42')

# 16: 절댓값의 좌우미분계수. P(t)!=0이면 곱=P'(t)^2, P(t)=0이면 곱=-P'(t)^2.
P = (x+1)**3*(x-3)+a
dp = s.factor(s.diff(P, x))
assert dp == 4*(x+1)**2*(x-2)
stationary = set(s.solve(dp, x))
assert stationary == {-1, 2}
assert s.simplify(P.subs(x, -1)) == a
assert s.simplify(P.subs(x, 2)) == a-27
assert s.solve_univariate_inequality(dp > 0, x, relational=False) == s.Interval.open(2, s.oo)
assert s.solve_univariate_inequality(dp < 0, x, relational=False) == s.Union(s.Interval.open(-s.oo, -1), s.Interval.open(-1, 2))
assert s.limit(P, x, -s.oo) == s.limit(P, x, s.oo) == s.oo
# 따라서 a<27이면 실근 2개, a=27이면 1개, a>27이면 0개이다.
# 매개변수의 모든 구간을 조사한다. 판별식의 영점 밖에서는 실근 수가 변하지 않으며,
# P와 P'의 공통근도 두 경계에서만 생긴다. 각 구간을 Sturm 정리로 대조한다.
discriminant = s.factor(s.discriminant(P, x))
assert discriminant == 256*a*a*(a-27)
assert s.solve(discriminant, a) == [0, 27]
cases = [('a<0', -1, 2, 0, 4), ('a=0', 0, 2, 1, 3),
         ('0<a<27', 1, 2, 0, 4), ('a=27', 27, 1, 1, 2),
         ('a>27', 28, 0, 0, 2)]
for label, av, nzeros, noverlap, ntotal in cases:
    poly = s.Poly(P.subs(a, av), x)
    count = poly.count_roots(-s.oo, s.oo)
    overlap = {r for r in stationary if poly.eval(r) == 0}
    assert count == nzeros and len(overlap) == noverlap
    assert count+len(stationary)-len(overlap) == ntotal
    print(f'CASES 16 {label}: P zeros={count}, overlap={sorted(overlap)}, solutions={ntotal}')
assert [av for _, av, _, _, count in cases if count == 3] == [0]
P0 = P.subs(a, 0)
zeros = set(s.solve(P0, x))
solutions = zeros | stationary
assert zeros == {-1, 3} and solutions == {-1, 2, 3}
assert sum(solutions) == 4
# 각 후보에서 좌우 차분몫의 극한을 직접 계산한다. a=27의 접하는 근도 확인한다.
h = s.symbols('h', real=True)
for av, r, want in [(0, -1, 0), (0, 2, 0), (0, 3, -4096), (1, -1, 0), (27, -1, 0), (27, 2, 0)]:
    poly = P.subs(a, av)
    quotient = (s.Abs(poly.subs(x, r+h))-s.Abs(poly.subs(x, r)))/h
    dr = s.limit(quotient, h, 0, dir='+')
    dl = s.limit(quotient, h, 0, dir='-')
    assert s.simplify(dr*dl) == want
# a=1일 때 x=-1은 P와 |P| 모두 극값이 아닌 정지점이지만 미분계수 곱은 0이다.
P1 = P.subs(a, 1)
assert P1.subs(x, -1) == 1 and dp.subs(x, -1) == 0
assert P1.subs(x, -s.Rational(11, 10)) > 1 > P1.subs(x, -s.Rational(9, 10)) > 0
assert dp.subs(x, -s.Rational(11, 10)) < 0 and dp.subs(x, -s.Rational(9, 10)) < 0
boundary_zeros = {r for r in s.solve(P.subs(a, 27), x) if r.is_real}
assert boundary_zeros == {2}
boundary_solutions = boundary_zeros | stationary
# ①P의 근을 겹친 횟수대로 합산, ②a=27을 잘못 선택, ③P=0만, ④중복 제거 전의 합.
wrong = [sum(s.Poly(P0, x).all_roots()), sum(boundary_solutions),
         sum(zeros), sum(zeros)+sum(stationary)]
assert wrong == [0, 1, 2, 3]
check(16, sum(solutions), 5, wrong)

# 조건을 하나씩 지웠을 때 답이 달라지거나 정해지지 않음을 구체적으로 확인한다.
# 함수식 삭제: |x²-1|이면 후보 {-1,0,1}로 3개이지만 합은 0이다.
alternative_P = x*x-1
alternative_solutions = set(s.solve(alternative_P, x)) | set(s.solve(s.diff(alternative_P, x), x))
assert len(alternative_solutions) == 3 and sum(alternative_solutions) == 0 != sum(solutions)
print('ABLATION 16 함수식: 필요(f=|x²-1|이면 해 3개, 합 0)')
# 개수 조건 삭제: a=27에서도 미분계수 곱 조건으로 해를 고를 수 있으나 합은 1이다.
assert sum(boundary_solutions) == 1 != sum(solutions)
print('ABLATION 16 서로 다른 해 3개: 필요(a=27이면 해 {-1,2}, 합 1)')
# 부등식 삭제: t를 제한하는 조건이 없어 모든 실수가 허용된다.
assert s.FiniteSet(0, 1, 2, 3).is_subset(s.S.Reals)
print('ABLATION 16 좌우미분계수 곱 부등식: 필요(모든 실수 t가 허용되어 해 3개와 유한한 합이 정해지지 않음)')
# <=를 <로 바꾸면 겹치지 않은 실근만 남는다. 모든 경우에 최대 2개이므로 3개는 불가능하다.
simple_counts = []
for _, av, _, _, _ in cases:
    intervals = s.Poly(P.subs(a, av), x).intervals()
    simple_counts.append(sum(mult == 1 for _, mult in intervals))
assert simple_counts == [2, 1, 2, 0, 0]
print('TRAP 16: strict <0 gives at most 2 solutions; a=27 repeated zero has product 0')

Po = x**4-4*x**3+8*x-32
zo = set(s.solve(Po, x))
zo = {r for r in zo if r.is_real}
do = set(s.solve(s.diff(Po, x), x))
assert zo == {-2, 4} and len(do) == 3 and not zo & do
original('D61', s.simplify(sum(zo | do)), s.Integer(5), '④')
print('ALL OK')
