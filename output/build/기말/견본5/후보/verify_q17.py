# -*- coding: utf-8 -*-
# q17.py (견본5 17번 Claude 후보 B, claudeB17) 검증
# 원문 I37 풀이(-3) · (가) → f 유일 · (나) ⇔ a>=2 (경계 포함) · 정답 4 · 선지 등차 · 오답 근거 값 · 조건 빼 보기 · 원문 원리 줄 불통 · 길이
import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy import Rational as Q

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'q17.py')).read(), ns)
IT = ns['ITEMS']; P = IT[17]
assert list(IT) == [17] and P['author'] == 'claude' and P['cand'] == 'claudeB17' and P['key'] == 'I37'
assert [c[0] for c in P['cond']] == ['가', '나'] and P['core']['axis'] == '①'
assert all(P['core'][k] for k in ('setting', 'principle', 'new'))
x = sp.symbols('x', real=True)

def absint(p, l, u):
    """∫_l^u |p(x)| dx (정확값, l<=u)"""
    p = sp.expand(p)
    if p == 0: return Q(0)
    rs = sorted(set(r for r in sp.real_roots(sp.Poly(p, x)) if l < r < u))
    pts = [l] + rs + [u]
    return sp.nsimplify(sum(abs(sp.integrate(p, (x, pts[i], pts[i + 1]))) for i in range(len(pts) - 1)))
def I(p, l, u): return sp.integrate(sp.expand(p), (x, l, u))

def condA(f, a): return sp.simplify(absint(f, 0, a) - (I(f, 0, 1) - I(f, 1, a))) == 0
def condB(f, a):
    g = sp.expand(f + f.subs(x, a - x))
    return sp.simplify(absint(g, 0, a) - abs(I(g, 0, a))) == 0

f0 = -4 * x * (x - 1)
A_grid = sorted(set([Q(n, 8) for n in range(9, 41)] + [Q(2) - Q(1, 1000), Q(2) + Q(1, 1000), Q(3, 2), Q(5, 4)]))

# ===== 원문 I37: f=-4x(x-1), (나) |∫_0^a f| <= ∫_{1-a}^1 f ⇔ a<=3/2, f(a) 최솟값 -3 =====
sys.path.insert(0, '/home/user/Finale/template/db/parts'); sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
from items_common import COND
import items_final as F
org = [a for a in A_grid if abs(I(f0, 0, a)) <= I(f0, 1 - a, 1)]
assert org == [a for a in A_grid if a <= Q(3, 2)] and Q(3, 2) in org
assert f0.subs(x, Q(3, 2)) == -3 and F.I['I37'][2] == '②' and F.I['I37'][1][1] == '-3'
print('원문 I37: (나) ⇔ 1<a<=3/2, f(a) 최솟값 -3 (선지 ②) OK')

# ===== (가) → f(x)=-4x(x-1) 유일 (f(0)=0, 계수 ±4, 일차항 b 전수) =====
b = sp.symbols('b', real=True)
sols = []
for s in (4, -4):
    for bv in [Q(n, 4) for n in range(-24, 25)]:
        f = s * x**2 + bv * x
        if any(condA(f, a) for a in [Q(9, 8), Q(3, 2), Q(2), Q(5, 2), Q(3)]):
            sols.append(f)
assert sols == [sp.expand(f0)], sols
print('(가)를 만족시키는 f는 -4x^2+4x 뿐 OK (모든 a>1에서 성립:', all(condA(f0, a) for a in A_grid), ')')
assert all(condA(f0, a) for a in A_grid)

# ===== (나) ⇔ a>=2 (a=2 포함, 2-0.001 제외) =====
S = [a for a in A_grid if condB(f0, a)]
assert S == [a for a in A_grid if a >= 2], S
assert Q(2) in S and Q(2) - Q(1, 1000) not in S
g2 = sp.expand(f0 + f0.subs(x, 2 - x)); assert sp.factor(g2) == -8 * (x - 1)**2
gA = sp.expand(f0 + f0.subs(x, sp.Symbol('a') - x))
av = sp.Symbol('a'); assert sp.simplify(gA.subs(x, av / 2) - 2 * f0.subs(x, av / 2)) == 0
print('(나) ⇔ a>=2 (a=2에서 g=-8(x-1)^2 접함, 꼭짓점 값 2f(a/2)) OK')

# 판정 원리 직접 확인: 연속 범위에서 꼭짓점 값 부호
assert sp.solve(sp.Eq(2 * f0.subs(x, av / 2), 0), av) == [0, 2]

# ===== 정답: G(a)=∫_0^a|f| 는 a에 대하여 증가 → 최솟값 G(2)=4 =====
G = lambda a: absint(f0, 0, a)
Ga = sp.expand(Q(2, 3) - I(f0, 1, av))
assert sp.diff(Ga, av).subs(av, 2) > 0 and all(sp.diff(Ga, av).subs(av, t) > 0 for t in [Q(n, 4) for n in range(5, 41)])
ans_val = min(G(a) for a in S)
assert ans_val == 4 == G(Q(2))
ch = [Fr(str(sp.nsimplify(c.replace(r'\dfrac', '').replace('}{', '/').replace('{', '').replace('}', ''))))
      if 'frac' not in c else None for c in P['choices']]
def cv(c):
    m = re.fullmatch(r'\\dfrac\{?(\d+)\}?\{?(\d+)\}?', c)
    return Fr(int(m[1]), int(m[2])) if m else Fr(int(c))
ch = [cv(c) for c in P['choices']]
assert len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1
assert P['ans'] == 4 and ch[P['ans'] - 1] == ans_val
print('정답:', ans_val, '(a=2), 선지', [str(c) for c in ch], '등차, ④ OK')

# ===== 오답 근거 값 =====
Pp, Nn, Fs = I(f0, 0, 1), absint(f0, 1, 2), I(f0, 0, 2)
W = {'①': Nn - 2 * Pp,          # [0,1] 넓이를 빼서 계산
     '②': abs(Fs),              # 넓이 대신 |∫_0^2 f| (부호 상쇄)
     '③': Nn,                   # [1,2] 부분만 (경우 누락)
     '⑤': Nn + 2 * Pp}          # |∫f| 대신 ∫_1^2|f| 를 넣음
assert W == {'①': 2, '②': Q(8, 3), '③': Q(10, 3), '⑤': Q(14, 3)}, W
pos = dict(zip('①②③④⑤', ch))
for kk, v in W.items():
    assert pos[kk] == Fr(str(v)) and v != ans_val and kk in P['wrong']
print('오답 근거 값', {k: str(v) for k, v in W.items()}, 'OK')

# ===== 원문 원리 줄 불통: 원문 판정(∫_0^a f>=0, a<=3/2)은 (나)의 해집합과 겹치지 않음 =====
assert not any(a in S for a in org)
print('원문 원리 줄(∫_0^a f>=0 ⇔ a<=3/2)로 얻는 a는 (나)를 하나도 만족시키지 않음 → 불통 OK')

# ===== 조건 빼 보기 =====
# (가) 빼기: f=-4x(x-2)도 (나)를 만족시키는 a가 있고(a>=4) 최솟값 ∫_0^4|f|=32 → 답이 달라짐. f=-4x(x-1/2)이면 a>=1(경계 a=1 제외) → 최솟값 없음
f1 = -4 * x * (x - 2)
S1 = [a for a in [Q(n, 4) for n in range(5, 25)] if condB(f1, a)]
assert S1 == [a for a in [Q(n, 4) for n in range(5, 25)] if a <= 2 or a >= 4], S1   # g(0)=f(a)>0인 1<a<=2도 부호 일정
assert all(condB(f1, a) for a in [Q(1001, 1000), Q(101, 100)]) and sp.limit(sp.expand(-I(f1, 0, av)), av, 1, '+') == -Q(8, 3)  # 1<a<=2: ∫|f1|=∫f1 → 8/3 아래로 다가갈 뿐
f2 = -4 * x * (2 * x - 1) / 2
assert all(condB(f2, a) for a in [Q(1001, 1000), Q(9, 8), Q(2)])
print('ABLATION 17 (가): 필요(빼면 f(x)=-4x(x-2)도 가능하여 1<a<=2에서 ∫_0^a|f|가 8/3에 가까워질 뿐 최솟값 없음, f(x)=-4x(x-1/2)이면 a→1에서 최솟값 없음 → 답 4가 아님)')
# (나) 빼기: 모든 a>1 가능 → G(a)>2/3, a→1+에서 2/3에 가까워질 뿐 최솟값 없음
assert all(condA(f0, a) for a in [Q(1001, 1000), Q(101, 100)]) and G(Q(1001, 1000)) < 4 and G(Q(1001, 1000)) > Q(2, 3)
assert sp.limit(Ga, av, 1, '+') == Q(2, 3)
print('ABLATION 17 (나): 필요(빼면 1<a 모두 가능하여 ∫_0^a|f|의 최솟값이 없음, 하한 2/3은 a=1에서만)')

# ===== 길이: 원문 이상 =====
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', t))
L_new = len(plain(P['body'] + COND(P['cond']))); L_org = len(plain(F.I['I37'][0]))
assert L_org == 265 and L_new >= L_org, (L_new, L_org)
print(f'길이: 변형 {L_new}자 >= 원문 {L_org}자 OK')
print('ALL OK')
