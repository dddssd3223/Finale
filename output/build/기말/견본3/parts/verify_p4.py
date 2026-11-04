# -*- coding: utf-8 -*-
# 견본3 p4 (13–16번) 정답 검증
import os
import numpy as np
import sympy as sp

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 1, 14: 5, 15: 1, 16: 2}
x, t, s, a = sp.symbols('x t s a', real=True)
ok = True

def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)

def num_choices(no):
    v = [sp.sympify(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d})')
    return v

def ans_ok(no, val):
    v = num_choices(no)
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    return v

# ---------------- 원문 확인 ----------------
d0 = sp.integrate((2*s**3 - 2*s) - (s**2 + 4*s), (s, 0, t))
c0 = [r for r in sp.solve(sp.diff(d0, t), t) if 0 <= r <= 3] + [0, 3]
check('J39', max(abs(d0.subs(t, r)) for r in c0) == sp.Rational(20, 3), 'J39 원문 최댓값 20/3 (③)')
h0 = x**2 - 2*x + a
A0 = sp.solve(h0.subs(x, 1) - 1, a)[0]
H0 = h0.subs(a, A0)
check('J63', A0 == 2 and sp.integrate(H0, (x, 0, 3)) == 6 and sp.integrate(H0, (x, -2, 2)) == sp.integrate(H0, (x, 0, 4)),
      'J63 원문 a=2, S(3)=6, [-2,2] 넓이 = S(4) → ㄴ, ㄷ (⑤)')
g0 = 4*x**2 + 12*x - 6; f0 = x*sp.diff(g0, x)
lhs0 = sp.integrate((t*f0).subs(x, t), (t, 1, x)) + sp.integrate((t*g0).subs(x, t), (t, -1, x))
check('I67', sp.expand(lhs0 - (3*x**4 + 8*x**3 - 3*x**2)) == 0 and sp.integrate(g0, (x, 0, 3)) == 72, 'I67 원문 ∫₀³g = 72 (①)')
fm = 2*x**4 - 3*x**2 - 2*x + 4
fpm = sp.diff(fm, x)
xs = [r for r in sp.solve(sp.diff(fpm, x), x) if r > 0]
y0 = (fm - x*fpm).subs(x, xs[0])
check('M5', xs == [sp.Rational(1, 2)] and y0 == sp.Rational(35, 8), 'M5 원문 y절편 35/8 → p+q=43 (③)')

# ---------------- 13번 ----------------
v1 = 12*t**3 - 36*t**2
v2 = 12*t**2 + a*t
sa = sp.solve(v2.subs(t, 3), a)
check(13, sa == [-36], f'v2(3)=0 → a={sa}')
V2 = v2.subs(a, sa[0])
e = sp.Rational(1, 1000)
check(13, V2.subs(t, 3 - e) * V2.subs(t, 3 + e) < 0, 't=3 좌우 v2 부호 바뀜(실제 방향 전환)')
d = sp.expand(sp.integrate((v1 - V2).subs(t, s), (s, 0, t)))
check(13, d == 3*t**4 - 16*t**3 + 18*t**2, f'x1-x2 = {d}')
check(13, sp.factor(sp.diff(d, t)) == sp.factor(12*t*(t - 1)*(t - 3)), f"d' = {sp.factor(sp.diff(d, t))}")
cand = sorted(set([r for r in sp.solve(sp.diff(d, t), t) if 0 <= r <= 4] + [0, 4]))
vals = {c: d.subs(t, c) for c in cand}
print('   후보', vals)
m13 = max(abs(v) for v in vals.values())
tt = np.linspace(0, 4, 400001); dn = sp.lambdify(t, d, 'numpy')(tt)
check(13, abs(np.abs(dn).max() - float(m13)) < 1e-6, '수치 최댓값 일치')
ch = ans_ok(13, m13)
check(13, abs(vals[3]) == 27 and 27 in ch, "오답 27(끝값 누락: |d(3)|) 선지에 있음")

# ---------------- 14번 ----------------
f = x**4 - 3*x**3 - 6*x**2 + 4*x
fp = sp.diff(f, x); fpp = sp.diff(fp, x)
check(14, sp.factor(fpp) == sp.factor(6*(2*x + 1)*(x - 2)), f"y'' = {sp.factor(fpp)}")
def g_exact(T):
    # [0,T]에서 f'의 최소점: 끝점과 내부 임계점 전수, 최소점이 하나인지 확인
    pts = [sp.Integer(0), sp.sympify(T)] + [r for r in sp.solve(fpp, x) if 0 < r < T]
    sl = {p: fp.subs(x, p) for p in pts}
    mn = min(sl.values()); arg = [p for p in pts if sl[p] == mn]
    assert len(arg) == 1, (T, sl)
    p = arg[0]
    return p, sp.expand(f.subs(x, p) - p*fp.subs(x, p))
def g_num(T):
    xx = np.linspace(0, T, 600001); sl = sp.lambdify(x, fp, 'numpy')(xx)
    i = int(np.argmin(sl)); p = xx[i]
    return float(f.subs(x, p) - p*fp.subs(x, p))
p1, g1 = g_exact(1); p3, g3 = g_exact(3)
check(14, (p1, g1) == (1, 9) and (p3, g3) == (2, 24), f'g(1): 접점 x={p1}, y절편 {g1} / g(3): 접점 x={p3}, y절편 {g3}')
check(14, abs(g_num(1) - 9) < 1e-4 and abs(g_num(3) - 24) < 1e-4, '수치 확인')
Gs = sp.expand((f - x*fp).subs(x, s))
check(14, Gs == -3*s**4 + 6*s**3 + 6*s**2, f'y절편 f(s)-sf\'(s) = {Gs} (일차항 소거)')
# 범위 경계: t<=2이면 x=t, t>=2이면 x=2
check(14, all(g_exact(sp.Rational(k, 4))[0] == min(sp.Rational(k, 4), 2) for k in range(1, 21)), '접점 = min(t, 2) (t=1/4~5 전수)')
ch = ans_ok(14, g1 + g3)
wrong14 = Gs.subs(s, 2) * 2
check(14, wrong14 == 48 and 48 in ch, '오답 48(t=1에도 x=2 사용) 선지에 있음')

# ---------------- 15번 ----------------
h = x**3 + a*x**2 + 3*x
A = sp.solve(h.subs(x, 1) - 1, a)
check(15, A == [-3], f'h(1)=1 → a={A}')
H = h.subs(a, A[0])
check(15, sp.expand(H - ((x - 1)**3 + 1)) == 0, 'h=(x-1)^3+1')
check(15, all(r.is_real is False or r == 0 for r in sp.solve(H, x)) and sp.solve(H, x).count(0) == 1, f'h의 실근은 0뿐: {sp.solve(H, x)}')
xx = np.linspace(1e-6, 50, 200001)
check(15, np.all(sp.lambdify(x, H, 'numpy')(xx) > 0), 'x>0에서 h>0 (조건 성립)')
S = sp.integrate(H.subs(x, s), (s, 0, t))
# ㄱ: h' = 3(x-1)^2, x=1에서 부호 안 바뀜
hp = sp.diff(H, x)
gi = (hp.subs(x, 1) == 0) and (hp.subs(x, 1 - e) > 0 and hp.subs(x, 1 + e) > 0)
check(15, sp.factor(hp) == 3*(x - 1)**2 and gi, "ㄱ 거짓: h'=3(x-1)^2, x=1에서 극값 없음")
G_ = (S.subs(t, 2) == 2)
check(15, G_, f'ㄴ 참: S(2) = {S.subs(t, 2)}')
area = sp.integrate(-H, (x, -1, 0)) + sp.integrate(H, (x, 0, 3))
xx = np.linspace(-1, 3, 400001); an = np.trapezoid(np.abs(sp.lambdify(x, H, 'numpy')(xx)), xx) if hasattr(np, 'trapezoid') else np.trapz(np.abs(sp.lambdify(x, H, 'numpy')(xx)), xx)
D_ = (area == 2*S.subs(t, 2))
check(15, (not D_) and area == sp.Rational(19, 2) and abs(an - 9.5) < 1e-6, f'ㄷ 거짓: 넓이 {area} (수치 {an:.6f}) ≠ 2S(2)={2*S.subs(t, 2)}')
check(15, sp.integrate(H, (x, -1, 3)) == 4, '함정: 정적분 ∫₋₁³h = 4 = 2S(2)')
truth = {'ㄱ': not gi, 'ㄴ': bool(G_), 'ㄷ': bool(D_)}  # gi: 부호 변화 없음 → 극값 없음 → ㄱ 거짓
correct = ', '.join(k for k in 'ㄱㄴㄷ' if truth[k])
chs = [c[2:] for c in IT[15]['choices']]
check(15, len(set(chs)) == 5, f'선지 {chs} 서로 다름')
check(15, IT[15]['ans'] == WANT[15] and chs[IT[15]['ans'] - 1] == correct, f'정답 {correct} = 선지 {IT[15]["ans"]}번')
check(15, 'ㄴ, ㄷ' in chs and 'ㄱ, ㄴ' in chs, '오답 ㄴ, ㄷ(ㄷ 함정)·ㄱ, ㄴ(ㄱ 함정) 선지에 있음')

# ---------------- 16번 ----------------
# g를 5차 이하 일반 다항식으로 두고 (가)·(나)를 항등식으로 풀어 유일성 확인
cs = sp.symbols('c0:6')
g = sum(cs[i]*x**i for i in range(6))
fx = x*sp.diff(g, x)
lhs = sp.integrate((t*fx).subs(x, t), (t, 1, x)) - sp.integrate((t*g).subs(x, t), (t, -1, x))
eqs = sp.Poly(sp.expand(lhs - (x**4 - x**2 - 2)), x).all_coeffs()
sol = sp.solve(eqs, cs, dict=True)
check(16, len(sol) == 1, f'해 {sol}')
G16 = g.subs(sol[0])
check(16, sp.expand(G16 - (4*x**2 + 3*x + 2)) == 0, f'g = {sp.expand(G16)}')
check(16, all(c in sol[0] for c in cs), '모든 계수가 정해짐(유일)')
# 미분한 식만으로는 일차항이 자유임을 확인
der = sp.Poly(sp.expand(x*fx - x*g - sp.diff(x**4 - x**2 - 2, x)), x).all_coeffs()
sd = sp.solve(der, cs, dict=True)
check(16, len(sd) == 1 and cs[1] not in sd[0], f'미분식만 쓰면 c1 자유: {sd}')
ch = ans_ok(16, G16.subs(x, 2))
g_wrong0 = (4*x**2 + 2).subs(x, 2); g_wrongm = (4*x**2 - 3*x + 2).subs(x, 2)
check(16, g_wrong0 == 18 and g_wrongm == 12 and 18 in ch and 12 in ch, '오답 18(일차항 0), 12(부호 실수) 선지에 있음')

# ===== 조건 제거 검사(ABLATION) =====
# 조건을 하나씩 지우고, 남은 조건을 만족시키는 경우를 다시 구해 답이 그대로인지 / 바뀌는지 / 정해지지 않는지 본다.
# 군더더기는 FAIL로 처리하지 않고 보고만 한다(ok 에 반영하지 않음).
def ablation(no, cname, vals, ans, why='', est=False, undef=None, key=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(vals), key=key or (lambda v: float(v)))
        fmt = (lambda v: f'「{v}」') if isinstance(ans, str) else str
        if sv == [ans]:
            msg = f'성립 조건(답 그대로 {fmt(ans)}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(fmt, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {fmt(ans)} → {fmt(sv[0])}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')

print('--- 조건 제거 검사 ---')
# ----- 13번: 조건 = [동시에 원점 출발], [Q가 t=3에서 운동 방향을 바꿈], [0≤t≤4], [t≥0] -----
def maxabs13(dexpr, lo=0, hi=4):
    cs_ = [r for r in sp.solve(sp.diff(dexpr, t), t) if r.is_real and lo <= r <= hi] + [lo, hi]
    return sp.nsimplify(sp.simplify(max(abs(dexpr.subs(t, r)) for r in cs_)))
d_of = lambda av, C=0: C + sp.integrate((v1 - v2.subs(a, av)).subs(t, s), (s, 0, t))
ablation(13, "'동시에 원점을 출발'", [maxabs13(d_of(-36, C)) for C in (0, 5, -10)], m13,
         why='t=0에서 x1-x2=C가 자유')
v13 = []
for av in (-36, 0, -12, -48):
    v13.append(maxabs13(d_of(av)))
ablation(13, "'Q가 t=3에서 운동 방향을 바꿈'", v13, m13, why='a가 자유')
dd = d_of(-36)
check(13, sp.limit(dd, t, sp.oo) == sp.oo, '구간 제거 시 |x1-x2| → ∞ (ABLATION 근거)')
ablation(13, "'0≤t≤4'", [], m13, undef='t≥0 전체에서 |x1-x2|=3t^4-16t^3+18t^2 → ∞, 최댓값 없음')
ablation(13, "'(t≥0)'", [maxabs13(dd)], m13, est=True, why='0≤t≤4가 따로 있어 겹침, 시각의 정의역 선언')

# ----- 14번: 조건 = [닫힌구간], [왼끝 0], [양수 t] -----
check(14, all(fpp.subs(x, sp.Rational(k, 10)) < 0 for k in range(0, 11)) and sp.solve(fpp, x) == [sp.Rational(-1, 2), 2],
      "(0,1)에서 y''<0 → y' 감소 (ABLATION 근거)")
ablation(14, "'닫힌구간'(→ 열린구간 (0,t))", [], g1 + g3,
         undef="t=1일 때 (0,1)에서 y'이 감소해 최솟값이 없음 → g(1) 정의되지 않음")
check(14, sp.limit(fp, x, -sp.oo) == -sp.oo, "x→-∞ 에서 y'→-∞ (ABLATION 근거)")
ablation(14, "'왼끝 0'(→ (-∞,t])", [], g1 + g3, undef="y'=4x^3-9x^2-12x+4 → -∞ (x→-∞), 기울기의 최솟값 없음")
ablation(14, "'양수 t'", [g_exact(1)[1] + g_exact(3)[1]], g1 + g3, est=True, why='t=1, 3만 쓰지만 [0,t]가 구간이 되려면 필요')

# ----- 15번: 조건 = [다항함수], [x>0에서 f>g], [f(1)=g(1)+1], [S'(t)=t^3+at^2+3t] -----
def area_abs(he, lo, hi):
    rs = sorted({r for r in sp.real_roots(sp.Poly(sp.expand(he), x)) if lo < r < hi}, key=float)
    pts = [lo] + rs + [hi]
    return sum(abs(sp.integrate(he, (x, u, w))) for u, w in zip(pts, pts[1:]))
def ans15(he, Sval2=None, area=None):
    """h=f-g 로 ㄱ, ㄴ, ㄷ 판정 → 정답 문자열"""
    hp_ = sp.diff(he, x); E = sp.Rational(1, 10**6)
    t1 = hp_.subs(x, 1) == 0 and hp_.subs(x, 1 - E)*hp_.subs(x, 1 + E) < 0
    S2_ = area_abs(he, 0, 2) if Sval2 is None else Sval2
    A_ = area_abs(he, -1, 3) if area is None else area
    tv = {'ㄱ': t1, 'ㄴ': S2_ == 2, 'ㄷ': A_ == 2*S2_}
    return ', '.join(k for k in 'ㄱㄴㄷ' if tv[k]) or '(없음)'
key15 = lambda v: v
ANS15 = ans15(H)
assert ANS15 == 'ㄴ'
# f(1)=g(1)+1 제거: a 자유(단 x>0에서 h>0 ⇔ a>-2√3)
v15 = []
for av in (-3, -2, 0, 1):
    he = x**3 + av*x**2 + 3*x
    assert all(he.subs(x, sp.Rational(k, 10)) > 0 for k in range(1, 200))
    v15.append(ans15(he))
ablation(15, "'f(1)=g(1)+1'", v15, ANS15, key=key15, why='a가 자유')
# x>0에서 f>g 제거: S'(t)=|h(t)| (t>0), h 다항식 ⇒ h^2=P^2 ⇒ h=±P. h(1)=1 이고 P(t)=|h(t)|≥0
P15 = x**3 + a*x**2 + 3*x
v15 = []
for eps in (1, -1):
    for av in sp.solve(eps*P15.subs(x, 1) - 1, a):
        Pv = P15.subs(a, av)
        if sp.minimum(Pv, x, sp.Interval.open(0, sp.oo)) >= 0:      # P=|h| ≥ 0 이어야 함
            v15.append(ans15(eps*Pv))
check(15, v15 == ['ㄴ'], 'h=-P 경우는 P(1)=-1<0 으로 탈락 (ABLATION 근거)')
ablation(15, "'x>0인 모든 실수 x에 대하여 f(x)>g(x)'", v15, ANS15, key=key15,
         why="S'(t)=|f(t)-g(t)|와 f(1)=g(1)+1만으로 f-g=(x-1)^3+1이 정해짐")
# 다항함수 제거(연속함수): x≥0 에서 h=(x-1)^3+1, x<0 은 임의(연속). ㄷ은 [0,3] 넓이 27/4 > 4 라 항상 거짓
v15 = []
for cv in (0, 3, -5):          # x<0 에서 h=cv*x 로 이어 붙인 연속함수
    A_ = sp.integrate(sp.Abs(cv*x), (x, -1, 0)) + area_abs(H, 0, 3)
    v15.append(ans15(H, area=A_))
check(15, area_abs(H, 0, 3) == sp.Rational(27, 4), '∫₀³h = 27/4 > 4 = 2S(2) (ABLATION 근거)')
ablation(15, "'다항함수'", v15, ANS15, key=key15, est=True,
         why="S(t)의 미분가능(연속) 보장; x<0 부분이 정해지지 않아도 ㄷ은 [0,3] 넓이 27/4>4라 거짓")
# S'(t) 식 제거: 예 f-g=1 이면 ㄱ 거짓, ㄴ 참(S(2)=2), ㄷ 참(넓이 4)
ablation(15, "'S'(t)=t^3+at^2+3t'", [ans15(sp.Integer(1) + 0*x), ANS15], ANS15, key=key15, why='예: f-g=1')

# ----- 16번: 조건 = [다항함수], [모든 실수 x], (가), (나) -----
def ok16(gg, ff, xs=None):
    l_ = sp.integrate((t*ff).subs(x, t), (t, 1, x)) - sp.integrate((t*gg).subs(x, t), (t, -1, x))
    r_ = x**4 - x**2 - 2
    A_ = (sp.expand(l_ - r_) == 0) if xs is None else all(sp.simplify((l_ - r_).subs(x, v)) == 0 for v in xs)
    B_ = (sp.expand(ff - x*sp.diff(gg, x)) == 0) if xs is None else all((ff - x*sp.diff(gg, x)).subs(x, v) == 0 for v in xs)
    return A_, B_
vs = []
for gg in (4*x**2 + 3*x + 2, x, x**2):
    A_, B_ = ok16(gg, x*sp.diff(gg, x))
    if B_: vs.append(gg.subs(x, 2))
ablation(16, "(가)", vs, G16.subs(x, 2), why='(나)만으로는 g가 자유')
vs = []
for C_ in (0, 5, -1):
    gg = 3*x + C_; ff = gg + 4*x**2 - 2
    A_, B_ = ok16(gg, ff)
    if A_: vs.append(gg.subs(x, 2))
ablation(16, "(나)", vs, G16.subs(x, 2), why='예: g=3x+C, f=g+4x^2-2')
# 다항함수 제거: (가) 미분 → x f - x g = 4x^3-2x, (나) 대입 → x g' - g = 4x^2-2 (x≠0)
gfn = sp.Function('gfn')
gen = sp.dsolve(sp.Eq(x*gfn(x).diff(x) - gfn(x), 4*x**2 - 2), gfn(x)).rhs
C1 = [c for c in gen.free_symbols if c != x][0]
check(16, sp.expand(gen - (4*x**2 + C1*x + 2)) == 0, f'미분방정식 일반해 {gen} (x>0, x<0 따로 C) (ABLATION 근거)')
# x>0, x<0 의 상수 Cp, Cm: g'(0) 존재((나)의 x=0) ⇒ Cp=Cm, 그다음 (가)의 x=1 ⇒ C=3
Cp, Cm = sp.symbols('Cp Cm', real=True)
gR, gL = 4*x**2 + Cp*x + 2, 4*x**2 + Cm*x + 2
eqC = [sp.diff(gR, x).subs(x, 0) - sp.diff(gL, x).subs(x, 0),
       -(sp.integrate(t*gL.subs(x, t), (t, -1, 0)) + sp.integrate(t*gR.subs(x, t), (t, 0, 1))) - (1 - 1 - 2)]
solC = sp.solve(eqC, [Cp, Cm], dict=True)
vs = [gR.subs(sC).subs(x, 2) for sC in solC]
ablation(16, "'다항함수'", vs, G16.subs(x, 2), est=True,
         why="(나)에서 g가 미분가능하면 g=4x^2+Cx+2로 정해짐; 적분·미분이 성립하도록 하는 전제")
vs = []
for C_ in (0, 7):
    gg = 3*x + C_; ff = x*sp.diff(gg, x)
    A_, B_ = ok16(gg, ff, xs=[1])
    if A_ and B_: vs.append(gg.subs(x, 2))
vs.append(G16.subs(x, 2))
ablation(16, "'모든 실수 x에 대하여'", vs, G16.subs(x, 2), why='x=1에서만 성립하면 예: g=3x+C')

print('ALL OK' if ok else 'SOME FAIL')
raise SystemExit(0 if ok else 1)
