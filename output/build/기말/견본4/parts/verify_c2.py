# -*- coding: utf-8 -*-
"""10·12·14·16: 정답, 경우 분기, 오답, 원문 및 16번 조건 빼 보기."""
from pathlib import Path
import runpy
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

# 14: y방향과 x방향으로 각각 적분. a>3이면 원점 이외의 교점(a,a)은 정사각형 밖.
S1 = s.integrate(x*x/a, (x, 0, 3))
S2 = S1
S3 = 9-S1-S2
aa = s.solve(S3-2*(S1+S2), a)
assert aa == [6] and aa[0] > 3
assert S1.subs(a, 6) == S2.subs(a, 6) == s.Rational(3, 2)
assert S3.subs(a, 6) == 6
assert (HERE / 'fig_c_14.svg').is_file()
wrong = [s.solve(S3-S1, a)[0], s.solve(S3-S1-S2, a)[0], s.solve(9-S2-2*(S1+S2), a)[0], s.solve(9-2*S1-S2-2*(S1+S2), a)[0]]
check(14, aa[0], 4, wrong)
o1 = s.Rational(9, 2)/a
o2 = 9/a
o3 = 9-o1-o2
roots = s.solve(o2**2-o1*o3, a)
assert roots == [s.Rational(7, 2)] and roots[0] > 3
original('J15', 12*roots[0], s.Integer(42), '42')

# 16: P=0 또는 P'=0. 좌우미분계수의 곱도 모든 후보에서 확인한다.
P = (x+1)*(x-1)**2*(x-2)**2
dp = s.factor(s.diff(P, x))
assert dp == (x-1)*(x-2)*(5*x*x-5*x-4)
zeros = set(s.solve(P, x))
stationary = set(s.solve(dp, x))
assert len(zeros) == 3 and len(stationary) == 4
assert zeros & stationary == {s.Integer(1), s.Integer(2)}
solutions = zeros | stationary
assert len(solutions) == 5
assert s.simplify(sum(solutions)) == 3
for r in solutions:
    pr = s.simplify(P.subs(x, r))
    dr = s.simplify(dp.subs(x, r))
    if pr == 0:
        # 차분몫의 좌우극한은 ±|P'(r)|. 접하는 근에서는 둘 다 0이다.
        product = -dr**2
    else:
        product = dr**2
    assert s.simplify(product) <= 0
assert s.discriminant(5*x*x-5*x-4, x) == 105
for r in [-1, 1, 2]:
    assert (5*x*x-5*x-4).subs(x, r) != 0
sum_dp, sum_p = s.simplify(sum(stationary)), sum(zeros)
check(16, s.simplify(sum(solutions)), 5, [sum_dp+len(zeros), sum_dp+sum_p, sum_dp+sum_p-1, sum_dp])

# 조건 빼 보기: 남은 조건을 만족하는 구체적인 반례/추가해를 사용한다.
alternative_f = x*x  # 함수식을 삭제하면 허용. 곱=4t²의 해는 0 하나.
alternative_solutions = s.solve(s.diff(alternative_f, x)**2, x)
assert alternative_solutions == [0] and sum(alternative_solutions) != sum(solutions)
print('ABLATION 16 함수식: 필요(f=x²이면 답 0, 원래 답 3)')
assert P.subs(x, 3) != 0 and dp.subs(x, 3)**2 > 0
print('ABLATION 16 좌우미분계수 곱 부등식: 필요(삭제하면 모든 실수 t가 허용되어 유한한 합이 정해지지 않음)')
assert {r for r in zeros if dp.subs(x, r) != 0} == {-1}
assert sum_dp == 4
print('TRAP 16: <0이면 -1만, 절댓값을 벗기면 합 4, 중복을 제거하지 않으면 합 6')

Po = x**4-4*x**3+8*x-32
zo = set(s.solve(Po, x))
zo = {r for r in zo if r.is_real}
do = set(s.solve(s.diff(Po, x), x))
assert zo == {-2, 4} and len(do) == 3 and not zo & do
original('D61', s.simplify(sum(zo | do)), s.Integer(5), '④')
print('ALL OK')
