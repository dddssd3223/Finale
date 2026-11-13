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
# M29: a=-2t^3+3t^2-1 의 극값 -1, 0 → 합 -1
hM = sp.expand(sp.diff(t**3 - t, t)*(1 - t) + t**3 - t)
crit = sp.solve(sp.diff(hM, t), t)
check('M29', sorted(hM.subs(t, c) for c in crit) == [-1, 0], f'M29 원문: h={hM}, 극값 {sorted(hM.subs(t, c) for c in crit)} → 합 -1 (②)')
# J17: A=B ⇔ ∫_0^2{(x^3+x^2)-(-x^2+k)}dx=0 → k=14/3 (4<k<5)
kJ = sp.solve(sp.integrate((x**3 + x**2) - (-x**2 + a), (x, 0, 2)), a)
check('J17', kJ == [sp.Rational(14, 3)] and 4 < kJ[0] < 5, 'J17 원문: 4+16/3-2k=0 → k=14/3 (④)')
# M66: g'(x≤0)=3x^2+2ax+15 두 음근 r1<r2, x>0 근 s, 사슬 r1+4=r2, r2+4=s
r = sp.symbols('r')
rr = [v for v in sp.solve(r*(r + 4) - 5, r) if v < 0 and v + 4 < 0]
r1 = rr[0]; r2 = r1 + 4; s0 = r2 + 4
aM = -sp.Rational(3, 2)*(r1 + r2)
pM = sp.Rational(15, 2)/s0
gm = lambda X: (X**3 + aM*X**2 + 15*X + 7) if X <= 0 else (-pM*X**2 + 15*X + 7)
check('M66', (r1, r2, s0, aM, pM) == (-5, -1, 3, 9, sp.Rational(5, 2)) and gm(-2) + gm(2) == 32, 'M66 원문: 근 -5,-1,3, a=9, p=5/2 → g(-2)+g(2)=32 (②)')

# ================= 10번 =================
import sys as _sys
_sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as _F
check(10, IT[10]['key'] == 'J58' and IT[10]['src'] == _F.I['J58'][3], f"key=J58, src={_F.I['J58'][3]}")
p1, p2, p0 = sp.symbols('p1 p2 p0')
fg = x**3 + p2*x**2 + p1*x + p0
sol10 = sp.solve([sp.diff(fg, x).subs(x, -1), sp.diff(fg, x).subs(x, 3), fg.subs(x, 3) + 3], [p2, p1, p0], dict=True)
check(10, len(sol10) == 1, f'(조건) f 유일: {sol10}')
f10 = fg.subs(sol10[0])
check(10, sp.expand(f10 - (x**3 - 3*x**2 - 9*x + 24)) == 0, f'f={f10}')
P10 = (4, f10.subs(x, 4)); m10 = P10[1]/4
check(10, P10[1] == 4 and m10 == 1, 'P(4,4), 선분 OP: y=x')
h10 = sp.expand(f10 - m10*x)
check(10, sp.factor(h10) == (x - 4)*(x - 2)*(x + 3), f'f-x={sp.factor(h10)}')
qs = [r for r in sp.solve(h10, x) if 0 <= r < 4]
check(10, qs == [2], f'선분 OP(0≤x≤4) 위 교점 중 P가 아닌 점: x={qs} (유일)')
q10 = qs[0]
check(10, f10.subs(x, 0) > 0 and all(h10.subs(x, sp.Rational(k, 10)) > 0 for k in range(0, 20)) and all(h10.subs(x, sp.Rational(k, 10)) < 0 for k in range(21, 40)),
      '[0,2)에서 f>x, (2,4)에서 f<x (A: y축·곡선·OQ, B: 곡선·PQ)')
A10 = sp.integrate(h10, (x, 0, q10)); B10 = sp.integrate(-h10, (x, q10, 4))
check(10, (A10, B10) == (24, 8), f'A={A10}, B={B10}')
ans_ok(10, A10 + B10)
# 오답 근거
d10 = sp.integrate(h10, (x, 0, 4)); s10 = sp.integrate(f10, (x, 0, 4))
check(10, d10 == A10 - B10 == 16 and s10 == 24, f'∫_0^4(f-x)={d10}=A-B, ∫_0^4 f={s10}')
wrong_in(10, [d10, s10, A10, B10], '원본식 한 번 적분 A-B, x축 적분/A만, B만')
print('--- 10번 조건 빼 보기 ---')
def ab10(fx):
    h = sp.expand(fx - fx.subs(x, 4)/4*x)
    q = [r for r in sp.solve(h, x) if r.is_real and 0 <= r < 4]
    v = sp.integrate(sp.Abs(h), (x, 0, 4))
    return [sp.Integer(v) if v.is_integer else sp.Float(round(float(v), 2), 4)] if q else []
ablation(10, "'f(3)=-3'", [ab10(x**3 - 3*x**2 - 9*x + cc)[0] for cc in [24, 20, 30]], 32, why='상수항 C 미정')
ablation(10, "'f'(-1)=0'", [v for cc in [-9, -7] for v in ab10(sp.expand(x**3 + (-(3*3**2 + cc)/6)*x**2 + cc*x + (-3 - 27 - 9*(-(27 + cc)/6) - 3*cc)))[:1]], 32, why="f'(3)=0, f(3)=-3만이면 일차항 계수 미정")
# 원문 J58: f=(x-1)(x-2)(x+c), f'(0)=-7 → B-A=∫_0^3(직선-f)=45/4 (⑤)
cJ = sp.symbols('cJ')
fJ = sp.expand((x - 1)*(x - 2)*(x + cJ))
cJ0 = sp.solve(sp.diff(fJ, x).subs(x, 0) + 7, cJ)[0]
fJ = fJ.subs(cJ, cJ0)
BA = sp.integrate(fJ.subs(x, 3)/3*x - fJ, (x, 0, 3))
check('J58', fJ == x**3 - 7*x + 6 and BA == sp.Rational(45, 4) and _F.I['J58'][2] == '⑤' and sp.sympify(_F.I['J58'][1][4].replace('\\dfrac{45}4', '45/4')) == BA, f'J58 원문: f={fJ}, B-A={BA} (⑤)')

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
f14 = x*(x - 3)**2
# f 결정: 최고차항 1, f(0)=0, f(3)=0, f'(3)=0 (극솟값 0) → 유일
pa, pb, pc = sp.symbols('pa pb pc')
gen = x**3 + pa*x**2 + pb*x + pc
sol14 = sp.solve([gen.subs(x, 0), gen.subs(x, 3), sp.diff(gen, x).subs(x, 3)], [pa, pb, pc], dict=True)
check(14, len(sol14) == 1 and sp.expand(gen.subs(sol14[0]) - f14) == 0 and sp.diff(f14, x, 2).subs(x, 3) > 0, f'f=x(x-3)^2 유일, x=3에서 극소(f\'\'(3)>0), 극솟값 {f14.subs(x, 3)}')
kk = sp.symbols('kk')
AmB = sp.integrate(kk - f14, (x, 0, 2))                     # A-B (직선 아래쪽 - 위쪽)
ks = sp.solve(AmB, kk)
check(14, ks == [3] and sp.expand(AmB - (2*kk - 6)) == 0, f'A-B=∫_0^2(k-f)={sp.expand(AmB)} → k={ks} (k에 대한 일차식이라 유일)')
k14 = ks[0]
cr14 = sorted(r for r in sp.Poly(f14 - k14, x).real_roots() if 0 < r < 2)
A14 = sp.Integral(sp.Max(k14 - f14, 0), (x, 0, 2)).evalf(30); B14 = sp.Integral(sp.Max(f14 - k14, 0), (x, 0, 2)).evalf(30)
check(14, len(cr14) == 2 and f14.subs(x, 0) < k14 and f14.subs(x, 2) < k14 and abs(A14 - B14) < 1e-20 and B14 > 0,
      f'k=3: 0<x<2에서 교점 {[round(float(r), 3) for r in cr14]} → A(y축 쪽)+C(x=2 쪽)=B(가운데), A+C={float(A14):.4f}=B')
check(14, sp.diff(f14, x, 2).subs(x, 2) == 0 and f14.subs(x, 2) == 2 and f14.subs(x, 1) == 4 and sp.diff(f14, x).subs(x, 1) == 0, '변곡점 (2, 2), 극대 (1, 4)')
ans_ok(14, k14)
wrong_in(14, [f14.subs(x, 2), f14.subs(x, 1), (f14.subs(x, 0) + f14.subs(x, 2))/2], '변곡점 성질 오용 f(2)=2, 가운데 함숫값 f(1)=4, 양 끝 평균 1')
print('--- 14번 조건 빼 보기 ---')
cc = sp.symbols('cc')
kf = lambda F: sp.solve(sp.integrate(kk - F, (x, 0, 2)), kk)[0]
ablation(14, "'f(0)=0'", [kf((x - 3)**2*(x - cv)) for cv in (0, -1, 1)], 3, why='f=(x-3)^2(x-c), k가 c에 따라 바뀜')
ablation(14, "'극솟값 0'(→ x=3에서 극소만)", [kf(x**3 - 6*x**2 + 9*x + 0*x), kf(sp.expand(x**3 + pa*x**2 + (-27 - 6*pa)*x).subs(pa, -5))], 3, why="f'(3)=0, f(0)=0만으로는 f=x^3+ax^2-(27+6a)x, a 미정")
ablation(14, "'x=2'(→ x=3)", [sp.solve(sp.integrate(kk - f14, (x, 0, 3)), kk)[0]], 3, why='구간 [0, 3]에서의 평균값 9/4')
ablation(14, "'최고차항의 계수 1'", [kf(2*f14), kf(f14)], 3, why='f=ax(x-3)^2이면 k=3a')

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
