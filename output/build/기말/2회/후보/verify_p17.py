# -*- coding: utf-8 -*-
# p17.py (2회 17번 Claude 후보 claude17) 검증
# 원문 M31 풀이(36) · g 표(sympy 실근 개수로 확인) · h=g(g(t)+k)를 실제 방정식으로 확인 · k별 불연속점 개수(기호 + 격자) ·
# 정답 유일성 · 선지 등차 · 오답 근거 · 원문 원리 줄 불통 · 조건 빼 보기 · 길이
import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy import Rational as R, Interval, Union, S, oo

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p17.py')).read(), ns)
IT = ns['ITEMS']; P = IT[17]
assert list(IT) == [17] and P['author'] == 'claude' and P['cand'] == 'claude17' and P['key'] == 'M31'
assert P['core']['axis'] == '①' and all(P['core'][k] for k in ('setting', 'principle', 'new'))
assert P['effect'] == '어려워짐' and P['bunseok'] is False and P['precedent'] and P['vtype']
assert 'cond' not in P and '\\[' not in P['body']          # 원문처럼 상자·줄 바꾼 식 없음
x = sp.symbols('x', real=True)
f = x**3 - 3*x**2 - 9*x + 10
fp = sp.diff(f, x)

# ===== 정확한 실근 개수: |f(x)| = s 의 서로 다른 실근 개수 (s 유리수) =====
def ndist(poly):
    p = sp.Poly(sp.expand(poly), x)
    return sp.Poly(sp.sqf_part(p.as_expr()), x).count_roots()
def G_exact(s, F=f, absval=True):
    s = R(s)
    if not absval:
        return ndist(F - s)
    if s < 0: return 0
    if s == 0: return ndist(F)
    return ndist(F - s) + ndist(F + s)      # f=s, f=-s 는 공통근이 없음

# ===== 설정: 극값과 g 표 =====
assert sp.expand(fp - 3*(x + 1)*(x - 3)) == 0
assert f.subs(x, -1) == 15 and f.subs(x, 3) == -17
assert sp.expand(f - 15 - (x - 5)*(x + 1)**2) == 0 and sp.expand(f + 17 - (x - 3)**2*(x + 3)) == 0
def g(t):
    t = Fr(t)
    if t < 0: return 0
    if t == 0: return 3
    if t < 15: return 6
    if t == 15: return 5
    if t < 17: return 4
    if t == 17: return 3
    return 2
tg = sorted(set([Fr(n, 4) for n in range(-12, 121)] + [Fr(15) + d for d in (Fr(1, 1000), -Fr(1, 1000))] + [Fr(17) + d for d in (Fr(1, 1000), -Fr(1, 1000))] + [Fr(1, 1000), -Fr(1, 1000)]))
for t in tg:
    assert G_exact(t) == g(t), (t, G_exact(t), g(t))
print(f'설정: f\'=3(x+1)(x-3), 극값 15, -17 → g 표(0|3|6|5|4|3|2) sympy 실근 개수 {len(tg)}점 일치 OK')

# ===== 원문 M31: h(t)=g(t)-g(t-2)의 불연속점 합 36 =====
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말'); sys.path.insert(0, '/home/user/Finale/template/db/parts')
import items_final as F
E = Fr(1, 10**4)
def discs(H, cands):
    return [c for c in cands if not (H(c - E) == H(c) == H(c + E))]
h0 = lambda t: g(t) - g(t - 2)
cand0 = sorted({0, 15, 17, 2, 19})
D0 = discs(h0, cand0)
# 후보 밖에서는 g, g(t-2)가 모두 일정 → 격자로도 확인
grid0 = [Fr(n, 8) for n in range(-40, 200)]
assert [t for t in grid0 if not (h0(t - E) == h0(t) == h0(t + E))] == D0
assert D0 == [0, 2, 15, 19] and sum(D0) == 36
assert F.I['M31'][2] == '⑤' and F.I['M31'][1][4] == '36'
print('원문 M31: h=g(t)-g(t-2) 불연속점', D0, '(t=17은 같은 모양 겹침으로 상쇄) 합 36 → ⑤ OK')

# ===== 변형의 h(t)=g(g(t)+k): 실제 방정식 |f(x)|=g(t)+k의 실근 개수와 같음 =====
for k in (R(1), R(9), R(10), R(12), R(14), R(15), R(16), R(18)):
    for t in (-1, 0, R(1, 2), 7, 15, 16, 17, 20):
        assert G_exact(G_exact(t) + k) == g(g(t) + Fr(k)), (k, t)
print('h(t)=g(g(t)+k): 방정식 |f(x)|=g(t)+k의 서로 다른 실근 개수와 표본 64점 일치 OK')

def Nset(k, gg=g, pts=(0, 15, 17), noleft=False):
    h = lambda t: gg(gg(t) + k)
    out = []
    for s in pts:
        Lv, Mv, Rv = h(s - E), h(s), h(s + E)
        bad = (Mv != Rv) if (noleft and s == 0) else not (Lv == Mv == Rv)
        if bad: out.append(s)
    return out

# h가 바뀔 수 있는 점은 t=0,15,17뿐 (g가 일정한 구간에서 h도 일정) — 격자로 확인
for k in (Fr(9), Fr(12), Fr(15), Fr(27, 2)):
    h = lambda t: g(g(t) + k)
    jumps = [t for t in grid0 if not (h(t - E) == h(t) == h(t + E))]
    assert set(jumps) <= {0, 15, 17} and jumps == Nset(k), (k, jumps)

# ===== 기호: 각 점에서 불연속인 k의 집합 (세 높이가 g의 같은 평평한 열린구간에 있지 않음) =====
kk = sp.symbols('k', real=True)
plates = [Interval.open(-oo, 0), Interval.open(0, 15), Interval.open(15, 17), Interval.open(17, oo)]
def cont_set(offs):
    """세 높이 k+o (o in offs)가 모두 한 평평한 구간에 들어가는 k의 집합"""
    U = S.EmptySet
    for I in plates:
        J = Interval(-oo, oo)
        for o in offs:     # k+o 가 열린구간 I 안 ⇔ k 가 I 를 -o 만큼 옮긴 열린구간 안
            J = J.intersect(Interval.open(I.start - o, I.end - o))
        # 같은 결과를 부등식 풀이로도 확인
        if I.start != -oo and I.end != oo:
            J2 = Interval(-oo, oo)
            for o in offs:
                J2 = J2.intersect(sp.solve_univariate_inequality(kk + o > I.start, kk, relational=False)).intersect(
                    sp.solve_univariate_inequality(kk + o < I.end, kk, relational=False))
            assert J2 == J, (J2, J)
        U = U.union(J)
    return U
POS = Interval.open(0, oo)
A = POS - cont_set((0, 3, 6))      # t=0
B = POS - cont_set((6, 5, 4))      # t=15
C = POS - cont_set((4, 3, 2))      # t=17
assert A == Interval(9, 17) and B == Interval(9, 13) and C == Interval(11, 15), (A, B, C)
TWO = (A.intersect(B) - C).union(A.intersect(C) - B).union(B.intersect(C) - A)
assert TWO == Union(Interval.Ropen(9, 11), Interval.Lopen(13, 15)), TWO
assert TWO.sup == 15 and TWO.inf == 9 and TWO.contains(15) and TWO.contains(9)
print('기호: t=0 불연속 [9,17], t=15 [9,13], t=17 [11,15] → 개수 2인 k = [9,11) ∪ (13,15] OK')

# ===== 격자 전수: k in (0, 30], 경계 근방 포함 =====
kgrid = sorted(set([Fr(n, 8) for n in range(1, 241)] + [Fr(b) + d for b in (9, 11, 13, 15, 17) for d in (Fr(1, 1000), -Fr(1, 1000), 0)]))
N = {k: len(Nset(k)) for k in kgrid}
two = [k for k in kgrid if N[k] == 2]
assert all((9 <= k < 11) or (13 < k <= 15) for k in two) and all(N[k] == 2 for k in kgrid if (9 <= k < 11) or (13 < k <= 15))
assert max(two) == 15 and min(two) == 9 and N[Fr(15) + Fr(1, 1000)] == 1 and N[Fr(9) - Fr(1, 1000)] == 0
assert N[Fr(11)] == 3 and N[Fr(13)] == 3
# 경계의 판단: 높이가 15, 17에 닿을 때 고립값 g(15)=5, g(17)=3
assert [g(9), g(12), g(15)] == [6, 6, 5] and [g(19), g(18), g(17)] == [2, 2, 3]
# 경계값은 실제 방정식으로도 확인
for k, pts in ((R(9), [0, 15]), (R(15), [0, 17])):
    hh = lambda t: G_exact(G_exact(t) + k)
    D = [s for s in (0, 15, 17) if not (hh(s - R(1, 1000)) == hh(s) == hh(s + R(1, 1000)))]
    assert D == pts, (k, D)
ans_val = max(two) - min(two)
assert ans_val == 6
ch = [Fr(c) for c in P['choices']]
assert len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1 and ch == sorted(ch) and ch[1] - ch[0] == 1
assert P['ans'] == 5 and ch[P['ans'] - 1] == ans_val
print(f'격자 {len(kgrid)}개 전수: 개수 2인 k의 최댓값 15, 최솟값 9 (둘 다 포함) → 차 {ans_val}, 선지 ⑤, 오름차순 공차 1 OK')

# ===== 오답 근거 값 =====
two_noleft = [k for k in kgrid if len(Nset(k, noleft=True)) == 2]          # t<0 쪽 높이 k를 빠뜨림
assert max(two_noleft) == 14 and min(two_noleft) == 9 and max(two_noleft) - min(two_noleft) == 5
two_no0 = [k for k in kgrid if len(Nset(k, pts=(15, 17))) == 2]            # g의 t=0 불연속을 빠뜨림
assert max(two_no0) == 13 and min(two_no0) == 11 and max(two_no0) - min(two_no0) == 2
assert sorted(P['wrongs']) == ['2', '5'] and all(w in P['choices'] for w in P['wrongs'])
assert '④ \\(5\\)' in P['wrong'] and '① \\(2\\)' in P['wrong']
# 접점 고립값을 놓친 경우(g(15), g(17)을 양옆 값 하나로): 경계가 빠져 최댓값 또는 최솟값이 없음
gNoTan = lambda t: 4 if Fr(t) == 15 else (2 if Fr(t) == 17 else g(t))
gMult = lambda t: 6 if Fr(t) == 15 else (4 if Fr(t) == 17 else g(t))
assert len(Nset(Fr(15), gg=gNoTan)) == 1 and len(Nset(Fr(9), gg=gMult)) == 0
print('오답 근거: ④5(t<0 쪽 높이 누락 → 최댓값 14), ①2(t=0 누락 → [11,13]) 선지 안 OK')

# ===== 원문 원리 줄 불통 =====
# 원문 줄: 불연속점 = 성분 함수들의 불연속점을 합한 것 - 같은 모양 겹침. h=g(g(t)+k)에서 성분의 불연속점은 안쪽 g의 0,15,17뿐이고
# 상쇄할 둘째 함수가 없어 그 줄대로면 모든 k에서 불연속점이 3개 → '개수 2'를 만족시키는 k를 정하지 못함
pred = {k: 3 for k in kgrid}
assert {N[k] for k in kgrid} == {0, 1, 2, 3} and any(N[k] != pred[k] for k in kgrid)
# 원문 방식의 답(불연속점의 합)도 k에 따라 달라져 원문 값 36과 무관
assert sum(Nset(Fr(10))) == 15 and sum(Nset(Fr(14))) == 17 and sum(Nset(Fr(12))) == 32
print('원문 원리 줄 불통: 합집합-상쇄로는 늘 3개(0,15,17) → 실제 개수 0~3이 k에 따라 바뀜, 판정은 높이 세 값의 위치 OK')

# ===== 조건 빼 보기 =====
# '개수가 2' 빼기: k가 임의의 양수 → 최댓값 없음
# 조건이 없으면 모든 양수 k가 허용되므로 k의 최댓값이 없음(예: k=1000도 됨). 조건이 있으면 k>15에서 개수가 1 또는 0이라 제외
assert all(len(Nset(k)) in (0, 1) for k in kgrid if k > 15) and len(Nset(Fr(1000))) == 0
print('ABLATION 17 개수 2: 필요(빼면 k가 임의의 양수라 최댓값이 없음)')
# '양수' 빼기: k<0도 허용 → [-6,-4) ∪ (-4,-2] 추가, 최솟값 -6 → 차 21
kneg = sorted(set([Fr(n, 8) for n in range(-80, 241)] + [Fr(b) + d for b in (-6, -4, -2, 9, 11, 13, 15) for d in (Fr(1, 1000), -Fr(1, 1000), 0)]))
twoall = [k for k in kneg if len(Nset(k)) == 2]
assert min(twoall) == -6 and max(twoall) == 15 and max(twoall) - min(twoall) == 21
print('ABLATION 17 양수: 필요(빼면 k=-6까지 되어 차 21 → 답이 바뀜)')
# 절댓값 빼기: g를 곡선 y=f(x)와 직선 y=t의 교점 개수로 → 개수 2인 k는 [12,14], 차 2
def n_noabs(t):
    t = Fr(t)
    if t < -17: return 1
    if t == -17: return 2
    if t < 15: return 3
    if t == 15: return 2
    return 1
for t in (-20, -17, 0, 15, 16, R(-33, 2)):
    assert G_exact(t, absval=False) == n_noabs(t)
two_na = [k for k in kgrid if len(Nset(k, gg=n_noabs, pts=(-17, 15))) == 2]
assert min(two_na) == 12 and max(two_na) == 14 and max(two_na) - min(two_na) != 6
print('ABLATION 17 절댓값: 필요(빼면 개수 2인 k가 [12,14]이고 차 2 → 답이 바뀜)')
# 합성의 안쪽 '+k' 를 빼고 h=g(g(t)) 로 두면 k가 없어 물음이 성립하지 않음, 바깥 g를 빼고 h=g(t)+k 로 두면 늘 3개
for k in (Fr(1), Fr(9), Fr(15)):
    hk = lambda t: g(t) + k
    assert [s for s in (0, 15, 17) if not (hk(s - E) == hk(s) == hk(s + E))] == [0, 15, 17]
print('ABLATION 17 합성: 필요(바깥 g를 빼고 g(t)+k로 두면 모든 k에서 3개 → 개수 2가 되지 않음)')

# ===== 길이: 원문 이상, 원문 거리 =====
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', t))
L_new = len(plain(P['body'])); L_org = len(plain(F.I['M31'][0]))
assert L_new >= L_org, (L_new, L_org)
print(f'길이: 변형 {L_new}자 >= 원문 {L_org}자 OK')
print('ALL OK')
