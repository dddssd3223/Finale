# -*- coding: utf-8 -*-
# p5 (17·18번) 검증: 전수 케이스 분석 (sympy 기호 + 수치 스캔)
import sympy as sp
import random
from fractions import Fraction

x, A, p, B, C, k = sp.symbols('x A p B C k', real=True)

def distinct_real_roots(poly_expr, var=x):
    P = sp.Poly(sp.expand(poly_expr), var)
    return sorted(set(sp.real_roots(P)), key=lambda r: float(r))

def odd_mult_real_roots(poly_expr, var=x):
    """부호가 바뀌는 실근(홀수 중복도) 목록"""
    P = sp.Poly(sp.expand(poly_expr), var)
    out = []
    for fac, m in sp.factor_list(P)[1]:
        if m % 2 == 1:
            out += list(set(sp.real_roots(fac)))
    return sorted(set(out), key=lambda r: float(r))

# =====================================================================
# 17번 (M55 구조 변경)
#  f: 최고차항 양수 삼차, f(0)=0, f'(1)=1
#  (가) 곡선 y=f(x)와 직선 y=x가 서로 다른 두 점에서 만남
#  (나) 방정식 f(f(x))=f(x)의 서로 다른 실근 3개
#  답: 가능한 모든 f(3)의 합 = 81  (정답 ⑤)
# =====================================================================
print('=== 17번 ===')
# (1) (가)의 전수 분류: f-x = x(Ax^2+Bx+C-1), A>0
#   서로 다른 실근 2개 <=> 이차식 Ax^2+Bx+(C-1)이 (i) 0을 근으로 갖고 다른 근이 0이 아님, 또는 (ii) 0이 아닌 중근
#   -> f-x = A x^2 (x-p)  또는  f-x = A x (x-p)^2  (p != 0)
# 이를 계수 공간 무작위 표본으로 확인 (정수/유리 계수에서 실근 개수 = 2 인 경우 모두 두 형태 중 하나)
cnt_checked = 0
for a_ in [Fraction(1, 3), Fraction(1, 2), 1, 2, 3]:
    for b_ in range(-6, 7):
        for c_ in [Fraction(n, 4) for n in range(-12, 13)]:
            q = a_ * x**2 + b_ * x + (c_ - 1)
            expr = sp.expand(x * q)
            rs = distinct_real_roots(expr)
            if len(rs) == 2:
                cnt_checked += 1
                pr = [r for r in rs if r != 0]
                assert len(pr) == 1
                pp = pr[0]
                ok1 = sp.expand(expr - a_ * x**2 * (x - pp)) == 0
                ok2 = sp.expand(expr - a_ * x * (x - pp)**2) == 0
                assert ok1 or ok2, (a_, b_, c_)
print('(가) 분류 확인 표본 수:', cnt_checked)

fam = {
    'I: f-x=Ax(x-p)^2 (원점 단순근, p 중근)': x + A * x * (x - p)**2,
    'II: f-x=Ax^2(x-p) (원점 중근, p 단순근)': x + A * x**2 * (x - p),
}
sols17 = []
for name, f in fam.items():
    # (나): f(f(x))=f(x) <=> f(x) in {0, p}
    e0 = sp.factor(f)
    ep = sp.factor(f - p)
    print(name)
    print('   f      =', e0)
    print('   f - p  =', ep)
    # 판별식: 두 경우 모두 이차인수 A x^2 - A p x + 1 이 등장
    quad = A * x**2 - A * p * x + 1
    disc = sp.discriminant(quad, x)
    print('   공통 이차인수 판별식 =', sp.factor(disc))
    # 세 번째 조건 f'(1)=1 + Ap^2=4 연립
    eqs = [sp.Eq(sp.diff(f, x).subs(x, 1), 1), sp.Eq(A * p**2, 4)]
    for s in sp.solve(eqs, [A, p], dict=True):
        if s[A] > 0 and s[p] != 0:
            ff = sp.expand(f.subs(s))
            sols17.append((name, s, ff))

# 수치 전수 확인: 두 가족에서 (A,p) 무작위 → (나) 실근 수가 3 <=> Ap^2 = 4
random.seed(1)
for name, f in fam.items():
    for _ in range(300):
        a_ = sp.Rational(random.randint(1, 60), random.randint(1, 20))
        p_ = sp.Rational(random.choice([-1, 1]) * random.randint(1, 40), random.randint(1, 10))
        ff = sp.expand(f.subs({A: a_, p: p_}))
        comp = sp.expand(ff.subs(x, ff) - ff)
        n = len(distinct_real_roots(comp))
        assert (n == 3) == (a_ * p_**2 == 4), (name, a_, p_, n)
    # 경계 Ap^2=4 위에서도 몇 점 확인
    for p_ in [sp.Rational(1, 2), 1, 2, 3, -1, -3]:
        p_ = sp.nsimplify(p_); a_ = sp.Integer(4) / p_**2
        ff = sp.expand(f.subs({A: a_, p: p_}))
        comp = sp.expand(ff.subs(x, ff) - ff)
        assert len(distinct_real_roots(comp)) == 3

# 최종 후보 각각 조건 전부 재검산
vals = []
for name, s, ff in sols17:
    lead = sp.Poly(ff, x).LC()
    assert sp.Poly(ff, x).degree() == 3 and lead > 0
    assert ff.subs(x, 0) == 0
    assert sp.diff(ff, x).subs(x, 1) == 1
    assert len(distinct_real_roots(ff - x)) == 2
    comp = sp.expand(ff.subs(x, ff) - ff)
    rr = distinct_real_roots(comp)
    assert len(rr) == 3
    v = ff.subs(x, 3)
    vals.append(v)
    print('  후보', name.split(':')[0], s, 'f =', sp.factor(ff - x), '+ x', ' f(f(x))=f(x) 근:', rr, ' f(3) =', v)
assert sorted(vals) == [3, 27, 51], vals
print('f(3) 값들:', sorted(vals), '합 =', sum(vals))
assert sum(vals) == 81

# 독립 확인: 일반 삼차 f=a x^3+b x^2+c x 에서 (가),(나),f'(1)=1 을 직접 연립 (가족 가정 없이)
#  (가)⇔[c=1,b≠0] 또는 [b^2=4a(c-1), b≠0]; 각 경우 f'(1)=1 로 c 소거 후 (나) 근 수를 a로 스캔
a, b, c = sp.symbols('a b c', real=True)
gen = a * x**3 + b * x**2 + c * x
found = set()
# 경우 (i) c=1: f'(1)=3a+2b+1=1 -> b=-3a/2
# 경우 (ii) b^2=4a(c-1), 3a+2b+c=1 -> c=1-3a-2b, b^2=4a(-3a-2b) -> (b+2a)(b+6a)=0 -> b=-2a 또는 b=-6a
cases = {'c=1': {b: -sp.Rational(3, 2) * a, c: 1},
         'b=-2a': {b: -2 * a, c: 1 - 3 * a + 4 * a},
         'b=-6a': {b: -6 * a, c: 1 - 3 * a + 12 * a}}
for nm, sub in cases.items():
    fa = sp.expand(gen.subs(sub))
    # (나)의 실근 수가 3이 되는 a>0 를 기호로: 두 이차인수 판별식 조건에서 a 결정
    good = []
    for a_ in [sp.Rational(n, 9) for n in range(1, 400)]:
        ff = fa.subs(a, a_)
        if len(distinct_real_roots(ff - x)) != 2:
            continue
        comp = sp.expand(ff.subs(x, ff) - ff)
        if len(distinct_real_roots(comp)) == 3:
            good.append(a_)
    print('  일반형', nm, '(나) 만족 a (a=n/9 스캔):', good)
    for a_ in good:
        found.add(fa.subs(a, a_).subs(x, 3))
assert found == {3, 27, 51}, found
print('17번 통과: 답 81 (⑤)')

# =====================================================================
# 18번 (I61 구조 변경)
#  f=(x+1)(x-1)(x-3), g_k(x)=x^2∫_k^x f - ∫_k^x t^2 f,  N(k)=g_k 가 극값을 갖는 x 의 개수
#  N(k) 가 불연속인 실수 k 의 개수 = 9  (정답 ③)
# =====================================================================
print('=== 18번 ===')
t = sp.symbols('t', real=True)
f18 = (x + 1) * (x - 1) * (x - 3)
H = sp.integrate(f18.subs(x, t), (t, 0, x))
print('H(x) =', sp.factor(H), ' ; H + 9/4 =', sp.factor(H + sp.Rational(9, 4)), ' ; H - 7/4 =', sp.factor(H - sp.Rational(7, 4)))
kk = sp.symbols('kk', real=True)
g = x**2 * sp.integrate(f18.subs(x, t), (t, kk, x)) - sp.integrate(t**2 * f18.subs(x, t), (t, kk, x))
gp = sp.factor(sp.diff(g, x))
assert sp.simplify(sp.diff(g, x) - 2 * x * (H - H.subs(x, kk))) == 0
print("g'(x) = 2x(H(x)-H(k))  확인")

def N(kv):
    expr = sp.expand(2 * x * (H - H.subs(x, kv)))
    return len(odd_mult_real_roots(expr))

special = [1 - 2 * sp.sqrt(2), 1 - sp.sqrt(7), -1, 0, 1, 2, 3, 1 + sp.sqrt(7), 1 + 2 * sp.sqrt(2)]
# N(k)는 H(k)가 H의 임계값(-9/4, 7/4)이나 상쇄값 0(=H(0))을 지날 때만 바뀐다: 그 k 전체가 special과 일치하는지 확인
crit_levels = set([H.subs(x, r) for r in sp.solve(sp.diff(H, x), x)] + [H.subs(x, 0)])
assert crit_levels == {sp.Rational(-9, 4), sp.Rational(7, 4), 0}, crit_levels
ks = set()
for L in crit_levels:
    ks |= set(sp.solve(sp.Eq(H, L), x))
assert ks == set(sp.nsimplify(s_) for s_ in special), ks
for s_ in special:
    print('  N(', s_, ') =', N(s_))
# 조밀 스캔: 유리수 격자 (특수점 제외)에서 N 값 → 구간별 상수인지, 불연속점 위치 파악
grid = [sp.Rational(i, 40) for i in range(-320, 321)]
vals18 = [(float(kv), N(kv)) for kv in grid]
# 유리 격자점 중 특수점과 같은 것: -1,0,1,2,3 (격자에 포함)
specials_f = sorted(float(s_) for s_ in special)
# 특수점을 제외한 격자에서 N은 5 (1-2√2<k<1+2√2) 또는 3 (그 밖)이어야 함
for kf, n in vals18:
    if any(abs(kf - s_) < 1e-12 for s_ in specials_f):
        continue
    inside = float(1 - 2 * sp.sqrt(2)) < kf < float(1 + 2 * sp.sqrt(2))
    assert n == (5 if inside else 3), (kf, n)
# 큰 |k|에서도 3
for kv in [-100, -20, 20, 100, sp.Rational(-77, 3), sp.Rational(91, 7)]:
    assert N(kv) == 3
# 불연속점 판정: 각 특수점 c에서 N(c)와 양옆 근방값 비교
disc_pts = []
for s_ in special:
    left = N(sp.nsimplify(float(s_) - 1e-4, rational=True))
    right = N(sp.nsimplify(float(s_) + 1e-4, rational=True))
    mid = N(s_)
    if not (left == mid == right):
        disc_pts.append(s_)
    print('  c =', s_, ' (좌, 값, 우) =', (left, mid, right))
# 특수점 이외의 격자점에서는 N이 국소 상수 → 불연속 아님 (위 assert 로 확인)
print('불연속점:', disc_pts, '개수 =', len(disc_pts))
assert len(disc_pts) == 9
# 상쇄점 누락(H(k)=0의 4개) 시 5, k=1(극대 접함) 누락 시 8 등 오답 설계 확인용
print('18번 통과: 답 9 (③)')
# 부품 파일의 선지·정답 번호 대조
import os
ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
assert IT[17]['ans'] == 5 and IT[17]['choices'][4] == '81'
assert IT[18]['ans'] == 3 and IT[18]['choices'][2] == '9'
for n in (17, 18):
    ch = [int(c) for c in IT[n]['choices']]
    assert ch == sorted(ch) and len(set(ch)) == 5
print('ALL PASS')
