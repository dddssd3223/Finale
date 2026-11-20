# -*- coding: utf-8 -*-
# 서답형1 (자체, M2 유형) · 서답형2 (M54 학교식) 검증 · author='claude'
import sympy as sp, os, sys, re
import numpy as np
x, a, k = sp.symbols('x a k', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def minmax(f, lo, hi):
    """닫힌구간 [lo, hi]에서 다항함수 f의 (최솟값, 최댓값) — 끝점과 구간 안 정류점 전수"""
    pts = [sp.Integer(lo), sp.Integer(hi)] + [c for c in sp.Poly(sp.diff(f, x), x).real_roots() if lo < c < hi]
    vals = [sp.simplify(f.subs(x, c)) for c in pts]
    return min(vals), max(vals)

# ================= S1 =================
# --- 원문 M2: [1,4], -x^3+3x^2+a, 최댓값 8 → 최솟값 -12
fo = -x**3 + 3 * x**2 + a
so = [v for v in sp.solve(fo.subs(x, 2) - 8, a) if minmax(fo.subs(a, v), 1, 4)[1] == 8]
assert so == [4] and minmax(fo.subs(a, 4), 1, 4) == (-12, 8)
assert F.I['M2'][2] == '⑤' and F.I['M2'][1][4] == '-12'
print('M2 원문 OK: a=4, 최솟값 -12 (원문 정답 ⑤)')

# --- S1: [-2,4], 2x^3-3x^2-12x+a, 최솟값 -15
assert r"f(x)=2x^3-3x^2-12x+a" in S1['body'] and r"\([-2,\ 4]\)" in S1['body'] and r"최솟값이 \(-15\)" in S1['body']
f1 = 2 * x**3 - 3 * x**2 - 12 * x + a
assert sp.expand(sp.diff(f1, x) - 6 * (x + 1) * (x - 2)) == 0
vals = {c: sp.expand(f1.subs(x, c)) for c in (-2, -1, 2, 4)}
assert vals == {-2: a - 4, -1: a + 7, 2: a - 20, 4: a + 32}
# 최솟값은 a 와 무관하게 f(2)=a-20 (상수항은 모든 후보를 같이 옮김) → a 하나
mn0, mx0 = minmax(f1.subs(a, 0), -2, 4)
assert (mn0, mx0) == (-20, 32)
A1 = sp.solve(mn0 + a + 15, a)
assert A1 == [5] and minmax(f1.subs(a, 5), -2, 4) == (-15, 37)
assert [av for av in range(-60, 61) if minmax(f1.subs(a, av), -2, 4)[0] == -15] == [5]      # 전수
assert S1['ans'] == [r'(1) \(5\)', r'(2) \(37\)']
# 판단: 최댓값은 극댓값 12 가 아니라 오른쪽 끝 37
assert f1.subs({a: 5, x: -1}) == 12 and f1.subs({a: 5, x: 4}) == 37
# 오답 값
assert sp.solve(vals[-2] + 15, a) == [-11]
assert sp.solve(16 - 12 + 24 + a + 15, a) == [-43]
assert 128 - 48 + 5 == 85
for w in (r'a=-11', r'a=-43', r'f(-1)=12', r'128-48+5=85'): assert w in S1['wrong'], w
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 M2)'
print('S1 OK: (1) a=5 하나, (2) 최댓값 f(4)=37 (극댓값 12 아님)')

def abl1(c, m): print(f'ABLATION S1 {c}: {m}')
abl1('최솟값이 -15', '필요(없으면 a가 정해지지 않아 최댓값이 a+32로 남음)')
assert minmax(f1.subs(a, 0), -2, 4)[1] - 32 == 0
# 구간 오른쪽 끝 4 → 3: 최댓값이 극댓값 12 로 바뀜
assert minmax(f1.subs(a, 5), -2, 3) == (-15, 12)
abl1('구간의 오른쪽 끝 4', '필요(3으로 바꾸면 a=5는 그대로지만 최댓값이 극댓값 12로 바뀜)')
# 구간 왼쪽 끝 -2 → -3: f(-3)=a-45 가 최솟값이 되어 a 가 바뀜
m3 = minmax(f1.subs(a, 0), -3, 4)[0]
assert m3 == -45 and sp.solve(m3 + a + 15, a) == [30]
abl1('구간의 왼쪽 끝 -2', '필요(-3으로 바꾸면 최솟값이 f(-3)=a-45가 되어 a=30)')


# ================= S2 =================
def branches(h, c2, mul, lo=0, hi=1):
    """f=h(x)+k, f' 대칭축 c2/2. f'(g(x))=f'(mul*x) 의 두 갈래 g=mul*x, g=c2-mul*x 에서
    x=f(g) ⇒ k=x-h(g). [lo,hi]에서 각 갈래의 k 범위 (전수: 끝점+정류점)"""
    out = []
    for gx in (mul * x, c2 - mul * x):
        kx = sp.expand(x - h.subs(x, gx))
        out.append(minmax(kx, lo, hi) + (kx,))
    return out

def union_range(rs):
    rs = sorted((r[0], r[1]) for r in rs)
    connected = rs[1][0] <= rs[0][1]
    return min(r[0] for r in rs), max(r[1] for r in rs), connected

# --- 원문 M54
ho = x**3 - 3 * x**2 + 6 * x
assert sp.expand(4 * sp.diff(ho, x) + 12 * x - 18 - sp.diff(ho, x).subs(x, 2 * x)) == 0
bo = branches(ho, 2, 2)
assert [(b[0], b[1]) for b in bo] == [(-7, 0), (-8, 1)]
mo, Mo, _ = union_range(bo)
assert mo**2 + Mo**2 == 65 and F.I['M54'][2] == '65'
print('M54 원문 OK: [-7,0]∪[-8,1], m^2+M^2=65')
# --- LIVE1-02-212 (보평고): x^3-6x^2+15x+k, 16f'+144x-225=f'(4x) → 차 29
hl = x**3 - 6 * x**2 + 15 * x
assert sp.expand(16 * sp.diff(hl, x) + 144 * x - 225 - sp.diff(hl, x).subs(x, 4 * x)) == 0
bl = branches(hl, 4, 4); ml, Ml, _ = union_range(bl)
assert [(b[0], b[1]) for b in bl] == [(-27, 0), (-28, 1)] and Ml - ml == 29

# --- S2
assert r"f(x)=x^3-6x^2+18x+k" in S2['body'] and '역함수' in S2['body'] and 'cond' not in S2
q1, q2, q3 = [q[0] for q in S2['subs']]
assert r"f'(a)=f'(b)" in q1 and '서로 다른 두 실수' in q1 and r"a+b" in q1
assert r"g(x)=3x" in q2 and r"\([0,\ 1]\)" in q2 and '최솟값' in q2
assert r"9f'(x)+72x-144=f'(g(x))" in q3 and r"\([0,\ 1]\)" in q3 and '최댓값과 최솟값의 차' in q3
h = x**3 - 6 * x**2 + 18 * x
fp = sp.diff(h, x)
assert sp.expand(fp - (3 * (x - 2)**2 + 6)) == 0                       # f'>0: 역함수 존재, 축 x=2
# (1) f'(a)=f'(b), a≠b ⇒ a+b=4
aa, bb = sp.symbols('aa bb')
assert sp.expand(fp.subs(x, aa) - fp.subs(x, bb) - 3 * (aa - bb) * (aa + bb - 4)) == 0
ANS1 = 4
# 좌변 = f'(3x)
assert sp.expand(9 * fp + 72 * x - 144 - fp.subs(x, 3 * x)) == 0
b2 = branches(h, 4, 3)
assert b2[0][2] == -27 * x**3 + 54 * x**2 - 53 * x and b2[1][2] == 27 * x**3 - 54 * x**2 + 55 * x - 40
assert sp.Poly(sp.diff(b2[0][2], x), x).real_roots() == [] and sp.Poly(sp.diff(b2[1][2], x), x).real_roots() == []   # 둘 다 단조
assert sp.expand(sp.diff(b2[0][2], x) - (-81 * (x - R(2, 3))**2 - 17)) == 0 and sp.expand(sp.diff(b2[1][2], x) - (81 * (x - R(2, 3))**2 + 19)) == 0
assert [(b[0], b[1]) for b in b2] == [(-26, 0), (-40, -12)]
ANS2 = b2[0][0]
m2, M2, conn = union_range(b2)
assert conn and (m2, M2) == (-40, 0)                                   # 두 범위가 이어져 있음
ANS3 = M2 - m2
assert (ANS1, ANS2, ANS3) == (4, -26, 40)
assert S2['ans'] == [r'(1) \(4\)', r'(2) \(-26\)', r'(3) \(40\)']
# 최댓값·최솟값이 서로 다른 갈래에서 나옴(한 갈래만으로는 답이 안 나옴)
assert b2[0][1] == M2 and b2[1][0] == m2 and b2[0][0] != m2 and b2[1][1] != M2

# 수치 전수: 역함수를 직접 풀어 방정식 9f'(x)+72x-144=f'(g(x)) 의 [0,1] 실근 존재 여부를 k 격자에서 확인
hf = sp.lambdify(x, h, 'numpy'); fpf = sp.lambdify(x, fp, 'numpy')
xs = np.linspace(0, 1, 40001)
def ginv(kv):
    y = np.full_like(xs, 1.0)
    for _ in range(80):
        y = y - (hf(y) + kv - xs) / fpf(y)            # f 증가·f'>=6 이라 뉴턴법 수렴
    assert np.max(np.abs(hf(y) + kv - xs)) < 1e-9
    return y
def has_root(kv, lhs):
    G = lhs(xs) - fpf(ginv(kv))
    return bool(np.min(np.abs(G)) < 1e-3 or np.any(G[:-1] * G[1:] < 0))
lhs3 = lambda t: 9 * fpf(t) + 72 * t - 144
ks = [R(i, 4) for i in range(-180, 21)]
got = [kv for kv in ks if has_root(float(kv), lhs3)]
assert min(got) == -40 and max(got) == 0 and len(got) == 161, (min(got), max(got), len(got))   # -40≤k≤0 전부(1/4 간격 161개)
# (2) g(x)=3x 의 실근 존재: -26≤k≤0
def has_root2(kv):
    G = ginv(kv) - 3 * xs
    return bool(np.min(np.abs(G)) < 1e-4 or np.any(G[:-1] * G[1:] < 0))
got2 = [kv for kv in ks if has_root2(float(kv))]
assert min(got2) == -26 and max(got2) == 0 and len(got2) == 105
print('S2 수치 전수 OK: 방정식의 실근이 있는 k = [-40, 0], g(x)=3x 는 [-26, 0]')

# 오답 값
assert ANS1 // 2 == 2
assert minmax(sp.expand(-(h - 3 * x)), 0, 1)[0] == -10                 # f(x)=3x 로 읽음: k=-x^3+6x^2-15x
assert 3 - h.subs(x, 3) == -24
assert b2[0][1] - b2[0][0] == 26 and b2[1][1] - b2[1][0] == 28 and 26 + 28 == 54
for w in (r'\(2\)', r'\(-10\)', r'\(-24\)', r'=26\)', r'=28\)', r'=54\)'): assert w in S2['wrong'], w
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['3점, 답만 적으시오.', '3점, 답만 적으시오.', '4점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S2['rubric'][:3]]
assert pts2 == [[3], [3], [4]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line for line in S2['rubric'][:3])
assert S2['db_ref'] == 'M54 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
for it in (S1, S2):
    t = it['body'] + ''.join(q[0] for q in it['subs'])
    assert '이러한' not in t and '이와 같은' not in t
    assert not [m for m in re.findall(r'\\\(.*?\\\)', t) if '<' in m or '>' in m]
print('S2 OK: (1) 4 (2) -26 (3) 40')

def abl2(c, m): print(f'ABLATION S2 {c}: {m}')
# (a) 구간 [0,1] → [0,2]
ba = branches(h, 4, 3, 0, 2); ma, Ma, _ = union_range(ba)
assert (ba[0][0], Ma - ma) != (ANS2, ANS3)
abl2('닫힌구간 [0, 1]', f'필요([0, 2]이면 (2) {ba[0][0]}, (3) {Ma - ma}로 바뀜)')
# (b) 보정항 72x-144 삭제: 9f'(x)=f'(g(x)) 는 f'(3x) 꼴이 아니어서 두 갈래가 일차식이 아님 → 답이 바뀜
yb = [2 + np.sqrt(9 * (xs - 2)**2 + 16), 2 - np.sqrt(9 * (xs - 2)**2 + 16)]      # f'(y)=9f'(x) 의 두 해
kb = np.concatenate([xs - hf(y) for y in yb])
assert abs((kb.max() - kb.min()) - 40) > 1 and not np.any(np.abs(yb[0] - 3 * xs) < 1e-9)
abl2('좌변의 +72x-144', f"필요(없으면 좌변이 f'(3x)가 아니어서 g(x)가 x의 일차식으로 정해지지 않고 k의 범위가 [{kb.min():.1f}, {kb.max():.1f}]으로 바뀜)")
# (c) 함수의 일차항 계수 18 → 15(LIVE212 의 함수): 좌변이 f'(3x) 와 어긋남
h15 = x**3 - 6 * x**2 + 15 * x
assert sp.expand(9 * sp.diff(h15, x) + 72 * x - 144 - sp.diff(h15, x).subs(x, 3 * x)) != 0
abl2('f(x)의 18x', "필요(15x이면 9f'(x)+72x-144가 f'(3x)가 아니게 됨: 함수와 보정항이 한 세트)")
# (d) (3)에서 한 갈래 빼기: 26 또는 28
abl2('두 갈래 g=3x, g=4-3x', '필요(g=3x만이면 26, g=4-3x만이면 28)')
# (e) 실수 k(상수항): 묻는 대상
abl2('실수 k', '필요((2), (3)이 묻는 대상)')

print('ALL OK')
