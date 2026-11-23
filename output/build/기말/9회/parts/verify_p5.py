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

# ---------- 3) f(3)의 값이 될 수 있는 정수의 개수
f3 = sp.expand(f.subs(x, 3)); assert f3 == 6 * a - 18


def cnt(Sa, g3=f3):
    """a의 집합 Sa(구간) 위에서 g3(a)(일차, 증가)가 갖는 값의 범위 안 정수 개수"""
    assert sp.diff(g3, a) > 0
    img = sp.Interval(g3.subs(a, Sa.inf), g3.subs(a, Sa.sup), Sa.left_open, Sa.right_open)
    ints = sp.Intersection(img, sp.S.Integers)
    return len(list(ints)) if ints.is_finite_set else 'inf'


ANS = cnt(S)
assert ANS == 7 and sp.Interval(f3.subs(a, S.inf), f3.subs(a, S.sup)) == sp.Interval(-8, -2)
# 격자 표본과 대조: 연속이므로 -8..-2 의 정수마다 그 값을 주는 a 가 범위 안에 있음
for v in range(-8, -1):
    av = sp.solve(f3 - v, a)[0]; assert av in S and na_ok(f.subs(a, av), av)
print('f(3) = 6a - 18 (연속·증가), 5/3 ≤ a ≤ 8/3 → -8 ≤ f(3) ≤ -2 → 정수', ANS, '개')

# ---------- 4) 선지
ch = IT['choices']; vals = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 4
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals)
assert vals[1] - vals[0] == 1
print('정답 = 선지 ④, 선지', vals, '공차 1 오름차순')

# ---------- 5) 오답
naive = sp.solve(X, a)[0]; assert naive == 2       # 원문처럼 ∫_0^3 f ≥ 0 으로 읽음: 2 ≤ a ≤ 8/3
w_naive = cnt(sp.Interval(2, R(8, 3)))
w_noup = cnt(sp.Interval.Ropen(R(5, 3), 3))         # 위쪽 X ≤ Y 를 빼먹음: 5/3 ≤ a < 3
assert (w_naive, w_noup) == (5, 8)
assert set(IT['wrongs']) == {'5', '8'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 5(원문처럼 ∫_0^3 f ≥ 0, 2≤a≤8/3), 8(위 끝 빼먹음, 5/3≤a<3)')
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


def Aset(cond):
    conds = list(cond.args) if isinstance(cond, sp.And) else [cond]
    return sp.Intersection(*[sp.solve_univariate_inequality(c, a, relational=False) for c in conds], sp.Interval.open(0, 3))


# (가) 삭제: f=2x(x-3), a=1/10 도 (나)를 만족 → f(3)=0 이 더해져 개수가 바뀜
gw = C * x * (x - 3); aw = R(1, 100)
assert not ga_ok(gw, aw) and na_ok(gw, aw) and gw.subs(x, 3) == 0
ablation('(가)', '정해지지 않음', 'f(x)=2x(x-3), a=1/100 이 (나)를 만족해 f(3)=0 도 가능 → 7개가 아님')

# f(0)=0 삭제: f=-2(x-a)(x+1) 도 (가)를 만족, (나)를 만족하는 a 에서 f(3) 이 -12 아래까지 → 개수 바뀜
g = -C * (x - a) * (x + 1)
vals_ = [g.subs({x: 3, a: av}) for av in [R(j, 300) for j in range(1, 900)]
         if ga_ok(g.subs(a, av), av) and na_ok(g.subs(a, av), av)]
assert min(vals_) < -12
ablation('f(0)=0', '정해지지 않음', f'f(x)=-2(x-a)(x+1)이면 f(3)이 {min(vals_)}까지 → 정수 7개가 아님')

# 계수의 절댓값 2 → 4: f(3)=12a-36, a 범위 같음 → 13개
g4 = -4 * x * (x - a)
S4 = Aset(sp.And(3 * I(g4, a - 1, a) - I(g4, 0, 3) >= 0, 3 * I(g4, a - 1, a) + I(g4, 0, 3) >= 0))
ablation('최고차항의 계수의 절댓값 2(→4)', cnt(S4, sp.expand(g4.subs(x, 3))))

# 절댓값 삭제: 0<a≤8/3 → -18<f(3)≤-2
ablation('(나)의 절댓값', cnt(Aset(3 * Y1 - X >= 0)))

# 바깥 계수 3 → 1: 28/15 ≤ a ≤ 49/24
ablation('(나)의 바깥 계수 3(→1)', cnt(Aset(sp.And(Y1 - X >= 0, Y1 + X >= 0))))

# 구간 [a-1,a] → [a-3,a](원문처럼 같은 길이): 두 변이 같은 적분 → 2 ≤ a < 3
Y3 = sp.expand(I(f, a - 3, a)); assert Y3 == X
ablation('(나)의 구간 끝 a-1(→a-3)', cnt(Aset(sp.And(Y3 - X >= 0, Y3 + X >= 0))))

# ∫_0^3 → ∫_0^a
Xa = sp.expand(I(f, 0, a))
ablation('(나)의 ∫_0^3(→∫_0^a)', cnt(Aset(sp.And(3 * Y1 - Xa >= 0, 3 * Y1 + Xa >= 0))))

# (나) 전체 삭제: 0<a<3 → -18<f(3)<0
ablation('(나) 전체', cnt(sp.Interval.open(0, 3)))

# 범위 선언 0<a<3 삭제: a ≥ 3 에서 f=2x(x-r), a=3r/2 (r ≥ 3) 가 (가)·(나)를 만족 → f(3)=6(3-r) 아래로 유계 아님
#   (1판 검사는 a ≤ 5 만 보아 r ≤ 10/3, f(3) ≥ -2 만 나와 반대로 보였다)
for rv in (R(10, 3), 4, 5, 10, 20):
    g = C * x * (x - rv); av = R(3, 2) * rv
    assert av >= 3 and ga_ok(g, av) and na_ok(g, av)
    assert g.subs(x, 3) == 6 * (3 - rv)
ablation('범위 선언 0<a<3', 'inf', 'a=3r/2 (r≥3), f(x)=2x(x-r)에서 f(3)=6(3-r) → r=20이면 -102, 정수가 무수히 많음')
print('ALL OK')
