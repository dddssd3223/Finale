# -*- coding: utf-8 -*-
# A18.py (3회 18번 후보, 원문 J46, db_ref 'J46 킬러 설계A') 검증
# 원문 풀이(22/27) · 원리(S1=S2 ⇔ f(-p)=f(0) ⇔ k=-p/3) · 설정 줄 불통 · 판별식으로 전수 조사(유일성) · 넓이 직접 계산
# · 정답 = ④ · 선지 등차 · 오답 값(선지 안) · 조건 빼 보기 · 문장 길이 · 원문 골격 · 설계A 원안(극댓값의 합)의 약점
import os, re, sys, html, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
from items_common import COND
import items_final as F
x, t = sp.symbols('x t', real=True)
p, k, c = sp.symbols('p k c', real=True)
ns = {}; exec(open(os.path.join(HERE, 'A18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'J46' and it['ans'] == 4 and it['db_ref'] == 'J46 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert [k_ for k_, _ in it['cond']] == ['가', '나', '다']
assert it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'fig_18.svg' in it['body'] and os.path.exists(os.path.join(HERE, 'fig_18.svg'))
CH = [sp.nsimplify(v) for v in it['choices']]

def nroots(f):
    return len(set(sp.real_roots(sp.Poly(sp.expand(f), x))))

def areas(f):
    """f'의 두 근 a<b<0에 대해 S1=∫_a^b |f'|, S2=∫_b^0 f'"""
    fp = sp.diff(f, x); rs = sorted(set(sp.real_roots(sp.Poly(fp, x))))
    assert len(rs) == 2
    a, b = rs
    return a, b, -sp.integrate(fp, (x, a, b)), sp.integrate(fp, (x, b, 0))

# ---------- 원문 J46 ----------
fo_p = 3*(x + 2)*(x - k)
ko = sp.solve(sp.integrate(fo_p, (x, -2, 0)), k)
assert ko == [R(-2, 3)]
fo = sp.integrate(fo_p.subs(k, R(-2, 3)), x)
fo = fo + 2 - fo.subs(x, -2)                       # 극댓값 f(-2)=2
assert fo.subs(x, 0) == 2
mo = fo.subs(x, R(-2, 3))
a_, b_, s1, s2 = areas(fo)
assert (a_, b_) == (-2, R(-2, 3)) and s1 == s2
assert mo == R(22, 27) and F.I['J46'][2] == '⑤' and sp.nsimplify(F.I['J46'][1][4].replace('\\dfrac{22}{27}', '22/27')) == R(22, 27)
print('원문 J46: k=-2/3, 극솟값 22/27 = ⑤ OK')

# ---------- 원리: S1=S2 ⇔ ∫_{-p}^0 f'=0 ⇔ k=-p/3 ----------
fp_gen = 3*(x + p)*(x - k)
I = sp.factor(sp.integrate(fp_gen, (x, -p, 0)))
assert sp.simplify(I + p**2*(p + 3*k)/2) == 0
assert sp.solve(I, k) == [-p/3]
f_gen = sp.expand(x*(x + p)**2 + c)
assert sp.expand(sp.diff(f_gen, x) - 3*(x + p)*(x + p/3)) == 0
assert sp.simplify(f_gen.subs(x, -p) - f_gen.subs(x, 0)) == 0
maxv, minv = f_gen.subs(x, -p), sp.factor(f_gen.subs(x, -p/3))
assert maxv == c and sp.simplify(minv - (c - R(4, 27)*p**3)) == 0
print("원리: ∫_{-p}^0 f' = -p^2(p+3k)/2 → k=-p/3, f(x)=x(x+p)^2+c, 극댓값 c, 극솟값 c-4p^3/27")

# ---------- 설정 줄 불통: 극값이 주어지지 않으므로 '극댓값 - 극값의 차' 한 줄로 끝나지 않음 ----------
fam = {pv: sp.expand(x*(x + pv)**2 + 4*(pv - 4)**2) for pv in (1, 2, 5, 10)}   # (가)(다)만 만족하는 함수
assert all(fam[pv].subs(x, -4) == 0 for pv in fam) and len({fam[pv].subs(x, -pv) for pv in fam}) == 4
print('설정 줄 불통: (가)(다)만으로는 극댓값이 p마다 달라 정해지지 않음, (나)의 실근 개수로 p를 정해야 함')

# ---------- 전수 조사: (가) → f=x(x+p)^2+c, (다) → c=4(p-4)^2, (나) → 판별식 0 ----------
c_da = sp.solve(f_gen.subs(x, -4), c)
assert len(c_da) == 1 and sp.expand(c_da[0] - 4*(p - 4)**2) == 0
f_pc = sp.expand(f_gen.subs(c, 4*(p - 4)**2))
D = sp.factor(sp.discriminant(sp.Poly(f_pc, x)))
print('판별식 D(p) =', D)
Dpoly = sp.Poly(sp.numer(sp.together(D)), p)
zs = sorted(set(sp.real_roots(Dpoly)))
cand = [z for z in zs if z > 0]
assert cand == [3, 4, 12], cand
# 실근 개수: D=0이면 2개(삼중근 제외), D>0이면 3개, D<0이면 1개 → 서로 다른 실근 2개 ⇔ D=0 이고 삼중근 아님
for z in cand:
    assert nroots(f_pc.subs(p, z)) == 2
grid = [R(n, 4) for n in range(1, 81)]
for pv in grid:
    n_ = nroots(f_pc.subs(p, pv))
    assert (n_ == 2) == (pv in cand), pv
# 삼중근 가능성: f=(x-r)^3이면 f'=3(x-r)^2 → -p=k 이므로 -p<k에 어긋남
FS = {z: sp.factor(f_pc.subs(p, z)) for z in cand}
assert sp.expand(FS[4] - x*(x + 4)**2) == 0
assert sp.expand(FS[12] - (x + 4)**2*(x + 16)) == 0
assert sp.expand(FS[3] - (x + 1)**2*(x + 4)) == 0
for z, f_ in FS.items():
    a_, b_, s1, s2 = areas(f_)
    assert a_ == -z and b_ == -z/3 and -z < b_ < 0 and s1 == s2 and s1 > 0
    assert f_.subs(x, -4) == 0 and nroots(f_) == 2 and sp.Poly(f_, x).LC() == 1
print('세 함수: p=4 → x(x+4)^2, p=12 → (x+4)^2(x+16), p=3 → (x+1)^2(x+4) (각각 S1=S2, -p<k<0, f(-4)=0, 실근 2개 확인)')

# 경우 분기 기호 확인: 극댓값 0 / 극솟값 0, x=-4가 어느 근인지
case = {}
case['M0'] = sp.solve(sp.expand(x*(x + p)**2).subs(x, -4), p)                       # 근 0, -p 중 -p=-4
case['m0_double'] = sp.solve(-p/3 + 4, p); case['m0_simple'] = sp.solve(-4*p/3 + 4, p)
assert [v for v in case['M0'] if v > 0] == [4] and case['m0_double'] == [12] and case['m0_simple'] == [3]
assert sp.expand((x + p/3)**2*(x + 4*p/3) - (x*(x + p)**2 + R(4, 27)*p**3)) == 0
print('경우 분기: 극댓값 0 (근 0, -p) → -p=-4 (근 0은 불가) / 극솟값 0 (근 -p/3 접점, -4p/3) → p=12, p=3 / 실근 1개·3개 제외')

vals = {z: FS[z].subs(x, -2) for z in cand}
assert vals == {3: 2, 4: -8, 12: 56}
ans = sum(vals.values())
assert ans == 50 and CH[it['ans'] - 1] == ans
print(f'정답: f(-2)의 합 = -8 + 56 + 2 = {ans} = ④')

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {-2}
print('선지', [str(v) for v in CH], '공차 -2 (내림차순), 정답 ④')

# ---------- 오답 (선지 안) ----------
w48 = vals[4] + vals[12]          # x=-4를 접점으로만 봄 (p=3 놓침)
w56 = vals[12]                    # 극솟값 0인 경우만, x=-4를 그 접점(Q)으로
w58 = vals[12] + vals[3]          # 극댓값 0인 경우를 놓침 (선지 밖)
assert (w48, w56, w58) == (48, 56, 58)
assert it['wrongs'] == ['56', '48'] and all(sp.nsimplify(w) in CH for w in it['wrongs']) and w58 not in CH
for s_ in ('48', '56', '-8+56', '(x+4)^2(x+16)'):
    assert s_ in it['wrong'], s_
print('오답 (선지 안): 48 (x=-4를 접점으로만 보고 p=3 놓침), 56 (극솟값 0의 접점 하나만) / 58 (극댓값 0 경우 놓침)은 선지 밖')

# ---------- 설계A 원안(극댓값의 합 32)의 약점 (바꾼 이유) ----------
fA1, fA2 = x*(x + 8)**2, x*(x + 6)**2 + 32
assert fA1.subs(x, 1) == 81 and fA2.subs(x, 1) == 81 and nroots(fA1) == 2 and nroots(fA2) == 2
mA = [fA1.subs(x, -8), fA2.subs(x, -6)]
assert mA == [0, 32] and sum(mA) == mA[1]
print('설계A 원안: 극댓값 0 + 32 = 32 → 극댓값 0인 경우를 놓쳐도 답이 같음(경우 분기가 답에 일하지 않음), 32가 ④이면 0은 공차 16 이상에서만 선지에 들어감')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# (가) 빼기: k 자유. f=(x+q)^2(x+4) (극댓값 0, x=-4 단순근)은 q>4이면 f'의 근 -q<(-q-8)/3<0 → (나)(다) 만족
alt = {}
for qv in (5, 6, 8):
    f_ = sp.expand((x + qv)**2*(x + 4))
    rs = sorted(set(sp.real_roots(sp.Poly(sp.diff(f_, x), x))))
    assert rs[0] == -qv and -qv < rs[1] < 0 and nroots(f_) == 2 and f_.subs(x, -4) == 0
    _, _, s1, s2 = areas(f_); assert s1 != s2
    alt[qv] = f_.subs(x, -2)
assert len(set(alt.values())) == 3
print(f'ABLATION 18 (가) S1=S2: 필요(정해지지 않음: f=(x+q)^2(x+4), q=5,6,8 → f(-2)={list(alt.values())} 등 무수히 많음)')
alt = {}
for pv in (1, 2, 5, 6):
    f_ = f_pc.subs(p, pv); assert f_.subs(x, -4) == 0 and nroots(f_) != 2
    alt[pv] = f_.subs(x, -2)
assert len(set(alt.values())) == 4
print(f'ABLATION 18 (나) 실근 2개: 필요(정해지지 않음: f=x(x+p)^2+4(p-4)^2, p=1,2,5,6 → f(-2)={list(alt.values())} 등)')
alt = {}
for pv in (1, 2, 5, 6):
    f_ = sp.expand(x*(x + pv)**2); assert nroots(f_) == 2
    alt[pv] = f_.subs(x, -2)
assert len(set(alt.values())) == 4
print(f'ABLATION 18 (다) f(-4)=0: 필요(정해지지 않음: f=x(x+p)^2, p=1,2,5,6 → f(-2)={list(alt.values())} 등)')
# 개수를 2 대신 다른 값으로 읽으면: 1개·3개 모두 p가 구간으로 남음
n1 = [pv for pv in grid if nroots(f_pc.subs(p, pv)) == 1]; n3 = [pv for pv in grid if nroots(f_pc.subs(p, pv)) == 3]
assert len(n1) > 5 and len(n3) > 5
print(f'ABLATION 18 (나) 개수 2 → 1 또는 3: 필요(p가 구간으로 남음: 1개 {len(n1)}개·3개 {len(n3)}개 격자점)')
# 범위 -p<k<0: S2(곡선·x축·y축) 정의에 필요. k>0이면 둘러싸인 부분이 두 조각이라 S2가 정해지지 않고, 어느 쪽이든 S2<S1
pv, kv = 3, 1
fp_ = 3*(x + pv)*(x - kv)
S1_ = -sp.integrate(fp_, (x, -pv, kv)); pieces = [-sp.integrate(fp_, (x, -pv, 0)), -sp.integrate(fp_, (x, 0, kv))]
assert all(0 < s < S1_ for s in pieces)
print('ABLATION 18 범위 -p<k<0: 필요(정의: k>0이면 곡선·x축·y축으로 둘러싸인 부분이 두 조각이라 S2가 정해지지 않고 어느 쪽도 S1과 같을 수 없음, 원문 범위 그대로)')
print('경우 하나만 놓친 값: x=-4가 단순근인 경우를 놓침 → 48(⑤), 극댓값 0 경우와 단순근 경우를 놓침 → 56(①), 극댓값 0 경우를 놓침 → 58(선지 밖)')

# ---------- 문장 길이 ----------
L = lambda h: len(re.sub(r'\s', '', html.unescape(re.sub(r'</?(div|img|br|span|u|b)\b[^>]*>', '', h))))
Lo = L(F.I['J46'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 256 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개, 원문 1개)')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond'])))))
B_ = set(DC.shingles(DC.skel(DC.norm(F.I['J46'][0].replace('<k<', '&lt;k&lt;')))))
jd = len(A_ & B_) / len(A_ | B_)
assert jd <= 0.25, jd
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하)')
assert '\\[' not in it['body'] + COND(it['cond'])
assert '<k' not in it['body'] and '&lt;k&lt;0' in it['body']
print('ALL OK')
