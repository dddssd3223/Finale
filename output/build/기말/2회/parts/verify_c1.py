"""정답, 선지, 오답 산식, 원문 및 다항함수의 존재 검증."""
from pathlib import Path
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'output/build/부교재_기말'))
import items_final as F
ITEMS = runpy.run_path(str(HERE / 'c1.py'))['ITEMS']
x, a, b, k = s.symbols('x a b k', real=True)


def number(raw):
    raw = str(raw).replace(' ', '')
    m = re.fullmatch(r'(-?)\\(?:dfrac|frac)\{?(\d+)\}?\{?(\d+)\}?', raw)
    if m:
        return (-1 if m[1] else 1) * s.Rational(m[2], m[3])
    return s.Rational(raw)


def check(n, result, expected, mistakes):
    it = ITEMS[n]
    vals = list(map(number, it['choices']))
    assert len(vals) == len(set(vals)) == 5
    assert len(set(vals[i + 1] - vals[i] for i in range(4))) == 1
    assert vals[1] > vals[0]
    assert it['ans'] == expected and result == vals[expected - 1]
    assert vals.count(result) == 1
    assert set(it['wrongs']) == set(mistakes)
    for text, value in mistakes.items():
        assert text in it['choices'] and number(text) == value != result
    assert it['author'] == 'codex'
    print(f'{n}: answer={result}, index={expected}, choices/wrongs OK')


def original(key, result):
    _, choices, answer, _ = F.I[key]
    want = number(choices['①②③④⑤'.index(answer)]) if answer in '①②③④⑤' else number(answer)
    assert result == want, (key, result, want)
    print(f'ORIGINAL {key}: {result} OK')


# 1: the two independent equations uniquely fix a and b; derivative signs
# distinguish the maximum from the minimum.
f = a*x**3+b*x+a
sol = s.solve([s.diff(f, x).subs(x, 1), f.subs(x, 1)+1], [a, b], dict=True)
assert sol == [{a: 1, b: -3}]
f = f.subs(sol[0])
assert s.solve(s.diff(f, x), x) == [-1, 1]
assert s.diff(f, x, 2).subs(x, -1) < 0 < s.diff(f, x, 2).subs(x, 1)
check(1, f.subs(x, -1), 2, {'2': (f-1).subs(x, -1)})
fo = a*x**3+b*x+a
so = s.solve([s.diff(fo, x).subs(x, 1), fo.subs(x, 1)+2], [a, b])
original('D17', fo.subs(so).subs(x, -1))

# 3: pair x and -x. This algebra holds for arbitrary f, not just sampled
# polynomial degrees. The remaining integral is 2*given + int(2-2x).
y = s.symbols('y')
pair = s.expand((x+1)*y+(1-x)*(2-y))
assert pair == 2*x*y-2*x+2
answer = 2+s.integrate(2-2*x, (x, 0, 1))
# A witness checks that the conditions are consistent.
fw = 1+s.Rational(3, 2)*x
assert s.expand(fw+fw.subs(x, -x)) == 2
assert s.integrate(x*fw, (x, 0, 1)) == 1
check(3, answer, 1, {'4': 2*1+2})
assert s.expand((x+2)**2*y+(-x+2)**2*(-y)) == 8*x*y
original('I29', 8*s.Integer(3))

# 5: k>2 fixes the order of all zeros, hence the two integrals have
# opposite signs. The integral equation has precisely one admissible root.
f = (x+1)*(x-2)*(x-k)**2
area_difference = s.factor(s.integrate(f, (x, -1, k)))
assert area_difference == (k+1)**4*(2*k-13)/60
roots = s.solve(area_difference, k)
admissible = [v for v in roots if v > 2]
assert admissible == [s.Rational(13, 2)]
fv = f.subs(k, admissible[0])
A = -s.integrate(fv, (x, -1, 2))
B = s.integrate(fv, (x, 2, admissible[0]))
assert A == B and A > 0
check(5, admissible[0], 5, {'5': s.solve(s.Eq((-1+k)/2, 2), k)[0]})
fo = x**2*(x-2)*(x-k)
original_roots = [v for v in s.solve(s.integrate(fo, (x, 0, k)), k) if v > 2]
assert len(original_roots) == 1
original('J20', original_roots[0])

# 7: oddness cancels the symmetric interval. Between consecutive zeros
# continuity makes the sign constant, so these two integrals determine area.
inner, outer = s.symbols('inner outer')
solution = s.solve([outer-1, -inner-outer-3], [inner, outer], dict=True)
assert solution == [{inner: -4, outer: 1}]
answer = 2*(abs(solution[0][inner])+abs(solution[0][outer]))
check(7, answer, 4, {'6': 2*abs(solution[0][inner]+solution[0][outer])})
# A globally positive even factor guarantees no unwanted real zeros.
positive = (x*x-11)**2+s.Rational(823, 485)
base = -x*(x*x-4)*(x*x-16)*positive
scale = -4/s.integrate(base, (x, 0, 2))
witness = s.expand(scale*base)
assert scale > 0 and s.Rational(823, 485) > 0
assert s.expand(witness+witness.subs(x, -x)) == 0
assert s.integrate(witness, (x, -2, 4)) == 1
assert s.integrate(witness, (x, -4, 0)) == 3
# Thus its only positive roots are 2 and 4, and the required signs hold.
assert witness.subs(x, 1) < 0 < witness.subs(x, 3)
old = s.solve([outer-3, -inner-outer-5], [inner, outer])
original('J45', 2*(abs(old[inner])+abs(old[outer])))
print('ALL OK')
