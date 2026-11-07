# -*- coding: utf-8 -*-
# 견본2 9–12번 정답 검증 (sympy + 수치 전수, 유일성·케이스 누락 포함)
import os, re, sympy as sp
t, x, a, b, c, C, k = sp.symbols('t x a b c C k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p3.py')).read(), ns)
IT = ns['ITEMS']

def val(s):
    m = re.fullmatch(r'\\dfrac\{(-?\d+)\}\{?(\d+)\}?', s)
    return sp.Rational(int(m.group(1)), int(m.group(2))) if m else sp.Integer(int(s))

def chk(no, v, traps=()):
    it = IT[no]; num = [val(s) for s in it['choices']]
    assert num == sorted(num) and len(set(num)) == 5, (no, num)
    assert num[it['ans'] - 1] == v, (no, num, v)
    for tv in traps: assert tv in num and tv != v, (no, tv)
    print(f'{no}번 정답 {v} = 선지 {"①②③④⑤"[it["ans"]-1]} OK, 선지 {num}, 함정값 {list(traps)}')

def sign_changes(expr, lo=0, hi=None):
    """t>lo (열린 끝) 에서 expr의 부호가 바뀌는 점 개수 (다항식)"""
    P = sp.Poly(sp.expand(expr), t)
    rts = sorted({r for r in sp.real_roots(P) if r > lo and (hi is None or r < hi)})
    cnt = 0
    for r in rts:
        e = 0; q = P
        while q.eval(r) == 0: q = sp.Poly(sp.quo(q.as_expr(), t - r), t); e += 1
        cnt += e % 2
    return cnt

def dist(v, lo, hi):
    rts = sorted({r for r in sp.real_roots(sp.Poly(sp.expand(v), t)) if lo < r < hi})
    pts = [lo] + rts + [hi]
    return sum(abs(sp.integrate(v, (t, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))

# ---- 9번
X = 2*t**3 + a*t**2 + b*t
av = sp.solve(sp.diff(X, t, 2).subs(t, 1), a)[0]; assert av == -6
V = sp.diff(X, t).subs(a, av)
ok = [bv for bv in [sp.Rational(n, 4) for n in range(-80, 81)] if sign_changes(V.subs(b, bv)) == 1]
assert max(ok) == 0 and all(bv <= 0 for bv in ok) and len(ok) == 81  # b≤0 전부, 0<b 없음
assert sign_changes(V.subs(b, 6)) == 0 and sign_changes(V.subs(b, 3)) == 2
ans9 = dist(V.subs(b, 0), 0, 4)
trap9a = dist(V.subs(b, 6), 0, 4)              # 중근을 전환으로 셈
trap9b = sp.integrate(V.subs(b, 0), (t, 0, 4))  # 변위
assert (ans9, trap9a, trap9b) == (48, 56, 32)
chk(9, ans9, [trap9a])

# ---- 10번: 연속 조건 + 적분 조건 → a, b 유일, 누적 적분 부등식
f0 = a*x**3 + x - 1
cont = sp.Eq(f0.subs(x, 1), f0.subs(x, 0) + b)           # x=1 연속
cc = sp.integrate(f0, (x, 0, 1))
sol = sp.solve([cont, sp.Eq(cc + b, 3)], [a, b], dict=True); assert len(sol) == 1
sol = sol[0]; assert (sol[a], sol[b]) == (2, 3)
cv, bv = cc.subs(sol), sol[b]; assert cv == 0
# 직접 적분: f(x)=f0(x-k)+kb on [k,k+1]
def Fint(n): return sum(sp.integrate((f0.subs(sol)).subs(x, x - j) + j*bv, (x, j, j + 1)) for j in range(n))
assert sp.integrate((f0.subs(sol)).subs(x, x - 1) + bv, (x, 1, 2)) == 3
S = {n: Fint(n) for n in range(1, 12)}
ans10 = max(n for n in S if S[n] <= 63); assert S[7] == 63 and ans10 == 7
trap10 = max(n for n in S if S[n] < 63); assert trap10 == 6
trap10b = max(n for n in range(1, 12) if sum(cv + (j + 1)*bv for j in range(n)) <= 63); assert trap10b == 6
chk(10, ans10, [trap10])

# ---- 11번
f = sp.Rational(1, 4)*x**3 + a*x**2 + b*x + c
fp = sp.diff(f, x)
s1 = sp.solve([fp.subs(x, 1), sp.diff(fp, x).subs(x, 1)], [a, b], dict=True)[0]  # 최솟값 0 at x=1 (이차, 최고차 양수)
assert sp.factor(fp.subs(s1)) == sp.Rational(3, 4)*(x - 1)**2
ff = f.subs(s1)
tang = ff.subs(x, 3) + sp.diff(ff, x).subs(x, 3)*(x - 3)
cv = sp.solve(tang.subs(x, 0) + 7, c)[0]; assert cv == sp.Rational(-1, 4)
D = sp.factor((ff - tang).subs(c, cv)); assert sp.expand(D - sp.Rational(1, 4)*(x - 3)**2*(x + 3)) == 0
H = sp.Abs(D)
def nroots(kv):
    # |D|=k ⇔ D=k 또는 D=-k
    if kv < 0: return 0
    rs = set()
    for s in ([kv, -kv] if kv != 0 else [0]):
        rs |= set(sp.real_roots(sp.Poly(sp.expand(D - s), x)))
    return len(rs)
cnt = {kv: nroots(kv) for kv in range(-3, 15)}
good = [kv for kv in cnt if cnt[kv] >= 3]
assert cnt[8] == 3 and cnt[0] == 2 and all(cnt[kv] == 4 for kv in range(1, 8)) and cnt[9] == 2
ans11 = len(good); assert ans11 == 8
chk(11, ans11, [7, 9])

# ---- 12번: C 전수 (모든 실수 C 경우 분석 + 수치 스캔)
v1 = 2*t
v2 = sp.integrate(8 - 2*t, t) + C
def Pdist(Cv):
    Pv = sp.Poly(sp.expand(v2.subs(C, Cv)), t)
    rts = sorted(r for r in sp.real_roots(Pv))
    if Cv >= 0:
        hi = max(rts); return sp.integrate(v1, (t, 0, hi))
    if len(set(rts)) < 2: return 0
    lo, hi = rts
    lo = max(lo, 0); return sp.integrate(v1, (t, lo, hi))
# 해석적: C<0 (−16<C<0) 분기
sols = [Cv for Cv in sp.solve(sp.Eq(sp.integrate(v1, (t, 4 - sp.sqrt(16 + C), 4 + sp.sqrt(16 + C))), 16), C) if -16 < Cv < 0]
assert sols == [-15]
# C≥0 분기 해 없음: (4+sqrt(16+C))^2 = 16 → 해 없음
assert [Cv for Cv in sp.solve(sp.Eq((4 + sp.sqrt(16 + C))**2, 16), C) if Cv >= 0] == []
# 수치 스캔
import numpy as np
hits = [Cv for Cv in np.arange(-20, 20.0001, 0.25) if abs(float(Pdist(sp.nsimplify(Cv))) - 16) < 1e-9]
assert hits == [-15.0], hits
V2 = v2.subs(C, -15)
xP6 = sp.integrate(v1, (t, 0, 6)); xQ6 = sp.integrate(V2, (t, 0, 6))
ans12 = abs(xP6 - xQ6); assert (xP6, xQ6, ans12) == (36, -18, 54)
trap12 = abs(xP6 - sp.integrate(v2.subs(C, -16), (t, 0, 6)))  # [0,T] 가정
trap12b = xP6 + dist(V2, 0, 6)                                # 이동 거리 합
assert (trap12, trap12b) == (60, sp.Rational(170, 3))
chk(12, ans12, [trap12])
print('ALL OK')
