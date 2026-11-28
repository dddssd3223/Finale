# -*- coding: utf-8 -*-
# p1.py (견본4 Claude 1·3·5·7번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · 오답 값이 선지에 있음 · 조건 빼 보기
import os
import numpy as np
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, Piecewise, limit, nsimplify
x, t, a, b = symbols('x t a b', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 3: 1, 5: 2, 7: 5}
assert sorted(IT) == [1, 3, 5, 7] and all(IT[n]['author'] == 'claude' for n in IT)
assert [IT[n]['key'] for n in (1, 3, 5, 7)] == ['I27', 'I12', 'D15', 'I42']

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

def increasing_everywhere(fp_left, fp_right, av, lo=-30, hi=30, n=600001):
    """꺾인 점 x=av 좌우 도함수로 실수 전체 증가(도함수 >=0, 0인 점은 고립) 판정 (수치)"""
    xs = np.linspace(lo, hi, n)
    fl = sp.lambdify(x, fp_left, 'numpy'); fr = sp.lambdify(x, fp_right, 'numpy')
    d = np.where(xs < av, fl(xs), fr(xs))
    return bool(np.all(d > -1e-12))

# ===== 원문 풀이 =====
# I27: ∫_{-a}^a (x^5-2x^3+3x^2-7)dx=-12, 양수 a의 합 3 (①)
A = symbols('A')
r27 = solve(integrate(x**5 - 2*x**3 + 3*x**2 - 7, (x, -A, A)) + 12, A)
assert sum(r for r in r27 if r > 0) == 3
# I12: f=∫_0^x(3t^2+a), lim (f-3)/(x^2-1)=b, a+10b=27
F12 = integrate(3*t**2 + a, (t, 0, x))
a12 = solve(F12.subs(x, 1) - 3, a)[0]
b12 = limit((F12.subs(a, a12) - 3) / (x**2 - 1), x, 1)
assert a12 + 10*b12 == 27
# D15: x^3+x^2+|x-a|+2 역함수 존재, a 최댓값 -1 (②)
okD = [av for av in np.arange(-3, 1.001, 0.25) if increasing_everywhere(3*x**2 + 2*x - 1, 3*x**2 + 2*x + 1, av)]
assert abs(max(okD) - (-1)) < 1e-9
# I42: f=x^2+1(x<=1), 2x(x>1), g=∫_{-1}^x t f(t)dt. ㄱ g(1)=0 참, ㄴ 극댓값 없음(거짓), ㄷ g(x)=n 두 실근(참) → ㄱ,ㄷ (③)
assert integrate(t*(t**2 + 1), (t, -1, 1)) == 0
g0 = integrate(t*(t**2 + 1), (t, -1, 0))
assert g0 < 0  # x=0 극소(유일한 임계점), 양쪽으로 +∞ → 모든 자연수 n에서 두 실근
print('원문 풀이 OK (I27=3, I12=27, D15=-1, I42=ㄱ,ㄷ)')

# ===== 1번 =====
I1 = integrate(4*x**3 + 3*x**2 - 5*x - 13, (x, -A, A))
assert expand(I1) == 2*A**3 - 26*A
r1 = solve(I1 + 24, A)
assert sorted(r1) == [-4, 1, 3]
pos1 = [r for r in r1 if r > 0]
chk(1, sum(pos1), wrongs=(sum(r1), sum(abs(r) for r in r1)))

# ===== 3번 =====
F3 = integrate(3*t**2 + a, (t, 0, x))
# 극한이 존재하려면 분자 → 0 (아니면 ±∞): a가 다른 값이면 극한 없음을 확인
a3s = solve(F3.subs(x, 1) - 7, a)
assert len(a3s) == 1
a3 = a3s[0]
b3 = limit((F3.subs(a, a3) - 7) / (x**3 - 1), x, 1)
assert limit((F3.subs(a, a3) - 7) / (x**3 - 1), x, 1, '-') == b3
# a≠6 이면 좌·우극한이 ±∞로 갈림(극한 없음)
for av in (5, 7):
    L, R = limit((F3.subs(a, av) - 7) / (x**3 - 1), x, 1, '-'), limit((F3.subs(a, av) - 7) / (x**3 - 1), x, 1, '+')
    assert L in (sp.oo, -sp.oo) and R in (sp.oo, -sp.oo) and L != R
b3_wrong = diff(F3.subs(a, a3), x).subs(x, 1)          # x^2+x+1 누락
chk(3, a3 + b3, wrongs=(a3 + b3_wrong,))

# ===== 5번 =====
fl5 = diff(x**3 - 3*x**2 - 9*(a - x) + 1, x)   # x<a
fr5 = diff(x**3 - 3*x**2 - 9*(x - a) + 1, x)   # x>a
assert expand(fr5 - 3*(x - 3)*(x + 1)) == 0
assert sp.solve(fl5, x) == [] or all(not s.is_real for s in sp.solve(fl5, x))  # 왼쪽 조각 도함수는 항상 양수
# 역함수 존재 ⇔ 실수 전체 증가(연속, 양끝 ±∞). a를 촘촘히 전수
grid = np.round(np.arange(-6, 8.0001, 0.05), 10)
ok5 = [av for av in grid if increasing_everywhere(fl5, fr5, av, lo=-20, hi=20, n=200001)]
assert abs(min(ok5) - 3) < 1e-9 and all(av >= 3 - 1e-9 for av in ok5)
# 경계: a=3은 가능, a=3-ε은 불가 (기호)
eps = Rational(1, 1000)
assert fr5.subs(x, 3 - eps / 2) < 0              # a=3-ε 이면 (a,3)에서 감소
assert all(fr5.subs(x, 3 + Rational(k, 100)) > 0 for k in range(1, 200))
chk(5, 3, wrongs=(-1, 1))

# ===== 7번 =====
f7 = Piecewise((x**2 + 5, x <= 1), (8 - 2*x, True))
gp = x * f7                                        # g'(x)=x f(x) (t f(t) 연속)
assert (x * (x**2 + 5)).subs(x, 1) == (x * (8 - 2*x)).subs(x, 1)
# 임계점과 부호 변화 전수
crit = sorted(set([s for s in solve(x * (x**2 + 5), x) if s.is_real and s <= 1] + [s for s in solve(x * (8 - 2*x), x) if s > 1]))
assert crit == [0, 4]
sg = lambda v: sp.sign(gp.subs(x, v))
pts = [-5, -Rational(1, 2), Rational(1, 2), 1, 2, 3, 5, 10]
signs = [sg(v) for v in pts]
assert signs == [-1, -1, 1, 1, 1, 1, -1, -1]
maxima = [c for c in crit if sg(c - Rational(1, 10)) > 0 and sg(c + Rational(1, 10)) < 0]
minima = [c for c in crit if sg(c - Rational(1, 10)) < 0 and sg(c + Rational(1, 10)) > 0]
assert maxima == [4] and minima == [0]
def g7(X):
    return integrate(t * (t**2 + 5), (t, -1, min(X, 1))) + (integrate(t * (8 - 2*t), (t, 1, X)) if X > 1 else 0)
assert integrate(t * (t**2 + 5), (t, -1, 1)) == 0
val7 = g7(4)
# 수치 교차
ts = np.linspace(-1, 4, 2000001); ft = np.where(ts <= 1, ts**2 + 5, 8 - 2*ts)
assert abs(np.trapezoid(ts * ft, ts) - float(val7)) < 1e-6
chk(7, val7, wrongs=(integrate(8 - 2*t, (t, 1, 4)),))

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
s_all = sum(r1)
print(f'ABLATION 1 양수 조건: 필요(답 바뀜 {sum(pos1)} → {s_all}; 근 {sorted(r1)} 전체 합)')
# 3번: 분모를 x^3-1 대신 원문 x^2-1로 되돌리면 b가 바뀜(비교용), 분자 상수 7을 빼면(f(x)/(x^3-1)) a=-1, b=0
b3_alt = limit((F3.subs(a, a3) - 7) / (x**2 - 1), x, 1)
print(f'ABLATION 3 분모 x^3-1(→x^2-1): 필요(답 바뀜 {a3 + b3} → {a3 + b3_alt})')
a3n = solve(F3.subs(x, 1), a)[0]; b3n = limit(F3.subs(a, a3n) / (x**3 - 1), x, 1)
print(f'ABLATION 3 분자 상수 -7: 필요(답 바뀜 {a3 + b3} → {a3n + b3n})')
# 5번: 절댓값 항 계수의 부호(−9 → +9)를 되돌리면 판정하는 쪽이 x<a로 바뀌어 a≤-1, 최솟값이 없어짐
fl5b = diff(x**3 - 3*x**2 + 9*(a - x) + 1, x); fr5b = diff(x**3 - 3*x**2 + 9*(x - a) + 1, x)
ok5b = [av for av in grid if increasing_everywhere(fl5b, fr5b, av, lo=-20, hi=20, n=200001)]
assert abs(max(ok5b) + 1) < 1e-9 and min(ok5b) == grid[0]
print(f'ABLATION 5 절댓값 계수 부호(−9): 필요(정해지지 않음: +9이면 가능한 a는 a≤{max(ok5b)}, 최솟값 없음)')
# 7번: 조각을 하나씩 지움
def g_of(fexpr):
    gp_ = x * fexpr
    cr = sorted(s_ for s_ in solve(gp_, x) if s_.is_real)
    mx = [c for c in cr if gp_.subs(x, c - Rational(1, 10)) > 0 and gp_.subs(x, c + Rational(1, 10)) < 0]
    return [integrate(t * fexpr.subs(x, t), (t, -1, c)) for c in mx]
m1 = g_of(x**2 + 5); m2 = g_of(8 - 2*x)
print(f'ABLATION 7 x>1 조각 8-2x: 필요(정해지지 않음: 극댓값 {m1 if m1 else "없음"})')
print(f'ABLATION 7 x≤1 조각 x^2+5: 필요(답 바뀜 {val7} → {m2[0]})')
assert m1 == [] and m2[0] != val7

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
