# -*- coding: utf-8 -*-
# 17번 후보 A17 2판 (J39: v2=6t-a, '만나는 순간 속도가 같다', 구간 k≤t≤2k, 최댓값 8 → k의 최댓값) 검증 · author='claude'
import sympy as sp, os, sys
t, a, m, k, c = sp.symbols('t a m k c', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def posdiff(v1, v2, start_q=0):
    return sp.expand(sp.integrate(v1 - v2, (t, 0, t)) - start_q)


def winmax(D, k0, w=2, left=None):
    """구간 [k0, w*k0] (left 가 주어지면 [left, k0]) 에서 |D| 의 최댓값(끝점 + 임계점 + 근 전수)"""
    lo, hi = (k0, w * k0) if left is None else (left, k0)
    pts = [lo, hi] + [r for r in sp.Poly(sp.diff(D, t), t).real_roots() if lo <= r <= hi]
    return max(abs(D.subs(t, p)) for p in pts)


# ---------- 1) a 결정: 만나는 순간 속도가 같다 → D(m)=0, D'(m)=0, m>0
v1 = R(3, 4) * t**2 + 1; v2 = 6 * t - a
Da = posdiff(v1, v2)
sols = sp.solve([Da.subs(t, m), sp.diff(Da, t).subs(t, m)], [a, m], dict=True)
sols = [s for s in sols if s[m] > 0]
assert sols == [{a: 8, m: 6}], sols
A = 8
D = Da.subs(a, A)
assert sp.factor(D) == sp.factor(t * (t - 6)**2 / 4)
# a=8 이면 출발 후 만나는 시각은 6 하나뿐이고 그때 속도가 같음
assert [r for r in sp.Poly(D, t).real_roots() if r > 0] == [6, 6] and (v1 - v2).subs({a: A, t: 6}) == 0
print('a = 8 유일(만나는 시각 6, 중근), D(t)=t(t-6)^2/4 ≥ 0')
assert sp.factor(sp.diff(D, t)) == sp.factor(R(3, 4) * (t - 2) * (t - 6)) and D.subs(t, 2) == 8
assert sp.factor(D - 8) == sp.factor((t - 2)**2 * (t - 8) / 4)
print("D'=(3/4)(t-2)(t-6), 극댓값 D(2)=8, D-8=(t-2)^2(t-8)/4")

# ---------- 2) k 전수: 정확 판정 + 조밀 유리수 표본
# 이론: [1,2] ∪ {4}
for kv in [R(1), R(3, 2), R(2), R(4)]:
    assert winmax(D, kv) == 8
for kv in [R(99, 100), R(201, 100), R(3), R(399, 100), R(401, 100), R(8), R(1, 2)]:
    assert winmax(D, kv) != 8, kv
good = [R(j, 100) for j in range(1, 1601) if winmax(D, R(j, 100)) == 8]
assert good == [R(j, 100) for j in range(100, 201)] + [R(4)], good[-5:]
# 연속 구간 사이 (2,4), (4,∞)의 각 부분에서 8 미만·초과가 바뀌지 않음을 식으로: 2<k<4 → [k,2k] ⊂ (2,8), D<8
assert sp.solve_univariate_inequality(sp.expand(8 - D) > 0, t, relational=False).contains(R(5))
assert sp.Interval.open(2, 8).is_subset(sp.solve_univariate_inequality(sp.expand(8 - D) > 0, t, relational=False))
assert sp.Interval.open(8, sp.oo).is_subset(sp.solve_univariate_inequality(sp.expand(D - 8) > 0, t, relational=False))
ANS = max(good)
assert ANS == 4
print('최댓값이 8 인 k: 1≤k≤2 또는 k=4 (0.01 간격 1600개 표본 + 식 판정) → k의 최댓값 =', ANS)

# ---------- 3) 선지
ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
vals = [int(x) for x in ch]
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals)
print('정답 4 = 선지 ②, 선지', vals, '공차 2 오름차순')

# ---------- 4) 오답
w_only_peak = max(x for x in good if x <= 2)            # 극대를 품는 경우만
w_left_end = [r for r in sp.Poly(sp.expand(D - 8), t).real_roots() if r > 2][0]   # D(k)=8 인 k
assert (w_only_peak, w_left_end) == (2, 8) and winmax(D, R(8)) == 400
assert set(IT['wrongs']) == {'2', '8'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 2(극대를 품는 경우만), 8(D(k)=8, 구간 [8,16] 최댓값 400)')

# ---------- 5) 원문 J39: 20/3 (③)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J39']; assert o[2] == '③'
d0 = posdiff(2 * t**3 - 2 * t, t**2 + 4 * t)
assert winmax(d0, R(3), left=0) == R(20, 3) and o[1][2] == r'\dfrac{20}3'
print('원문 J39 OK: 20/3 (③)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS

def kmax_for(Dx, H=8, w=2, step=100, top=1600):
    g = [R(j, step) for j in range(1, top + 1) if winmax(Dx, R(j, step), w) == H]
    return max(g) if g else None

# '만나는 순간 속도가 같다' 삭제: a 가 정해지지 않음 (a=7, 9 등에서 답이 다름/없음)
res = {av: kmax_for(posdiff(v1, v2.subs(a, av))) for av in (7, 9, 10)}
assert all(v != ANS for v in res.values())   # None: 최댓값 8 인 k 가 표본에 없음(극댓값 높이가 a 에 따라 바뀜)
ablation("'만나는 순간 두 점의 속도가 서로 같다'", '정해지지 않음', f'a 에 따라 {res}')

# '만나는 순간' → '출발 후 만난다'만: a 의 범위만 남음 (q(t)=t^2-12t+4(a+1) 이 양근을 가지면 됨 → a≤8 무수히 많음)
qa = t**2 - 12 * t + 4 * (a + 1)
assert all(any(r > 0 for r in sp.Poly(qa.subs(a, av), t).real_roots()) for av in (8, 5, 0, -3))
ablation("'속도가 서로 같다'(만나기만)", '정해지지 않음', 'a≤8 이면 모두 만남')

# 원점 동시 출발 삭제: Q 가 c 에서 출발하면 위치 차가 D-c
res = {cv: kmax_for(D - cv) for cv in (1, -1)}
assert all(v != ANS for v in res.values())
ablation("'동시에 원점을 출발'", '정해지지 않음', f'Q 출발점 c 에 따라 {res}')

# 구간 끝 계수: 왼쪽 끝을 0 으로(원문처럼) → [0, k] 에서 최댓값 8 인 k 의 최댓값 8
g0 = [R(j, 100) for j in range(1, 1601) if winmax(D, R(j, 100), left=0) == 8]
ablation('구간 k≤t≤2k → 0≤t≤k', max(g0))
# 구간 [k, 3k] 로 바꾸면 8/3
ablation('구간 끝 2k → 3k', kmax_for(D, w=3, step=300, top=4800))
# 최댓값 8 → 다른 값(예: 4) 이면 답이 달라짐
ablation('최댓값 8 → 4', kmax_for(D, H=4))
print('ALL OK')
