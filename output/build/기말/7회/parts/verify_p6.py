# -*- coding: utf-8 -*-
# A18 3판(수치 한 세트 교체) (7회 18번 후보, 원문 J44, db_ref 'J44 킬러 설계A') 검증
# 원문 풀이(57/2) · 변형의 세 경우 전수(거리 범위가 겹치지 않고 이어짐, 유일해) · 최댓값 27인 a 격자 전수(정의대로)
# · 정답 = ① · 선지 등차 · 오답(폭 전체로 세운 값이 선지에 있음) · 조건 빼 보기 · 원문 원리 줄 시험 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
t, a, b, h, T, C = sp.symbols('t a b h T C', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'J44' and it['ans'] == 3 and it['db_ref'] == 'J44 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'cond' not in it                                              # 분담표: 상자 ×
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
full = it['body']
assert 'v_1(t)=2t+13' in full and 'v_2(t)=-3t^2+at+b' in full and r'최댓값은 \(27\)' in full and r'거리가 \(90\)' in full and r'\(t=6\)까지' in full
assert 'g(t)' not in full and '개수' not in full and 'int' not in full  # 개수 세기·정적분 조건 없음
for k in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):               # 수식 안 맨 부등호 없음
    assert not re.search(r'\\\([^)]*?[<>]', it[k]), k
CH = [sp.Integer(v) for v in it['choices']]
v1 = 2*t + 13
MAXV, DIST, T0, W = 27, 90, 6, 3

# ---------- 원문 J44 ----------
v1o = 3*t**2 + 1
v2o = sp.integrate(1 - 2*t, t) + C
Ts = [r for r in sp.solve(sp.Eq(sp.integrate(v1o, (t, 0, T)), 10), T) if r.is_real]
assert Ts == [2]
Co = sp.solve(v2o.subs(t, 2), C)[0]; assert Co == 2
assert sp.integrate(v1o, (t, 0, 1)) == 2                       # C<=0이면 시간이 [0,1] 안 → 거리 <= 2 < 10
do = sp.integrate(v1o, (t, 0, 3)) - sp.integrate(v2o.subs(C, Co), (t, 0, 3))
assert do == R(57, 2) and F.I['J44'][2] == '④' and F.I['J44'][1][3] == '\\dfrac{57}2'
print('원문 J44: v2=-t^2+t+C, C>0, T^3+T=10 → T=2, C=2, t=3에서 거리 57/2 = ④ OK')

# ---------- 변형: 속도가 0 이상인 시간과 P의 거리 (정의대로) ----------
def window(av, bv, clip=True):
    """v2=-3t^2+at+b >= 0 인 시간 [lo, hi] (clip: t>=0 로 자름, 없으면 None)"""
    disc = av**2 + 12*bv
    if disc < 0: return None
    r1, r2 = (av - sp.sqrt(disc))/6, (av + sp.sqrt(disc))/6
    if clip and r2 < 0: return None
    return (sp.Max(r1, 0) if clip else r1, r2)
def pdist(w):
    return sp.integrate(v1, (t, w[0], w[1]))      # t>=0 에서 v1>0 이므로 움직인 거리 = 위치 변화량
def b_from_max(av):
    return sp.Integer(MAXV) if av <= 0 else MAXV - sp.nsimplify(av)**2/12
assert sp.expand(-3*(t - a/6)**2 + b + a**2/12 - (-3*t**2 + a*t + b)) == 0

# 경우 (i) a<=0: b=75, 시간 [0, T], T<=5, 거리 <= 85/2
Ti = (a + sp.sqrt(a**2 + 12*MAXV))/6
assert sp.simplify((-3*t**2 + a*t + MAXV).subs(t, Ti)) == 0 and Ti.subs(a, 0) == W
assert (-3*t**2 + a*t + MAXV).subs(t, W) == 3*a and all(Ti.subs(a, -k) < W for k in (R(1, 10), 1, 5, 100))
Pm = sp.integrate(v1, (t, 0, T)); assert sp.expand(Pm - (T**2 + 13*T)) == 0 and Pm.subs(T, W) == 48
# 경우 (ii-1) 0<h<5: 시간 [0, h+5], 거리 T^2/2+6T (85/2 < 거리 < 110)
assert Pm.subs(T, 2*W) == 114
# 경우 (ii-2) h>=5: 시간 [h-5, h+5], 거리 10h+60 >= 110
D3 = sp.expand(sp.integrate(v1, (t, h - W, h + W))); assert D3 == 12*h + 78 and D3.subs(h, W) == 114
# 세 경우의 거리 범위 (0, 85/2], (85/2, 110), [110, ∞) 가 겹치지 않고 각 구간에서 증가 → 80 은 (ii-1)에서만
assert 48 < DIST < 114
Tsol = [r for r in sp.solve(sp.Eq(Pm, DIST), T) if W < r < 2*W]; assert Tsol == [5]
h0 = Tsol[0] - W; a0 = 6*h0; b0 = MAXV - a0**2/12
assert (h0, a0, b0) == (2, 12, 15)
v2 = -3*t**2 + a0*t + b0
assert sp.expand(v2 + 3*(t - 5)*(t + 1)) == 0
# 폭 전체로 세운 식: 10h+60=80 → h=2 (<5 이므로 h-5<0, 버려야 함)
hn = sp.solve(sp.Eq(D3, DIST), h); assert hn == [1] and hn[0] < W
an, bn = 6*hn[0], MAXV - 3*hn[0]**2
v2n = -3*t**2 + an*t + bn
assert (an, bn) == (6, 24) and sp.expand(v2n + 3*(t - 4)*(t + 2)) == 0
assert pdist(window(an, bn)) == 68 != DIST                      # 실제로는 [0, 4] 라 거리 68
print('변형: 세 경우(a<=0 / 0<h<3 / h>=3)의 거리 범위가 48, 114 에서 이어지고 해는 (ii-1)에서 하나; 폭 전체로 세운 정수 해는 무효 OK')

# 최댓값 27 인 a 격자 수치 전수: a=-30..60(1/8 간격)에서 P의 거리를 정의대로 계산
hits, prev = [], None
for k in range(-240, 481):
    av = R(k, 8); bv = b_from_max(av)
    w = window(av, bv); assert w is not None
    d = sp.nsimplify(pdist(w))
    if prev is not None: assert d > prev, av          # 증가
    prev = d
    if d == DIST: hits.append(av)
assert hits == [12]
print('전수: 최댓값 27 인 a=-30..60(1/8 간격) 721개에서 거리가 a에 대해 증가, 조건의 거리가 되는 a 는 하나뿐 OK')

# ---------- 정답 ----------
def moved(vexpr, t0, t1):
    zs = sorted({r for r in sp.solve(vexpr, t) if r.is_real and t0 < r < t1})
    cuts = [t0] + zs + [t1]
    return sum(abs(sp.integrate(vexpr, (t, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))
xq = sp.integrate(v2, t)
assert xq.subs(t, 5) == 100 and xq.subs(t, 6) == 90
ans = moved(v2, 0, T0)
assert ans == 110 and CH[it['ans'] - 1] == ans
print('정답: 계산값 = 선지의 정답 자리 OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {7}
w_full = moved(v2n, 0, T0); w_turn = sp.integrate(v2, (t, 0, 5))
xn = sp.integrate(v2n, t); assert xn.subs(t, 4) == 80 and 80 - xn.subs(t, 6) == 44
assert (w_full, w_turn) == (124, 100)
assert sp.Integer(it['wrongs'][0]) == w_full and w_full in CH and w_turn not in CH
assert sp.Integer(it['wrongs'][1]) == 2*ans - w_full      # 둘째 오답은 계산 경로 없는 값(정답 기준 대칭 자리) — note 에 적음
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert ans != R(57, 2) and all(str(ans) != n for n in re.findall(r'\d+', full))
print('선지 등차(공차 7, 오름차순), 폭 전체로 세운 값이 선지 안, 정답은 원문 답·문제 속 수와 다름 OK')

# ---------- 조건 빼 보기 ----------
def answer_for(av, bv): return sp.nsimplify(moved(-3*t**2 + av*t + bv, 0, T0))
# (1) '최댓값 27' 없음: 거리 90 만으로는 (a, b)가 한 줄로 남는다 — v2=-3(t-p)(t-q), 시간 [max(p,0), q] 에서 P 거리 90
alt1 = {}
for pv in (-1, 0, 1):
    lo = max(pv, 0)
    qv = [r for r in sp.solve(sp.Eq(sp.integrate(v1, (t, lo, T)), DIST), T) if r > lo][0]
    av, bv = 3*(pv + qv), -3*pv*qv
    assert sp.simplify(pdist(window(av, bv)) - DIST) == 0
    alt1[str(pv)] = round(float(answer_for(av, bv)), 3)
assert alt1['-1'] == 110.0 and len(set(alt1.values())) == 3
print(f'ABLATION 18 최댓값 27: 필요(정해지지 않음: 빼면 v2 의 작은 근 p=-1, 0, 1 모두 거리 90 을 만족, 답이 {len(set(alt1.values()))}가지로 갈림)')
# (2) '거리 90' 없음: h 자유
alt2 = {str(hv): answer_for(6*hv, MAXV - 3*hv**2) for hv in (2, 1, 3, R(3, 2))}
assert alt2['2'] == 110 and len(set(alt2.values())) >= 3, alt2
print(f'ABLATION 18 거리 90: 필요(정해지지 않음: 빼면 h=2, 1, 3, 3/2 에서 답이 {len(set(alt2.values()))}가지로 갈림)')
# (3) 't>=0'(시간의 범위) 없음: 폭 전체 [h-3, h+3] 이 그대로 시간이 되어 폭 전체로 세운 해가 답이 된다
wfull = window(an, bn, clip=False)
assert wfull == (-2, 4) and sp.integrate(v1, (t, -2, 4)) == DIST and answer_for(an, bn) == 124
print('ABLATION 18 t>=0: 필요(답이 바뀜: 빼면 폭 전체가 그대로 시간이 되어 다른 선지 값)')
# (4) 새 장치 — 미정계수 a 를 원문처럼 수로 고정(v2=-3t^2+18t+b, 미지수 b 하나): 거리 90 만으로 b=48 이 정해져 최댓값 조건이 남는다(원문 꼴)
bs = [r for r in sp.solve((-3*t**2 + 12*t + b).subs(t, 5), b)]; assert bs == [15]
#     a 를 다른 수(12)로 고정하면 [0, 8] 에서 b=96, 최댓값 108 ≠ 75 — 최댓값 조건이 a 를 정한다
b12 = sp.solve((-3*t**2 + 6*t + b).subs(t, 5), b)[0]
assert b12 == 45 and b12 + sp.Integer(6)**2/12 == 48 and answer_for(6, b12) != ans
print('ABLATION 18 미정계수 a(새 장치): 필요(a 를 다른 수로 고정하면 거리 조건에서 정한 b 가 최댓값 조건과 어긋나고 답이 달라짐; 최댓값 조건이 a 를 정함)')

# ---------- 원문 원리 줄 시험 ----------
# 원문 줄: 'C 의 부호로 [0, T] 를 정한다' — 변형에서 [0, T] 인지는 b 의 부호가 아니라 h 와 5 의 대소로 정해진다.
# b>0 이면 [0, T] 꼴인 것은 맞지만(b0>0), 최댓값 조건을 폭 전체로 읽은 h=1 도 b=24>0 이라 부호 판정으로는 걸러지지 않는다.
assert b0 > 0 and bn > 0 and answer_for(an, bn) != ans
print('원문 원리 줄: b 의 부호 판정만으로는 폭 전체로 세운 해(b>0)를 걸러내지 못함(그대로는 끝나지 않음) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['J44'][0])); Lm = len(plain(full))
assert Lm >= 0.9 * Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(full))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['J44'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하, 관문 0.60 미만)')
assert jd <= 0.25
print('ALL OK')
