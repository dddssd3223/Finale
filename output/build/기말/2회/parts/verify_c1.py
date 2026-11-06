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

# 3: f(-x)=-f(x)+8 means h=f-4 is odd. Take a general odd polynomial h of
# degree up to 11 with symbolic coefficients, impose int_0^1 x f = 1, and the
# value never depends on the remaining coefficients (answer unique).
cs = s.symbols('c0:6')
h = sum(cv*x**(2*i+1) for i, cv in enumerate(cs))
f3 = 4+h
assert s.expand(f3.subs(x, -x)-(-f3+8)) == 0
# Conversely f(-x)=-f(x)+8 forces the even part of f-4 to vanish, so f3 covers all f.
c0 = s.solve(s.integrate(x*f3, (x, 0, 1))-1, cs[0])[0]
val3 = s.expand(s.integrate((3*x**2+x+1)*f3, (x, -1, 1)).subs(cs[0], c0))
assert val3 == 14 and not val3.free_symbols
xh = s.Integer(1)-s.integrate(4*x, (x, 0, 1))          # int_0^1 x h = 1-2 = -1
E3 = 4*s.integrate(3*x**2+x+1, (x, -1, 1))              # 16
assert E3+2*xh == val3
mist3 = {'18': E3+2*1,          # 보정 누락: int_0^1 x(f-4) taken as 1
         '15': E3+xh,           # 2배 누락: int_{-1}^1 xh = int_0^1 xh
         '16': E3}              # 홀수 차수 항까지 소거
check(3, val3, 1, mist3)
assert E3+1 == 17 and E3+1 not in mist3.values()   # 두 실수 겹침(17)은 정답과 다름
# 검토안(+2, int_0^1 xf=1, 3x²+2x+1)은 보정 누락+2배 누락을 겹치면 정답과 같아져 피했다.
rv_ok = 4+2*2*(1-s.Rational(1, 2)); rv_both = 4+2*1
assert rv_ok == rv_both == 6
# ablation 3
fe = 3*x   # int_0^1 x·3x = 1 but f(-x)=-f(x) (상수 0): 대칭 조건을 바꾸면 값이 달라짐
va = s.integrate((3*x**2+x+1)*fe, (x, -1, 1))
assert s.integrate(x*fe, (x, 0, 1)) == 1 and va != val3
print(f'ABLATION 3 f(-x)=-f(x)+8: 필요(f=3x이면 값 {va})')
fe = 3*x**2+s.Rational(1, 4)   # 짝함수 예, int_0^1 x f = 3/4+1/8 ≠ 1 → scale
fe = fe/s.integrate(x*fe, (x, 0, 1))
assert s.integrate(x*fe, (x, 0, 1)) == 1
va = s.integrate((3*x**2+x+1)*fe, (x, -1, 1))
assert va != val3
print(f'ABLATION 3 f(-x)=-f(x)+8: 필요(짝함수 예에서 값 {va})')
for cv in (0, 2):
    fv = 4+s.Rational(3*(cv-2), 1)*x   # int_0^1 x f = 2+(cv-2) = cv
    assert s.integrate(x*fv, (x, 0, 1)) == cv
    va = s.integrate((3*x**2+x+1)*fv, (x, -1, 1))
    assert va != val3
    print(f'ABLATION 3 ∫₀¹xf=1: 필요(∫₀¹xf={cv}이면 값 {va})')
fo = sum(cv*x**(2*i+1) for i, cv in enumerate(cs))
oc = s.solve(s.integrate(x*fo, (x, 0, 1))-3, cs[0])[0]
original('I29', s.expand(s.integrate((x+2)**2*fo, (x, -1, 1)).subs(cs[0], oc)))

# 5: 0<k<5 gives -5<-k<0 with the double root 0 at the RIGHT end; the curve is
# negative on (-5,-k) and positive on (-k,0), so equal areas <=> int_{-5}^0 = 0.
f = x**2*(x+k)*(x+5)
area_difference = s.factor(s.integrate(f, (x, -5, 0)))
assert s.expand(area_difference-625*(k-3)/12) == 0
split = s.Rational(5**5, 30)+(k-5)*s.Rational(5**4, 12)   # 계산 정리: x+k=(x+5)+(k-5)
assert s.expand(split-area_difference) == 0
assert s.integrate(x**2*(x+5)**2, (x, -5, 0)) == s.Rational(5**5, 30)
assert s.integrate(x**2*(x+5), (x, -5, 0)) == s.Rational(5**4, 12)
admissible = [v for v in s.solve(area_difference, k) if 0 < v < 5]
assert admissible == [3]
fv = f.subs(k, 3)
assert fv.subs(x, -4) < 0 < fv.subs(x, -1)
A = -s.integrate(fv, (x, -5, -3))
B = s.integrate(fv, (x, -3, 0))
assert A == B and A > 0
# 위치 비: 중근 0에서 잰 거리 0, k, 5 → k:5 = 3:5
assert s.solve(s.Eq(k/5, s.Rational(3, 5)), k) == [3]
check(5, admissible[0], 5, {
    '2': s.solve(s.Eq((5-k)/5, s.Rational(3, 5)), k)[0],      # 왼쪽 근 -5에서 0:3:5
    r'\dfrac52': s.solve(s.Eq(-k, s.Rational(-5, 2)), k)[0]})  # 삼차 중점 규칙

# ablation 5: without 0<k<5 another k works, so the 단서 is needed.
# k>5: zeros -k<-5<0, double root 0 at the right end.
big = [v for v in s.solve(s.integrate(f, (x, -k, 0)), k) if v.is_real and v > 5]
assert big == [s.Rational(25, 3)]
fb = f.subs(k, big[0])
assert -s.integrate(fb, (x, -big[0], -5)) == s.integrate(fb, (x, -5, 0)) > 0
# k<0: zeros -5<0<-k, double root in the middle, both parts below the axis.
P1 = -s.integrate(f, (x, -5, 0)); P2 = -s.integrate(f, (x, 0, -k))
neg = [v for v in s.solve(s.expand(P1-P2), k) if v.is_real and v < 0 and v != -5]
assert neg == []
print('ABLATION 5 (단, 0<k<5): 필요(없으면 k=25/3도 두 넓이가 같음)')
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
