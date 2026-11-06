"""9·11·13·15번 및 원문 검증. 15번은 모든 이동량과 조건 제거를 검사."""
from pathlib import Path
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'output/build/부교재_기말'))
import items_final as F
ITEMS = runpy.run_path(str(HERE / 'c2.py'))['ITEMS']
x, t, p, q, c, m, n, b = s.symbols('x t p q c m n b', real=True)


def number(raw):
    raw = str(raw).replace(' ', '')
    z = re.fullmatch(r'(-?)\\(?:dfrac|frac)\{?(\d+)\}?\{?(\d+)\}?', raw)
    if z:
        return (-1 if z[1] else 1)*s.Rational(z[2], z[3])
    return s.Rational(raw)


def check(no, result, expected, mistakes):
    it = ITEMS[no]
    vals = list(map(number, it['choices']))
    assert len(vals) == len(set(vals)) == 5
    assert len(set(vals[i+1]-vals[i] for i in range(4))) == 1
    assert vals[1] > vals[0]
    assert it['ans'] == expected and result == vals[expected-1]
    assert vals.count(result) == 1
    assert set(it['wrongs']) == set(mistakes)
    for text, value in mistakes.items():
        assert text in it['choices'] and number(text) == value != result
    assert it['author'] == 'codex'
    print(f'{no}: answer={result}, index={expected}, choices/wrongs OK')


def original(key, result):
    _, choices, answer, _ = F.I[key]
    want = number(choices['①②③④⑤'.index(answer)]) if answer in '①②③④⑤' else number(answer)
    assert result == want, (key, result, want)
    print(f'ORIGINAL {key}: {result} OK')


# 9: determine the cubic, then independently check the two shaded areas.
family = (x-1)*(x-2)*(x+c)
diff = s.simplify(3*family.subs(x, 3)/2-s.integrate(family, (x, 0, 3)))
assert diff == s.Rational(27, 4)+3*c/2
cs = s.solve(diff-s.Rational(51, 4), c)
assert cs == [4]                                  # B-A가 c의 일차식 → 해 하나
f = s.expand(family.subs(c, cs[0]))
line = f.subs(x, 3)*x/3
intersections = s.solve(f-line, x)
inside = [v for v in intersections if 0 < v < 3]
assert len(inside) == 1
u = inside[0]
assert (f-line).subs(x, 0) > 0 and (f-line).subs(x, 1) < 0
A = s.integrate(f-line, (x, 0, u))
B = s.integrate(line-f, (x, u, 3))
assert A > 0 and B > 0 and s.simplify(B-A-s.Rational(51, 4)) == 0
answer = f.subs(x, 0)
assert answer == 8
check(9, answer, 3, {'4': cs[0]})
old_c = s.solve(s.diff(family, x).subs(x, 0)+7, c)
assert old_c == [3]
original('J58', diff.subs(c, old_c[0]))

# 11: x=0 in xg(x)=H(x) gives H(0)=int|t|f=0 for any function g.
# f(0)=-3 leaves f=pt^2+rt-3; |t|·rt is odd, so H(0)=0 fixes p=6 and r is free.
# Outside [-1,1] |x-t| has one sign: x>=1 → xg=Bx-A, x<=-1 → xg=A-Bx.
r = s.symbols('r', real=True)
ft = p*t*t+r*t-3
H0 = s.integrate(-t*ft, (t, -1, 0))+s.integrate(t*ft, (t, 0, 1))
assert s.expand(H0-2*s.integrate(t*(p*t*t-3), (t, 0, 1))) == 0   # r drops
ps = s.solve(H0, p)
assert ps == [6]
f11 = ft.subs(p, 6)
A = s.integrate(t*f11, (t, -1, 1)); B = s.integrate(f11, (t, -1, 1))
assert A == 2*r/3 and B == -2
g2 = s.integrate((2-t)*f11, (t, -1, 1))/2        # |2-t| = 2-t on [-1,1]
gm2 = s.integrate((t+2)*f11, (t, -1, 1))/(-2)    # |-2-t| = t+2 on [-1,1]
assert s.expand(g2-(B-A/2)) == 0 and s.expand(gm2-(-B-A/2)) == 0
ans11 = s.expand(g2-gm2)
assert ans11 == -4 and not ans11.free_symbols    # unique for every r
# numeric cross-check with the absolute value itself, several r
for rv in (-5, 0, s.Rational(7, 3)):
    fv = f11.subs(r, rv)
    for xv in (2, -2):
        Hv = s.integrate(s.Abs(xv-t)*fv, (t, -1, 1))
        assert s.simplify(Hv/xv-(g2 if xv == 2 else gm2).subs(r, rv)) == 0
# mistakes
same_side = s.expand(g2-(s.integrate((-2-t)*f11, (t, -1, 1))/(-2)))   # x-t at x=-2 too
assert s.expand(same_side+A) == 0 and same_side.subs(r, 0) == 0      # -A, then A=0 as in 원문
wrong_p = s.solve(s.integrate(p*t*t+r*t-3, (t, -1, 1)), p)[0]          # |t| dropped at x=0
assert wrong_p == 9 and 2*s.integrate((9*t*t+r*t-3), (t, -1, 1)) == 0
half = 2*s.integrate(f11, (t, 0, 1)).subs(r, 0)                         # B as int_0^1 f
check(11, ans11, 1, {'0': same_side.subs(r, 0), '-2': half})
# Existence: for every r, H(0)=0 and g(x)=H(x)/x (x≠0), g(0) any real value.
Hin = s.integrate((x-t)*f11, (t, -1, x))+s.integrate((t-x)*f11, (t, x, 1))
assert s.expand(Hin.subs(x, 0)) == 0
# ablation 11
pf, qf = s.symbols('pf qf')
fq = pf*t*t+r*t+qf
qq = s.solve(s.integrate(-t*fq, (t, -1, 0))+s.integrate(t*fq, (t, 0, 1)), qf)
assert qq == [-pf/2]
val = s.expand(2*s.integrate(fq.subs(qf, qq[0]), (t, -1, 1)))
assert val == -2*pf/3
print('ABLATION 11 f(0)=-3: 필요(f=p(t²-1/2)+rt이면 값 -2p/3, p 미정)')
u = s.symbols('u')
fu = u*t**4+p*t*t+r*t-3   # quartic with f(0)=-3
pu = s.solve(s.integrate(-t*fu, (t, -1, 0))+s.integrate(t*fu, (t, 0, 1)), p)[0]
valu = s.expand(2*s.integrate(fu.subs(p, pu), (t, -1, 1)))
assert valu.free_symbols == {u}
print(f'ABLATION 11 이차함수: 필요(사차이면 값 {valu}, 최고차항 계수에 따라 달라짐)')
print('ABLATION 11 식 xg(x)=…: 필요(없으면 g와 f의 관계가 없어 값 미정)')
# The reviewer's version (f\'(0)=0 kept, g(-2)-g(2)) would make f\'(0)=0 redundant:
assert s.expand(gm2-g2) == 4
print("NOTE 11 f'(0)=0을 두어도 g(-2)-g(2)=4는 r과 무관 → 군더더기라 뺐다")
old_ft = p*t*t+q
old_pq = s.solve([2*s.integrate(t*old_ft, (t, 0, 1)), s.integrate((t+2)*old_ft, (t, -1, 1))+4], [p, q])
original('I43', (4*p+q).subs(old_pq))

# 13: the integral quotient is m/2+n/x; a finite two-sided limit forces n=0.
quot = s.expand(s.integrate(m*t+n, (t, 0, x))/x**2)
assert quot == m/2+n/x
assert s.limit(quot.subs({m: 2, n: 0}), x, 0) == 1
gg = x*x+b*x+c
bc = s.solve([s.integrate(2*x*gg, (x, -1, 1))-s.Rational(4, 3),
              s.integrate(gg, (x, 0, 1))-s.Rational(11, 6)], [b, c], dict=True)
assert bc == [{b: 1, c: 1}]
wrong_c = s.solve(s.integrate(x*x+c, (x, 0, 1))-s.Rational(11, 6), c)[0]
check(13, 2*gg.subs(bc[0]).subs(x, 1), 2,
      {'5': 2*(1+wrong_c), '7': 2*(1+1+wrong_c)})
# Each independent equation is needed for the requested value.
assert 2*(1+0+wrong_c) == 5
print('ABLATION 13 첫 정적분: 필요(b=0이면 답 5)')
assert 2*(1+1+0) == 4
print('ABLATION 13 둘째 정적분: 필요(c=0이면 답 4)')
# Without (가), f=x, g=x²+2x+1/2 still satisfy both integrals, answer 7/2.
altg = x*x+2*x+s.Rational(1, 2)
assert s.integrate(x*altg, (x, -1, 1)) == s.Rational(4, 3)
assert s.integrate(altg, (x, 0, 1)) == s.Rational(11, 6)
assert altg.subs(x, 1) == s.Rational(7, 2)
print('ABLATION 13 극한 조건: 필요(f=x인 예에서 답 7/2)')
old_m = s.solve(s.integrate(m*x*s.diff(gg, x), (x, -1, 1))-8, m)[0]
old_b = s.solve(s.integrate(old_m*x*gg, (x, -1, 1)), b)[0]
original('I45', old_m*s.diff(gg, x).subs({b: old_b, x: 1}))


def shifts(S, target=5):
    """Outside pairwise positive differences no roots overlap: exhaustive."""
    candidates = sorted({v-u for u in S for v in S if v > u})
    counts = {d: len(S | {v+d for v in S}) for d in candidates}
    # All examples have 2*|S| != target, so only these candidates can work.
    assert 2*len(S) != target
    return [d for d in candidates if counts[d] == target], counts


# 15: first use continuity and matching derivatives, then f(2)=3.
right = p*x*x+b*x+c
rp = s.solve([right.subs(x, 0)-3, s.diff(right, x).subs(x, 0)-9,
              right.subs(x, 2)-3], [p, b, c], dict=True)
assert rp == [{p: -s.Rational(9, 2), b: 9, c: 3}]
left = x**3+6*x*x+9*x+3
S = {v for v in s.solve(s.diff(left, x), x) if v <= 0}
S |= {v for v in s.solve(s.diff(right.subs(rp[0]), x), x) if v > 0}
assert S == {-3, -1, 1}
valid, counts = shifts(S)
assert counts == {2: 4, 4: 5} and valid == [4]
check(15, sum(valid), 3, {'2': min(counts), '6': sum(counts)})
print(f'15 exhaustive shift counts: {counts}; all other positive shifts give 6')

# ABLATION of both labeled conditions, plus degree and k>0.
alternative = -s.Rational(9, 4)*x*x+9*x+3
assert alternative.subs(x, 0) == left.subs(x, 0)
assert s.diff(alternative, x).subs(x, 0) == s.diff(left, x).subs(x, 0)
assert alternative.subs(x, 2) != 3
valid_alt, _ = shifts({-3, -1, 2})
assert sum(valid_alt) == 10
print('ABLATION 15 (나): 필요(f=-9x²/4+9x+3이면 답 10)')
unjoined = -x*x+4*x-1
assert unjoined.subs(x, 2) == 3 and unjoined.subs(x, 0) != left.subs(x, 0)
# The derivative at 0 would not exist, so the equation loses its global
# definition; the derivatives on the two open pieces also give a different sum.
assert sum(shifts({-3, -1, 2})[0]) == 10
print('ABLATION 15 (가): 필요(f=-x²+4x-1이면 접합 실패로 g\'(0) 정의 불가; 열린 조각의 근으로도 합 10)')
# Without the quadratic restriction a cubic satisfies both labeled conditions
# but produces four stationary points whose pairwise gaps are all different.
derivative_cubic = s.Rational(54, 5)*(x-s.Rational(1, 2))*(x-s.Rational(5, 3))
cubic = 3+s.integrate(derivative_cubic.subs(x, t), (t, 0, x))
assert cubic.subs(x, 0) == 3 and derivative_cubic.subs(x, 0) == 9
assert cubic.subs(x, 2) == 3
assert shifts({-3, -1, s.Rational(1, 2), s.Rational(5, 3)})[0] == []
print('ABLATION 15 이차함수: 필요(삼차함수 반례는 조건을 만족하나 해당 이동량 없음)')
assert len(S | {v-4 for v in S}) == 5
assert sum([-4, 4]) == 0
print('ABLATION 15 k의 양수 조건: 필요(음수 -4까지 허용하면 합 0)')

# Original M66: the excluded discriminant-zero case leaves either one or
# three stationary points. One point yields two union elements, so there
# must be three; union size four forces a length-three chain of step four.
r = s.symbols('r', real=True)
# Two negative roots of 3x²+2ax+15 have product 5.
chain_starts = s.solve(r*(r+4)-5, r)
chains = [(v, v+4, v+8) for v in chain_starts if v < v+4 < 0 < v+8]
assert chains == [(-5, -1, 3)]
old_a = -s.Rational(3, 2)*sum(chains[0][:2])
old_p = -s.Rational(15, 2)/chains[0][2]
old_left = x**3+old_a*x*x+15*x+7
old_right = old_p*x*x+15*x+7
assert old_a != 3*s.sqrt(5) and old_p < 0
assert len(set(chains[0]) | {v+4 for v in chains[0]}) == 4
original('M66', old_left.subs(x, -2)+old_right.subs(x, 2))
print('ALL OK')
