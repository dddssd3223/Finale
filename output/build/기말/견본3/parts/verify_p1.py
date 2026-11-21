# -*- coding: utf-8 -*-
# p1.py (견본3 1–4번) 검증: 계산값 = 지정 선지, 정답 번호, 유일성, 선지 등차·서로 다름, 오답 값 선지 포함, 원문 직접 풀이
import os
from sympy import symbols, Rational, diff, integrate, solve, factor, sympify, Abs, Piecewise, nsimplify
x, t, a = symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 2, 2: 4, 3: 1, 4: 3}
WRONG = {1: [6], 2: [-12], 3: [17, 15], 4: [16, 12]}
ok = True

def ch(no):
    return [nsimplify(sympify(c)) for c in IT[no]['choices']]

def check(no, val, note=''):
    global ok
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    arith = len(d) == 1 and 0 not in d and len(set(v)) == 5
    good = arith and IT[no]['ans'] == WANT[no] and sympify(val) == v[IT[no]['ans'] - 1]
    w = all(sympify(u) in v and sympify(u) != sympify(val) for u in WRONG[no])
    good &= w
    ok &= good
    print(f'{no}번 [{IT[no]["key"]}]: 계산 {val}, 선지 {v} 정답 위치 {IT[no]["ans"]}, 등차 {arith}, 오답 {WRONG[no]} 포함 {w} -> {"OK" if good else "FAIL"} {note}')

def orig(name, got, want):
    global ok
    g = sympify(got) == sympify(want)
    ok &= g
    print(f'   원문 {name}: 계산 {got}, 원문 정답 {want} {"OK" if g else "FAIL"}')

# ---------- 1번 (J26)
v = 4*t**3 - 8*t + a
X = integrate(v, (t, 0, 2))
s = solve(X - 6, a); assert len(s) == 1
mis = solve(integrate(4*t**3 - 8*t, (t, 0, 2)) + a - 6, a)[0]     # a 적분을 a로
check(1, s[0], f'(x(2)={X}, 오답 a를 at 대신 a로: {mis})')
assert mis == 6
# 원문: v=t^4-50t+a, x(5)=15, 선지 1..5 정답 ③=3
so = solve(integrate(t**4 - 50*t + a, (t, 0, 5)) - 15, a)
orig('J26', so[0], 3)

# ---------- 2번 (M2)
f = -x**3 + 3*x**2 + 9*x + a
lo, hi = -2, 2
crit = [r for r in solve(diff(f, x), x) if lo <= r <= hi]
cand = [lo, hi] + crit
vals = {c: f.subs(x, c) for c in cand}
# 최댓값·최솟값을 주는 점은 a와 무관(모두 a + 상수) → 상수부 비교
consts = {c: vals[c] - a for c in cand}
cmax = max(consts, key=lambda c: consts[c]); cmin = min(consts, key=lambda c: consts[c])
sa = solve(vals[cmax] - 20, a); assert len(sa) == 1
m = vals[cmin].subs(a, sa[0])
# 함정: 구간 밖 극댓값 f(3)을 최댓값으로
a_wrong = solve(f.subs(x, 3) - 20, a)[0]
m_wrong = vals[cmin].subs(a, a_wrong)
check(2, m, f"(f'={factor(diff(f, x))}, 후보 {consts}, 최대점 {cmax}, 최소점 {cmin}, a={sa[0]}, 함정값 {m_wrong})")
assert m_wrong == -12
# 원문: [1,4], -x^3+3x^2+a, 최댓값 8 → 최솟값 -12
fo = -x**3 + 3*x**2 + a
co = [1, 4] + [r for r in solve(diff(fo, x), x) if 1 <= r <= 4]
cv = {c: fo.subs(x, c) - a for c in co}
ao = solve(fo.subs(x, max(cv, key=lambda c: cv[c])) - 8, a)[0]
orig('M2', fo.subs(x, min(cv, key=lambda c: cv[c])).subs(a, ao), -12)

# ---------- 3번 (I55)
I3 = integrate(x, (x, 0, 5)) + integrate(2 - x, (x, 0, 2)) + integrate(x - 2, (x, 2, 5))
I3b = integrate(x + Abs(x - 2), (x, 0, 5))
assert I3 == I3b
w_left = integrate(x, (x, 0, 5)) + integrate(x - 2, (x, 2, 5))       # 왼쪽 삼각형 누락
w_abs = integrate(2*x - 2, (x, 0, 5))                               # 절댓값 무시
check(3, I3, f'(Abs 직접 {I3b}, 왼쪽 누락 {w_left}, 절댓값 무시 {w_abs})')
assert [w_left, w_abs] == [17, 15]
orig('I55', integrate(x + Abs(x - 3), (x, 1, 4)), 10)

# ---------- 4번 (D55)
f4 = 2*x**3 + a*x + 12
sa4 = solve(diff(f4, x).subs(x, -1), a); assert len(sa4) == 1
g = f4.subs(a, sa4[0]); gp = diff(g, x)
cps = sorted(solve(gp, x))
assert diff(g, x, 2).subs(x, -1) < 0          # x=-1 극대 확인
mins = [c for c in cps if diff(g, x, 2).subs(x, c) > 0]
assert len(mins) == 1                          # 극소점 유일
check(4, g.subs(x, mins[0]), f'(a={sa4[0]}, 극점 {cps}, 극댓값 {g.subs(x, -1)}, f(0)={g.subs(x, 0)})')
assert g.subs(x, -1) == 16 and g.subs(x, 0) == 12
fo4 = x**3 + a*x + 9
ao4 = solve(diff(fo4, x).subs(x, -1), a)[0]
go = fo4.subs(a, ao4)
orig('D55', [go.subs(x, c) for c in solve(diff(go, x), x) if diff(go, x, 2).subs(x, c) > 0][0], 7)

# ---------- 단원·정답 번호
assert [IT[k]['key'][0] for k in sorted(IT)] == ['J', 'M', 'I', 'D']
print('정답 위치:', [IT[k]['ans'] for k in sorted(IT)])
print('ALL OK' if ok else 'FAIL')
assert ok
