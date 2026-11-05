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
assert [IT[n]['key'] for n in (2, 4, 6, 8)] == ['M4', 'I49', 'D30', 'M15']

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

# ===== 원문 풀이 =====
# M4: [-2,2], f=x^3/3+x^2-3x+1, M-m=9 (④)
Mo, mo = closed_maxmin(x**3 / 3 + x**2 - 3*x + 1, -2, 2)
assert Mo - mo == 9
# I49: f'=6x^2+5, f(0)=3 → f(1)=10
fo = integrate(6*t**2 + 5, (t, 0, x)) + 3
assert fo.subs(x, 1) == 10
# D30: f+kx=(x-α)^3, (나) α=1, f(2)+f'(2)=0 → k=4/3 (②)
fo30 = (x - 1)**3 - k*x
assert solve(fo30.subs(x, 2) + diff(fo30, x).subs(x, 2), k) == [Rational(4, 3)]
# M15: m ≥ -1 (x<0), m ≤ min_{x>0}(2x^2-9x+12)=15/8 → 7/8 (④)
q15 = 2*x**2 - 9*x + 12
assert q15.subs(x, Rational(9, 4)) == Rational(15, 8) and Rational(15, 8) + (-1) == Rational(7, 8)
print('원문 풀이 OK (M4=9, I49=10, D30=4/3, M15=7/8)')

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
# (가) 보조정리: 최고차항의 계수가 1인 삼차 h에 대하여 |h| 미분가능 ⇔ h=(x-α)^3
#  h의 실근 r에서 |h| 미분가능 ⇔ h'(r)=0 (h(r)=0, h'(r)≠0이면 좌우 미분계수가 ±h'(r)).
#  가능한 인수 구조 전수: (x-r)(이차, 판별식<0) / (x-r1)(x-r2)(x-r3) 서로 다름 / (x-r1)^2(x-r2) / (x-r)^3
r1, r2, r3, P, Q = symbols('r1 r2 r3 P Q', real=True)
struct = {
    '단일실근+허근': ((x - r1) * (x**2 + P*x + Q), [r1]),
    '세 실근': ((x - r1) * (x - r2) * (x - r3), [r1, r2, r3]),
    '이중근+단일근': ((x - r1)**2 * (x - r2), [r2]),
}
for name, (h, simple) in struct.items():
    hp = diff(h, x)
    # 단일근에서 h'≠0 (이차 인수 판별식<0 이므로 r1에서 이차식≠0, 서로 다른 근이면 곱≠0)
    val = factor(hp.subs(x, simple[0]))
    assert val != 0
h3 = (x - r1)**3
assert diff(h3, x).subs(x, r1) == 0
# 구체 수치로 단일근에서 좌우 미분계수가 다름을 확인
for h in [(x - 1) * (x**2 + 1), (x - 1) * x * (x + 1), (x - 1)**2 * (x + 2)]:
    for r in [rr for rr in sp.real_roots(Poly(h, x)) if diff(h, x).subs(x, rr) != 0]:
        L = sp.limit((abs(h) - abs(h.subs(x, r))) / (x - r), x, r, '-'); R = sp.limit((abs(h) - abs(h.subs(x, r))) / (x - r), x, r, '+')
        assert L != R
# 따라서 f(x)=(x-α)^3+kx. (나)를 전수로 푼다
al = symbols('al', real=True)
f6g = (x - al)**3 + k*x
sols = solve([diff(f6g, x).subs(x, -1), f6g.subs(x, -1) - 4], [al, k], dict=True)
sols = [S_ for S_ in sols if all(v.is_real for v in S_.values())]
assert sorted([(S_[al], S_[k]) for S_ in sols]) == [(-2, -3), (1, -12)]
good6 = [S_ for S_ in sols if local_kind(f6g.subs(S_), -1) == 'min']
bad6 = [S_ for S_ in sols if local_kind(f6g.subs(S_), -1) == 'max']
assert len(good6) == 1 and len(bad6) == 1
f6 = f6g.subs(good6[0])
assert expand(f6 - ((x + 2)**3 - 3*x)) == 0
assert expand(f6 - good6[0][k]*x - (x + 2)**3) == 0       # (가) 확인
w6_max = f6g.subs(bad6[0]).subs(x, -2)                    # 극소 확인 누락
w6_nokx = ((x + 2)**3).subs(x, -2)                         # kx 누락
w6_sgn = ((x + 2)**3 - good6[0][k]*x).subs(x, -2)          # 부호 실수
chk(6, f6.subs(x, -2), wrongs=(w6_max, w6_nokx, w6_sgn))

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
# 6번: (가)를 빼면 일반 삼차 f=x^3+bx^2+cx+d에서 f'(-1)=0, f(-1)=4, 극소 → 매개변수 하나 남음
pp = symbols('pp', real=True)
fgen = 4 + (x + 1)**2 * (x + pp)          # f'(-1)=0, f(-1)=4 인 최고차항의 계수가 1인 삼차함수 전체
vals = set()
for pv in [2, 3, 4, 5]:
    fb = fgen.subs(pp, pv)
    if local_kind(fb, -1) == 'min':
        vals.add(fb.subs(x, -2))
assert len(vals) >= 2
print(f'ABLATION 6 (가): 필요(정해지지 않음: f(-2) 값 {sorted(vals)} 등 여러 개)')
both = sorted({f6g.subs(S_).subs(x, -2) for S_ in sols})
print(f'ABLATION 6 (나)의 극소: 필요(정해지지 않음: 극값 4이면 f(-2)={both})')
assert len(both) == 2
# 8번: x<0 조건을 빼면 최솟값 없음, x>0 조건을 빼면 최댓값 없음
okL = [mv for mv in grid if bool(np.all((np.linspace(0, 50, 20001)**3 - 8*np.linspace(0, 50, 20001)**2 + 21*np.linspace(0, 50, 20001) + 1) - (mv*np.linspace(0, 50, 20001) + 1) >= -1e-9))]
assert min(okL) == grid[0]
print(f'ABLATION 8 x<0 조각 x+1: 필요(정해지지 않음: x≥0만 보면 m≤5, 최솟값 없음; 원문 1-x이면 {w8_orig})')
print('ABLATION 8 x≥0 조각: 필요(정해지지 않음: x<0만 보면 m≥1, 최댓값 없음)')

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
