# -*- coding: utf-8 -*-
# 9–12번 정답 검증 (sympy + 수치 전수)
import os, sympy as sp
from fractions import Fraction as Fr
x, u, t, a, c = sp.symbols('x u t a c', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p3.py')).read(), ns)
IT = ns['ITEMS']
def chk(no, val):
    it = IT[no]; ch = it['choices']
    # 선지 크기순 확인
    num = []
    for s in ch:
        if 'frac' in s:
            p, q = s.replace(r'\dfrac', '').replace('}', ' ').replace('{', ' ').split()[:2] if '{' in s else (s[-2], s[-1])
            num.append(sp.Rational(int(p), int(q)))
        else:
            num.append(sp.Integer(int(s)))
    assert num == sorted(num) and len(set(num)) == 5, (no, num)
    assert num[it['ans'] - 1] == val, (no, num, val)
    print(f'{no}번 정답 {val} = 선지 {"①②③④⑤"[it["ans"]-1]} OK, 선지 {num}')

# ---- 9번: f는 조건만 만족하면 임의. 서로 다른 f 세 개로 같은 값인지 확인
def item9(f):
    assert f.subs(x, 0) == 0 and f.subs(x, 1) == 2 and sp.integrate(f, (x, 0, 1)) == sp.Rational(1, 2)
    base = {-1: sp.integrate(-f.subs(x, x + 1) + 2, (x, -1, 0)), 0: sp.integrate(f, (x, 0, 1))}
    # 칸 [n, n+1] 적분: g(x)=2^m g(x-2m), 기준 칸 -1 또는 0
    def cell(n):
        b = -1 if n % 2 else 0  # n 홀수 → [-1,0] 칸, 짝수 → [0,1] 칸
        m = (n - b) // 2
        return sp.Integer(2) ** m * base[b]
    return sum(cell(n) for n in range(-3, 2))
p, q, r = sp.symbols('p q r')
gen = p*x**3 + q*x**2 + r*x
sol = sp.solve([gen.subs(x, 1) - 2, sp.integrate(gen, (x, 0, 1)) - sp.Rational(1, 2)], [q, r], dict=True)[0]
vals9 = set()
for pv in [0, 1, -3, sp.Rational(7, 2)]:
    f = sp.expand(gen.subs(sol).subs(p, pv)); vals9.add(item9(f))
# 비다항(구간별) f 하나 더: 수치 적분으로 독립 확인
import math
def g_num(xx, F):
    m = math.floor((xx + 1) / 2); y = xx - 2*m  # y in [-1,1)
    if y == -1: y, m = 1, m - 1
    base = (-F(y + 1) + 2) if y < 0 else F(y)
    return 2**m * base
F2 = lambda s: 6*s**3 - 6*s**2 + 2*s  # ∫=1.5-2+1=0.5, f(1)=2
N = 200000; h = 5 / N
num9 = sum(g_num(-3 + (i + 0.5)*h, F2) for i in range(N)) * h
assert len(vals9) == 1 and abs(num9 - 6) < 1e-6, (vals9, num9)
chk(9, vals9.pop())

# ---- 10번: g(x)=-f(2-x)+k, 만나지 않음 ⇔ f(x)-g(x)≠0 ∀x (사차, 최고차 양수 → >0)
f = x**4 - 4*x**3 + 2*x**2
H = sp.expand(f + f.subs(x, 2 - x))
crit = [rt for rt in sp.solve(sp.diff(H, x), x) if rt.is_real]
mH = min(sp.simplify(H.subs(x, rt)) for rt in crit)
assert mH == -10
ok = [k for k in range(-40, 10) if not any(abs(sp.im(z)) < 1e-12 for z in sp.Poly(H - k, x).nroots())]
# 중근(접함) 검사: k=-10은 실근(중근) 존재 → 만남
assert -10 not in ok and max(ok) == -11
# 원본식 함정값
mf = min(sp.N(f.subs(x, z)) for z in sp.Poly(sp.diff(f, x), x).nroots() if abs(sp.im(z)) < 1e-12)
print('  10번 함정: 2·min f =', round(float(2*mf), 3), '→', math.floor(float(2*mf)))
chk(10, max(ok))

# ---- 11번: 모든 실수 a에 대해 넓이 4 조건 전수
D = sp.expand((x**3 - 9*x**2 + a*x) - (x**3 - 6*x**2 + 9*x))
res = []
for av in sp.solve(sp.Eq(sp.Abs((a - 9)/3)**3 / 2, 4), a):
    rts = sorted(sp.solve(D.subs(a, av), x))
    lo, hi = rts[0], rts[-1]
    A = abs(sp.integrate(D.subs(a, av), (x, lo, hi)))  # 두 교점 사이 부호 일정
    assert A == 4
    ks = [kk for kk in sp.solve(sp.Eq(sp.integrate(D.subs(a, av), (x, lo, t)), sp.integrate(D.subs(a, av), (x, lo, hi))/2), t) if kk.is_real and lo < kk < hi]
    assert len(ks) == 1
    res.append(av + ks[0])
# 넓이 함수 연속·단조로 a=15, 3 외 해 없음 (a=9면 영역 없음)
assert sorted(res) == [2, 16], res
chk(11, min(res))

# ---- 12번: f=-x^4+px^3+qx^2+rx+s, 공차 6 → 1모수족(c), 교점 개수 전수
P, Q, R, S = sp.symbols('P Q R S')
f = -x**4 + P*x**3 + Q*x**2 + R*x + S
eqs = [f.subs(x, 1) - f.subs(x, -1) - 6, f.subs(x, 3) - f.subs(x, 1) - 6, f.subs(x, 5) - f.subs(x, 3) - 6]
sl = sp.solve(eqs, [P, Q, R], dict=True)[0]
fS = sp.expand(f.subs(sl))
h = sp.expand(fS - 3*x)
assert sp.expand(h - (-(x + 1)*(x - 1)*(x - 3)*(x - 5) + h.subs(x, 2) + 9)) == 0  # h = -R + c 꼴
def nroots_distinct(expr):
    pz = sp.Poly(expr, x)
    return len(sp.real_roots(pz)) and len(set(sp.real_roots(pz)))
good = []
# 교점 개수는 S(=c 이동)의 함수: 임계값 S0+{9,-16} 근방과 그 사이 구간을 정확히 판정
S0 = sp.solve(sp.Eq(h.subs(x, 2), 0), S)[0]  # h(2)=0 되는 S
cands = sorted(set([S0 + d for d in [-30, -20, -16, -10, 0, 5, 9, 10, 20]] + [S0 + sp.Rational(d, 2) for d in range(-40, 30)]))
for sv in cands:
    if nroots_distinct(h.subs(S, sv)) == 3:
        good.append(sv)
assert len(good) == 1
f4 = fS.subs(S, good[0]).subs(x, 4)
# 판정이 바뀌는 S는 h의 극값이 0이 되는 곳뿐임을 확인
ext = [sp.simplify(h.subs(x, z)) for z in sp.solve(sp.diff(h, x), x)]
print('  12번: h의 극값(=S의 1차식)', ext, ', 3근 되는 S', good, ', f =', sp.factor(fS.subs(S, good[0])))
chk(12, f4)
print('ALL PASS')
