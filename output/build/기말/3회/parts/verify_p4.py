# -*- coding: utf-8 -*-
# 3회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 4, 14: 1, 15: 5, 16: 3}
DBREF = {13: 'D43 예상밖 2', 14: 'J8 후보_순위 1', 15: 'J60 예상밖 1', 16: 'I66 후보_순위 1'}
x, t = sp.symbols('x t', real=True)
R = sp.Rational
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.Rational(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('ops') and IT[no].get('bunseok') is False,
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} bunseok=False')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [sp.Rational(z) for z in IT[no]['wrongs']]
    vals = [sp.nsimplify(z) for z in vals]
    check(no, all(z in v and z != v[IT[no]['ans'] - 1] for z in vals) and sorted(w) == sorted(set(vals)) and len(set(vals)) >= 2,
          f'오답 {vals} 선지에 있음, wrongs {IT[no]["wrongs"]}와 같음 ({why})')


def ablation(no, cname, vals, ans, why='', undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = f'필요(남은 조건을 만족시키는 경우가 없음{"; " + why if why else ""})'
    else:
        sv = sorted(set(vals), key=lambda v: float(v))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


def choice_val(s):
    s = re.sub(r'\s', '', s)
    m = re.fullmatch(r'(-?)\\dfrac\{?(\d+)\}?\{?(\d+)\}?', s)
    if m:
        return sp.Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    return sp.Rational(s)


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    return choice_val(o[1]['①②③④⑤'.index(o[2])])


# ================= 13번 (D43 예상밖 2) =================
a, b, c = sp.symbols('a b c', real=True)
k13 = 4
L13 = -x**2 + a * x + b                      # x<=0
M13 = x**3 + c * x - k13 * (c - x)           # 0<x<c
H13 = x**3 + c * x - k13 * (x - c)           # x>c
s_b = sp.solve(sp.Eq(L13.subs(x, 0), sp.limit(M13, x, 0, '+')), b)[0]
s_a = sp.solve(sp.Eq(sp.diff(L13, x).subs(x, 0), sp.diff(M13, x).subs(x, 0)), a)[0]
check(13, s_b == -4 * c and s_a == c + 4, f'연속 b={s_b}, x=0 미분가능 a={s_a}')
# 증가 조건: x>c에서 f'=3x^2+c-4 (x>0에서 증가) → 3c^2+c-4>=0, c>0
cset = sp.solve_univariate_inequality(sp.diff(H13, x).subs(x, c) >= 0, c, relational=False).intersect(sp.Interval.open(0, sp.oo))
check(13, cset == sp.Interval(1, sp.oo), f'x>c 증가 경계 3c^2+c-4>=0, c>0 → c∈{cset}')
fm1 = sp.expand(L13.subs({a: s_a, b: s_b}).subs(x, -1))
ans13 = sp.maximum(fm1, c, sp.Interval(1, sp.oo))
check(13, fm1 == -5 - 5 * c and ans13 == -10, f'f(-1)={fm1}, c>=1에서 최댓값 {ans13}')


def inc13(cv, av=None, bv=None, need_diff=True, grid=400):
    """조건 (가)(나)를 c=cv에서 직접 확인(구간별 도함수 + 연결점 연속)."""
    av = s_a.subs(c, cv) if av is None else av
    bv = s_b.subs(c, cv) if bv is None else bv
    fL = L13.subs({a: av, b: bv}); fM = M13.subs(c, cv); fH = H13.subs(c, cv)
    if fL.subs(x, 0) != fM.subs(x, 0): return False
    if need_diff and sp.diff(fL, x).subs(x, 0) != sp.diff(fM, x).subs(x, 0): return False
    pts = [R(-i, 40) for i in range(1, grid)]
    if any(sp.diff(fL, x).subs(x, p) < 0 for p in pts): return False
    pts = [cv * R(i, grid) for i in range(1, grid)]
    if any(sp.diff(fM, x).subs(x, p) < 0 for p in pts): return False
    pts = [cv + R(i, grid) for i in range(1, grid)]
    return not any(sp.diff(fH, x).subs(x, p) < 0 for p in pts)


# 전수: c를 1/20 간격으로 0..5 → 조건을 만족시키는 c의 최솟값 1, f(-1) 최댓값 -10
okc = [cv for cv in [R(i, 20) for i in range(1, 101)] if inc13(cv, grid=60)]
check(13, okc and min(okc) == 1 and max(fm1.subs(c, cv) for cv in okc) == -10, f'c 격자 전수: 가능한 c 최솟값 {min(okc)}, f(-1) 최댓값 {max(fm1.subs(c, cv) for cv in okc)}')
check(13, inc13(1, grid=400) and not inc13(R(99, 100), grid=400), 'c=1은 증가, c=0.99는 x=c 오른쪽에서 감소')
ans_ok(13, ans13)
# 오답: ⑤ -5 (미분가능 무시, 원문 습관 a=0: -1-a-4c, a>=0, c>=1) / ① -25 (x>0 전체에서 3x^2+c-4>=0 → c>=4)
w_a0 = sp.maximum(-1 - 0 - 4 * c, c, sp.Interval(1, sp.oo))
c_wrong = sp.solve_univariate_inequality(sp.diff(H13, x).subs(x, 0) >= 0, c, relational=False)
w_25 = fm1.subs(c, c_wrong.inf)
check(13, w_a0 == -5 and c_wrong == sp.Interval(4, sp.oo) and w_25 == -25, f'오답: a=0 습관 {w_a0}, x→0+ 판정 c>={c_wrong.inf} → {w_25}')
wrong_in(13, [w_a0, w_25], '미분가능 무시(a=0) / 증가 판정 위치 x→0+')
# 원문 D43: -2|x-c|, a>=0, b=-2c, c>=2/3 → f(-1) 최댓값 -7/3 (④)
cs0 = sp.solve_univariate_inequality(3 * c**2 + c - 2 >= 0, c, relational=False).intersect(sp.Interval.open(0, sp.oo))
o13 = sp.maximum(-1 - 0 - 2 * c, c, cs0)
check('D43', cs0 == sp.Interval(R(2, 3), sp.oo) and o13 == R(-7, 3) == orig_ans('D43'), f'D43 원문: c∈{cs0}, f(-1) 최댓값 {o13} = 원문 정답 {orig_ans("D43")}')
print('--- 13번 조건 빼 보기 ---')
# (가) x=0 미분가능 없음: x=0에서 연속도 없어져 a, b 자유 → f(-1)=-1-a+b 위로 무한
#   (참고: 연속만 남기면 b=-4c, a>=0 → a=0, c=1에서 -5 = 오답 ⑤)
okc2 = [(av, cv) for av in [0, 1, 3] for cv in [1, 2] if inc13(cv, av=av, need_diff=False, grid=60)]
check(13, max(-1 - av - 4 * cv for av, cv in okc2) == -5, '연속만 남기면(원문 (가)) 최댓값 -5 → 미분가능 조건이 답을 바꿈')
ablation(13, "(가) 'x=0에서 미분가능'", [], -10, undef='a, b가 정해지지 않아 f(-1)=-1-a+b의 최댓값이 없음(b→∞); 연속만 두어도 답 -10 → -5')
# (나) 없음: c>0 아무 값 → -5-5c는 최댓값 없음(상한 -5에 닿지 않음)
ablation(13, '(나)', [], -10, undef=f'c>0이면 모두 가능, f(-1)=-5-5c의 최댓값이 없음(c=1/100에서 {fm1.subs(c, R(1, 100))})')

# ================= 14번 (J8 후보_순위 1, 숫자만) =================
a2, b2 = sp.symbols('a2 b2')
p14 = 5
lin = x + p14
quad = x**2 + a2 * x + b2
s14 = sp.solve([sp.Eq(lin.subs(x, 0), quad.subs(x, 0)), sp.Eq(quad.subs(x, p14), lin.subs(x, -p14))], [a2, b2], dict=True)
check(14, len(s14) == 1 and s14[0] == {a2: -6, b2: 5}, f'x=0 연속, f(5)=f(-5)=0 → {s14}(유일)')
q14 = quad.subs(s14[0])
check(14, sp.factor(q14) == sp.factor((x - 1) * (x - 5)), f'이차 조각 {sp.factor(q14)} (숨은 관계: 근 1, 5)')


def f14(xv):
    xv = sp.nsimplify(xv)
    r = xv - 10 * sp.floor((xv + 5) / 10)   # (-5, 5]
    if r == -5: r = sp.Integer(5)
    return lin.subs(x, r) if r < 0 else q14.subs(x, r)


def I14(s_, e_):
    """주기 10 함수의 [s_, e_] 정적분: 길이 5 조각 경계에서 나누어 적분"""
    s_, e_ = sp.Integer(s_), sp.Integer(e_)
    tot = 0; cur = s_
    while cur < e_:
        nxt = min(e_, 5 * sp.floor(cur / 5) + 5)
        k = sp.floor((cur + 5) / 10)
        lo, hi = cur - 10 * k, nxt - 10 * k
        piece = lin if (lo + hi) / 2 < 0 else q14
        tot += sp.integrate(piece, (x, lo, hi)); cur = nxt
    return tot


check(14, all(f14(R(i, 4) - 5) == f14(R(i, 4) + 5) for i in range(-80, 80)) and all(sp.limit(lin, x, -5, '+') == f14(-5) for _ in [0]) and f14(0) == lin.subs(x, 0),
      '(나) f(x-5)=f(x+5) 성립, x=0·x=±5 연속')
ans14 = I14(-42, -37) - I14(68, 70)
check(14, I14(-42, -37) == I14(-2, 3) == 5 and I14(68, 70) == I14(-2, 0) == 8 and ans14 == sp.integrate(q14, (x, 0, 3)) == -3,
      f'∫_-42^-37 = ∫_-2^3 = {I14(-2, 3)}, ∫_68^70 = ∫_-2^0 = {I14(-2, 0)}, 차 = ∫_0^3 (x-1)(x-5) = {ans14}')
ans_ok(14, ans14)
wrong_in(14, [-ans14, I14(-42, -37)], '차를 거꾸로 / 뒤 정적분 빼기 빠뜨림')
# 원문 J8: x+3, 주기 6, ∫_-33^-29 - ∫_57^60 = 4/3 (④)
o_s = sp.solve([sp.Eq(3, b2), sp.Eq(9 + 3 * a2 + b2, 0)], [a2, b2])
oq = x**2 + o_s[a2] * x + o_s[b2]
o14 = (sp.integrate(x + 3, (x, -3, 0)) + sp.integrate(oq, (x, 0, 1))) - sp.integrate(x + 3, (x, -3, 0))   # -33+36=3→[3,7]=[-3,1], 57-60=-3→[-3,0]
check('J8', o14 == R(4, 3) == orig_ans('J8'), f'J8 원문: f=(x-1)(x-3), ∫_-3^1 - ∫_-3^0 = {o14} = 원문 정답 {orig_ans("J8")}')
print('--- 14번 조건 빼 보기 ---')
# 연속 없음: x=0, x=5에서 이어지지 않아도 되면 a, b 자유
vals = [sp.integrate(x**2 + av * x + bv, (x, 0, 3)) for av, bv in [(-6, 5), (0, 0), (-4, 3)]]
ablation(14, "'연속'", vals, -3, 'a, b가 정해지지 않음')
ablation(14, '(나)', [], -3, undef='f(x)가 -5<x<=5 밖에서 정의되지 않아 두 정적분이 정해지지 않음')

# ================= 15번 (J60 예상밖 1) =================
# (가)에서 ∫_3^6 f = ∫_0^3 f + 12, (나) → ∫_0^3 f = -6. 증가: f(0)<f(x)<f(3) (0<x<3) → 3f(0) < -6 < 3f(3), f(3)=f(0)+4
I0 = sp.symbols('I0')
blk = sp.solve(sp.Eq(I0 + (I0 + 4 * 3), 0), I0)[0]
c3 = sp.symbols('c3', real=True)
rng = sp.solve_univariate_inequality(3 * (c3 - 4) < blk, c3, relational=False).intersect(sp.solve_univariate_inequality(blk < 3 * c3, c3, relational=False))
check(15, blk == -6 and rng == sp.Interval.open(-2, 2), f'∫_0^3 f = {blk}, 필요조건 f(0)<-2<f(3)=f(0)+4 → f(3)∈{rng}')
ints = [n for n in range(-10, 11) if rng.contains(n)]


def make15(base):
    """[0,3]의 식 base로 (가)를 이어 붙인 함수를 확인: 연속(이음매), 증가(도함수>=0, 0은 유한 개), (가), (나)"""
    f0, f3 = base.subs(x, 0), base.subs(x, 3)
    seam = sp.simplify(f3 - (f0 + 4)) == 0
    dpos = all(sp.diff(base, x).subs(x, R(i, 50)) >= 0 for i in range(0, 151)) and sp.diff(base, x) != 0
    zeros = [r for r in sp.solve(sp.diff(base, x), x) if r.is_real and 0 <= r <= 3]
    def ff(xv):
        n = sp.floor(sp.nsimplify(xv) / 3)
        return base.subs(x, xv - 3 * n) + 4 * n
    ga = all(sp.simplify(ff(R(i, 7)) - ff(R(i, 7) - 3) - 4) == 0 for i in range(-30, 40))
    gn = sp.simplify(sp.integrate(base, (x, 0, 3)) + sp.integrate(base + 4, (x, 0, 3))) == 0
    inc = all(ff(R(i, 10)) < ff(R(i + 1, 10)) for i in range(-40, 90))
    return seam and dpos and len(zeros) <= 2 and ga and gn and inc, f3


ex = {0: R(4, 3) * x - 4, 1: R(4, 27) * x**3 - 3, -1: -1 - 4 * (1 - x / 3)**3}
real = {}
for cv, base in ex.items():
    good, f3 = make15(base)
    real[cv] = good and f3 == cv
check(15, all(real.values()) and sorted(real) == ints, f'f(3)=-1, 0, 1인 예시 함수 모두 (가)(나)·연속·증가 만족: {real}, 가능한 정수 {ints}')
# 전수(필요조건 쪽): 정수 -10..10 중 열린구간 (-2, 2) 밖은 불가능(위 부등식), 안은 위 예시로 가능 → 3개
ans15 = sp.Integer(len(ints))
check(15, ans15 == 3, f'f(3)의 값이 될 수 있는 정수의 개수 {ans15}')
ans_ok(15, ans15)
# 오답: ③ 5 (등호 포함 [-2,2]) / ④ 4 (블록 증가량을 4로: 2I+4=0, I=-2, 평균 -2/3 → (-2/3, 10/3))
w_eq = len([n for n in range(-10, 11) if -2 <= n <= 2])
Iw = sp.solve(sp.Eq(I0 + (I0 + 4), 0), I0)[0]
w_blk = len([n for n in range(-10, 11) if Iw / 3 < n < Iw / 3 + 4])
check(15, w_eq == 5 and Iw == -2 and w_blk == 4, f'오답: 등호 포함 {w_eq}개, 블록 증가량 4로 보면 ∫_0^3 f={Iw}, 범위 ({Iw / 3}, {Iw / 3 + 4}) → {w_blk}개')
wrong_in(15, [w_eq, w_blk], '등호 포함 / 블록 증가량 착각')
# 원문 J60: [6,9] 넓이 = ∫_6^9 f = ∫_0^3 f + 24 = 18, f(6)=f(3)+4>2>0 이므로 [6,9]에서 f>0 (④)
o15 = blk + 24
check('J60', o15 == 18 == orig_ans('J60') and rng.inf + 4 >= 0, f'J60 원문: 넓이 = ∫_0^3 f + 24 = {o15}, f(6)=f(3)+4>{rng.inf + 4} → [6,9]에서 f>0, 원문 정답 {orig_ans("J60")}')
print('--- 15번 조건 빼 보기 ---')
# '증가' 없음: f = 4x/3 - 4 + h(x), h 주기 3, ∫_0^3 h = 0, h(0)=h(3)=cc → f(3)=cc 아무 값
vals = []
for cc in (-5, 0, 5):
    h = cc - R(2, 3) * cc * x * (3 - x)
    base = R(4, 3) * x - 4 + h
    chk = sp.simplify(base.subs(x, 3) - base.subs(x, 0) - 4) == 0 and sp.simplify(sp.integrate(base, (x, 0, 3)) + sp.integrate(base + 4, (x, 0, 3))) == 0
    if chk: vals.append(base.subs(x, 3))
ablation(15, "'증가'", vals, 3, 'f(3)이 어떤 실수도 될 수 있어 정수가 무수히 많음')
# (가) 없음: f=(x-s)^3+β, ∫_0^6 f=0 → f(3)이 s∈[0,3]에서 -27..0 연속으로 변함 → 정수 28개 이상
ss = sp.symbols('ss')
beta = sp.solve(sp.Eq(sp.integrate((x - ss)**3, (x, 0, 6)) + 6 * sp.Symbol('B'), 0), sp.Symbol('B'))[0]
f3s = sp.expand((3 - ss)**3 + beta)
cnt = len([n for n in range(-40, 10) if f3s.subs(ss, 0) <= n <= f3s.subs(ss, 3)])
ablation(15, '(가)', [], 3, undef=f'정해지지 않음: f=(x-s)^3+β(∫_0^6 f=0)에서 f(3)={f3s}가 s=0일 때 {f3s.subs(ss, 0)}, s=3일 때 {f3s.subs(ss, 3)} → 될 수 있는 정수 {cnt}개 이상')
# (나) 없음: f = 4x/3 + k → f(3) = 4 + k 아무 값
vals = [(R(4, 3) * x + kk).subs(x, 3) for kk in (-8, -4, 0)]
ablation(15, '(나)', vals, 3, 'f=4x/3+k에서 f(3)=4+k, 정수가 무수히 많음')
ablation(15, "'연속'", [], 3, undef='미적분Ⅰ에서 정적분은 연속함수에 대하여 정의하므로 (나)가 정해지지 않음')

# ================= 16번 (I66 후보_순위 1, 숫자만) =================
P_, Q_ = sp.symbols('P_ Q_')


def gprime(f):
    return lambda xv: sp.Abs(f.subs(x, xv + 1)) - sp.Abs(f.subs(x, xv))


def is_min(f, pt, eps=R(1, 1000)):
    gp = gprime(f)
    return sp.simplify(gp(pt)) == 0 and gp(pt - eps) < 0 and gp(pt + eps) > 0


def solve16(lead, p, q):
    """|f(p+1)|=|f(p)|, |f(q+1)|=|f(q)|의 부호 경우 4개를 모두 풀고, 실제로 x=p, x=q에서 극소인 f만 남김"""
    f = lead * x**2 + P_ * x + Q_
    out, cases = [], []
    for sp_ in (1, -1):
        for sq_ in (1, -1):
            eqs = [f.subs(x, p + 1) - sp_ * f.subs(x, p), f.subs(x, q + 1) - sq_ * f.subs(x, q)]
            sol = sp.solve(eqs, [P_, Q_], dict=True)
            for s in sol:
                ff = sp.expand(f.subs(s))
                good = is_min(ff, p) and is_min(ff, q)
                cases.append((('같은 부호' if sp_ == 1 else '반대 부호'), ('같은 부호' if sq_ == 1 else '반대 부호'), ff, good))
                if good: out.append(ff)
            if not sol:
                cases.append((('같은 부호' if sp_ == 1 else '반대 부호'), ('같은 부호' if sq_ == 1 else '반대 부호'), None, False))
    return out, cases


sols16, cases16 = solve16(2, -3, 2)
for cs_ in cases16:
    print(f'    경우 x=-3:{cs_[0]}, x=2:{cs_[1]} → f={cs_[2]}, 두 점 모두 극소: {cs_[3]}')
check(16, len(sols16) == 1 and sols16[0] == 2 * x**2 - 13, f'부호 경우 4개 전수 → 조건 만족 f = {sols16}(유일)')
f16 = sols16[0]
check(16, sp.expand(f16 + f16.subs(x, x + 1) - 4 * (x + 3) * (x - 2)) == 0, 'f(x)+f(x+1)=4(x+3)(x-2)')
rts = sorted(sp.solve(f16, x), key=float)
check(16, -3 < rts[0] < -2 and 2 < rts[1] < 3, f'f의 근 {rts}가 (-3,-2), (2,3)에 하나씩')
# g'(x)=|f(x+1)|-|f(x)|의 부호 변화를 -6..6에서 1/100 간격으로 전수 확인
gp = gprime(f16)
zs = []
for i in range(-600, 600):
    u, w = R(i, 100), R(i + 1, 100)
    if gp(u) == 0: zs.append(u)
    elif gp(u) * gp(w) < 0: zs.append((u + w) / 2)
mins = [z for z in zs if gp(z - R(1, 1000)) < 0 < gp(z + R(1, 1000))]
maxs = [z for z in zs if gp(z - R(1, 1000)) > 0 > gp(z + R(1, 1000))]
check(16, mins == [-3, 2] and len(maxs) == 1 and abs(maxs[0] - R(-1, 2)) < R(1, 50), f"g'의 부호 변화(-6..6): 극소 {mins}, 극대 ≈{[float(m) for m in maxs]}")
ans16 = f16.subs(x, 0)
ans_ok(16, ans16)
# 오답: ④ -12 (극소점을 근으로 2(x+3)(x-2)) / ⑤ -11 (g'=|f(x)|-|f(x-1)| → 극소 위치를 -4, 1로 푼 셈 = f(x+1))
w_root = (2 * (x + 3) * (x - 2)).subs(x, 0)
fw = sp.solve([(2 * x**2 + P_ * x + Q_).subs(x, -4) + (2 * x**2 + P_ * x + Q_).subs(x, -3), (2 * x**2 + P_ * x + Q_).subs(x, 1) + (2 * x**2 + P_ * x + Q_).subs(x, 2)], [P_, Q_], dict=True)[0]
w_shift = (2 * x**2 + P_ * x + Q_).subs(fw).subs(x, 0)
check(16, w_root == -12 and w_shift == -11 and sp.expand((2 * x**2 + P_ * x + Q_).subs(fw) - f16.subs(x, x + 1)) == 0, f'오답: 극소점=근 {w_root}, g\' 잘못(f(x+1)) {w_shift}')
wrong_in(16, [w_root, w_shift], '극소점을 근으로 / g\'을 |f(x)|-|f(x-1)|로')
# 같은 부호 경우가 극대로 빠지는 것 확인 (축 -5/2, 5/2)
same = [c_ for c_ in cases16 if c_[2] is not None and not c_[3]]
check(16, len(same) == 2 and all(c_[2].subs(x, -3) == -50 or c_[2].subs(x, 2) == -50 for c_ in same), f'같은 부호 경우 2개는 함숫값 -50<0인 창이라 극대로 제외: {[c_[2] for c_ in same]}')
# 원문 I66: 최고차 2, x=1, 4 → f(0)=13
so, _ = solve16(2, 1, 4)
check('I66', len(so) == 1 and so[0].subs(x, 0) == 13 == orig_ans('I66'), f'I66 원문: f={so}, f(0)=13 = 원문 정답 {orig_ans("I66")}')
# 작년 2025 기말 16(폭 b·오직 하나의 극값·존재 조건)과 다른 축: 폭 1·두 극소 위치 유지
print('--- 16번 조건 빼 보기 ---')
vals = []
for lead in (1, 2, 4):
    s_, _ = solve16(lead, -3, 2)
    vals += [s__.subs(x, 0) for s__ in s_]
ablation(16, "'최고차항의 계수가 2'", vals, -13, 'f=a(x^2-13/2)')


def one_min(lead, pt, fam):
    res = []
    for pv in fam:
        f = lead * x**2 + pv * x + Q_
        for sgn in (1, -1):
            qs = sp.solve(f.subs(x, pt + 1) - sgn * f.subs(x, pt), Q_)
            for qv in qs:
                ff = f.subs(Q_, qv)
                if is_min(ff, pt): res.append(ff.subs(x, 0))
    return res


ablation(16, "'x=-3에서 극소'", one_min(2, 2, [0, -2, -4]), -13, '남은 조건이 x=2 하나')
ablation(16, "'x=2에서 극소'", one_min(2, -3, [0, 2, 4]), -13, '남은 조건이 x=-3 하나')
# 절댓값 없음: g'=f(x+1)-f(x)=4x+2+p (일차) → 극값이 하나뿐이라 두 점에서 극소 불가
gl = sp.expand((2 * x**2 + P_ * x + Q_).subs(x, x + 1) - (2 * x**2 + P_ * x + Q_))
nos = sp.solve([gl.subs(x, -3), gl.subs(x, 2)], [P_, Q_], dict=True)
ablation(16, "'|f(t)|의 절댓값'", [] if not nos else [sp.Integer(0)], -13, f"g'={gl}는 일차식이라 x=-3, x=2에서 동시에 0일 수 없음")

print('ALL OK' if ok else 'SOME FAIL')
