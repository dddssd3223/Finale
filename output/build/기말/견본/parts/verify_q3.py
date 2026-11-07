# -*- coding: utf-8 -*-
# q3 (17·18번) 검증: sympy 기호 계산 + 수치 전수 스캔
import sympy as sp
import random
from fractions import Fraction

x, y, u, a, b, c, t = sp.symbols('x y u a b c t', real=True)
ns = {}
exec(open(__file__.replace('verify_q3.py', 'q3.py')).read(), ns)
ITEMS = ns['ITEMS']

def val(s):
    s = s.replace(r'\dfrac', '').replace('{', '(').replace('}', ')')
    if s.startswith('('):
        p, q = s[1:].split(')(')
        return sp.Rational(p) / sp.Rational(q.rstrip(')'))
    return sp.Rational(s)

def check_choices(no, expect):
    ch = [val(s) for s in ITEMS[no]['choices']]
    assert ch == sorted(ch) and len(set(ch)) == 5, ('선지 정렬', no, ch)
    assert ch[ITEMS[no]['ans'] - 1] == expect, ('정답 위치', no, ch, expect)
    print(f'{no}번 선지 {ch} 정답 {ITEMS[no]["ans"]}번 = {expect} OK')

# =====================================================================
# 17번
# f=x^4+ax^3+b, c>0, g=f (x<c), 4-f (x>=c), 연속
# (가) f(g(x)) 미분가능  (나) f(g(x))=f(0)의 서로 다른 실근 3개
# =====================================================================
print('=== 17번 ===')
f = x**4 + a*x**3 + b
fp = sp.diff(f, x)
# 연속: f(c)=2
bc = sp.solve(sp.Eq(f.subs(x, c), 2), b)[0]          # b = 2 - c^4 - a c^3
# x=c에서 f(g(x))의 좌미분 - 우미분 = f'(g(c))*f'(c) - f'(g(c))*(-f'(c))
jump = sp.factor(2 * fp.subs(x, 2) * fp.subs(x, c))
print('좌우 미분계수 차 =', jump)  # 0 ⇔ f'(c)=0 또는 f'(2)=0
sols_a = sp.solve(sp.Eq(jump, 0), a)
print('a 후보:', sols_a)
assert set(sols_a) == {-sp.Rational(8, 3), -sp.Rational(4, 3) * c}

def fg_roots_count(av, bv, cv, targets):
    """g(x)=yv (yv in targets)의 서로 다른 실근 수 (정확 계산)"""
    fx = x**4 + av*x**3 + bv
    roots = set()
    for yv in targets:
        for r in sp.Poly(sp.expand(fx - yv), x).real_roots():
            if sp.simplify(r - cv) < 0 or (r - cv).is_negative:
                roots.add(r)
        for r in sp.Poly(sp.expand(4 - fx - yv), x).real_roots():
            if not (r - cv).is_negative:
                roots.add(r)
    # 중복 제거(대수적 수 비교)
    uniq = []
    for r in roots:
        if all(sp.N(r - s, 50) != 0 for s in uniq):
            uniq.append(r)
    return len(uniq)

def count_nacond(av, cv, bv=None):
    if bv is None:
        bv = 2 - cv**4 - av*cv**3
    # 정확한 b가 주어지면 f(c)=2 확인
    assert abs(sp.N(cv**4 + av*cv**3 + bv - 2, 50)) < 1e-40
    # f(y)=f(0) ⇔ y^3(y+a)=0
    ys = sorted(set(sp.Poly(y**3*(y + av), y).real_roots()))
    return fg_roots_count(av, bv, cv, ys), bv

# Ⅰ. a=-4c/3: g 감소 일대일대응 → 실근 항상 2개
for cv in [Fraction(k, 8) for k in range(1, 41)]:
    cv = sp.Rational(cv.numerator, cv.denominator)
    av = -sp.Rational(4, 3) * cv
    n, _ = count_nacond(av, cv)
    assert n == 2, (cv, n)
print('경우 Ⅰ (f\'(c)=0): c=1/8~5 전 구간에서 실근 2개 → 부적합')

# Ⅱ. a=-8/3, c 변화: 실근 3개인 c는 경계값뿐임을 확인
av = -sp.Rational(8, 3)
cnts = {}
for k in range(1, 321):
    cv = sp.Rational(k, 64)       # 0<c<=5
    if cv == 2:
        continue
    n, _ = count_nacond(av, cv)
    cnts.setdefault(n, []).append(cv)
print('경우 Ⅱ 격자 c(1/64 간격) 실근 개수 분포:', {k: len(v) for k, v in cnts.items()})
assert 3 not in cnts  # 3개는 고립된 c에서만
# 정확한 경계: c<2에서 4-f(2)=8/3, c>2에서 f(2)=0
fA = 3*c**4 - 8*c**3 + 14   # b=20/3, f(c)=2
fB = 3*c**4 - 8*c**3 + 10   # b=16/3, f(c)=2
cA = [r for r in sp.Poly(fA, c).real_roots() if 0 < r < 2]
cB = [r for r in sp.Poly(fB, c).real_roots() if r > 2]
assert len(cA) == 1 and len(cB) == 1, (cA, cB)
nA, bA = count_nacond(av, cA[0], sp.Rational(20, 3)); nB, bB = count_nacond(av, cB[0], sp.Rational(16, 3))
print('c_A =', sp.N(cA[0], 8), 'b =', sp.nsimplify(sp.N(bA, 30)), '실근', nA)
print('c_B =', sp.N(cB[0], 8), 'b =', sp.nsimplify(sp.N(bB, 30)), '실근', nB)
assert nA == 3 and nB == 3
assert abs(sp.N(bA - sp.Rational(20, 3), 40)) < 1e-30 and abs(sp.N(bB - sp.Rational(16, 3), 40)) < 1e-30
# 그 외 경계값(실근 개수가 바뀌는 c)도 모두 조사: b에 대한 조건 M=8/3, m=0, m=8/3, m=...
# 경우 Ⅱ의 b(c)=2-c^4+8c^3/3, f(2)=b-16/3. 개수 변화는 극값 4-f(2) 또는 f(2)가 0, 8/3과 같아질 때뿐
crit = []
bconst = [sp.Rational(20, 3), sp.Rational(28, 3), sp.Rational(16, 3), sp.Rational(8, 1)]
for bk, expr in zip(bconst, [4 - (bc.subs(a, av) - sp.Rational(16, 3)) - sp.Rational(8, 3),   # 극댓값(c<2) = 8/3
             4 - (bc.subs(a, av) - sp.Rational(16, 3)),                        # 극댓값(c<2) = 0
             bc.subs(a, av) - sp.Rational(16, 3),                              # 극솟값(c>2) = 0
             bc.subs(a, av) - sp.Rational(16, 3) - sp.Rational(8, 3)]):        # 극솟값(c>2) = 8/3
    crit += [(r, bk) for r in sp.Poly(sp.expand(expr), c).real_roots() if r > 0 and r != 2]
ok = []
for r, bk in crit:
    n, bv = count_nacond(av, r, bk)
    print('   경계 c =', sp.N(r, 6), 'b =', bk, '실근', n)
    if n == 3:
        ok.append(sp.nsimplify(sp.N(bv, 30)))
print('경계 c에서 실근 3개가 되는 b:', ok)
assert sorted(ok) == [sp.Rational(16, 3), sp.Rational(20, 3)]

# (가) 역방향 수치 확인: f'(c)f'(2)≠0이면 미분 불가능
random.seed(1)
for _ in range(300):
    av_ = random.uniform(-6, 3); cv_ = random.uniform(0.1, 4)
    bv_ = 2 - cv_**4 - av_*cv_**3
    F = lambda z: z**4 + av_*z**3 + bv_
    G = lambda z: F(z) if z < cv_ else 4 - F(z)
    h = 1e-6
    dl = (F(G(cv_)) - F(G(cv_ - h))) / h
    dr = (F(G(cv_ + h)) - F(G(cv_))) / h
    prod = (4*cv_**3 + 3*av_*cv_**2) * (32 + 12*av_)
    if abs(prod) > 1e-2:
        assert abs(dl - dr) > 1e-4, (av_, cv_)
print('(가) 수치 확인: f\'(c)f\'(2)≠0인 무작위 300개 모두 미분 불가능')

f1 = [ (x**4 - sp.Rational(8, 3)*x**3 + bv).subs(x, 1) for bv in (sp.Rational(20, 3), sp.Rational(16, 3))]
print('f(1) 후보:', f1, '합', sum(f1))
assert sum(f1) == sp.Rational(26, 3)
check_choices(17, sp.Rational(26, 3))

# =====================================================================
# 18번
# f=-x^3+x, a>0, b 실수
# (가) y=f(x), y=f(x-a)+b 가 서로 다른 두 점에서 만남
# (나) A(-1,0)을 지나고 y=f(x)에 접하는 직선 l이 두 교점의 중점을 지남
# =====================================================================
print('=== 18번 ===')
f = -x**3 + x
C2 = f.subs(x, x - a) + b
D = sp.expand(C2 - f)                     # 3a x^2 - 3a^2 x + a^3 - a + b
print('두 곡선의 차:', sp.factor(D))
# A를 지나는 접선: 접점 t
tl = sp.solve(sp.Eq(0, sp.diff(f, x).subs(x, t)*(-1 - t) + f.subs(x, t)), t)
print('A를 지나는 접선의 접점:', tl)
assert set(tl) == {-1, sp.Rational(1, 2)}
lines = {tv: sp.expand(sp.diff(f, x).subs(x, tv)*(x - tv) + f.subs(x, tv)) for tv in set(tl)}
print('접선:', lines)
# 두 교점의 중점 (기호): 근 α, β
al, be = sp.symbols('alpha beta')
r1, r2 = sp.solve(D, x)
mx = sp.simplify((r1 + r2) / 2)
my = sp.simplify((f.subs(x, r1) + f.subs(x, r2)) / 2)
print('중점:', mx, my)
assert sp.simplify(mx - a/2) == 0 and sp.simplify(my - b/2) == 0
# 판별: 서로 다른 두 실근 ⇔ 이차식 최솟값 < 0
dmin = sp.factor(D.subs(x, a/2))
print('차의 최솟값:', dmin)
survivors = {}
for tv, L in lines.items():
    bb = sp.solve(sp.Eq(L.subs(x, a/2), b/2), b)[0]
    mn = sp.factor(dmin.subs(b, bb))
    rng = sp.solve_univariate_inequality(mn < 0, a, relational=False).intersect(sp.Interval.open(0, sp.oo))
    print(f'  접점 x={tv}: b={bb}, 최솟값={mn}, (가) 만족 a 범위 {rng}')
    if rng != sp.EmptySet:
        survivors[tv] = (L, bb, rng)
assert list(survivors) == [-1]
assert survivors[-1][2] == sp.Interval.open(0, 4)
L, bb, _ = survivors[-1]
# S1: l과 y=f(x)
diff1 = sp.factor(f - L)
rts1 = sorted(set(sp.Poly(diff1, x).real_roots()))
S1 = sp.integrate(sp.Abs(diff1), (x, rts1[0], rts1[-1]))
S1 = sp.integrate(-diff1 if sp.N(diff1.subs(x, (rts1[0]+rts1[-1])/2)) < 0 else diff1, (x, rts1[0], rts1[-1]))
print('f - l =', diff1, 'S1 =', S1)
# S2: l과 y=f(x-a)+b, b=-2a-4 (a 기호)
diff2 = sp.factor(sp.expand((C2 - L).subs(b, bb)))
print('C2 - l =', diff2)
rts2 = sp.solve(diff2, x)
lo, hi = min(rts2, key=lambda r: r.subs(a, 1)), max(rts2, key=lambda r: r.subs(a, 1))
S2 = sp.simplify(sp.integrate(diff2, (x, lo, hi)))
S2 = sp.Abs(S2)
print('S2 (a 무관) =', S2)
assert S1 == sp.Rational(27, 4) and sp.simplify(S2 - sp.Rational(27, 4)) == 0
# 수치 확인: 0<a<4 여러 값에서 교점 2개, l이 중점 지남, S1+S2
import numpy as np
for av_ in [0.3, 1, 1.7, 2.5, 3.2, 3.9]:
    bv_ = -2*av_ - 4
    Dn = sp.lambdify(x, D.subs({a: av_, b: bv_}))
    co = sp.Poly(D.subs({a: av_, b: bv_}), x).all_coeffs()
    rr = np.roots([float(q) for q in co]); assert np.all(np.isreal(rr)) and abs(rr[0]-rr[1]) > 1e-9
    mxn = rr.real.mean(); myn = np.mean([-(q**3) + q for q in rr.real])
    assert abs(-2*(mxn + 1) - myn) < 1e-9
    g2 = sp.lambdify(x, (C2 - L).subs({a: av_, b: bv_}))
    co2 = sp.Poly((C2 - L).subs({a: av_, b: bv_}), x).all_coeffs()
    r2n = np.roots([float(q) for q in co2]).real
    xs = np.linspace(r2n.min(), r2n.max(), 200001)
    S2n = np.trapezoid(np.abs(g2(xs)), xs)
    assert abs(S2n - 6.75) < 1e-6, (av_, S2n)
print('수치: a=0.3~3.9에서 S2=27/4 일정')
# 원본 방식 오답(x=1/2 접선, 검증 없이): S1=S2=(3/2)^4/12
wrongS = 2 * sp.Rational(3, 2)**4 / 12
print('x=1/2 접선 오답 S1+S2 =', wrongS, ', 두 결과 합 =', wrongS + sp.Rational(27, 2))
assert wrongS == sp.Rational(27, 32) and wrongS + sp.Rational(27, 2) == sp.Rational(459, 32)
check_choices(18, S1 + S2)
print('ALL OK')
