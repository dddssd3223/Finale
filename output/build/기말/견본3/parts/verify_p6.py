# -*- coding: utf-8 -*-
# p6 (18번, M33 구조 변경) 검증: sympy 정확 계산 + 경우 전수 조사 + 정수 격자 전수 스캔
#  f(x)=x^3+ax+b, c 실수, g(x)=(x-c)|f(x)|
#  S={k | |g(x)-k| 가 실수 전체에서 미분가능}
#  (가) |S|=1  (나) g(x)=0 의 서로 다른 실근 2개  (다) g 의 극솟값 -81
#  답: f(0) = -16 (정답 ④)
import sympy as sp
import os, random

x = sp.symbols('x', real=True)
PREC = 60
EPS = sp.Rational(1, 10**30)


def N(v):
    return sp.N(v, PREC)


# ---------------------------------------------------------------------
# 일반 도구: 연속 조각 다항함수 g = [(식, 왼끝, 오른끝)] 에 대해
#   미분가능성, 정지점, 집합 S, 극솟값/극댓값을 정확히 계산
# ---------------------------------------------------------------------
def real_roots_in(poly_expr, lo, hi):
    """lo < x < hi (lo, hi 는 유리수 또는 ±oo) 의 실근 (정확값)"""
    P = sp.Poly(sp.expand(poly_expr), x)
    if P.is_zero:
        raise ValueError('항등적으로 0인 조각')
    out = []
    for r in set(sp.real_roots(P)):
        v = N(r)
        if (lo == -sp.oo or v > N(lo)) and (hi == sp.oo or v < N(hi)):
            out.append(r)
    return out


def analyze(pieces):
    """pieces: 왼쪽부터 [(expr, lo, hi)], 연속 가정. 반환 dict"""
    # 연속성 확인
    for (e1, _, h1), (e2, l2, _) in zip(pieces, pieces[1:]):
        assert h1 == l2
        assert sp.simplify(e1.subs(x, h1) - e2.subs(x, l2)) == 0, '불연속'
    # 꺾인 점(이음점에서 좌우 미분계수 다름)
    corners = []
    for (e1, _, h1), (e2, _, _) in zip(pieces, pieces[1:]):
        dl = sp.diff(e1, x).subs(x, h1)
        dr = sp.diff(e2, x).subs(x, h1)
        if sp.simplify(dl - dr) != 0:
            corners.append(h1)
    # 끝 행동: -oo 에서 -oo, +oo 에서 +oo (또는 반대) 이어야 전사
    lim_l = sp.limit(pieces[0][0], x, -sp.oo)
    lim_r = sp.limit(pieces[-1][0], x, sp.oo)
    surj = {lim_l, lim_r} == {-sp.oo, sp.oo}
    # 정지점 (조각 내부의 g'=0, 그리고 미분가능한 이음점 중 g'=0)
    stat = []
    for e, lo, hi in pieces:
        stat += real_roots_in(sp.diff(e, x), lo, hi)
    for (e1, _, h1), (e2, _, _) in zip(pieces, pieces[1:]):
        if h1 not in corners and sp.diff(e1, x).subs(x, h1) == 0:
            stat.append(h1)
    stat = sorted(set(stat), key=lambda r: float(N(r)))

    def piece_of(v):
        for e, lo, hi in pieces:
            if (lo == -sp.oo or v >= N(lo)) and (hi == sp.oo or v <= N(hi)):
                return e
        raise ValueError

    def gval(r):
        return piece_of(N(r)).subs(x, r)

    def dval(r, side):
        """r 근방 side(+1 오른쪽, -1 왼쪽)에서 g' 의 부호"""
        t = N(r) + side * EPS
        return sp.sign(N(sp.diff(piece_of(t), x).subs(x, t)))

    # 집합 S
    if corners:
        S = []
    else:
        assert surj
        cand = []
        for r in stat:
            k = sp.simplify(gval(r))
            if all(abs(N(k - q)) > 1e-40 for q in cand):
                cand.append(k)
        statN = [N(r) for r in stat]
        S = []
        for k in cand:
            sols = []
            if k.is_Rational:
                for e, lo, hi in pieces:
                    sols += [N(s) for s in real_roots_in(e - k, lo, hi)]
            else:  # 무리수 높이: 고정밀 수치 근
                kN = N(k)
                for e, lo, hi in pieces:
                    cs_ = [sp.Float(cf, PREC) for cf in sp.Poly(e, x).all_coeffs()]
                    cs_[-1] -= kN
                    for z in sp.Poly(cs_, x).nroots(n=PREC, maxsteps=500):
                        if abs(sp.im(z)) < 1e-20:
                            v = sp.re(z)
                            if (lo == -sp.oo or v > N(lo) - 1e-20) and (hi == sp.oo or v < N(hi) + 1e-20):
                                sols.append(v)
            for (e1, _, h1), _ in zip(pieces, pieces[1:]):
                if abs(N(e1.subs(x, h1) - k)) < 1e-40:
                    sols.append(N(h1))
            tol = 1e-40 if k.is_Rational else 1e-12
            ok = all(any(abs(s_ - t_) < tol for t_ in statN) for s_ in sols)
            if ok:
                S.append(k)
    # 극값 (g' 부호 변화)
    mins, maxs = [], []
    for r in stat:
        L, R = dval(r, -1), dval(r, 1)
        if L < 0 < R:
            mins.append(gval(r))
        if L > 0 > R:
            maxs.append(gval(r))
    for r in corners:  # 꺾인 점에서의 극값도 포함
        L, R = dval(r, -1), dval(r, 1)
        if L < 0 < R:
            mins.append(gval(r))
        if L > 0 > R:
            maxs.append(gval(r))
    return dict(corners=corners, stat=stat, S=S, mins=mins, maxs=maxs, surj=surj)


def pieces_g(f, c):
    """g(x)=(x-c)|f(x)| 를 f 의 실근(유리수만 허용)으로 잘라 조각으로"""
    rts = sorted({r for r in sp.real_roots(sp.Poly(f, x))}, key=lambda r: float(N(r)))
    assert all(r.is_Rational for r in rts), rts
    cuts = [-sp.oo] + rts + [sp.oo]
    out = []
    for lo, hi in zip(cuts, cuts[1:]):
        if lo == -sp.oo and hi == sp.oo:
            t = 0
        elif lo == -sp.oo:
            t = hi - 1
        elif hi == sp.oo:
            t = lo + 1
        else:
            t = (lo + hi) / 2
        s = sp.sign(f.subs(x, t))
        out.append((sp.expand((x - c) * s * f), lo, hi))
    return out


def roots_g0(f, c):
    """g(x)=0 의 서로 다른 실근 개수"""
    rts = {N(r) for r in sp.real_roots(sp.Poly(f, x))}
    rts = list(rts)
    n = len(rts)
    if all(abs(r - c) > 1e-40 for r in rts):
        n += 1
    return n


def conds(f, c):
    """(가)(나)(다) 판정과 분석 결과"""
    A = analyze(pieces_g(f, c))
    ga = len(A['S']) == 1
    na = roots_g0(f, c) == 2
    da = len(A['mins']) >= 1 and all(abs(N(m + 81)) < 1e-40 for m in A['mins'])
    return ga, na, da, A


allok = True


def check(cond, msg):
    global allok
    print(('OK   ' if cond else 'FAIL ') + msg)
    if not cond:
        allok = False


print('=== 18번 (M33 구조 변경) ===')

# ---------------------------------------------------------------------
# 0. 꺾인 점 보조정리: f(p)=0, f'(p)≠0, p≠c 이면 x=p 에서 g 의 좌우 미분계수가 ±(p-c)|f'(p)|
# ---------------------------------------------------------------------
p, c, q, r = sp.symbols('p c q r', real=True)
fp = (x - p) * (x**2 + q * x + r)        # x=p 에서 단순근인 일반 삼차 (h(p)=p^2+qp+r≠0)
hp = (p**2 + q * p + r)
right = sp.diff((x - c) * fp, x).subs(x, p)   # f>0 쪽 기울기 (부호는 h(p) 부호에 따라)
check(sp.simplify(right - (p - c) * hp) == 0,
      '보조정리: x=p 에서 (x-c)f 의 기울기 = (p-c)f\'(p), |f| 로 바꾸면 좌우가 부호만 반대 → p≠c, f\'(p)≠0 이면 꺾임')

# ---------------------------------------------------------------------
# 1. (나)를 만족시키는 f 의 근 구조 네 경우 (x^2 의 계수가 0)
# ---------------------------------------------------------------------
print('--- 경우 ①~④ 의 꼴 결정 (x^2 계수 0)')
c = sp.symbols('c', real=True)
pp = sp.symbols('pp', real=True)
sol1 = sp.solve(sp.Poly(sp.expand((x - c) * (x - pp)**2), x).coeff_monomial(x**2), pp)
sol2 = sp.solve(sp.Poly(sp.expand((x - c)**2 * (x - pp)), x).coeff_monomial(x**2), pp)
sol3 = sp.solve(sp.Poly(sp.expand((x - pp)**3), x).coeff_monomial(x**2), pp)
check(sol1 == [-c / 2], f'① f=(x-c)(x-p)^2 → p={sol1}')
check(sol2 == [-2 * c], f'② f=(x-c)^2(x-p) → p={sol2}')
check(sol3 == [0], f'③ f=(x-p)^3 → p={sol3} (f=x^3)')

# 동차성: x=|c|t 로 두면 g_c(|c|t) = c^4 g_{sgn c}(t)  (①, ②, ③ 모두)
t = sp.symbols('t', real=True)
cp = sp.symbols('cp', positive=True)
for name, F in [('①', lambda cc: (x - cc) * (x + cc / 2)**2), ('②', lambda cc: (x - cc)**2 * (x + 2 * cc)), ('③', lambda cc: x**3)]:
    for sg in (1, -1):
        lhs = ((x - sg * cp) * F(sg * cp)).subs(x, cp * t)
        rhs = cp**4 * ((x - sg) * F(sg)).subs(x, t)
        check(sp.expand(lhs - rhs) == 0, f'{name} 동차성 (c 부호 {sg:+d}): (x-c)f 가 c^4 배로 닮음 → |f| 도 같음')

# ---------------------------------------------------------------------
# 2. 각 경우의 S, 극솟값 (c=±1 정규형 + 여러 c 직접)
# ---------------------------------------------------------------------
print('--- 경우별 S 와 극솟값')
for cc in [sp.Integer(1), sp.Integer(-1), sp.Integer(4), sp.Integer(-4), sp.Rational(2, 3), sp.Integer(6)]:
    f1 = sp.expand((x - cc) * (x + cc / 2)**2)
    A = analyze(pieces_g(f1, cc))
    if cc > 0:
        check(A['corners'] == [] and A['S'] == [0] and len(A['mins']) == 1
              and sp.simplify(A['mins'][0] + sp.Rational(81, 256) * cc**4) == 0,
              f'① c={cc}: 미분가능, S={A["S"]}, 극솟값 {A["mins"]} = -81c^4/256')
    else:
        check(A['corners'] == [] and A['S'] == [0] and A['mins'] == [0],
              f'① c={cc}: S={A["S"]}, 극솟값 {A["mins"]} = 0 → (다) 불가')
    f2 = sp.expand((x - cc)**2 * (x + 2 * cc))
    A2 = analyze(pieces_g(f2, cc))
    check(A2['corners'] == [-2 * cc] and A2['S'] == [], f'② c={cc}: x={-2*cc} 에서 꺾임, S=∅')
    A3 = analyze(pieces_g(x**3, cc))
    check(A3['corners'] == [] and A3['S'] == [], f'③ f=x^3, c={cc}: 미분가능하지만 S={A3["S"]} (공집합)')
# ③ 에서 0∉S 인 이유: g(c)=0, g'(c)=|c|^3
cs = sp.symbols('cs', nonzero=True, real=True)
check(sp.simplify(sp.diff((x - cs) * sp.Abs(x)**3, x).subs(x, cs) - sp.Abs(cs)**3) == 0, "③ g'(c)=|c|^3≠0")

# ④ 허근 두 개 + 실근 p (p≠c): 무작위 표본에서 모두 꺾임, S=∅
random.seed(18)
cnt4 = 0
for _ in range(60):
    P = sp.Rational(random.randint(-12, 12), random.randint(1, 4))
    R = sp.Rational(3, 4) * P**2 + sp.Rational(random.randint(1, 40), random.randint(1, 5))  # x^2+Px+R 판별식<0
    f4 = sp.expand((x - P) * (x**2 + P * x + R))
    assert sp.Poly(f4, x).coeff_monomial(x**2) == 0
    C = sp.Rational(random.randint(-12, 12), random.randint(1, 3))
    if C == P:
        continue
    A4 = analyze(pieces_g(f4, C))
    cnt4 += (A4['corners'] == [P] and A4['S'] == [] and roots_g0(f4, C) == 2)
    if not (A4['corners'] == [P] and A4['S'] == []):
        check(False, f'④ 반례 P={P} R={R} c={C}')
check(cnt4 >= 55, f'④ 표본 {cnt4}개 모두 (나)는 만족하나 x=p 에서 꺾여 S=∅')

# ---------------------------------------------------------------------
# 3. (다)로 c 결정 → 답
# ---------------------------------------------------------------------
print('--- (다) 와 답')
csol = [s for s in sp.solve(sp.Rational(81, 256) * cp**4 - 81, cp)]
check(csol == [4], f'① c>0, 81c^4/256=81 → c={csol}')
fans = sp.expand((x - 4) * (x + 2)**2)
check(fans == x**3 - 12 * x - 16, f'f(x)={fans}')
ga, na, da, A = conds(fans, sp.Integer(4))
check(ga and na and da, f'정답 함수: (가){ga} (나){na} (다){da}, S={A["S"]}, 극솟값={A["mins"]}, 극댓값={A["maxs"]}')
ANS = fans.subs(x, 0)

# ---------------------------------------------------------------------
# 4. 정수 격자 전수 스캔: a∈[-30,6], b∈[-40,40], c∈[-8,8]
#    (가)(나)(다) 를 모두 만족시키는 (a,b,c) 는 (-12,-16,4) 하나뿐인지
# ---------------------------------------------------------------------
print('--- 정수 격자 전수 스캔')
hits, pass_na, pass_ga_na = [], 0, []
for a in range(-30, 7):
    for b in range(-40, 41):
        f = x**3 + a * x + b
        Pf = sp.Poly(f, x)
        rts = sp.real_roots(Pf)
        if not all(rr.is_Rational for rr in rts):
            # 유리계수 삼차의 무리 실근은 단순근이고 정수 c 와 다르므로 x=그 근에서 꺾임 → S=∅ (보조정리)
            irr = [rr for rr in rts if not rr.is_Rational]
            assert all(abs(N(sp.diff(f, x).subs(x, rr))) > 1e-30 for rr in irr)
            continue
        for cc in range(-8, 9):
            if roots_g0(f, cc) != 2:
                continue
            pass_na += 1
            ga, na, da, A = conds(f, sp.Integer(cc))
            if ga:
                pass_ga_na.append((a, b, cc))
            if ga and na and da:
                hits.append((a, b, cc))
print('  (나) 만족', pass_na, '개 · (가)(나) 만족', pass_ga_na)
check(hits == [(-12, -16, 4)], f'(가)(나)(다) 모두 만족: {hits}')
check(all(sp.expand(x**3 + a * x + b - (x - cc) * (x + sp.Rational(cc, 2))**2) == 0 for a, b, cc in pass_ga_na),
      '(가)(나) 를 만족시키는 격자점은 모두 ① 꼴 f=(x-c)(x+c/2)^2')

# ---------------------------------------------------------------------
# 5. 선지·오답 확인
# ---------------------------------------------------------------------
print('--- 선지')
ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p6.py'), encoding='utf-8').read(), ns)
it = ns['ITEMS'][18]
ch = [sp.Rational(s) for s in it['choices']]
check(len(set(ch)) == 5, '선지 5개 서로 다름')
d = {ch[i + 1] - ch[i] for i in range(4)}
check(len(d) == 1, f'선지 등차 (공차 {d})')
check(ch[it['ans'] - 1] == ANS and it['ans'] == 4, f'정답 f(0)={ANS} = ④ {it["choices"][3]}')
# 오답 근거 값
w_x3 = (x**3).subs(x, 0)                                   # ③ f=x^3 을 넣은 경우
w_neg = sp.expand((x + 4) * (x - 2)**2).subs(x, 0)          # c=-4 를 택한 경우
A_neg = analyze(pieces_g(sp.expand((x + 4) * (x - 2)**2), sp.Integer(-4)))
check(w_x3 in ch and w_x3 != ANS, f'오답 {w_x3}: f=x^3 (③) 을 S={{0}} 으로 오인 — 선지에 있음')
check(w_neg in ch and A_neg['mins'] == [0], f'오답 {w_neg}: c=-4 (극솟값 0이라 실제로는 (다) 불만족) — 선지에 있음')
# ③ 에서 (다)를 만족시키는 c 가 실제로 존재 (오답 경로가 성립)
c3 = sp.solve(sp.Rational(27, 256) * cp**4 - 81, cp)
A3 = analyze(pieces_g(x**3, sp.Integer(5)))
check(len(c3) == 1 and sp.simplify(A3['mins'][0] + sp.Rational(27, 256) * 5**4) == 0,
      f'③ 극솟값 -27c^4/256=-81 인 c={c3} 존재 (오답 경로)')

# ---------------------------------------------------------------------
# 6. 원문 M33 직접 풀이: f=x^4+ax^3+b, g=f (x<c), 8-f (x≥c), |S|=2, 합 25/3 → f(2)=29/3 (⑤)
# ---------------------------------------------------------------------
print('--- 원문 M33')
a_, b_ = sp.symbols('a_ b_', real=True)
F = x**4 + a_ * x**3 + b_
sols = sp.solve([F.subs(x, cp) - 4, sp.diff(F, x).subs(x, cp), b_ + 4 - sp.Rational(25, 3)], [a_, b_, cp], dict=True)
sols = [s for s in sols if s[cp].is_positive]
check(len(sols) == 1, f'원문 연립 해 {sols}')
s0 = sols[0]
Fo = F.subs(s0)
co = s0[cp]
Ao = analyze([(Fo, -sp.oo, co), (8 - Fo, co, sp.oo)])
check(sorted(Ao['S']) == sorted([sp.Rational(13, 3), 4]) and Ao['corners'] == [], f'원문 S={Ao["S"]} (원소 2개, 합 {sum(Ao["S"])})')
fo2 = Fo.subs(x, 2)
check(fo2 == sp.Rational(29, 3), f'원문 f(2)={fo2} = ⑤ 29/3')
# 원문에서 f'(c)≠0 이면 S=∅ 인 예
Ao2 = analyze([(x**4 - x**3 + 4, -sp.oo, 1), (8 - (x**4 - x**3 + 4), 1, sp.oo)])
check(Ao2['corners'] == [1] and Ao2['S'] == [], "원문: f'(c)≠0 이면 꺾여 S=∅")

# ---------------------------------------------------------------------
# 7. 조건 제거 검사(ABLATION): 조건을 하나씩 지우고 답이 그대로인지 / 바뀌는지 / 정해지지 않는지
#    군더더기는 FAIL 로 처리하지 않고 보고만 한다(아래 근거 확인만 check 로 건다).
#    동차성(1절): f 의 근을 λ배 하면 g 는 λ^4 배로 닮아 S 의 원소 개수, 실근 개수는 그대로, 극솟값은 λ^4 배, f(0) 은 λ^3 배
# ---------------------------------------------------------------------
print('--- 조건 제거 검사 ---')


def ablation(no, cname, vals, ans, why='', est=False, undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = []
        for v in sorted(vals, key=lambda v: float(N(v))):
            if all(abs(N(v - u)) > 1e-30 for u in sv):
                sv.append(v)
        show = lambda v: str(v) if v.is_Rational else f'≈{float(N(v)):.3f}(무리수)'
        if len(sv) == 1 and abs(N(sv[0] - ans)) < 1e-30:
            msg = f'성립 조건(답 그대로 {ans}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(show, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {show(sv[0])}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


def scaled_f0(f1, c1, need):
    """c=c1 정규형 f1 에 대해 need 조건을 확인하고, 극솟값이 -81 이 되도록 λ 배 했을 때의 f(0)"""
    ga, na, da, A = conds(f1, c1)
    flags = dict(ga=ga, na=na)
    assert all(flags[k_] for k_ in need), (f1, c1, flags)
    assert len(A['mins']) == 1 and N(A['mins'][0]) < 0, A['mins']
    lam = (81 / (-A['mins'][0]))**sp.Rational(1, 4)
    return sp.nsimplify(lam**3 * f1.subs(x, 0)), flags, A


# (가) 제거: ② f=(x-c)^2(x+2c), ③ f=x^3 도 (나)(다) 를 만족
v_ga = [ANS]
v2_, fl2, A2_ = scaled_f0(sp.expand((x - 1)**2 * (x + 2)), sp.Integer(1), ['na'])
v3_, fl3, A3_ = scaled_f0(x**3, sp.Integer(1), ['na'])
check(not fl2['ga'] and not fl3['ga'], f'(가) 제거 근거: ② 극솟값 {A2_["mins"]}, ③ 극솟값 {A3_["mins"]} (c=1), 둘 다 S=∅')
v_ga += [v2_, v3_]
ablation(18, '(가) |S|=1', v_ga, ANS, why='② f=(x-c)^2(x+2c), ③ f=x^3 도 (나)(다)를 만족')

# (나) 제거: ⑤ f=(x-c)(x^2+cx+r) (허근 2개, 실근 c 하나), c^2/4<r<17c^2/32 이면 S={0}, 극솟값 1개
v_na = [ANS]
for r0 in (sp.Rational(3, 10), sp.Rational(2, 5)):
    f5 = sp.expand((x - 1) * (x**2 + x + r0))
    assert sp.Poly(f5, x).coeff_monomial(x**2) == 0
    v5, fl5, A5 = scaled_f0(f5, sp.Integer(1), ['ga'])
    check(fl5['ga'] and not fl5['na'] and A5['S'] == [0],
          f'(나) 제거 근거: f=(x-1)(x^2+x+{r0}), c=1 → S={A5["S"]}, g=0 실근 {roots_g0(f5, 1)}개, 극솟값 {[float(N(m)) for m in A5["mins"]]}')
    v_na.append(v5)
ablation(18, '(나) g(x)=0의 실근 2개', v_na, ANS, why='⑤ f=(x-c)(x^2+cx+r) (실근 c 하나)도 (가)(다)를 만족')

# (다) 제거: ① c>0 이면 모두 (가)(나) 만족
v_da = []
for cc in (2, 4, 6):
    f1 = sp.expand((x - cc) * (x + sp.Rational(cc, 2))**2)
    ga, na, da, A = conds(f1, sp.Integer(cc))
    if ga and na:
        v_da.append(f1.subs(x, 0))
ablation(18, '(다) 극솟값 -81', v_da, ANS, why='① c>0 이면 모두 (가)(나) 성립, f(0)=-c^3/4')

# x^2 의 계수 0 제거(f=x^3+px^2+ax+b): f=(x-c)(x-c+6)^2 는 평행이동이라 모두 (가)(나)(다) 만족
v_x2 = []
for cc in (4, 0, 1):
    fT = sp.expand((x - cc) * (x - cc + 6)**2)
    ga, na, da, A = conds(fT, sp.Integer(cc))
    if ga and na and da:
        v_x2.append(fT.subs(x, 0))
ablation(18, "f의 꼴 x^3+ax+b의 'x^2의 계수 0'", v_x2, ANS, why='예: f=(x-c)(x-c+6)^2, c=4, 0, 1')

# 최고차항의 계수 1 제거: f=α(x-c)(x+c/2)^2, 극솟값 -81αc^4/256 → α=256/c^4
v_lc = []
for cc in (4, 2):
    al_ = sp.Rational(256, cc**4)
    fA = sp.expand(al_ * (x - cc) * (x + sp.Rational(cc, 2))**2)
    ga, na, da, A = conds(fA, sp.Integer(cc))
    if ga and na and da:
        v_lc.append(fA.subs(x, 0))
ablation(18, "f의 꼴 x^3+ax+b의 '최고차항의 계수 1'", v_lc, ANS, why='예: f=16(x-2)(x+1)^2, c=2')

print('ALL OK' if allok else 'SOME FAILED')
