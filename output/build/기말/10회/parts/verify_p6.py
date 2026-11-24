# -*- coding: utf-8 -*-
# A18 (10회 18번 후보, 원문 M34, db_ref 'M34 킬러 설계A') 검증
# 원문 풀이(-5/16, ③) · 단순근 판정(정의대로: 한쪽 미분계수) · h(t)=1 ⇔ 정류 변곡점 높이(근 중복도 전수)
# · 조건 (가)(나)(다) 전수(일반 사차식 x^4+ax^3+bx^2+d, f'(0)=0) · 갈래마다 상수 · (다)로 가림 · 정답 유일
# · (a, b) 격자 전수(정의대로 h 계산) · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문 골격
import os, re, sys, html, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, t, a, b, c, p, q, d = sp.symbols('x t a b c p q d', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M34' and it['ans'] == 3 and it['db_ref'] == 'M34 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert [k for k, _ in it['cond']] == ['가', '나', '다']                # 분담표: 상자 원문대로
full = it['body'] + COND(it['cond'])
for s_ in (r'최고차항의 계수가 \(1\)인 사차함수 \(f(x)\)', r'\(f(1)\)의 값은?', r'\(|f(x)-f(t)|\)가 미분가능하지 않은 실수 \(x\)의 개수를 \(h(t)\)',
           r'\(h(t)=1\)을 만족시키는 모든 실수 \(t\)의 값의 합은 \(1\)', r"점 \((0,\ f(0))\)에서의 접선의 기울기는 \(0\)이고, \(f(-1)=5\)", r'모든 실수 \(x\)에 대하여 부등식 \(f(x)&gt;0\)이 성립한다'):
    assert s_ in full, s_
assert '오직' not in full and '이러한' not in full and '이와 같은' not in full
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for _, cc in it['cond']: assert not re.search(r'\\\([^)]*?[<>]', cc)
CH = [sp.Integer(v) for v in it['choices']]
SUM, J, V, ASK = 1, -1, 5, 1

# ---------- 정의대로: |g|가 미분가능하지 않은 점 = g(x0)=0, g'(x0)≠0 (좌우 미분계수 -|g'|, |g'|) ----------
def nondiff_pts(g):
    g = sp.Poly(sp.expand(g), x); out = []
    for r in set(g.real_roots()):
        if g.diff(x).eval(r) != 0: out.append(r)
    return out
def nondiff_pts_def(g, x0):   # 한쪽 미분계수로 직접 (검산용)
    G = sp.Abs(g); h_ = sp.symbols('h_', positive=True)
    L = sp.limit((G.subs(x, x0 - h_) - G.subs(x, x0)) / (-h_), h_, 0)
    Rr = sp.limit((G.subs(x, x0 + h_) - G.subs(x, x0)) / h_, h_, 0)
    return sp.simplify(L - Rr) != 0
# 중복도별: 한 번 곱해진 근만 미분불가
for m in (1, 2, 3):
    assert nondiff_pts_def((x - 2)**m * (x + 5), 2) == (m == 1)
print('정의: |g|는 한 번만 곱해진 근에서만 미분가능하지 않음(중복도 2·3은 미분가능) OK')

# ---------- 원문 M34 ----------
al = sp.symbols('al')
fo = (x - 1)**3*(x - al)
alv = sp.solve(sp.diff(fo, x).subs(x, R(-1, 2)) , al)
alv = [z for z in alv if z != R(-1, 2) and z != 1][0]
fo = sp.expand((x - 1)**3*(x - alv)); C0 = -fo.subs(x, R(-1, 2)); fo = fo + C0
assert alv == -1 and C0 == R(27, 16) and fo.subs(x, R(-1, 2)) == 0
assert nondiff_pts(fo - fo.subs(x, 1)) == [-1]
# f(f(x))=t: u=f(x)≥0, f는 u≥0에서 증가 → g(t)는 t=f(0)에서만 바뀜(0, 1, 2)
import numpy as np
FO = [float(z) for z in sp.Poly(fo, x).all_coeffs()]
def nreal(cf, tv):   # 서로 다른 실근 개수(수치, 겹근은 묶음)
    r = sorted(z.real for z in np.roots(cf[:-1] + [cf[-1] - tv]) if abs(z.imag) < 1e-6)
    return len([z for i, z in enumerate(r) if i == 0 or z - r[i - 1] > 1e-4])
def g_orig(tv):
    tv = float(tv); cf = FO[:-1] + [FO[-1] - tv]
    us = sorted(z.real for z in np.roots(cf) if abs(z.imag) < 1e-6 and z.real >= -1e-9)
    us = [z for i, z in enumerate(us) if i == 0 or z - us[i - 1] > 1e-4]
    return sum(nreal(FO, u) for u in us)
beta = fo.subs(x, 0)
assert [g_orig(beta - R(1, 100)), g_orig(beta), g_orig(beta + R(1, 100)), g_orig(5)] == [0, 1, 2, 2]
assert alv + beta == R(-5, 16) and F.I['M34'][2] == '③' and F.I['M34'][1][2] == r'-\dfrac{5}{16}'
print('원문 M34: α=-1, f(1)=27/16, β=f(0)=11/16, α+β=-5/16 = ③ OK')

# ---------- h(t)=1 ⇔ 정류 변곡점 높이 (사차식 근 중복도 전수) ----------
# 최고차항 1인 사차식의 실근 중복도 배열(합 4 또는 2·0 + 허근쌍) 중 '한 번 곱해진 근'이 정확히 1개인 것은 (3,1)뿐
pats = []
for k in range(0, 5):
    for comb in itertools.combinations_with_replacement([1, 2, 3, 4], k):
        if sum(comb) in (4, 2, 0) and sum(comb) <= 4 and (4 - sum(comb)) % 2 == 0:
            pats.append(tuple(sorted(comb)))
ones = sorted({pt for pt in pats if pt.count(1) == 1})
assert ones == [(1, 3)], ones
print('한 번 곱해진 실근이 1개인 사차식은 (x-p)^3(x-q) 꼴뿐 → h(t)=1이면 f(t)는 정류 변곡점 높이 OK')

def hval(f, tv):
    return len(nondiff_pts(f - f.subs(x, tv)))
def h1_set(f):
    """h(t)=1인 t 전체: f(t)가 임계값이 아니면 근이 모두 한 번 곱해져 h는 짝수 → 임계값 높이만 조사"""
    out = set()
    for xc in set(sp.Poly(sp.diff(f, x), x).real_roots()):
        L = f.subs(x, xc); g = f - L
        if len(nondiff_pts(g)) == 1:
            out |= set(sp.Poly(g, x).real_roots())
    return out

# ---------- 전수: f = x^4 + a x^3 + b x^2 + d (f'(0)=0), (가)(나)(다) ----------
f_gen = x**4 + a*x**3 + b*x**2 + d
assert sp.diff(f_gen, x).subs(x, 0) == 0
# 정류 변곡점 p: f'=4x(x^2 + 3a/4 x + b/2)가 이중근 p를 가짐 → (A) p=0: b=0  (B) p≠0: 4x^2+3ax+2b=4(x-p)^2
cands = []
# (A) b=0: f-f(0)=x^3(x+a), q=-a (a≠0), 합 0+q=1
for av in sp.solve(sp.Eq(0 + (-a), SUM), a):
    cands.append(dict(a=av, b=0))
# (B) 4x^2+3ax+2b = 4(x-p)^2 → a=-8p/3, b=2p^2; f-f(p)=(x-p)^3(x-q)에서 x^3 계수 비교 q=-p/3, 합 p+q=1
pv = sp.solve(sp.Eq(p + (-p/3), SUM), p)
for pp in pv:
    assert pp != 0
    fp = x**4 + (-R(8, 3)*pp)*x**3 + 2*pp**2*x**2
    assert sp.expand(fp - fp.subs(x, pp) - (x - pp)**3*(x + pp/3)) == 0
    cands.append(dict(a=-R(8, 3)*pp, b=2*pp**2))
table = []
for cd in cands:
    f0 = f_gen.subs({a: cd['a'], b: cd['b']})
    dv = sp.solve(sp.Eq(f0.subs(x, J), V), d)[0]
    f = sp.expand(f0.subs(d, dv))
    S = h1_set(f); assert len(S) == 2 and sum(S) == SUM, S
    assert sp.diff(f, x).subs(x, 0) == 0 and f.subs(x, J) == V
    xs = set(sp.Poly(sp.diff(f, x), x).real_roots()); mn = min(f.subs(x, z) for z in xs)
    table.append((f, mn, mn > 0, f.subs(x, ASK)))
assert len(table) == 2
fI, fII = table[0][0], table[1][0]
assert sp.expand(fI - (x**3*(x - 1) + 3)) == 0
assert sp.expand(fII - ((x - R(3, 2))**3*(x + R(1, 2)) - R(45, 16))) == 0
assert table[0][1] == 3 - R(27, 256) and table[1][1] == R(-9, 2)
assert [r[2] for r in table] == [True, False]
print('갈래 (i) p=0: f=x^3(x-1)+3, 최솟값 3-27/256>0 ✓ / (ii) p=3/2: f=(x-3/2)^3(x+1/2)-45/16, 최솟값 -9/2 ✗')
ok = [r for r in table if r[2]]
assert len(ok) == 1
ans = ok[0][3]
# 정류 변곡점 갈래에서 0은 극값이 아님(OP32), 극소점 갈래에서 0은 극소
assert sp.diff(fI, x, 2).subs(x, 0) == 0 and hval(fI, 0) == 1 and hval(fII, 0) == 0
print('정답 유일: (다)를 만족시키는 갈래는 p=0 하나 OK')

# 정의대로 격자 전수: a, b ∈ [-6, 6] (1/6 간격), d는 f(-1)=5에서, h(t)=1인 t를 직접 구해 합 1, (다)
hits = []
for i in range(-36, 37):
    for k in range(-36, 37):
        av, bv = R(i, 6), R(k, 6)
        fp = sp.Poly(4*x**2 + 3*av*x + 2*bv, x)
        if bv != 0 and sp.discriminant(fp) != 0: continue      # 이중근(정류 변곡점) 없으면 h=1 없음
        f0 = x**4 + av*x**3 + bv*x**2
        f = sp.expand(f0 + V - f0.subs(x, J))
        S = h1_set(f)
        if not S or sum(S) != SUM: continue
        xs = set(sp.Poly(sp.diff(f, x), x).real_roots())
        if min(f.subs(x, z) for z in xs) > 0: hits.append((av, bv, f.subs(x, ASK)))
assert hits == [(-1, 0, 3)], hits
print('전수: a,b ∈ [-6,6] (1/6 간격) 중 (가)(나)(다)를 만족시키는 경우는 f=x^4-x^3+3 하나 OK')

# ---------- 정답 · 선지 · 오답 ----------
assert ans == 3 and CH[it['ans'] - 1] == ans
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {3}     # 오름차순
w1 = table[1][3]                                         # (다) 확인 없이 극소점 갈래만
fsw = (x - 1)**3*x; fsw = fsw + V - fsw.subs(x, J)       # 원문 습관: x=1을 삼중근으로
assert sp.diff(fsw, x).subs(x, 0) != 0 and fsw.subs(x, ASK) == w1
w2 = (x**3*(x - 1)).subs(x, ASK)                         # f(x)-f(0)=x^3(x-1)과 f를 섞음
assert [w1, w2] == [sp.Integer(v) for v in it['wrongs']] == [-3, 0]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert ans != alv + beta
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+|&[a-z]+;', ' ', full))}
assert ans not in nums and -ans not in nums, nums
print('정답이 본문의 어떤 수(부호 포함)·원문 답과도 같지 않음 OK')
print('정답 = ③, 선지 등차(공차 3, 오름차순), 오답 -3(버려지는 갈래·원문 습관)·0(f-f(0)과 f 혼동) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
print(f"ABLATION 18 (다) f(x)>0: 필요(정해지지 않음: 빼면 두 갈래가 모두 남아 답이 {sorted(r[3] for r in table)})")
alt = set()
for qv in (R(1, 2), 2, 3, -1):      # 합 조건 없이 p=0 갈래: f=x^3(x-q)+c, f(-1)=5
    f = x**3*(x - qv); f = sp.expand(f + V - f.subs(x, J))
    xs = set(sp.Poly(sp.diff(f, x), x).real_roots())
    if min(f.subs(x, z) for z in xs) > 0: alt.add(f.subs(x, ASK))
assert len(alt) >= 3
print(f'ABLATION 18 합 1: 필요(정해지지 않음: 빼면 q=1/2,2,3,-1 에서도 성립, 답 {sorted(alt)} 등)')
alt = set()
for pv_ in (R(1, 4), R(1, 3), R(3)):  # f'(0)=0 없이 p+q=1
    qv = 1 - pv_; f = (x - pv_)**3*(x - qv); f = sp.expand(f + V - f.subs(x, J))
    xs = set(sp.Poly(sp.diff(f, x), x).real_roots())
    if min(f.subs(x, z) for z in xs) > 0: alt.add(f.subs(x, ASK))
assert len(alt) >= 2
print(f"ABLATION 18 f'(0)=0: 필요(정해지지 않음: 빼면 p=1/4,1/3,3 등에서 성립, 답 {sorted(alt)})")
alt = {(x**3*(x - 1) + cv).subs(x, ASK) for cv in (1, 3, 10)}
assert len(alt) == 3
print(f'ABLATION 18 f(-1)=5: 필요(정해지지 않음: 빼면 c>27/256인 모든 c에서 성립, 답 {sorted(alt)} 등)')

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
# 원문 줄: f(x)-f(1)=(x-1)^3(x-α). 정답 함수에서 f(x)-f(1)=x^3(x-1) → x=1은 한 번만 곱해진 근(삼중근 아님)
g1 = sp.factor_list(sp.expand(fI - fI.subs(x, 1)))
mult1 = [m for fac, m in g1[1] if sp.expand(fac - (x - 1)) == 0][0]
assert mult1 == 1
print('원문 설정 줄((x-1)^3 인수): 정답 함수에서 x=1은 한 번만 곱해진 근(불통) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M34'][0])); Lm = len(plain(full))
assert Lm >= 0.9 * Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(full))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M34'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
print('ALL OK')
