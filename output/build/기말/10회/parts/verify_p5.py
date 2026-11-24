# -*- coding: utf-8 -*-
# 17번 후보 A17 (I40: f'=a (x<b), -3x^2+8x (x>=b), 역함수 존재, f(b+1)-f(b-2)=-15, f(4)-f(2)) 검증 · author='claude'
import sympy as sp, os, sys
x, b, A_ = sp.symbols('x b a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def diff(m, n, av, bv, c):
    """f(m)-f(n) for f'=av (x<bv), -3x^2+c x (x>=bv): 조각마다 나눠 정확히 적분"""
    def G(t):   # ∫_bv^t f'
        if t < bv:
            return av * (t - bv)
        return sp.integrate(-3 * x**2 + c * x, (x, bv, t))
    return sp.nsimplify(G(m) - G(n))


def inverse_ok(av, bv, c):
    """f가 실수 전체에서 단조(역함수 존재) ⇔ f'≥0 전부 또는 f'≤0 전부, 그리고 어떤 구간에서도 0이 아님.
    f'=av (x<bv) 상수, x>=bv 에서 이차식(→ -∞) → 감소만 가능. 끝점·꼭짓점·근 전수로 판정"""
    q = -3 * x**2 + c * x
    if av > 0 or av == 0:          # x<b 에서 증가 또는 상수 → x 큰 쪽(감소)과 모순 / 상수 구간
        return False
    crit = [bv] + [r for r in sp.solve(q, x) + sp.solve(sp.diff(q, x), x) if r >= bv]
    mx = max(q.subs(x, r) for r in crit)
    return mx <= 0                  # 이차식은 근에서만 0 (구간 아님)


def solve_all(c=8, lo=-2, hi=1, V=-15, link=True):
    """조건 f(b+hi)-f(b+lo)=V 를 만족시키는 실수 b 전부 (lo<0<hi 이므로 b가 늘 구간 안: 식 하나)"""
    a_ = -3 * b**2 + c * b
    Fb = sp.expand(a_ * (0 - lo) + sp.integrate(-3 * x**2 + c * x, (x, b, b + hi)))
    return Fb, [r for r in sp.solve(Fb - V, b) if r.is_real]


# ---------- 1) 조건식과 근
Fb, roots = solve_all()
assert Fb == -9 * b**2 + 21 * b + 3, Fb
assert set(roots) == {3, R(-2, 3)}, roots
# 구간 끝이 b를 따라 움직여 b-2<b<b+1 이 늘 성립 → 식 하나로 전수 (조각 판정 함수와 대조)
for bv in [R(k, 6) for k in range(-30, 31)]:
    av = -3 * bv**2 + 8 * bv
    assert diff(bv + 1, bv - 2, av, bv, 8) == Fb.subs(b, bv)
print('f(b+1)-f(b-2) = -9b^2+21b+3 (모든 실수 b, 1/6 눈금 대조) → b = 3, -2/3')

# ---------- 2) 역함수 조건 ⇔ b > 8/3
for bv in [R(k, 12) for k in range(-60, 72)]:
    av = -3 * bv**2 + 8 * bv
    assert inverse_ok(av, bv, 8) == (bv > R(8, 3)), bv
assert not inverse_ok(0, R(8, 3), 8)                     # 경계 b=8/3: a=0, 상수 구간
a2 = -3 * R(4, 9) + 8 * R(-2, 3); assert a2 == R(-20, 3) and a2 < 0   # 버리는 근도 a<0
assert not inverse_ok(a2, R(-2, 3), 8)
good = [r for r in roots if inverse_ok(-3 * r**2 + 8 * r, r, 8)]
assert good == [3]
bv = 3; av = -3 * 9 + 8 * 3; assert av == -3
print('역함수 ⇔ b>8/3 (1/12 눈금 전수, 경계 제외) → b=3, a=-3 (b=-2/3은 a=-20/3<0 이지만 탈락)')

# ---------- 3) 답
ANS = diff(4, 2, av, bv, 8)
assert ANS == -12
assert ANS == -3 * (3 - 2) + sp.integrate(-3 * x**2 + 8 * x, (x, 3, 4))
print('f(4)-f(2) =', ANS)

# ---------- 4) 선지
ch = IT['choices']; vals = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals)
assert vals[1] - vals[0] == 1
print('정답 = 선지 ①, 선지', vals, '공차 1 오름차순')

# ---------- 5) 오답
w_noa = sp.integrate(-3 * x**2 + 8 * x, (x, 3, 4))                  # ∫_2^3 a 빠뜨림
w_neg = diff(4, 2, a2, R(-2, 3), 8)                                  # b=-2/3 택함
w_nosplit = sp.integrate(-3 * x**2 + 8 * x, (x, 2, 4))               # [2,4] 전체를 이차식으로
assert (w_noa, w_neg, w_nosplit) == (-9, -8, -8)
assert set(IT['wrongs']) == {'-9', '-8'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: -9(∫_2^3 a 빠뜨림), -8(b=-2/3 택함 / x=3에서 안 나눔)')
body_nums = {8, 1, 2, 15, -15, 4, 3}
assert ANS not in body_nums and ANS != -1                            # 본문의 수 · 원문 답과 다름

# ---------- 6) 원문 I40: -1 (②)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I40']; assert o[2] == '②' and o[1][1] == '-1'
sols = []
for k in range(-600, 1200):          # b 눈금 1/200 + 근 직접 풀이로 전수
    pass
# 원문: f(2)-f(0) 을 b 위치로 나눠 식으로 풀기
a_o = -3 * b**2 + b
cand = []
cand += [r for r in sp.solve(sp.integrate(-3 * x**2 + x, (x, 0, 2)) + R(15, 2), b)]          # b<=0: 상수식 -6 ≠ -15/2 → 해 없음
cand += [r for r in sp.solve(a_o * b + sp.integrate(-3 * x**2 + x, (x, b, 2)) + R(15, 2), b) if r.is_real and 0 < r <= 2]
cand += [r for r in sp.solve(2 * a_o + R(15, 2), b) if r.is_real and r > 2]
assert cand == [1], cand
assert inverse_ok(-2, 1, 1)
print('원문 I40 OK: b=1, a=-2, a+b=-1 (②) · 원문은 역함수 조건 없이도 b=1 하나')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS


# 역함수 조건 삭제: b=3, -2/3 둘 다 → f(4)-f(2) 가 -12, -8
vals_ = sorted({diff(4, 2, -3 * r**2 + 8 * r, r, 8) for r in roots})
assert vals_ == [-12, -8]
ablation('역함수 존재', '정해지지 않음', f'b=3, -2/3 → {vals_}')

# 미분가능(x=b에서 a=-3b^2+8b) 삭제: a, b 자유 → 2a-3b^2+5b+3=-15, b>8/3, a<0 인 (a,b)가 여럿
outs = set()
for bv_ in (3, R(10, 3), 4):
    av_ = sp.solve(2 * A_ + (-3 * bv_**2 + 5 * bv_ + 3) + 15, A_)[0]
    assert av_ < 0 and bv_ > R(8, 3)
    outs.add(diff(4, 2, av_, bv_, 8) if bv_ < 4 else diff(4, 2, av_, bv_, 8))
assert len(outs) > 1
ablation('미분가능(a=-3b^2+8b)', '정해지지 않음', f'b=3, 10/3, 4 → f(4)-f(2) = {sorted(outs)}')

# 값 -15 → -14: 근이 무리수, 답 바뀜
_, r14 = solve_all(V=-14)
g14 = [r for r in r14 if inverse_ok(-3 * r**2 + 8 * r, r, 8)]
assert len(g14) == 1
v14 = sp.nsimplify(diff(4, 2, -3 * g14[0]**2 + 8 * g14[0], g14[0], 8))
ablation('값 -15(→-14)', sp.N(v14, 6))

# 구간 끝 b-2 → b-1
_, r1 = solve_all(lo=-1)
g1 = [r for r in r1 if inverse_ok(-3 * r**2 + 8 * r, r, 8)]
assert len(g1) == 1
ablation('구간 끝 b-2(→b-1)', sp.N(diff(4, 2, -3 * g1[0]**2 + 8 * g1[0], g1[0], 8), 6))

# 구간 끝 b+1 → b+2
_, r2 = solve_all(hi=2)
g2 = [r for r in r2 if inverse_ok(-3 * r**2 + 8 * r, r, 8)]
ablation('구간 끝 b+1(→b+2)', sp.N(diff(4, 2, -3 * g2[0]**2 + 8 * g2[0], g2[0], 8), 6) if g2 else '해 없음')

# 구간 끝을 상수로(원문처럼 f(2)-f(0)=-15): b 위치로 나눠야 하고 답 바뀜
cnd = []
for r in sp.solve(2 * (-3 * b**2 + 8 * b) + 15, b):
    if r.is_real and r > 2 and inverse_ok(-3 * r**2 + 8 * r, r, 8): cnd.append(r)
for r in sp.solve((-3 * b**2 + 8 * b) * b + sp.integrate(-3 * x**2 + 8 * x, (x, b, 2)) + 15, b):
    if r.is_real and 0 < r <= 2 and inverse_ok(-3 * r**2 + 8 * r, r, 8): cnd.append(r)
assert len(cnd) == 1
ablation('구간 끝의 b(→f(2)-f(0))', sp.N(diff(4, 2, -3 * cnd[0]**2 + 8 * cnd[0], cnd[0], 8), 6))

# 계수 8 → 1(원문): 경계 1/3
_, rc = solve_all(c=1)
gc = [r for r in rc if inverse_ok(-3 * r**2 + r, r, 1)]
assert len(gc) == 1
ablation('이차식의 계수 8(→1)', sp.N(diff(4, 2, -3 * gc[0]**2 + gc[0], gc[0], 1), 6))
print('ALL OK')
