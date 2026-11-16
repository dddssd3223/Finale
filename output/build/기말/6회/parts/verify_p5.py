# -*- coding: utf-8 -*-
# 17번 후보 A17 (M31 킬러 설계A 변형: h(t)=g(t)+g(c-2t), p(c)=불연속점 개수, m=min p, n=#{c: p(c)=m}, mn) 검증 · author='claude'
import sympy as sp, os, sys
from fractions import Fraction as Fr
x = sp.symbols('x', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
f = x**3 - 3 * x**2 - 9 * x + 10


# ---------- 1) g(t) 를 근 개수로 직접 계산해 표 확인
def g_exact(tv, F=f):
    tv = sp.nsimplify(tv)
    if tv < 0: return 0
    rs = set(sp.real_roots(sp.Poly(F - tv, x))) | set(sp.real_roots(sp.Poly(F + tv, x)))
    return len(rs)

assert sp.solve(sp.diff(f, x), x) == [-1, 3] and f.subs(x, -1) == 15 and f.subs(x, 3) == -17
tbl = {Fr(-1): 0, Fr(0): 3, Fr(1): 6, Fr(14): 6, Fr(15): 5, Fr(16): 4, Fr(17): 3, Fr(18): 2, Fr(40): 2}
for tv, v in tbl.items(): assert g_exact(tv) == v, (tv, g_exact(tv))
print('g(t): 0 (t<0), 3 (t=0), 6 (0<t<15), 5 (t=15), 4 (15<t<17), 3 (t=17), 2 (t>17) — 근 개수 직접 계산 확인')


def g(t, P=15, Q=17):
    if t < 0: return 0
    if t == 0: return 3
    if t < P: return 6
    if t == P: return 5
    if t < Q: return 4
    if t == Q: return 3
    return 2


def disc_pts(c, k=2, sign=1, gf=g):
    """h(t)=g(t)+g(c-k t) (sign=1) 의 불연속점. 후보는 g 와 g(c-kt) 의 불연속점뿐."""
    h = lambda t: gf(t) + sign * gf(c - k * t)
    cands = {Fr(0), Fr(15), Fr(17)} | {(c - Fr(v)) / k for v in (0, 15, 17)}
    e = Fr(1, 10**6)
    return sorted(t for t in cands if not (h(t - e) == h(t) == h(t + e)))


def scan(k=2, gf=g):
    """c 전수: 개수가 바뀔 수 있는 c 는 두 불연속점이 겹치는 값뿐 → 그 값들 + 그 사이·바깥 표본"""
    special = sorted({Fr(u) + k * Fr(v) for u in (0, 15, 17) for v in (0, 15, 17)})
    samples = set(special)
    for i in range(len(special) - 1): samples.add((special[i] + special[i + 1]) / 2)
    samples |= {special[0] - 7, special[-1] + 7}
    samples |= {Fr(n, 4) for n in range(-200, 400)}
    return {c: len(disc_pts(c, k, gf=gf)) for c in samples}


# ---------- 2) k=2 전수
P2 = scan(2)
m = min(P2.values()); C = sorted(c for c, v in P2.items() if v == m); n = len(C)
assert m == 4 and C == [0, 45, 47, 49, 51], (m, C)
assert sorted(c for c, v in P2.items() if v == 5) == [15, 17, 30, 34]
assert set(P2.values()) == {4, 5, 6}
ANS = m * n
assert ANS == 20
# 각 겹침의 좌극한·함숫값·우극한 합 (해설 표)
def lvr(c, t0):
    e = Fr(1, 10**6); return tuple(g(t) + g(c - 2 * t) for t in (t0 - e, t0, t0 + e))
assert lvr(0, 0) == (6, 6, 6) and lvr(45, 15) == (10, 10, 10) and lvr(51, 17) == (6, 6, 6)
assert lvr(47, 15) == (8, 8, 8) and lvr(49, 17) == (8, 8, 8) and lvr(15, 0) == (4, 8, 12)
print(f'k=2: p(c) ∈ {{4,5,6}}, 최솟값 m=4 ⇔ c ∈ {[str(c) for c in C]} (n=5), p=5 ⇔ c ∈ {{15,17,30,34}} → mn = {ANS}')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {-4}
print('정답 20 = 선지 ②, 선지 24..8 공차 4 내림차순')

# ---------- 3) 오답 근거
w16 = 4 * len([c for c in C if c != 0])                     # c=0 놓침
same_level = [0, 45, 51]                                    # 같은 높이끼리만 상쇄로 봄(엇갈린 47, 49 놓침)
assert all(c in C for c in same_level)
w12 = 4 * len(same_level)
w8 = 4 * len([c for c in same_level if c != 0])             # 둘 다
assert (w16, w12, w8) == (16, 12, 8)
assert {str(w16), str(w12), str(w8)} == set(IT['wrongs']) and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 16(c=0 놓침) · 12(엇갈린 겹침 47·49 놓침) · 8(둘 다)')
# 정답이 문제 속 다른 수·원문 답과 겹치지 않음
assert ANS not in (3, 9, 10, 15, 17, 2, 36, 4, 5)

# ---------- 4) 원문 M31 직접 풀기: 36
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['M31']
assert o[2] == '⑤' and o[1][4] == '36'
ho = lambda t: g(t) - g(t - 2)
cands = {Fr(v) for v in (0, 15, 17, 2, 17, 19)}
e = Fr(1, 10**6)
dpo = sorted(t for t in cands if not (ho(t - e) == ho(t) == ho(t + e)))
assert dpo == [0, 2, 15, 19] and sum(dpo) == 36
print('원문 M31 OK: h=g(t)-g(t-2) 불연속 0, 2, 15, 19 (17 상쇄) → 36 (원문 ⑤)')

# ---------- 5) 핵심 한 줄 (①형: 원문 원리 '같은 방향·크기 점프 겹치면 상쇄' 불통)
# 원문 원리를 그대로 적용(같은 방향 점프가 겹칠 때 지움)하면 합 h=g(t)+g(c-2t) 에서는 지워지는 점이 없다고 판정 → 틀림
same_dir_cancel = False
for c in C:
    for t0 in disc_pts(c, 2) + [Fr(0), Fr(15), Fr(17)]:
        pass
# 실제로 지워지는 겹침은 모두 '반대 방향' 점프
def jump(fun, t0):
    e = Fr(1, 10**6); return (fun(t0) - fun(t0 - e), fun(t0 + e) - fun(t0))
for c, t0 in ((0, 0), (45, 15), (47, 15), (49, 17), (51, 17)):
    j1 = jump(g, Fr(t0)); j2 = jump(lambda t: g(c - 2 * t), Fr(t0))
    assert j1[0] == -j2[0] and j1[1] == -j2[1] and j1[0] != 0
print('핵심: 지워지는 겹침 다섯 모두 반대 방향·같은 크기 점프 → 원문 원리 줄(같은 방향이 지워짐) 불통')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})')
    assert res != ANS

# (1) 계수 2 빼기 (g(c-t)): c=32 에서 15·17 동시 상쇄 → m=2, n=1
P1 = scan(1); m1 = min(P1.values()); C1 = [c for c, v in P1.items() if v == m1]
assert m1 == 2 and C1 == [32]
ablation('g(c-2t)의 계수 2 (→ g(c-t))', m1 * len(C1), 'c=32 에서 두 점 동시 상쇄')
# (2) 반사 빼기 (g(t-c) 꼴, 원문처럼 같은 쪽 이동, 계수 2: g(2t-c))
def scan_shift(k=2):
    out = {}
    for n_ in range(-200, 400):
        c = Fr(n_, 4)
        h = lambda t: g(t) + g(k * t - c)
        cands = {Fr(0), Fr(15), Fr(17)} | {(c + Fr(v)) / k for v in (0, 15, 17)}
        out[c] = len([t for t in cands if not (h(t - e) == h(t) == h(t + e))])
    return out
PS = scan_shift(); ms = min(PS.values()); ns_ = len([c for c, v in PS.items() if v == ms])
ablation("반사 c-2t (→ 2t-c)", f'm={ms}, c 가 {ns_}개 이상 → {ms * ns_}', '같은 방향 점프는 합에서 안 지워짐')
# (3) '+' 를 원문처럼 '-' 로: h=g(t)-g(c-2t)
def scan_minus():
    out = {}
    for n_ in range(-200, 400):
        c = Fr(n_, 4)
        h = lambda t: g(t) - g(c - 2 * t)
        cands = {Fr(0), Fr(15), Fr(17)} | {(c - Fr(v)) / 2 for v in (0, 15, 17)}
        out[c] = len([t for t in cands if not (h(t - e) == h(t) == h(t + e))])
    return out
PM = scan_minus(); mm = min(PM.values()); nm = len([c for c, v in PM.items() if v == mm])
ablation("합 + (→ 차 -)", f'm={mm}, c {nm}개 → {mm * nm}', '')
# (4) 'p(c)=m 을 만족시키는 c 의 개수'를 빼고 m 만 물으면 4 (선지 밖) — 묻는 식이 일함
ablation("n (c 의 개수)", m, 'm 만으로는 4')
print('ALL OK')
