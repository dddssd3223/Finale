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


# 1: f'(-1)=0 and f(-1)=6 are two independent linear equations, so a and b
# are unique; a>0 makes x=-1 a maximum and x=1 the minimum.
f = a*x**3+b*x+a
sol = s.solve([s.diff(f, x).subs(x, -1), f.subs(x, -1)-6], [a, b], dict=True)
assert sol == [{a: 2, b: -6}]
f = f.subs(sol[0])
assert s.solve(s.diff(f, x), x) == [-1, 1]
assert s.diff(f, x, 2).subs(x, -1) < 0 < s.diff(f, x, 2).subs(x, 1)
fd = a*x**3+b*x   # mistake: constant term a dropped in f(-1)
sd = s.solve([s.diff(fd, x).subs(x, -1), fd.subs(x, -1)-6], [a, b], dict=True)[0]
check(1, f.subs(x, 1), 2, {'-3': (a*x**3+b*x+a).subs(sd).subs(x, 1)})
# ablation 1
fa = a*x**3+b*x+a
w = (fa.subs({a: 1, b: -3})).subs(x, 1)   # drop max value 6: a=1 also has max at -1
assert w != f.subs(x, 1)
print(f'ABLATION 1 극댓값 6: 필요(a=1이면 극솟값 {w})')
mins = []
for av in (1, 2):   # drop 'x=-1에서 극대': only the max value 6 remains
    bv = s.symbols('bv', negative=True)
    x0 = -s.sqrt(-bv/(3*av))
    bs = [v for v in s.solve(s.Eq((av*x**3+bv*x+av).subs(x, x0), 6), bv) if v.is_real and v < 0]
    assert len(bs) == 1
    mins.append(s.simplify(2*av-6))   # f-a odd: min = 2a - max
assert len(set(mins)) == 2
print(f'ABLATION 1 x=-1에서 극대: 필요(극솟값 {mins} 로 정해지지 않음)')
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
# continuity makes the sign constant, and |f| is even.
inner, outer = s.symbols('inner outer')
solution = s.solve([outer-1, -inner-outer-3], [inner, outer], dict=True)
assert solution == [{inner: -4, outer: 1}]
I0, I1 = solution[0][inner], solution[0][outer]
answer = 2*abs(I0)+abs(I1)
check(7, answer, 4, {'7': abs(I0)+abs(I0+I1), '10': 2*(abs(I0)+abs(I1))})


def absint(g, lo=-2, hi=4):
    rs = sorted({r for r in s.real_roots(s.Poly(g, x)) if lo < r < hi})
    pts = [lo]+rs+[hi]
    return sum(abs(s.integrate(g, (x, pts[i], pts[i+1]))) for i in range(len(pts)-1))


def odd_witness(i0, i1):
    """odd f = -x(x^2-4)(x^2-16)((x^2-11)^2+e) scaled, int_0^2=i0, int_2^4=i1."""
    e = s.symbols('e')
    base = -x*(x*x-4)*(x*x-16)*((x*x-11)**2+e)
    A, B = s.integrate(base, (x, 0, 2)), s.integrate(base, (x, 2, 4))
    ev = [v for v in s.solve(A*i1-B*i0, e) if v.is_real and v > 0]
    assert len(ev) == 1
    g = s.expand(base.subs(e, ev[0]))
    g = s.expand(g*i1/s.integrate(g, (x, 2, 4)))
    assert s.expand(g+g.subs(x, -x)) == 0
    assert sorted(r for r in s.real_roots(s.Poly(g, x)) if r > 0) == [2, 4]
    return g


def conds(g):
    return dict(odd=s.expand(g+g.subs(x, -x)) == 0,
                n1=s.integrate(g, (x, -2, 4)) == 1, n2=s.integrate(g, (x, -4, 0)) == 3,
                zeros=sorted(set(r for r in s.real_roots(s.Poly(g, x)) if r > 0)) == [2, 4])


witness = odd_witness(I0, I1)   # all conditions consistent, value 9
assert all(conds(witness).values()) and absint(witness) == answer
assert witness.subs(x, 1) < 0 < witness.subs(x, 3)
# ablation 7: drop one condition at a time, a polynomial meeting the rest
p, q = s.symbols('p q')
g = (x-2)*(x-4)*(p+q*x*x)
g = s.expand(g.subs(s.solve([s.integrate(g, (x, -2, 4))-1, s.integrate(g, (x, -4, 0))-3], [p, q])))
c = conds(g); assert not c['odd'] and c['n1'] and c['n2'] and c['zeros']
assert absint(g) != answer
print(f'ABLATION 7 (가): 필요(기함수 아닌 예 값 {float(absint(g)):.4f})')
g = odd_witness(-5, 2)
c = conds(g); assert not c['n1'] and c['n2'] and c['zeros'] and absint(g) != answer
print(f'ABLATION 7 (나) 첫째 적분: 필요(값 {absint(g)})')
g = odd_witness(-3, 1)
c = conds(g); assert c['n1'] and not c['n2'] and c['zeros'] and absint(g) != answer
print(f'ABLATION 7 (나) 둘째 적분: 필요(값 {absint(g)})')
g = x*(x*x-4)*(x*x-9)*(x*x-16)*(p+q*x*x)
g = s.expand(g.subs(s.solve([s.integrate(g, (x, 2, 4))-1, s.integrate(g, (x, -4, 0))-3], [p, q])))
c = conds(g); assert c['odd'] and c['n1'] and c['n2'] and not c['zeros']
assert abs(float(absint(g))-9) > 1e-6
print(f'ABLATION 7 (다): 필요(양의 근이 더 있으면 값 {float(absint(g)):.4f})')
old = s.solve([outer-3, -inner-outer-5], [inner, outer])
original('J45', 2*(abs(old[inner])+abs(old[outer])))
print('ALL OK')
