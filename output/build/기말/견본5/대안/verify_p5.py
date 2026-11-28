# -*- coding: utf-8 -*-
# p5.py (견본5 Claude 1·3·5·7번, 분담표 Codex 자리 대체) 검증:
# 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · 오답 값이 선지에 있음 · 조건 빼 보기
import os
import numpy as np
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, nsimplify, sqrt, Poly
x, t, a, b, k = symbols('x t a b k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 4, 3: 5, 5: 3, 7: 1}
assert sorted(IT) == [1, 3, 5, 7] and all(IT[n]['author'] == 'claude' for n in IT)
assert [IT[n]['key'] for n in (1, 3, 5, 7)] == ['I3', 'D17', 'J16', 'J33']

def arith(no):
    v = [nsimplify(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs=()):
    ch = [nsimplify(c) for c in IT[no]['choices']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and all(nsimplify(w) in ch and nsimplify(w) != nsimplify(val) for w in wrongs))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {list(wrongs)} {"OK" if good else "FAIL"}')
    assert good

def solve_identity(P, deg=5):
    """F - f = P(x), F' = f 를 만족시키는 다항식 f를 차수 deg 이하에서 전수로 구함 (유일성 확인)"""
    cs = symbols(f'c0:{deg + 1}')
    f = sum(cs[i] * x**i for i in range(deg + 1))
    # F = f + P 이고 F' = f  ⇔  f' + P' = f
    eqs = Poly(expand(diff(f, x) + diff(P, x) - f), x).all_coeffs()
    sol = solve(eqs, cs, dict=True)
    assert len(sol) == 1
    return expand(f.subs(sol[0]))

def real_roots(expr):
    return sorted(set(Poly(expr, x).real_roots()))

def area_abs(pieces, lo, hi):
    """조각 [(u, v, 식)]으로 주어진 함수의 |f| 정적분 (조각 안의 영점에서 나눔)"""
    tot = 0
    for (u, v, e) in pieces:
        A, B = max(u, lo), min(v, hi)
        if A >= B: continue
        rs = sorted(r for r in solve(e, x) if r.is_real and A < r < B)
        pts = [A] + rs + [B]
        for i in range(len(pts) - 1):
            tot += abs(integrate(e, (x, pts[i], pts[i + 1])))
    return nsimplify(tot)

def signed_int(pieces, lo, hi):
    return sum(integrate(e, (x, max(u, lo), min(v, hi))) for (u, v, e) in pieces if max(u, lo) < min(v, hi))

def periodic_pieces(base, shift, nmin=-4, nmax=4, add=True):
    """-1<=x<1 에서 base, f(x+2)=f(x)+shift 로 확장한 조각들"""
    return [(2*n - 1, 2*n + 1, expand(base.subs(x, x - 2*n) + (n * shift if add else 0))) for n in range(nmin, nmax + 1)]

# ===== 원문 풀이 =====
# I3: F = f + 2x^3 - 7x^2, f(x)=5x^2 의 실근의 합 2 (①)
fI3 = solve_identity(2*x**3 - 7*x**2)
assert fI3 == 6*x**2 - 2*x - 2
rI3 = solve(fI3 - 5*x**2, x)
assert len(rI3) == 2 and all(r.is_real for r in rI3) and sp.simplify(sum(rI3)) == 2
# D17: f = ax^3+bx+a, x=1 극소, 극솟값 -2 → 극댓값 6
fD = a*x**3 + b*x + a
sD = solve([diff(fD, x).subs(x, 1), fD.subs(x, 1) + 2], [a, b], dict=True)[0]
fD17 = fD.subs(sD)
assert diff(fD17, x, 2).subs(x, 1) > 0 and fD17.subs(x, -1) == 6
# J16: f=(x-4)^2, g=-2x+k (7<k<16), S2=2S1 → k=10 (③): 넓이 직접 계산
def J16_k(fq, gl, lo, hi):
    """S2 = 2 S1 이 되는 k를 넓이 직접 계산(교점 기호)으로 구함, 범위 안 근 전수"""
    h = expand(fq - gl)
    r = sorted(solve(h, x), key=lambda z: float(z.subs(k, (lo + hi) / 2)))
    al, be = r
    S1 = integrate(h, (x, 0, al)); S2 = -integrate(h, (x, al, be))
    ks = [kv for kv in np.linspace(lo + 1e-6, hi - 1e-6, 4001)]
    vals = [float((S2 - 2*S1).subs(k, kv)) for kv in ks]
    roots = [ks[i] for i in range(len(ks) - 1) if vals[i] == 0 or vals[i] * vals[i + 1] < 0]
    return roots, S1, S2
rJ, _, _ = J16_k((x - 4)**2, -2*x + k, 7, 16)
assert len(rJ) == 1 and abs(rJ[0] - 10) < 1e-2
# J33: -1<=x<1 f=-x^2+ax, f(x)=f(x-2)+4, 연속 → a=2, A(x=-2)+B(x=3) = 38/3 (②)
aJ = solve((-1 + a) - ((-1 - a) + 4), a)[0]
assert aJ == 2
PJ = periodic_pieces(-x**2 + aJ*x, 4)
assert area_abs(PJ, -2, 0) + area_abs(PJ, 0, 3) == Rational(38, 3)
print('원문 풀이 OK (I3=2, D17=6, J16=10, J33=38/3)')

# ===== 1번 =====
P1 = x**3 - 4*x**2 + 3*x
f1 = solve_identity(P1)                      # 차수 5 이하 전수에서 f가 유일 (존재 확인)
assert f1 == 3*x**2 - 2*x + 1
F1 = expand(f1 + P1)
assert expand(diff(F1, x) - f1) == 0 and expand(F1 - f1 - P1) == 0
# 답은 f를 구하지 않아도 정해짐: F'=f 로 미분하면 f - f' = P' (어떤 해 f에 대해서도)
assert expand(f1 - diff(f1, x) - diff(P1, x)) == 0
ans1 = (f1 - diff(f1, x)).subs(x, 1)
assert ans1 == diff(P1, x).subs(x, 1) == -2
w1_nodiff = P1.subs(x, 1)                                    # 미분하지 않고 F(1)-f(1) → 0
w1_dropf = (diff(P1, x) - diff(P1, x, 2)).subs(x, 1)         # f의 도함수를 빠뜨려 f=P' → 0
w1_sign = -ans1                                              # f'-f 로 부호 반대 → 2
w1_fonly = f1.subs(x, 1)                                     # f(1)만 → 2
w1_fponly = diff(f1, x).subs(x, 1)                           # f'(1)만 → 4
assert (w1_nodiff, w1_dropf, w1_sign, w1_fonly, w1_fponly) == (0, 0, 2, 2, 4)
chk(1, ans1, wrongs=(w1_nodiff, w1_sign, w1_fponly))

# ===== 3번 =====
f3 = a*x**3 + b*x - 1
S3 = solve([diff(f3, x).subs(x, 1), f3.subs(x, 1) - 3], [a, b], dict=True)
assert len(S3) == 1 and S3[0] == {a: -2, b: 6}
f3s = f3.subs(S3[0])
crit3 = sorted(solve(diff(f3s, x), x))
assert crit3 == [-1, 1]
sg3 = lambda v: sp.sign(diff(f3s, x).subs(x, v))
assert (sg3(-2), sg3(0), sg3(2)) == (-1, 1, -1)   # x=-1 극소, x=1 극대
ans3 = f3s.subs(x, -1)
w3_min_at1 = 3                                     # x=1을 극소로 봄
w3_odd = -3                                        # 원점 대칭으로 봄 (상수항 무시)
S3b = solve([diff(f3, x).subs(x, 1), (a + b + 1) - 3], [a, b], dict=True)[0]   # 상수항 부호 실수
w3_sign = (a*x**3 + b*x - 1).subs(S3b).subs(x, -1)
assert w3_sign == -3
w3_center = f3s.subs(x, 0)                          # 대칭의 중심 (0, -1)
chk(3, ans3, wrongs=(w3_min_at1, w3_odd, w3_center))

# ===== 5번 =====
f5 = 3*(x - 4)**2; g5 = -6*x + k
h5 = expand(f5 - g5)
assert expand(h5 - (3*(x - 3)**2 + 21 - k)) == 0
# 넓이 직접 계산(교점 기호)으로 S2 = 2 S1 의 근을 21<k<48 에서 전수
r5, S1e, S2e = J16_k(f5, g5, 21, 48)
assert len(r5) == 1
ans5 = solve(integrate(h5, (x, 0, 3)), k)[0]
assert ans5 == 30 and abs(r5[0] - 30) < 1e-2
assert sp.simplify((S2e - 2*S1e).subs(k, 30)) == 0
al5, be5 = 3 - sqrt(3), 3 + sqrt(3)
assert sp.simplify(h5.subs(k, 30).subs(x, al5)) == 0 and al5 > 0      # 두 교점 모두 양수, y축이 왼쪽 경계
w5_vertex = solve(integrate(h5, (x, 0, 4)), k)[0]                    # 꼭짓점 x=4
w5_sign = solve(integrate(h5, (x, 0, 5)), k)[0]                      # f'(x)=-6 부호 실수 x=5
w5_dslip = solve(integrate(h5, (x, 0, 2)), k)[0]                     # f'(x)=3(x-4) 로 미분 실수 x=2
assert w5_vertex == w5_sign == 28 and w5_dslip == 34
chk(5, ans5, wrongs=(w5_vertex, w5_dslip))

# ===== 7번 =====
base7 = -3*x**2 + a*x
a7s = solve((-3 + a) - (base7.subs(x, -1) + 12), a)
assert a7s == [6]
P7 = periodic_pieces(base7.subs(a, 6), 12)
# 연속성 (모든 이음점) 확인
for (u, v, e) in P7[:-1]:
    nxt = [pc for pc in P7 if pc[0] == v][0]
    assert e.subs(x, v) == nxt[2].subs(x, v)
# 이동 조건 f(x+2)=f(x)+12 확인
for (u, v, e) in P7[:-1]:
    nxt = [pc for pc in P7 if pc[0] == v][0]
    assert expand(nxt[2].subs(x, x + 2) - e - 12) == 0
# [-1,3]에서 영점은 x=0 하나
z7 = sorted({r for (u, v, e) in P7 for r in solve(e, x) if r.is_real and max(u, -1) <= r < min(v, 3) and -1 < r < 3})
assert z7 == [0]
ans7 = area_abs(P7, -1, 3)
# 수치 교차
xs = np.linspace(-1, 3, 4000001)
fx = np.where(xs < 1, -3*xs**2 + 6*xs, -3*(xs - 2)**2 + 6*(xs - 2) + 12)
assert abs(np.trapezoid(np.abs(fx), xs) - float(ans7)) < 1e-6
w7_a0 = area_abs(periodic_pieces(base7.subs(a, 0), 12), -1, 3)       # 연속 조건에서 이동량 누락 → a=0
w7_signed = signed_int(P7, -1, 3)                                    # x축 아래 부분을 빼서 계산
w7_noshift = area_abs(periodic_pieces(base7.subs(a, 6), 12, add=False), -1, 3)   # 옮길 때 +12 누락
assert (w7_a0, w7_signed, w7_noshift) == (24, 20, 12)
chk(7, ans7, wrongs=(w7_a0, w7_signed, w7_noshift))

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 1번: 우변 다항식에서 항 하나씩 빼면 답이 바뀜 / 'F는 f의 부정적분'을 빼면 정해지지 않음
for drop in [x**3, -4*x**2, 3*x]:
    Pd = P1 - drop
    vd = diff(Pd, x).subs(x, 1)
    assert vd != ans1
    print(f'ABLATION 1 우변 항 {drop}: 필요(답 바뀜 {ans1} → {vd})')
vals1 = sorted({(g - diff(g, x)).subs(x, 1) for g in [x, x**2, x**3]})   # F=f+P 는 어떤 f로도 성립
assert len(vals1) == 3
print(f"ABLATION 1 F는 f의 부정적분: 필요(정해지지 않음: F'=f가 없으면 F=f+P는 어떤 f로도 성립, f=x, x^2, x^3에서 {vals1})")
# 3번: '극값 3' 을 빼면 a 미정, x=1 을 빼면 미정 / 상수항 -1을 0으로 하면 답 바뀜
fa = a*x**3 - 3*a*x - 1
print(f'ABLATION 3 극값 3: 필요(정해지지 않음: f=ax^3-3ax-1, 극솟값 {fa.subs(x, -1)} (a<0) 등 a에 따라 달라짐)')
print('ABLATION 3 x=1: 필요(정해지지 않음: 극값을 갖는 위치가 정해지지 않으면 a, b 미정)')
f3c = a*x**3 + b*x
S3c = solve([diff(f3c, x).subs(x, 1), f3c.subs(x, 1) - 3], [a, b], dict=True)[0]
print(f'ABLATION 3 상수항 -1: 필요(답 바뀜 {ans3} → {f3c.subs(S3c).subs(x, -1)})')
# 5번: S2=2S1 을 빼면 k 미정, y축 경계를 x=1 로 바꾸면 답 바뀜, 기울기 -6 을 -2로 바꾸면 답 바뀜
k_alt = solve(integrate(h5, (x, 1, 3)), k)[0]
h5b = expand(3*(x - 4)**2 - (-2*x + k)); m5b = Rational(11, 3)
k_alt2 = solve(integrate(h5b, (x, 0, m5b)), k)[0]
print(f'ABLATION 5 S2=2S1: 필요(정해지지 않음: 21<k<48 의 모든 k에서 넓이가 정해질 뿐)')
print(f'ABLATION 5 y축 경계(→ x=1): 필요(답 바뀜 30 → {k_alt})')
print(f'ABLATION 5 직선 기울기 -6(→ -2): 필요(답 바뀜 30 → {k_alt2})')
assert k_alt != 30 and k_alt2 != 30
# 7번: 연속 조건을 빼면 a 미정, 이동량 12 → 4 이면 답 바뀜, 경계 x=-1 → x=-2 이면 답 바뀜
vals7 = sorted({area_abs(periodic_pieces(base7.subs(a, av), 12), -1, 3) for av in [5, 6, 7]})
print(f'ABLATION 7 연속: 필요(정해지지 않음: a=5,6,7 에서 넓이 {vals7})')
assert len(vals7) == 3
a4 = solve((-3 + a) - (base7.subs(x, -1) + 4), a)[0]
v74 = area_abs(periodic_pieces(base7.subs(a, a4), 4), -1, 3)
assert abs(float(v74) - 28) > 1e-6
print(f'ABLATION 7 이동량 12(→ 4): 필요(답 바뀜 {ans7} → {sp.N(v74, 6)})')
print(f'ABLATION 7 왼쪽 경계 x=-1(→ x=-2): 필요(답 바뀜 {ans7} → {area_abs(P7, -2, 3)})')

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
