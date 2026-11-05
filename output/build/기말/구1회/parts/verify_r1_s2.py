# -*- coding: utf-8 -*-
"""1회 서답형2 교체(D64 구조 변경) 검증: sympy + 수치 전수 점검"""
import os, numpy as np, sympy as sp

ok = True
def chk(c, msg):
    global ok
    print(('OK  ' if c else 'FAIL'), msg); ok &= bool(c)

x, t, a, b, c = sp.symbols('x t a b c', real=True)
f = x**3 + a*x**2 + b*x + c
s = sp.expand(sp.diff(f, x).subs(x, t) - t**2 + 2*t + 4)
chk(sp.Poly(s, t).LC() == 2, 'RHS s(t) convex (t^2 coeff 2)')
av = sp.solve(sp.Eq(sp.solve(sp.diff(s, t), t)[0], 1), a)[0]
chk(av == -3, 'vertex t=1 -> a=-3')
f1 = f.subs(a, -3); s1 = s.subs(a, -3)
cv = sp.solve(sp.Eq(f1.subs(x, 3), s1.subs(t, 1)), c)[0]
chk(sp.simplify(cv - (2 - 2*b)) == 0, 'g(1)=3 -> c=2-2b')
F = f1.subs(c, cv)
chk(sp.simplify(F.subs(x, 2)) == -2, '(1) f(2)=-2 (b independent)')
chk(sp.expand(F - F.subs(x, 3) - (x - 3)*(x**2 + b)) == 0, 'f(x)-f(3)=(x-3)(x^2+b)')

# numeric g(t)
def maxroot(co, y):
    r = np.roots([1, co[0], co[1], co[2] - y])
    rr = r[np.abs(r.imag) < 1e-7].real
    return rr.max()
def gfun(A, B, C, T):
    return np.array([maxroot((A, B, C), (3*tt*tt + 2*A*tt + B) - tt*tt + 2*tt + 4) for tt in T])
T = np.linspace(-6, 8, 14001)
def cond(A, B, C):
    G = gfun(A, B, C, T); i = int(np.argmin(G))
    return abs(T[i] - 1) < 2e-3 and abs(G[i] - 3) < 1e-6 and np.all(G[np.abs(T - 1) > 0.05] > 3 + 1e-9)

# 양성: a=-3, c=2-2b, b>=-9
good = [bb for bb in np.arange(-14, 9.01, 0.5) if cond(-3, bb, 2 - 2*bb)]
chk(abs(min(good) + 9) < 1e-9 and all(bb in good for bb in np.arange(-9, 9.01, 0.5)), f'feasible b grid = [-9, ...] (min {min(good)})')
chk(not cond(-3, -9.25, 2 + 18.5) and not cond(-3, -10, 22), 'b<-9 fails (3 not max root)')
# 음성: a, c 어긋나면 실패
bad = sum(cond(A, B, 2 - 2*B + dc) for A in (-3.5, -2.5, -3) for B in (-8, -2, 1, 4) for dc in ((0.3, -0.3) if A == -3 else (0, 0.4)))
chk(bad == 0, 'perturbed a or c never satisfies condition (uniqueness of a, c relation)')

# (2) 극값 존재 b<3, 정수 개수
ints = [k for k in range(-30, 30) if k >= -9 and 36 - 12*k > 0]
chk(len(ints) == 12 and ints[0] == -9 and ints[-1] == 2, f'(2) integer f\'(0) count = {len(ints)}')
chk(all(cond(-3, k, 2 - 2*k) for k in ints), '(2) every counted b satisfies condition numerically')
chk(not cond(-3, -10, 22), '(2) b=-10 excluded')
chk(len([k for k in ints if k <= 0]) == 10 and len([k for k in ints if k > 0]) == 2 and len(ints) - 1 == 11, 'wrong-answer values 10, 2, 11 distinct from 12')

# (3) 미분가능성
def slopes(B, t0, h=1e-6):
    C = 2 - 2*B; g0 = gfun(-3, B, C, [t0])[0]
    gr = gfun(-3, B, C, [t0 + h])[0]; gl = gfun(-3, B, C, [t0 - h])[0]
    return (gr - g0)/h, (g0 - gl)/h
r, l = slopes(-9, 1)
chk(abs(r - 1/np.sqrt(3)) < 1e-3 and abs(l + 1/np.sqrt(3)) < 1e-3, f'(3) b=-9: corner at t=1 (right {r:.4f}, left {l:.4f})')
def smooth(B):
    pts = np.linspace(-5, 7, 241)
    return max(abs(np.subtract(*slopes(B, p))) for p in pts) < 1e-3
chk(all(smooth(B) for B in (-8, -5, 0, 2, 3, 6)), '(3) b>-9: g differentiable everywhere (left=right derivative on grid incl. t=1)')
chk(not smooth(-9), '(3) b=-9 not differentiable')
# also b=3 (f'=3(x-1)^2): max root stays >=3, smooth
f0 = {k: 2 - 2*k for k in range(-9, 40)}
best = max(f0[k] for k in f0 if k > -9)
chk(best == 18, f'(3) max f(0) with integer b>-9 = {best}')
chk(f0[-9] == 20, 'trap value 20 at b=-9')
# 원본 판정 학생의 답 (b=-9만) 과 다른지
chk(1 != 12 and 20 != 18, 'original-principle answers (1, 20) differ from correct (12, 18)')

# 부품 형식
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r1_s2.py')).read(), ns)
S = ns['SITEMS']
chk(list(S) == ['S2'], 'only S2')
it = S['S2']
chk(it['ans'] == ['(1) −2', '(2) 12', '(3) 18'], 'ans strings')
chk([q[1][:2] for q in it['subs']] == ['4점', '4점', '2점'] and all('답만' in q[1] for q in it['subs']), '4+4+2 답만')
chk(all(k in it for k in ('rubric', 'fast', 'note', 'sol', 'wrong', 'key', 'src', 'var', 'level')) and len(it['rubric']) == 3, 'fields present')
txt = it['body'] + ''.join(q[0] for q in it['subs'])
chk(not any(ch in txt for ch in ('W', 'V', 'Y', 'Z')), 'no forbidden capitals in math')
print('ALL PASS' if ok else 'SOME FAILED')
