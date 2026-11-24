# -*- coding: utf-8 -*-
# 17번 후보 A17 2판 (I40: f'=a (x<b), -3x^2+8x (x>=b), 역함수, f(5)-f(2b-2)=-25, f(4)-f(2)) 검증 · author='claude'
import sympy as sp, os, sys
x, b, A_ = sp.symbols('x b a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def q(c):
    return -3 * x**2 + c * x


def diff(m, n, av, bv, c):
    """f(m)-f(n), f'=av (x<bv), q_c (x>=bv): 조각마다 나눠 정확히 적분"""
    def G(t):
        return av * (t - bv) if t < bv else sp.integrate(q(c), (x, bv, t))
    return sp.nsimplify(G(m) - G(n))


def inverse_ok(av, bv, c):
    """역함수 존재 ⇔ 단조. x>=b 조각은 -∞로 가므로 감소만 가능: a<0 이고 [b,∞)에서 이차식 ≤ 0(근에서만 0)"""
    if av >= 0:
        return False
    crit = [bv] + [r for r in sp.solve(q(c), x) + sp.solve(sp.diff(q(c), x), x) if r >= bv]
    return max(q(c).subs(x, r) for r in crit) <= 0


def all_solutions(c=8, al=2, k=2, M=5, V=-25, link=True):
    """f(M)-f(al*b-k)=V 를 만족시키는 실수 b 전부: b 와 아래 끝·위 끝의 위치로 조각을 나눠 갈래마다 정확히 풂"""
    a_ = -3 * b**2 + c * b
    lo = al * b - k
    P = lambda t: sp.integrate(q(c), (x, 0, t))          # 이차식 조각의 부정적분(0에서)
    G = lambda t, side: a_ * (t - b) if side == 0 else P(t) - P(b)   # ∫_b^t f'
    out = set()
    # 갈래: 위 끝 M 이 b 왼쪽(0)/오른쪽(1), 아래 끝 lo 가 b 왼쪽/오른쪽
    for sM in (0, 1):
        for sL in (0, 1):
            expr = sp.expand(G(M, sM) - G(lo, sL) - V)
            if expr == 0:
                continue
            for r in sp.solve(expr, b):
                if not r.is_real:
                    continue
                if (M < r) == (sM == 0) and (lo.subs(b, r) < r) == (sL == 0):
                    out.add(sp.nsimplify(r))
    return sorted(out, key=lambda z: float(z))


# ---------- 1) 역함수 조건 ⇔ b > 8/3 (눈금 전수)
for bv in [R(k, 12) for k in range(-60, 96)]:
    assert inverse_ok(-3 * bv**2 + 8 * bv, bv, 8) == (bv > R(8, 3)), bv
assert not inverse_ok(0, R(8, 3), 8)
print('역함수 ⇔ b>8/3 (1/12 눈금 전수, 경계 b=8/3은 a=0이라 제외)')

# ---------- 2) 조건을 만족시키는 b 전부(갈래 전수) → 역함수로 거름
S = all_solutions()
assert S == [0, (9 - sp.sqrt(17)) / 4, 3], S
good = [r for r in S if inverse_ok(-3 * r**2 + 8 * r, r, 8)]
assert good == [3]
for r in S:   # 조각 판정 함수로 대조
    assert diff(5, 2 * r - 2, -3 * r**2 + 8 * r, r, 8) == -25
# 갈래 ②의 식: b>=2 이면 구간이 통째로 이차식 조각, -t^2(t-4)=0
t = sp.symbols('t')
assert sp.expand(sp.integrate(q(8), (x, t, 5)) + 25 - t**2 * (t - 4)) == 0
# 갈래 ③: b>5 이면 차가 양수(감소함수) — 표본
for bv in (R(11, 2), 6, 10):
    assert diff(5, 2 * bv - 2, -3 * bv**2 + 8 * bv, bv, 8) > 0
# 원문 줄(b<2, 구간 안에서 나눔)의 방정식과 근
a_ = -3 * b**2 + 8 * b
E1 = sp.expand(a_ * (b - (2 * b - 2)) + sp.integrate(q(8), (x, b, 5)) + 25)
assert sp.factor(E1) == sp.factor(2 * b * (2 * b**2 - 9 * b + 8)) or sp.expand(E1 - 2 * b * (2 * b**2 - 9 * b + 8)) == 0
print('조건의 해 b =', S, '→ 역함수로 b=3 (b=0: a=0, (9-√17)/4: a>0)')
bv = 3; av = -3 * 9 + 24; assert av == -3

# ---------- 3) 답
ANS = diff(4, 2, av, bv, 8)
assert ANS == -12 == -3 + sp.integrate(q(8), (x, 3, 4))
print('f(4)-f(2) =', ANS)

# ---------- 4) 선지
ch = IT['choices']; vals = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals) and vals[1] - vals[0] == 1
print('정답 = 선지 ①, 선지', vals, '공차 1 오름차순')

# ---------- 5) 오답
w_noa = sp.integrate(q(8), (x, 3, 4))                 # ∫_2^3 a 빠뜨림
w_b0 = diff(4, 2, 0, 0, 8)                             # 원문 줄대로 b=0 택함
w_nosplit = sp.integrate(q(8), (x, 2, 4))
assert (w_noa, w_b0, w_nosplit) == (-9, -8, -8)
assert set(IT['wrongs']) == {'-9', '-8'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: -9(∫_2^3 a 빠뜨림), -8(b=0 택함 / x=3에서 안 나눔)')
assert ANS not in {8, 2, 5, 25, -25, 4, 3} and ANS != -1

# ---------- 6) 원문 I40: -1 (②)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I40']; assert o[2] == '②' and o[1][1] == '-1'
a_o = -3 * b**2 + b
cand = []
cand += [r for r in sp.solve(a_o * b + sp.integrate(q(1), (x, b, 2)) + R(15, 2), b) if r.is_real and 0 < r <= 2]
cand += [r for r in sp.solve(2 * a_o + R(15, 2), b) if r.is_real and r > 2]
assert sp.integrate(q(1), (x, 0, 2)) != R(-15, 2)       # b<=0 갈래 해 없음
assert cand == [1] and inverse_ok(-2, 1, 1)
print('원문 I40 OK: b=1, a=-2, a+b=-1 (②)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS


def answer(**kw):
    c = kw.get('c', 8)
    g = [r for r in all_solutions(**kw) if inverse_ok(-3 * r**2 + c * r, r, c)]
    if len(g) != 1:
        return f'정해지지 않음({len(g)}개)'
    r = g[0]
    return sp.N(diff(4, 2, -3 * r**2 + c * r, r, c), 6)


vals_ = sorted({diff(4, 2, -3 * r**2 + 8 * r, r, 8) for r in S}, key=float)
assert len(vals_) > 1
ablation('역함수 존재', '정해지지 않음', f'b={S} → f(4)-f(2) = {vals_}')

# 미분가능(a=-3b^2+8b) 삭제: 조건에 a가 없으므로 b=3은 그대로지만 a가 정해지지 않음 → f(4)-f(2)=a-9
for av_ in (-1, -3, -5):
    assert inverse_ok(av_, 3, 8)
ablation('미분가능(a=-3b^2+8b)', '정해지지 않음', 'b=3, a<0 아무 값 → f(4)-f(2)=a-9')

ablation('값 -25(→-24)', answer(V=-24))
ablation('아래 끝 2b-2(→2b-1)', answer(k=1))
ablation('아래 끝의 계수 2(→b-2)', answer(al=1, k=2))
ablation('위 끝 5(→6)', answer(M=6))
ablation('이차식의 계수 8(→6)', answer(c=6))
print('ALL OK')
