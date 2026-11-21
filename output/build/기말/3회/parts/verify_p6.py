# -*- coding: utf-8 -*-
# A18.py (3회 18번 후보, 원문 J46, db_ref 'J46 킬러 설계A') 검증 — 재설계 1회(관문 3 미통과 반영)
# 원문 풀이(22/27) · 원리(S1=S2 ⇔ k=-p/3) · 상수항 c 무관(극값·상수 결정 단계 없음) · 점 A를 지나는 접선 전수
# · 넓이 공식 (s-t)^4/12 · 판정 p=1,5,7 (p=-1 버림, p=3 접선 하나) · 격자 전수 · 정답 = ④ · 선지 등차 · 오답(선지 안)
# · 조건 빼 보기 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
from items_common import COND
import items_final as F
x, t, s = sp.symbols('x t s', real=True)
p, k, c = sp.symbols('p k c', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'J46' and it['ans'] == 4 and it['db_ref'] == 'J46 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert [k_ for k_, _ in it['cond']] == ['가', '나']
assert it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'fig_18.svg' in it['body'] and os.path.exists(os.path.join(HERE, 'fig_18.svg'))
assert '64}{3}' in it['cond'][1][1] and 'A}(-2' in it['cond'][1][1] and 'int_{-3}^{-2}' in it['body']
CH = [sp.nsimplify(v) for v in it['choices']]
AREA = R(64, 3); XA = -2

def enclosed(f_, line):
    """곡선 f_와 직선 line으로 둘러싸인 부분의 넓이(교점이 둘 이상일 때), 없으면 None"""
    d = sp.Poly(sp.expand(f_ - line), x)
    rs = sorted(set(sp.real_roots(d)))
    if len(rs) < 2: return None
    return sum(abs(sp.integrate(d.as_expr(), (x, rs[i], rs[i + 1]))) for i in range(len(rs) - 1))

def tangents_through_A(f_):
    """점 A(-2, f(-2))를 지나는 접선의 접점 전부(실수)"""
    fpp = sp.diff(f_, x)
    eq = sp.expand(f_.subs(x, t) + fpp.subs(x, t)*(XA - t) - f_.subs(x, XA))
    return sorted(set(sp.real_roots(sp.Poly(eq, t))))

def tline(f_, tt):
    return f_.subs(x, tt) + sp.diff(f_, x).subs(x, tt)*(x - tt)

def ok_na(f_):
    return any(enclosed(f_, tline(f_, tt)) == AREA for tt in tangents_through_A(f_))

# ---------- 원문 J46 ----------
fo_p = 3*(x + 2)*(x - k)
assert sp.solve(sp.integrate(fo_p, (x, -2, 0)), k) == [R(-2, 3)]
fo = sp.integrate(fo_p.subs(k, R(-2, 3)), x)
fo = fo + 2 - fo.subs(x, -2)                       # 극댓값 f(-2)=2
assert fo.subs(x, 0) == 2 and fo.subs(x, R(-2, 3)) == R(22, 27) and F.I['J46'][2] == '⑤'
print('원문 J46: k=-2/3, 극솟값 22/27 = ⑤ OK')

# ---------- 원리: S1=S2 ⇔ ∫_{-p}^0 f'=0 ⇔ k=-p/3 ----------
I_ = sp.integrate(3*(x + p)*(x - k), (x, -p, 0))
assert sp.simplify(I_ + p**2*(p + 3*k)/2) == 0 and sp.solve(I_, k) == [-p/3]
f_gen = x**3 + 2*p*x**2 + p**2*x + c
assert sp.expand(sp.diff(f_gen, x) - 3*(x + p)*(x + p/3)) == 0
print("원리: ∫_{-p}^0 f' = -p^2(p+3k)/2 → k=-p/3, f(x)=x^3+2px^2+p^2x+c (c는 끝까지 정해지지 않음)")

# ---------- 상수항 c 무관: 접점 방정식·넓이·묻는 값 모두 c가 없음 (원문 극값·상수 결정 단계가 쓸 곳이 없음) ----------
eqA = sp.factor(f_gen.subs(x, t) + sp.diff(f_gen, x).subs(x, t)*(XA - t) - f_gen.subs(x, XA))
assert sp.simplify(eqA - (-2*(t + 2)**2*(t + p - 1))) == 0 and c not in eqA.free_symbols
J = sp.expand(sp.integrate(sp.diff(f_gen, x), (x, -3, -2)))
assert sp.expand(J - (p**2 - 10*p + 19)) == 0 and c not in J.free_symbols
print('c 무관: 점 A를 지나는 접선의 접점 방정식 -2(t+2)^2(t+p-1)=0, ∫_{-3}^{-2} f\' = p^2-10p+19')

# ---------- 넓이 공식과 근과 계수의 관계 ----------
tt_, ss_ = sp.symbols('tt ss', real=True)
assert sp.simplify(abs(sp.integrate((x - tt_)**2*(x - ss_), (x, tt_, ss_))).subs({tt_: 0, ss_: 3}) - R(81, 12)) == 0
assert sp.factor(sp.integrate((x - tt_)**2*(x - ss_), (x, tt_, ss_))) == -(ss_ - tt_)**4/12
fT = sp.expand(f_gen - tline(f_gen, t))
assert sp.expand(fT - (x - t)**2*(x + 2*p + 2*t)) == 0                 # 재교점 s = -2p-2t
print('넓이: ∫(x-t)^2(x-s) 절댓값 = (s-t)^4/12, 접선의 재교점 s=-2p-2t')

# ---------- 경우 분기 (기호) ----------
# (i) 접점 A(t=-2): s=4-2p, 넓이 (6-2p)^4/12 / (ii) 재교점 A(s=-2): t=1-p, 넓이 (3-p)^4/12
c1 = sorted(sp.solve(sp.Eq((6 - 2*p)**4/12, AREA), p))
c2 = sorted(sp.solve(sp.Eq((3 - p)**4/12, AREA), p))
c1 = [v for v in c1 if v.is_real]; c2 = [v for v in c2 if v.is_real]
assert c1 == [1, 5] and c2 == [-1, 7]
sols = sorted([v for v in c1 + c2 if v > 0])
assert sols == [1, 5, 7]
print('경우: A에서 접함 |6-2p|=4 → p=1, 5 / 다른 점(x=1-p)에서 접하고 A에서 다시 만남 |3-p|=4 → p=7 (p=-1은 p>0에 어긋나 버림)')
f3 = f_gen.subs({p: 3, c: 0})
assert tangents_through_A(f3) == [-2] and enclosed(f3, tline(f3, -2)) is None
print('경계: p=3이면 A가 변곡점이라 접선이 하나뿐이고 둘러싸인 부분이 없음')

# ---------- 각 해를 직접 확인 (c 여러 값) ----------
info = {}
for pv in sols:
    for cv in (0, 5, -7):
        f_ = sp.expand(f_gen.subs({p: pv, c: cv}))
        fp_ = sp.diff(f_, x); rs = sorted(set(sp.real_roots(sp.Poly(fp_, x))))
        assert rs == [-pv, R(-pv, 3)] and -pv < rs[1] < 0
        S1 = -sp.integrate(fp_, (x, rs[0], rs[1])); S2 = sp.integrate(fp_, (x, rs[1], 0))
        assert S1 == S2 > 0
        assert ok_na(f_)
        hits = [tt for tt in tangents_through_A(f_) if enclosed(f_, tline(f_, tt)) == AREA]
        assert len(hits) == 1
        info[pv] = (hits[0], sp.integrate(fp_, (x, -3, -2)))
assert info == {1: (-2, 10), 5: (-2, -6), 7: (-6, -2)}, info
print('직접 확인: p=1 (A에서 접함) → 10, p=5 (A에서 접함) → -6, p=7 (x=-6에서 접하고 A를 지남) → -2 (c=0, 5, -7 모두 같음)')

# ---------- 격자 전수: p를 1/4 간격으로 0~20 ----------
grid = [R(n, 4) for n in range(1, 81)]
hit = [pv for pv in grid if ok_na(f_gen.subs({p: pv, c: 0}))]
assert hit == [1, 5, 7], hit
# 두 넓이 함수는 각 구간에서 단조이므로 64/3을 지나는 p는 위 기호 풀이의 해뿐
for e, roots in (((6 - 2*p)**4/12, [1, 5]), ((3 - p)**4/12, [7])):
    for r_ in roots:
        assert e.subs(p, r_) == AREA
print(f'격자 {len(grid)}개 p 중 (나)를 만족시키는 것은 p=1, 5, 7뿐')

ans = sum(v for _, v in info.values())
assert ans == 2 and CH[it['ans'] - 1] == ans
print(f'정답: 10 + (-6) + (-2) = {ans} = ④')

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {-2}
print('선지', [str(v) for v in CH], '공차 -2 (내림차순), 정답 ④')

# ---------- 오답 (선지 안) ----------
w4 = info[1][1] + info[5][1]          # A에서의 접선만 (p=7 놓침)
w8 = info[1][1] + info[7][1]          # 재교점을 A 오른쪽으로만 보고 p=5 놓침
wm1 = ans + J.subs(p, -1)             # p=-1을 버리지 않음 (선지 밖)
w_sign = -ans                         # f(-3)-f(-2)로 부호 실수 (선지 밖)
assert (w4, w8) == (4, 8) and wm1 == 32 and w_sign not in CH and wm1 not in CH
assert it['wrongs'] == ['8', '4'] and all(sp.nsimplify(w) in CH for w in it['wrongs'])
for s_ in ('10+(-6)=4', '10+(-2)=8', 'p=5'):
    assert s_ in it['wrong'].replace(r'\(', '').replace(r'\)', '').replace(' ', ''), s_
print('오답 (선지 안): 4 (A에서의 접선만, p=7 놓침), 8 (재교점을 A 오른쪽으로만, p=5 놓침) / p=-1 포함 32, 부호 실수 -2는 선지 밖')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# (가) 빼기: k 자유. f'=3(x+p)(x-k)의 f에서 이차항 계수 B=3(p-k)/2. (나)는 B로만 정해지고(|6-B|=4 또는 |3-B/2|=4), 묻는 값은 p, k 따로 의존
B_ = sp.symbols('B', real=True)
alt = {}
pairs = []
for pv in (R(3, 4), R(5, 6), R(7, 6)):
    kv = pv - R(4, 3)                 # B = 3(p-k)/2 = 2 (원래 p=1과 같은 B), 2/3<p<4/3이면 -p<k<0
    assert -pv < kv < 0
    f_ = sp.expand(sp.integrate(3*(x + pv)*(x - kv), x))
    assert ok_na(f_)
    alt[(pv, kv)] = sp.integrate(sp.diff(f_, x), (x, -3, -2))
    pairs.append((pv, kv))
assert len(set(alt.values())) >= 3, alt
print(f'ABLATION 18 (가) S1=S2: 필요(정해지지 않음: 이차항 계수 2인 f\'=3(x+p)(x-k), (p,k)={[(str(a), str(b)) for a, b in pairs]} → ∫={[str(v) for v in alt.values()]} 등)')
altn = {pv: J.subs(p, pv) for pv in (2, 3, 4, 6)}
assert len(set(altn.values()) | {ans}) >= 4
print(f'ABLATION 18 (나) 넓이 64/3: 필요(정해지지 않음: p=2,3,4,6 → ∫={list(altn.values())} 등, p는 양수 전체)')
# (나)의 '접선 중 존재' 해석: A에서의 접선만으로 읽으면 p=1,5 → 4, 다른 접선만이면 p=7 → -2 (모두 선지 4 / 정답과 다름)
onlyA = sum(v for tt, v in info.values() if tt == -2); onlyT = sum(v for tt, v in info.values() if tt != -2)
assert (onlyA, onlyT) == (4, -2) and onlyA != ans and onlyT != ans
print(f'ABLATION 18 (나) 접선 종류: 필요(A에서의 접선만 → {onlyA}, 다른 점에서 접하고 A를 지나는 접선만 → {onlyT}, 두 종류를 모두 봐야 {ans})')
pv, kv = 3, 1
fp_ = 3*(x + pv)*(x - kv)
S1_ = -sp.integrate(fp_, (x, -pv, kv)); pieces = [-sp.integrate(fp_, (x, -pv, 0)), -sp.integrate(fp_, (x, 0, kv))]
assert all(0 < q < S1_ for q in pieces)
print('ABLATION 18 범위 -p<k<0: 필요(정의: k>0이면 곡선·x축·y축으로 둘러싸인 부분이 두 조각이라 S2가 정해지지 않고 어느 쪽도 S1과 같을 수 없음, 원문 범위 그대로)')

# ---------- 문장 길이 ----------
L = lambda h: len(re.sub(r'\s', '', html.unescape(re.sub(r'</?(div|img|br|span|u|b)\b[^>]*>', '', h))))
Lo = L(F.I['J46'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 256 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개, 원문 1개)')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond'])))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['J46'][0].replace('<k<', '&lt;k&lt;')))))
jd = len(A_ & B2) / len(A_ | B2)
assert jd <= 0.25, jd
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하)')
assert '\\[' not in it['body'] + COND(it['cond'])
assert '<k' not in it['body'] and '&lt;k&lt;0' in it['body']
print('ALL OK')
