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

# 5: 64<k<100 ⇔ 0<d<3, 교점은 3±d. 넓이비의 동치와 유일성.
d = s.symbols('d', positive=True)
h = 4*(x-3)**2+64-k
left = s.integrate(h.subs(k,64+4*d**2), (x,0,3-d))
middle = -s.integrate(h.subs(k,64+4*d**2), (x,3-d,3+d))
assert s.simplify(left-middle/2-s.integrate(h.subs(k,64+4*d**2),(x,0,3))) == 0
ks = s.solve(s.integrate(h,(x,0,3)),k)
assert ks == [76] and 64<ks[0]<100
assert s.simplify((middle-2*left).subs(d,s.sqrt(3))) == 0
# 잘못된 S1=S2 조건은 오른쪽 교점까지 부호 있는 적분이 0.
ds = s.solve(left-middle,d)
valid_ds = [r for r in ds if r.is_real and 0<r<3]
assert valid_ds == [s.Rational(3,2)]
wrong_equal = 64+4*valid_ds[0]**2
wrong_half = s.solve(s.Rational(2,3)*3**3-12*3**2+3*(100-k),k)[0]
wrong_power = s.solve(2*3**3-12*3**2+3*(100-k),k)[0]
check(5, ks[0], [wrong_half, wrong_equal, wrong_power])
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
