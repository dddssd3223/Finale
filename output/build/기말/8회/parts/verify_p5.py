# -*- coding: utf-8 -*-
# 17번 후보 A17 (J39 킬러 설계A: 누적 최댓값 M(T)와 그 정적분) 검증 · author='claude'
import sympy as sp, numpy as np, os, sys
t, T, s, c = sp.symbols('t T s c', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def setup(v1, v2, start_q=0):
    x1 = sp.integrate(v1.subs(t, s), (s, 0, t))
    x2 = start_q + sp.integrate(v2.subs(t, s), (s, 0, t))
    return sp.expand(x1 - x2)


def cummax_exact(Dt, U):
    """g=|D|의 [0,T] 최댓값 M(T)를 조각으로 만들어 ∫_0^U M 을 정확히 계산(경계는 유리수여야 함).
    방법: 후보 경계 = 0, U, D의 근, D'의 근, 그리고 각 극대 높이에 다시 닿는 시각. 그 사이 조각마다
    M 은 '|D|(T)' 또는 '상수'이므로 중점에서 판정한다."""
    pts = {R(0), sp.nsimplify(U)}
    for r in sp.Poly(Dt, t).real_roots() + sp.Poly(sp.diff(Dt, t), t).real_roots():
        if 0 < r < U: pts.add(r)
    for r in list(pts):
        h = abs(Dt.subs(t, r))
        for q in sp.Poly(sp.expand(Dt - h), t).real_roots() + sp.Poly(sp.expand(Dt + h), t).real_roots():
            if 0 < q < U: pts.add(q)
    pts = sorted(pts)
    assert all(p.is_rational for p in pts), pts
    total = 0; pieces = []
    for a, b in zip(pts[:-1], pts[1:]):
        m = (a + b) / 2
        # 중점에서의 누적 최댓값(조밀 표본 + 정확값 후보)
        cand = [abs(Dt.subs(t, p)) for p in pts if p <= m] + [abs(Dt.subs(t, m))]
        cand += [abs(Dt.subs(t, r)) for r in sp.Poly(sp.diff(Dt, t), t).real_roots() if 0 <= r <= m]
        Mm = max(cand)
        g = Dt if Dt.subs(t, m) >= 0 else -Dt
        if Mm == g.subs(t, m):
            total += sp.integrate(g, (t, a, b)); pieces.append((a, b, 'D'))
        else:
            total += Mm * (b - a); pieces.append((a, b, Mm))
    return total, pieces


def cummax_numeric(Dt, U, N=400001):
    f = sp.lambdify(t, Dt, 'numpy'); x = np.linspace(0, float(U), N)
    return np.trapezoid(np.maximum.accumulate(np.abs(f(x))), x)


# ---------- 1) 설정: 위치 차
v1 = R(3, 4) * t**2 + 1; v2 = 6 * t - 8
D = setup(v1, v2)
assert sp.factor(D) == sp.factor(t * (t - 6)**2 / 4)
assert sp.factor(sp.diff(D, t)) == sp.factor(R(3, 4) * (t - 2) * (t - 6))
assert D.subs(t, 2) == 8 and D.subs(t, 6) == 0
assert sp.factor(D - 8) == sp.factor((t - 2)**2 * (t - 8) / 4)
print('D(t)=x1-x2=t(t-6)^2/4 ≥ 0, D\'=(3/4)(t-2)(t-6), D(2)=8, D-8=(t-2)^2(t-8)/4')

# ---------- 2) M(T) 조각 전수 확인
# (i) 0<T≤2: D 증가 → M=D(T); (ii) 2≤T≤8: max=8; (iii) T≥8: M=D(T)
assert all(sp.diff(D, t).subs(t, x) >= 0 for x in [R(k, 10) for k in range(0, 21)])
# [0,8]에서 D≤8: 8-D = (t-2)^2(8-t)/4 ≥ 0
assert sp.factor(8 - D) == sp.factor((t - 2)**2 * (8 - t) / 4)
# T≥8: D는 t≥6에서 증가하고 D(T)≥8 = 앞 구간 최댓값 → M=D(T)
assert all(sp.diff(D, t).subs(t, x) > 0 for x in [6 + R(k, 10) for k in range(1, 50)])
for Tv in [R(1, 2), 1, 2, 3, 6, 7, 8, 9, 10]:
    exact = max([D.subs(t, 0), D.subs(t, Tv)] + [D.subs(t, r) for r in (2, 6) if r <= Tv])
    piece = D.subs(t, Tv) if (Tv <= 2 or Tv >= 8) else 8
    assert exact == piece, (Tv, exact, piece)
F = sp.integrate(D, (t, 0, T))
assert sp.expand(F) == sp.expand(T**4 / 16 - T**3 + R(9, 2) * T**2)
I02, I810 = F.subs(T, 2), F.subs(T, 10) - F.subs(T, 8)
assert (I02, I810) == (11, 43)
ANS = I02 + 8 * 6 + I810
assert ANS == 102
tot, pieces = cummax_exact(D, 10)
assert tot == ANS, (tot, pieces)
assert abs(cummax_numeric(D, 10) - 102) < 1e-3
print('M(T): D(T) [0,2] · 8 [2,8] · D(T) [8,∞) ; ∫_0^10 M = 11+48+43 =', ANS, '(조각 자동 분해·수치 적분 일치)', pieces)
# 경계 판단: T=2 미분가능(D'(2)=0), T=8 좌미분 0 · 우미분 9
assert sp.diff(D, t).subs(t, 2) == 0 and sp.diff(D, t).subs(t, 8) == 9
print('경계: T=2에서 M 미분가능, T=8에서 좌미분 0 · 우미분 9 (꺾임)')

# ---------- 3) 선지
ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 3
vals = [int(x) for x in ch]
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals)
print('정답 102 = 선지 ③, 선지', vals, '공차 11 오름차순')

# ---------- 4) 오답
W_reset = I02 + 8 * 4 + (F.subs(T, 10) - F.subs(T, 6))       # t=6 만나는 시각에서 최댓값이 다시 시작
W_flat = 8 * 10                                              # 극댓값 8 을 전 구간에
W_dist = F.subs(T, 10)                                       # 거리 자체 적분(선지 밖)
assert (W_reset, W_flat, W_dist) == (91, 80, 75)
# 만나는 시각에서 다시 시작하는 누적 최댓값을 직접 계산해도 91
f = sp.lambdify(t, D, 'numpy'); x = np.linspace(0, 10, 400001); g = f(x); k = np.searchsorted(x, 6.0)
Mr = np.concatenate([np.maximum.accumulate(g[:k]), np.maximum.accumulate(g[k:])])
assert abs(np.trapezoid(Mr, x) - 91) < 1e-3
assert set(IT['wrongs']) == {'91', '80'} and all(w in ch for w in IT['wrongs'])
assert str(W_dist) not in ch
assert ANS not in (20, 3, 6, 8, 10, 1, 4)    # 원문 답 20/3 · 문항 속 수와 다름
print('오답 근거 OK: 91(만나는 시각에서 최댓값 재시작), 80(극댓값 8 전 구간); 거리 적분 75 는 선지 밖')

# ---------- 5) 원문 J39: 20/3 (③)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J39']; assert o[2] == '③'
d0 = setup(2 * t**3 - 2 * t, t**2 + 4 * t)
assert sp.factor(sp.diff(d0, t)) == sp.factor(t * (2 * t + 3) * (t - 2))
cands = [abs(d0.subs(t, v)) for v in (0, 2, 3)]
assert max(cands) == R(20, 3) and o[1][2] == r'\dfrac{20}3'
print('원문 J39 OK: 극값 |d(2)|=20/3 vs 끝값 |d(3)|=9/2 → 20/3 (③)')

# ---------- 6) 답의 유일성: 조각 분해를 경계 후보 전수로(D, D\', D=±극값 의 모든 실근) 다시 확인
allpts = set()
for poly in (D, sp.diff(D, t), D - 8, D + 8):
    allpts |= {r for r in sp.Poly(sp.expand(poly), t).real_roots() if 0 <= r <= 10}
assert allpts == {0, 2, 6, 8}, allpts
print('경계 후보 전수 {0,2,6,8}: 6 은 D=0 인 중근(최댓값 변화 없음), 실제 경계는 2·8 뿐 → 답 유일')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS

# '시각 t=0일 때 모두 원점' 삭제: Q 가 c 에서 출발하면 위치 차 D-c → 값이 c 에 따라 달라짐
vals_c = {}
for cv in (2, -2, 4):
    Dc = setup(v1, v2, start_q=cv)
    vals_c[cv] = round(cummax_numeric(Dc, 10), 3)
assert len(set(vals_c.values())) == 3 and all(abs(v - 102) > 0.5 for v in vals_c.values())
ablation("'시각 t=0일 때 모두 원점'", '정해지지 않음', f'Q 출발점 c 에 따라 {vals_c}')

# '0≤t≤T 에서의 최댓값' 삭제 → 시각 T 의 거리
ablation("'0≤t≤T에서의 최댓값'(시각 T의 거리로)", W_dist)

# v1 의 상수항 1 삭제(중근 설정이 일하는지): D = t(t-4)(t-8)/4, 부호가 바뀜
Dn = setup(R(3, 4) * t**2, v2)
assert sp.factor(Dn) == sp.factor(t * (t - 4) * (t - 8) / 4)
vn = cummax_numeric(Dn, 10)
ablation("v1 의 상수항 1(위치 차의 중근)", round(vn, 3), '두 점이 t=4, 8에서 앞뒤가 바뀜')

# 구간 시작 0 → 만나는 시각 이후만 보는 학생(재시작)과 구별됨
ablation('만나는 시각 6에서 앞뒤 그대로(중근) 판단', W_reset)
ablation('극댓값이 다시 따라잡히는 시각 T=8 판단', W_flat, '8을 끝까지 쓰면 80, 거리 적분이면 75')
print('ALL OK')
