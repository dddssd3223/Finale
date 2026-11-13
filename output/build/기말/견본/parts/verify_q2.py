# -*- coding: utf-8 -*-
# 부품 q2 (10·11·13·14번) 정답 검증
import os
import sympy as sp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'q2.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
x, t, u, b, m, d2, A, B = sp.symbols('x t u b m d2 A B', real=True)

ok = True
def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)

def cval(s):
    s = s.replace(r'\dfrac', r'\frac')
    if s.startswith(r'\frac'):
        import re
        p, q = re.match(r'\\frac\{?(-?\d+)\}?\{?(\d+)\}?', s).groups()
        return sp.Rational(int(p), int(q))
    return sp.Rational(s)

def check_choices(no, value):
    ch = [cval(c) for c in IT[no]['choices']]
    check(no, ch == sorted(ch) and len(set(ch)) == 5, f'선지 크기순·서로 다름 {ch}')
    check(no, ch[IT[no]['ans'] - 1] == value, f'정답 번호 {IT[no]["ans"]} → {ch[IT[no]["ans"]-1]} = {value}')
    return ch

# ---------- 10번 ----------
f = x**3 + b*x**2 + m*x            # 최고차항 1, f(0)=0, f'(0)=m
check(10, sp.diff(f, x).subs(x, 0) == m, "f'(0)=m")
g = x*f
T1 = m*x                            # 원점 접선
T2 = sp.diff(g, x).subs(x, 4)*(x - 4) + g.subs(x, 4)
sol = sp.solve(sp.Poly(sp.expand(T2 - T1), x).all_coeffs(), [b, m], dict=True)
check(10, len(sol) == 1, f'해 유일: {sol}')
fs = f.subs(sol[0])
check(10, sp.expand(fs - (x**3 - 10*x**2 + 32*x)) == 0, f'f = {sp.expand(fs)}')
check(10, sp.diff(fs, x).subs(x, 4) == 0 and fs.subs(x, 4) == 32, "f'(4)=0, f(4)=m=32")
v10 = fs.subs(x, 5)
check(10, v10 == 35, f'f(5) = {v10}')
# 오답: 곱의 미분 누락(기울기 4f'(4)), 기울기 f'(4)
e1 = sp.solve(sp.Poly(sp.expand(4*sp.diff(f, x).subs(x, 4)*(x - 4) + 4*f.subs(x, 4) - T1), x).all_coeffs(), [b, m], dict=True)
e2 = sp.solve(sp.Poly(sp.expand(sp.diff(f, x).subs(x, 4)*(x - 4) + 4*f.subs(x, 4) - T1), x).all_coeffs(), [b, m], dict=True)
w1, w2 = f.subs(e1[0]).subs(x, 5), f.subs(e2[0]).subs(x, 5)
print('   오답: 곱의 미분 누락', w1, ' / 기울기 f\'(4)', w2)
ch = check_choices(10, v10)
check(10, w1 in ch and w2 in ch, '오답 95/3, 85/3이 선지에 있음')

# ---------- 11번 ----------
# 세 근 1-d, 1, 1+d (등차, 가운데 1) → f = (x-1)^3 - d^2 (x-1)
def area_between(fx, lx):
    h = sp.Poly(sp.expand(fx - lx), x)
    rr = sorted([r for r in h.real_roots()], key=float)
    rr = sorted(set(sp.nsimplify(r) for r in rr), key=float)
    if len(rr) < 2:
        return None, rr
    tot = 0
    for p, q in zip(rr, rr[1:]):
        tot += abs(sp.integrate(h.as_expr(), (x, p, q)))
    return sp.nsimplify(tot), rr
line = -7*x + 7
cands = []
for D2 in sp.solve(sp.Eq((d2 - 7)**2 / 2, 8), d2):     # 대칭 공식에서 나온 후보
    fx = (x - 1)**3 - D2*(x - 1)
    ar, rr = area_between(fx, line)
    print(f'   d^2={D2}: 교점 {rr}, 넓이 {ar}')
    if ar == 8 and D2 > 0:
        cands.append(D2)
# 전수: d^2를 0.01 간격으로 스캔해 넓이 8인 다른 해가 없는지 확인
def area_num(D2):
    h = np.poly1d([1, -3, 3 - D2 + 7, -1 + D2 - 7])   # (x-1)^3 - (D2-7)(x-1)
    rr = sorted(r.real for r in h.r if abs(r.imag) < 1e-9)
    if len(rr) < 3:
        return 0.0
    H = h.integ()
    return sum(abs(H(q) - H(p)) for p, q in zip(rr, rr[1:]))
grid = np.arange(0.01, 40, 0.01)
vals = np.array([area_num(v) - 8 for v in grid])
roots_num = [round(grid[i], 2) for i in range(len(grid) - 1) if vals[i] == 0 or vals[i]*vals[i+1] < 0]
check(11, cands == [11], f'유효한 d^2 = {cands} (d^2=3은 교점 1개라 제외)')
check(11, all(abs(r - 11) < 0.02 for r in roots_num), f'수치 스캔 해 d^2 ≈ {roots_num}')
f11 = (x - 1)**3 - 11*(x - 1)
r11 = sp.Poly(f11, x).real_roots()
check(11, sp.expand(f11).coeff(x, 3) == 1 and len(set(r11)) == 3 and sp.simplify(r11[0] + r11[2] - 2*r11[1]) == 0 and r11[1] == 1,
      f'f의 세 근 {r11} 등차·가운데 1')
v11 = f11.subs(x, 5)
check(11, v11 == 20, f'f(5) = {v11}')
w_bad = ((x - 1)**3 - 3*(x - 1)).subs(x, 5); w_axis = ((x - 1)**3 - 4*(x - 1)).subs(x, 5)
ch = check_choices(11, v11)
check(11, w_bad in ch and w_axis in ch, f'오답 {w_bad}(부적합 해), {w_axis}(x축 착각) 선지에 있음')

# ---------- 13번 ----------
f13 = 4*x**3 - 13*x**2
F13 = sp.lambdify(x, f13)
def h_num(tv, n=4001):
    xs = np.linspace(tv, tv + 2, n)
    ys = F13(xs)
    mx = ys.max()
    return xs[np.where(ys >= mx - 1e-9)[0].max()]
def h_exact(tv):
    if tv <= 0: return 0
    if tv < 1: return tv
    return tv + 2
ts = np.linspace(-1, 3, 4001)
hn = np.array([h_num(v) for v in ts])
he = np.array([h_exact(v) for v in ts])
check(13, np.max(np.abs(hn - he)) < 2e-3, f'h(t) 구간별 식 일치 (최대 오차 {np.max(np.abs(hn-he)):.1e})')
check(13, sp.expand(f13.subs(x, t + 2) - f13.subs(x, t) - 4*(t - 1)*(6*t + 5)) == 0, 'f(t+2)-f(t)=4(6t+5)(t-1)')
check(13, abs(h_num(1.0) - 3) < 1e-3, 'h(1)=3 (두 끝값이 같을 때 큰 쪽)')
I13 = sp.integrate(0, (t, -1, 0)) + sp.integrate(t, (t, 0, 1)) + sp.integrate(t + 2, (t, 1, 3))
Inum = np.trapezoid(hn, ts) if hasattr(np, 'trapezoid') else np.trapz(hn, ts)
check(13, I13 == sp.Rational(17, 2) and abs(Inum - 8.5) < 5e-3, f'∫h = {I13} (수치 {Inum:.4f})')
ch = check_choices(13, I13)

# ---------- 14번 ----------
f14 = x**4 - 4*x**3 - 3*x**2
fp = sp.diff(f14, x)
def diff_at(tv):
    return sp.expand(f14 - (fp.subs(x, tv)*(x - tv) + f14.subs(x, tv)))
# 몫 확인
q, r = sp.div(sp.expand(f14 - (fp.subs(x, t)*(x - t) + f14.subs(x, t))), (x - t)**2, x)
check(14, r == 0 and sp.expand(q - (x**2 + (2*t - 4)*x + 3*t**2 - 8*t - 3)) == 0, f'f-l=(x-t)^2·({q})')

def parts_num(tv):
    """접점이 아닌 두 교점이 있을 때 두 부분의 넓이 (수치)"""
    qq = np.poly1d([1, 2*tv - 4, 3*tv**2 - 8*tv - 3])
    rr = qq.r
    if np.any(np.abs(rr.imag) > 1e-12) or abs(rr[0] - rr[1]) < 1e-9 or np.min(np.abs(rr - tv)) < 1e-9:
        return None
    pts = sorted([rr[0].real, rr[1].real, tv])
    ft, fpt = tv**4 - 4*tv**3 - 3*tv**2, 4*tv**3 - 12*tv**2 - 6*tv
    D = np.poly1d([1, -4, -3, 0, 0]) - np.poly1d([fpt, ft - fpt*tv])
    I = D.integ()
    return [abs(I(pts[1]) - I(pts[0])), abs(I(pts[2]) - I(pts[1]))]
# 정확한 후보: 바깥 접점(같은 부호 A,B) 64AB=15(A+B)^2, 가운데 접점 A+B=0
SA, PA = -4*(t - 1), 6*t**2 - 12*t - 3
out = sp.solve(sp.Eq(64*PA, 15*SA**2), t)
mid = [s for s in sp.solve(sp.Eq(SA, 0), t) if PA.subs(t, s) < 0]
print('   바깥 접점 후보', out, ' 가운데 접점 후보', mid)
exact = []
for tv in out + mid:
    D = diff_at(tv)
    rr = sorted(set(sp.Poly(D, x).real_roots()), key=float)
    a_parts = [abs(sp.integrate(D, (x, p, qv))) for p, qv in zip(rr, rr[1:])]
    print(f'   t={tv}: 교점 {rr}, 두 부분 넓이 {a_parts}')
    if len(rr) == 3 and len(a_parts) == 2 and a_parts[0] == a_parts[1]:
        exact.append(tv)
# 전수 스캔: 두 부분 넓이 차의 부호 변화로 다른 해가 없는지
grid = np.linspace(-6, 6, 120001)
diffs = []
for tv in grid:
    p = parts_num(tv)
    diffs.append(np.nan if p is None else p[0] - p[1])
diffs = np.array(diffs)
scan = []
for i in range(len(grid) - 1):
    a1, a2 = diffs[i], diffs[i + 1]
    if np.isnan(a1) or np.isnan(a2): continue
    if a1 == 0 or a1*a2 < 0: scan.append(round(grid[i], 3))
print('   스캔으로 찾은 t ≈', scan)
check(14, sorted(exact) == [-1, 1, 3], f'정확한 해 t = {sorted(exact)}')
check(14, len(scan) == 3 and all(min(abs(s - e) for e in [-1, 1, 3]) < 1e-3 for s in scan), '스캔 해가 -1, 1, 3 셋뿐')
ab = sp.integrate(u**2*(u - A)*(u - B), (u, 0, B))
check(14, sp.factor(ab - B**4*(5*A - 3*B)/60) == 0, '∫_0^B u²(u-A)(u-B)du = B⁴(5A-3B)/60')
v14 = sum(exact)
check(14, v14 == 3, f'모든 t의 합 = {v14}')
ch = check_choices(14, v14)

print('\n전체:', '통과' if ok else '실패')
raise SystemExit(0 if ok else 1)
