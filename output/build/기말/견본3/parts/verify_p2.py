# -*- coding: utf-8 -*-
# p2.py (견본3 5–8번) 정답 검증: 계산값 = 지정 선지, 정답 번호, 유일성, 선지 등차·서로 다름, 오답 값이 선지에 있음, 원문 정답
import os, sys
from sympy import (symbols, Rational, sqrt, diff, integrate, solve, factor, sympify, nsimplify, Piecewise,
                   Abs, simplify, expand, Poly, real_roots, S)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
x, t = symbols('x t', real=True)
a, b, c, C, k = symbols('a b c C k', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 5, 6: 2, 7: 4, 8: 1}
KEY = {5: 'D18', 6: 'J2', 7: 'I41', 8: 'I14'}
ok = True

def ch(no):
    return [nsimplify(sympify(s)) for s in IT[no]['choices']]

def arith(no):
    v = ch(no); d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def check(no, val, wrongs, note=''):
    global ok
    v = ch(no)
    g = (simplify(sympify(val) - v[IT[no]['ans'] - 1]) == 0) and IT[no]['ans'] == WANT[no] and arith(no) \
        and IT[no]['key'] == KEY[no] and all(w in v and w != val for w in wrongs)
    ok &= g
    print(f'{no}번: 계산 {val}, 선지 {v[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {wrongs} {"OK" if g else "FAIL"} {note}')

def sign_change(fp, x0, eps=Rational(1, 10**6)):
    l, r = fp.subs(x, x0 - eps), fp.subs(x, x0 + eps)
    return (l > 0) != (r > 0)

# ---------- 5번 ----------
f5 = x**4 + a*x**3 + b*x**2 + c
fp5 = diff(f5, x)
# f'(3)=0 → a를 b로 표시. b≠0 이면 f'=x·q(x), q(0)=2b≠0 이라 x=0에서 부호가 바뀜 → 극값 존재. 따라서 b=0.
q = expand(fp5 / x)
assert q.subs(x, 0) == 2*b
# 수치로 b≠0 몇 개 확인 (a는 f'(3)=0에서)
for bv in [-5, -1, Rational(1, 3), 2, 7]:
    av = solve(fp5.subs({x: 3, b: bv}), a)[0]
    assert sign_change(fp5.subs({a: av, b: bv}), 0)
sol5 = solve([fp5.subs({x: 3, b: 0}), f5.subs({x: 3, b: 0}) + 20], [a, c], dict=True)
assert len(sol5) == 1
s5 = dict(sol5[0]); s5[b] = 0
fp5s = fp5.subs(s5); f5s = f5.subs(s5)
assert not sign_change(fp5s, 0)                      # x=0 극값 없음
assert fp5s.subs(x, 3 - Rational(1, 100)) < 0 < fp5s.subs(x, 3 + Rational(1, 100))   # x=3 극소
assert f5s.subs(x, 3) == -20
ans5 = s5[a] + s5[b] + s5[c]
check(5, ans5, [s5[c], f5s.subs(x, 1)], f'(f={f5s}, f\'={factor(fp5s)})')

# ---------- 6번 ----------
r3 = sqrt(3)
A6 = integrate(3 - x**2, (x, -r3, r3))
B6 = integrate(x**2 - 3, (x, r3, k))
ks = [s for s in solve(A6 - B6, k) if s.is_real and s > r3]
assert len(ks) == 1
assert simplify(expand(3 * (B6 - A6)) - (k - 2*r3) * (k + r3)**2) == 0
# B는 k>√3에서 증가 → 유일
assert simplify(diff(B6, k) - (k**2 - 3)) == 0
ans6 = simplify(ks[0]**2)
# 오답: ∫_0^k (x^2-3)=0 (A=2B 원문 방식)
kw = [s for s in solve(integrate(x**2 - 3, (x, 0, k)), k) if s.is_real and s > r3][0]
assert simplify(A6 - 2 * integrate(x**2 - 3, (x, r3, kw))) == 0
check(6, ans6, [simplify(kw**2)], f'(A={A6}, k={ks[0]})')

# ---------- 7번 ----------
inner = 3*x**2 + 2*x; outer = a*x**3 + b*x**2
s7 = solve([inner.subs(x, 1) - outer.subs(x, 1), inner.subs(x, -1) - outer.subs(x, -1)], [a, b], dict=True)
assert len(s7) == 1
o7 = outer.subs(s7[0])
fp7 = Piecewise((o7, x <= -1), (inner, x < 1), (o7, True))
f2 = integrate(inner, (x, 0, 1)) + integrate(o7, (x, 1, 2))
fm2 = -(integrate(o7, (x, -2, -1)) + integrate(inner, (x, -1, 0)))
assert integrate(fp7, (x, 0, 2)) == f2 and -integrate(fp7, (x, -2, 0)) == fm2
ans7 = f2 + fm2
check(7, ans7, [f2 - fm2], f'(a,b={s7[0]}, f(2)={f2}, f(-2)={fm2})')

# ---------- 8번 ----------
# f를 n차 다항식으로 두고 항등식 전수 풀이(차수 1..6)
sols8 = []
for n in range(0, 7):
    cs = symbols(f'c0:{n + 1}')
    fx = sum(cs[i] * x**i for i in range(n + 1))
    eq = expand(x * fx - (integrate(fx.subs(x, t), (t, 2, x)) + 3*x**4 - 6*x**2))
    s = solve(Poly(eq, x).all_coeffs(), cs, dict=True)
    for d in s:
        sols8.append(expand(fx.subs(d)))
sols8 = list({str(e): e for e in sols8}.values())
assert len(sols8) == 1 and not sols8[0].free_symbols - {x}
f8 = sols8[0]
crit = solve(diff(f8, x), x)
mins = [p for p in crit if diff(f8, x, 2).subs(x, p) > 0]
assert len(mins) == 1
ans8 = f8.subs(x, mins[0])
# 오답: x=2 대입 때 좌변 x 누락 → f(2)=P(2)=24
fw = 4*x**3 - 12*x + C
Cw = solve(fw.subs(x, 2) - 24, C)[0]
check(8, ans8, [fw.subs(C, Cw).subs(x, 1)], f'(f={f8}, 극소 x={mins[0]})')

# ---------- 원문 직접 풀이 ----------
orig = {}
# D18: f=x^4-2x^2+ax+b, x=0 극대 → a=0, 극솟값 3
g = x**4 - 2*x**2 + a*x + b
av = solve(diff(g, x).subs(x, 0), a)[0]
bv = solve(g.subs({a: av, x: 1}) - 3, b)[0]
assert g.subs({a: av, b: bv, x: -1}) == 3
orig['D18'] = (av + bv, 4)
# J2: |x^2-1|, A=2B
A0 = integrate(1 - x**2, (x, -1, 1))
kk = [s for s in solve(A0 - 2 * integrate(x**2 - 1, (x, 1, k)), k) if s.is_real and s > 1]
assert len(kk) == 1
orig['J2'] = (kk[0], sqrt(3))
# I41
fpo = Piecewise((-4*x**3 + x**2, x <= -1), (x**2 - 4*x, x < 1), (-4*x**3 + x**2, True))
orig['I41'] = (simplify(integrate(fpo, (x, -2, 0)) / (-integrate(fpo, (x, 0, 2)))), Rational(59, 43))
# I14
cs = symbols('d0:5'); fx = sum(cs[i] * x**i for i in range(5))
eq = expand(x * fx - (integrate(fx.subs(x, t), (t, 2, x)) + 3*x**4 - 4*x**2))
so = solve(Poly(eq, x).all_coeffs(), cs, dict=True)
assert len(so) == 1
orig['I14'] = (fx.subs(so[0]).subs(x, 3), 84)
CIRC = '①②③④⑤'
for kname, (got, want) in orig.items():
    item = F.I[kname]
    if item[1]:   # 원문 선지에서 정답 번호의 값과 대조
        tx = item[1][CIRC.index(item[2])]
        assert tx in {'4', '\\sqrt3', '\\dfrac{59}{43}'}, tx
    g_ok = simplify(got - want) == 0
    ok &= g_ok
    print(f'원문 {kname}: 직접 풀이 {got}, 원문 정답 {item[2]} → {want} {"OK" if g_ok else "FAIL"}')

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
assert ok
print('ALL OK')
