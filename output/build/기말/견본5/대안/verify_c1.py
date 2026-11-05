# -*- coding: utf-8 -*-
"""실행 위치에 무관한 c1 검증. 원문 본문은 복제하지 않고 키로 읽는다."""
from pathlib import Path
import importlib.util
import re
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('codex_c1', HERE / 'c1.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
IT = module.ITEMS
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as source

x, t, a, b, k = s.symbols('x t a b k', real=True)
WANT = {1: ('I3', 4), 3: ('D17', 5), 5: ('J16', 3), 7: ('J33', 1)}


def value(text):
    m = re.fullmatch(r'\\[dt]?frac\{?(-?\d+)\}?\{?(\d+)\}?', text)
    return s.Rational(m[1], m[2]) if m else s.sympify(text)


def check(n, answer, wrong):
    item = IT[n]
    choices = list(map(value, item['choices']))
    assert (item['key'], item['ans']) == WANT[n]
    assert item['author'] == 'codex'
    assert len(choices) == len(set(choices)) == 5
    assert len({choices[i+1] - choices[i] for i in range(4)}) == 1
    assert s.simplify(answer - choices[item['ans']-1]) == 0
    assert sum(s.simplify(answer - v) == 0 for v in choices) == 1
    # wrong 문자열에 실제로 적힌 수치와 계산 결과, 선지 포함을 함께 검사한다.
    listed = re.findall(r'[①②③④⑤] \\\((.*?)\\\)', item['wrong'])
    assert list(map(value, listed)) == wrong
    assert all(v in choices and v != answer for v in wrong)
    print(f'{n}: 정답 {answer}, 위치 {item["ans"]}, 유일성·등차·오답 {wrong} OK')


def original(key, got):
    _, choices, ans, _ = source.I[key]
    expected = value(choices['①②③④⑤'.index(ans)]) if choices else value(ans)
    assert s.simplify(got - expected) == 0, (key, got, expected)
    print(f'ORIGINAL {key}: {got} OK')


assert set(IT) == set(WANT)

# 1: f-f'가 일차이므로 f는 일차. 상수/영함수는 우변 차수와 모순.
f = a*x+b
sol = s.solve(s.Poly(f-s.diff(f, x)-(4*x-3), x).all_coeffs(), (a, b), dict=True)
assert sol == [{a: 4, b: 1}]
f = f.subs(sol[0])
F = f + 2*x**2-3*x
assert s.expand(s.diff(F, x)-f) == 0
check(1, f.subs(x, 0), [s.Integer(-3), s.Integer(3)])
assert (4*x-3).subs(x, 0) == -3  # f' 누락
assert -((4*x-3).subs(x, 0)) == 3  # 상수항의 부호 혼동
c = s.symbols('c')
fo = a*x**2+b*x+c
so = s.solve(s.Poly(fo-s.diff(fo, x)-(6*x**2-14*x), x).all_coeffs(), (a,b,c), dict=True)
assert len(so) == 1
fo = fo.subs(so[0])
roots = s.solve(fo-5*x**2, x)
assert len(roots) == 2 and all(r.is_real for r in roots)
original('I3', sum(roots))

# 3: 계수의 유일성이 아닌 극댓값의 유일성을 증명한다.
f = a*x**3+b*x+5
assert s.expand(f+f.subs(x, -x)) == 10
# f가 극소를 가지면 a*b<0. 도함수의 두 근은 ±sqrt(-b/(3a)).
assert s.Poly(s.diff(f, x), x).all_coeffs() == [3*a, 0, b]
# 임의의 극소점 r 주변의 부등식은 -r에서 극대 부등식으로 반전된다.
maximum = 2*f.subs(x,0)-2
check(3, maximum, [2*s.Integer(2), s.Integer(5), s.Integer(5)+2])
# 양/음의 최고차항 양쪽 모두 실제로 실현 가능하다.
for witness in [s.Rational(3,2)*x**3-s.Rational(9,2)*x+5,
                -s.Rational(3,2)*x**3+s.Rational(9,2)*x+5]:
    extrema = [(s.diff(witness,x,2).subs(x,r), witness.subs(x,r))
               for r in s.solve(s.diff(witness,x),x)]
    assert [v for d,v in extrema if d>0] == [2]
    assert [v for d,v in extrema if d<0] == [8]
fo = a*x**3+b*x+a
so = s.solve([s.diff(fo,x).subs(x,1), fo.subs(x,1)+2], (a,b), dict=True)
assert len(so) == 1
fo = fo.subs(so[0])
assert s.diff(fo,x,2).subs(x,1)>0
original('D17', fo.subs(x,-1))

# 5: 15<k<27 ⇔ 0<d<2, 교점은 2±d, k=15+3d². 넓이비의 동치와 유일성 (측정 후 경량화안).
d = s.symbols('d', positive=True)
f5 = 3*(x-3)**2; g5 = -6*x+k
h = s.expand(f5-g5)
assert s.expand(h-(3*(x-2)**2+15-k)) == 0
hd = h.subs(k, 15+3*d**2)
assert s.simplify(hd.subs(x, 2-d)) == 0 and s.simplify(hd.subs(x, 2+d)) == 0
assert h.subs(x, 0) == 27-k  # k<27 이면 y축에서 곡선이 직선 위, 왼쪽 교점 2-d>0
left = s.integrate(hd, (x, 0, 2-d))           # S1
middle = -s.integrate(hd, (x, 2-d, 2+d))      # S2
assert s.simplify(middle-4*d**3) == 0
assert s.simplify(left-middle/2-s.integrate(hd, (x, 0, 2))) == 0
# S2-2S1 = 12d²-16 : 0<d<2 에서 근은 d²=4/3 하나 → 유일
eq = s.expand(middle-2*left)
assert s.expand(eq-(12*d**2-16)) == 0
dd = [r for r in s.solve(eq, d) if r.is_real and 0 < r < 2]
assert dd == [2/s.sqrt(3)]
ks = s.solve(s.integrate(h, (x, 0, 2)), k)
assert ks == [19] and 15 < ks[0] < 27 and 15+3*dd[0]**2 == 19
assert all(15 < v < 27 for v in map(value, IT[5]['choices']))   # 범위로 지워지는 선지 없음
# 오답: 꼭짓점 x=3을 대칭축으로 / S2=S1 (오른쪽 교점까지 정적분 0) / (-1)^3 부호 실수 / 3x² → (3/2)x³
wrong_vertex = s.solve(s.integrate(h, (x, 0, 3)), k)[0]
d1 = [r for r in s.solve(left-middle, d) if r.is_real and 0 < r < 2]
assert d1 == [1]
wrong_equal = 15+3*d1[0]**2
assert wrong_vertex == wrong_equal == 18
assert s.integrate(f5, (x, 0, 2)) == 26 and s.integrate(g5, (x, 0, 2)) == 2*k-12
wrong_sign = s.solve((1-(-3)**3)-(2*k-12), k)[0]
wrong_half = s.solve(s.Rational(3, 2)*2**3-6*2**2+(27-k)*2, k)[0]
check(5, ks[0], [wrong_vertex, wrong_sign, wrong_half])
ho = (x-4)**2-(-2*x+k)
ko = s.solve(s.integrate(ho,(x,0,3)),k)
assert ko == [10] and 7<ko[0]<16
original('J16', ko[0])

# 7: 연속성은 이음점 x=1에서 충분하고, 이동 관계로 모든 이음점에 전파된다.
base = -x**2+a*x
aval = s.solve(base.subs(x,1)-(base.subs(x,-1)+4),a)
assert aval == [2]
shifted = s.expand(base.subs({x:x-2}).subs(a,2)+4)
assert shifted.subs(x,1)==1 and shifted.subs(x,2)==4
assert s.diff(shifted,x).subs(x,2)>0  # 도함수는 [1,2] 전체에서 양수
area = s.integrate(shifted,(x,1,2))
wrong_no_square = s.integrate(2*x+4,(x,-1,0))
wrong_a0 = s.integrate(-x**2+4,(x,-1,0))
check(7, area, [wrong_no_square, wrong_a0, s.integrate(4,(x,-1,0))])
# 추가 확인: 연속 조건을 지우면 a=0도 가능하며 넓이가 달라진다.
assert wrong_a0 != area
original_base = -x**2+2*x
A = -s.integrate(original_base.subs(x,x+2)-4,(x,-2,-1))-s.integrate(original_base,(x,-1,0))
B = s.integrate(original_base,(x,0,1))+s.integrate(original_base.subs(x,x-2)+4,(x,1,3))
assert (A,B) == (s.Rational(14,3),s.Integer(8))
original('J33', A+B)

print('ALL OK')
