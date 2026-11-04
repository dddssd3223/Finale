# -*- coding: utf-8 -*-
# p17.py (견본4 17번 Claude 후보 claude17) 검증
# 원문 M27 풀이(36) · 변형 정답 유일성(b 전수) · 경계 포함/제외 · 선지 등차 · 오답 근거 값 · 조건 빼 보기 · 길이
import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy import Rational, sqrt, Poly, real_roots

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p17.py')).read(), ns)
IT = ns['ITEMS']; P = IT[17]
assert list(IT) == [17] and P['author'] == 'claude' and P['cand'] == 'claude17' and P['key'] == 'M27'
assert len(P['cond']) == 2 and [c[0] for c in P['cond']] == ['가', '나']
assert P['core']['axis'] == '①' and all(P['core'][k] for k in ('setting', 'principle', 'new'))
x = sp.symbols('x', real=True)

# ---------- 교점 개수: 일반 다항식 f에 대하여 곡선 y=|f(x)|와 직선 y=kx+h (정확 계산) ----------
def meet(fpoly, k, h=0):
    """|f(x)| = kx + h 의 서로 다른 실근 개수 (f: x에 대한 sympy 다항식, 유리 계수)"""
    pts = []
    for s in (1, -1):
        g = Poly(sp.expand(s * fpoly - k * x - h), x)
        if g.is_zero:
            raise ValueError('일치')
        for r in real_roots(g):
            if sp.N(k * r + h, 60) >= -sp.Float('1e-50'):
                v = sp.N(r, 60)
                if all(abs(v - w) > sp.Float('1e-40') for w in pts):
                    pts.append(v)
    return len(pts)

# 홀함수 f=2x^3+bx 전용 빠른 정확 계산 (해가 0, ±sqrt((k-b)/2), ±sqrt((-k-b)/2) 뿐)
def meet_odd(b, k):
    b, k = Rational(b), Rational(k)
    cand = {Rational(0)}
    for q in ((k - b) / 2, (-k - b) / 2):
        if q > 0:
            cand |= {sqrt(q), -sqrt(q)}
    return sum(1 for r in cand if k * r >= 0)   # |f(r)| = kr 이려면 kr >= 0

KR = range(-60, 61)   # |b| <= 16 이면 |k| > |b| 에서 교점은 2개 이하(아래에서 확인) → 충분
def count3(b):
    return sum(1 for k in KR if meet_odd(b, k) == 3)

# ===== 원문 M27: f=2x^3+cx, y=|f(x)|와 y=-f(1)이 서로 다른 네 점 → c=-6, f(3)=36 =====
grid_c = [Rational(n, 4) for n in range(-80, 17)]
four = []
for c in grid_c:
    f = 2 * x**3 + c * x; h = -(2 + c)
    if meet(f, 0, h) == 4:
        four.append(c)
assert four == [-6], four
assert (2 * x**3 - 6 * x).subs(x, 3) == 36
# 원문 원리 줄 확인: c=-6에서 -f(1)=4 = 극댓값, x=1은 극소점
f6 = 2 * x**3 - 6 * x
assert sp.diff(f6, x).subs(x, 1) == 0 and sp.diff(f6, x, 2).subs(x, 1) > 0 and -f6.subs(x, 1) == f6.subs(x, -1) == 4
print('원문 M27: 네 점이 되는 c는', four, '→ f(3)=36 OK')

# ===== 홀함수 빠른 계산 = 일반 계산 (교차 확인) =====
for b in [Rational(n, 2) for n in range(-16, 9)]:
    for k in range(-12, 13):
        assert meet_odd(b, k) == meet(2 * x**3 + b * x, k), (b, k)
print('교점 개수 두 방법 일치 OK')

# ===== 판정 표: b<0이면 |k|<-b ⇔ 세 점, |k|>=-b ⇔ 두 점 / b>=0이면 세 점 없음 =====
for b in [Rational(n, 4) for n in range(-64, 25)]:
    for k in KR:
        n = meet_odd(b, k)
        if b < 0:
            assert n == (3 if abs(k) < -b else 2), (b, k, n)
        else:
            assert n <= 2, (b, k, n)
# 경계 함정: b=-3, k=±3은 원점에서 봉우리에 접해 두 점
assert meet_odd(-3, 3) == meet_odd(-3, -3) == 2 and meet_odd(-3, 2) == 3 and meet_odd(-3, 0) == 3
print('판정 표 OK (경계 |k|=-b는 두 점)')

# ===== 정답 유일성: b 전수 (1/16 간격 + 경계 근방) =====
grid_b = sorted(set([Rational(n, 16) for n in range(-256, 97)] +
                    [Rational(-3), Rational(-2), Rational(-3) - Rational(1, 1000), Rational(-2) - Rational(1, 1000),
                     Rational(-2) + Rational(1, 1000), Rational(-3) + Rational(1, 1000)]))
S = [b for b in grid_b if count3(b) == 5]
assert all(-3 <= b < -2 for b in S) and Rational(-3) in S and Rational(-2) not in S
assert Rational(-3) - Rational(1, 1000) not in S and Rational(-2) - Rational(1, 1000) in S
assert S == [b for b in grid_b if -3 <= b < -2]
F3 = lambda b: 54 + 3 * b
ans_val = min(F3(b) for b in S)
assert ans_val == 45 and min(S) == -3
ch = [Fr(c) for c in P['choices']]
assert len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1
assert P['ans'] == 2 and ch[P['ans'] - 1] == ans_val
print(f'정답: (나)를 만족시키는 b = [-3, -2) → f(3) 최솟값 {ans_val} (b=-3, f=2x^3-3x), 선지 ② OK')

# ===== 오답 근거 값 (각 착오 규칙으로 같은 전수 조사) =====
def wrong_set(rule):
    out = []
    for b in grid_b:
        if b >= 0: continue
        m = -b
        if sum(1 for k in KR if rule(k, m)) == 5:
            out.append(b)
    return out
W = {}
s1 = wrong_set(lambda k, m: abs(k) <= m)          # 접하는 경계도 세 점으로 봄
assert s1 == [b for b in grid_b if -3 < b <= -2]; W['①'] = F3(max(s1))      # 포함되는 끝 b=-2
s3 = wrong_set(lambda k, m: 0 <= k <= m)          # 음수 k 누락 + 경계 포함
assert s3 == [b for b in grid_b if -5 < b <= -4]; W['③'] = F3(max(s3))      # b=-4
s4 = wrong_set(lambda k, m: 0 <= k < m)           # 음수 k 누락
assert s4 == [b for b in grid_b if -5 <= b < -4]; W['④'] = F3(min(s4))      # b=-5
s5 = wrong_set(lambda k, m: 1 <= k < m)           # 음수 k, k=0 누락
assert s5 == [b for b in grid_b if -6 <= b < -5]; W['⑤'] = F3(min(s5))      # b=-6 (원문 함수)
assert W == {'①': 48, '③': 42, '④': 39, '⑤': 36}, W
pos = dict(zip('①②③④⑤', ch))
for kk, v in W.items():
    assert pos[kk] == v and v != ans_val and f'{kk} \\({v}\\)' in P['wrong']
print('오답 근거 값', W, 'OK')

# ===== 조건 빼 보기 =====
# (가) 빼기: 최고차항의 계수 2인 삼차함수 일반. f=2x^3-4x^2-2x도 (나)를 만족시키고 f(3)=12 < 45
fg = 2 * x**3 - 4 * x**2 - 2 * x
cg = sum(1 for k in range(-40, 41) if meet(fg, k) == 3)
assert cg == 5 and fg.subs(x, 3) == 12 and all(meet(fg, k) <= 2 for k in list(range(-60, -40)) + list(range(41, 61)))
print('ABLATION 17 (가): 필요(빼면 f(x)=2x^3-4x^2-2x도 (나)를 만족시켜 f(3)=12<45 → 최솟값 45가 아님)')
# (나) 빼기: f=2x^3+bx 모두 가능 → f(3)=54+3b 아래로 유계 아님
assert F3(-100) == -246 and F3(-1000) < -2000
print('ABLATION 17 (나): 필요(빼면 b가 임의여서 f(3)=54+3b의 최솟값이 없음)')

# ===== 길이: 원문 이상 (태그·공백 제거) =====
sys.path.insert(0, '/home/user/Finale/template/db/parts'); sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
from items_common import COND
import items_final as F
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', t))
L_new = len(plain(P['body'] + COND(P['cond']))); L_org = len(plain(F.I['M27'][0]))
assert L_org == 132 and L_new >= L_org, (L_new, L_org)
assert F.I['M27'][2] == '②' and F.I['M27'][1][1] == '36'
print(f'길이: 변형 {L_new}자 >= 원문 {L_org}자 OK')
print('ALL OK')
