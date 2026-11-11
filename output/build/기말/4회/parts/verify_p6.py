# -*- coding: utf-8 -*-
# A18 (4회 18번 후보, 원문 M28, db_ref 'M28 킬러 설계A') 검증
# 원문 풀이(13/2) · 판정 원리(A = 곡선의 실근 ∪ 접선의 x절편) · 일반식 g(r) = -(t-r)^2 h'(t) · 정의대로 센 t의 집합(종결식)
# · 실근 r로 매개화한 전수(세 갈래) · a 격자 전수 · 정답 = ③ · 선지 등차 · 오답(선지 안) · 조건 빼 보기 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, t, a, r, q = sp.symbols('x t a r q', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M28' and it['ans'] == 3 and it['db_ref'] == 'M28 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert not it.get('cond') and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'x^3-3x^2+ax-5a+22' in it['body'] and 'f(x)g(x)=0' in it['body'] and r'\(S=2\)' in it['body'] and r'\(f(2)\)' in it['body']
assert set(it['ops']) >= {'OP51', 'OP28', 'OP33'} and 'fig_18' not in it['body']
CH = [sp.nsimplify(v) for v in it['choices']]
S_GIVEN = 2
fam = x**3 - 3*x**2 + a*x - 5*a + 22           # 변형 함수
ask = lambda av: fam.subs({a: av, x: 2})       # 묻는 값 f(2)

def iszero(e):
    """정확히 0인지: 유리수는 그대로, 무리수(근호·CRootOf)는 60자리 수치로 판정"""
    e = sp.sympify(e)
    if e.is_Rational: return e == 0
    return abs(sp.N(e, 60)) < sp.Float('1e-40')

def n_elem(f_, tv):
    """집합 A={x | f(x)g(x)=0}의 원소의 개수 (g: x=tv에서의 접선). g가 0이면 무한(oo).
    A = (f의 서로 다른 실근) ∪ (g의 실근)을 그대로 센다"""
    m_, c_ = sp.diff(f_, x).subs(x, tv), f_.subs(x, tv)
    Zf = set(sp.real_roots(sp.Poly(f_, x)))
    if iszero(m_):
        return sp.oo if iszero(c_) else len(Zf)
    x0 = tv - c_/m_                                   # 접선의 x절편
    return len(Zf) + (0 if any(iszero(x0 - z) for z in Zf) else 1)

def T_def(f_):
    """정의대로: 원소의 개수가 1인 실수 t 전부.
    후보는 f'(t)=0인 t와, f와 접선이 공통근을 갖는 t(x에 대한 종결식 = 0)뿐이다.
    (그 밖의 t에서는 접선의 x절편이 f의 근이 아니어서 원소가 (f의 실근 수)+1 ≥ 2)"""
    fp_ = sp.diff(f_, x)
    g_ = fp_.subs(x, t)*(x - t) + f_.subs(x, t)
    res = sp.Poly(sp.resultant(f_, g_, x), t)
    cand = set(sp.real_roots(sp.Poly(fp_.subs(x, t), t))) | set(sp.real_roots(res))
    return sorted(c for c in cand if n_elem(f_, c) == 1)

# ---------- 원문 M28 ----------
fo = x**3 - 6*x**2 + 9*x + 16
assert sp.factor(fo) == (x + 1)*(x**2 - 7*x + 16) and sp.real_roots(fo) == [-1]
To = T_def(fo)
assert To == [-1, 1, 3, R(7, 2)] and sum(To) == R(13, 2) and F.I['M28'][2] == '②' and F.I['M28'][1][1] == r'\dfrac{13}{2}'
print('원문 M28: 원소 1개인 t = -1, 1, 3, 7/2, 합 13/2 = ② OK')

# ---------- 판정 원리 · 일반식 ----------
# f=(x-r)h(x), h=x^2+(r-3)x+q (이차항 계수 -3) → 접선이 (r,0)을 지남 ⇔ -(t-r)^2 h'(t)=0 ⇔ t=r 또는 t=(3-r)/2
h = x**2 + (r - 3)*x + q
fg = sp.expand((x - r)*h)
assert sp.Poly(fg, x).all_coeffs()[1] == -3
gr = sp.expand(fg.subs(x, t) + (r - t)*sp.diff(fg, x).subs(x, t))
assert sp.expand(gr - (-(t - r)**2*sp.diff(h, x).subs(x, t))) == 0
assert sp.solve(sp.diff(h, x).subs(x, t), t) == [(3 - r)/2]
assert sp.expand(sp.diff(fg, x).subs(x, r) - h.subs(x, r)) == 0                                   # f'(r)=h(r)
assert sp.expand(sp.diff(fg, x).subs(x, (3 - r)/2) - h.subs(x, (3 - r)/2)) == 0                  # f'((3-r)/2)=h((3-r)/2)
print("원리: g(r) = f(t)+(r-t)f'(t) = -(t-r)^2 h'(t) → t=r, (3-r)/2 (r=1이면 겹침), 두 점에서 f'=h>0")

# ---------- 실근 r로 매개화한 전수 ----------
# f(5)=72≠0이므로 r≠5, a는 r로 하나로 정해짐
assert fam.subs(x, 5) == 72
a_of = sp.simplify(sp.solve(fam.subs(x, r), a)[0])                       # a = -(r^3-3r^2+22)/(r-5)
hq = sp.div(sp.Poly(fam.subs(a, a_of)*(r - 5), x), sp.Poly(x - r, x))    # (r-5)f = (x-r)*몫
assert hq[1] == 0
fp = sp.diff(fam, x); Dp = sp.discriminant(fp, x)                         # 36-12a
assert sp.expand(Dp - (36 - 12*a)) == 0
def ncrit(av): return 2 if av < 3 else (1 if av == 3 else 0)
def one_root(av):
    return len(set(sp.real_roots(sp.Poly(fam.subs(a, av), x)))) == 1
cands = {}
for n in (2, 1, 0):                         # 수평접선 n개인 갈래: r≠1이면 S = n + (r+3)/2
    rv = sp.solve(sp.Eq(n + (r + 3)/2, S_GIVEN), r)[0]
    av = a_of.subs(r, rv)
    cands[n] = (rv, av)
assert cands == {2: (-3, -4), 1: (-1, 3), 0: (1, 5)}, cands
valid = []
for n, (rv, av) in cands.items():
    f_ = fam.subs(a, av)
    ok_branch = ncrit(av) == n
    ok_root = one_root(av)
    Td = T_def(f_)
    ok = ok_branch and ok_root and rv != 1
    print(f'  수평접선 {n}개 갈래: r={rv}, a={av}, 갈래 맞음={ok_branch}, 실근 하나={ok_root}, 정의대로 t={[str(v) for v in Td]}, S={sum(Td)} → {"해" if ok else "버림"}')
    assert (sp.simplify(sum(Td) - S_GIVEN) == 0) == ok
    if ok: valid.append(av)
# r=1인 경우(두 접점이 겹침): S = n+1 = 2이려면 n=1(a=3)이어야 하는데 r=1이면 a=5
assert a_of.subs(r, 1) == 5 and ncrit(5) == 0 and T_def(fam.subs(a, 5)) == [1]
assert sorted(valid) == [-4, 3]
assert sp.factor(fam.subs(a, -4)) == (x + 3)*(x**2 - 6*x + 14) and sp.discriminant(x**2 - 6*x + 14, x) < 0
assert sp.expand(fam.subs(a, 3) - ((x - 1)**3 + 8)) == 0 and T_def(fam.subs(a, 3)) == [-1, 1, 2]
T4 = T_def(fam.subs(a, -4))
assert len(T4) == 4 and set(T4) >= {-3, 3} and sp.simplify(sum(T4)) == 2
assert sp.factor(fam.subs(a, 5)) == (x - 1)*(x**2 - 2*x + 3)
print('전수(실근 r 매개화): a<3 → r=-3, a=-4 (x^2-6x+14>0) 해 / a=3 → r=-1 해 / a>3 → r=1, a=5는 두 접점이 t=1로 겹쳐 S=1, 버림')

# ---------- a 격자 전수 (정의대로 센 S) ----------
def S_formula(av):
    f_ = fam.subs(a, av)
    rs = set(sp.real_roots(sp.Poly(f_, x)))
    if len(rs) != 1: return None
    rv = list(rs)[0]; n = ncrit(av)
    return n + (1 if rv == 1 else (rv + 3)/2)
grid = [R(n, 2) for n in range(-40, 41)] + [sp.Integer(v) for v in (-120, -110, -109, -108, 30, 100)]
hit = []; none = 0
for av in grid:
    Td = T_def(fam.subs(a, av)); Sf = S_formula(av)
    if not Td:
        none += 1; assert Sf is None, av
        continue
    assert Sf is not None and abs(sp.N(sum(Td) - Sf, 30)) < 1e-20, (av, Td, Sf)
    if iszero(sum(Td) - S_GIVEN): hit.append(av)
assert hit == [-4, 3], hit
assert none == 3 and fam.subs({a: 5, x: 1}) == 0 and sp.expand(fam.subs(x, 1) - (20 - 4*a)) == 0
print(f'격자 {len(grid)}개 a(-20~20 간격 1/2, 그리고 -120, -110, -109, -108, 30, 100): 정의대로 센 S와 식이 모두 같고, S=2는 a=-4, 3뿐 (실근이 셋이라 t가 없는 a {none}개: -120, -110, -109)')
# 갈래마다 S는 r에 대한 일차식이고 a↔r이 일대일이므로 갈래마다 해는 하나뿐
# 경계: 실근이 하나가 아닌 a (극값이 0 또는 부호가 다름)
aD = sp.Poly(sp.discriminant(fam, x), a)
print('  실근이 둘 이상인 a 구간의 끝(판별식=0):', [str(sp.N(v, 6)) for v in sp.real_roots(aD)])

ans = sum(ask(av) for av in valid)
assert sp.expand(fam.subs(x, 2) - (18 - 3*a)) == 0
assert [ask(av) for av in sorted(valid)] == [30, 9] and ans == 39 and CH[it['ans'] - 1] == ans
print(f'정답: f(2)=18-3a → 30 + 9 = {ans} = ③')

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {3}
print('선지', [str(v) for v in CH], '공차 3 (오름차순), 정답 ③')

# ---------- 오답 (선지 안) ----------
w42 = ans + ask(5)                    # a=5(두 접점 겹침)를 버리지 않음
w33 = ask(-4) + ask(5)                # a=3(수평접선 하나)을 놓치고 a=5를 넣음
w30 = ask(-4)                         # 수평접선 두 개인 경우만 (선지 밖)
w9 = ask(3)                           # a=3만 (선지 밖)
assert (w42, w33, w30, w9) == (42, 33, 30, 9) and w30 not in CH and w9 not in CH
assert it['wrongs'] == ['42', '33'] and all(sp.nsimplify(w) in CH for w in it['wrongs'])
flat = it['wrong'].replace(r'\(', '').replace(r'\)', '').replace(' ', '')
for s_ in ('30+9+3=42', '30+3=33', 'a=5'):
    assert s_ in flat, s_
print('오답 (선지 안): 42 (a=5의 두 접점 겹침을 놓침), 33 (a=3을 놓치고 a=5 포함) / 수평접선 두 개인 경우만 30, a=3만 9는 선지 밖')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
alt = {av: (S_formula(av), ask(av)) for av in (-6, -5, 4, 6, 10)}
assert all(v[0] is not None for v in alt.values()) and len({v[1] for v in alt.values()}) == 5
print(f'ABLATION 18 S=2: 필요(정해지지 않음: a=-6,-5,4,6,10도 원소 1개인 t가 있고 f(2)={[str(v[1]) for v in alt.values()]} 등)')
alt2 = {}
for sv in (1, 3, R(5, 2)):
    vs = []
    for n in (2, 1, 0):
        rv = sp.solve(sp.Eq(n + (r + 3)/2, sv), r)[0]
        if rv == 5: continue
        av = a_of.subs(r, rv)
        Td = T_def(fam.subs(a, av))
        if Td and sp.simplify(sum(Td) - sv) == 0: vs.append(av)
    if sv == 1 and 5 not in vs and sp.simplify(sum(T_def(fam.subs(a, 5))) - 1) == 0: vs.append(sp.Integer(5))
    alt2[sv] = sum(ask(av) for av in vs)
assert all(v != ans for v in alt2.values()), alt2
print(f'ABLATION 18 합의 값 2: 필요(답 바뀜: S=1, 3, 5/2이면 f(2)의 합이 {[str(v) for v in alt2.values()]})')
# 원소의 개수 1 → 2: 실근이 하나인 f에서 거의 모든 t가 원소 2개라 합이 정해지지 않음
f3 = fam.subs(a, 3)
assert all(n_elem(f3, tv) == 2 for tv in (0, 3, 5, -2, R(1, 2), 10))
print('ABLATION 18 원소의 개수 1: 필요(정해지지 않음: 개수 조건을 2로 바꾸면 a=3에서 t=0, 3, 5, -2, 1/2, 10 등 무수히 많은 t가 맞아 합 S가 없음)')
# 접선 → 접점에서의 함숫값만(수평선 y=f(t))으로 바꾸면 A = f의 실근 ∪ ∅ 또는 전체라 t가 무수히 많음
assert len(set(sp.real_roots(sp.Poly(f3, x)))) == 1 and len(set(sp.real_roots(sp.Poly(fam.subs(a, -4), x)))) == 1
print('ABLATION 18 접선 y=g(x): 필요(정해지지 않음: g가 없으면 A는 f(x)=0의 실근뿐이라 a=3, -4 등에서 모든 t가 맞아 합 S가 없음)')
only2, only1 = ask(-4), ask(3)
assert only2 != ans and only1 != ans and ans + ask(5) != ans
print(f'ABLATION 18 갈래: 필요(a<3 갈래만 → {only2}, a=3 갈래만 → {only1}, a>3 갈래의 a=5를 넣으면 {ans + ask(5)}, 세 갈래를 모두 가려야 {ans})')
# 상수항 -5a+22 (매개변수 자리): 상수항이 a와 무관한 22이면 다른 답
fam2 = x**3 - 3*x**2 + a*x + 22
a2 = sp.solve(fam2.subs(x, r), a)[0]
vs2 = []
for n in (2, 1, 0):
    rv = sp.solve(sp.Eq(n + (r + 3)/2, S_GIVEN), r)[0]
    av = sp.nsimplify(a2.subs(r, rv)); Td = T_def(fam2.subs(a, av))
    if Td and sp.simplify(sum(Td) - S_GIVEN) == 0: vs2.append(av)
alt3 = sum(fam2.subs({a: av, x: 2}) for av in vs2)
assert alt3 != ans and vs2 == []
print('ABLATION 18 상수항 -5a+22: 필요(답 바뀜: 상수항이 a와 무관한 22이면 세 갈래 후보가 모두 맞지 않아 S=2인 a가 없음)')

# ---------- 문장 길이 ----------
L = lambda h_: len(re.sub(r'\s', '', html.unescape(re.sub(r'</?(div|img|br|span|u|b)\b[^>]*>', '', h_))))
Lo = L(F.I['M28'][0]); Lm = L(it['body'])
assert Lo == 121 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body']))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M28'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
assert jd <= 0.25, jd
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하)')
assert '\\[' not in it['body'] and '(단,' not in it['body']
print('ALL OK')
