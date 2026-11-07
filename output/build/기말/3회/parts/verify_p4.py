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
DBREF = {13: 'D43 예상밖 2', 14: 'J8 후보_순위 1', 15: 'J60 예상밖 1', 16: 'I66 v3_추가 2'}
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

# ================= 14번 (J8 후보_순위 1 + OP15: 주기 → 점 (5,0) 대칭, 시험지 8번) =================
a2, b2 = sp.symbols('a2 b2')
lin = x + 5
quad = x**2 + a2 * x + b2
# x=0 연속: b=5, (나)에 x=0: f(5)=-f(5) → f(5)=0
s14 = sp.solve([sp.Eq(lin.subs(x, 0), quad.subs(x, 0)), sp.Eq(quad.subs(x, 5), -quad.subs(x, 5))], [a2, b2], dict=True)
check(14, len(s14) == 1 and s14[0] == {a2: -6, b2: 5}, f'x=0 연속, f(5)=-f(5)=0 → {s14}(유일)')
q14 = quad.subs(s14[0])


def f14(xv, mode='point'):
    """(가)로 x<=5, (나)로 x>5: point f(x)=-f(10-x) / line f(10-x) / shift -f(x-5)(원문 주기 습관)"""
    xv = sp.nsimplify(xv)
    if xv <= 5:
        return lin.subs(x, xv) if xv < 0 else q14.subs(x, xv)
    if mode == 'point': return -f14(10 - xv)
    if mode == 'line': return f14(10 - xv)
    return -f14(xv - 5)


def I14(s_, e_, mode='point'):
    """구간을 경계(0, 5, 10)에서 나누어 각 조각의 다항식을 적분"""
    cuts = sorted({sp.Integer(s_), sp.Integer(e_)} | {c for c in (0, 5, 10) if s_ < c < e_})
    tot = 0
    for lo, hi in zip(cuts, cuts[1:]):
        mid = (lo + hi) / 2
        if mid < 5: piece = lin if mid < 0 else q14
        elif mode == 'point': piece = -(lin if 10 - mid < 0 else q14).subs(x, 10 - x)
        elif mode == 'line': piece = (lin if 10 - mid < 0 else q14).subs(x, 10 - x)
        else: piece = -(lin if mid - 5 < 0 else q14).subs(x, x - 5)
        tot += sp.integrate(piece, (x, lo, hi))
    return tot


xs = [R(i, 4) for i in range(-40, 81)]
check(14, all(f14(5 + u) == -f14(5 - u) for u in [R(i, 4) for i in range(0, 60)]) and all(abs(f14(c + R(1, 10**6)) - f14(c - R(1, 10**6))) < R(1, 1000) for c in (0, 5, 10)),
      '(나) f(5+x)=-f(5-x) 성립, x=0·5·10에서 연속(실수 전체에서 정의)')
ans14 = I14(5, 8)
check(14, ans14 == -sp.integrate(q14, (x, 2, 5)) == 9, f'∫_5^8 f = -∫_2^5 (x-1)(x-5) dx = {ans14}')
ans_ok(14, ans14)
w_shift = I14(5, 8, 'shift'); w_line = I14(5, 8, 'line')
check(14, w_shift == 3 and w_line == -9 and str(w_line) not in IT[14]['choices'], f'오답: 주기 습관(오른쪽으로 옮겨 뒤집음) {w_shift}, 선대칭 착각 {w_line}(선지 밖)')
v = ch(14); wv = [sp.Rational(z) for z in IT[14]['wrongs']]
check(14, wv == [w_shift] and w_shift in v and w_shift != ans14, f'오답 {wv} 선지에 있음(시험지 8번 자리: 1개 이상)')
# 원문 J8: x+3, 주기 6, ∫_-33^-29 - ∫_57^60 = 4/3 (④)
o_s = sp.solve([sp.Eq(3, b2), sp.Eq(9 + 3 * a2 + b2, 0)], [a2, b2])
oq = x**2 + o_s[a2] * x + o_s[b2]
o14 = (sp.integrate(x + 3, (x, -3, 0)) + sp.integrate(oq, (x, 0, 1))) - sp.integrate(x + 3, (x, -3, 0))   # -33+36=3→[3,7]=[-3,1], 57-60=-3→[-3,0]
check('J8', o14 == R(4, 3) == orig_ans('J8'), f'J8 원문: f=(x-1)(x-3), ∫_-3^1 - ∫_-3^0 = {o14} = 원문 정답 {orig_ans("J8")}')
print('--- 14번 조건 빼 보기 ---')
# 연속 없음: b 자유, (나)의 f(5)=0만 → a=-(25+b)/5
vals = []
for bv in (5, 0, 10):
    qq = x**2 - sp.Rational(25 + bv, 5) * x + bv
    vals.append(-sp.integrate(qq, (x, 2, 5)))
ablation(14, "'연속'", vals, 9, 'b가 정해지지 않음(a=-(25+b)/5)')
ablation(14, '(나)', [], 9, undef='x>5에서 f(x)가 정의되지 않아 ∫_5^8 f가 정해지지 않음')

# ================= 15번 (J60 예상밖 1 + OP10·OP01·OP05: f(x+2)=f(x)+6, ∫_-1^3 f=0) =================
# (가)에서 ∫_1^3 f = ∫_-1^1 f + 12, (나) → ∫_-1^1 f = -6. 증가: f(-1)<f(x)<f(1) → 2f(-1) < -6 < 2f(1), f(1)=f(-1)+6, f(3)=f(1)+6
I0 = sp.symbols('I0')
blk = sp.solve(sp.Eq(I0 + (I0 + 6 * 2), 0), I0)[0]
c1 = sp.symbols('c1', real=True)
rng1 = sp.solve_univariate_inequality(2 * (c1 - 6) < blk, c1, relational=False).intersect(sp.solve_univariate_inequality(blk < 2 * c1, c1, relational=False))
rng = sp.Interval.open(rng1.inf + 6, rng1.sup + 6)
check(15, blk == -6 and rng1 == sp.Interval.open(-3, 3) and rng == sp.Interval.open(3, 9), f'∫_-1^1 f = {blk}, f(-1)<-3<f(1)=f(-1)+6 → f(1)∈{rng1}, f(3)=f(1)+6∈{rng}')
ints = [n for n in range(-20, 21) if rng.contains(n)]
tt = (x + 1) / 2


def make15(base):
    """[-1,1]의 식 base로 (가)를 이어 붙인 함수를 확인: 연속(이음매), 증가, (가), (나)"""
    fl, fr = base.subs(x, -1), base.subs(x, 1)
    seam = sp.simplify(fr - (fl + 6)) == 0
    dpos = all(sp.diff(base, x).subs(x, -1 + R(i, 50)) >= 0 for i in range(0, 101)) and sp.diff(base, x) != 0
    def ff(xv):
        n = sp.floor((sp.nsimplify(xv) + 1) / 2)
        return base.subs(x, xv - 2 * n) + 6 * n
    ga = all(sp.simplify(ff(R(i, 7) + 2) - ff(R(i, 7)) - 6) == 0 for i in range(-30, 40))
    gn = sp.simplify(sp.integrate(base, (x, -1, 1)) + sp.integrate(base + 6, (x, -1, 1))) == 0
    inc = all(ff(R(i, 10)) < ff(R(i + 1, 10)) for i in range(-40, 90))
    return seam and dpos and ga and gn and inc, ff(3)


ex = {6: 6 * tt - 6, 7: 6 * tt**2 - 5, 8: 6 * tt**5 - 4, 5: -1 - 6 * (1 - tt)**2, 4: -2 - 6 * (1 - tt)**5}
real = {}
for cv, base in ex.items():
    good, f3 = make15(sp.expand(base))
    real[cv] = good and f3 == cv
check(15, all(real.values()) and sorted(real) == ints, f'f(3)=4..8인 예시 함수 모두 (가)(나)·연속·증가 만족: {real}, 가능한 정수 {ints}')
ans15 = sp.Integer(len(ints))
check(15, ans15 == 5, f'f(3)=k가 될 수 있는 정수 k의 개수 {ans15}')
ans_ok(15, ans15)
# 오답: ③ 7 (등호 포함 [3,9]) / ④ 6 (블록 증가량을 6으로: 2I+6=0, I=-3, 평균 -3/2 → f(3)∈(9/2, 21/2))
w_eq = len([n for n in range(-20, 21) if 3 <= n <= 9])
Iw = sp.solve(sp.Eq(I0 + (I0 + 6), 0), I0)[0]
w_blk = len([n for n in range(-20, 21) if Iw / 2 + 6 < n < Iw / 2 + 12])
check(15, w_eq == 7 and Iw == -3 and w_blk == 6, f'오답: 등호 포함 {w_eq}개, 블록 증가량 6으로 보면 ∫_-1^1 f={Iw}, f(3)∈({Iw / 2 + 6}, {Iw / 2 + 12}) → {w_blk}개')
wrong_in(15, [w_eq, w_blk], '등호 포함 / 블록 증가량 착각')
# 작년 2025 기말 9번 꼴(f(x+3)=f(x)+3)과 다른지: 이동 폭 2, 증가량 6
check(15, (2, 6) != (3, 3) and (2, 6) != (3, 4), '(가) 이동 폭·증가량 (2, 6) ≠ 원문 (3, 4) ≠ 작년 (3, 3)')
# 원문 J60: [6,9] 넓이 = ∫_6^9 f = ∫_0^3 f + 24 = 18 (∫_0^3 f = -6), f(6)=f(3)+4>2>0 (④)
o_blk = sp.solve(sp.Eq(I0 + (I0 + 12), 0), I0)[0]
o15 = o_blk + 24
check('J60', o15 == 18 == orig_ans('J60'), f'J60 원문: ∫_0^3 f={o_blk}, 넓이 = ∫_0^3 f + 24 = {o15}, 원문 정답 {orig_ans("J60")}')
print('--- 15번 조건 빼 보기 ---')
# '증가' 없음: f = 3x - 3 + h(x), h 주기 2, ∫_-1^1 h = 0, h(±1)=cc → f(3)=6+cc 아무 값
vals = []
for cc in (-5, 0, 5):
    h = cc - R(3, 2) * cc * (1 - x**2)
    base = 3 * x - 3 + h
    chk = sp.simplify(base.subs(x, 1) - base.subs(x, -1) - 6) == 0 and sp.simplify(sp.integrate(base, (x, -1, 1)) + sp.integrate(base + 6, (x, -1, 1))) == 0
    if chk: vals.append(base.subs(x, 1) + 6)
ablation(15, "'증가'", vals, 5, 'f(3)이 어떤 실수도 될 수 있어 정수가 무수히 많음')
# (가) 없음: f=(x-s)^3+β, ∫_-1^3 f=0 → f(3)이 s에 따라 연속으로 변함
ss = sp.symbols('ss'); Bs = sp.Symbol('B')
beta = sp.solve(sp.Eq(sp.integrate((x - ss)**3, (x, -1, 3)) + 4 * Bs, 0), Bs)[0]
f3s = sp.expand((3 - ss)**3 + beta)
lo_, hi_ = sorted([f3s.subs(ss, 1), f3s.subs(ss, 3)])
cnt = len([n for n in range(-100, 100) if lo_ <= n <= hi_])
ablation(15, '(가)', [], 5, undef=f'정해지지 않음: f=(x-s)^3+β(∫_-1^3 f=0)에서 f(3)={f3s}가 s=1일 때 {f3s.subs(ss, 1)}, s=3일 때 {f3s.subs(ss, 3)} → 될 수 있는 정수 {cnt}개 이상')
# (나) 없음: f = 3x + k → f(3) = 9 + k 아무 값
vals = [(3 * x + kk).subs(x, 3) for kk in (-8, -4, 0)]
ablation(15, '(나)', vals, 5, 'f=3x+k에서 f(3)=9+k, 정수가 무수히 많음')
ablation(15, "'연속'", [], 5, undef='미적분Ⅰ에서 정적분은 연속함수에 대하여 정의하므로 (나)가 정해지지 않음')

# ================= 16번 (I66 v3_추가 2 + v3_추가 1: 계수 미정·극댓값 + 기준선 y=x) =================
P_, Q_ = sp.symbols('P_ Q_')
pp = sp.symbols('pp', positive=True)


def gprime(h):
    return lambda xv: sp.Abs(h.subs(x, xv + 1)) - sp.Abs(h.subs(x, xv))


def is_min(h, pt, eps=R(1, 1000)):
    gp = gprime(h)
    return bool(sp.simplify(gp(pt)) == 0) and bool(gp(pt - eps) < 0) and bool(gp(pt + eps) > 0)


def solve_pos(lead, p, q):
    """h=lead x^2+P x+Q: |h(p+1)|=|h(p)|, |h(q+1)|=|h(q)| 부호 경우 4개를 풀고 x=p, x=q에서 모두 극소인 h만"""
    h = lead * x**2 + P_ * x + Q_
    out, cases = [], []
    for sp_ in (1, -1):
        for sq_ in (1, -1):
            sol = sp.solve([h.subs(x, p + 1) - sp_ * h.subs(x, p), h.subs(x, q + 1) - sq_ * h.subs(x, q)], [P_, Q_], dict=True)
            for s in sol:
                hh = sp.expand(h.subs(s)); good = is_min(hh, p) and is_min(hh, q)
                cases.append((sp_, sq_, hh, good))
                if good: out.append(hh)
            if not sol: cases.append((sp_, sq_, None, False))
    return out, cases


def extrema(h, lo=-8, hi=8, n=100):
    gp = gprime(h); zs = []
    for i in range(lo * n, hi * n):
        u, w = R(i, n), R(i + 1, n)
        if gp(u) == 0: zs.append(u)
        elif gp(u) * gp(w) < 0: zs.append(sp.nsimplify((u + w) / 2))
    e = R(1, 10 * n)
    return [z for z in zs if gp(z - e) < 0 < gp(z + e)], [z for z in zs if gp(z - e) > 0 > gp(z + e)]


def gval(h, xv):
    rts = sorted([r for r in sp.solve(h, x) if r.is_real], key=float)
    cuts = [sp.nsimplify(xv)] + [r for r in rts if xv < r < xv + 1] + [sp.nsimplify(xv) + 1]
    return sum(sp.Abs(sp.integrate(h, (x, a_, b_))) for a_, b_ in zip(cuts, cuts[1:]))


# 계수 p를 여러 양수로 두어도 극소 위치 조건의 해는 h=p(x^2-5x+5) 하나(부호 경우 전수)
okp = True
for lv in (1, 2, 6, R(1, 3)):
    s_, cs_ = solve_pos(lv, 1, 3)
    okp &= len(s_) == 1 and sp.expand(s_[0] - lv * (x**2 - 5 * x + 5)) == 0 and sum(c[3] for c in cs_) == 1
check(16, okp, '최고차항 p>0이면 부호 경우 4개 중 반대·반대만 남아 h=f-x=p(x^2-5x+5) (p=1, 2, 6, 1/3 확인)')
s6, cs6 = solve_pos(6, 1, 3)
for c_ in cs6:
    print(f"    경우 x=1:{'같은' if c_[0] == 1 else '반대'} 부호, x=3:{'같은' if c_[1] == 1 else '반대'} 부호 → h={c_[2]}, 두 점 모두 극소: {c_[3]}")
hP = pp * (x**2 - 5 * x + 5)
mins, maxs = extrema(hP.subs(pp, 1))
check(16, mins == [1, 3] and maxs == [2], f"g'(x) 부호 변화(-8..8): 극소 {mins}, 극대 {maxs}(극댓값은 하나)")
gmax = sp.simplify(-sp.integrate(hP, (x, 2, 3)))
check(16, gmax == R(7, 6) * pp and gval(hP.subs(pp, 6), 2) == 7, f'극댓값 g(2) = {gmax} (p=6이면 {gval(hP.subs(pp, 6), 2)})')
psol = sp.solve(sp.Eq(gmax, 7), pp)
f16 = sp.expand(hP.subs(pp, psol[0]) + x)
check(16, psol == [6] and f16 == 6 * x**2 - 29 * x + 30, f'7p/6=7 → p={psol}, f={f16}')
ans16 = f16.subs(x, 1)
ans_ok(16, ans16)
# 오답: ② 6 (기준선 무시 |f| → f=h) / ① 5 (h=f+x로 부호 잘못: f=h-x)
h6 = hP.subs(pp, 6)
w_nob = h6.subs(x, 1); w_sgn = (h6 - x).subs(x, 1)
check(16, w_nob == 6 and w_sgn == 5, f'오답: 기준선 무시 {w_nob}, 기준선 부호 실수 {w_sgn}')
wrong_in(16, [w_nob, w_sgn], '기준선 y=x 무시 / f=h-x 부호 실수')
# 원문 I66: 최고차 2, x=1, 4 → f(0)=13
so, _ = solve_pos(2, 1, 4)
check('I66', len(so) == 1 and so[0].subs(x, 0) == 13 == orig_ans('I66'), f'I66 원문: f={so}, f(0)=13 = 원문 정답 {orig_ans("I66")}')
print('--- 16번 조건 빼 보기 ---')
# '양수' 없음: p<0이어도 반대·반대 극소, 극대는 x=2에서 g(2)=-7p/6=7 → p=-6, f(1)=-6+1=-5
sn, _ = solve_pos(-6, 1, 3)
mn, mx = extrema(sn[0])
gneg = gval(sn[0], 2)
ablation(16, "'최고차항의 계수가 양수'", [7, (sn[0] + x).subs(x, 1)] if (mn == [1, 3] and mx == [2] and gneg == 7) else [7], 7, 'p=-6에서도 x=1, 3 극소·극댓값 7 → f(1)=-5')
# '극댓값이 7' 없음: p 자유 → f(1)=p+1
ablation(16, "'극댓값이 7'", [(hP + x).subs(x, 1).subs(pp, pv) for pv in (2, 6, 12)], 7, 'p가 정해지지 않음, f(1)=p+1')


def one_min(pt, side):
    """극소 하나(pt)와 극댓값 7, p>0만 남긴 경우: h=p((x-c)^2-w^2), w^2=1/4+s^2이면 극소 c-1/2±s, 극대 c-1/2, 극댓값 p(w^2-1/12)"""
    res = []
    for sv in (1, 2, R(1, 2)):
        w2 = R(1, 4) + sv**2
        pv = 7 / (w2 - R(1, 12))
        c = pt + R(1, 2) - side * sv
        h = pv * ((x - c)**2 - w2)
        mn_, mx_ = extrema(h, -8, 8, 20)
        if pt in mn_ and len(mx_) == 1 and gval(h, mx_[0]) == 7:
            res.append((h + x).subs(x, 1))
    return res


ablation(16, "'x=1에서 극소'", one_min(3, 1), 7, '남은 극소 조건이 x=3 하나라 h가 정해지지 않음')
ablation(16, "'x=3에서 극소'", one_min(1, -1), 7, '남은 극소 조건이 x=1 하나라 h가 정해지지 않음')
ablation(16, "기준선 '-t'", [w_nob], 7, '|f(t)|이면 f=h, f(1)=6')
gl = sp.expand((pp * x**2 + P_ * x + Q_).subs(x, x + 1) - (pp * x**2 + P_ * x + Q_))
nos = sp.solve([gl.subs(x, 1), gl.subs(x, 3)], [P_, Q_], dict=True)
ablation(16, "'|f(t)-t|의 절댓값'", [] if not nos else [sp.Integer(0)], 7, f"g'={gl}는 일차식이라 x=1, x=3에서 동시에 0일 수 없음")

print('ALL OK' if ok else 'SOME FAIL')
