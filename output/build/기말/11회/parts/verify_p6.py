# -*- coding: utf-8 -*-
# A18 (11회 18번 후보, 원문 M36, db_ref 'M36 킬러 설계A') 검증
# 원문 풀이(10) · 숨은 고정값 f(3)-f(0)=9 · (가) 두 개수 함수를 k 전 범위에서 정확히(사건점 + 사이 표본) · 다섯 갈래 · (나) 정수 해 전수
# · 정답 유일 · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 설계A 개수 변화점 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, k, a, b, C = sp.symbols('x k a b C', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M36' and it['ans'] == 4 and it['db_ref'] == 'M36 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert [kk for kk, _ in it['cond']] == ['가', '나']                     # 분담표: 상자 원문대로
full = it['body'] + COND(it['cond'])
for s_ in (r"실수 \(k\)에 대하여 함수 \(f(x)\)의 도함수가 \(f'(x)=x(x-2)(x-k)\)",
           r"\(f'(-1)\)의 값은?",
           r"방정식 \(f(x)=f(2)\)의 서로 다른 실근의 개수와 방정식 \(f(x)=f(3)\)의 서로 다른 실근의 개수는 같다",
           r"부등식 \(f(x)\le f(2)\)를 만족시키는 정수 \(x\)의 개수는 \(3\)이다"):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for _, cc in it['cond']: assert not re.search(r'\\\([^)]*?[<>]', cc)
CH = [sp.Integer(v) for v in it['choices']]

# ---------- 원문 M36 ----------
fo = x**4 + a*x**3 + b*x**2
bsol = sp.solve(sp.diff(fo, x).subs(x, 2), b)[0]                # f'(2)=0
fo = sp.expand(fo.subs(b, bsol))
assert sp.simplify(fo.subs(x, 3)) == 9                           # 숨은 고정값
good = []
for av in sp.solve(sp.discriminant(sp.Poly(sp.cancel((fo - 9) / (x - 3)), x), x), a) + sp.solve(sp.cancel((fo - 9) / (x - 3)).subs(x, 3), a):
    if not av.is_real: continue
    f_ = sp.expand(fo.subs(a, av))
    if len(set(sp.Poly(f_ - 9, x).real_roots())) == 3 and 0 < f_.subs(x, 3) < f_.subs(x, 2):
        good.append(f_)
assert len(good) == 1
fO = good[0]; assert sp.expand(fO - (x**4 - R(20, 3)*x**3 + 12*x**2)) == 0
pO = max(sp.Poly(sp.cancel((fO - 9) / (x - 3)**2), x).real_roots())
assert sp.simplify((3*pO - 1)**2) == 10 and F.I['M36'][2] == '10'
print('원문 M36: a=-20/3, f-9=(x-3)^2(x^2-2x/3-1), p=(1+√10)/3, (3p-1)^2=10 OK')

# ---------- 변형: f'(x)=x(x-2)(x-k), f = ∫ + C ----------
fk = sp.expand(sp.integrate(x*(x - 2)*(x - k), (x, 0, x)))     # C=0으로 둔 f (조건·묻는 값은 상수항과 무관)
assert sp.expand(sp.diff(fk, x) - x*(x - 2)*(x - k)) == 0
assert sp.simplify(fk.subs(x, 3) - fk.subs(x, 0)) == R(9, 4)                 # k와 무관
assert sp.simplify(fk.subs(x, 2) - R(4, 3)*(k - 1)) == 0
assert sp.simplify(fk.subs(x, k) - k**3*(4 - k)/12) == 0
assert sp.factor(fk.subs(x, k) - R(9, 4)) == sp.factor(-(k - 3)**2*(k**2 + 2*k + 3)/12)
assert sp.factor(fk.subs(x, k) - fk.subs(x, 2)) == sp.factor(-(k - 2)**3*(k + 2)/12)
print('f(3)-f(0)=9/4 (k 무관), f(2)-f(0)=4(k-1)/3, f(k)-f(3)=-(k-3)^2(k^2+2k+3)/12, f(k)-f(2)=-(k-2)^3(k+2)/12 OK')
# 상수항 C 무관: (가)(나)·f'(3) 모두 f(x)-f(c) 꼴
assert sp.expand((fk + C) - (fk + C).subs(x, 2) - (fk - fk.subs(x, 2))) == 0

def ndist(poly_x):
    return len(set(sp.Poly(sp.expand(poly_x), x).real_roots()))
def counts(kv):
    f = fk.subs(k, kv)
    return ndist(f - f.subs(x, 2)), ndist(f - f.subs(x, 3))

# 두 개수가 바뀔 수 있는 k(사건점): f-f(2)=(x-2)^2 h, f-f(3)=(x-3) q 에서 h·q의 판별식 0, h(2)=0, q(3)=0
h = sp.cancel((fk - fk.subs(x, 2)) / (x - 2)**2)
q = sp.cancel((fk - fk.subs(x, 3)) / (x - 3))
assert sp.Poly(h, x).degree() == 2 and sp.Poly(q, x).degree() == 3
ev_polys = [sp.discriminant(sp.Poly(h, x), x), h.subs(x, 2), sp.discriminant(sp.Poly(q, x), x), q.subs(x, 3)]
events = set()
for P in ev_polys:
    P = sp.Poly(sp.expand(P * sp.lcm([sp.fraction(c_)[1] for c_ in sp.Poly(sp.expand(P), k).coeffs()])), k)
    for r in P.real_roots(): events.add(r)
events = sorted(events, key=lambda r: float(r))
print('사건점 k:', [sp.nsimplify(e) if e.is_rational else round(float(e), 4) for e in events])
# 사건점마다 정확히, 사이 구간은 유리수 표본으로(구간 안에서 두 개수는 일정)
samples = []
ev_f = [float(e) for e in events]
pts = [ev_f[0] - 3] + [(ev_f[i] + ev_f[i + 1]) / 2 for i in range(len(ev_f) - 1)] + [ev_f[-1] + 3]
for pval in pts: samples.append(sp.nsimplify(round(pval, 6)))
sol_k = []
for kv in events:
    kv = sp.nsimplify(kv) if kv.is_rational else kv
    c2, c3 = counts(kv)
    if c2 == c3: sol_k.append(kv)
for kv in samples:
    c2, c3 = counts(kv)
    assert c2 != c3, (kv, c2, c3)          # 구간 안에서는 같지 않음
assert sorted(sol_k) == [-2, 1, 2, R(43, 16), 3], sol_k
tab = {kv: counts(kv) for kv in sol_k}
assert tab == {-2: (2, 2), 1: (2, 2), 2: (2, 2), R(43, 16): (3, 3), 3: (3, 3)}
print('(가) 만족 k 전수: -2, 1, 2, 43/16, 3 (개수 (2,2),(2,2),(2,2),(3,3),(3,3)) OK')
# 설계A의 개수 변화: f(x)=f(3)의 개수는 k=43/16에서 점프(2→3→4), k=3에서 양옆 4·그 점만 3
c3 = lambda kv: counts(kv)[1]
assert [c3(R(43, 16) - R(1, 100)), c3(R(43, 16)), c3(R(43, 16) + R(1, 100))] == [2, 3, 4]
assert [c3(3 - R(1, 100)), c3(3), c3(3 + R(1, 100))] == [4, 3, 4]
print('설계A 개수 변화점: k=43/16 (2,3,4), k=3 (4,3,4) OK')

# ---------- (나): f(x)≤f(2)인 정수 x의 개수 ----------
def int_count(kv):
    f = fk.subs(k, kv); g = sp.expand(f - f.subs(x, 2))
    rr = [float(r) for r in sp.Poly(g, x).real_roots()]
    lo, hi = int(sp.floor(min(rr))) - 2, int(sp.ceiling(max(rr))) + 2
    ints = [n for n in range(lo, hi + 1) if g.subs(x, n) <= 0]
    assert g.subs(x, lo) > 0 and g.subs(x, hi) > 0
    return ints
IC = {kv: int_count(kv) for kv in sol_k}
assert IC == {-2: [-2, 2], 1: [0, 2], 2: [0, 1, 2], R(43, 16): [0, 1, 2, 3], 3: [0, 1, 2, 3]}, IC
ok = [kv for kv in sol_k if len(IC[kv]) == 3]
assert ok == [2]
print('(나) 정수 해: k=-2 {±2}, 1 {0,2}, 2 {0,1,2}, 43/16 {0,1,2,3}, 3 {0,1,2,3} → k=2 하나 OK')
# 갈래 인수분해(해설 문장 확인)
f2 = fk.subs(k, 2)
assert sp.expand(f2 - f2.subs(x, 2) - (x - 2)**3*(3*x + 2)/12) == 0
fa = fk.subs(k, R(43, 16)); assert sp.expand(fa - fa.subs(x, 2) - (x - 2)**2*(x - 3)*(4*x + 3)/16) == 0
f3 = fk.subs(k, 3); assert sp.expand(f3 - f3.subs(x, 2) - (x - 2)**2*(3*x**2 - 8*x - 8)/12) == 0
f1 = fk.subs(k, 1); assert sp.expand(f1 - x**2*(x - 2)**2/4) == 0
fm = fk.subs(k, -2); assert sp.expand(fm - (x**4 - 8*x**2)/4) == 0 and sp.expand(fm - fm.subs(x, 2) - (x**2 - 4)**2/4) == 0
assert f1.subs(x, 1) - f1.subs(x, 0) == R(1, 4)
# 원문 함수와 같은 갈래
assert sp.expand(4*f3 - fO) == 0          # 원문 함수의 1/4배(같은 그래프 모양)
# 정답
slope = lambda kv: sp.diff(fk, x).subs({k: kv, x: -1})
ans = slope(2)
assert ans == -9 and CH[it['ans'] - 1] == ans
assert {kv: slope(kv) for kv in sol_k} == {-2: 3, 1: -6, 2: -9, R(43, 16): R(-177, 16), 3: -12}
# 정수 k 격자 추가 점검(정의대로)
hits = [kv for kv in [R(i, 16) for i in range(-80, 97)] if counts(kv)[0] == counts(kv)[1] and len(int_count(kv)) == 3]
assert hits == [2], hits
print('격자 k ∈ [-5, 6] (1/16 간격): (가)(나) 만족은 k=2 하나 OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {3}      # 오름차순
w0 = slope(3)                                                    # 원문 갈래(x=3에서 접함), (나) 확인 없음
assert w0 == -12 and len(IC[3]) == 4
g1 = sp.expand(f1 - f1.subs(x, 2))                               # k=1: f≤0 의 해를 [0,2]로 착각
mis = [n for n in range(-3, 6) if 0 <= n <= 2]
assert len(mis) == 3 and IC[1] == [0, 2] and g1.subs(x, 1) > 0
w24 = slope(1); assert w24 == -6
assert [w0, w24] == [sp.Integer(v) for v in it['wrongs']]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+|&[a-z]+;', ' ', full))}
assert ans not in nums and -ans not in nums and ans != 10, nums
print('정답이 본문의 어떤 수(부호 포함)·원문 답 10과도 같지 않음 OK')
print('정답 = ④ -9, 선지 등차(공차 3, 오름차순), 오답 -12(원문 갈래 k=3)·-6(k=1, 해를 [0,2]로) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
print(f"ABLATION 18 (나) 정수 해 3개: 필요(정해지지 않음: 빼면 k=-2,1,2,43/16,3, 답 {[slope(kv) for kv in sol_k]})")
only_na = sorted({kv for kv in [R(i, 16) for i in range(-80, 97)] if len(int_count(kv)) == 3}, key=float)
assert len(only_na) > 3 and len({slope(kv) for kv in only_na}) > 3
print(f"ABLATION 18 (가) 개수가 같음: 필요(정해지지 않음: 빼면 (나)만으로 k={only_na[0]}…{only_na[-1]} 등 {len(only_na)}개 격자점, 답 여러 개)")
for nv, exp in ((2, [-2, 1]), (4, [R(43, 16), 3])):
    alt = [kv for kv in sol_k if len(IC[kv]) == nv]
    assert alt == exp
    print(f"ABLATION 18 (나)의 3: 필요(3 대신 {nv}이면 k={alt} 두 갈래)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
# 원문 줄: x=3에서 접함(r=3, f'(3)=0), f(x)=f(3)의 실근 3개. 정답 함수: f'(3)=3≠0, f(x)=f(3)의 실근 2개
assert sp.diff(fk, x).subs({k: 2, x: 3}) == 3 and counts(2)[1] == 2
print("원문 설정 줄(x=3에서 접함, f'=4x(x-2)(x-3)): 정답 함수에서 f'(3)=3, f(x)=f(3)의 실근 2개(불통) OK")

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M36'][0])); Lm = len(plain(full))
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')
assert Lm >= 0.9 * Lo, (Lo, Lm)

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(full))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M36'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
print('ALL OK')
