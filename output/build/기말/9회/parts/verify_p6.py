# -*- coding: utf-8 -*-
# A18 (9회 18번 후보, 원문 M25, db_ref 'M25 킬러 설계A') 검증
# 원문 풀이(-40, ⑤) · 재교점 x좌표 s=a-2t(정의대로 인수분해) · 짝 조건 전수(a의 모든 실수해) · 갈래마다 b · '세 점'으로 가림 · 정답 유일
# · (a, b) 격자 전수(정의대로) · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, t, a, b, u = sp.symbols('x t a b u', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M25' and it['ans'] == 1 and it['db_ref'] == 'M25 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it                                                # 분담표: 상자 원문대로(원문 상자 없음)
full = it['body']
for s_ in (r'f(x)=-x^3+ax^2+b', r'\((1,\ f(1))\), \((4,\ f(4))\) 중 한 점에서 곡선 \(y=f(x)\)에 접하는 직선이 다른 한 점을 지나고',
           r'\(x\)축과 서로 다른 세 점에서 만난다', r'\(4\le t\le 5\)인 실수 \(t\)', r'\(\mathrm{P}\)가 아닌 점을 \(\mathrm{Q}\)',
           r'최댓값이 \(-14\)일 때', r'함수 \(h(t)\)의 최솟값은?'):
    assert s_ in full, s_
assert '개수' not in full and '합은' not in full and '오직' not in full and '이러한' not in full
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
CH = [sp.Integer(v) for v in it['choices']]
T0, T1, P1, P2, VMAX = 4, 5, 1, 4, -14

def f_of(av, bv): return -x**3 + av*x**2 + bv
def other_x(av, tv, bv=0):
    """정의대로: 점 (tv, f(tv))에서의 접선과 곡선의 교점 중 tv가 아닌 x (없으면 None)"""
    f = f_of(av, bv); l = sp.diff(f, x).subs(x, tv)*(x - tv) + f.subs(x, tv)
    r = [z for z in sp.solve(sp.expand(f - l), x) if sp.simplify(z - tv) != 0]
    return r[0] if r else None

# ---------- 원문 M25 ----------
fo = -x**3 + 6*x**2
po = [z for z in sp.solve(sp.diff(fo, x), x) if z > 0][0]
g = sp.expand(fo.subs(x, t) - t*sp.diff(fo, x).subs(x, t))
assert po == 4 and g == 2*t**3 - 6*t**2
cand = [-po/2, po/2] + [z for z in sp.solve(sp.diff(g, t), t) if -po/2 <= z <= po/2]
assert min(g.subs(t, z) for z in cand) == -40 and F.I['M25'][2] == '⑤' and F.I['M25'][1][4] == '-40'
print('원문 M25: p=4, g(t)=2t^3-6t^2, [-2,2] 최솟값 -40 = ⑤ OK')

# ---------- 재교점: s = a - 2t (정의대로) ----------
fa = f_of(a, b); la = sp.diff(fa, x).subs(x, t)*(x - t) + fa.subs(x, t)
assert sp.expand(fa - la + (x - t)**2*(x - (a - 2*t))) == 0
for av in (6, 9):
    for tv in (4, R(9, 2), 5):
        assert other_x(av, tv) == av - 2*tv
    assert not (T0 <= R(av, 3) <= T1)        # 변곡점(Q 없음)이 구간 밖
print('재교점 x좌표 s=a-2t, h(t)=f(a-2t) · 두 갈래 모두 변곡점이 4≤t≤5 밖 OK')

# ---------- 짝 조건 전수 ----------
def tangent_passes(av, p, q):   # 점 (p, f(p))에서의 접선이 점 (q, f(q))를 지남 (b는 소거)
    f = f_of(av, 0); return sp.expand(f.subs(x, q) - (sp.diff(f, x).subs(x, p)*(q - p) + f.subs(x, p)))
sols = set()
for p, q in ((P1, P2), (P2, P1)):
    for z in sp.solve(tangent_passes(a, p, q), a):
        assert z.is_real; sols.add(z)
assert sols == {6, 9}, sols
print('짝 조건: (1→4) a=6, (4→1) a=9 두 갈래 OK')

# ---------- 갈래마다 b, '세 점'으로 가림 ----------
def h_expr(av, bv): return f_of(av, bv).subs(x, av - 2*t)
def ext(av, bv):
    hh = h_expr(av, bv); cs = [T0, T1] + [z for z in sp.solve(sp.diff(hh, t), t) if z.is_real and T0 < z < T1]
    v = [hh.subs(t, z) for z in cs]; return max(v), min(v)
def three_roots(av, bv):
    rr = sp.Poly(f_of(av, bv), x).real_roots(); return len(set(rr)) == 3
table = {}
for av in sorted(sols):
    M0, _ = ext(av, 0); bv = VMAX - M0
    assert ext(av, bv)[0] == VMAX
    table[av] = (bv, ext(av, bv)[1], three_roots(av, bv))
assert table[6] == (-174, -142, False) and table[9] == (-24, -24, True), table
assert f_of(6, -174).subs(x, 4) == -142 and f_of(6, -174).subs(x, -2) == f_of(6, -174).subs(x, 4)
assert f_of(9, -24).subs(x, 0) == -24 and f_of(9, -24).subs(x, 6) == 84
assert table[6][0] < 0 and table[9][0] < 0      # 극솟값(b) 부호만으로는 가려지지 않음
print('갈래별 (b, 최솟값, x축과 세 점):', table)
ok = [av for av, v in table.items() if v[2]]
assert ok == [9]
ans = table[9][1]
print('정답 유일: 세 점 조건을 만족하는 갈래는 a=9 하나 OK')

# 정의대로 격자 전수: a = -10..20 (1/4 간격), b는 최댓값 조건에서, Q는 접선 교점으로 직접
hits = []
for i in range(-40, 81):
    av = R(i, 4)
    if not any(tangent_passes(av, p, q) == 0 for p, q in ((P1, P2), (P2, P1))): continue
    if T0 <= av/3 <= T1: continue
    hs = [f_of(av, 0).subs(x, other_x(av, tv)) for tv in [T0 + R(k, 40) for k in range(41)]]
    M0 = max(max(hs), ext(av, 0)[0]); bv = VMAX - M0
    if three_roots(av, bv): hits.append((av, ext(av, bv)[1]))
assert hits == [(9, -24)], hits
print('전수: a=-10..20 (1/4 간격) 중 모든 조건을 만족하는 경우는 a=9, 최솟값 -24 하나 OK')

# ---------- 정답 · 선지 · 오답 ----------
assert ans == -24 and CH[it['ans'] - 1] == ans
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {2}
# -22: a=9, 최댓값을 f(1)=8+b로 → b=-22, 최솟값 f(0)
w1 = f_of(9, VMAX - f_of(9, 0).subs(x, 1)).subs(x, 0)
# -18: s=a-t로 잘못 → 두 짝 모두 a=5, s∈[0,1], 최댓값 f(1)
aw = set(sp.solve(sp.Eq(a - P1, P2), a)) | set(sp.solve(sp.Eq(a - P2, P1), a)); assert aw == {5}
fw = f_of(5, 0); sw = [5 - T1, 5 - T0]
cw = sw + [z for z in sp.solve(sp.diff(fw, x), x) if sw[0] < z < sw[1]]
bw = VMAX - max(fw.subs(x, z) for z in cw); w2 = min(fw.subs(x, z) for z in cw) + bw
assert three_roots(5, bw)
# -16: a=9, b=-24에서 최솟값을 끝값만 비교
w3 = min(f_of(9, -24).subs(x, z) for z in (-1, 1))
assert [w1, w2, w3] == [sp.Integer(v) for v in it['wrongs']] == [-22, -18, -16]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert ans != -40
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+', ' ', full))}
assert ans not in nums and -ans not in nums, nums
print('정답이 본문의 어떤 수(부호 포함)·원문 답과도 같지 않음 OK')
print('정답 = ①, 선지 등차(공차 2, 오름차순), 오답 -22(끝점 오독)·-18(s=a-t)·-16(극소 누락) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
print(f"ABLATION 18 x축과 세 점: 필요(정해지지 않음: 빼면 두 갈래가 모두 남아 답이 {sorted(v[1] for v in table.values())})")
alt = {}
for av in (3, 4, 5, 7, 8, 10):
    if T0 <= R(av, 3) <= T1: continue
    bv = VMAX - ext(av, 0)[0]
    if three_roots(av, bv): alt[av] = ext(av, bv)[1]
assert len(set(alt.values())) >= 2
print(f'ABLATION 18 짝 조건: 필요(정해지지 않음: 빼면 a={sorted(alt)} 에서도 나머지 조건이 성립, 답이 {len(set(alt.values()))}가지 이상)')
alt = {bv: ext(9, bv)[1] for bv in (-10, -24, -50) if three_roots(9, bv)} | {}
alt6 = [bv for bv in (-5, -10, -20) if three_roots(6, bv)]
assert len(set(alt.values())) == 3 and alt6
print(f'ABLATION 18 최댓값 -14: 필요(정해지지 않음: 빼면 a=9에서 b=-10,-24,-50 모두 세 점, 답 {sorted(alt.values())} 등, a=6도 b={alt6}에서 성립)')
# 구간을 원문 [-p/2, p/2]로 되돌리면 a=9의 p/2=3, a=6의 p/2=2 가 변곡점이라 Q가 없음
assert other_x(9, 3) is None and other_x(6, 2) is None
assert sp.limit(h_expr(9, -24), t, sp.oo) == sp.oo and sp.limit(h_expr(6, -174), t, sp.oo) == sp.oo
print('ABLATION 18 4≤t≤5: 필요(구간 없이는 h의 최댓값이 없고, 원문 구간 [-p/2,p/2]이면 끝점이 변곡점이라 Q가 없음)')

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
gy = sp.expand(f_of(9, -24).subs(x, t) - t*sp.diff(f_of(9, -24), x).subs(x, t))   # y절편 식
hy = sp.expand(h_expr(9, -24))
assert sp.simplify(gy - hy) != 0
assert hy == sp.expand(2*t*(2*t - 9)**2 - 24)
print('원문 설정 줄(y절편 f(t)-tf\'(t)): 변형의 h(t)=f(a-2t)와 다름(불통) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M25'][0])); Lm = len(plain(it['body']))
assert Lm >= 0.9 * Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body']))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M25'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
print('ALL OK')
