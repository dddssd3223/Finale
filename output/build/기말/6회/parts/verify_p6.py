# -*- coding: utf-8 -*-
# A18 (6회 18번 후보, 원문 M39, db_ref 'M39 킬러 설계A') 검증
# 원문 풀이(f(1)=-3) · 판정 원리(h = 단순근 개수, 불연속 = 서로 다른 정류점 함숫값) · (가)의 네 유형(인수분해로 전수)
# · (나)(다)로 하나 · 정의대로 센 h의 정수점 합 · 정답 = ⑤ · 선지 등차 · 오답(선지 안, 경로 재현) · 조건 빼 보기 · 문장 길이 · 원문 골격 · 흔한 패턴
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, p, q, s = sp.symbols('x p q s', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M39' and it['ans'] == 5 and it['db_ref'] == 'M39 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert [k for k, _ in it['cond']] == ['가', '나', '다'] and 'x^4+ax^3+bx^2' in it['body']
full = it['body'] + COND(it['cond']) + it['after']
assert 'f(t)' not in full and '|f(t)|' not in full          # 높이를 f(t)로 움직이는 장치 없음
CH = [sp.Integer(v) for v in it['choices']]
A0, B0 = -20, 20                                            # (다)의 적분 구간, 묻는 합의 범위

# ---------- h(t): 정의대로 (|f(x)-t|가 미분가능하지 않은 점 = f(x)=t의 단순 실근) ----------
def h_at(f_, t):
    P = sp.Poly(sp.expand(f_ - t), x)
    return sum(len(sp.real_roots(sp.Poly(fac, x))) for fac, k in sp.sqf_list(P)[1] if k == 1)
def h_num(f_, t):   # 무리수 계수용(수치): 실근을 모으고 중복을 묶어 단순근만 센다
    c = [complex(v) for v in sp.Poly(sp.expand(f_ - t), x).all_coeffs()]
    import numpy as np
    rs = np.roots(c); re_ = sorted(r.real for r in rs if abs(r.imag) < 1e-6)
    grp = []
    for r in re_:
        if grp and abs(r - grp[-1][-1]) < 1e-4: grp[-1].append(r)
        else: grp.append([r])
    return sum(1 for g in grp if len(g) == 1)
def crit_vals(f_):
    cp = sp.Poly(sp.diff(f_, x), x)
    return sorted({sp.nsimplify(sp.simplify(f_.subs(x, r))) for r in sp.real_roots(cp)}, key=lambda v: float(v))
def profile(f_, num=False):
    """임계값 목록 V와 각 점·구간의 h 값"""
    if not num and not all(v.is_Rational for v in crit_vals(f_)): num = True
    H = h_num if num else h_at
    V = crit_vals(f_) if not num else sorted({round(float(f_.subs(x, r)), 9) for r in sp.Poly(sp.diff(f_, x), x).nroots() if abs(sp.im(r)) < 1e-12}, key=float)
    pts = [(v, H(f_, v)) for v in V]
    mids = [float(V[0]) - 1] + [(float(V[i]) + float(V[i + 1])) / 2 for i in range(len(V) - 1)] + [float(V[-1]) + 1]
    ints = [H(f_, sp.nsimplify(m) if not num else m) for m in mids]
    return V, pts, ints
def n_disc(f_, num=False):
    V, pts, ints = profile(f_, num)
    return sum(1 for i, (v, hv) in enumerate(pts) if not (ints[i] == hv == ints[i + 1]))
def integral(f_, a_=A0, b_=B0, num=False):
    V, pts, ints = profile(f_, num)
    cuts = [a_] + [min(max(float(v), a_), b_) for v in V] + [b_]
    return sum(ints[i] * (cuts[i + 1] - cuts[i]) for i in range(len(ints)))
def int_sum(f_, num=False):
    H = h_num if num else h_at
    return sum(H(f_, sp.Integer(n) if not num else n) for n in range(A0, B0 + 1))

# ---------- 원문 M39 ----------
fo = x**3 * (x - 4)
Vo, pto, into = profile(fo)
assert Vo == [-27, 0] and dict(pto) == {-27: 0, 0: 1} and into == [0, 2, 2]   # h(0±)=2, h(0)=1 → 합 5
assert fo.subs(x, 1) == -3 and fo.subs(x, 1) < 1 and (x**3 * (x + 4)).subs(x, 1) == 5
assert F.I['M39'][2] == '③' and F.I['M39'][1][2] == '-3'
print('원문 M39: f=x^3(x-4), 불연속 t=-27, 0, 극한 합 2+2+1=5, f(1)=-3 = ③ OK')

# ---------- 판정 원리: 불연속점 = 서로 다른 정류점 함숫값 (견본 함수로 확인) ----------
samples = [x**4 - 6*x**2, x**3*(x - 4), x**2*(x - 2)**2, x**4 - 4*x**3 + R(9, 2)*x**2, x**4 + x**3 - 2*x**2, x**4, x**4 - 2*x**3 - 3*x**2]
for f_ in samples:
    assert n_disc(f_) == len(crit_vals(f_)), f_
print('판정 원리: 견본 7개에서 h의 불연속점 개수 = 서로 다른 극값(정류점 함숫값) 개수 OK')

# ---------- (가)의 네 유형: f'(x)=4x(x-p)(x-q) ----------
fpq = x**4 - R(4, 3)*(p + q)*x**3 + 2*p*q*x**2
assert sp.expand(sp.diff(fpq, x) - 4*x*(x - p)*(x - q)) == 0
assert sp.factor(fpq.subs(x, p) - fpq.subs(x, q)) == sp.factor(-(p - q)**3*(p + q)/3)
assert sp.factor(fpq.subs(x, p)) == sp.factor(-p**3*(p - 2*q)/3)
# 정류점 함숫값 {0, f(p), f(q)}가 두 개 ⇔ pq=0(p≠q) / p=q≠0 / p=2q·q=2p / p=-q≠0
types = {
    '(i) 정류 변곡 (q=0)': fpq.subs(q, 0),
    '(ii) 극소+변곡 (p=q)': fpq.subs(q, p),
    '(iii) 이중 접점 (p=2q)': fpq.subs(p, 2*q).subs(q, p),
    '(iv) 대칭 W (q=-p)': fpq.subs(q, -p),
}
for name, g in types.items():
    for pv in (R(1, 2), 1, R(3, 2), 2, 3, -1, -2):
        f_ = sp.expand(g.subs(p, pv)); assert n_disc(f_) == 2, (name, pv)
        hm1 = h_at(f_, -1)
        if name.startswith('(iv)'): assert hm1 == (4 if pv**4 > 1 else 0), (pv, hm1)
        else: assert hm1 <= 2, (name, pv, hm1)
# 일반 (p, q) 격자: 네 유형 밖에서는 불연속점이 3개(또는 x^4의 1개)
grid_bad = 0
for i in range(-8, 9):
    for j in range(-8, 9):
        pv, qv = R(i, 2), R(j, 2)
        f_ = sp.expand(fpq.subs({p: pv, q: qv}))
        typ = (pv * qv == 0 and pv != qv) or (pv == qv != 0) or (pv == 2*qv and qv != 0) or (qv == 2*pv and pv != 0) or (pv == -qv != 0)
        nd = n_disc(f_)
        if (nd == 2) != typ: grid_bad += 1
assert grid_bad == 0
print('(가): 불연속 두 곳 ⇔ 네 유형 (인수분해 + (p,q) 격자 289개) OK, h(-1)=4는 대칭 W형(깊이>1)에서만 OK')

# ---------- (나)(다): 대칭 W형 f=x^4-2s^2x^2, 깊이 m=s^4 ----------
m = sp.Symbol('m', positive=True)
# h: t<-m → 0, t=-m → 0, -m<t<0 → 4, t>=0 → 2 ; 적분 = 4·min(m,20) + 40
assert sp.solve(sp.Eq(4*m + 2*20, 76), m) == [9] and 4*20 + 2*20 != 76
fW = x**4 - 6*x**2
assert crit_vals(fW) == [-9, 0] and integral(fW) == 76 and h_at(fW, -1) == 4 and n_disc(fW) == 2
for sv in (R(3, 2), 2, R(5, 2), R(7, 4)):
    g = sp.expand(types['(iv) 대칭 W (q=-p)'].subs(p, sv))
    assert integral(g) != 76
assert sp.expand(types['(iv) 대칭 W (q=-p)'].subs(p, sp.sqrt(3))) == fW      # 정류점 ±√3, 깊이 9
print('(나)(다): W형, 4m+40=76 → m=9, f(x)=x^4-6x^2 하나 (m>20이면 120) OK')

# ---------- 정답 ----------
vals = {n: h_at(fW, n) for n in range(A0, B0 + 1)}
assert vals[-9] == 0 and vals[0] == 2 and all(vals[n] == 4 for n in range(-8, 0)) and all(vals[n] == 2 for n in range(1, 21))
assert all(vals[n] == 0 for n in range(-20, -9))
ans = sum(vals.values())
assert ans == 74 and CH[it['ans'] - 1] == 74
print(f'정답: h(-9)=0, h(-8..-1)=4, h(0)=2, h(1..20)=2 → 합 {ans} = ⑤ OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] < CH[0]
def all_roots_cnt(f_, t): return len(set(sp.real_roots(sp.Poly(f_ - t, x))))
w_double = ans - vals[-9] + 2                                        # 중근 둘을 셈 (h(-9)=2)
w_zero = ans - vals[0] + all_roots_cnt(fW, 0)                         # h(0)=3 (중근 0까지)
w_all = sum(all_roots_cnt(fW, n) for n in range(A0, B0 + 1))          # h를 근의 개수로
w_closed = ans - vals[-9] + 4                                          # -9 ≤ t < 0 에서 4
assert (w_double, w_zero, w_all, w_closed) == (76, 75, 77, 78), (w_double, w_zero, w_all, w_closed)
assert integral(fW) == 76                                              # 정적분 값과 같다고 본 경우도 76
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != 74
print('선지 등차(공차 -1, 내림차순), 오답 76(h(-9)=2·적분값)·75(h(0)=3)·77(근의 개수)·78(h(-9)=4) 모두 선지 안 OK')

# ---------- 조건 빼 보기 ----------
# (가) 없음: x=0 극대, 두 극솟값이 다른 W(-m1<-m2<0): 적분 2m1+2m2+40=76 → m1+m2=18, h(-1)=4 → 여럿, 합이 갈림
import numpy as np
def depths(pv, qv):
    g = fpq.subs({p: pv, q: qv}); return -float(g.subs(x, pv)), -float(g.subs(x, qv)), sp.expand(g)
alts = {}
for lam in (R(1, 1), R(4, 5), R(7, 10), R(3, 5)):
    # p=-1·u, q=lam·u 로 두고 깊이 합 18이 되는 u를 수치로 구함
    u = sp.Symbol('u', positive=True)
    g = fpq.subs({p: -u, q: lam*u})
    eq = -(g.subs(x, -u)) - (g.subs(x, lam*u)) - 18
    uv = sp.nsolve(eq, u, 2)
    d1, d2, gg = depths(-uv, lam*uv)
    assert d1 > 1 and d2 > 1 and abs(d1 + d2 - 18) < 1e-9
    gg = sp.expand(fpq.subs({p: -uv, q: lam*uv}))
    if lam != 1:
        assert n_disc(gg, num=True) == 3
    assert h_num(gg, -1) == 4 and abs(integral(gg, num=True) - 76) < 1e-6
    alts[str(lam)] = (round(d1, 3), round(d2, 3), int_sum(gg, num=True))
assert len({v[2] for v in alts.values()}) >= 2
print(f'ABLATION 18 (가): 필요(정해지지 않음: 빼면 극솟값이 다른 W형도 (나)(다)를 만족, (깊이1, 깊이2, 합)={list(alts.values())})')
# (나) 없음: 정류 변곡형 m=18, 이중 접점형 M=18 도 (가)(다)를 만족
fi = types['(i) 정류 변곡 (q=0)']; fd = types['(iii) 이중 접점 (p=2q)']
pi_ = sp.solve(sp.Eq(-fi.subs(x, p), 18), p)                       # p^4/3=18
pd_ = sp.solve(sp.Eq(fd.subs(x, p), 18), p)                        # 이중 접점: 가운데 극댓값 f(p)=p^4=18
gi = sp.expand(fi.subs(p, [v for v in pi_ if v.is_real][0])); gd = sp.expand(fd.subs(p, [v for v in pd_ if v.is_real][0]))
assert n_disc(gi, num=True) == 2 and n_disc(gd, num=True) == 2
assert abs(integral(gi, num=True) - 76) < 1e-6 and abs(integral(gd, num=True) - 76) < 1e-6
si, sd = int_sum(gi, num=True), int_sum(gd, num=True)
assert h_num(gi, -1) == 2 and h_num(gd, -1) == 0 and {si, sd, 74} == {74, 75}
print(f'ABLATION 18 (나): 필요(정해지지 않음: 빼면 정류 변곡형(깊이 18)·이중 접점형(높이 18)도 (가)(다)를 만족, 합 {si}, {sd}, 74)')
# (다) 없음: W형 깊이 m>1 이면 모두 (가)(나)를 만족
d_alt = {}
for mv in (4, 9, 16):
    g = x**4 - 2*sp.sqrt(mv)*x**2
    assert n_disc(g) == 2 and h_at(g, -1) == 4
    d_alt[mv] = int_sum(g)
assert len(set(d_alt.values())) == 3
print(f'ABLATION 18 (다): 필요(정해지지 않음: 빼면 깊이 m=4, 9, 16 모두 가능, 합 {list(d_alt.values())})')
# (다)의 구간 끝 20: m≤20 경계 — 깊이가 20을 넘으면 적분은 120으로 일정
g25 = x**4 - 10*x**2
assert integral(g25) == 120
print('ABLATION 18 m≤20 경계: 필요(깊이 25이면 적분 120 — 76이 되려면 m≤20 안의 해 m=9)')

# ---------- 문장 길이 ----------
def plain(t): return html.unescape(re.sub(r'<[^>]+>', '', t))
Lo = len(plain(F.I['M39'][0])); Lm = len(plain(full))
assert Lm >= 0.9 * Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(full))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M39'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하, 관문 0.60 미만)')
assert jd < 0.60
assert '\\[' not in it['body'] and '(단,' not in it['body']
print('ALL OK')
