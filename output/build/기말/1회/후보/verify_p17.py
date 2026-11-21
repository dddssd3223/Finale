# -*- coding: utf-8 -*-
# p17.py (1회 17번 Claude 후보 claude17) 검증
# 원문 M32 풀이(19) · 설정 유일성 · (나) 판정 전수(k 격자 + 경계) · 정답 유일성 · 선지 등차 · 오답 근거 · 조건 빼 보기 · 원문 원리 줄 불통 · 길이
import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy import Rational as R, Poly, real_roots

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p17.py')).read(), ns)
IT = ns['ITEMS']; P = IT[17]
assert list(IT) == [17] and P['author'] == 'claude' and P['cand'] == 'claude17' and P['key'] == 'M32'
assert len(P['cond']) == 2 and [c[0] for c in P['cond']] == ['가', '나']
assert P['core']['axis'] == '①' and all(P['core'][k] for k in ('setting', 'principle', 'new'))
assert P['effect'] == '어려워짐' and P['bunseok'] is False and P['precedent'] and P['vtype']
x = sp.symbols('x', real=True)

def nonneg(poly):
    """다항식 poly(x)가 모든 실수 x에서 0 이상인지 정확히 판정 (실근 사이·바깥의 유리점에서 부호 확인)"""
    p = Poly(sp.expand(poly), x)
    if p.is_zero: return True
    rts = sorted(set(real_roots(p)), key=lambda r: sp.N(r, 50))
    if not rts: return p.eval(0) >= 0
    pts = [sp.floor(sp.N(rts[0], 30)) - 1, sp.ceiling(sp.N(rts[-1], 30)) + 1]
    for a, b in zip(rts, rts[1:]):
        lo, hi = sp.N(a, 40), sp.N(b, 40)
        pts.append(sp.nsimplify((lo + hi) / 2, rational=True))
    return all(p.eval(R(t)) >= 0 for t in pts)

def ndistinct(poly):
    return len(set(real_roots(Poly(sp.expand(poly), x))))

f = x**2 * (x - 4)
fp = sp.diff(f, x)

# ===== 원문 M32: f=x^2(x-4), f(x)-xf'(k)=0의 서로 다른 실근 2개 → k 합 16/3 → p+q=19 =====
k = sp.symbols('k', real=True)
cs = sorted(set([R(n, 4) for n in range(-80, 81)] + [R(-16, 3)]))
two = [c for c in cs if ndistinct(f - c * x) == 2]
assert two == [-4, 0], two
ks = set()
for c in two:
    ks |= set(sp.solve(sp.Eq(fp.subs(x, k), c), k))
assert ks == {0, R(8, 3), 2, R(2, 3)} and sum(ks) == R(16, 3)
import sys as _s
_s.path.insert(0, '/home/user/Finale/template/db/parts'); _s.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
assert F.I['M32'][2] == '19' and R(16, 3).p + R(16, 3).q == 19
print('원문 M32: 근 2개인 f\'(k) =', two, '→ k =', sorted(ks), '합 16/3 → 19 OK')

# ===== 설정 유일성: 최고차항 1인 삼차함수 중 (가)·f(0)=0을 만족시키는 것은 x^2(x-4)뿐 =====
# (가) ⇒ f(4)=0 (부호가 4에서 바뀜), f=(x-4)(x^2+px+q), h=x^2+px+q>=0, f(0)=0 ⇒ q=0 ⇒ x(x+p)>=0 ⇒ p=0
grid = [R(n, 4) for n in range(-24, 25)]
sols = []
for p in grid:
    for q in grid:
        ff = (x - 4) * (x**2 + p * x + q)
        if ff.subs(x, 0) == 0 and nonneg((x - 4) * ff):
            sols.append((p, q))
assert sols == [(0, 0)], sols
# 근 4가 아닌 삼차(부호가 4에서 안 바뀜)는 (가) 불가: 예 f=x^3, x^2(x-3), x^2(x-5)
for ff in (x**3, x**2 * (x - 3), x**2 * (x - 5), x * (x - 4)**2):
    assert not nonneg((x - 4) * ff)
print('설정: (가)·f(0)=0 → f(x)=x^2(x-4) 유일 OK')

# ===== (나) 판정: 기울기 m=f'(k), 절편 n인 직선 g에 대하여 (x-2)(f-g)>=0 =====
def ok_line(m, n):
    return nonneg((x - 2) * (f - m * x - n))

def ok_k(kv):
    m = fp.subs(x, kv)
    n_forced = f.subs(x, 2) - 2 * m          # (나) ⇒ g(2)=f(2)
    # 다른 절편이면 x=2에서 부호가 바뀌어 불가
    for dn in (R(1, 100), R(-1, 100), 1, -1, 5, -5):
        assert not ok_line(m, n_forced + dn), (kv, dn)
    return ok_line(m, n_forced)

kgrid = sorted(set([R(n, 24) for n in range(-72, 145)] + [R(1), R(5, 3), R(2, 3), R(2), R(4, 3),
               R(1) - R(1, 1000), R(5, 3) + R(1, 1000), R(1) + R(1, 1000), R(5, 3) - R(1, 1000)]))
K = [kv for kv in kgrid if ok_k(kv)]
assert K == [kv for kv in kgrid if 1 <= kv <= R(5, 3)], (K[:3], K[-3:])
assert R(1) in K and R(5, 3) in K and R(1) - R(1, 1000) not in K and R(5, 3) + R(1, 1000) not in K
print(f'(나)를 만족시키는 k: 격자 {len(kgrid)}개 전수 → 정확히 [1, 5/3] OK')

# 경계·겹침 판정 확인
assert fp.subs(x, 1) == -5 and fp.subs(x, R(5, 3)) == -5
assert sp.factor((x - 2) * (f - (-5 * x + 2))) == (x - 2)**2 * (x - 1)**2          # 접함(x=1): 부호 불변 → 성립
g4 = -4 * x                                                                      # 겹침: f'(k)=-4 (k=2, 2/3), g=-4x
assert f.subs(x, 2) == g4.subs(x, 2) and sp.factor(f - g4) == x * (x - 2)**2
assert not nonneg((x - 2) * (f - g4)) and ((x - 2) * (f - g4)).subs(x, 1) < 0    # 0<x<2에서 음수 → 불성립
assert fp.subs(x, 2) == -4 and fp.subs(x, R(2, 3)) == -4
print('경계: f\'(k)=-5(x=1에서 접함) 포함, 겹침 f\'(k)=-4(g=-4x) 제외 OK')

# ===== 정답: [1, 5/3]에서 f(k)의 최댓값 =====
crit = [c for c in sp.solve(fp, x) if 1 <= c <= R(5, 3)]
assert crit == []                                  # 구간 안 임계점 없음 → 단조
assert all(fp.subs(x, t) < 0 for t in (1, R(4, 3), R(5, 3)))
vals = [f.subs(x, t) for t in K]
ans_val = max(vals)
assert ans_val == -3 and f.subs(x, 1) == -3 and vals.count(-3) == 1
ch = [Fr(c) for c in P['choices']]
assert len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1 and ch == sorted(ch) and ch[1] - ch[0] == 1
assert P['ans'] == 3 and ch[P['ans'] - 1] == ans_val
print(f'정답: k=1에서 f(k) 최댓값 {ans_val}, 선지 ③, 오름차순 공차 1 OK')

# ===== 오답 근거 값 =====
assert max(fp.subs(x, t) for t in K) == -5 == ch[0] and '① \\(-5\\)' in P['wrong']
# 착오(겹침 허용) → k=2/3이 들어와 최댓값 -40/27 (정수 선지 아님)
assert f.subs(x, R(2, 3)) == R(-40, 27) and R(-40, 27) not in ch
# 착오(접함 제외) → 1<k<5/3, 최댓값 없음(상한 -3 미달성)
assert all(f.subs(x, t) < -3 for t in K if 1 < t < R(5, 3))
print('오답 근거 값 OK')

# ===== 원문 원리 줄 불통: 교점 개수(근 겹침·중근)로 판정하면 결과가 다름 =====
def cnt(kv):
    m = fp.subs(x, kv); return ndistinct(f - m * (x - 2) + 8)
two_k = [kv for kv in kgrid if cnt(kv) == 2]
assert set(two_k) == {R(2, 3), R(1), R(5, 3), R(2)}      # '두 점' 판정: 겹침(2/3, 2) + 중근(1, 5/3)
assert not ok_k(R(2)) and not ok_k(R(2, 3)) and ok_k(R(4, 3)) and cnt(R(4, 3)) == 1
print('원문 원리 줄 불통: 두 점 판정이면 k∈{2/3,1,5/3,2}(겹침 포함, 구간 내부 제외) → 실제 [1,5/3]과 다름 OK')

# ===== 조건 빼 보기 =====
def best(ff, ks):
    ffp = sp.diff(ff, x); out = []
    for kv in ks:
        m = ffp.subs(x, kv); n = ff.subs(x, 2) - 2 * m
        if nonneg((x - 2) * (ff - m * x - n)): out.append(kv)
    return out
# (가) 빼기: f=x^3도 f(0)=0·(나) 가능, (나)의 k는 [-1,1] → f(k) 최댓값 1 ≠ -3
kk = best(x**3, [R(n, 8) for n in range(-24, 25)])
assert kk == [R(n, 8) for n in range(-8, 9)] and max(t**3 for t in kk) == 1
print('ABLATION 17 (가): 필요(빼면 f(x)=x^3도 되어 k∈[-1,1], f(k)의 최댓값 1 → 답 -3이 아님)')
# (나) 빼기: k 임의 → f(k)=k^2(k-4) 위로 유계 아님
assert f.subs(x, 10) == 600 and f.subs(x, 100) > 10**5
print('ABLATION 17 (나): 필요(빼면 k가 임의여서 f(k)의 최댓값이 없음)')
# 본문 f(0)=0 빼기: f=(x-4)^3도 (가)를 만족, (나)의 k는 [3,5] → 최댓값 1
f3 = (x - 4)**3
assert nonneg((x - 4) * f3)
kk = best(f3, [R(n, 4) for n in range(0, 33)])
assert kk == [R(n, 4) for n in range(12, 21)] and max(f3.subs(x, t) for t in kk) == 1
print('ABLATION 17 f(0)=0: 필요(빼면 f(x)=(x-4)^3도 되어 f(k)의 최댓값 1 → 답이 바뀜)')

# ===== 길이: 원문 이상 (태그·공백 제거) =====
from items_common import COND
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', t))
L_new = len(plain(P['body'] + COND(P['cond']))); L_org = len(plain(F.I['M32'][0]))
assert L_new >= L_org, (L_new, L_org)
print(f'길이: 변형 {L_new}자 >= 원문 {L_org}자 OK')
print('ALL OK')
