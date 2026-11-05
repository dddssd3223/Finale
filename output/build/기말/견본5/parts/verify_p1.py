# -*- coding: utf-8 -*-
# p1.py (견본5 Claude 2·4·6·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · 오답 값이 선지에 있음 · 조건 빼 보기
import os
import numpy as np
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, nsimplify, Poly
x, t, a, b, c, d, k, m, C, s = symbols('x t a b c d k m C s', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {2: 1, 4: 2, 6: 5, 8: 4}
assert sorted(IT) == [2, 4, 6, 8] and all(IT[n]['author'] == 'claude' for n in IT)
assert [IT[n]['key'] for n in (2, 4, 6, 8)] == ['M4', 'I49', 'D27', 'M15']

def arith(no):
    v = [nsimplify(ch) for ch in IT[no]['choices']]
    dd = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(dd) == 1 and list(dd)[0] != 0

def chk(no, val, wrongs=()):
    ch = [nsimplify(cc) for cc in IT[no]['choices']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and all(nsimplify(w) in ch and nsimplify(w) != nsimplify(val) for w in wrongs)
            and len({nsimplify(w) for w in wrongs}) == len(wrongs))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {list(wrongs)} {"OK" if good else "FAIL"}')
    assert good

def closed_maxmin(f, lo, hi):
    cands = [lo, hi] + [r for r in sp.real_roots(Poly(diff(f, x), x)) if lo <= r <= hi]
    vals = [f.subs(x, r) for r in cands]
    return max(vals), min(vals)

def local_kind(f, r):
    """f'(r)=0인 r에서 f'의 부호 변화로 극대/극소 판정"""
    fp = diff(f, x); e = Rational(1, 1000)
    l, rr = sp.sign(fp.subs(x, r - e)), sp.sign(fp.subs(x, r + e))
    return 'min' if (l < 0 < rr) else 'max' if (l > 0 > rr) else 'none'


def nroots_distinct(expr, tol=1e-7):
    """다항식 expr(x)의 서로 다른 실근 (수치, 중근은 하나로)"""
    cs = [float(c) for c in Poly(expand(expr), x).all_coeffs()]
    r = sorted(z.real for z in np.roots(cs) if abs(z.imag) < 1e-5)
    out = []
    for z in r:
        if not out or abs(z - out[-1]) > 1e-4: out.append(z)
    return out

def g_count(F, tv):
    """곡선 y=F(x)와 직선 y=tv의 교점 개수"""
    return len(nroots_distinct(F - tv))

def g_disc(F):
    """교점 개수 함수 g(t)가 불연속인 t (극값에서만 바뀔 수 있으므로 극값 좌우를 비교)"""
    crit = nroots_distinct(diff(F, x))
    vals = sorted({round(float(F.subs(x, c)), 9) for c in crit})
    out = []
    gaps = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    e = min([1e-3] + [gp / 10 for gp in gaps if gp > 1e-9])
    for v in vals:
        if not (g_count(F, v) == g_count(F, v - e) == g_count(F, v + e)): out.append(v)
    return out

def D27_f(bv, dv, kv=1):
    """그림과 같은 f'(x) = -k x (x-b)(x-d) (k>0, 0<b<d) 의 한 부정적분 f (적분상수 0: 개수는 상수와 무관)"""
    return integrate(-kv*x*(x - bv)*(x - dv), x)

def D27_ac(bv, dv, kv=1):
    """f'(x)가 극소인 a (0<a<b), 극대인 c (b<c<d)"""
    r = sorted(nroots_distinct(diff(-kv*x*(x - bv)*(x - dv), x)))
    assert len(r) == 2 and 0 < r[0] < bv < r[1] < dv
    return r[0], r[1]

# ===== 원문 풀이 =====
# M4: [-2,2], f=x^3/3+x^2-3x+1, M-m=9 (④)
Mo, mo = closed_maxmin(x**3 / 3 + x**2 - 3*x + 1, -2, 2)
assert Mo - mo == 9
# I49: f'=6x^2+5, f(0)=3 → f(1)=10
fo = integrate(6*t**2 + 5, (t, 0, x)) + 3
assert fo.subs(x, 1) == 10
# D27: f'=-x(x-b)(x-d), 직선 y=f(a)와 교점 3개 → f(a)=f(d) → p=1 (y=f(0)), q=4 (y=(f(a)+f(b))/2), p+q=5 (③)
def brentq(h, lo, hi, n=60):
    hl = h(lo)
    for _ in range(n):
        mid = (lo + hi) / 2; hm = h(mid)
        if (hm < 0) == (hl < 0): lo, hl = mid, hm
        else: hi = mid
    return (lo + hi) / 2
bo = 1.0
def _h(dv):
    F = D27_f(bo, dv); a_, _ = D27_ac(bo, dv)
    return float(F.subs(x, a_) - F.subs(x, dv))
do = brentq(_h, 1.05, 1.99)
Fo = D27_f(bo, do); ao, co = D27_ac(bo, do)
assert g_count(Fo, float(Fo.subs(x, ao))) == 3
po = g_count(Fo, float(Fo.subs(x, 0))); qo = g_count(Fo, float((Fo.subs(x, ao) + Fo.subs(x, bo)) / 2))
assert (po, qo) == (1, 4) and po + qo == 5
# M15: m ≥ -1 (x<0), m ≤ min_{x>0}(2x^2-9x+12)=15/8 → 7/8 (④)
q15 = 2*x**2 - 9*x + 12
assert q15.subs(x, Rational(9, 4)) == Rational(15, 8) and Rational(15, 8) + (-1) == Rational(7, 8)
print('원문 풀이 OK (M4=9, I49=10, D27=5, M15=7/8)')

# ===== 2번 =====
f2 = x**3 - 3*x - 4
M2, m2 = closed_maxmin(f2, -1, 3)
assert (M2, m2) == (14, -6)
# 수치 교차 (구간 전수)
xs = np.linspace(-1, 3, 400001); ys = xs**3 - 3*xs - 4
assert abs(ys.max() - 14) < 1e-9 and abs(ys.min() + 6) < 1e-6
w2_end = f2.subs(x, 3) - f2.subs(x, -1)          # 끝값만
w2_sign = M2 + m2                                  # 부호 실수
w2_loc = f2.subs(x, -1) - f2.subs(x, 1)            # 극댓값-극솟값
chk(2, M2 - m2, wrongs=(w2_end, w2_sign, w2_loc))

# ===== 4번 =====
F4 = integrate(3*x**2 - 3, x) + C
crit4 = solve(3*x**2 - 3, x)
kinds = {r: local_kind(F4.subs(C, 0), r) for r in crit4}
assert kinds == {-1: 'max', 1: 'min'}
mins = [r for r in crit4 if kinds[r] == 'min']
assert len(mins) == 1                              # 극소점은 하나 → 적분상수 유일
C4 = solve(F4.subs(x, mins[0]) - 6, C)
assert len(C4) == 1
f4 = F4.subs(C, C4[0])
w4_f0 = F4.subs(C, 6).subs(x, 3)                   # 극솟값을 f(0)으로
w4_swap = F4.subs(C, solve(F4.subs(x, -1) - 6, C)[0]).subs(x, 3)   # 극소점을 x=-1로
w4_noC = integrate(3*x**2 - 3, (x, 1, 3))          # 적분만
chk(4, f4.subs(x, 3), wrongs=(w4_f0, w4_swap, w4_noC))

# ===== 6번 =====
HERE = os.path.dirname(os.path.abspath(__file__))
assert 'fig_b5_6.svg' in IT[6]['body'] and open(os.path.join(HERE, 'fig_b5_6.svg')).read() == open('/home/user/Finale/output/build/부교재_기말/parts/fig_D27.svg').read()   # 원문 그림 그대로
assert "f'(0)=f'(b)=f'(d)=0" in IT[6]['body'] and '0&lt;a&lt;b&lt;c&lt;d' in IT[6]['body']
# 그림과 같은 f'은 f'(x) = -k x (x-b)(x-d) (k>0, 0<b<d) 꼴뿐 (사차함수의 도함수 = 삼차, 세 근 0, b, d, x→∞에서 음)
# (1) 불연속점 개수: 기호로 f(d)-f(0) = k d^3 (d-2b)/12 → d=2b ⇔ 두 극댓값 같음
kk, bb, dd = symbols('kk bb dd', positive=True)
Fs = integrate(-kk*x*(x - bb)*(x - dd), x)
assert sp.factor(Fs.subs(x, dd) - Fs.subs(x, 0)) == sp.factor(kk*dd**3*(dd - 2*bb)/12)
# (2) d/b 비를 촘촘히 바꾸며 g의 불연속점 개수 전수: d=2b 일 때만 2개, 나머지는 3개
cnt = {}
for bv in [1, 2, 3]:
    for r in [Rational(j, 20) for j in range(21, 80)]:          # d/b = 1.05 ~ 3.95
        F = D27_f(bv, bv*r)
        cnt[(bv, r)] = len(g_disc(F))
assert all((v == 2) == (r == 2) for (bv, r), v in cnt.items()) and all(v in (2, 3) for v in cnt.values())
# (3) d=2b 에서 g(f(a))+g(f(b))+g(f(c)) (a, c는 f'의 극소·극대점, 그리고 구간 안 아무 점이어도 같음)
ans6s = set()
for bv in [1, 2, 3, Rational(5, 2)]:
    for kv in [1, 3]:
        F = D27_f(bv, 2*bv, kv)
        a_, c_ = D27_ac(bv, 2*bv, kv)
        ga, gb, gc = (g_count(F, float(F.subs(x, v))) for v in (a_, bv, c_))
        assert (ga, gb, gc) == (4, 3, 4)
        ans6s.add(ga + gb + gc)
        for aa in [bv*Rational(j, 10) for j in range(1, 10)]:
            assert g_count(F, float(F.subs(x, aa))) == 4                     # 0<a<b 아무 점
            assert g_count(F, float(F.subs(x, bv + aa))) == 4                # b<c<d 아무 점
assert ans6s == {11}
ans6 = 11
# 오답 근거
#  ① f' 그래프를 f 그래프로 읽음: 곡선 y=f'(x)와 y=f'(a), f'(b), f'(c)의 교점 수
Fp = diff(D27_f(1, 2), x); a1, c1 = D27_ac(1, 2)
w6_read = sum(g_count(Fp, float(Fp.subs(x, v))) for v in (a1, 1, c1))
assert w6_read == 7
#  ③ 두 극댓값이 다르다고 보고(f(0)>f(d)) f(a)>f(d)인 경우: 2+3+4
F3 = D27_f(1, Rational(3, 2)); a3, c3 = D27_ac(1, Rational(3, 2))
assert float(F3.subs(x, 0)) > float(F3.subs(x, Rational(3, 2))) and float(F3.subs(x, a3)) > float(F3.subs(x, Rational(3, 2)))
w6_neq = g_count(F3, float(F3.subs(x, a3))) + g_count(F3, float(F3.subs(x, 1))) + g_count(F3, float(F3.subs(x, c3)))
assert w6_neq == 9
#  ④ 접점 x=b를 빼고 g(f(b))=2 → 4+2+4 / 원문 조건 f(a)=f(d)로 두면 3+3+4
w6_tan = 4 + (g_count(D27_f(1, 2), float(D27_f(1, 2).subs(x, 1))) - 1) + 4
w6_orig = g_count(Fo, float(Fo.subs(x, ao))) + g_count(Fo, float(Fo.subs(x, bo))) + g_count(Fo, float(Fo.subs(x, co)))
assert w6_tan == 10 and w6_orig == 10
#  ② 두 극댓값이 다르다고 보고 접점도 뺌: 2+2+4
w6_both = w6_neq - 1
assert w6_both == 8
chk(6, ans6, wrongs=(w6_read, w6_neq, w6_tan, w6_both))

# ===== 8번 =====
fR = x**3 - 8*x**2 + 21*x + 1; fL = x + 1; g8 = m*x + 1
assert fR.subs(x, 0) == fL.subs(x, 0) == 1
assert expand((fR - 1) / x - ((x - 4)**2 + 5)) == 0
def ok8(mv, n=200001):
    """모든 실수 x에서 f(x)≥mx+1 (수치 전수: x∈[-50,50] 촘촘히 + 양 끝 극한 성질)"""
    xs = np.linspace(-50, 50, n)
    fx = np.where(xs >= 0, xs**3 - 8*xs**2 + 21*xs + 1, xs + 1)
    return bool(np.all(fx - (mv*xs + 1) >= -1e-9))
grid = np.round(np.arange(-3, 9.0001, 0.05), 10)
okm = [mv for mv in grid if ok8(mv)]
assert abs(min(okm) - 1) < 1e-9 and abs(max(okm) - 5) < 1e-9
assert all(1 - 1e-9 <= mv <= 5 + 1e-9 for mv in okm) and len(okm) == len([mv for mv in grid if 1 - 1e-9 <= mv <= 5 + 1e-9])
# 기호 확인: 경계 포함, 밖은 불가
assert all((fR - (5*x + 1)).subs(x, v) >= 0 for v in [Rational(j, 10) for j in range(1, 200)])
assert (fR - (Rational(501, 100)*x + 1)).subs(x, 4) < 0
assert (fL - (Rational(99, 100)*x + 1)).subs(x, -1) < 0
x0 = [r for r in solve(diff(fR, x), x) if local_kind(fR, r) == 'min'][0]
assert (x0, fR.subs(x, x0)) == (3, 19)
w8_orig = 5 + (-1)                                  # 원문처럼 m ≥ -1
w8_vertex = 4 + 1                                   # 꼭짓점 x좌표
w8_locmin = (fR.subs(x, x0) - 1) / x0 + 1           # 극소점을 지나는 직선 기울기
chk(8, 5 + 1, wrongs=(w8_orig, w8_vertex, w8_locmin))

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 2번: 구간 [-1,3]을 빼면(실수 전체) 최댓값·최솟값이 없음 / 왼쪽 끝 -1 → 원문 -2이면 답 바뀜
M2b, m2b = closed_maxmin(f2, -2, 3)
print(f'ABLATION 2 닫힌구간 [-1, 3]: 필요(정해지지 않음: 실수 전체에서 삼차함수는 최댓값·최솟값 없음; 왼쪽 끝 -2이면 {M2b - m2b}로 같지만 오른쪽 끝 2이면 {closed_maxmin(f2, -1, 2)[0] - closed_maxmin(f2, -1, 2)[1]})')
assert closed_maxmin(f2, -1, 2)[0] - closed_maxmin(f2, -1, 2)[1] != 20
# 4번: 극솟값 조건을 빼면 C 미정 / '극솟값'→'극댓값'이면 답 바뀜
print(f'ABLATION 4 극솟값 6: 필요(정해지지 않음: f(3)=18+C, C 미정; 극댓값 6이면 {w4_swap})')
# 6번: 불연속점 개수 조건을 빼면 d/b 에 따라 답이 달라짐(정해지지 않음), 개수를 3으로 바꾸면 답이 여러 개
vals6 = set()
for r in [Rational(3, 2), Rational(5, 2), 3]:
    F = D27_f(1, r); a_, c_ = D27_ac(1, r)
    vals6.add(sum(g_count(F, float(F.subs(x, v))) for v in (a_, 1, c_)))
assert len(vals6 | {11}) >= 2
print(f'ABLATION 6 불연속인 t의 개수 2: 필요(답 바뀜: 두 극댓값이 다른 d=1.5b, 2.5b, 3b 에서 {sorted(vals6)}, d=2b 에서만 11)')
print("ABLATION 6 f'(0)=f'(b)=f'(d)=0·그림: 필요(극대 x=0, d·극소 x=b 를 정함)")
print('ABLATION 6 단서 0<a<b<c<d: 필요(f(a), f(c)가 극솟값과 극댓값 사이임을 정함)')
# 8번: x<0 조건을 빼면 최솟값 없음, x>0 조건을 빼면 최댓값 없음
okL = [mv for mv in grid if bool(np.all((np.linspace(0, 50, 20001)**3 - 8*np.linspace(0, 50, 20001)**2 + 21*np.linspace(0, 50, 20001) + 1) - (mv*np.linspace(0, 50, 20001) + 1) >= -1e-9))]
assert min(okL) == grid[0]
print(f'ABLATION 8 x<0 조각 x+1: 필요(정해지지 않음: x≥0만 보면 m≤5, 최솟값 없음; 원문 1-x이면 {w8_orig})')
print('ABLATION 8 x≥0 조각: 필요(정해지지 않음: x<0만 보면 m≥1, 최댓값 없음)')

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
