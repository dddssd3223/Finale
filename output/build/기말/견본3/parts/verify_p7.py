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
# ===== 조건 제거 검사(ABLATION) =====
# 조건을 하나씩 지우고 답이 그대로인지 / 바뀌는지 / 정해지지 않는지 본다. 군더더기는 FAIL 이 아니라 보고만 한다.
print('--- 조건 제거 검사 ---')


def ablation(no, cname, vals, ans, why='', est=False, undef=None):
    """vals: 가능한 답 목록(각 원소는 값 또는 소문항별 튜플)"""
    if undef is not None:
        msg = f'필요({undef})'
    else:
        sv = list(dict.fromkeys(vals))
        if sv == [ans]:
            msg = f'성립 조건(답 그대로 {ans}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif isinstance(ans, tuple):
            parts = []
            for i in range(len(ans)):
                col = list(dict.fromkeys(v[i] for v in sv))
                parts.append(f'({i + 1}) ' + ('그대로 ' + str(ans[i]) if col == [ans[i]] else ' | '.join(map(str, col))))
            same = all(len(set(v[i] for v in sv)) == 1 for i in range(len(ans)))
            msg = f'필요({"답 바뀜" if same else "정해지지 않음"}: {", ".join(parts)}{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv))}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


# ----- S1: 조건 = [(단, k는 상수)], (1)·(2)의 '모든', (2)의 'x≥0', 부등식의 등호 -----
def kmax(lo):
    """구간 [lo, ∞) 에서 h ≥ 0 이 되는 k 의 최댓값 (= 그 구간에서 h+k 의 최솟값)"""
    return sp.minimum(h + k, x, sp.Reals if lo is None else sp.Interval(lo, sp.oo))
ablation('S1(2)', "'x≥0인'(→ 모든 실수)", [kmax(None)], kmax(0))
hk = lambda kv: h.subs(k, kv)
# x>0 (등호 제외): h'(0)=24>0 이라 x>0 에서도 inf = h(0) → k=10 에서 h(x)>0 (x>0)
assert sp.diff(h, x).subs(x, 0) == 24 and sp.minimum(hk(10), x, sp.Interval.open(0, sp.oo)) == 0
assert all(hk(10).subs(x, sp.Rational(i, 100)) > 0 for i in range(1, 1001))
ablation('S1(2)', "'x≥0'의 등호(→ x>0)", [10], kmax(0), why='h(x)>h(0)=10-k (0<x 근방)라 끝점을 빼도 k≤10')
# '모든' 제거('어떤 x에 대하여'): h→∞ 이므로 모든 k 에서 성립 → 최댓값 없음
assert sp.limit(h, x, sp.oo) == sp.oo
ablation('S1', "'모든 실수 x에 대하여'(→ 어떤 x)", [], -9, undef='h(x)→∞라 모든 k에서 성립, 최댓값 없음')
# 등호 제거(f>g): (1) k<-9 → 최댓값 없음
assert sp.minimum(hk(-9), x) == 0
ablation('S1', "부등식의 등호(≥ → >)", [], -9, undef='(1)은 k<-9, (2)는 k<10이 되어 최댓값 없음')
ablation('S1', "'(단, k는 상수이다)'", [-9], -9, est=True, why='k가 x에 따라 변하지 않는다는 선언')

# ----- S2: 조건 = [최고차항 계수 1], [삼차함수], [g 연속], [극댓값 9], [g(0)=-16] -----
def tri(G, A):
    """(1) g'(a), (2) a, (3) ∫₀¹⁰ g"""
    dl = sp.limit((G - G.subs(x, A)) / (x - A), x, A, '-')
    dr = sp.limit((G - G.subs(x, A)) / (x - A), x, A, '+')
    d1 = sp.nsimplify(dl) if dl == dr else '없음'
    I3 = sp.nsimplify(sp.integrate(G, (x, 0, 10)))
    return (d1, sp.nsimplify(A), I3)
def lmax_num(fun, lo=-30, hi=30, Nn=12001):
    xs = [lo + (hi - lo) * i / (Nn - 1) for i in range(Nn)]
    ys = [float(fun(v)) for v in xs]
    return sorted({round(ys[i], 4) for i in range(1, Nn - 1) if ys[i] > ys[i - 1] and ys[i] >= ys[i + 1]})
ANS2 = tri(gg(2, 8), 2)
assert ANS2 == (6, 2, 36)
# 최고차항 계수 1 제거: f=α(x-a)^2(x-b), g=|α|(x-a)|x-b|. 예 α=4, a=1, b=4
G4 = 4 * gg(1, 4)
assert lmax_num(lambda v: 4 * (v - 1) * abs(v - 4)) == [9.0] and G4.subs(x, 0) == -16
ablation('S2', "'최고차항의 계수 1'", [ANS2, tri(G4, 1)], ANS2, why='예: f=4(x-1)^2(x-4)')
# 삼차 제거(사차): f=(x-a)^2(x-b)^2, g=(x-a)(x-b)^2, 극댓값 4(b-a)^3/27=9, g(0)=-a b^2=-16
dl_ = sp.Rational(243, 4)**sp.Rational(1, 3)
aq = [r_ for r_ in sp.Poly(sp.expand(a * (a + dl_)**2 - 16), a).nroots() if abs(sp.im(r_)) < 1e-12]
aq = float(sp.re(aq[0])); bq = aq + float(dl_)
assert abs(-aq * bq**2 + 16) < 1e-9
assert [round(m, 3) for m in lmax_num(lambda v: (v - aq) * (v - bq)**2)] == [9.0]
d1q = round((aq - bq)**2, 3)      # g'(a)=(a-b)^2
ablation('S2', "'삼차함수'", [ANS2, (d1q, round(aq, 3), '…')], ANS2, why='예: f=(x-a)^2(x-b)^2 (사차), a≈%.3f' % aq)
# 연속 제거: f=(x-a)(x-2)(x-8), 0<a<2, g=|f|/(x-a) (x≠a), g(a)=0 → 극댓값 9(x=5), g(0)=-16, x=a 에서 불연속
v_ct = [ANS2]
for A in (1, sp.Rational(1, 2)):
    fA = sp.Abs((x - A) * (x - 2) * (x - 8))
    gfun = lambda v, A=A: abs((v - A) * (v - 2) * (v - 8)) / (v - A)
    Af = float(A)
    # x<a, x>a 각각의 극댓값(끝점 제외) + x=a 에서는 g(a)=0, 좌극한 <0< 우극한 이라 극값 아님
    lm = lmax_num(gfun, -30, Af - 1e-9, 6001) + lmax_num(gfun, Af + 1e-9, 30, 12001)
    lL, lR = sp.limit(fA / (x - A), x, A, '-'), sp.limit(fA / (x - A), x, A, '+')
    assert lm == [9.0] and lL < 0 < lR and sp.simplify((fA / (x - A)).subs(x, 0)) == -16, (A, lm, lL, lR)
    v_ct.append(('없음', A, '…'))
ablation('S2', "'g(x)는 실수 전체에서 연속'", v_ct, ANS2, why='예: f=(x-a)(x-2)(x-8), 0<a<2 (g(a)=0)')
# 극댓값 9 제거: b-a=δ 자유, g(0)=-a|a+δ|=-16
v_mx = []
for dv in (6, 15):
    for A in sp.solve(-a * (a + dv) + 16, a):
        if A >= -dv:
            v_mx.append(tri(gg(A, A + dv), A))
ablation('S2', "'극댓값 9'", v_mx, ANS2, why='b-a가 자유 (예: b-a=15이면 a=1)')
# g(0)=-16 제거: a 자유(평행이동) → (1)은 6 그대로, (2)(3) 정해지지 않음
v_g0 = [tri(gg(A, A + 6), A) for A in (2, 0, 4)]
ablation('S2', "'g(0)=-16'", v_g0, ANS2, why='g(x)=(x-a)|x-a-6|의 평행이동')

print('ALL OK')
