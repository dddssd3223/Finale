# -*- coding: utf-8 -*-
# p5.py (견본3 17번, J47 구조 변경) sympy 전수 검증
import os
import numpy as np
from sympy import (symbols, Rational, integrate, solve, sqrt, simplify, factor, sympify, nsimplify,
                   diff, Poly, real_roots, S as SS, oo, Interval, solveset, limit)
x, a, b, p, q = symbols('x a b p q', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
it = ns['ITEMS'][17]
ok = True
def chk(cond, msg):
    global ok
    ok &= bool(cond); print(('OK  ' if cond else 'FAIL') + ' ' + msg)

# ---------- 0. 원문 J47 직접 풀이 ----------
# 일반 f: f, f^-1 모두 (0,0), (±3,∓3) 지남, [-3,0]에서 ∫f=2 < 삼각형 9/2 → 넓이 4(9/2-2)=10
orig = 4 * (Rational(9, 2) - 2)
# 구체 예로 확인: f(x) = -x + x(x^2-9)(c0 + c1 x^2) 중 감소·교점 3개·∫=2 인 것 하나
c0, c1 = symbols('c0 c1', real=True)
F = -x + x*(x**2 - 9)*(c0 + c1*x**2)
eq = integrate(F, (x, -3, 0)) - 2
c0v = solve(eq.subs(c1, Rational(-1, 200)), c0)[0]
Fo = F.subs({c1: Rational(-1, 200), c0: c0v})
xs = np.linspace(-6, 6, 120001)
fpo = np.array([float(v) for v in [0]]) if False else None
from sympy import lambdify
fpn = lambdify(x, diff(Fo, x), 'numpy')(xs)
g_roots = [r for r in real_roots(Poly((Fo + x).expand() * 1, x))]
chk(np.all(fpn <= 1e-12) and len(set(g_roots)) == 3 and Fo.subs(x, 3) == -3,
    f'원문 예시 f 감소·y=-x 교점 {sorted(set(g_roots))}·f(3)=-3')
area_o = 4 * abs(integrate(Fo + x, (x, 0, 3)))
chk(area_o == orig == 10, f'원문 넓이 {area_o} = 원문 정답 ② 10')

# ---------- 1. 새 문항: 분기 전수 ----------
f = a*x**3 + b*x
fp = diff(f, x)                      # 3ax^2+b
I = integrate(f, (x, -2, 0))         # -(4a+2b)
# (1) 역함수 존재 ⇔ 증가(a>=0,b>=0) 또는 감소(a<=0,b<=0), a=b=0 제외
#     증가: I = -(4a+2b) <= 0 ≠ 1/2 → 탈락
chk(all(I.subs({a: A, b: B}) <= 0 for A in [0, Rational(1, 3), 2] for B in [0, Rational(1, 5), 3] if (A, B) != (0, 0)),
    '증가 분기: ∫_{-2}^0 f ≤ 0 → (나) 모순')
aval = solve(I - Rational(1, 2), a)[0]
chk(simplify(aval + (4*b + 1)/8) == 0, f'(나) → a = {aval}')
# (2) 감소 분기: a<=0, b<=0 → b >= -1/4 ; a=0(b=-1/4)은 직선 y=-x/4, 역함수 y=-4x → 교점 1개
lin = -x/4; lin_inv = -4*x
chk(solve(lin - lin_inv, x) == [0], 'a=0 분기: 두 직선은 원점에서만 만남 → (가) 모순')
# a>0,b<0 / a<0,b>0: 역함수 없음 (f'의 부호가 바뀜)
for B in [Rational(1, 2), 3, Rational(-1, 2), -5]:
    A = aval.subs(b, B)
    roots = solve(fp.subs({a: A, b: B}), x)
    chk(A * B < 0 and len(roots) == 2, f'b={B}: a={A}, f\'=0 근 {roots} → 단조 아님, 역함수 없음')
# (3) 유효 구간 -1/4 < b <= 0 : 교점 개수 전수(수치) — f(f(x))=x 의 실근이 정확히 3개이고 모두 y=-x 위
def inter_count(B):
    A = aval.subs(b, B); fb = f.subs({a: A, b: B})
    ff = fb.subs(x, fb) - x
    rr = sorted(set(real_roots(Poly(ff.expand(), x))))
    ony = all(abs(float(fb.subs(x, r) + r)) < 1e-9 for r in rr)
    return len(rr), ony
Bs = [Rational(-1, 4) + Rational(k, 400) for k in range(1, 101)]   # (-1/4, 0]
res = [inter_count(B) for B in Bs]
chk(all(n == 3 and o for n, o in res), f'유효 구간 b 100개: f∘f(x)=x 실근 3개, 모두 y=-x 위')
# 교점이 y=-x 밖에 있을 수 없음(기호): p+q≠0 이면 a(p^2+q^2) = -b
e1 = (f.subs(x, p) - q) + (f.subs(x, q) - p)
e2 = (f.subs(x, p) - q) - (f.subs(x, q) - p)
# e1 = (p+q)(a(p^2-pq+q^2)+b-1), e2 = (p-q)(a(p^2+pq+q^2)+b+1)
chk(simplify(e1 - (p + q)*(a*(p**2 - p*q + q**2) + b - 1)) == 0 and simplify(e2 - (p - q)*(a*(p**2 + p*q + q**2) + b + 1)) == 0,
    '교점 (p,q) 식 인수분해')
chk(simplify((a*(p**2 - p*q + q**2) + b - 1) + (a*(p**2 + p*q + q**2) + b + 1) - 2*(a*(p**2 + q**2) + b)) == 0,
    '두 인수 합 = 2(a(p^2+q^2)+b) → a<0,b<=0 이면 p=q=0')
# (4) 넓이 S(b)
r2 = -(b + 1)/a
Sb = simplify((4*integrate(f + x, (x, 0, sqrt(r2)))).subs(a, aval))
chk(simplify(Sb - 8*(b + 1)**2/(4*b + 1)) == 0, f'S(b) = {factor(Sb)}')
# 0<x<r 에서 f(x) > -x (위아래) 확인
chk(all(float((f + x).subs({a: aval.subs(b, B), b: B}).subs(x, sqrt(r2.subs(a, aval).subs(b, B))/2)) > 0 for B in Bs),
    '0<x<r 에서 f(x)+x>0')
# 넓이를 수치로(역함수 직접): b=0, -1/8, -1/5 에서 ∫|f - f^{-1}| (x로 적분, 역함수는 수치 이분법)
def numarea(B):
    A = float(aval.subs(b, B)); Bf = float(B)
    fn = lambda t: A*t**3 + Bf*t
    def finv(y):
        lo, hi = -50.0, 50.0
        for _ in range(100):
            mid = (lo + hi)/2
            if fn(mid) > y: lo = mid
            else: hi = mid
        return (lo + hi)/2
    R = float(sqrt(r2.subs(a, aval).subs(b, B)))
    ts = np.linspace(-R, R, 20001)
    d = np.abs(np.array([fn(t) - finv(t) for t in ts]))
    return float(np.sum((d[1:] + d[:-1])/2*np.diff(ts)))
for B in [0, Rational(-1, 8), Rational(-1, 5)]:
    na = numarea(B); sv = float(Sb.subs(b, B))
    chk(abs(na - sv) < 1e-3, f'b={B}: 수치 넓이 {na:.5f} = S(b) {sv:.5f}')
# (5) 최솟값: 구간 (-1/4, 0] 에서 S-8 = 8b(b-2)/(4b+1) >= 0, 등호 b=0 하나
chk(simplify(Sb - 8 - 8*b*(b - 2)/(4*b + 1)) == 0, 'S-8 = 8b(b-2)/(4b+1)')
grid = [Rational(-1, 4) + Rational(k, 10000) for k in range(1, 2501)]
vals = [Sb.subs(b, B) for B in grid]
chk(all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)), '(-1/4,0] 에서 S 감소(연속적으로 움직임)')
chk(limit(Sb, b, Rational(-1, 4), '+') == oo, 'b→-1/4+ 에서 S→∞ (최댓값 없음)')
ans = Sb.subs(b, 0)
crit = solve(diff(Sb, b), b)
chk(set(crit) == {-1, Rational(1, 2)}, f'S\'=0 : b={crit} (b=1/2 은 b<=0 밖 → 경계 b=0 에서 최소)')
chk(fp.subs({a: aval.subs(b, 0), b: 0}).subs(x, 0) == 0 and aval.subs(b, 0) == Rational(-1, 8),
    "최소일 때 f=-x^3/8, f'(0)=0 (경계 등호, 역함수 존재)")
print('정답', ans)

# ---------- 2. 선지·정답 ----------
ch = [sympify(c) for c in it['choices']]
chk(nsimplify(it['choices'][it['ans'] - 1]) == ans and it['ans'] == 3, f'정답 {ans} = 선지 {it["ans"]}번 (지정 ③)')
chk(len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1, f'선지 {ch} 서로 다름·등차')
# 오답 근거 값
w_orig = 4*(Rational(1, 2)*2*2 - Rational(1, 2))           # 교점 ±2 가정, 원문식
w_crit = Sb.subs(b, Rational(1, 2))                         # 역함수 조건 무시 극소
w_half = ans/2                                              # y=-x 와의 넓이만
chk(w_orig == w_crit == 6 and w_half == 4 and {6, 4} <= set(ch), f'오답 6(원문식 {w_orig}, 극소 {w_crit}), 4(절반 {w_half}) 선지에 있음')
chk('6' in it['wrong'] and '4' in it['wrong'], 'wrong 필드에 6, 4')
# b=1/2 은 실제로 역함수 없음
chk(solve(fp.subs({a: aval.subs(b, Rational(1, 2)), b: Rational(1, 2)}), x) != [], 'b=1/2 에서 f\'=0 두 근 → 역함수 없음')

print('ALL OK' if ok else 'SOME FAIL')
