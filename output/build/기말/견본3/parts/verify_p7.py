# -*- coding: utf-8 -*-
# 서답형1 (M16 유형 자체 제작) · 서답형2 (D25 구조 변경) 검증
import sympy as sp, os
x, k, a, b, p, q, c = sp.symbols('x k a b p q c', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S = ns['SITEMS']

# ---------- 원문 M16: g=-f+k, f>=g <=> 2f>=k, k 최댓값 -8 (②)
f0 = x**4 - 3*x**3 + x**2
cr = sp.solve(sp.diff(f0, x), x)
assert min(2*f0.subs(x, r) for r in cr) == -8
print('M16 원문 OK: k 최댓값 -8')

# ---------- S1
f = 3*x**4 - 6*x**2 + 10; g = 8*x**3 - 24*x + k
h = sp.expand(f - g)
assert h == 3*x**4 - 8*x**3 - 6*x**2 + 24*x + 10 - k
assert sp.expand(sp.diff(h, x) - 12*(x - 2)*(x - 1)*(x + 1)) == 0
H = {r: h.subs(x, r) for r in (-1, 0, 1, 2)}
assert H[-1] == -9 - k and H[2] == 18 - k and H[0] == 10 - k and H[1] == 23 - k
# 증감: (-inf,-1) 감소, (-1,1) 증가, (1,2) 감소, (2,inf) 증가
hp = sp.diff(h, x)
for t, s in ((-2, -1), (0, 1), (sp.Rational(3, 2), -1), (3, 1)):
    assert sp.sign(hp.subs(x, t)) == s
# (1) 최솟값 = min(극솟값) -> k <= -9
m1 = sp.Min(H[-1], H[2]).subs(k, 0)
assert m1 == -9
k1 = sp.solve(sp.Eq(-9 - k, 0), k)[0]; assert k1 == -9
# 경계 k=-9에서 성립, k=-9+1/100에서 실패
assert sp.minimum(h.subs(k, -9), x) == 0
assert sp.minimum(h.subs(k, -9 + sp.Rational(1, 100)), x) < 0
# (2) x>=0: 후보 h(0), h(2) (h(1)은 극대) -> 최솟값 10-k -> k <= 10
m2 = sp.minimum(h.subs(k, 0), x, sp.Interval(0, sp.oo))
assert m2 == 10
assert sp.minimum(h.subs(k, 10), x, sp.Interval(0, sp.oo)) == 0
assert sp.minimum(h.subs(k, 10 + sp.Rational(1, 100)), x, sp.Interval(0, sp.oo)) < 0
assert S['S1']['ans'] == [r'(1) \(-9\)', r'(2) \(10\)']
# 오답 근거: 극솟값 h(2)만 보면 18
assert sp.solve(sp.Eq(H[2], 0), k)[0] == 18
assert len(S['S1']['subs']) == 2 and S['S1']['subs'][0][1].startswith('4점') and S['S1']['subs'][1][1].startswith('6점')
print('S1 OK: (1) -9, (2) 10')

# ---------- 원문 D25: f=x^3-3x^2-9x-12, xg=|xF|, F=f(x-p)+q, p,q>0, 미분가능하지 않은 점 1개 -> p+q=8
fD = x**3 - 3*x**2 - 9*x - 12
sols = []
for pv in sp.solve(sp.diff(fD, x).subs(x, -p), p):        # 개수 1 <=> F'(0)=0 <=> f'(-p)=0 (아래에서 전수 확인)
    qv = -fD.subs(x, -pv)
    if pv > 0 and qv > 0: sols.append((pv, qv))
assert sols == [(1, 7)]
def kinks(pv):                                            # g = x|F/x| (F(0)=0): F/x 의 0 아닌, 부호가 바뀌는 근 개수
    qv = -fD.subs(x, -pv); hq = sp.cancel((fD.subs(x, x - pv) + qv) / x)
    rs = sp.roots(sp.Poly(hq, x))
    return sum(1 for r, m in rs.items() if r.is_real and r != 0 and m % 2 == 1)
assert kinks(1) == 1
for pv in [sp.Rational(n, 4) for n in range(1, 41)]:      # p>0 격자 전수: 개수 1은 p=1뿐
    if pv != 1: assert kinks(pv) != 1, pv
print('D25 원문 OK: p+q = 8')

# ---------- S2
# 연속: f(a)=0, f=(x-a)Q, x->a± 에서 g -> ±|Q(a)| 이므로 Q(a)=0  =>  f=(x-a)^2(x-b), g=(x-a)|x-b|
Qa = sp.Symbol('Qa', real=True)
assert sp.Eq(sp.Abs(Qa), -sp.Abs(Qa)).subs(Qa, 0) == True
assert sp.solve(sp.Abs(Qa) + sp.Abs(Qa), Qa) == [0]
gg = lambda A, B: (x - A) * sp.Abs(x - B)
# 단순근이면 불연속: f=(x-2)(x-8)(x-1) 이면 x->2 좌우극한이 -6, 6
_F = sp.Abs((x - 2) * (x - 8) * (x - 1)) / (x - 2)
assert sp.limit(_F, x, 2, '+') == 6 and sp.limit(_F, x, 2, '-') == -6
_F2 = sp.Abs((x - 2)**2 * (x - 8)) / (x - 2)
assert sp.limit(_F2, x, 2, '+') == 0 and sp.limit(_F2, x, 2, '-') == 0
fg = lambda A, B: (x - A)**2 * (x - B)
# 관계식 확인
for A, B in ((2, 8), (-1, 3)):
    for t in (-3, 0, 1, 5, 9):
        assert sp.simplify(((x - A) * gg(A, B) - sp.Abs(fg(A, B))).subs(x, t)) == 0
# 극댓값 판정: b>a 이면 극댓값 ((b-a)/2)^2 (x=(a+b)/2), b<a 이면 극댓값 0 (x=b), b=a 이면 극값 없음
def local_max(A, B, lo=-30, hi=30, N=6001):
    xs = [lo + (hi - lo) * i / (N - 1) for i in range(N)]
    ys = [(t - A) * abs(t - B) for t in xs]
    return sorted({round(ys[i], 6) for i in range(1, N - 1) if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1]})
assert local_max(2, 8) == [9.0]
assert local_max(8, 2) == [0.0]
assert local_max(3, 3) == []
assert local_max(-5, 1) == [9.0] and local_max(0, 4) == [4.0]
# b>a, ((b-a)/2)^2 = 9 -> b = a+6
assert set(sp.solve(sp.Eq(((c) / 2)**2, 9), c)) == {6, -6}
# (1) g'(a) = |a-b| = 6 (임의의 a에서)
for A in (-3, 0, 2, 5):
    G = gg(A, A + 6)
    d = sp.limit((G - G.subs(x, A)) / (x - A), x, A)
    assert d == 6 and sp.limit((G - G.subs(x, A)) / (x - A), x, A, '-') == 6
# (2) g(0) = -a|a+6| = -16 -> a = 2 (전수: 경우 a>=-6, a<-6)
r1 = [s for s in sp.solve(-a * (a + 6) + 16, a) if s >= -6]
r2 = [s for s in sp.solve(a * (a + 6) + 16, a) if s.is_real and s < -6]
assert r1 == [2] and r2 == []
assert sp.solve(-a * (a + 6) + 16, a) == [-8, 2]       # 오답 근거: 절댓값을 그대로 벗기면 -8, 2
assert gg(-8, -2).subs(x, 0) == 16                    # a=-8 이면 g(0)=16 (제외)
A0, B0 = 2, 8
assert gg(A0, B0).subs(x, 0) == -16 and local_max(A0, B0) == [9.0]
# (3) ∫_0^10 g = 36
I = sp.integrate((x - 2) * (8 - x), (x, 0, 8)) + sp.integrate((x - 2) * (x - 8), (x, 8, 10))
assert sp.integrate(gg(2, 8), (x, 0, 10)) == 36 and I == 36
assert sp.integrate((x - 2) * (8 - x), (x, 0, 8)) == sp.Rational(64, 3)
assert sp.integrate((x - 2) * (x - 8), (x, 8, 10)) == sp.Rational(44, 3)
assert sp.integrate((x - 2) * (8 - x), (x, 0, 10)) == sp.Rational(20, 3)   # 오답 근거: 나누지 않음
assert sp.integrate((x - 2) * (8 - x), (x, 2, 8)) == 36
assert S['S2']['ans'] == ['(1) 6', '(2) 2', '(3) 36']
assert [s[1][:2] for s in S['S2']['subs']] == ['4점', '4점', '2점']
print('S2 OK: (1) 6, (2) 2, (3) 36')
print('ALL OK')
