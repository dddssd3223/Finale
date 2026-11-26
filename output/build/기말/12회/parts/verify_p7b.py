# -*- coding: utf-8 -*-
# 12회 서답형2 (I74 후보_순위 2 학교식, 답만 3단계) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a = sp.symbols('x a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7b.py')).read(), ns)
S2 = ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def pieces(c, m, p, q=None, av=a, lift=0):
    """h'=g-f 조각 목록 [(식, 왼끝, 오른끝)]. f=-c x^2 (x<0), m x(x-q) (x≥0); g=a(x+p)/0/a(x-p) (+lift)"""
    q = p if q is None else q
    fl, fr = -c * x**2, m * x * (x - q)
    return [(av * (x + p) + lift - fl, -sp.oo, -p), (lift - fl, -p, 0), (lift - fr, 0, p), (av * (x - p) + lift - fr, p, sp.oo)]


def sgn_at(P, v):
    for e, lo, hi in P:
        if lo <= v < hi or (lo == -sp.oo and v < hi): return sp.sign(e.subs(x, v))


def extrema(P):
    """h'의 부호가 바뀌는 점 [(x, '극대'|'극소')] — 조각별 근·이음점을 후보로 두고 사이 구간 부호를 직접 봄"""
    cand = set()
    for e, lo, hi in P:
        if lo != -sp.oo: cand.add(sp.nsimplify(lo))
        for r in sp.Poly(sp.expand(e), x).real_roots():
            if (lo == -sp.oo or r >= lo) and r < hi: cand.add(r)
    cs = sorted(cand, key=lambda v: float(v))
    pts = [cs[0] - 1] + [(u + v) / 2 for u, v in zip(cs, cs[1:])] + [cs[-1] + 1]
    sg = [sgn_at(P, v) for v in pts]
    assert 0 not in sg
    return [(c_, '극대' if s1 > 0 else '극소') for c_, s1, s2 in zip(cs, sg, sg[1:]) if s1 != s2]


def hval(P, X):
    tot = 0
    for e, lo, hi in P:
        l, u = max(lo, 0), min(hi, X)
        if l < u: tot += sp.integrate(e, (x, l, u))
    return sp.nsimplify(tot)


def kmax(c, m, p, q=None, lift=0, grid=None):
    """극값이 오직 하나인 a의 최댓값: 격자 전수 + 경계 양옆 확인"""
    grid = grid or [R(i, 4) for i in range(1, 161)]
    ok = [av for av in grid if len(extrema(pieces(c, m, p, q, av, lift))) == 1]
    kv = max(ok)
    assert ok == [av for av in grid if av <= kv]                       # 0<a≤k 전체가 '하나'
    assert len(extrema(pieces(c, m, p, q, kv + R(1, 100), lift))) == 3
    return kv


# --- 원문 I74: k=4, h(3)=7/2, k+h(3)=15/2 (④)
ko = kmax(1, 1, 1); Po = pieces(1, 1, 1, av=ko)
assert ko == 4 and hval(Po, 3) == R(7, 2) and ko + hval(Po, 3) == R(15, 2)
assert F.I['I74'][2] == '④' and F.I['I74'][1][3] == r'\dfrac{15}2'
print('I74 원문 OK: k=4, h(3)=7/2, k+h(3)=15/2 (원문 정답 ④)')
# --- DB 학교식_예상 1 스케치(k=8, h(4)=32/3)·예상 2(14/3)와 우리 문항 수치가 다름
kd = kmax(1, 1, 2); assert kd == 8 and hval(pieces(1, 1, 2, av=8), 4) == R(32, 3)
assert hval(Po, 4) == R(14, 3)

# --- S2 본문 수치 확인
B = S2['body']
for w in (r"-\dfrac32x^2 & (x&lt;0)", r"3x^2-6x & (x\ge0)", r"ax+2a & (x&lt;-2)", r"0 & (-2\le x&lt;2)", r"ax-2a & (x\ge2)",
          r"\int_0^x\{g(t)-f(t)\}\,dt", r"양수 \(a\)"): assert w in B, w
assert 'cond' not in S2 and '<' not in re.sub(r'<br>', '', B)
c, m, p = R(3, 2), 3, 2
# f, g 연속 / f의 양의 근 = g의 꺾이는 점 (숨은 관계)
assert (m * x * (x - p)).subs(x, p) == 0 and (-c * x**2).subs(x, 0) == (m * x * (x - p)).subs(x, 0) == 0
assert sp.factor(pieces(c, m, p)[3][0]) == sp.factor((x - 2) * (a - 3 * x))

# (1) a=3
P1 = pieces(c, m, p, av=3); E1 = extrema(P1)
assert E1 == [(2, '극대')], E1
A1 = hval(P1, 2); assert A1 == 4
# (2) k
k = kmax(c, m, p); assert k == 12
assert sp.discriminant(c * x**2 + a * x + 2 * a, x) == a**2 - 12 * a
assert sp.factor((c * x**2 + a * x + 2 * a).subs(a, 12)) == sp.factor(R(3, 2) * (x + 4)**2)
# 일반 a: 오른쪽(x≥-2)은 늘 하나 — 극대 위치가 a≤6이면 2, a>6이면 a/3
for av in [R(i, 4) for i in range(1, 161)]:
    E = [e for e in extrema(pieces(c, m, p, av=av)) if e[0] >= -2]
    assert E == [(2 if av <= 6 else av / 3, '극대')], (av, E)
# a>12: 극값 3개(왼쪽 두 근 모두 -2보다 작음)
for av in (R(49, 4), 13, 20, 40):
    E = extrema(pieces(c, m, p, av=av)); assert len(E) == 3 and E[0][0] < E[1][0] < -2 and [e[1] for e in E] == ['극대', '극소', '극대']
# (3) a=k
P3 = pieces(c, m, p, av=k); E3 = extrema(P3)
assert E3 == [(4, '극대')], E3
A3 = hval(P3, 4); assert A3 == 8
assert S2['ans'] == [r'(1) \(4\)', r'(2) \(12\)', r'(3) \(8\)']
print('S2 OK: (1) 극대 x=2, 4 (2) k=12 (a 격자 0.25 간격 전수, 0<a≤12만 극값 하나) (3) 극대 x=4, 8')

# --- 정답이 본문 수와 같지 않음
txt = S2['body'] + ''.join(q[0] for q in S2['subs'])
nums = set(re.findall(r'\d+', txt.replace(r'\dfrac32', '3 2')))
for v in ('4', '12', '8'): assert v not in nums, (v, nums)

# --- 오답 값
assert hval(P1, 1) == 2 and hval(P1, 3) == R(3, 2)                 # (1) x=1 / x=a=3
assert kmax(1, 3, 2) == 8 and ko == 4                               # (2) 계수 3/2 누락 / 원문 답
assert [av for av in [R(i, 4) for i in range(1, 161)] if extrema(pieces(c, m, p, av=av)) == [(2, '극대')]][-1] == 6   # (2) x=2에서만
assert hval(P3, 2) == 4 and hval(P3, 3) == 6 and hval(P3, 12) == -696      # (3)
assert sp.integrate(3 * (x - 2) * (4 - x), (x, 2, 4)) == 4
for w in (r'h(1)=2\)', r'h(3)=\dfrac32\)', r'\(k=4\)', r'\(k=8\)', r'\(k=6\)', r'극대로 보아 \(4\)', r'멈추어 \(6\)', r'빠뜨려 \(4\)', r'h(12)=-696\)'):
    assert w in S2['wrong'], w

# --- 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['3점, 답만 적으시오.', '4점, 답만 적으시오.', '3점, 답만 적으시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', l)] for l in S2['rubric'][:3]]
assert pts == [[3], [4], [3]] and sum(map(sum, pts)) == 10
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:])) and all('채점자 참고용' in l for l in S2['rubric'][:3])
assert S2['db_ref'] == 'I74 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
assert '이러한' not in txt and '이와 같은' not in txt and txt.count('다음') == 0
allt = ' '.join([S2['body'], S2['fast'], S2['wrong'], S2['note'], S2['var']] + S2['rubric'] + S2['sol'] + [q[0] for q in S2['subs']] + list(S2['core'].values()))
assert not re.search(r'<(?!br>)', allt), '맨 < 있음'

# --- 인쇄 N제 I74 547–555와 다름 (N제 본문에 우리 f의 조각이 없음)
nz = open('/home/user/Finale/output/N제/미적분1_기말_N제_06_부정적분과정적분.md').read()
sec = nz[nz.index('## I74 (부교재'):nz.index('## I75', nz.index('## I74 (부교재'))]
assert '3x^2-6x' not in sec and r'\dfrac32x^2' not in sec and r'\frac32x^2' not in sec

# --- 조건 빼 보기
def abl(cn, msg): print(f'ABLATION S2 {cn}: {msg}')
# f의 왼쪽 조각 계수(-3/2 x^2): 바꾸면 k가 달라짐, (1)은 그대로
assert kmax(1, 3, 2) == 8 and kmax(3, 3, 2) == 24 and hval(pieces(1, 3, 2, av=3), 2) == 4
abl('f의 왼쪽 조각 -(3/2)x^2', '필요(계수를 1로 하면 k=8, 3으로 하면 k=24로 (2)·(3)이 바뀜; (1)에는 쓰이지 않음)')
# f의 오른쪽 조각(3x^2-6x): 바꾸면 (1)(3) 값과 극대 위치가 달라짐, k는 그대로
Pq = pieces(c, 1, p, av=3); assert extrema(Pq) == [(3, '극대')] and hval(Pq, 3) != 4
assert kmax(c, 1, p) == 12 and extrema(pieces(c, 1, p, av=12))[0][0] == 12
abl('f의 오른쪽 조각 3x^2-6x', '필요(x^2-2x로 바꾸면 a=3일 때 극대가 x=3으로, a=k일 때 x=12로 옮겨 (1)·(3)이 바뀜; (2)에는 x≥-2에서 극값이 늘 하나라는 판단으로 쓰임)')
# f의 오른쪽 근을 꺾이는 점과 어긋나게(q=1, 3x^2-3x): 극대가 x=1로 옮겨 (1)(3) 값이 바뀜
Pz1, Pz3 = pieces(c, 3, 2, 1, 3), pieces(c, 3, 2, 1, 12)
assert extrema(Pz1) == [(1, '극대')] == extrema(Pz3) and hval(Pz1, 1) == R(1, 2) == hval(Pz3, 1)
abl('f의 양의 근 2(= g의 꺾이는 점)', '필요(근을 1로 두면 극대가 x=1로 옮겨 (1)·(3)이 모두 1/2로 바뀜)')
# g의 꺾이는 점 ±2: ±1로 하면 (f 근도 1) k=6
assert kmax(c, 3, 1) == 6
abl('g의 꺾이는 점 ±2', '필요(±1로 옮기면 k=6으로 바뀜)')
# g의 가운데 0: 올리면(lift=3) k가 달라짐
assert len(extrema(pieces(c, m, p, av=13, lift=3))) == 1 and len(extrema(pieces(c, m, p, av=13))) == 3
abl('g의 가운데 조각 0', '필요(세 조각을 3만큼 올리면 a=13에서도 극값이 하나라 k가 12보다 커짐)')
# h의 아래끝 0: 다른 값이면 (1)(3) 극댓값이 달라짐 (k는 그대로)
assert sp.integrate(P1[2][0], (x, 1, 2)) == 2 != 4
abl('h의 아래끝 0', '필요(아래끝을 1로 하면 (1)의 극댓값이 2로 바뀜)')
# (1)의 a=3: a=9면 극대가 x=3
assert extrema(pieces(c, m, p, av=9)) == [(3, '극대')] and hval(pieces(c, m, p, av=9), 3) != 4
abl('(1)의 a=3', '필요(a=9이면 극대인 점이 x=3으로 옮겨 값이 바뀜)')
# '오직 하나': 3개로 바꾸면 최댓값 없음
abl("(2)의 '오직 하나의 극값'", '필요(없으면 k가 정해지지 않음; a>12이면 극값 3개)')
# '양수 a': a≤0에서도 극값은 하나 → k 그대로 (원문 단서)
assert all(len(extrema(pieces(c, m, p, av=av))) == 1 for av in (0, -1, R(-7, 2), -20))
abl('양수 a', '원문 단서 그대로(a≤0이어도 극값은 하나라 답은 그대로; g의 매개변수 범위를 정하는 원문 표현이라 둠)')
print('ALL OK')
