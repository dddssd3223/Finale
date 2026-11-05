# -*- coding: utf-8 -*-
# 견본5 p2 (Claude 10·12·14·16번) 정답 검증 + 조건 빼 보기(ABLATION)
import os
import sympy as sp
from fractions import Fraction as Fr

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {10: 2, 12: 1, 14: 3, 16: 2}
x, t, s, a = sp.symbols('x t s a', real=True)
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.sympify(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, IT[no].get('author') == 'claude', "author='claude'")


def wrong_in(no, vals, why):
    v = ch(no)
    check(no, all(sp.sympify(w) in v and sp.sympify(w) != v[IT[no]['ans'] - 1] for w in vals), f'오답 {vals} 선지에 있음 ({why})')


def ablation(no, cname, vals, ans, why='', est=False, undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(vals), key=lambda v: float(v))
        if sv == [ans]:
            msg = f'성립 조건(답 그대로 {ans}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


# ================= 원문 직접 풀이 =================
# J60: f(x)=f(x-3)+4 이면 f(x)-(4/3)x 는 주기 3 → G(u)=∫_u^{u+3} f 는 기울기 4 일차식
c0 = sp.symbols('c0')
fJ = sp.Rational(4, 3)*x + c0
cJ = sp.solve(sp.integrate(fJ, (x, 0, 6)), c0)[0]
fJ = fJ.subs(c0, cJ)
check('J60', sp.integrate(fJ, (x, 6, 9)) == 18 and fJ.subs(x, 6) > 0, 'J60 원문: ∫_0^6 f=0 → ∫_6^9 f=18, f(6)>0 → 넓이 18 (④)')
# M29: a=-2t^3+3t^2-1 의 극값 -1, 0 → 합 -1
hM = sp.expand(sp.diff(t**3 - t, t)*(1 - t) + t**3 - t)
crit = sp.solve(sp.diff(hM, t), t)
check('M29', sorted(hM.subs(t, c) for c in crit) == [-1, 0], f'M29 원문: h={hM}, 극값 {sorted(hM.subs(t, c) for c in crit)} → 합 -1 (②)')
# J25: D=t(t-6)^2/3, a=2, b=6, ∫_2^6|2t-7|=17/2
DJ = sp.integrate((t**2 - 6*t + 5) - (2*t - 7), (t, 0, t))
check('J25', sp.factor(DJ) == t*(t - 6)**2/3 and sp.integrate(sp.Abs(2*t - 7), (t, 2, 6)) == sp.Rational(17, 2), 'J25 원문: D=t(t-6)^2/3, a=2, b=6, Q 이동거리 17/2 (②)')
# M66: g'(x≤0)=3x^2+2ax+15 두 음근 r1<r2, x>0 근 s, 사슬 r1+4=r2, r2+4=s
r = sp.symbols('r')
rr = [v for v in sp.solve(r*(r + 4) - 5, r) if v < 0 and v + 4 < 0]
r1 = rr[0]; r2 = r1 + 4; s0 = r2 + 4
aM = -sp.Rational(3, 2)*(r1 + r2)
pM = sp.Rational(15, 2)/s0
gm = lambda X: (X**3 + aM*X**2 + 15*X + 7) if X <= 0 else (-pM*X**2 + 15*X + 7)
check('M66', (r1, r2, s0, aM, pM) == (-5, -1, 3, 9, sp.Rational(5, 2)) and gm(-2) + gm(2) == 32, 'M66 원문: 근 -5,-1,3, a=9, p=5/2 → g(-2)+g(2)=32 (②)')

# ================= 10번 =================
# 일반해: (가) ⇔ f(x)-(3/2)x 가 주기 2. f(x)=(3/2)x+k+φ(x), φ 주기 2, ∫_0^2 φ=0 으로 놓아도 일반성 잃지 않음.
k = sp.symbols('k')
lin = sp.Rational(3, 2)*x + k
k10 = sp.solve(sp.integrate(lin, (x, 1, 5)), k)[0]             # ∫_1^5 φ = 0 (두 주기)
lin = lin.subs(k, k10)
check(10, k10 == sp.Rational(-9, 2) and sp.integrate(lin, (x, 2, 4)) == 0, 'f=(3/2)x-9/2+φ, ∫_2^4 f=0 (φ 두 블록 평균 0)')
G = lambda u: sp.integrate(lin, (x, u, u + 2))
check(10, all(sp.simplify(G(u + 1) - G(u) - 3) == 0 for u in [sp.Integer(0), sp.Rational(1, 3), sp.Integer(5)]) and G(1) == -3 and G(4) == 6 and G(6) == 12,
      'G(t+1)-G(t)=3, G(1)=-3, G(4)=6, G(6)=12 (φ 부분은 길이 2 구간에서 0)')


# φ=A·삼각파(주기 2, 평균 0, 짝수점 1/2·홀수점 -1/2, 기울기 ±A): 구간 [i,i+1]에서 f는 일차식 (기울기 3/2 ± A)
def tri_int(i):
    return Fr(1, 2) if i % 2 == 0 else Fr(-1, 2)


def area_exact(A, lo=4, hi=8):
    tot = Fr(0); integ = Fr(0)
    for i in range(lo, hi):
        fa = Fr(3, 2)*i - Fr(9, 2) + A*tri_int(i)
        fb = Fr(3, 2)*(i + 1) - Fr(9, 2) + A*tri_int(i + 1)
        integ += (fa + fb)/2
        if fa*fb >= 0:
            tot += abs(fa + fb)/2
        else:
            z = fa/(fa - fb)
            tot += abs(fa)*z/2 + abs(fb)*(1 - z)/2
    return tot, integ


def int15(A):
    return sum((Fr(3, 2)*i - Fr(9, 2) + A*tri_int(i) + Fr(3, 2)*(i + 1) - Fr(9, 2) + A*tri_int(i + 1))/2 for i in range(1, 5))


vals10 = []
for A in [Fr(0), Fr(1, 2), Fr(-1), Fr(7, 5), Fr(-7, 5)]:     # |A|<3/2 이면 기울기 3/2±A>0 → 증가
    ar, ig = area_exact(A)
    check(10, int15(A) == 0, f'A={A}: (나) ∫_1^5 f=0 성립, 넓이 {ar}')
    vals10.append(ar)
check(10, set(vals10) == {18}, f'증가하는 여러 f(φ=A·삼각파, |A|<3/2)에서 넓이 {set(vals10)}')
check(10, all(Fr(3, 2)*4 - Fr(9, 2) + A*tri_int(4) > 0 for A in [Fr(0), Fr(7, 5), Fr(-7, 5)]), 'f(4)>0 (∫_2^4 f=0 과 증가)')
ans_ok(10, 18)
# 오답 근거
G5 = G(5) + G(7)
check(10, G5 == 24 and G(3) + G(5) == 12, '∫_5^9 f=24, ∫_3^7 f=12')
Gw = lambda u: -sp.Rational(3, 2) + sp.Rational(3, 2)*(u - 1)          # 블록 증가를 3으로 착각: G(t+2)=G(t)+3
check(10, Gw(1) + Gw(3) == 0 and Gw(4) + Gw(6) == 9, '블록 증가 3 착각 → 9')
wrong_in(10, [G5 - 3, 12, 9], '24-3, [3,7]/블록마다 6 줄임, 블록 증가 3 착각')
print('--- 10번 조건 빼 보기 ---')
ar8, ig8 = area_exact(Fr(8))
ablation(10, "'증가하는'", [18, ar8], 18, why=f'A=8 삼각파(증가 아님, 연속·(가)(나) 성립)이면 ∫_4^8 f={ig8}이나 f가 음수인 곳이 있어 넓이 {ar8}')
ablation(10, "'(가)'", [sp.integrate(2*x - 6, (x, 4, 8)), sp.integrate(x - 3, (x, 4, 8))], 18, why='f=2x-6, x-3 모두 증가·∫_1^5 f=0')
ablation(10, "'(나)'", [sp.integrate(sp.Rational(3, 2)*x + kk, (x, 4, 8)) for kk in [-3, 0]], 18, why='f=(3/2)x+k에서 k 미정')

# ================= 12번 =================
fc = x**3 + 3*x**2 - 4
fp = sp.diff(fc, x)
xi = sp.solve(sp.diff(fc, x, 2), x)[0]
check(12, (xi, fc.subs(x, xi), fp.subs(x, xi)) == (-1, -2, -3) and sp.factor(fc) == (x - 1)*(x + 2)**2, '변곡점 (-1,-2), 변곡점에서의 접선의 기울기 -3, 곡선 (x-1)(x+2)^2')
check(12, sp.expand(fc - (x - 1)) == sp.expand((x + 3)*(x + 1)*(x - 1)), '직선 y=x-1은 변곡점을 지나고 곡선과 x=-3,-1,1에서 만남')
K = sp.expand(-(fp.subs(x, s)*(t - s) + fc.subs(x, s) - (t - 1)))      # 접선이 (t, t-1)을 지날 조건 K(s)=0
check(12, K == sp.expand(2*s**3 - 3*(t - 1)*s**2 - 6*t*s + t + 3) and sp.expand(sp.diff(K, s) - 6*(s + 1)*(s - t)) == 0,
      f"K(s)={K}, K'(s)={sp.factor(sp.diff(K, s))}")
check(12, sp.expand(K.subs(s, -1) - 4*(t + 1)) == 0 and sp.expand(K.subs(s, t) + (t + 3)*(t + 1)*(t - 1)) == 0, 'K(-1)=4(t+1), K(t)=-(t+3)(t+1)(t-1)')


def ntan(tv, curve=fc, line=lambda u: u - 1):
    """점 (tv, line(tv))에서 그은 서로 다른 접선의 개수 (접점 s의 실근마다 (기울기, 절편)을 모아 센다)"""
    cp = sp.diff(curve, x)
    eq = sp.expand(cp.subs(x, s)*(tv - s) + curve.subs(x, s) - line(tv))
    L = {(sp.simplify(cp.subs(x, rt)), sp.simplify(curve.subs(x, rt) - rt*cp.subs(x, rt))) for rt in set(sp.Poly(eq, s).real_roots())}
    return len(L)


def disc_points(curve=fc, line=lambda u: u - 1):
    """개수가 바뀔 수 있는 t: 접점 방정식(s에 대한 삼차)의 판별식의 실근 → 그 점과 양옆을 비교"""
    cp = sp.diff(curve, x)
    eq = sp.expand(cp.subs(x, s)*(t - s) + curve.subs(x, s) - line(t))
    dsc = sp.discriminant(eq, s)
    cand = sorted(set(sp.Poly(dsc, t).real_roots()))
    e = sp.Rational(1, 1000)
    return cand, [c for c in cand if not (ntan(c - e, curve, line) == ntan(c, curve, line) == ntan(c + e, curve, line))]


cand12, disc = disc_points()
check(12, cand12 == [-3, -1, 1], f'판별식이 0인 t {cand12} (이 밖에서는 실근 개수 일정)')
for tv in cand12:
    print(f'    t={tv}: f(t-ε)={ntan(tv - sp.Rational(1, 1000))}, f(t)={ntan(tv)}, f(t+ε)={ntan(tv + sp.Rational(1, 1000))}')
grid = [sp.Rational(k2, 4) for k2 in range(-32, 33)]
check(12, all(ntan(tv) == (3 if (tv < -3 or tv > 1) else (2 if tv in (-3, 1) else 1)) for tv in grid),
      't=-8..8 (0.25 간격) 접선 개수: t<-3·t>1 이면 3, t=-3·1 이면 2, -3<t<1 이면 1 (t=-1 포함)')
check(12, disc == [-3, 1], f'불연속 t {disc} (변곡점 t=-1은 연속)')
ans_ok(12, sum(disc))
ys = [t0 - 1 for t0 in disc]
wrong_in(12, [sum(cand12), sum(ys), sum(ys) + (-2)], '변곡점 t=-1 포함 -3, 경계점의 y좌표 합 -4, 변곡점 y좌표까지 -6')
print('--- 12번 조건 빼 보기 ---')
c2_, d2 = disc_points(line=lambda u: 4*u - 4)
ablation(12, "'점이 변곡점을 지나는 직선 위'(→ 점 (t, 4t-4), 변곡점을 지나지 않음)", [sum(d2)], -2, why=f'불연속 t={d2}: 곡선과 만나는 세 점과 변곡점에서의 접선과 만나는 점 모두')
c3_, d3 = disc_points(line=lambda u: -4*u - 6)
ablation(12, "'직선의 기울기 1'(→ -4, 변곡점을 지나고 접선 기울기 -3보다 작음)", [], -2,
         undef=f'곡선과 변곡점에서만 만나고 접선은 늘 1개, 불연속 t {d3}' if not d3 else None)

# ================= 14번 =================
v1 = 3*t**2 - 12*t + 9
v2 = 6*t - 6
x1 = sp.integrate(v1.subs(t, s), (s, 0, t)); x2 = sp.integrate(v2.subs(t, s), (s, 0, t))
D = sp.expand(x1 - x2)
check(14, D == t**3 - 9*t**2 + 15*t and sp.expand(sp.diff(D, t) - 3*(t - 1)*(t - 5)) == 0, f'D={D}, D\'=3(t-1)(t-5)')


def local_max_abs(Dx, lo=0):
    """t>lo 에서 |D| 의 극대점: D'=0 이고 D≠0 인 점 중 |D| 가 극대인 것 (영점은 |D|=0 이라 극소)"""
    outs = []
    for c in sp.Poly(sp.diff(Dx, t), t).real_roots():
        if c > lo and Dx.subs(t, c) != 0:
            e = sp.Rational(1, 10**4)
            if abs(Dx.subs(t, c - e)) < abs(Dx.subs(t, c)) > abs(Dx.subs(t, c + e)):
                outs.append(c)
    return outs


mx = local_max_abs(D)
zs = [z for z in sp.Poly(D, t).real_roots() if z > 0]
check(14, mx == [1, 5] and D.subs(t, 1) == 7 and D.subs(t, 5) == -25, f'|D| 극대 t={mx} (D(1)=7, D(5)=-25), |D|=0 인 t={[sp.nsimplify(z) for z in zs]}(극소)')
dist = sp.integrate(sp.Abs(v1), (t, 1, 5))
check(14, dist == 24 and sp.solve(v1, t) == [1, 3] and [x1.subs(t, c) for c in (1, 3, 5)] == [4, 0, 20], 'P: v1=3(t-1)(t-3)이 t=3에서 부호 바뀜, x1(1)=4, x1(3)=0, x1(5)=20 → 거리 24')
ans_ok(14, dist)
wrong_in(14, [x1.subs(t, 5) - x1.subs(t, 1), x1.subs(t, 5), abs(D.subs(t, 1)) + abs(D.subs(t, 5))], '위치 변화량 16, 위치 20(=t≥3 부분 거리), f(1)+f(5)=32')
print('--- 14번 조건 빼 보기 ---')
mn = [sp.nsimplify(z) for z in zs]
dmin = sp.integrate(sp.Abs(v1), (t, mn[0], mn[1]))
ablation(14, "'극대'(→ 극소)", [sp.nsimplify(sp.simplify(dmin))], 24, why='극소 시각은 D=0인 (9∓√21)/2(무리수), 그 사이 P의 이동거리 x1(t1)+x1(t2)')
D30 = D + 30                                     # Q가 좌표 -30에서 출발하면
mx30 = local_max_abs(D30)
ablation(14, "'동시에 원점을 출발'(→ Q가 좌표 -30에서 출발)", [], 24, undef=f'위치의 차 D+30의 극솟값 5>0이라 거리의 극대는 t={mx30} 하나뿐, b가 정해지지 않음')
ablation(14, "'(t≥0)'", [dist], 24, est=True, why='t<0에서 |D|는 감소해 t=0에서 극소, 새 극대 없음; 운동 서술 틀')

# ================= 16번 =================
pp = sp.symbols('p', positive=True)


def left_roots(av):
    """x≤0 에서 6x^2+2ax+24=0 의 서로 다른 실근"""
    return sorted({rt for rt in sp.Poly(6*x**2 + 2*av*x + 24, x).real_roots() if rt <= 0})


def count16(av, sv):
    """g'=0 의 근 집합 A(왼쪽 근 ∪ {s}), g'(-2x)=0 의 근 B={-α/2}, |A∪B|"""
    sv = sp.sympify(sv)
    A = set(left_roots(av)) | {sv}
    B = {-u/2 for u in A}
    return len(A | B)


# (가): f(0)=36, f'(0)=24 → f=-p x^2+24x+36 ; (다): x>0 최댓값 72 (p>0일 때만 최댓값 존재; p<0이면 x>0에서 증가)
fq = -pp*x**2 + 24*x + 36
smax = sp.solve(sp.diff(fq, x), x)[0]
p16 = sp.solve(fq.subs(x, smax) - 72, pp)
check(16, p16 == [4] and smax.subs(pp, 4) == 3, f'(다) → p={p16}, x>0의 근 s=3')
S16 = 3
# a 전수: 왼쪽 근이 -3/2 또는 -6 과 같아지는 a (겹침이 생길 수 있는 유일한 경우) 와 판별식 0, 그리고 촘촘한 격자
crit_a = set()
for z in [-sp.Rational(3, 2), -6]:
    crit_a |= set(sp.solve((6*x**2 + 2*a*x + 24).subs(x, z), a))
crit_a |= set(sp.solve(4*a**2 - 4*6*24, a))
grid_a = sorted(crit_a | {sp.Rational(k2, 4) for k2 in range(-160, 161)}, key=float)
good = [av for av in grid_a if count16(av, S16) == 4]
check(16, sorted(crit_a, key=float) == [-12, 12, sp.Rational(25, 2), 20] and good == [12],
      f'특수 a {sorted(crit_a, key=float)} (25/2·20은 겹침 1개 → 5개), a=-40..40 전수에서 개수 4인 a {good}')
check(16, count16(sp.Rational(25, 2), 3) == 5 and count16(20, 3) == 5 and count16(13, 3) == 6 and count16(0, 3) == 2 and count16(-12, 3) == 2,
      'a=25/2, 20 → 5개, a=13 → 6개, a=0·-12 → 2개')
a16 = good[0]
gL = lambda X, av=a16: 2*X**3 + av*X**2 + 24*X + 36
fR = lambda X, pv=4: -pv*X**2 + 24*X + 36
check(16, sp.factor(gL(x) - 36) == 2*x*(x**2 + 6*x + 12) and sp.factor(sp.diff(gL(x), x)) == 6*(x + 2)**2, "a=12: g'(x)=6(x+2)^2 (x≤0)")
check(16, fR(0) == gL(0) and sp.diff(fR(x), x).subs(x, 0) == sp.diff(gL(x), x).subs(x, 0), '(가) 이음점 x=0 값·미분계수 일치')
val16 = gL(-2) + fR(2)
ans_ok(16, val16)
# 오답 근거
E1 = gL(-2, 15) + fR(2, 6); E3 = gL(-2, 13) + fR(2, 4); E5 = gL(-2) + fR(2, 2); E2 = gL(-2, 15) + fR(2, 4)
check(16, count16(15, 2) == 4 and count16(12, 1) == 3 and count16(12, 6) == 4, '사슬 a=15, s=2이면 (나) 성립(원본식 풀이), p=2(s=6)도 (나) 성립')
check(16, len({rt for rt in [-3, -sp.Rational(4, 3)]}) == 2 and sp.Poly(6*x**2 + 26*x + 24, x).real_roots() == [-3, -sp.Rational(4, 3)], "g'(-x)로 착각: S∪(-S)에서 -3 ↔ 3 → a=13")
wrong_in(16, [E1, E3, E5, E2], f'사슬(a=15,p=6) {E1}, g\'(-x) 착각(a=13) {E3}, 상수항 미반영 p=2 {E5}, 사슬 a+(다) p {E2}')
print('--- 16번 조건 빼 보기 ---')
# (다) 제거: p 자유 → (나)를 만족시키는 (a, p) 여러 개
alt = []
for pv in [6, 3, 2, sp.Rational(12, 5)]:
    sv = sp.Rational(12, 1)/pv
    for av in sorted(crit_a | {sp.Rational(15, 1), 12} | set(sp.solve([(6*x**2 + 2*a*x + 24).subs(x, z) for z in [-sv/2]][0], a)) | set(sp.solve((6*x**2 + 2*a*x + 24).subs(x, -2*sv), a)), key=float):
        if count16(av, sv) == 4:
            alt.append(gL(-2, av) + fR(2, pv))
ablation(16, "'(다)'", alt, 88, why='p=6이면 사슬 a=15(92)와 중근 a=12(80) 모두 가능, p마다 중근 a=12 가능')
# (나) 제거
ablation(16, "'(나)'", [gL(-2, av) + fR(2) for av in [0, 12, 15]], 88, why='a 미정')
# (가) 제거: x>0 의 f 는 최댓값 72인 아무 이차함수, 예: -(x-3)^2+72 (근 3은 그대로라 a=12)
fA = lambda X: -(X - 3)**2 + 72
ablation(16, "'(가)'", [gL(-2) + fA(2), val16], 88, why='f=-(x-3)^2+72이면 (나)(다) 성립, 답 91')
ablation(16, "'(나)의 개수 4'(→ 5)", [gL(-2, av) + fR(2) for av in grid_a if count16(av, 3) == 5], 88)

print('정답 위치:', {n: IT[n]['ans'] for n in sorted(IT)})
print('ALL OK' if ok else 'SOME FAIL')
