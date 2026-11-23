# -*- coding: utf-8 -*-
# 8회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 1, 14: 4, 15: 3, 16: 4}          # 분담표 목표 13④·14①·15③·16④ → 13·14 맞바꿈(note·보고에 적음)
DBREF = {13: 'M27 후보_순위 2', 14: 'M16 후보_순위 2', 15: 'J70 후보_순위 2', 16: 'M57 결합 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 '계수' ● / ○
BOX = {13: True, 14: False, 15: False, 16: True}        # 13·16 '원문대로'(원문에 상자 있음), 14·15 ×
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t = sp.symbols('x t', real=True)
R = sp.Rational
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def choice_val(s):
    s = re.sub(r'\s', '', s)
    m = re.fullmatch(r'(-?)\\dfrac\{?(\d+?)\}?\{?(\d+)\}?', s)
    if m:
        return sp.Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    return sp.Rational(s)


def ch(no):
    c = IT[no]['choices']
    return c if c[0].startswith('T:') else [choice_val(z) for z in c]


def ans_ok(no, val):
    v = ch(no)
    if not IT[no]['choices'][0].startswith('T:'):
        d = {v[i + 1] - v[i] for i in range(4)}
        check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
        check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    else:
        check(no, len(set(v)) == 5, f'보기 조합 선지 {v} 서로 다름')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    cf = sorted(COEF & set(IT[no].get('ops') or []))
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and (cf or not NEED_COEF[no]),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {cf}) bunseok=False')
    check(no, ('cond' in IT[no]) == BOX[no], f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(분담표 상자 칸대로)')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs', 'level'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')
    check(no, IT[no]['level'] == LEVEL[no], f'level {IT[no]["level"]} (목표 {LEVEL[no]})')
    body = IT[no]['body'] + ''.join(c for _, c in IT[no].get('cond', [])) + ''.join(c for _, c in IT[no].get('bogi', []))
    check(no, '이러한' not in body and '이와 같은' not in body, "'이러한'·'이와 같은' 없음")


def wrong_in(no, vals, why):
    v = ch(no)
    if IT[no]['choices'][0].startswith('T:'):
        w = list(IT[no]['wrongs'])
    else:
        w = [choice_val(z) for z in IT[no]['wrongs']]
        vals = [sp.nsimplify(z) for z in vals]
    check(no, all(z in v and z != v[IT[no]['ans'] - 1] for z in vals) and sorted(w, key=str) == sorted(set(vals), key=str) and len(set(vals)) >= 2,
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
    global ok
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else choice_val(c)


def n_distinct_real(poly):
    """다항식(x)의 서로 다른 실근 개수(정확)"""
    P = sp.Poly(sp.expand(poly), x)
    return len(set(P.real_roots()))


def count_abs_line(f, h):
    """|f(x)| = h (h>0)의 서로 다른 실근 개수"""
    return len(set(sp.Poly(sp.expand(f - h), x).real_roots()) | set(sp.Poly(sp.expand(f + h), x).real_roots()))


# ================= 13번 (M27: 최고차항 양수 미정, f(6)=54, |f|와 직선 y=f(6)이 네 점, f(−2)) =================
# (가) → f = a x³ + c x. a>0 격자 × c 격자 전수 + 일반식(2p=6)
cands = []
for an in [R(i, 8) for i in range(1, 41)]:            # a ∈ (0, 5]
    # f(6)=54 → 216a + 6c = 54 → c = 9 − 36a
    c = 9 - 36 * an
    f = an * x**3 + c * x
    if count_abs_line(f, f.subs(x, 6)) == 4:
        cands.append((an, c))
check(13, cands == [(1, -27)], f'a 격자(1/8 간격, 0<a≤5)·f(6)=54 → (나) 네 점이 되는 (a, c) = {cands}')
p_, a_ = sp.symbols('p a', positive=True)
fp = a_ * (x**3 - 3 * p_**2 * x)
check(13, sp.factor(fp - 2 * a_ * p_**3) == a_ * (x + p_)**2 * (x - 2 * p_), "f−(극댓값)=a(x+p)²(x−2p): 극댓값과 같은 높이의 점 x=−p, 2p")
sol13 = sp.solve([sp.Eq(2 * p_, 6), sp.Eq(2 * a_ * p_**3, 54)], [a_, p_], dict=True)
check(13, sol13 == [{a_: 1, p_: 3}], f'6=2p, 2ap³=54 → {sol13}')
f13 = x**3 - 27 * x
check(13, f13.subs(x, 6) == 54 and count_abs_line(f13, 54) == 4, 'f=x³−27x: f(6)=54, |f|=54의 실근 4개(±3, ±6)')
ans13 = f13.subs(x, -2)
ans_ok(13, ans13)
gA = R(1, 8) * (x**3 - 108 * x)               # x=6을 극소점(p=6)으로 보고 봉우리 높이 54
check(13, gA.subs(x, 6) == -54 and count_abs_line(gA, 54) == 4, '오답 경로 A: g=(x³−108x)/8 → |g|=54는 네 점이지만 g(6)=−54 ≠ 54')
wrong_in(13, [gA.subs(x, -2), orig_ans('M27')], 'x=6을 극소점으로 26 · 원문 답 36')
# 원문 M27: 2x³+cx, −f(1)이 봉우리 높이 → c=−6, f(3)=36
fo = 2 * x**3 + sp.Symbol('c') * x
co = [cv for cv in range(-30, 0) if count_abs_line(fo.subs('c', cv), -fo.subs({'c': cv, x: 1})) == 4 and -fo.subs({'c': cv, x: 1}) > 0]
check(13, co == [-6] and (2 * x**3 - 6 * x).subs(x, 3) == orig_ans('M27') == 36, f'원문 M27: c={co}, f(3)=36 = 원문 답')
# 빼 보기
fneg = -R(1, 8) * (x**3 - 108 * x)            # a<0: x=6이 극대점
check(13, fneg.subs(x, 6) == 54 and count_abs_line(fneg, 54) == 4, "a<0 경우 f=−(x³−108x)/8도 f(6)=54·(가)(나) 만족")
ablation(13, "'최고차항의 계수가 양수'", [ans13, fneg.subs(x, -2)], ans13, 'a<0이면 x=6이 극대점')
ablation(13, "'f(6)=54'", [(av * (x**3 - 27 * x)).subs(x, -2) for av in (1, 2, R(1, 2))], ans13, 'f=a(x³−27x)에서 a가 정해지지 않음')
ft = (x - 6) * (x - 1) * (x - 3) + 54          # 홀함수 아님, f(6)=54, |f|=54 네 점
check(13, count_abs_line(ft, 54) == 4 and ft.subs(x, 6) == 54, '(가) 반례 f=(x−6)(x−1)(x−3)+54: |f|와 y=54 네 점')
ablation(13, "(가) 'f(−x)=−f(x)'", [ans13, ft.subs(x, -2)], ans13, '홀함수가 아니면 다른 삼차함수도 가능')
fb = x**3 / 4                                   # 홀함수, f(6)=54, |f|와 y=54는 두 점
check(13, fb.subs(x, 6) == 54 and count_abs_line(fb, 54) == 2, '(나) 반례 f=x³/4')
ablation(13, "(나) '네 점'", [ans13, fb.subs(x, -2)], ans13, '(나)가 없으면 f=x³/4 등도 가능')


# ================= 14번 (M16: 두 함수 f−g = x²(x²−4x+2−k), x≤1, k의 최댓값) =================
k = sp.symbols('k', real=True)
f14 = x**4 - x**3 + 2 * x**2
g14 = 3 * x**3 + k * x**2
h14 = sp.expand(f14 - g14)
check(14, sp.expand(h14 - x**2 * (x**2 - 4 * x + 2 - k)) == 0, f'f−g={sp.factor(h14)} = x²(x²−4x+2−k)')


def holds14(kv, lo=-40, hi=1, step=R(1, 16)):
    """x≤1에서 f−g≥0: 정확 판정(구간 [lo,1]의 극값 후보 + 격자) — x→−∞에서는 x⁴가 이겨 양수"""
    hk = h14.subs(k, kv)
    pts = [r for r in sp.Poly(sp.diff(hk, x), x).real_roots() if r <= 1] + [R(1)]
    pts += [lo + i * step for i in range(int((hi - lo) / step) + 1)]
    return all(hk.subs(x, pv) >= 0 for pv in pts)


kg = [R(i, 4) for i in range(-24, 13)]
okk = [kv for kv in kg if holds14(kv)]
check(14, okk == [kv for kv in kg if kv <= -1], f'k 격자(−6~3, 1/4 간격) 전수: 성립 ⇔ k≤−1 (최대 {max(okk)})')
check(14, sp.factor(h14.subs(k, -1)) == x**2 * (x - 3) * (x - 1), 'k=−1: f−g=x²(x−1)(x−3) ≥ 0 (x≤1), x=1에서 등호')
ans14 = max(okk)
ans_ok(14, ans14)
q = x**2 - 4 * x + 2
w_all = sp.minimum(q, x)                                        # 범위 무시
w_sign = sp.minimum(x**2 + 2 * x + 2, x, sp.Interval(-sp.oo, 1))  # x³ 계수 부호 실수
check(14, w_all == -2 and w_sign == 1, f'오답 경로: 범위 무시 최솟값 {w_all}, x³ 계수 부호 실수 최솟값 {w_sign}')
wrong_in(14, [w_sign, w_all], '부호 실수 1 · 범위 무시 −2')
# 원문 M16: g=−f+k, f≥g ⇔ 2f≥k → k≤2·min f = −8
fo16 = x**4 - 3 * x**3 + x**2
check(14, 2 * sp.minimum(fo16, x) == orig_ans('M16') == -8, f'원문 M16: 2·min f = {2 * sp.minimum(fo16, x)} = 원문 답')
# 빼 보기
ablation(14, "범위 'x≤1'(→ 모든 실수 x)", [w_all], ans14, '최솟값이 꼭짓점 x=2에서 −2')
print("      (참고: k를 상수항 자리로 되돌리면 x⁴−4x³+2x²의 x≤1에서의 최솟값도 −1이라 값은 같지만, 이 문항은 x²을 인수로 묶는 풀이가 핵심)")


# ================= 15번 (J70: x=t(t−4)(at+b), ∫₀⁴|v|=8, 보기) =================
a, b = sp.symbols('a b', real=True)
X = t * (t - 4) * (a * t + b)


def dist(av, bv, T=4):
    xt = X.subs({a: av, b: bv})
    vt = sp.diff(xt, t)
    rs = sorted(set([r for r in sp.Poly(vt, t).real_roots() if 0 < r < T]))
    pts = [0] + rs + [T]
    return sum(abs(xt.subs(t, pts[i + 1]) - xt.subs(t, pts[i])) for i in range(len(pts) - 1)), xt


def maxabs(xt, T=4):
    vt = sp.diff(xt, t)
    rs = [r for r in sp.Poly(vt, t).real_roots() if 0 <= r <= T] if sp.degree(vt, t) > 0 else []
    return max([abs(xt.subs(t, r)) for r in rs] + [0])


def scaled(av, bv):
    """(a, b)를 같은 비율로 늘여 거리 8로 맞췄을 때의 max|x|와 가운데 영점 여부 (거리·max|x|는 (a, b)에 1차 비례)"""
    d, xt = dist(av, bv)
    M = maxabs(xt)
    interior = any(0 < r < 4 for r in sp.Poly(xt, t).real_roots()) if sp.degree(xt, t) > 0 else False
    return sp.nsimplify(sp.simplify(8 * M / d)), interior, 8 / d, xt


samples = [(1, -cn) for cn in [R(i, 4) for i in range(-12, 29) if i != 0]]   # 셋째 영점 c=−b/a (a=1로 두고 정규화)
samples += [(1, 0), (-1, 0), (0, 1), (0, -1)]                                 # c=0, a=0(이차)도 허용(단서 a≠0을 뺌)
T1 = T2 = T3 = True
ex2 = None
for av, bv in samples:
    M8, interior, sc, xt = scaled(av, bv)
    if xt.subs(t, 2) == 0:                                      # ㄱ: x(2)=0 → |x|≤2
        T1 &= M8 == 2
        ex2 = (av * sc, bv * sc)
    if M8 != 4: T2 = False                                      # ㄴ: |x|=4인 t가 늘 있는가
    if sp.N(M8, 30) < 4: T3 &= interior                         # ㄷ
check(15, ex2 is not None and T1, f'ㄱ 참: x(2)=0(b=−2a)이고 거리 8이면 max|x|=2 (예 a, b = {tuple(sp.nsimplify(sp.simplify(z)) for z in ex2)})')
check(15, ex2 is not None and sp.simplify(ex2[0] - 3 * sp.sqrt(3) / 8) == 0, 'ㄴ 반례: a=3√3/8, b=−3√3/4 → 거리 8, max|x|=2')
check(15, not T2, 'ㄴ 거짓(위 반례)')
check(15, T3, f'ㄷ 참: c=−b/a 격자·a=0 {len(samples)}개 전수 — max|x|<4이면 (0,4)에 영점')
cs = sp.symbols('c', real=True)
xc = t * (t - 4) * (t - cs)                                     # 가운데 영점이 없으면(c∉(0,4)) 방향 전환 1번 → 거리 2max|x|
check(15, all(len([r for r in sp.Poly(sp.diff(xc.subs(cs, cv), t), t).real_roots() if 0 < r < 4]) == 1 for cv in (-3, -1, 0, 4, 5, 9)),
      'c∉(0,4)이면 (0,4)에서 v=0인 t가 하나(방향 전환 한 번)')
ans15 = 'T:' + ', '.join(n for n, v in zip('ㄱㄴㄷ', (T1, T2, T3)) if v)
ans_ok(15, ans15)
wrong_in(15, ['T:ㄱ, ㄴ, ㄷ', 'T:ㄴ, ㄷ'], 'ㄴ을 참으로 ⑤ · ㄱ 거짓·ㄴ 참으로 ④')
# 원문 J70: [0,1], 거리 2 → ㄱ ∫₀¹v=0 참, ㄴ |x|>1 존재 거짓, ㄷ 참 → ③ ㄱ, ㄷ
o2 = o3 = True
for cn in [R(i, 8) for i in range(-16, 25) if i != 0]:
    xt = t * (t - 1) * (t - cn)
    vt = sp.diff(xt, t)
    rs = sorted(set([r for r in sp.Poly(vt, t).real_roots() if 0 < r < 1]))
    pts = [0] + rs + [1]
    d = sum(abs(xt.subs(t, pts[i + 1]) - xt.subs(t, pts[i])) for i in range(len(pts) - 1))
    M = sp.N(2 * maxabs(xt, 1) / d, 30)
    if M > 1 + 1e-20: o2 = False
    if M < 1 - 1e-20: o3 &= 0 < cn < 1
check(15, o2 and o3 and orig_ans('J70') == 'T:ㄱ, ㄷ', f'원문 J70: ㄴ(|x|>1 존재) 거짓(모든 경우 max|x|≤1), ㄷ 참 → 원문 답 {orig_ans("J70")}')
# 빼 보기
ablation(15, "'∫₀⁴|v|=8'", None, ans15, undef='거리가 정해지지 않으면 ㄱ(|x|≤2)·ㄷ(|x|<4 → 가운데 영점)이 모두 거짓(예: a=1, b=0이면 max|x|=256/27>4, a=1/100, b=0이면 |x|<4인데 가운데 영점 없음) → 옳은 것 없음')
xs = (t * (t - 4) * t) / 100
check(15, maxabs(sp.expand(xs)) < 4 and not any(0 < r < 4 for r in sp.Poly(xs, t).real_roots()), '거리 조건 없이 ㄷ 반례 x=t²(t−4)/100')
print("ABLATION 15 원문 단서 '(a≠0)': 뺐음(이 변형에서 일하지 않음 — a=0이면 ㄱ의 가정에서 x≡0이라 거리 8에 어긋나고 ㄷ의 가정 max|x|<4가 성립하지 않아 답 그대로; note에 기록)")


# ================= 16번 (M57: (나) f(x−2f(x))=0 세 근 + 점 (1,0)에서 그은 접선의 접점 x=3, f(−1)) =================
A_, al, be = sp.symbols('A alpha beta', real=True)


def count_nested(f, kk=2):
    return n_distinct_real(f.subs(x, x - kk * f))


def tangents_from(f, x0, y0=0):
    """점 (x0, y0)에서 곡선 y=f(x)에 그은 접선들의 접점 x좌표(실수)와 기울기"""
    s = sp.symbols('s', real=True)
    fpp = sp.diff(f, x)
    eq = sp.expand(f - (fpp * (x - x0) + y0))   # 접점 x에서의 접선이 (x0, y0)를 지남
    return sorted(set((r, fpp.subs(x, r)) for r in sp.Poly(eq, x).real_roots()))


f16 = -R(1, 8) * (x - 1)**2 * (x - 5)
check(16, n_distinct_real(f16) == 2 and count_nested(f16) == 3, f'f=−(x−1)²(x−5)/8: (가) 실근 2개, (나) f(x−2f(x))=0의 서로 다른 실근 {count_nested(f16)}개')
tg = tangents_from(f16, 1)
check(16, [(r, s) for r, s in tg if s != 0] == [(3, R(1, 2))] and any(s == 0 for r, s in tg), f'점 (1,0)에서 그은 접선: {tg} → x축이 아닌 것은 x=3에서 접함(기울기 1/2)')
# 유일성: (가) → A(x−α)²(x−β). 점 (1,0)이 곡선 위 → α=1 또는 β=1. 각각 β(또는 α)와 A를 격자 전수
found = []
for case in ('alpha', 'beta'):
    for other in [R(i, 2) for i in range(-20, 31) if i != 2]:
        for Av in [R(s * n, d) for s in (1, -1) for n in (1, 2, 3, 4) for d in (1, 2, 4, 8, 16, 32)]:
            fc = Av * (x - 1)**2 * (x - other) if case == 'alpha' else Av * (x - other)**2 * (x - 1)
            tg = tangents_from(fc, 1)
            if [r for r, s in tg if s != 0] != [3]: continue
            if count_nested(fc) == 3: found.append((case, other, Av))
found = sorted(set(found))
check(16, found == [('alpha', 5, -R(1, 8))], f'α·β 위치 × 다른 근(−10~15, 1/2 간격) × A(±1/32~±4) 전수 → {found}')
# (나)의 일반식: A<0이고 A(β−α)²=−2일 때만 3개 (A 부호·크기 격자)
gen = [(Av, count_nested(Av * (x - 1)**2 * (x - 5))) for Av in [R(i, 32) for i in range(-12, 13) if i != 0]]
check(16, [Av for Av, n in gen if n == 3] == [-R(1, 8)], f'α=1, β=5에서 A 격자 → (나) 3개인 A = {[Av for Av, n in gen if n == 3]} (A>0이면 {sorted(set(n for Av, n in gen if Av > 0))}개)')
ans16 = f16.subs(x, -1)
ans_ok(16, ans16)
w1 = (-R(1, 4) * (x - 1)**2 * (x - 5))       # 원문 방식(기울기 1): A(β−α)²=−4
w2 = (R(1, 8) * (x - 1)**2 * (x - 5))        # 기울기 −1/2로 착각: A(β−α)²=2
check(16, count_nested(w1, 1) == 3 and [r for r, s in tangents_from(w1, 1) if s != 0] == [3], '오답 경로 1: f(x−f(x))=0이면 A=−1/4 (원문 방식)')
wrong_in(16, [w1.subs(x, -1), w2.subs(x, -1)], '기울기 1(원문 방식) 6 · 기울기 −1/2 부호 실수 −3')
# 원문 M57: f(1)=4, f'(1)=1, f'(0)>1 → f=−(x+3)²(x−5)/16, f(0)=45/16 → 61
fo57 = -R(1, 16) * (x + 3)**2 * (x - 5)
check(16, fo57.subs(x, 1) == 4 and sp.diff(fo57, x).subs(x, 1) == 1 and sp.diff(fo57, x).subs(x, 0) > 1 and count_nested(fo57, 1) == 3
      and sp.fraction(fo57.subs(x, 0))[0] + sp.fraction(fo57.subs(x, 0))[1] == orig_ans('M57') == 61, f'원문 M57: f(0)={fo57.subs(x, 0)} → 61 = 원문 답')
# 빼 보기
fg = (x - 1) * ((x - 3)**2 + R(1, 4))         # 실근 1개(가 위반), (1,0)에서 x=3에 접하는 접선(기울기 1/4), (나) 3개
check(16, n_distinct_real(fg) == 1 and count_nested(fg) == 3 and (3, R(1, 4)) in tangents_from(fg, 1), '(가) 반례 f=(x−1)((x−3)²+1/4): (나) 3개, (1,0)에서 그은 접선이 x=3에서 접함')
fg2 = (x - 1) * ((x - 3)**2 + R(1, 8))        # 기울기 1/8
check(16, n_distinct_real(fg2) == 1 and count_nested(fg2) == 3 and (3, R(1, 8)) in tangents_from(fg2, 1), '(가) 반례 2 f=(x−1)((x−3)²+1/8)')
ablation(16, "(가) '실근 2개'", [ans16, fg.subs(x, -1), fg2.subs(x, -1)], ans16, '실근이 하나인 삼차함수도 (나)와 접선 조건을 만족')
ablation(16, "(나) 'f(x−2f(x))=0의 실근 3개'", [(Av * (x - 1)**2 * (x - 5)).subs(x, -1) for Av in (-R(1, 8), -1, -R(1, 4))], ans16, 'A가 정해지지 않음(접선 조건은 모든 A에서 성립)')
ablation(16, "'점 (1,0)에서 그은 접선의 접점 x좌표 3'", [(R(-2, (bv - av)**2) * (x - av)**2 * (x - bv)).subs(x, -1) for av, bv in ((1, 5), (1, 7), (-1, 3))], ans16, 'α, β가 정해지지 않음')
ablation(16, "(나)의 계수 2(→ 원문 f(x−f(x)))", [w1.subs(x, -1)], ans16, '기울기 1인 평행선이 되어 A=−1/4')

print('ALL OK' if ok else 'SOME FAIL')
