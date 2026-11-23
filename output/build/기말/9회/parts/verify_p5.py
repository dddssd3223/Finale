# -*- coding: utf-8 -*-
# 17번 후보 A17 (I37: 근을 매개변수 a로, (가) [0,a]·[a,3], (나) |∫_0^3 f| ≤ 3∫_{a-1}^{a} f, f(3)의 최솟값) 검증 · author='claude'
import sympy as sp, os, sys, itertools
x, a, r = sp.symbols('x a r', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
C = 2                                   # 최고차항의 계수의 절댓값


def I(g, lo, hi):
    return sp.integrate(g, (x, lo, hi))


def sign_ok(g, lo, hi, s):
    """닫힌구간 [lo,hi]에서 s*g(x) >= 0 (이차함수: 끝점 + 꼭짓점 전수)"""
    if lo > hi:
        lo, hi = hi, lo
    pts = [lo, hi] + [p for p in sp.solve(sp.diff(g, x), x) if lo <= p <= hi]
    return all(s * g.subs(x, p) >= 0 for p in pts)


def absint(g, lo, hi):
    """∫_lo^hi |g| (lo<hi, 근에서 나눠 정확히)"""
    cuts = [lo] + sorted(p for p in sp.Poly(g, x).real_roots() if lo < p < hi) + [hi]
    return sum(abs(I(g, cuts[i], cuts[i + 1])) for i in range(len(cuts) - 1))


def ga_ok(g, av):
    """(가): ∫_0^3|f| = ∫_0^a f - ∫_a^3 f (0<a<3) — 정확한 적분으로 판정"""
    return sp.simplify(absint(g, 0, 3) - (I(g, 0, av) - I(g, av, 3))) == 0


def na_ok(g, av, m=3, L=1, up=3, absval=True):
    X = I(g, 0, up); Y = m * I(g, av - L, av)
    return (abs(X) <= Y) if absval else (X <= Y)


# ---------- 1) (가)로 f 결정: f = k x (x-r), k=±2, r 전수(유리수 격자 + r=a)
grid_a = [R(j, 6) for j in range(1, 18)]               # 0<a<3
grid_r = sorted(set([R(j, 4) for j in range(-24, 41)]))
for av in grid_a:
    sols = []
    for k in (C, -C):
        for rv in set(grid_r) | {av}:
            g = k * x * (x - rv)
            if ga_ok(g, av):
                sols.append((k, rv))
    assert sols == [(-C, av)], (av, sols)
print('(가) → f(x) = -2x(x-a) 유일 (a = 1/6 … 17/6, k=±2, r 격자 전수)')
# (가) ⇔ [0,a]에서 f≥0 이고 [a,3]에서 f≤0 (격자 전체에서 두 판정이 같음)
for av in grid_a[::4]:
    for k in (C, -C):
        for rv in grid_r[::3]:
            g = k * x * (x - rv)
            assert ga_ok(g, av) == (sign_ok(g, 0, av, 1) and sign_ok(g, av, 3, -1))
print('(가) ⇔ [0,a]에서 f≥0, [a,3]에서 f≤0 (격자 대조)')
f = -C * x * (x - a)

# ---------- 2) (나)를 a의 식으로
Y1 = sp.expand(I(f, a - 1, a)); Y01 = sp.expand(I(f, 0, 1))
assert Y1 == Y01 == a - R(2, 3)                         # x=a/2 대칭으로 [a-1,a] ↔ [0,1]
X = sp.expand(I(f, 0, 3)); assert X == 9 * a - 18
print("∫_{a-1}^a f = ∫_0^1 f = a - 2/3,  ∫_0^3 f = 9a - 18 (부호가 a=2에서 바뀜)")
S1 = sp.solve_univariate_inequality(3 * Y1 - X >= 0, a, relational=False)
S2 = sp.solve_univariate_inequality(3 * Y1 + X >= 0, a, relational=False)
S = sp.Intersection(S1, S2, sp.Interval.open(0, 3))
assert S == sp.Interval(R(5, 3), R(8, 3)), S
# 유리수 표본 전수(0.01 간격의 1/300 눈금)로 같은 집합 확인
good = [R(j, 300) for j in range(1, 900) if na_ok(f.subs(a, R(j, 300)), R(j, 300))]
assert good[0] == R(5, 3) and good[-1] == R(8, 3) and len(good) == 301, (good[0], good[-1], len(good))
print('(나) ⇔ 5/3 ≤ a ≤ 8/3 (식 풀이 + 1/300 눈금 전수)')

# ---------- 3) f(3)의 최솟값
f3 = sp.expand(f.subs(x, 3)); assert f3 == 6 * a - 18
ANS = min(f3.subs(a, v) for v in good)
assert ANS == -8 and f3.subs(a, R(5, 3)) == -8
print('f(3) = 6a - 18 (증가) → 최솟값', ANS, '(a = 5/3)')

# ---------- 4) 선지
ch = IT['choices']; vals = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 4
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals)
print('정답 -8 = 선지 ④, 선지', vals, '공차 2 오름차순')

# ---------- 5) 오답
yonly = sp.solve(3 * Y1, a)[0]                     # 오른쪽 변 ≥ 0 만: a ≥ 2/3
naive = sp.solve(X, a)[0]                          # 원문처럼 ∫_0^3 f ≥ 0 으로 읽음: a ≥ 2 (∩ a ≤ 8/3)
assert (yonly, naive) == (R(2, 3), 2)
w1, w2 = f3.subs(a, yonly), f3.subs(a, naive)
assert (w1, w2) == (-14, -6)
assert set(IT['wrongs']) == {'-14', '-6'} and all(w in ch for w in IT['wrongs'])
assert f3.subs(a, 1) == -12 and f3.subs(a, R(4, 3)) == -10   # ②·③ 등차 채움 값의 a
print('오답 근거 OK: -14(오른쪽 변 ≥ 0만, a=2/3), -6(원문처럼 ∫_0^3 f ≥ 0, a=2)')
assert ANS not in (0, 2, 3, 1, -3)                  # 본문의 수 · 원문 답과 다름

# ---------- 6) 원문 I37: -3 (②)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I37']; assert o[2] == '②' and o[1][1] == '-3'
fo = -4 * x * (x - 1)
for k in (4, -4):
    for rv in grid_r:
        g = k * x * (x - rv)
        if sign_ok(g, 0, 1, 1) and sign_ok(g, 1, 2, -1):
            assert (k, rv) == (-4, 1)
Yo, Xo = sp.expand(I(fo, 1 - a, 1)), sp.expand(I(fo, 0, a))
assert Yo == Xo                                    # 원문: x=1/2 대칭으로 두 변이 같은 적분
So = sp.Intersection(sp.solve_univariate_inequality(Xo >= 0, a, relational=False), sp.Interval.open(1, sp.oo))
assert So == sp.Interval.Lopen(1, R(3, 2)), So
assert fo.subs(x, R(3, 2)) == -3
print('원문 I37 OK: a ≤ 3/2, f(a) 최솟값 -3 (②)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS


def fam_min(cands):
    """(a, f) 후보들에서 f(3)의 최솟값(유리수 격자 전수)"""
    v = [g.subs(x, 3) for av, g in cands]
    return min(v) if v else None


# (가) 삭제: f = -2x(x-r) 에서 r 이 자유 → 예: r=13/8, a=21/16 이 (나)를 만족하고 f(3) = -33/4 < -8
gw = -C * x * (x - R(13, 8)); aw = R(21, 16)
assert not ga_ok(gw, aw) and na_ok(gw, aw) and gw.subs(x, 3) == R(-33, 4)
ablation('(가)', '정해지지 않음', 'f(x)=-2x(x-13/8), a=21/16 이 (나)를 만족하고 f(3)=-33/4 < -8')

# f(0)=0 삭제: f = -2(x-a)(x-s), s≤0 이면 (가)를 만족 → s에 따라 답이 다름
res = {}
for s0 in (0, R(-1, 2), -1):
    g = -C * (x - a) * (x - s0)
    vals_ = [g.subs({x: 3, a: av}) for av in [R(j, 300) for j in range(1, 900)]
             if ga_ok(g.subs(a, av), av) and na_ok(g.subs(a, av), av)]
    res[s0] = min(vals_) if vals_ else None
assert res[0] == ANS and any(v != ANS for k_, v in res.items() if k_ != 0)
ablation('f(0)=0', '정해지지 않음', f'다른 근 s에 따라 최솟값 {res}')

# 계수의 절댓값 2 → 4: 답 -16
g4 = -4 * x * (x - a)
v4 = min(g4.subs({x: 3, a: av}) for av in [R(j, 300) for j in range(1, 900)] if na_ok(g4.subs(a, av), av))
ablation('최고차항의 계수의 절댓값 2(→4)', v4)

# 절댓값 삭제(∫_0^3 f ≤ 3∫ f 만): a ≤ 8/3 이 전부 → f(3) 최솟값 없음(a→0+에서 -18로 다가감)
gA = [R(j, 300) for j in range(1, 900) if na_ok(f.subs(a, R(j, 300)), R(j, 300), absval=False)]
assert gA[0] == R(1, 300) and gA[-1] == R(8, 3)
ablation('(나)의 절댓값', '최솟값 없음', 'a ≤ 8/3 전체가 남아 f(3)이 -18에 가까워지기만 함')

# 바깥 계수 3 → 1: a ≥ 28/15, 답 -34/5
v1 = min(f3.subs(a, av) for av in [R(j, 900) for j in range(1, 2700)] if na_ok(f.subs(a, av), av, m=1))
assert v1 == R(-34, 5)
ablation('(나)의 바깥 계수 3(→1)', v1)

# 구간 [a-1,a] → [a-3,a](원문처럼 같은 길이): 두 변이 같은 적분 → ∫_0^3 f ≥ 0, a ≥ 2, 답 -6
v3 = min(f3.subs(a, av) for av in [R(j, 300) for j in range(1, 900)] if na_ok(f.subs(a, av), av, m=1, L=3))
ablation('(나)의 구간 끝 a-1(→a-3)', v3)

# ∫_0^3 → ∫_0^a (원문처럼 왼쪽 끝 a): |∫_0^a f| = (1/3)a^3 ≤ 3(a - 2/3) → 답이 바뀜
v5 = [f3.subs(a, av) for av in [R(j, 300) for j in range(1, 900)] if na_ok(f.subs(a, av), av, up=av)]
ablation('(나)의 ∫_0^3(→∫_0^a)', min(v5))

# (나) 전체 삭제: 0<a<3 → f(3)=6a-18 최솟값 없음
ablation('(나) 전체', '최솟값 없음', '0<a<3에서 f(3)=6a-18은 -18에 다가가기만 함')

# 범위 선언 0<a<3(원문의 a>1 자리): 밖의 a 를 격자로 확인 — (가)·(나)를 함께 만족하는 f가 있어도 f(3) > -8
outside = []
for av in [R(-2), R(-1), R(-1, 2), R(0), R(3), R(7, 2), R(4), R(5)]:
    for k in (C, -C):
        for rv in grid_r + [R(3, 2) * av, R(2, 3) * av]:
            g = k * x * (x - rv)
            if ga_ok(g, av) and na_ok(g, av):
                outside.append((av, g.subs(x, 3)))
assert all(v > ANS for _, v in outside), outside
print('범위 선언 0<a<3: 밖의 a 에서 가능한 f(3) =', sorted({v for _, v in outside}), '(모두 -8 보다 큼)')
print('ALL OK')
