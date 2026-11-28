# -*- coding: utf-8 -*-
# 13회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 2, 14: 4, 15: 1, 16: 3}          # 분담표 13②·14④·15①·16③
DBREF = {13: 'M29 v3_추가 1', 14: 'D9 v3_추가 1', 15: 'D69 후보_순위 3', 16: 'I76 후보_순위 3'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 계수 13●·14●·15○·16●
BOX = {13: False, 14: False, 15: False, 16: True}         # 원문대로(M29·D9·D69 상자 없음, I76 상자 있음)
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t, a, b, p = sp.symbols('x t a b p', real=True)
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
    return [choice_val(z) for z in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    cf = sorted(COEF & set(IT[no].get('ops') or []))
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and (cf or not NEED_COEF[no]),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {cf}) bunseok=False')
    check(no, ('cond' in IT[no]) == BOX[no] and 'bogi' not in IT[no], f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(분담표 상자 칸대로), 보기형 아님')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs', 'level'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')
    check(no, IT[no]['level'] == LEVEL[no], f'level {IT[no]["level"]} (목표 {LEVEL[no]})')
    body = IT[no]['body'] + ''.join(c for _, c in IT[no].get('cond', [])) + (IT[no].get('after') or '')
    check(no, '이러한' not in body and '이와 같은' not in body, "'이러한'·'이와 같은' 없음")
    nums = set(re.findall(r'(?<![\w.])\d+(?![\w.])', re.sub(r'<[^>]*>|style="[^"]*"|&[lg]t;', ' ', body)))
    check(no, str(abs(val)) not in nums, f'정답 {val}이 본문에 나온 수 {sorted(nums, key=int)}와 다름')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [choice_val(z) for z in IT[no]['wrongs']]
    vals = [sp.nsimplify(z) for z in vals]
    check(no, all(z in v and z != v[IT[no]['ans'] - 1] for z in vals) and sorted(w) == sorted(set(vals)) and len(set(vals)) >= 2,
          f'오답 {vals} 선지에 있음, wrongs {IT[no]["wrongs"]}와 같음 ({why})')


def ablation(no, cname, vals, ans, why='', undef=None):
    global ok
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = f'필요(남은 조건을 만족시키는 경우가 없음{"; " + why if why else ""})'
    else:
        sv = sorted(set(vals), key=lambda z: float(z))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:6]))}{" 등" if len(sv) > 6 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else sp.nsimplify(choice_val(c)) if re.fullmatch(r'-?\d+|-?\\dfrac.*', c) else c


def nroots(poly_expr, var):
    P = sp.Poly(sp.expand(poly_expr), var)
    if P.degree() <= 0:
        return None if P.is_zero else 0
    return len(set(P.real_roots()))


# ================= 13번 (M29: 점 (1,a)에서 y=px³−x에 그은 접선 수 f(a), 불연속 a의 합 3, f(a)=3인 정수 a의 개수) =================
def H13(pv, cx=1):
    """접점 t의 접선이 (cx, a)를 지날 조건 a = H(t)"""
    cur = pv * t**3 - t
    return sp.expand(sp.diff(cur, t) * (cx - t) + cur)


def tangent_count(pv, av, cx=1):
    """y=px³−x에 그은 서로 다른 접선의 개수(접선 기울기·절편이 같은 접점은 하나로)"""
    cur = pv * t**3 - t
    rts = sp.Poly(H13(pv, cx) - av, t).real_roots() if sp.Poly(H13(pv, cx) - av, t).degree() > 0 else ([] if H13(pv, cx) != av else None)
    if rts is None:
        return sp.oo
    lines = {(sp.nsimplify(sp.diff(cur, t).subs(t, r)), sp.nsimplify((cur - t * sp.diff(cur, t)).subs(t, r))) for r in set(rts)}
    return len(lines)


def disc_points(pv, cx=1):
    """f(a)가 불연속인 a: H의 극값(임계값)에서 개수가 바뀜. 후보 a마다 좌우 값과 비교해 확인"""
    Hh = H13(pv, cx)
    cands = set()
    dH = sp.diff(Hh, t)
    if sp.Poly(dH, t).degree() > 0:
        cands |= {Hh.subs(t, c) for c in sp.Poly(dH, t).real_roots()}
    elif dH == 0:
        cands |= {Hh}
    else:
        pass
    out = []
    for c in sorted(cands, key=float):
        e = R(1, 1000)
        vals = [tangent_count(pv, c - e, cx), tangent_count(pv, c, cx), tangent_count(pv, c + e, cx)]
        if len(set(vals)) > 1:
            out.append(c)
    return out


check(13, sp.expand(H13(p) - (-2 * p * t**3 + 3 * p * t**2 - 1)) == 0, f'접점 방정식 a = {sp.expand(H13(p))}')
# p 전수: 극값 −1, p−1 → 합 p−2 (p≠0), p=0이면 직선이라 불연속점 −1 하나
P13 = []
for pv in [R(k, 2) for k in range(-20, 21)]:
    if sum(disc_points(pv)) == 3:
        P13.append(pv)
check(13, P13 == [5], f'p∈[−10,10](간격 1/2) 전수: 불연속점 합이 3인 p = {P13} (합 = p−2, p=0이면 {disc_points(0)})')
check(13, disc_points(5) == [-1, 4], f'p=5: 불연속인 a = {disc_points(5)}')
cnt3 = [av for av in range(-20, 21) if tangent_count(5, av) == 3]
ans13 = len(cnt3)
check(13, cnt3 == [0, 1, 2, 3] and tangent_count(5, -1) == 2 and tangent_count(5, 4) == 2, f'f(a)=3인 정수 a {cnt3} (a=−1, 4에서는 2개)')
ans_ok(13, ans13)
w13a = len([av for av in range(-20, 21) if tangent_count(4, av) == 3])          # p−1=3으로 p=4
w13b = len([av for av in range(-1, 4)])                                            # 한쪽 끝 포함
w13c = len([av for av in range(-1, 5)])                                            # 양 끝 포함
wrong_in(13, [w13a, w13b, w13c], 'a=−1 빠뜨려 p=4 → 3 · 한쪽 끝 포함 5 · 양 끝 포함 6')
check(13, sum(disc_points(1)) == orig_ans('M29') == -1, f'원문 M29(y=x³−x) 불연속점 합 {sum(disc_points(1))} = 원문 답 {orig_ans("M29")}')
ablation(13, "'불연속점의 합이 3'", [len([av for av in range(-40, 41) if tangent_count(pv, av) == 3]) for pv in [2, 3, 5, 7]], ans13, '개수 = p−1 (p가 정수일 때)')

# ================= 14번 (D9: f=⅓x³+ax|x|−bx, (−∞,−2]↑ [−2,2]↓ [2,∞)↑, a+b의 최솟값) =================
def fp14(av, bv, z):
    return z**2 + 2 * av * abs(z) - bv


ZS = [R(k, 16) for k in range(-128, 129)]          # [−8, 8] 촘촘한 표본(유리수, 정확 비교)


def cond14(av, bv, dec=True, inc=True):
    """f′는 연속인 우함수이고 x≥0에서 아래로 볼록한 이차식 → 표본 + 볼록성으로 판정"""
    okd = all(fp14(av, bv, z) <= 0 for z in ZS if -2 <= z <= 2) if dec else True
    oki = all(fp14(av, bv, z) >= 0 for z in ZS if abs(z) >= 2) if inc else True
    if inc and av < -2:   # 꼭짓점 x=−a가 [2,∞) 안: 꼭짓점 값도 확인
        oki = oki and (-av**2 - bv >= 0)
    return okd and oki


check(14, all(sp.expand((R(1, 3) * z**3 + a * z * abs(z) - b * z).subs(z, -u) + (R(1, 3) * z**3 + a * z * abs(z) - b * z).subs(z, u)) == 0 for z in [x] for u in [1, 2, R(7, 3)]), 'f(−x)=−f(x)(기함수)')
A14 = sorted(set([R(k, 8) for k in range(-40, 41)] + [R(-17, 16), R(-15, 16), R(-33, 32)]))
B14 = lambda av: [4 * av + 4 + d for d in (-R(1, 8), 0, R(1, 8))]
good = [(av, bv) for av in A14 for bv in B14(av) if cond14(av, bv)]
check(14, all(bv == 4 * av + 4 for av, bv in good), '조건을 만족시키면 b=4a+4 (f′(2)=0; b를 ±1/8 옮기면 실패)')
check(14, sorted({av for av, _ in good}) == [av for av in A14 if av >= -1], f'a∈[−5,5] 전수: 조건을 만족시키는 a는 a≥−1 (최소 {min(av for av, _ in good)}), a=−17/16(b=−1/4)이면 x=1/16에서 f′={fp14(R(-17, 16), R(-1, 4), R(1, 16))}>0')
ans14 = min(av + bv for av, bv in good)
check(14, ans14 == -1 and cond14(-1, 0), f'a+b의 최솟값 {ans14} (a=−1, b=0: f′=|x|(|x|−2))')
ans_ok(14, ans14)
loose = [av for av in A14 if 4 + 2 * av > 0]      # x=2 좌우 부호만 본 범위
w14a = 5 * (-2) + 4
w14b = sp.solve([4 + 4 * a - b, 4 - 4 * a - b], [a, b])
check(14, min(loose) > -2, f"x=2의 좌우 부호만 보면 a>−2 (경계 −2에서 a+b={w14a})")
wrong_in(14, [w14a, w14b[a] + w14b[b]], '다른 근을 놓쳐 경계 a=−2 → −6 · 두 근 ±2로 a=0,b=4 → 4')
# 원문 D9: (−∞,−1] 감소, [−1,∞) 증가 → M−m = 9/2+3√2
def orig_ok(av):
    bv = 2 * av - 1
    zs = [R(k, 20) for k in range(-80, 81)]
    fpz = lambda z: (-z**2 - 2 * av * z - bv) if z < 0 else (z**2 + 2 * av * z - bv)
    return all(fpz(z) <= 1e-12 for z in zs if z < -1) and all(fpz(z) >= -1e-12 for z in zs if z > -1)
lo, hi = -1 - sp.sqrt(2), R(1, 2)
check(14, orig_ok(sp.N(lo + R(1, 1000))) and not orig_ok(sp.N(lo - R(1, 100))) and orig_ok(hi) and not orig_ok(hi + R(1, 100)),
      '원문 a의 범위 [−1−√2, 1/2] (표본)')
check(14, sp.simplify((3 * hi - 1) - (3 * lo - 1) - (R(9, 2) + 3 * sp.sqrt(2))) == 0 and F.I['D9'][2] == '③' and F.I['D9'][1][2] == r'\dfrac92+3\sqrt2',
      f'원문 M−m = {sp.simplify((3 * hi - 1) - (3 * lo - 1))} = 원문 답 ③')
g_nodec = [(av, bv) for av in [R(k, 2) for k in range(-6, 7)] for bv in [R(k, 1) for k in range(-60, 21)] if cond14(av, bv, dec=False)]
ablation(14, "'[−2,2]에서 감소'", [], ans14, undef=f'b를 얼마든지 작게 할 수 있어 최솟값 없음(표본 최소 a+b {min(av + bv for av, bv in g_nodec)})')
g_noinc = [(av, bv) for av in [R(k, 1) for k in range(-30, 3)] for bv in [R(k, 1) for k in range(0, 10)] if cond14(av, bv, inc=False)]
ablation(14, "'(−∞,−2]·[2,∞)에서 증가'", [], ans14, undef=f'a를 얼마든지 작게 할 수 있어 최솟값 없음(표본 최소 a+b {min(av + bv for av, bv in g_noinc)})')

# ================= 15번 (D69: f 최고차항 1 이차, g: [−2,1]에서 f, 밖에서 x, h=g(x+)·g((x+3)+) 연속, f(2)) =================
cs = sp.symbols('c0:2')
kq = sp.symbols('kq')


def Gright(fx, lo_, hi_):
    """lim_{t→0+} g(z+t): z<lo이면 z, lo≤z<hi이면 f(z), z≥hi이면 z"""
    return lambda zexpr, zval: zexpr if (zval < lo_ or zval >= hi_) else fx.subs(x, zexpr)


def hpieces(fx, lo_=-2, hi_=1, sh=3):
    G = Gright(fx, lo_, hi_)
    cuts = sorted({lo_ - sh, hi_ - sh, lo_, hi_})
    pts = [-sp.oo] + cuts + [sp.oo]
    pieces = []
    for i in range(len(pts) - 1):
        l_, r_ = pts[i], pts[i + 1]
        rep = r_ - R(1, 2) if l_ == -sp.oo else (l_ + R(1, 2) if r_ == sp.oo else (l_ + r_) / 2)
        pieces.append(((l_, r_), sp.expand(G(x, rep) * G(x + sh, rep + sh))))
    return pieces, cuts


def hval(fx, z, lo_=-2, hi_=1, sh=3):
    G = Gright(fx, lo_, hi_)
    return G(sp.Integer(z), z) * G(sp.Integer(z) + sh, z + sh)


def cont_eqs(fx, lo_=-2, hi_=1, sh=3):
    pc, cuts = hpieces(fx, lo_, hi_, sh)
    eqs = []
    for i, c in enumerate(cuts):
        L, Rr = pc[i][1], pc[i + 1][1]
        eqs += [sp.expand(L.subs(x, c) - hval(fx, c, lo_, hi_, sh)), sp.expand(Rr.subs(x, c) - hval(fx, c, lo_, hi_, sh))]
    return [e for e in eqs if e != 0]


f15 = x**2 + cs[1] * x + cs[0]
sol15 = sp.solve(cont_eqs(f15), cs, dict=True)
check(15, len(sol15) == 1, f'이음점 x=−5, −2, 1의 연속 조건(좌극한·우극한 = 함숫값)의 해 {sol15}')
fs15 = sp.expand(f15.subs(sol15[0]))
check(15, sp.factor(fs15 - x) == sp.factor((x + 2) * (x - 1)) and not cont_eqs(fs15), f'f(x) = {fs15} (f(x)−x = {sp.factor(fs15 - x)}), h는 세 이음점에서 연속')
# 연속의 직접 확인(수치 좌우)
e_ = R(1, 10**6)
G15 = Gright(fs15, -2, 1)
hnum = lambda z: G15(z, z) * G15(z + 3, z + 3)
check(15, all(abs(sp.N(hnum(sp.Integer(c)) - hnum(c - e_))) < 1e-4 and abs(sp.N(hnum(sp.Integer(c)) - hnum(c + e_))) < 1e-4 for c in [-5, -2, 1]), '수치 좌우 극한으로 연속 확인')
ans15 = fs15.subs(x, 2)
check(15, ans15 == 6, f'f(2) = {ans15}')
ans_ok(15, ans15)
fo1 = sp.expand((x**2 + cs[1] * x + cs[0]).subs(sp.solve(cont_eqs(x**2 + cs[1] * x + cs[0], -1, 1, 2), cs, dict=True)[0]))
w15a = fo1.subs(x, 2)                                   # 원문 구간 [−1,1]·이동량 2대로
w15b = sp.expand((x + 2) * (x - 1)).subs(x, 2)          # f−x에서 x를 빠뜨림
check(15, fo1 == sp.expand(x**2 + x - 1), f'원문 수치(구간 [−1,1], 이동량 2)로 풀면 f = {fo1}')
wrong_in(15, [w15a, w15b], '원문 수치대로 f=x²+x−1 → 5 · f=(x+2)(x−1) → 4')
# 원문 D69: g는 [−1,1]에서 f, 이동량 2, 보기 ㄱ h(1)=3 참, ㄴ 거짓(반례), ㄷ 거짓(반례) → ① ㄱ
def H_orig(fx):
    def G(zv):
        return zv if (zv < -1 or zv >= 1) else fx.subs(x, zv)
    return lambda zv: G(zv) * G(zv + 2)
gn = H_orig(x**2 + 5)
check(15, H_orig(x**2 + 5)(1) == 3 and H_orig(x**3)(1) == 3, 'ㄱ h(1)=1·3=3 (f와 무관) 참')
check(15, abs(sp.N(gn(-1 - e_) - gn(-1))) > R(1, 10), f'ㄴ 반례 f=x²+5: x=−1에서 좌극한 {sp.N(gn(-1 - e_), 6)} ≠ h(−1)={gn(-1)} → 거짓')
fd = -x - 3     # [−1,1]에서 감소, g(−1)=−2
hd = H_orig(fd)
vals_ = [hd(R(k, 1000)) for k in range(-4000, 3000)]
inf_ = 3 * fd.subs(x, 1)
check(15, min(vals_) > inf_ and all(hd(z) != inf_ for z in [R(k, 10) for k in range(-50, 40)]) and min(vals_) - inf_ < R(1, 100),
      f'ㄷ 반례 f=−x−3: h의 값은 3f(1)={inf_}에 가까워지나 도달하지 않음 → 최솟값 없음, 거짓')
check(15, orig_ans('D69') == 'T:ㄱ', f'원문 D69 답 {orig_ans("D69")} = ㄱ')
# 빼 보기
fk = kq * x**2 + cs[1] * x + cs[0]
alt = []
for kv in [1, 2, 3, -1]:
    s_ = sp.solve(cont_eqs(fk.subs(kq, kv)), cs, dict=True)
    alt.append(sp.expand(fk.subs(kq, kv).subs(s_[0])).subs(x, 2))
ablation(15, "'최고차항의 계수가 1'", alt, ans15, 'f(x)=x+k(x+2)(x−1)이면 f(2)=2+4k')
ablation(15, "'연속'", [], ans15, undef='h에 조건이 없으면 f의 두 계수가 정해지지 않음')
check(15, IT[15]['effect'] == '같음', "effect '같음'(원문 수준의 연속 조건)")

# ================= 16번 (I76: f 최고차항 음수, f(0)=0, g=∫(|f|−2|t|), (가) 근 4개 (나) 1, 5에서 극값, f(1)>0>f(5), g(1)<0, g′=0의 근의 합) =================
aa = sp.symbols('aa', real=True)


def cand16(K, P1, P2, lead_sign, use_ga=True):
    """f=xq, q(P1)=±K, q(P2)=±K. (가)는 접하거나 q(0)=±K인 이산 후보에서만 성립 → 이산 후보 전수"""
    out = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            sl = sp.solve([aa * P1**2 + b * P1 + p - K * s1, aa * P2**2 + b * P2 + p - K * s2], [b, p], dict=True)[0]
            q = aa * x**2 + sl[b] * x + sl[p]
            avs = set()
            for s in (1, -1):
                avs |= {r for r in sp.solve(sp.discriminant(sp.expand(q - K * s), x), aa) if r.is_real}
                avs |= {r for r in sp.solve(q.subs(x, 0) - K * s, aa) if r.is_real}
            if not use_ga:
                avs |= {R(lead_sign * k, 7) for k in range(1, 12)}
            for av in sorted(avs, key=float):
                if av == 0 or sp.sign(av) != lead_sign:
                    continue
                qq = sp.expand(q.subs(aa, av))
                f = sp.expand(x * qq)
                rts = {0}
                for s in (1, -1):
                    rts |= set(sp.Poly(qq - K * s, x).real_roots())
                rts = sorted(rts, key=float)
                if use_ga and len(rts) != 4:
                    continue
                gp = lambda z: abs(f.subs(x, z)) - K * abs(z)
                e = R(1, 10**6)
                ext = [r for r in rts if sp.sign(gp(r - e)) * sp.sign(gp(r + e)) < 0]
                if P1 not in ext or P2 not in ext:
                    continue
                g1 = sp.integrate(sp.Piecewise((f.subs(x, t), f.subs(x, t) >= 0), (-f.subs(x, t), True)) - K * t, (t, 0, P1)) if P1 > 0 else None
                # |f|의 적분: [0,P1]에서 f의 부호 구간으로 나눔
                brk = sorted({0, P1} | {r for r in sp.Poly(f, x).real_roots() if 0 < r < P1}, key=float)
                gP1 = sum(sp.integrate(abs(f.subs(x, (brk[i] + brk[i + 1]) / 2)) / f.subs(x, (brk[i] + brk[i + 1]) / 2) * f - K * x, (x, brk[i], brk[i + 1])) for i in range(len(brk) - 1))
                out.append(dict(f=sp.factor(f), roots=rts, ext=ext, fP2=f.subs(x, P2), gP1=sp.N(gP1, 6), s=sum(rts), prod=sp.sign(float(f.subs(x, P2)) * float(sp.N(gP1, 30)))))
    return out


C16 = cand16(2, 1, 5, -1)
for c_ in C16:
    ff = sp.expand(c_['f'])
    c_['f1'] = ff.subs(x, 1)
    print('   후보', c_['f'], '근', c_['roots'], '극값', c_['ext'], f"f(1)={c_['f1']}, f(5)={c_['fP2']}, g(1)={c_['gP1']}, 근의 합 {c_['s']}")
step1 = [c_ for c_ in C16 if c_['f1'] > 0 > c_['fP2']]
sel = [c_ for c_ in step1 if c_['gP1'] < 0]
check(16, len(step1) == 2 and len(sel) == 1, f'(가)(나)를 만족시키는 후보 {len(C16)}개 중 f(1)>0>f(5)는 {len(step1)}개(후보 둘), 그중 g(1)<0은 {len(sel)}개')
check(16, sp.expand(sel[0]['f'] - (x * (-x**2 + 5 * x - 2))) == 0 and sel[0]['roots'] == [0, 1, 4, 5] and sel[0]['ext'] == [0, 1, 4, 5], f"f = {sel[0]['f']}, g′=0의 근 {sel[0]['roots']}(모두 극값)")
ans16 = sel[0]['s']
ans_ok(16, ans16)
other = [c_ for c_ in step1 if c_ is not sel[0]][0]
wrong_in(16, [other['s'], 0 + 1 + 5], f"g(1) 부호를 안 본 후보(근 {other['roots']}) → 2 · 넷째 근 빠뜨림 0+1+5 → 6")
# 원문 I76: |t|, 양수, 2·6, f(6)g(2)<0 → f(8)=40
Co = cand16(1, 2, 6, 1)
so = [c_ for c_ in Co if c_['prod'] < 0]
check(16, len(so) == 1 and sp.expand(so[0]['f']).subs(x, 8) == orig_ans('I76') == 40, f"원문 I76: 후보 {len(Co)}개, f(6)g(2)<0은 {so[0]['f']}, f(8)={sp.expand(so[0]['f']).subs(x, 8)} = 원문 답")
# 빼 보기
ablation(16, "'g(1)<0'", [c_['s'] for c_ in step1], ans16)
ablation(16, "'f(1)>0>f(5)'", [c_['s'] for c_ in C16 if c_['gP1'] < 0], ans16, '다른 부호 조합의 후보')
ablation(16, '(가) 근 4개', [c_['s'] for c_ in cand16(2, 1, 5, -1, use_ga=False) if sp.expand(c_['f']).subs(x, 1) > 0 > c_['fP2'] and c_['gP1'] < 0], ans16, '이차항 계수가 연속적으로 움직임')
alt_pos = [c_['s'] for c_ in cand16(2, 1, 5, 1) if sp.expand(c_['f']).subs(x, 1) > 0 > c_['fP2'] and c_['gP1'] < 0]
ablation(16, "'최고차항의 계수가 음수'(→ 양수)", alt_pos, ans16, '양수이면 f(1)>0>f(5)인 후보가 없음')
alt_nb = []
for P1_, P2_ in [(1, 4), (1, 6), (2, 5)]:
    alt_nb += [c_['s'] for c_ in cand16(2, P1_, P2_, -1) if sp.expand(c_['f']).subs(x, 1) > 0 > sp.expand(c_['f']).subs(x, 5) and c_['gP1'] < 0]
alt_nb += [ans16]
ablation(16, '(나) 극값 위치 1, 5', alt_nb, ans16, '극값 위치를 (1,4), (1,6)으로 두어도 나머지 조건을 만족시키는 함수가 있음')
check(16, IT[16]['effect'] == '어려워짐', "effect '어려워짐'(회차 13–16 어려워짐 1–2 기준을 이 문항이 채움)")

print()
print('ALL OK' if ok else 'SOME FAIL')
