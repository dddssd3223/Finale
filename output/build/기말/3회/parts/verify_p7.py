# -*- coding: utf-8 -*-
# 서답형1 (자체, J1 유형) · 서답형2 (J59 구조 변경) 검증 · author='claude'
import sympy as sp, os, sys
x, t, k, m = sp.symbols('x t k m', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def area_numeric(gfun, a, b, n=4000):
    """구간 [a,b]에서 y=gfun(x)와 x축 사이 (gfun>=0인 부분) 넓이, 사다리꼴 수치 적분"""
    h = (b - a) / n; s = 0.0
    for i in range(n + 1):
        v = max(gfun(a + i * h), 0.0)
        s += v * (0.5 if i in (0, n) else 1.0)
    return s * h


# ================= S1 =================
def S1_setup(f, slope, lo, hi):
    """f: x<t 곡선, x>=t 기울기 slope(<0) 직선. 0<t<lo..hi 에서 f(t)>0 가정. 넓이 함수 S(t)"""
    ft = f.subs(x, t)
    return sp.integrate(f, (x, 0, t)) + ft**2 / (2 * (-slope))

# --- 원문 J1: f=x(x-6)(x-9)/9, 기울기 -1, 0<t<6 → 129/4
fo = x * (x - 6) * (x - 9) / 9
So = S1_setup(fo, -1, 0, 6)
So_d = sp.factor(sp.diff(So, t))
crit = [r for r in sp.solve(sp.diff(So, t), t) if r.is_real and 0 < r < 6]
assert crit == [3] and So.subs(t, 3) == R(129, 4)
assert F.I['J1'][2] == '③' and F.I['J1'][1][2] == '\\dfrac{129}4'
print('J1 원문 OK: t=3, 최댓값 129/4 (원문 정답 ③)')

# --- S1: f=4x(x-2)(x-7), 기울기 -4, 0<t<2
f1 = 4 * x * (x - 2) * (x - 7)
assert sp.expand(f1) == 4 * x**3 - 36 * x**2 + 56 * x
for tv in [R(i, 100) for i in range(1, 200)]: assert f1.subs(x, tv) > 0          # 0<t<2 에서 f(t)>0
assert all(f1.subs(x, -R(i, 10)) < 0 for i in range(1, 50))                    # x<0 에서 f<0 (영역 왼쪽 끝은 x=0)
S = S1_setup(f1, -4, 0, 2)
dS = sp.diff(S, t)
assert sp.simplify(dS - f1.subs(x, t) * (4 + sp.diff(f1, x).subs(x, t)) / 4) == 0
assert sp.expand(4 + sp.diff(f1, x) - 12 * (x - 1) * (x - 5)) == 0
assert sp.expand(dS - 12 * t * (t - 7) * (t - 5) * (t - 2) * (t - 1)) == 0
# 부호: (0,1) 양, (1,2) 음 → t=1 에서 최대 (전수: 0<t<2 의 정지점은 t=1 하나)
crit1 = [r for r in sp.solve(dS, t) if 0 < r < 2]
assert crit1 == [1]
assert all(dS.subs(t, R(i, 100)) > 0 for i in range(1, 100)) and all(dS.subs(t, R(i, 100)) < 0 for i in range(101, 200))
assert sp.integrate(f1, (x, 0, 1)) == 17 and f1.subs(x, 1) == 24 and f1.subs(x, 1)**2 / 8 == 72
ANS1 = S.subs(t, 1)
assert ANS1 == 89 and S1['ans'] == [r'\(89\)']
# 끝값: t→0+ 이면 0, t→2- 이면 ∫_0^2 f = 32 < 89 (최댓값은 내부 t=1)
assert sp.limit(S, t, 0, '+') == 0 and sp.limit(S, t, 2, '-') == 32
# 접선 x절편 = 남은 근 7 (숨은 관계 보존)
assert 1 + f1.subs(x, 1) / 4 == 7
# 넓이 식이 실제 그래프 넓이와 같은지 수치 확인 (t=1/2, 1, 3/2)
for tv in [R(1, 2), 1, R(3, 2)]:
    ft = float(f1.subs(x, tv)); fl = sp.lambdify(x, f1)
    g = lambda xx, tv=float(tv), ft=ft, fl=fl: fl(xx) if xx < tv else -4 * (xx - tv) + ft
    num = area_numeric(g, 0.0, float(tv) + ft / 4)
    assert abs(num - float(S.subs(t, tv))) < 1e-3, (tv, num)
# 오답 값
assert sp.integrate(f1, (x, 0, 1)) + f1.subs(x, 1)**2 / 2 == 305
assert sp.integrate(f1, (x, 0, 1)) + f1.subs(x, 1)**2 / 4 == 161
sol_m1 = sp.solve(sp.diff(f1, x) + 1, x)
assert all(not r.is_rational for r in sol_m1)                                  # f'(t)=-1 로 풀면 무리수
print('S1 OK: S(t)=∫_0^t f + f(t)^2/8, S\'(t)=3f(t)(t-1)(t-5), 0<t<2 에서 t=1 최대, 최댓값 89')

# ----- 조건 빼 보기 S1
def abl1(cname, msg): print(f'ABLATION S1 {cname}: {msg}')
# (a) 0<t<2 삭제: t>7 이면 [7, t+f(t)/4] 의 영역 넓이가 한없이 커짐 → 최댓값 없음
Sbig = sp.integrate(f1, (x, 7, t)) + f1.subs(x, t)**2 / 8
assert sp.limit(Sbig, t, sp.oo) == sp.oo
abl1('범위 0<t<2', '필요(없으면 t>7에서 넓이가 한없이 커져 최댓값 없음)')
# (b) 기울기 -4 → 기울기 -m 일반: 최댓값이 m 에 따라 달라짐 (m=1 이면 89/4가 아닌 값)
Sm = sp.integrate(f1, (x, 0, t)) + f1.subs(x, t)**2 / (2 * m)
vals = {}
for mv in [1, 2, 4, 8]:
    Sv = Sm.subs(m, mv); cs = [r for r in sp.solve(sp.diff(Sv, t), t) if r.is_real and 0 < r < 2]
    assert len(cs) == 1
    vals[mv] = sp.nsimplify(Sv.subs(t, cs[0]))
assert vals[4] == 89 and len(set(vals.values())) == 4
abl1('기울기 -4', '필요(기울기 -m의 최댓값이 ' + ', '.join(f'm={a}: {float(b):.4f}' for a, b in vals.items()) + '로 달라짐, 정수 답은 m=4일 때)')
# (c) 계수 4 → 1 (같은 기울기 -4): 최대 위치·값이 바뀜
f1b = x * (x - 2) * (x - 7); Sb = sp.integrate(f1b, (x, 0, t)) + f1b.subs(x, t)**2 / 8
cs = [r for r in sp.solve(sp.diff(Sb, t), t) if r.is_real and 0 < r < 2]
assert cs == [] or Sb.subs(t, cs[0]) != 89
abl1('계수 4', '필요(계수 1이면 0<t<2에 정지점이 없어 최댓값 없음, 접선 관계가 깨짐)' if cs == [] else f'필요(계수 1이면 최댓값 {float(Sb.subs(t, cs[0])):.4f}로 달라짐)')

# ================= S2 =================
def count(F_, G_, kv):
    """F_(x)=G_(x)+kv 꼴이 아니라 h(x)=kv: h 는 (왼쪽식, 오른쪽식), x<0 / x>=0. 서로 다른 실근 수"""
    hl, hr = F_, G_
    rs = set()
    for r in set(sp.Poly(sp.expand(hl - kv), x).real_roots()):
        if r < 0: rs.add(r)
    for r in set(sp.Poly(sp.expand(hr - kv), x).real_roots()):
        if r >= 0: rs.add(r)
    return len(rs), rs

# --- 원문 J59: f=x^3+x^2-x, g=4|x|+k, k<0, 교점 2 → 30S = 80
fo2 = x**3 + x**2 - x
hoL, hoR = fo2 + 4 * x, fo2 - 4 * x
ko = [kv for kv in [R(j, 4) for j in range(-80, 0)] if count(hoL, hoR, kv)[0] == 2]
assert ko == [-3]
So2 = sp.integrate(fo2 - (-4 * x - 3), (x, -1, 0)) + sp.integrate(fo2 - (4 * x - 3), (x, 0, 1))
assert So2 == R(8, 3) and 30 * So2 == 80 and F.I['J59'][2] == '80'
print('J59 원문 OK: k=-3, S=8/3, 30S=80 (원문 정답 80)')

# --- S2: f=x^3-x^2, g=2x|x|+k
f2 = x**3 - x**2
gL, gR = -2 * x**2, 2 * x**2               # 2x|x| : x<0 → -2x^2, x>=0 → 2x^2
assert all(sp.Abs(2 * xv * sp.Abs(xv)) == sp.Abs(gL.subs(x, xv) if xv < 0 else gR.subs(x, xv)) for xv in [R(-3), R(-1, 2), 0, R(1, 3), 2])
hL, hR = sp.expand(f2 - gL), sp.expand(f2 - gR)     # h = f - 2x|x|
assert hL == x**3 + x**2 and hR == x**3 - 3 * x**2
# g 는 x=0 에서 미분가능 (꺾이지 않음), g'(x)=4|x|
assert sp.diff(gL, x).subs(x, 0) == sp.diff(gR, x).subs(x, 0) == 0
# 개수 표: 임계값 k = -4 (오른쪽 극소), 0 (h(0)), 4/27 (왼쪽 극대)
assert sp.solve(sp.diff(hR, x), x) == [0, 2] and hR.subs(x, 2) == -4
assert sp.solve(sp.diff(hL, x), x) == [-R(2, 3), 0] and hL.subs(x, -R(2, 3)) == R(4, 27)
grid = sorted(set([R(j, 8) for j in range(-80, 9)] + [R(-4), R(0), R(4, 27), R(-4) + R(1, 1000), R(-4) - R(1, 1000), R(4, 27) + R(1, 1000), R(4, 27) - R(1, 1000)]), key=float)
def expect(kv):
    if kv < -4: return 1
    if kv == -4: return 2
    if kv < 0: return 3
    if kv == 0: return 3
    if kv < R(4, 27): return 3
    if kv == R(4, 27): return 2
    return 1
for kv in grid: assert count(hL, hR, kv)[0] == expect(kv), (kv, count(hL, hR, kv))
K2 = [kv for kv in grid if kv < 0 and count(hL, hR, kv)[0] == 2]
assert K2 == [-4]
# 대수적 전수: k<0 에서 교점 2 가 되려면 어느 한 쪽 다항식이 중근 → 판별식 0 인 k 만 후보
cand = set()
for P in (hL, hR):
    for r in sp.solve(sp.discriminant(sp.Poly(P - k, x).as_expr(), x), k): cand.add(r)
cand_neg = [c for c in cand if c.is_real and c < 0]
assert cand_neg == [-4], cand
assert S2['ans'][0] == r'(1) \(k=-4\)'
print('S2 (1) OK: k<0 에서 교점 개수 1(k<-4)·2(k=-4)·3(-4<k<0), 유일한 k=-4')

# (2) 넓이
assert sp.expand(hR + 4 - (x - 2)**2 * (x + 1)) == 0 and sp.expand(hL + 4 - (x + 2) * (x**2 - x + 2)) == 0
assert sp.discriminant(x**2 - x + 2, x) < 0
n2, rs2 = count(hL, hR, -4); assert rs2 == {-2, 2}
for xv in [R(i, 10) for i in range(-19, 20)]:
    hv = hL.subs(x, xv) if xv < 0 else hR.subs(x, xv)
    assert hv + 4 > 0 or xv == 2                     # -2<x<2 에서 f>g
A_L = sp.integrate(hL + 4, (x, -2, 0)); A_R = sp.integrate(hR + 4, (x, 0, 2))
assert A_L == R(20, 3) and A_R == 4
ANS2 = A_L + A_R
assert ANS2 == R(32, 3) and S2['ans'][1] == r'(2) \(\dfrac{32}{3}\)'
# 수치 확인: |f - g| 를 [-2,2] 에서 직접 적분
fl = sp.lambdify(x, f2)
num = area_numeric(lambda xx: fl(xx) - (2 * xx * abs(xx) - 4), -2.0, 2.0, 20000)
assert abs(num - 32 / 3) < 1e-4
# 다른 둘러싸인 부분 없음: x>2 에서 f>g (접점 뒤 다시 만나지 않음), x<-2 에서 f<g
assert all(hR.subs(x, R(i, 2)) + 4 > 0 for i in range(5, 40)) and all(hL.subs(x, -R(i, 2)) + 4 < 0 for i in range(5, 40))
# 오답 값
assert sp.integrate(sp.expand((x - 2)**2 * (x + 1)), (x, -1, 2)) == R(27, 4)   # |x| 무시
assert count(hL, hR, R(4, 27))[0] == 2                                           # k<0 무시 시 다른 답
assert count(hL, hR, 0)[1] == {-1, 0, 3}                                         # k=0 은 3개
print('S2 (2) OK: 교점 -2, 2(접점), 넓이 20/3 + 4 = 32/3')

# ----- 조건 빼 보기 S2
def abl2(cname, msg): print(f'ABLATION S2 {cname}: {msg}')
Kall = [kv for kv in grid if count(hL, hR, kv)[0] == 2]
assert Kall == [-4, R(4, 27)]
abl2('k<0', '필요(없으면 k=4/27(x<0 쪽 극댓값에서 접함)도 교점 2개 → (1)의 답이 둘)')
# 절댓값 삭제: g=2x^2+k 이면 (1)은 같은 -4 이지만 교점이 -1, 2 로 바뀌어 (2) 넓이 27/4
hN = sp.expand(f2 - 2 * x**2)
KN = [kv for kv in grid if kv < 0 and count(hN, hN, kv)[0] == 2]
assert KN == [-4] and sp.integrate(hN + 4, (x, -1, 2)) == R(27, 4)
abl2('절댓값 |x|', '필요(g=2x^2+k이면 (2)의 넓이가 27/4로 바뀜, x<0 쪽 판단이 사라짐)')
# 개수 조건 2 → 3 으로 바꾸면 k 가 구간 (-4,0) 이 되어 정해지지 않음
K3 = [kv for kv in grid if kv < 0 and count(hL, hR, kv)[0] == 3]
assert len(K3) > 5
abl2('교점 개수 2', '필요(개수를 바꾸면 k가 범위로 남아 하나로 정해지지 않음)')
# f 의 이차항 -x^2 삭제(f=x^3): 왼쪽이 x^3+2x^2, 오른쪽 x^3-2x^2 → k 와 넓이가 바뀜
hL0, hR0 = sp.expand(x**3 + 2 * x**2), sp.expand(x**3 - 2 * x**2)
K0 = [kv for kv in sorted(set([R(j, 54) for j in range(-300, 0)]), key=float) if count(hL0, hR0, kv)[0] == 2]
assert K0 and K0 != [-4]
abl2('f의 -x^2', f'필요(f=x^3이면 k={K0}로 바뀜)')

print('ALL OK')
