# -*- coding: utf-8 -*-
# A18 (7회 18번 후보, 원문 J44, db_ref 'J44 킬러 설계A') 검증
# 원문 풀이(57/2) · 변형의 세 경우 전수(거리 함수 D(a)의 식·연속·증가·유일해) · (a, b) 격자 수치 전수 · 정답 = ① · 선지 등차
# · 오답(선지 안, 경로 재현) · 조건 빼 보기(새 장치 포함) · 원문 원리 줄 시험 · 문장 길이 · 원문 골격
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
assert it['cand'] == 'A18' and it['key'] == 'J44' and it['ans'] == 1 and it['db_ref'] == 'J44 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'cond' not in it                                              # 분담표: 상자 ×
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
full = it['body']
assert 'v_1(t)=3t^2+1' in full and 'v_2(t)=-3t^2+at+b' in full and r'최댓값은 \(3\)' in full and r'거리가 \(28\)' in full
assert 'g(t)' not in full and '개수' not in full and 'int' not in full  # 개수 세기·정적분 조건 없음
CH = [sp.Integer(v) for v in it['choices']]
v1 = 3*t**2 + 1
MAXV, DIST = 3, 28

# ---------- 원문 J44 ----------
v2o = sp.integrate(1 - 2*t, t) + C
Ts = [r for r in sp.solve(sp.Eq(sp.integrate(v1, (t, 0, T)), 10), T) if r.is_real]
assert Ts == [2]
Co = sp.solve(v2o.subs(t, 2), C)[0]; assert Co == 2
# C<=0이면 v2>=0인 시간이 [0,1] 안 → P의 거리 <= 2 < 10
assert sp.integrate(v1, (t, 0, 1)) == 2
do = sp.integrate(v1, (t, 0, 3)) - sp.integrate(v2o.subs(C, Co), (t, 0, 3))
assert do == R(57, 2) and F.I['J44'][2] == '④' and F.I['J44'][1][3] == '\\dfrac{57}2'
print('원문 J44: v2=-t^2+t+C, C>0, T^3+T=10 → T=2, C=2, t=3에서 거리 57/2 = ④ OK')

# ---------- 변형: 속도가 0 이상인 시간과 P의 거리 (정의대로) ----------
def window(av, bv):
    """t>=0에서 v2=-3t^2+at+b >= 0 인 시간 [lo, hi] (없으면 None)"""
    disc = av**2 + 12*bv
    if disc < 0: return None
    r1, r2 = (av - sp.sqrt(disc))/6, (av + sp.sqrt(disc))/6
    if r2 < 0: return None
    return (sp.Max(r1, 0), r2)
def pdist(w):
    return sp.integrate(v1, (t, w[0], w[1]))      # v1>0 이므로 움직인 거리 = 위치 변화량
def b_from_max(av):
    return sp.Integer(MAXV) if av <= 0 else MAXV - sp.nsimplify(av)**2/12
# 최댓값 공식 확인: a<=0이면 t>=0에서 감소(최댓값 v2(0)=b), a>0이면 꼭짓점 t=a/6
assert sp.expand(-3*(t - a/6)**2 + b + a**2/12 - (-3*t**2 + a*t + b)) == 0

# 경우 (i) a<=0: b=3, 시간 [0, T], T<=1, 거리 <= 2
Ti = (a + sp.sqrt(a**2 + 36))/6
assert sp.simplify((-3*t**2 + a*t + 3).subs(t, Ti)) == 0 and Ti.subs(a, 0) == 1
assert sp.simplify(sp.diff(Ti, a)).subs(a, -5) > 0 and all(Ti.subs(a, -k) < 1 for k in (R(1, 10), 1, 5, 100))
D1 = sp.expand(Ti**3 + Ti)
assert D1.subs(a, 0) == 2
# 경우 (ii) 0<a<6 (h=a/6<1): 시간 [0, h+1], 거리 (h+1)^3+(h+1) < 10
D2 = sp.expand((h + 1)**3 + (h + 1)); assert D2.subs(h, 0) == 2 and D2.subs(h, 1) == 10
# 경우 (iii) a>=6 (h>=1): 시간 [h-1, h+1], 거리 6h^2+4
D3 = sp.expand(sp.integrate(v1, (t, h - 1, h + 1))); assert D3 == 6*h**2 + 4 and D3.subs(h, 1) == 10
# 세 구간이 이어지고(2, 10) 각 구간에서 증가 → D=28 은 (iii)에서만, 해는 하나
assert sp.expand(sp.diff(D2, h) - (3*(h + 1)**2 + 1)) == 0      # 양수 → 증가
hs = [r for r in sp.solve(sp.Eq(D3, DIST), h) if r >= 1]
assert hs == [2]
assert [r for r in sp.solve(sp.Eq(D2, DIST), h) if r.is_real and 0 < r < 1] == []
a0 = 6*hs[0]; b0 = MAXV - a0**2/12
assert (a0, b0) == (12, -9)
v2 = -3*t**2 + a0*t + b0
assert sp.expand(v2 + 3*(t - 1)*(t - 3)) == 0
print('변형: (i) a<=0 거리<=2, (ii) 0<h<1 거리<10, (iii) h>=1 거리 6h^2+4=28 → h=2, (a, b)=(12, -9) 하나 OK')

# (a, b) 격자 수치 전수: 최댓값 3 인 모든 a(-30..60, 1/8 간격)에서 P의 거리를 정의대로 계산
hits, prev = [], None
for k in range(-240, 481):
    av = R(k, 8); bv = b_from_max(av)
    w = window(av, bv); assert w is not None
    d = sp.nsimplify(pdist(w))
    if prev is not None: assert d > prev, av          # 증가
    prev = d
    if d == DIST: hits.append(av)
assert hits == [12]
print('전수: 최댓값 3 인 a=-30..60(1/8 간격) 721개에서 거리가 a에 대해 증가, 28 은 a=12 뿐 OK')

# ---------- 정답 ----------
xq = sp.integrate(v2, t); assert xq.subs(t, 0) == 0 and sp.expand(xq + t*(t - 3)**2) == 0
ret = sorted(r for r in sp.solve(xq, t) if r > 0); assert ret == [3]
def moved(vexpr, t0, t1):
    zs = sorted({r for r in sp.solve(vexpr, t) if r.is_real and t0 < r < t1})
    cuts = [t0] + zs + [t1]
    return sum(abs(sp.integrate(vexpr, (t, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))
ans = moved(v2, 0, ret[0])
assert ans == 8 and CH[it['ans'] - 1] == ans and xq.subs(t, 1) == -4
assert all(xq.subs(t, R(k, 10)) < 0 for k in range(1, 30))          # t=3 전에는 원점에 오지 않음
print(f'정답: x_Q=-t(t-3)^2, t=3에서 원점, 거리 4+4={ans} = ① OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] < CH[0]
w_half = abs(xq.subs(t, 1)); w_pos = sp.integrate(v2, (t, 1, 3)); w_sym = moved(v2, 0, 2)
assert (w_half, w_pos, w_sym) == (4, 4, 6)
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert {sp.Integer(w) for w in it['wrongs']} == {w_half, w_sym}
assert ans != R(57, 2) and ans not in (3, 1, 28, 0) and '8' not in re.sub(r'28', '', full)
print('선지 등차(공차 -1, 내림차순), 오답 4(편도·속도 0 이상인 시간의 Q 거리)·6(t=2에 돌아온다고 봄) 선지 안, 정답은 원문 답·문제 속 수와 다름 OK')

# ---------- 조건 빼 보기 ----------
def answer_for(av, bv):
    v = -3*t**2 + av*t + bv; xx = sp.integrate(v, t)
    rs = sorted(r for r in sp.solve(xx, t) if r.is_real and r > 0)
    return None if not rs else sp.nsimplify(moved(v, 0, rs[0]))
# (1) '최댓값 3' 없음: 거리 28 만으로는 (a, b)가 한 줄로 남는다 — v2=-3(t-p)(t-q), q^3+q-p^3-p=28
alt1 = {}
for pv in (1, R(1, 2), 0):
    qv = [r for r in sp.Poly(T**3 + T - pv**3 - pv - 28, T).nroots() if abs(sp.im(r)) < 1e-12][0]
    av, bv = 3*(pv + qv), -3*pv*qv
    assert abs(pdist(window(av, bv)) - 28) < 1e-9
    r_ = answer_for(av, bv); alt1[str(pv)] = None if r_ is None else round(float(r_), 3)
assert alt1['1'] == 8.0 and len(set(alt1.values())) == 3
print(f'ABLATION 18 최댓값 3: 필요(정해지지 않음: 빼면 속도가 0 이상인 시간의 시작 p=1, 1/2, 0 모두 거리 28 을 만족, 답 {list(alt1.values())})')
# (2) '거리 28' 없음: h 자유
alt2 = {str(hv): answer_for(6*hv, MAXV - 3*hv**2) for hv in (2, 3, R(3, 2))}
assert alt2['2'] == 8 and alt2['3'] is None and alt2['3/2'] == R(7, 4)
print(f'ABLATION 18 거리 28: 필요(정해지지 않음: 빼면 h=2, 3, 3/2 에서 답 {list(alt2.values())}, h=3은 원점으로 돌아오지 않음)')
# (3) 't>=0에서'(최댓값의 범위·시간의 범위) 없음: 실수 전체로 읽으면 a<0 인 창 [h-1, h+1] (h=-2) 도 거리 28
assert sp.integrate(v1, (t, -3, -1)) == 28
print('ABLATION 18 t>=0: 필요(빼면 h=-2 인 시간 -3<=t<=-1 도 거리 28 이 되어 a=-12 가 남음)')
# (4) 새 장치 — 미정계수 a 를 원문처럼 수로 고정(a2=3-6t 꼴, v2=-3t^2+3t+b): 최댓값 3 만으로 b=9/4, 거리는 39/8 로 정해져 조건 28 과 맞지 않음
bfix = b_from_max(3); dfix = pdist(window(3, bfix))
assert bfix == R(9, 4) and dfix == R(39, 8) and dfix != 28
# 원문 꼴(최댓값 조건 없이 a 고정, 미지수 b 하나): [0, T] 에서 T^3+T=28 → 유리근 없음, 답이 달라짐
Tq = [r for r in sp.Poly(T**3 + T - 28, T).nroots() if abs(sp.im(r)) < 1e-12][0]
assert sp.Poly(T**3 + T - 28, T).ground_roots() == {} and 2 < Tq < 3
r_fix = answer_for(3, 3*Tq**2 - 3*Tq)
assert r_fix is not None and abs(float(r_fix) - 8) > 1
print(f'ABLATION 18 미정계수 a(새 장치): 필요(a 를 3 으로 고정하면 최댓값 조건만으로 거리 39/8, 최댓값 조건까지 빼면 원문 꼴 [0, T], T≈{float(Tq):.3f}, 답 {float(r_fix):.3f})')
# (5) 원점 출발: 묻는 값이 '원점으로 돌아올 때까지'라 출발점이 필요 — 출발점이 x=1 이면 x=1-t(t-3)^2=0 의 첫 양근이 달라짐
r5 = sorted(r for r in sp.Poly(1 + xq, t).nroots() if abs(sp.im(r)) < 1e-12 and r > 0)[0]
assert abs(r5 - 3) > 0.1
print(f'ABLATION 18 원점 출발: 필요(출발점이 달라지면 원점에 오는 시각이 t≈{float(r5):.3f} 로 달라짐)')

# ---------- 원문 원리 줄 시험 ----------
# 원문 습관(시간을 [0, T] 로): T^3+T=28 유리근 없음. 그 T 로 최댓값 3 을 맞추면 h=T-1>1 이라 v2(0)<0 → [0, T] 가정과 모순
hq = Tq - 1; assert (3 - 3*hq**2) < 0
print('원문 원리 줄: 시간을 [0, T] 로 두면 T^3+T=28 에 유리근이 없고 v2(0)<0 이 되어 모순(그대로는 통하지 않음) OK')

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
