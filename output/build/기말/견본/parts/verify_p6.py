# -*- coding: utf-8 -*-
"""p6 (서답형 S1, S2) 정답 검증: sympy 기호 계산 + 격자 전수 조사."""
import sympy as sp
from fractions import Fraction as Fr

x, t, a, k, m, c = sp.symbols('x t a k m c', real=True)
ok = True
def chk(cond, msg):
    global ok
    print(('OK  ' if cond else 'FAIL') + ' ' + msg)
    ok &= bool(cond)

# ---------------- S1 ----------------
print('== S1 ==')
P = x**3 - 3*x**2 - 9*x + k
f1 = sp.diff(P, x)                                   # 양변 미분
chk(sp.expand(f1 - 3*(x + 1)*(x - 3)) == 0, 'f(x)=3(x+1)(x-3)')
crit = sp.solve(f1, x)
# 극대점: f 부호 + → -
mx = [r for r in crit if f1.subs(x, r - sp.Rational(1, 10)) > 0 and f1.subs(x, r + sp.Rational(1, 10)) < 0]
chk(mx == [-1], '극대점 x=-1 하나')
ksol = sp.solve(sp.Eq(P.subs(x, -1), 0), k)
chk(ksol == [-5], f'(1) k={ksol}')
K = ksol[0]
Pk = P.subs(k, K)
chk(sp.factor(Pk) == (x - 5)*(x + 1)**2, f'P = {sp.factor(Pk)}')
avals = sorted(set(sp.solve(sp.Eq(Pk.subs(x, a), 0), a)))    # g(a)=0, 서로 다른 실근
avals = [r for r in avals if r.is_real]
chk(avals == [-1, 5], f'a 후보 {avals}')
# 역검산: 각 a에 대해 ∫_a^x f = P(x) 항등식
for av in avals:
    lhs = sp.integrate(f1.subs(x, t), (t, av, x))
    chk(sp.expand(lhs - Pk) == 0, f'a={av}: ∫_a^x f(t)dt = x^3-3x^2-9x-5 항등')
# 다른 a(예: 0, 1, 2)는 불가
for av in [0, 1, 2, -2, 3]:
    lhs = sp.integrate(f1.subs(x, t), (t, av, x))
    chk(sp.expand(lhs - Pk) != 0, f'a={av}는 불가')
chk(sum(avals) == 4, f'(2) 합={sum(avals)}')
# 극댓값이 0인 k는 유일 (k에 대해 일차)
chk(len(sp.solve(sp.Eq(P.subs(x, -1), 0), k)) == 1, 'k 유일')

# ---------------- S2 ----------------
print('== S2 ==')
def F(mm, cc):  # f = x^2 - 2 m x + c (최고차항 1인 일반 이차함수)
    return x**2 - 2*mm*x + cc
def G(mm, cc):
    return sp.integrate(F(mm, cc).subs(x, t), (t, 0, x))

# (가) W(x) = g(x+4)-g(x) 가 x>=1 에서 x=2 일 때 최소  <=>  m = 4
Wm = sp.expand(G(m, c).subs(x, x + 4) - G(m, c))
chk(sp.Poly(Wm, x).coeffs()[0] == 4, 'W 최고차항 계수 4 (아래로 볼록 이차)')
chk(sp.expand(sp.diff(Wm, x) - (F(m, c).subs(x, x + 4) - F(m, c))) == 0, "W'(x)=f(x+4)-f(x)")
vert = sp.solve(sp.diff(Wm, x), x)[0]
chk(sp.simplify(vert - (m - 2)) == 0, 'W 꼭짓점 x=m-2')
# 수치 전수: m 격자에서 (가) 성립 여부 (c 는 W-W(2)에서 소거됨)
def cond_ga(mm):
    Wn = sp.lambdify(x, Wm.subs({m: mm, c: 0}))
    w2 = Wn(2)
    xs = [1 + i * 0.01 for i in range(0, 6000)]
    return all(Wn(xx) >= w2 - 1e-9 for xx in xs)
ms = [Fr(i, 4) for i in range(-40, 81)]
good_m = [mm for mm in ms if cond_ga(float(mm))]
chk(good_m == [4], f'(가) 만족 m (격자 -10..20, 0.25 간격): {good_m}')
chk(sp.solve(sp.Eq(vert, 2), m) == [4], '(1) 축 x=4')

# (나) |g| 미분불가능점 = g 의 단순 실근 (g(r)=0, g'(r)=f(r)≠0)
def nondiff_count(cc, mm=4):
    g = sp.Poly(sp.expand(G(mm, cc)), x)
    cnt = 0
    for r, mult in sp.roots(g, filter=None).items():
        if sp.im(r) == 0 and mult == 1:
            cnt += 1
    return cnt
# 근거 확인: 중근은 |g| 미분가능, 단순근은 미분불가 (수치 한쪽 미분계수)
def onesided(gexpr, r, h=1e-6):
    gn = sp.lambdify(x, gexpr)
    return (abs(gn(r + h)) - abs(gn(r))) / h, (abs(gn(r)) - abs(gn(r - h))) / h
L, R = None, None
R_, L_ = onesided(G(4, 12), 6.0); chk(abs(R_ - L_) < 1e-3, 'c=12: x=6 중근에서 |g| 미분가능')
R_, L_ = onesided(G(4, 12), 0.0); chk(abs(R_ - L_) > 1, 'c=12: x=0 단순근에서 |g| 미분불가')
R_, L_ = onesided(G(4, 0), 0.0); chk(abs(R_ - L_) < 1e-3, 'c=0: x=0 중근에서 |g| 미분가능')
R_, L_ = onesided(G(4, 0), 12.0); chk(abs(R_ - L_) > 1, 'c=0: x=12 단순근에서 |g| 미분불가')
chk(sp.factor(G(4, 12)) == x*(x - 6)**2/3, 'c=12: g=x(x-6)^2/3')
chk(sp.factor(G(4, 0)) == x**2*(x - 12)/3, 'c=0: g=x^2(x-12)/3')

cs = sorted(set([Fr(i, 8) for i in range(-400, 401)] + [Fr(12), Fr(0), Fr(16), Fr(27, 2)]))
good_c = [cc for cc in cs if nondiff_count(sp.Rational(cc.numerator, cc.denominator)) == 1]
expect = [cc for cc in cs if cc == 0 or cc >= 12]
chk(good_c == expect, f'(나) 만족 c (격자 -50..50, 1/8 간격) = {{0}} ∪ [12,∞): {good_c[:3]}...{good_c[-1]}')
# 기호적으로: c≠0, c<12 이면 단순근 3개 (판별식 양수, 근 0 아님)
q = sp.expand(G(4, c) / x)
disc = sp.discriminant(sp.Poly(q * 3, x))
chk(sp.simplify(disc - (144 - 12*c)) == 0, '이차인수 x^2-12x+3c 판별식 144-12c')
counts = {}
for cc in cs:
    counts.setdefault(nondiff_count(sp.Rational(cc.numerator, cc.denominator)), []).append(cc)
chk(set(counts) == {1, 3}, f'미분불가 개수는 1 또는 3: {sorted(counts)}')

pos = [cc for cc in good_c if cc > 0]
chk(min(pos) == 12, f'(2) 양수 f(0) 최솟값 {min(pos)}')
f9 = [9 + cc for cc in good_c]
chk(min(f9) == 9, f'(3) f(9) 최솟값 {min(f9)} (c=0)')
chk(min(9 + cc for cc in good_c if cc != 0) == 21, '함정: c=0 누락 시 21')

# 결합 전수: (m, c) 동시 격자에서 두 조건 모두 만족 → m=4, c∈{0}∪[12,∞) 뿐
pairs = []
for mm in [Fr(i, 2) for i in range(-6, 17)]:
    if not cond_ga(float(mm)):
        continue
    for cc in [Fr(i, 2) for i in range(-40, 61)]:
        if nondiff_count(sp.Rational(cc.numerator, cc.denominator), sp.Rational(mm.numerator, mm.denominator)) == 1:
            pairs.append((mm, cc))
chk(all(p[0] == 4 and (p[1] == 0 or p[1] >= 12) for p in pairs) and (Fr(4), Fr(0)) in pairs and (Fr(4), Fr(12)) in pairs,
    f'결합 전수 {len(pairs)}쌍 모두 m=4, c∈{{0}}∪[12,∞)')

# p6.py 정답 문자열과 대조
ns = {}
exec(open(__file__.replace('verify_p6.py', 'p6.py')).read(), ns)
S = ns['SITEMS']
chk(S['S1']['ans'] == ['(1) −5', '(2) 4'], 'S1 ans 문자열')
chk(S['S2']['ans'] == ['(1) 4', '(2) 12', '(3) 9'], 'S2 ans 문자열')
chk([s[1][:2] for s in S['S1']['subs']] == ['4점', '6점'] and [s[1][:2] for s in S['S2']['subs']] == ['4점', '4점', '2점'], '배점 4+6, 4+4+2')

print('\n전체:', '통과' if ok else '실패')
raise SystemExit(0 if ok else 1)
