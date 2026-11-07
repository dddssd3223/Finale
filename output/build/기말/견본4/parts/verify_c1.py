# -*- coding: utf-8 -*-
"""2·4·6·8: 정답/유일성/지정 번호/등차/오답 네 개/부교재 원문 검증."""
from pathlib import Path
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
IT = runpy.run_path(str(HERE / 'c1.py'))['ITEMS']
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F
x, a, k = s.symbols('x a k', real=True)
assert set(IT) == {2, 4, 6, 8}

def check(n, answer, pos, errors):
    it = IT[n]
    cs = list(map(s.sympify, it['choices']))
    assert it['author'] == 'codex' and it['ans'] == pos
    assert len(cs) == len(set(cs)) == 5
    assert len({cs[j+1]-cs[j] for j in range(4)}) == 1
    assert cs[pos-1] == answer and cs.count(answer) == 1
    assert set(errors) == set(cs) - {answer}
    print(f'{n}: answer={answer}, position={pos}, AP={cs}, all distractors={errors}: OK')

def original(key, value, expected, label):
    assert s.simplify(value-expected) == 0
    assert F.I[key][2] == label
    print(f'ORIGINAL {key}: {value}, stored answer {label}: OK')

# 2: 닫힌 반직선의 모든 후보. 무한대에서는 발산하고 내부 정지점은 2뿐이다.
p = x**3-3*x**2+9
critical = s.solve(s.diff(p, x), x)
assert critical == [0, 2] and s.limit(p, x, s.oo) == s.oo
minimum = min(p.subs(x, t) for t in critical)
assert minimum == 5 and s.factor(p-minimum) == (x-2)**2*(x+1)
answer = minimum-1
check(2, answer, 5, [p.subs(x, 0)-1, p.subs(x, 1), p.subs(x, 1)-1, minimum])
po = 2*x**3-6*x**2+14
mins = [po.subs(x, t) for t in [0]+s.solve(s.diff(po, x), x) if t >= 0]
original('M11', min(mins)-1, s.Integer(5), '②')

# 4: 삼차함수의 전 구간 단조성. D=0에서도 상수 구간은 생기지 않는다.
d = x*x-2*a*x+4*a
region = s.solve_univariate_inequality(d.subs(x, a) >= 0, a, relational=False)
assert region == s.Interval(0, 4)
allowed = list(range(5))
for aa in allowed:
    assert s.minimum(d.subs(a, aa), x, s.S.Reals) >= 0
    assert not s.Poly(d.subs(a, aa), x).is_zero
check(4, s.Integer(len(allowed)), 4, [2, len(range(1, 4)), len(range(1, 5)), len(range(6))])
ro = s.solve_univariate_inequality(3*a-a*a >= 0, a, relational=False)
original('D54', ro.end, s.Integer(3), '①')

# 6: 세 실근 전후의 모든 부호 구간. 오른쪽 무한 영역은 넓이 대상에서 제외.
f = x*(x+2)*(x-3)
assert s.solve(f, x) == [-2, 0, 3]
assert [s.sign(f.subs(x, q)) for q in [-3, -1, 1, 4]] == [-1, 1, -1, 1]
area = 2*s.integrate(f, (x, -2, 0))
assert area == s.Rational(32, 3)
wrong_drop_quadratic = 3*2*s.integrate(x**3-6*x, (x, -2, 0))
check(6, 3*area, 3, [0, 3*area/2, wrong_drop_quadratic, 6*area])
fo = x*(x+2)*(x-k)
ko = s.solve(2*s.integrate(fo, (x, -2, 0))-6, k)
assert ko == [s.Rational(5, 4)]
original('J4', ko[0], s.Rational(5, 4), '②')

# 8: 경계 k=-4,0,4 및 그 사이 구간을 모두 조사한다.
h = 2*x**3-6*x
assert s.expand(s.diff(h, x)-6*(x-1)*(x+1)) == 0
assert [h.subs(x, q) for q in [-1, 0, 1]] == [4, 0, -4]
def counts(poly):
    roots = set(s.Poly(poly, x).real_roots())
    return (sum(bool(r > 0) for r in roots), sum(bool(r < 0) for r in roots))
cases = {kk: counts(h-kk) for kk in range(-5, 6)}
assert cases[-4] == (1, 1) and cases[0] == (1, 1) and cases[4] == (1, 1)
valid = [kk for kk, c in cases.items() if c == (2, 1)]
assert valid == [-3, -2, -1]
# 범위 밖은 극값의 범위 밖이므로 실근이 하나뿐이다. 위 범위가 후보를 모두 포함한다.
check(8, s.Integer(len(valid)), 1, [len(valid)+1, len(valid)+2, 2*len(valid), 2*len(valid)+1])
ho = 2*x**3+3*x**2-12*x
assert s.solve(s.diff(ho, x), x) == [-2, 1]
assert [ho.subs(x, q) for q in [-2, 0, 1]] == [20, 0, -7]
vo = [kk for kk in range(-7, 21) if s.prod(counts(ho-kk)) == 2]
original('M13', s.Integer(len(vo)), s.Integer(25), '⑤')
print('ALL OK')
