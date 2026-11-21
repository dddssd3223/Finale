# -*- coding: utf-8 -*-
# 부품 p4 (13·14번, 서답형1) 정답 검증
import os
import sympy as sp
import numpy as np

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT, SI = ns['ITEMS'], ns['SITEMS']
x, t, a, b = sp.symbols('x t a b', real=True)
ok = True
def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK " if cond else "FAIL"} {msg}')
    ok &= bool(cond)

def extrema_points(fp_expr, var, lo, hi):
    """구간 (lo,hi) 안에서 fp의 부호가 바뀌는 점(근)"""
    P = sp.Poly(sp.expand(fp_expr), var)
    pts = []
    for r, m in sp.roots(P, multiple=False).items():
        if r.is_real and m % 2 == 1 and lo < r < hi:
            pts.append(r)
    return pts

# ---------- 13번 ----------
f = -x**4 + 4*x**3
fp = sp.diff(f, x)
crit = sp.roots(sp.Poly(fp, x), multiple=False)
ext = [r for r, m in crit.items() if m % 2 == 1]
check(13, ext == [3], f"f'의 근 {crit} → 극점은 x=3뿐 (x=0 중근은 극점 아님)")
p = ext[0]
g = sp.expand(f.subs(x, t) + (p - t) * fp.subs(x, t))
# 정의 직접 확인: 접선 y=f'(t)(x-t)+f(t)에 x=p 대입
tan = fp.subs(x, t) * (x - t) + f.subs(x, t)
check(13, sp.expand(tan.subs(x, p) - g) == 0, f'g(t) = {g}')
check(13, sp.factor(sp.diff(g, t)) == sp.factor(12*t*(t-2)*(t-3)), f"g'(t) = {sp.factor(sp.diff(g, t))}")
L, R = p/3, 4*p/3
cands = [L, R] + [r for r in sp.solve(sp.diff(g, t), t) if L <= r <= R]
vals = {c: g.subs(t, c) for c in cands}
mn = min(vals.values())
print('   후보:', vals)
grid = np.linspace(float(L), float(R), 30001)
gnum = sp.lambdify(t, g, 'numpy')
check(13, abs(gnum(grid).min() - float(mn)) < 1e-6, '수치 최솟값 일치')
check(13, mn == 19, '최솟값 19')
check(13, IT[13]['choices'][IT[13]['ans'] - 1] == '19', '정답 ④ = 19')
check(13, sp.expand(g - 27 - (t-3)**2*(3*t**2-2*t-3)) == 0, 'g-27=(t-3)^2(3t^2-2t-3)')
# 함정 선지 값 확인
g0 = sp.expand(f.subs(x, t) - t*fp.subs(x, t))           # 원본 y절편
check(13, min(g0.subs(t, c) for c in [1, 2, 4]) == -16 and sp.factor(sp.diff(g0, t)) == sp.factor(12*t**2*(t-2)), 'y절편으로 풀면 -16')
check(13, g.subs(t, 0) == 0 and g.subs(t, 3) == 27 and f.subs(x, 1) == 3, '오답 0(g(0)), 27(극솟값), 3(f(1))')
ch = [sp.Integer(c) for c in IT[13]['choices']]
check(13, ch == sorted(ch) and len(set(ch)) == 5, '선지 크기순·서로 다름')

# ---------- 14번 ----------
def has_extremum(av):
    av = sp.Integer(av)
    fl = 3*x**2 - 3 - av     # x<2
    fr = 3*x**2 - 3 + av     # x>2
    # 부호 변화점: 각 조각 내부의 홀수중복 근 + 꺾인점 x=2
    pts = extrema_points(fl, x, -sp.oo, 2) + extrema_points(fr, x, 2, sp.oo)
    # x=2: 왼쪽 바로 옆과 오른쪽 바로 옆의 부호
    eps = sp.Rational(1, 10**6)
    sl = sp.sign(fl.subs(x, 2 - eps)); sr = sp.sign(fr.subs(x, 2 + eps))
    if sl * sr < 0: pts.append(sp.Integer(2))
    return len(pts)
def has_extremum_num(av):
    xs = np.linspace(-20, 20, 400001)
    fx = xs**3 - 3*xs + av*np.abs(xs - 2)
    d = np.diff(fx)
    s = np.sign(d[np.abs(d) > 1e-13])
    return int(np.sum(s[1:] != s[:-1]))
sol14 = [av for av in range(-40, 41) if has_extremum(av) == 0]
num14 = [av for av in range(-40, 41) if has_extremum_num(av) == 0]
print('14: 극값 없는 정수 a =', sol14, '/ 수치', num14)
check(14, sol14 == list(range(-9, -2)) and num14 == sol14, '극값 없음 ⇔ -9 ≤ a ≤ -3')
check(14, has_extremum(-10) > 0 and has_extremum(-2) > 0, '바깥 a=-10, -2는 극값 있음')
# 실수 a에 대해 경계 확인
for av in [-9.001, -2.999]:
    xs = np.linspace(-20, 20, 400001); fx = xs**3 - 3*xs + av*np.abs(xs - 2); d = np.diff(fx)
    s = np.sign(d[np.abs(d) > 1e-14]); check(14, np.sum(s[1:] != s[:-1]) > 0, f'a={av}: 극값 있음(경계 밖)')
check(14, IT[14]['choices'][IT[14]['ans'] - 1] == str(len(sol14)), '정답 ② = 7')
ch = [int(c) for c in IT[14]['choices']]
check(14, ch == sorted(ch), '선지 크기순')

# ---------- 서답형1 ----------
v1 = t**2 + a*t
v2 = b*(t - 6)
sol = sp.solve([sp.integrate(v1, (t, 0, 3)), v1.subs(t, 3) - v2.subs(t, 3)], [a, b], dict=True)
check('S1', sol == [{a: -2, b: -1}], f'(1) {sol}')
A, B = sol[0][a], sol[0][b]
V1, V2 = v1.subs(a, A), v2.subs(b, B)
vfun = sp.Piecewise((V1, t <= 3), (V2, True))
# 방향 전환: v=0이면서 부호 변화, t>0
zs = sorted(set([r for r in sp.solve(V1, t) if 0 <= r <= 3] + [r for r in sp.solve(V2, t) if r > 3]))
turn = []
for z in zs:
    if z == 0: continue
    e = sp.Rational(1, 1000)
    if sp.sign(vfun.subs(t, z - e)) * sp.sign(vfun.subs(t, z + e)) < 0: turn.append(z)
check('S1', zs == [0, 2, 6] and turn == [2, 6], f'v=0인 시각 {zs}, 방향 전환 {turn}')
check('S1', V1.subs(t, 3) == 3 and V2.subs(t, 3) == 3, 't=3: v=3>0으로 연속, 전환 아님')
# 수치로 전환 시각 확인
ts = np.linspace(0, 20, 200001)
vn = np.where(ts <= 3, ts**2 - 2*ts, 6 - ts)
tz = ts + 1.234567e-5
vz = np.where(tz <= 3, tz**2 - 2*tz, 6 - tz)
sg = np.sign(vz); idx = np.where((sg[1:] * sg[:-1] < 0))[0]
check('S1', len(idx) == 2 and np.allclose(tz[idx], [2, 6], atol=1e-3), f'수치 전환 시각 {tz[idx]}')
T2 = turn[1]
dist = sp.integrate(-V1, (t, 0, 2)) + sp.integrate(V1, (t, 2, 3)) + sp.integrate(V2, (t, 3, T2))
dnum = np.trapezoid(np.abs(vn[ts <= 6]), ts[ts <= 6]) if hasattr(np, 'trapezoid') else np.trapz(np.abs(vn[ts <= 6]), ts[ts <= 6])
check('S1', dist == sp.Rational(43, 6) and abs(dnum - 43/6) < 1e-6, f'(2) 거리 {dist} (수치 {dnum:.6f})')
pos6 = sp.integrate(V1, (t, 0, 3)) + sp.integrate(V2, (t, 3, 6))
check('S1', pos6 == sp.Rational(9, 2), '오답 함정: 위치 x(6)=9/2')
check('S1', '43' in SI['S1']['ans'][1] and '-2' in SI['S1']['ans'][0] and '-1' in SI['S1']['ans'][0], 'ans 문자열 일치')

print('ALL OK' if ok else 'SOME FAIL')
raise SystemExit(0 if ok else 1)
