# -*- coding: utf-8 -*-
"""p7 (서답형2, I75 구조 변경) 정답 검증: sympy 기호 계산 + 수치 전수 조사."""
import numpy as np
import sympy as sp

ok = True
def chk(c, msg):
    global ok
    print(('OK  ' if c else 'FAIL') + ' ' + msg)
    ok &= bool(c)

x, a, t = sp.symbols('x a t', real=True)

# ---------- 수치 도구 ----------
XS = None
def integ(vals, lo, hi):
    n = len(vals) - 1
    h = (hi - lo) / n
    return h * (vals[0] + vals[-1] + 4 * vals[1:-1:2].sum() + 2 * vals[2:-1:2].sum()) / 3

def A_num(fn, s, n=6000):
    xs = np.linspace(s, s + 3, n + 1); v = fn(xs)
    return integ(np.abs(v), s, s + 3) - abs(integ(v, s, s + 3))

def B_num(fn, tt, n=8000):
    xs = np.linspace(0, 4, n + 1); v = fn(xs) + tt
    return integ(np.abs(v), 0, 4) - abs(integ(v, 0, 4))

def A_set(fn):
    """A(s)>0 인 s를 격자에서 수집 → (최소, 최대, 연속 여부)"""
    ss = np.round(np.arange(-8, 10.0001, 0.05), 4)
    pos = [s for s in ss if A_num(fn, s, 1200) > 1e-7]
    return pos

# ---------- (1) (가) → 부호가 바뀌는 근은 3 하나 ----------
print('== (1) ==')
# 최고차항 1, 서로 다른 실근 2개 ⇒ f=(x-r)^2(x-b), r≠b. 부호가 바뀌는 근은 b 하나 → s 범위 (b-3, b)
for b in [1, 2, 3, 4, -1]:
    for r in [0, 5, -2, 3]:
        if r == b: continue
        fn = lambda X, r=r, b=b: (X - r)**2 * (X - b)
        pos = A_set(fn)
        lo, hi = min(pos), max(pos)
        chk(abs(lo - (b - 3)) <= 0.051 and abs(hi - b) <= 0.051 and len(pos) >= int(3 / 0.05) - 2,
            f'f=(x-{r})^2(x-{b}): A>0 범위 ≈ ({lo:.2f}, {hi:.2f}) = ({b-3}, {b})')
chk(True, '→ 범위가 0<s<3 이려면 단순근 b=3 (답 3), 중근 α≠3')
# 경계: s=0, s=3 에서는 A=0 (열린구간 끝에 근)
f0 = lambda X: X**2 * (X - 3)
chk(abs(A_num(f0, 0)) < 1e-9 and abs(A_num(f0, 3)) < 1e-9, 's=0, s=3 에서 A=0 (경계 제외)')
chk(A_num(f0, 0.01) > 0 and A_num(f0, 2.99) > 0, 's=0.01, 2.99 에서 A>0')

# ---------- (2) (나) → ∫_0^4 f = 0 → α ∈ {0, 4/3} ----------
print('== (2) ==')
fa = (x - 3) * (x - a)**2
I = sp.expand(sp.integrate(fa, (x, 0, 4)))
chk(sp.simplify(I - (-4 * a**2 + sp.Rational(16, 3) * a)) == 0, f'∫_0^4 (x-3)(x-α)^2 dx = {I}')
sol = sorted(sp.solve(sp.Eq(I, 0), a))
chk(sol == [0, sp.Rational(4, 3)], f'α 후보 {sol}')
chk(all(s != 3 for s in sol), '두 후보 모두 α≠3 (서로 다른 실근 2개 유지)')

# B(t) 최대점 = ∫_0^4 (f+t)=0 인 t = -(1/4)∫_0^4 f  (2min(P,N) 원리) 를 수치로 확인
TT = np.round(np.arange(-6, 6.0001, 0.01), 4)
def argmaxB(fn):
    vals = np.array([B_num(fn, tt, 2000) for tt in TT])
    return TT[vals.argmax()], vals.max()
for r in [0, 4 / 3]:
    fn = lambda X, r=r: (X - 3) * (X - r)**2
    tm, vm = argmaxB(fn)
    chk(abs(tm) < 0.011, f'α={r:.4f}: B 최대점 t≈{tm} (=0)')
    # 유일성: t=0 에서 좌우로 엄격히 작다
    b0 = B_num(fn, 0.0)
    chk(all(B_num(fn, d) < b0 - 1e-9 for d in [-0.5, -0.05, 0.05, 0.5, 2, -2]), f'α={r:.4f}: t=0이 유일한 최대점')
# 다른 α는 최대점이 0이 아님 (격자 전수)
bad = []
for r in np.round(np.arange(-4, 6.0001, 1 / 6), 6):
    if abs(r - 3) < 1e-9: continue
    fn = lambda X, r=r: (X - 3) * (X - r)**2
    tstar = -float(I.subs(a, sp.nsimplify(r))) / 4
    tm, _ = argmaxB(fn)
    if abs(tstar) <= 6 and abs(tm - tstar) > 0.011: bad.append((r, tm, tstar))
    if abs(tm) < 0.011 and not (abs(r) < 1e-9 or abs(r - 4 / 3) < 1e-6): bad.append(('extra', r))
chk(not bad, f'α 격자 전수: 최대점 = -(1/4)∫_0^4 f, t=0 인 것은 α=0, 4/3 뿐 {bad[:3]}')
# 중근이 3인 경우 f=(x-3)^2(x-b): (가)의 범위가 (b-3,b) → b=3 모순
chk(True, 'f=(x-3)^2(x-b)이면 (가) 범위 (b-3,b)=(0,3) → b=3, 서로 다른 실근 1개로 모순 (1단계에서 배제)')

# ---------- (3) B 최댓값 합 ----------
print('== (3) ==')
mx = []
for r in sol:
    f = (x - 3) * (x - r)**2
    P = sp.integrate(f, (x, 3, 4))
    N = -sp.integrate(f, (x, 0, 3))
    chk(sp.simplify(P - N) == 0, f'α={r}: 위 넓이 {P} = 아래 넓이 {N}')
    Bmax = 2 * sp.Min(P, N)
    # 부호: [0,3]에서 f≤0, [3,4]에서 f≥0
    fl = sp.lambdify(x, f)
    xs = np.linspace(0, 3, 3001); xs2 = np.linspace(3, 4, 1001)
    chk((fl(xs) <= 1e-12).all() and (fl(xs2) >= -1e-12).all(), f'α={r}: [0,3]에서 f≤0, [3,4]에서 f≥0')
    tm, vm = argmaxB(lambda X, r=float(r): (X - 3) * (X - r)**2)
    chk(abs(vm - float(Bmax)) < 1e-4, f'α={r}: B 최댓값 {Bmax} (수치 {vm:.6f})')
    mx.append(Bmax)
chk(mx == [sp.Rational(27, 2), sp.Rational(11, 2)], f'최댓값 {mx}')
chk(sum(mx) == 19, f'(3) 합 = {sum(mx)}')
# 오답 값 확인
chk(sp.Rational(27, 4) + sp.Rational(11, 4) == sp.Rational(19, 2), '오답: ∫_3^4 f 만 더하면 19/2')

print('ALL OK' if ok else 'SOME FAILED')
raise SystemExit(0 if ok else 1)
