# -*- coding: utf-8 -*-
# 17번 후보 A17 (J37, 넓이 S(k)와 정적분의 부등식 → 정수 k의 개수) 검증 · author='claude'
import sympy as sp, mpmath as mp, os, sys, re
x, w = sp.symbols('x w', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
P = x**3 - 6 * x**2 + 12 * x                       # f(x) = P(x) - k
assert sp.expand(P - 8 - (x - 2)**3) == 0           # f(x) = (x-2)^3 + 8 - k
assert sp.factor(sp.diff(P, x)) == 3 * (x - 2)**2   # f'(x) = 3(x-2)^2 ≥ 0 → 증가


def area(kv, a=0, b=4):
    """S = ∫_a^b |f|, I = ∫_a^b f 를 정확히: 구간 안 영점(증가함수라 많아야 하나)에서 끊는다.
    돌려주는 값 (S, I, inside): 영점이 열린구간 안에 없으면 S = |I| 가 정확히 성립(유리수)."""
    f = P - kv
    F = sp.integrate(f, x)
    I = F.subs(x, b) - F.subs(x, a)
    fa, fb = f.subs(x, a), f.subs(x, b)
    if not (fa < 0 < fb):                             # 증가함수: 부호가 바뀌지 않음
        return sp.Abs(I), I, False
    al = 2 + sp.real_root(kv - 8, 3)                  # (α-2)^3 = k-8 의 실근
    assert abs(sp.N(f.subs(x, al), 50)) < 1e-40 and a < sp.N(al) < b
    A = -(F.subs(x, al) - F.subs(x, a)); B = F.subs(x, b) - F.subs(x, al)
    assert sp.N(A, 50) > 0 and sp.N(B, 50) > 0
    return A + B, I, True


def lt(u, v):
    """u < v (같으면 False). 무리수 비교는 60자리, 여유 1e-30 확인"""
    d = sp.simplify(v - u)
    if d == 0: return False
    n = sp.N(d, 60); assert abs(n) > 1e-30, (u, v)
    return n > 0


def ok(kv, left=True, right=True, coef=2, absr=True, leq_left=False, a=0, b=4):
    S, I, inside = area(kv, a, b)
    L = (lt(sp.Abs(I), S) or (leq_left and sp.simplify(sp.Abs(I) - S) == 0)) if left else True
    rhs = coef * (sp.Abs(I) if absr else I)
    Rr = lt(S, rhs) if right else True
    return L and Rr


# ---------- 일반식 (영점 2+w, w^3 = k-8, -2<w<2): A, B, S, 정적분
fw = (x - 2)**3 - w**3
A_ = sp.expand(-sp.integrate(fw, (x, 0, 2 + w))); B_ = sp.expand(sp.integrate(fw, (x, 2 + w, 4)))
assert sp.expand(A_ - (R(3, 4) * w**4 + 2 * w**3 + 4)) == 0 and sp.expand(B_ - (R(3, 4) * w**4 - 2 * w**3 + 4)) == 0
assert sp.expand(A_ - B_ - 4 * w**3) == 0                                   # 원리 줄: A-B = -∫_0^4 f = 4(k-8)
assert sp.expand(sp.integrate(fw, (x, 0, 4)) + 4 * w**3) == 0               # ∫_0^4 f = 4(8-k)
assert sp.expand(A_ + B_ - (8 + R(3, 2) * w**4)) == 0                       # S = 8 + 3/2 w^4
assert sp.factor(sp.diff(B_, w)) == 3 * w**2 * (w - 2)                      # B 는 w<2 에서 감소 (k 에 대해 감소)
assert sp.factor(A_) == (w + 2)**2 * (3 * w**2 - 4 * w + 4) / 4 and sp.factor(B_) == (w - 2)**2 * (3 * w**2 + 4 * w + 4) / 4
h = sp.expand(2 * 4 * w**3 - (A_ + B_))                                     # w>0: 2|∫| - S
assert sp.factor(sp.diff(h, w)) == -6 * w**2 * (w - 4) and h.subs(w, 1) == R(-3, 2)
assert sp.N(h.subs(w, sp.real_root(2, 3))) > 0 and sp.simplify(h.subs(w, sp.real_root(2, 3)) - (8 - 3 * sp.real_root(2, 3))) == 0
print('일반식: A-B=4w^3(=4(k-8)), S=8+3/2·w^4, B\'(w)=3w^2(w-2)≤0, h(w)=8w^3-8-3/2·w^4 는 0<w<4 에서 증가, h(1)=-3/2, h(∛2)=8-3∛2>0')

# ---------- 풀이의 수치: k=9 (α=3), k=7 (α=1), 대칭 S(16-k)=S(k)
B9 = sp.integrate((x - 2)**3 - 1, (x, 3, 4)); A7 = -sp.integrate((x - 2)**3 + 1, (x, 0, 1))
assert B9 == R(11, 4) and A7 == R(11, 4) and B9 > 2
S9, I9, _ = area(9)
assert sp.simplify(S9 - R(19, 2)) == 0 and I9 == -4 and not ok(9) and not ok(7) and not ok(8)
for kv in range(-20, 37):
    S1, I1, _ = area(kv); S2, I2, _ = area(16 - kv)
    assert abs(sp.N(S1 - S2, 50)) < 1e-40 and I1 == -I2
kk = sp.symbols('k', real=True)
fk = P - kk; gk = P - (16 - kk)
assert sp.expand(gk + fk.subs(x, 4 - x)) == 0                                # g(x) = -f(4-x)
print('k=9: α=3, B=11/4>2 (탈락), S(9)=19/2 · k=7: α=1, A=11/4 · g(x)=-f(4-x) → S(16-k)=S(k), 정적분 부호 반대')

# ---------- 정수 k 전수 (-40..56). 그 밖은 f(0)=-k≥0 또는 f(4)=16-k≤0 이라 부호가 바뀌지 않아 S=|∫| (왼쪽 부등식 거짓)
RNG = range(-40, 57)
SOL = [kv for kv in RNG if ok(kv)]
assert SOL == [1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15], SOL
for kv in RNG:
    S, I, inside = area(kv)
    assert inside == (0 < kv < 16)
    assert ok(kv, right=False) == inside                                     # 왼쪽 부등식 ⇔ 0<k<16
    if not inside: assert sp.simplify(S - sp.Abs(I)) == 0
for kv in (10**3, -10**3, 10**6, -10**6): assert not ok(kv)
# 독립 수치 확인 (mpmath 구적)
mp.mp.dps = 30
for kv in range(-3, 20):
    f_ = lambda t: abs(t**3 - 6 * t**2 + 12 * t - kv)
    z = 2 + mp.cbrt(kv - 8) if kv >= 8 else 2 - mp.cbrt(8 - kv)
    pts = [0, z, 4] if 0 < z < 4 else [0, 4]
    Sn = mp.quad(f_, pts); In = abs(32 - 4 * kv)
    assert (In < Sn - mp.mpf(10)**-15 and Sn < 2 * In - mp.mpf(10)**-15) == (kv in SOL), kv
ANS = len(SOL)
assert ANS == 12
print(f'정수 k 전수(-40..56, ±10^3, ±10^6) + mpmath 구적: 왼쪽 ⇔ 0<k<16, 해 {SOL} → {ANS}개')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 5
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {-1}
print('정답 12 = 선지 ⑤, 선지 16..12 공차 1 내림차순')

# ---------- 경우 분기 (다섯 갈래)
assert all(not ok(kv) and not area(kv)[2] for kv in range(-40, 1))            # k≤0: 부호 안 바뀜, S=|∫|
assert all(ok(kv) for kv in range(1, 7))                                      # 1≤k≤6: B>3A
assert [ok(kv) for kv in (7, 8, 9)] == [False, False, False]                   # 7, 9: 넓이 비 27:11 < 3, 8: 정적분 0
assert all(ok(kv) for kv in range(10, 16))                                    # 10≤k≤15: A>3B
assert all(not ok(kv) and not area(kv)[2] for kv in range(16, 57))            # k≥16
for kv in range(9, 16):                                                       # 8<k<16: S<2|∫| ⇔ A>3B ⇔ B<2(k-8)
    wv = sp.real_root(kv - 8, 3); Av, Bv = A_.subs(w, wv), B_.subs(w, wv)
    assert ok(kv) == lt(3 * Bv, Av) == lt(Bv, 2 * (kv - 8))
assert sp.simplify(A_.subs(w, 1) / B_.subs(w, 1)) == R(27, 11)
print('경우: k≤0 탈락 · 1..6 성립 · 7,8,9 탈락(넓이 비 27:11, 정적분 0) · 10..15 성립 · k≥16 탈락')

# ---------- 원문 J37: S - ∫_0^4 g = -∫_0^4 f = 16
f0 = P - 12
assert sp.integrate(-f0, (x, 0, 4)) == 16 and f0.subs(x, 4) == 4 and f0.subs(x, 0) == -12
g = lambda t: 2 + mp.cbrt(t + 4) if t + 4 >= 0 else 2 - mp.cbrt(-(t + 4))     # 역함수 g(x) = 2 + ∛(x+4)
c0 = 2 + mp.cbrt(4)                                                           # f 의 영점
S0 = mp.quad(g, [-12, -4, 0, 4]) - mp.quad(lambda t: t**3 - 6 * t**2 + 12 * t - 12, [c0, 4])
assert abs(S0 - mp.quad(g, [0, 4]) - 16) < mp.mpf(10)**-15
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
o = F.I['J37']
assert o[2] == '16' and o[1] is None
print('원문 J37 OK: S-∫_0^4 g = -∫_0^4 f = 16 (원문 정답 16, 단답)')

# ---------- 오답 근거
W15 = len([kv for kv in RNG if ok(kv, right=False)])                           # 왼쪽 부등식만
W14a = len([kv for kv in RNG if ok(kv, right=False) and area(kv)[1] != 0])     # 0<k<16 에서 k=8 만 뺌
W14b = len([kv for kv in range(0, 17) if kv not in (7, 8, 9)])                 # 닫힌구간으로 보아 k=0, 16 포함
W16 = len([kv for kv in range(0, 17) if kv != 8])
W6 = len([kv for kv in SOL if kv > 8])
assert (W15, W14a, W14b, W16, W6) == (15, 14, 14, 16, 6)
assert all(sp.simplify(area(kv)[0] - 32) == 0 and abs(area(kv)[1]) == 32 for kv in (0, 16))
assert all(v in ch for v in IT['wrongs']) and IT['wrongs'] == ['15', '14']
print('오답 근거 OK: 15(왼쪽만) · 14(k=8 만 뺌 / k=0,16 포함) · 16(0≤k≤16 에서 8 만 뺌) · 한쪽만 6(선지 밖)')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄은 통하되 그것만으로 끝나지 않음)
assert sp.solve(sp.Eq((P - kk).subs(x, 4), 4), kk) == [12]                     # 고정점 (4,4)는 k=12 에서만 → 변형에 없음
assert '역함수' not in IT['body'] and 'g(x)' not in IT['body']
# 원리 줄 A-B=4(k-8) 은 k=9 와 k=10 을 가르지 못한다(둘 다 A>B). 가르는 것은 B<2(k-8)
assert not ok(9) and ok(10) and 4 * (9 - 8) > 0 and 4 * (10 - 8) > 0
print('핵심 한 줄: 설정 줄(역함수·고정점 (4,4)·x절편 -12) 불통 · 원리 줄(A-B=4(k-8))은 통하나 k=9|10, k=15|16 경계를 정하지 못함')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
out = []
def ablation(cname, res, why=''):
    msg = (f'군더더기(답 그대로{"; " + why if why else ""})' if res == ANS else f'필요({res}{"; " + why if why else ""})')
    print(f'ABLATION 17 {cname}: {msg}'); out.append(msg)
# 1) 왼쪽 부등식 빼기: S<2|∫| 만 → k≥16 에서 S=|∫|<2|∫| 이라 끝없이 많음
assert all(ok(kv, left=False) for kv in list(range(16, 57)) + [10**3, 10**6]) and all(ok(kv, left=False) for kv in range(-40, 1))
ablation('왼쪽 부등식 |∫f|<S(k)', '정해지지 않음(k≤6 또는 k≥10 인 모든 정수)', '영점이 구간 밖인 k 가 모두 들어옴')
# 2) 오른쪽 부등식 빼기
ablation('오른쪽 부등식 S(k)<2|∫f|', len([kv for kv in RNG if ok(kv, right=False)]), '0<k<16 전부')
# 3) 계수 2 빼기: S<|∫| 는 불가능
ablation('오른쪽의 계수 2', len([kv for kv in RNG if ok(kv, coef=1)]), 'S<|∫| 인 k 는 없음')
# 4) 오른쪽 절댓값 빼기: S<2∫ → k<8 쪽만
ablation('오른쪽의 절댓값', len([kv for kv in RNG if ok(kv, absr=False)]), 'k=1..6 만')
# 5) '정수' 빼기: 실수 k 면 구간이라 끝없이 많음
assert ok(R(21, 2)) and ok(R(11, 2)) and ok(R(25, 2))
ablation("'정수 k'", '정해지지 않음(실수 k 는 끝없이 많음)', 'k=21/2, 11/2 등도 만족')
# 6) 왼쪽 부등호의 등호(< → ≤): S≥|∫| 는 늘 참이라 1)과 같아짐
assert ok(16, leq_left=True) and ok(0, leq_left=True) and ok(40, leq_left=True)
ablation('왼쪽 부등호에 등호 넣기', '정해지지 않음(k=0, 16, 17, … 이 들어옴)', '등호가 없어야 k≤0, k≥16 이 빠짐')
# 7) 직선 x=4 → x=6 (구간이 대칭 중심에 대해 대칭이 아님): 답이 달라짐
def ok6(kv):
    f = P - kv; Fq = sp.integrate(f, x); I = Fq.subs(x, 6) - Fq.subs(x, 0)
    if not (f.subs(x, 0) < 0 < f.subs(x, 6)): return False
    al = 2 + sp.real_root(kv - 8, 3)
    S = -(Fq.subs(x, al) - Fq.subs(x, 0)) + (Fq.subs(x, 6) - Fq.subs(x, al))
    return lt(sp.Abs(I), S) and lt(S, 2 * sp.Abs(I))
n6 = len([kv for kv in range(-40, 120) if ok6(kv)])
ablation('직선 x=4(→ x=6)', n6, '구간이 바뀌면 개수가 달라짐')
assert all(r_.startswith('필요') for r_ in out), out

# ---------- 형식·기록
import html
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html.unescape(t)))
assert len(plain(IT['body'])) >= len(plain(o[0])), (len(plain(IT['body'])), len(plain(o[0])))   # 문장 길이 원문 이상
assert IT['key'] == 'J37' and IT['cand'] == 'A17' and IT['db_ref'] == 'J37 킬러 설계A'
assert IT['core']['axis'] == '②' and set(IT['core']) == {'axis', 'setting', 'principle', 'new'}
assert '함정 추가' not in IT['vtype'] and IT['bunseok'] is False and 'cond' not in IT
assert {'OP28', 'OP11'} <= set(IT['ops']) and '\\[' not in IT['body']
print(f"문장 길이 {len(plain(IT['body']))}자 ≥ 원문 {len(plain(o[0]))}자 · 조건 상자 없음 · 줄 바꾼 식 없음")
print('ALL OK')
