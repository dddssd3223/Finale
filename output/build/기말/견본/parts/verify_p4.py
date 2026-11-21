# -*- coding: utf-8 -*-
# 부품 4 (13–16번) 정답 검증
import sympy as sp
import numpy as np
if not hasattr(np, 'trapz'): np.trapz = np.trapezoid
from fractions import Fraction as Fr

ns = {}
exec(open(__file__.replace('verify_p4.py', 'p4.py')).read(), ns)
IT = ns['ITEMS']
x, t, a, k, u = sp.symbols('x t a k u', real=True)

def sign_changes(poly, var, lo=-60, hi=60):
    """실근 중 홀수 중복도(부호 변화점) 목록"""
    P = sp.Poly(sp.expand(poly), var)
    out = []
    for r, m in sp.roots(P, multiple=False).items():
        if r.is_real and m % 2 == 1:
            out.append(r)
    # 수치 보조 (roots가 놓칠 경우 대비)
    if sum(sp.roots(P, multiple=False).values()) != P.degree():
        rr = np.roots([float(c) for c in P.all_coeffs()])
        out = [r.real for r in rr if abs(r.imag) < 1e-9]
    return sorted(out, key=lambda z: float(z))

ok = True
def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK " if cond else "FAIL"} {msg}')
    ok &= bool(cond)

# ---------- 13번 ----------
f = x**2 - 6*x + 5
F = sp.integrate(f, (x, 0, x))
def g13_maxcount(av):
    gp = sp.diff(f, x) * (F - F.subs(x, av))       # g'(x)
    # 직접 정의에서 g' 확인
    g = sp.integrate((f - f.subs(x, t)) * f.subs(x, t), (t, av, x))
    assert sp.simplify(sp.diff(g, x) - gp) == 0
    sc = sign_changes(gp, x)
    lead = sp.Poly(gp, x).LC()
    # 부호: x→-∞에서 (-1)^4*lead>0 → 변화점 순서대로 극대, 극소, ...
    return sum(1 for i in range(len(sc)) if i % 2 == 0) if lead > 0 else None, len(sc)
sol13 = []
for av in range(-15, 16):
    nmax, nch = g13_maxcount(sp.Integer(av))
    if nmax == 2: sol13.append(av)
print('13: 극대점 2개인 정수 a =', sol13)
check(13, sol13 == [0, 2, 4, 6], '정수 a = 0,2,4,6')
# 실수 a 전체 스캔 (구간 확인)
sc_real = []
for av in np.linspace(-3, 9, 1201):
    gp = sp.Poly(sp.expand(sp.diff(f, x) * (F - F.subs(x, sp.Rational(str(round(av, 3)))))), x)
    rr = np.roots([float(c) for c in gp.all_coeffs()])
    real = [r.real for r in rr if abs(r.imag) < 1e-7]
    # 근접 근 병합(중근)
    real.sort(); simple = []
    for r in real:
        if simple and abs(r - simple[-1]) < 1e-4: simple.pop()  # 짝수 중복 제거
        else: simple.append(r)
    if len(simple) == 4: sc_real.append(round(av, 3))
print('   실수 a 범위(4번 부호 변화):', min(sc_real), '~', max(sc_real))
check(13, -1 < min(sc_real) and max(sc_real) < 7, '실수 a는 (-1,7) 안')
for bad in [1, 3, 5]:
    check(13, g13_maxcount(sp.Integer(bad))[0] == 1, f'a={bad}이면 극대점 1개(함정)')
check(13, IT[13]['choices'][IT[13]['ans'] - 1] == '4', '정답 ② = 4')

# ---------- 14번 ----------
# f(x) = 3/2 (x-1) + Q(x), Q 주기 2 연속, Q(1)=0, ∫_0^2 Q = -1, Q' > -3/2 (증가)
# 일반식: 답은 Q에 무관하게 14 임을 기호로 확인
c = sp.symbols('c')
# H(x)=∫_x^{x+2} f = 3x + c (H' = 3)
cv = sp.solve(sp.Eq((3*0 + c) + (3*2 + c), 4), c)[0]
H = lambda s: 3*s + cv
ans14 = -H(-1) + H(1) + H(3)
check(14, ans14 == 14, f'-H(-1)+H(1)+H(3) = {ans14}')
# 구체적 증가함수 두 개로 수치 확인
def make_f(Qpts):
    # Qpts: [0,2] 위 꺾은선 (x, Q) 목록, Q(0)=Q(2)
    xs = np.array([p[0] for p in Qpts]); ys = np.array([p[1] for p in Qpts])
    def Q(z):
        z = np.mod(z, 2.0)
        return np.interp(z, xs, ys)
    return lambda z: 1.5 * (z - 1) + Q(z), xs, ys
def Qint(xs, ys): return np.trapz(ys, xs)
def brentq(fn, lo, hi):
    flo = fn(lo)
    for _ in range(200):
        mid = (lo + hi) / 2; fm = fn(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2
def build(shape):
    # shape(s) -> 꺾은선, s로 ∫Q=-1 맞춤
    s = brentq(lambda s: Qint(*map(np.array, zip(*shape(s)))) + 1, 1e-3, 5)
    return make_f(shape(s))
# 모양 1: x=1에서 0, [1,1+s]에서 기울기 -1.4로 감소, 이후 상수, 1 직전 급상승
def shape1(s):
    m = -1.4
    return [(0, m*s), (1 - 1e-3, m*s), (1, 0.0), (1 + s, m*s), (2, m*s)]
def shape2(s):
    return [(0, -s), (0.5, -1.2*s), (1 - 1e-3, -0.2*s), (1, 0.0), (1.5, -0.5*s), (2, -s)]
for nm, sh in [('모양1', shape1), ('모양2', shape2)]:
    ff, xs, ys = build(sh)
    Z = np.linspace(-6, 10, 400001)
    vals = ff(Z)
    inc = np.all(np.diff(vals) > -1e-12)
    per = np.max(np.abs(ff(Z) + 3 - ff(Z + 2))) < 1e-9
    I04 = np.trapz(ff(np.linspace(0, 4, 400001)), np.linspace(0, 4, 400001))
    zz = np.linspace(-1, 5, 600001)
    Iabs = np.trapz(np.abs(ff(zz)), zz)
    check(14, inc and per and abs(ff(np.array([1.0]))[0]) < 1e-9 and abs(I04 - 4) < 1e-3 and abs(Iabs - 14) < 1e-3,
          f'{nm}: 증가={inc}, f(x+2)=f(x)+3={per}, f(1)=0, ∫0^4 f={I04:.4f}, ∫|f|={Iabs:.4f}')
lin = lambda z: 1.5 * (z - 1)
zz = np.linspace(-1, 5, 600001)
print('   (함정) 일차 가정 ∫|f| =', round(np.trapz(np.abs(lin(zz)), zz), 4), ', 그때 ∫0^4 f =', 1.5 * (8 - 4))
check(14, IT[14]['choices'][IT[14]['ans'] - 1] == '14', '정답 ③ = 14')

# ---------- 15번 ----------
f15 = sp.Rational(1, 2)*x**3 - sp.Rational(7, 2)*x**2 + sp.Rational(15, 2)*x
fac = sp.factor(f15 + x**2)
print('15: f+x^2 =', fac)
check(15, sp.discriminant(x**2 - 5*x + 15, x) < 0, 'x^2-5x+15 > 0')
def N15(kv):
    cnt = 0
    # x>=0: 2f+x^2 = 6x+k
    for r in sp.real_roots(sp.Poly(2*f15 + x**2 - 6*x - kv, x)):
        pass
    rs = set(sp.real_roots(sp.Poly(2*f15 + x**2 - 6*x - kv, x)))
    cnt += sum(1 for r in rs if r >= 0)
    rs2 = set(sp.real_roots(sp.Poly(-x**2 - 6*x - kv, x)))
    cnt += sum(1 for r in rs2 if r < 0)
    # 원식 직접 대입 확인
    for r in list(rs) + list(rs2):
        val = f15.subs(x, r) + abs(f15.subs(x, r) + r**2) - 6*r - kv
        if (r >= 0 and r in rs) or (r < 0 and r in rs2):
            assert abs(sp.N(val)) < 1e-9
    return cnt
tab = {kv: N15(sp.Integer(kv)) for kv in range(-5, 15)}
print('   N(k):', tab)
for kv in [sp.Rational(1, 2), sp.Rational(9, 2), sp.Rational(17, 2), sp.Rational(-1, 2), sp.Rational(19, 2)]:
    print('   N(', kv, ') =', N15(kv))
sol15 = [kv for kv, n in tab.items() if n == 3]
check(15, sol15 == [0, 5, 6, 7, 8] and all(N15(sp.Integer(kv)) != 3 for kv in range(-200, -5)) and all(N15(sp.Integer(kv)) != 3 for kv in range(15, 200)),
      f'실근 3개인 정수 k = {sol15} (5개)')
check(15, IT[15]['choices'][IT[15]['ans'] - 1] == '5', '정답 ④ = 5')

# ---------- 16번 ----------
def v16(av): return (t - 1)*(t**2 - 4*t + av)
def N16(av):
    P = sp.Poly(sp.expand(v16(av)), t)
    return sum(1 for r, m in sp.roots(P, multiple=False).items() if r.is_real and r > 0 and m % 2 == 1)
check(16, N16(5) == 1, 'ㄱ: a=5 → 1번 (참)')
check(16, N16(0) == 2, 'ㄴ: a=0 → 2번 (거짓, "세 번" 아님)')
# 한 번만 바꾸는 a 집합 스캔
once = [Fr(i, 20) for i in range(-200, 400) if N16(sp.Rational(i, 20)) == 1]
print('16: 한 번만 바꾸는 a (격자 1/20, -10~20):', 'a=3' if Fr(3) in once else '', '/ a<4인 것', [q for q in once if q < 4], '/ 4 이상 최소', min(q for q in once if q >= 4))
check(16, [q for q in once if q < 4] == [Fr(3)] and min(q for q in once if q >= 4) == 4 and all(q in once for q in [Fr(i, 20) for i in range(80, 400)]), '집합 = {3} ∪ [4,∞)')
D = sp.integrate(v16(a), (t, 0, 3))
print('   ∫0^3 v =', sp.expand(D))
mn = min(D.subs(a, 3), D.subs(a, 4))
check(16, sp.expand(D - (sp.Rational(3, 2)*a - sp.Rational(27, 4))) == 0 and D.subs(a, 3) == sp.Rational(-9, 4) and D.subs(a, 4) == sp.Rational(-3, 4),
      'ㄷ: Δ(a)=3a/2-27/4 증가, 최솟값 Δ(3)=-9/4 (참), 함정값 Δ(4)=-3/4')
check(16, IT[16]['choices'][IT[16]['ans'] - 1] == 'T:ㄱ, ㄷ', '정답 ③ = ㄱ, ㄷ')

# ---------- 형식 ----------
for no, it in IT.items():
    ch = it['choices']
    if no != 16:
        vals = [float(sp.sympify(c.replace(r'\dfrac', '').replace('{', '(').replace('}', ')'))) for c in ch]
        check(no, vals == sorted(vals) and len(set(vals)) == 5, '선지 오름차순·중복 없음')
print('\n전체 결과:', '통과' if ok else '실패')
raise SystemExit(0 if ok else 1)
