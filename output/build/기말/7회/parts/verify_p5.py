# -*- coding: utf-8 -*-
# 17번 후보 A17 (J47 킬러 설계A 변형: 도함수 대칭 f'(1+x)=f'(1-x), 직선 y=-5x+7, ∫_1^2 f=k, 넓이가 정수인 k의 개수) 검증 · author='claude'
import sympy as sp, os, sys
x, u, t = sp.symbols('x u t', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
L = -5 * x + 7


def pmax(expr, a, b):
    """다항식 expr 의 [a,b] 최댓값(끝점 + 임계점)"""
    cr = [r for r in sp.real_roots(sp.Poly(sp.diff(expr, x), x)) if a <= r <= b] if sp.degree(expr, x) > 0 else []
    return max(sp.N(expr.subs(x, v)) for v in [a, b] + cr)


# ---------- 1) 설정: f'(1+x)=f'(1-x) → f(1+x)+f(1-x)=2f(1), f(1)=(7-3)/2=2, 직선이 (0,7),(1,2),(2,-3)을 지남
assert [L.subs(x, v) for v in (0, 1, 2)] == [7, 2, -3] and R(7 - 3, 2) == L.subs(x, 1)
IL = sp.integrate(L, (x, 1, 2)); assert IL == R(-1, 2)
print('직선 y=-5x+7 은 (0,7), (1,2), (2,-3)을 지나고 ∫_1^2(-5x+7)dx = -1/2; f(1)=(f(0)+f(2))/2=2')

# ---------- 2) k 의 범위: 1≤x≤2 에서 -3≤f≤2, 위 배치 -5x+7<f≤2, 아래 배치 -3≤f<-5x+7
up, lo = sp.integrate(2, (x, 1, 2)), sp.integrate(-3, (x, 1, 2))
assert (lo, up) == (-3, 2) and up - IL == IL - lo == R(5, 2)        # S=2|k+1/2| 의 상한 5 (끝값 제외)
S_of = lambda k: 2 * abs(k - IL)
ks = sorted({kk for S in range(1, 5) for kk in (IL + R(S, 2), IL - R(S, 2))})
assert all(lo < kk < up for kk in ks) and len(ks) == 8
assert ks == [R(-5, 2), -2, R(-3, 2), -1, 0, R(1, 2), 1, R(3, 2)]
assert S_of(up) == 5 and S_of(lo) == 5 and S_of(IL) == 0
ANS = len(ks)
print('S=2|k+1/2|, -3<k<2 (k≠-1/2) → 0<S<5 → S=1,2,3,4 → k =', ks, '→', ANS, '개')


# ---------- 3) 실제로 가능한지: 예시 함수 (위 배치: 다항식, 아래 배치: 상자 중심 대칭으로 뒤집은 조각함수)
def above(c, n=5):
    return L + c * (x - 1) * (1 - (x - 1)**(2 * n))


def check_above(c, n=5):
    f = above(c, n); g = sp.expand(f - L)
    assert f.subs(x, 0) == 7 and f.subs(x, 2) == -3 and f.subs(x, 1) == 2
    fp = sp.diff(f, x)
    assert sp.simplify(fp.subs(x, 1 + t) - fp.subs(x, 1 - t)) == 0                 # (가) 도함수 대칭
    assert sp.simplify(sp.diff(g, x).subs(x, 1 + t) - (c - c * (2 * n + 1) * t**(2 * n))) == 0 and c <= 5   # f' = c-5-c(2n+1)t^{2n} ≤ 0
    assert sorted(set(sp.real_roots(sp.Poly(g, x)))) == [0, 1, 2]                   # (나)
    assert g.subs(x, R(3, 2)) > 0
    k = sp.integrate(f, (x, 1, 2))
    S = sp.integrate(g, (x, 1, 2)) - sp.integrate(g, (x, 0, 1))
    assert S == S_of(k)
    return k, S


def check_below(c, n=5):
    fA = above(c, n)
    p12 = sp.expand(-1 - fA.subs(x, 3 - x))            # 1≤x≤2 (상자 중심 (3/2,-1/2) 대칭)
    p01 = sp.expand(4 - p12.subs(x, 2 - x))            # 0≤x≤1 (점 (1,2) 대칭)
    m = sp.diff(p12, x).subs(x, 2)
    pR = -3 + m * (x - 2); pL = sp.expand(4 - pR.subs(x, 2 - x))
    # 연속·미분가능(이음점 0, 1, 2)
    for a, b, v in ((p01, p12, 1), (p12, pR, 2), (pL, p01, 0)):
        assert a.subs(x, v) == b.subs(x, v) and sp.diff(a, x).subs(x, v) == sp.diff(b, x).subs(x, v)
    assert p01.subs(x, 0) == 7 and p12.subs(x, 2) == -3 and p12.subs(x, 1) == 2
    # (가): f'≤0, 도함수 대칭
    assert m < 0 and pmax(sp.diff(p12, x), 1, 2) <= 0 and pmax(sp.diff(p01, x), 0, 1) <= 0
    assert sp.simplify(sp.diff(p12, x).subs(x, 1 + t) - sp.diff(p01, x).subs(x, 1 - t)) == 0
    assert sp.simplify(sp.diff(pR, x).subs(x, 1 + t) - sp.diff(pL, x).subs(x, 1 - t)) == 0
    # (나): 교점은 0, 1, 2 뿐
    z = set()
    for pc, a, b in ((p12, 1, 2), (p01, 0, 1)):
        z |= {r for r in sp.real_roots(sp.Poly(sp.expand(pc - L), x)) if a <= r <= b}
    assert z == {0, 1, 2}
    assert sp.expand(pR - L) == c * (x - 2) and sp.expand(pL - L) == c * x      # 바깥에서는 0, 2 말고 만나지 않음
    assert (p12 - L).subs(x, R(3, 2)) < 0
    k = sp.integrate(p12, (x, 1, 2))
    S = -sp.integrate(p12 - L, (x, 1, 2)) + sp.integrate(p01 - L, (x, 0, 1))
    assert S == S_of(k)
    return k, S


got = set()
for S in range(1, 5):
    c = R(6, 5) * S                      # n=5: S = 2c(1/2-1/12) = 5c/6
    kA, SA = check_above(c); kB, SB = check_below(c)
    assert SA == SB == S and kA == IL + R(S, 2) and kB == IL - R(S, 2)
    got |= {kA, kB}
assert got == set(ks)
print('예시 함수로 8개 k 모두 실현(위 배치 4개 · 아래 배치 4개): 미분가능, f\'≤0, 도함수 대칭, 교점 3개, 넓이 직접 적분 확인')
# 상한 5 는 가까이 갈 수 있으나 닿지 않음: c=5, n→∞ 이면 S=5(1-1/(n+1))
for n in (5, 20, 100):
    k_, S_ = check_above(5, n); assert S_ == 5 * (1 - R(1, n + 1)) and S_ < 5
print('S 의 상한 5 는 닿지 않음(c=5, n=100 이면 S=500/101): k=2 이면 [1,2)에서 f=2 → f(2)=-3 과 연속 모순')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 4
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {2}
print('정답 8 = 선지 ④, 선지 2..10 공차 2')

# ---------- 4) 오답
w4 = len([kk for kk in ks if kk > IL])                                  # 한 배치만
w10 = len({kk for S in range(1, 6) for kk in (IL + R(S, 2), IL - R(S, 2)) if lo <= kk <= up})   # 끝값 포함
assert (w4, w10) == (4, 10)
assert {str(w4), str(w10)} == set(IT['wrongs']) and all(w in ch for w in IT['wrongs'])
assert ANS not in (10, 7, -3, 1, 2, -5, 3, 5)
print('오답 근거 OK: 4(한 배치만) · 10(끝값 k=2, -3 포함); 정답 8 은 원문 답 10·문항 속 수와 다름')

# ---------- 5) 원문 J47: 10
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J47']; assert o[2] == '②' and o[1][1] == '10'
f0 = -x + R(5, 6) * x * (1 - x**4 / 81)                     # 감소하는 기함수 예
assert sp.simplify(f0 + f0.subs(x, -x)) == 0 and f0.subs(x, 3) == -3 and sp.integrate(f0, (x, -3, 0)) == 2
assert pmax(sp.diff(f0, x), -10, 10) <= 0 and sorted(set(sp.real_roots(sp.Poly(sp.expand(f0 + x), x)))) == [-3, 0, 3]
A0 = sp.integrate(f0 + x, (x, 0, 3)) - sp.integrate(f0 + x, (x, -3, 0))
assert A0 == 2 * (R(9, 2) - 2) == 5 and 2 * A0 == 10        # 역함수 쪽은 y=-x 대칭이라 2배
print('원문 J47 OK: 곡선과 y=-x 사이 2(9/2-2)=5, 역함수까지 10 (②)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS

# (가) 도함수 대칭 삭제: 오른쪽은 n=5, 왼쪽은 n=2 모양(이음점 x=1 에서 기울기 같음) → 같은 k 에 넓이가 다름
c = R(12, 5)
gR = c * (x - 1) * (1 - (x - 1)**10); gL = c * (x - 1) * (1 - (x - 1)**4)
assert sp.diff(gR, x).subs(x, 1) == sp.diff(gL, x).subs(x, 1) and pmax(sp.diff(gL, x) - 5, 0, 1) <= 0
kk = sp.integrate(L + gR, (x, 1, 2)); S2 = sp.integrate(gR, (x, 1, 2)) - sp.integrate(gL, (x, 0, 1))
assert kk == R(1, 2) and S2 != S_of(kk)
ablation("(가) f'(1+x)=f'(1-x)", '정해지지 않음', f'k=1/2 인데 넓이 {S2}(대칭이면 2) — 왼쪽 부분의 넓이가 k 로 정해지지 않음')

# (가) f'≤0 삭제: c 에 제한이 없어 S=5c/6 이 모든 양수 → k 가 무수히 많음
k_, S_ = sp.integrate(above(60), (x, 1, 2)), 2 * sp.integrate(above(60) - L, (x, 1, 2))
assert S_ == 50 and k_ > up
ablation("(가) f'(x)≤0", '무수히 많음', f'예: k={k_} 이면 넓이 {S_}')

# (나) 삭제: 교점이 5개인 감소함수 → 넓이가 2|k+1/2| 보다 큼
g5 = -(x - 1) * (1 - (x - 1)**2) * (R(1, 4) - (x - 1)**2)
assert pmax(sp.diff(g5, x) - 5, -50, 50) <= 0 and len(set(sp.real_roots(sp.Poly(sp.expand(g5), x)))) == 5
assert sp.simplify(sp.diff(g5, x).subs(x, 1 + t) - sp.diff(g5, x).subs(x, 1 - t)) == 0 and g5.subs(x, 0) == 0 == g5.subs(x, 2)
k5 = sp.integrate(L + g5, (x, 1, 2))
S5 = 2 * abs(sp.integrate(g5, (x, 1, R(3, 2))) - sp.integrate(g5, (x, R(3, 2), 2)))
assert S5 > S_of(k5)
ablation('(나) 실근 3개', '정해지지 않음', f'교점 5개 예: k={k5}, 넓이 {S5} ≠ 2|k+1/2|={S_of(k5)}')

# f(0)=7 삭제: 중심 높이가 정해지지 않음 — 점 (1,1) 대칭 예(f(0)=5, f(2)=-3), 교점 x=-2, 2, 3
phi = 1 - R(1, 6) * (u - 1) * (u + 3) * (u - 2)
assert sp.expand(phi + phi.subs(u, -u)) == 0
fE = (L - 1 + phi.subs(u, x - 1)); gE = sp.expand(fE - L)
assert fE.subs(x, 2) == -3 and fE.subs(x, 0) == 5 and pmax(sp.diff(fE, x), -50, 50) <= 0
assert sp.simplify(sp.diff(fE, x).subs(x, 1 + t) - sp.diff(fE, x).subs(x, 1 - t)) == 0
assert sorted(set(sp.real_roots(sp.Poly(gE, x)))) == [-2, 2, 3]
kE = sp.integrate(fE, (x, 1, 2)); SE = sp.integrate(sp.Abs(gE), (x, -2, 3))
assert SE != S_of(kE)
ablation('f(0)=7', '정해지지 않음', f'f(0)=5 인 예: 교점 -2, 2, 3, k={kE}, 넓이 {SE} — 직선이 대칭의 중심을 지나지 않음')
ablation('f(2)=-3', '정해지지 않음', '같은 이유(f(0)=7 만으로는 f(1) 과 오른쪽 교점이 정해지지 않음)')

# 새 장치: 두 배치 · 끝값 · 직선의 기울기
ablation('두 배치(위·아래) → 원문처럼 한 배치만', w4)
ablation('끝값 제외 → 포함', w10)
# 직선을 원문 기울기 -1 로(y=-x+3, f(0)=3, f(2)=1): 상자 1×1, S<1 → 0개
IL1 = sp.integrate(-x + 3, (x, 1, 2)); n1 = len([S for S in range(1, 10) if S < 2 * (2 - IL1)]) * 2
assert n1 == 0
ablation('직선의 기울기 -5 → 원문 -1', n1, 'S<1')
print('ALL OK')
