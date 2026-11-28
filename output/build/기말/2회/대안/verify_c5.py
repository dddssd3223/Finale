# -*- coding: utf-8 -*-
"""M56 서답형2: 모든 k 구간·경계의 정확한 근 수와 조건 빼 보기."""
from pathlib import Path
import runpy
import sympy as s

x, a, b, z = s.symbols('x a b z', real=True)
R = s.Rational
it = runpy.run_path(str(Path(__file__).with_name('c5.py')))['SITEMS']['S2']
assert it['key'] == 'M56' and it['author'] == 'codex'


def roots_on(poly, negative):
    roots = set(s.Poly(poly, x).real_roots(radicals=False))
    return [r for r in roots if bool(r < 0) == negative]


def count(left, right, height):
    return len(roots_on(left-height, True)) + len(roots_on(right-height, False))


# 원문: 직선 조각과 삼차 조각의 임계값만이 근 수를 바꾼다.
original_f = x**3/2-R(9, 2)*x**2+10*x
assert s.factor(original_f+x) == x*(x**2-9*x+22)/2
assert s.discriminant(x**2-9*x+22, x) == -7
old_left, old_right = -7*x, s.expand(2*original_f-5*x)
assert old_right == x**3-9*x**2+15*x
assert s.solve(s.diff(old_right, x), x) == [1, 5]
assert [old_right.subs(x, v) for v in [1, 5]] == [7, -25]
old_cells = [(-26, 0), (-25, 1), (-1, 2), (0, 3), (1, 4), (7, 3), (8, 2)]
for height, expected in old_cells:
    assert count(old_left, old_right, height) == expected
# 단조성과 경계값에서 네 근 ⇔ 0<k<7. 가능한 정수 전수 조사.
old_integers = [v for v in range(1, 7) if count(old_left, old_right, v) == 4]
assert old_integers == [1, 2, 3, 4, 5, 6] and sum(old_integers) == 21
print('원문 M56: 네 근 0<k<7, 정수 합 21 OK')

# (1) 절댓값의 두 부호를 모두 조사한다.
assert s.expand(z-(z+1)) == -1  # 이 가지로는 좌변 6 불가능
f1 = s.solve(z+(z+1)-6, z)[0]
assert f1 == R(5, 2) and f1+1 > 0
f = x**3/2+a*x**2+b*x
positive_h = 2*f+x-2*x**2
coefficients = s.solve([f.subs(x, 1)-f1, s.diff(positive_h, x).subs(x, 1)], (a, b), dict=True)
assert coefficients == [{a: -2, b: 4}]
f = f.subs(coefficients[0])
assert s.factor(f+x) == x*(x**2-4*x+10)/2
assert s.expand((x-2)**2+6) == x**2-4*x+10
left, right = -2*x**2-x, s.expand(2*f+x-2*x**2)
assert right == x*(x-3)**2 or s.expand(right-x*(x-3)**2) == 0
assert s.solve(s.diff(left, x), x) == [-R(1, 4)]
assert s.solve(s.diff(right, x), x) == [1, 3]
assert left.subs(x, -R(1, 4)) == R(1, 8)
assert [right.subs(x, v) for v in [0, 1, 3]] == [0, 4, 0]
assert s.expand(left+2*(x+R(1, 4))**2-R(1, 8)) == 0
assert s.expand(s.diff(right, x)-3*(x-3)*(x-1)) == 0

# 모든 실수 k를 덮는 구간과 경계. 끝점 높이·극값 이외에서는 근 수가 일정하다.
cells = [(-1, (1, 0)), (0, (1, 2)), (R(1, 16), (2, 3)),
         (R(1, 8), (1, 3)), (1, (0, 3)), (4, (0, 2)), (5, (0, 1))]
four_root_cells = []
for height, expected in cells:
    actual = (len(roots_on(left-height, True)), len(roots_on(right-height, False)))
    assert actual == expected
    if sum(actual) == 4:
        four_root_cells.append(height)
assert four_root_cells == [R(1, 8)]
k = four_root_cells[0]
negative = roots_on(left-k, True)
positive = roots_on(right-k, False)
assert negative == [-R(1, 4)] and len(positive) == 3
poly = s.Poly(right-k, x)
assert len(set(poly.real_roots(radicals=False))) == 3
positive_sum = -poly.all_coeffs()[1]/poly.LC()
answer3 = positive_sum + negative[0]
assert positive_sum == 6 and answer3 == R(23, 4)
assert it['ans'] == ['(1) 4', r'(2) \frac18', r'(3) \frac{23}{4}']
assert [pts for _, pts in it['subs']] == ['4점, 답만 적으시오.', '4점, 답만 적으시오.', '2점, 답만 적으시오.']
print('S2: 모든 k 구간 근 수 1/3/5/4/3/2/1, 유일한 k=1/8 OK')
print('S2 정답: (1) 4, (2) 1/8, (3) 23/4 OK')

# 오답 근거를 실제 식으로 재현한다.
bad_coefficients = s.solve([a+b-2, 2*a+b+2], (a, b))
assert bad_coefficients[b] == 6
assert count(left, right, 0) == 3 and count(left, right, 4) == 2
assert positive_sum+2*negative[0] == R(11, 2)
assert not it['wrongs'] and not it.get('choices')
print('오답 b=6, k=0/4, 근의 합 11/2 근거 OK (서답형: 선지 검사 해당 없음)')


def local_values(av, bv, leading=R(1, 2), constant=0):
    ff = leading*x**3+av*x**2+bv*x+constant
    assert ff.subs(x, 1)+1 > 0
    hh = 2*ff+x-2*x**2
    return hh.subs(x, 1), s.diff(hh, x).subs(x, 1)


assert local_values(-3, 6) == (6, 0)
print('ABLATION S2 h(1)=4: 필요(a=-3,b=6이면 h\'(1)=0 유지, b=6)')
assert local_values(-1, 3) == (4, 2)
print('ABLATION S2 h\'(1)=0: 필요(a=-1,b=3이면 h(1)=4 유지, b=3)')
assert local_values(-3, R(9, 2), leading=1) == (4, 0)
print('ABLATION S2 삼차항 계수 1/2: 필요(계수 1이면 a=-3,b=9/2 가능)')
assert local_values(-1, 2, constant=1) == (4, 0)
print('ABLATION S2 상수항 0: 필요(상수항 1이면 a=-1,b=2 가능)')
assert count(left, right, 1) == 3 and 1 != k
print('ABLATION S2 (2) 실근 네 개: 필요(k=1 등 여러 값 가능)')
print('ALL OK')
