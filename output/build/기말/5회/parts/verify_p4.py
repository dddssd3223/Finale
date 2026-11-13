# -*- coding: utf-8 -*-
# 5회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 2, 14: 2, 15: 4, 16: 5}          # 분담표 목표 13③·14②·15④·16⑤ — 13번은 선지 배치로 ②(보고에 적음)
DBREF = {13: 'D46 결합 1', 14: 'D32 예상밖 1', 15: 'J57 후보_순위 3', 16: 'M64 결합 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 '계수' ●(반드시) / ○
BOX = {13: True, 14: False, 15: False, 16: True}        # 분담표 '상자': 원문대로(13·16) / ×(14·15)
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
    return [choice_val(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    cf = sorted(COEF & set(IT[no].get('ops') or []))
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and (cf or not NEED_COEF[no]),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {cf}) bunseok=False')
    check(no, ('cond' in IT[no]) == BOX[no], f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(분담표 상자 칸대로)')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs', 'level'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')
    check(no, IT[no]['level'] == ('상' if no == 16 else '중상'), f'level {IT[no]["level"]} (목표 {"상" if no == 16 else "중상"})')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [choice_val(z) for z in IT[no]['wrongs']]
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
    global ok
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    return o[1]['①②③④⑤'.index(o[2])]


def crit_types(poly):
    """다항식의 극점: [(x0, '극대'|'극소', 값)] (도함수 부호 변화로 판정)"""
    dp = sp.Poly(sp.diff(poly, x), x)
    out = []
    for r_ in sorted(set(sp.real_roots(dp)), key=lambda z: float(z)):
        e = R(1, 10**6)
        l_, r2 = sp.sign(dp.eval(r_ - e)), sp.sign(dp.eval(r_ + e))
        if l_ > 0 > r2: out.append((r_, '극대', sp.nsimplify(poly.subs(x, r_))))
        if l_ < 0 < r2: out.append((r_, '극소', sp.nsimplify(poly.subs(x, r_))))
    return out


# ================= 13번 (D46 결합 1: g=(x^2-2x)f, 두 접선과 y축으로 둘러싸인 넓이) =================
def touch_count(g):
    rs = set(sp.roots(sp.Poly(g, x)).keys())
    rs = {r_ for r_ in rs if r_.is_real}
    return len(rs), sum(1 for r_ in rs if sp.diff(g, x).subs(x, r_) == 0)


def area13(f, g, a0=-1):
    m_ = sp.expand(sp.diff(f, x).subs(x, a0) * (x - a0) + f.subs(x, a0))
    n_ = sp.expand(sp.diff(g, x).subs(x, a0) * (x - a0) + g.subs(x, a0))
    xi = sp.solve(sp.Eq(m_, n_), x)
    if not xi: return None
    return sp.nsimplify(abs((m_.subs(x, 0) - n_.subs(x, 0)) * xi[0]) / 2)


def cond13(f, k_sym_free=False):
    g = sp.expand((x**2 - 2 * x) * f)
    nz, nt = touch_count(g)
    mins = [v for _, ty, v in crit_types(g) if ty == '극소']
    return g, nz, nt, mins


k = sp.symbols('k', nonzero=True)
# (가)(나): f=kx(x+p) — 영점 개수와 접점 개수를 p 전수(1/2 격자 -6..6, k=1·-1)로
ps = [R(i, 2) for i in range(-12, 13)]
ok_p = sorted({p for p in ps for kv in (1, -1) if touch_count(sp.expand(kv * (x**2 - 2 * x) * x * (x + p))) == (2, 1)})
ok_pa = sorted({p for p in ps if touch_count(sp.expand((x**2 - 2 * x) * x * (x + p)))[0] == 2})
check(13, ok_pa == [-2, 0] and ok_p == [0], f'(가)만: p∈{ok_pa}, (가)(나): p∈{ok_p} (삼중근 x=0은 x축에 접함, x^2(x-2)^2은 접점 2개)')
# (다): p=0, k 부호
gk = sp.expand(k * x**3 * (x - 2))
mins_pos = [v for _, ty, v in crit_types(gk.subs(k, 1)) if ty == '극소']
mins_neg = [v for _, ty, v in crit_types(gk.subs(k, -1)) if ty == '극소']
check(13, mins_pos == [-R(27, 16)] and mins_neg == [], f'k>0이면 극솟값 -27k/16 하나({mins_pos}), k<0이면 극솟값 없음({mins_neg})')
k13 = sp.solve(sp.Eq(-R(27, 16) * k, -R(9, 2)), k)
check(13, k13 == [R(8, 3)], f'-27k/16=-9/2 → k={k13}')
f13 = R(8, 3) * x**2; g13 = sp.expand((x**2 - 2 * x) * f13)
_, nz, nt, mins = cond13(f13)
check(13, (nz, nt) == (2, 1) and mins == [-R(9, 2)], f'f=8x^2/3: 영점 {nz}개, 접점 {nt}개, 극솟값 {mins}')
m13 = sp.expand(sp.diff(f13, x).subs(x, -1) * (x + 1) + f13.subs(x, -1)); n13 = sp.expand(sp.diff(g13, x).subs(x, -1) * (x + 1) + g13.subs(x, -1))
check(13, m13 == -R(16, 3) * x - R(8, 3) and n13 == -R(80, 3) * x - R(56, 3) and sp.solve(m13 - n13, x) == [-R(3, 4)], f'm: y={m13}, n: y={n13}, 교점 x=-3/4')
ans13 = area13(f13, g13)
check(13, ans13 == 6, f'넓이 1/2*16*3/4 = {ans13}')
# 전수: 상자 조건을 만족시키는 (p, k)는 p=0, k=8/3뿐 — p는 (가)에서 0, -2, k 부호 둘
cands = []
for p in (0, -2):
    for sg in (1, -1):
        gg = sp.expand(sg * (x**2 - 2 * x) * x * (x + p))
        mn = [v for _, ty, v in crit_types(gg) if ty == '극소']
        if touch_count(gg) == (2, 1) and len(set(mn)) == 1:
            kv = -R(9, 2) / mn[0] if mn[0] != 0 else None
            if kv is not None and kv > 0: cands.append((p, sg * kv))
check(13, cands == [(0, R(8, 3))], f'(가)(나)(다)를 만족시키는 (p, k) 전수: {cands}')
ans_ok(13, ans13)
w_h1 = R(1, 2) * 16 * 1; w_nohalf = 16 * R(3, 4)
check(13, (w_h1, w_nohalf) == (8, 12), f'오답: 높이를 접점 x좌표 -1로 {w_h1}, 1/2 빠뜨림 {w_nohalf}')
wrong_in(13, [w_h1, w_nohalf], '높이 1 / 1/2 빠뜨림')
o13 = [v for _, ty, v in crit_types(sp.expand(x**3 * (x - 2))) if ty == '극소']
check('D46', o13 == [-R(27, 16)] and orig_ans('D46') == r'-\dfrac{27}{16}', f'D46 원문: g=x^3(x-2), 극솟값 {o13} = 원문 정답 {orig_ans("D46")}')
print('--- 13번 조건 빼 보기 ---')
# (가) 없이: p=-1, k<0이면 g=kx^2(x-2)(x-1), 접점은 x=0 하나, 극소는 하나(가운데 극점)
g_m1 = sp.expand(-(x**2 - 2 * x) * x * (x - 1))
mn_m1 = [v for _, ty, v in crit_types(g_m1) if ty == '극소']
k_alt = -R(9, 2) / mn_m1[0] * (-1)
f_alt = sp.expand(k_alt * x * (x - 1)); g_alt = sp.expand((x**2 - 2 * x) * f_alt)
_, nz_a, nt_a, mn_a = cond13(f_alt)
alt_area = area13(f_alt, g_alt)
check(13, nt_a == 1 and len(mn_a) == 1 and sp.simplify(mn_a[0] + R(9, 2)) == 0 and k_alt < 0, f'(가) 없이: p=-1, k={sp.nsimplify(k_alt)}도 (나)(다)를 만족(영점 {nz_a}개)')
ablation(13, '(가) 집합의 원소의 개수', [ans13, sp.nsimplify(alt_area)], ans13, f'p=-1이면 넓이 {float(alt_area):.4f}')
# (나) 없이: p=-2, k=-9/2 (g=kx^2(x-2)^2, 극소 x=1에서 k)
f_b = -R(9, 2) * x * (x - 2); g_b = sp.expand((x**2 - 2 * x) * f_b)
_, nz_b, nt_b, mn_b = cond13(f_b)
check(13, nz_b == 2 and mn_b == [-R(9, 2)] and nt_b == 2, f'(나) 없이: p=-2, k=-9/2도 (가)(다) 만족(접점 {nt_b}개), 넓이 {area13(f_b, g_b)}')
ablation(13, '(나) x축에 접하는 점의 개수', [ans13, area13(f_b, g_b)], ans13)
ablation(13, '(다) 극솟값 -9/2', [area13(kv * x**2, sp.expand((x**2 - 2 * x) * kv * x**2)) for kv in (1, 2, R(8, 3))], ans13, '넓이 9k/4')
f_c = R(8, 3) * (x - 2)**2; g_c = sp.expand((x**2 - 2 * x) * f_c)
_, nz_c, nt_c, mn_c = cond13(f_c)
check(13, (nz_c, nt_c) == (2, 1) and mn_c == [-R(9, 2)], f'f(0)=0 없이: f=8(x-2)^2/3도 (가)(나)(다) 만족, 넓이 {area13(f_c, g_c)}')
ablation(13, 'f(0)=0', [ans13, area13(f_c, g_c)], ans13)

# ================= 14번 (D32 예상밖 1: g(t)=∫_t^{t+1} f, f=x^2-a|x| 우함수, t=3/2에서 극소 → 극댓값-극솟값) =================
a = sp.symbols('a', positive=True)


def F14(u, av):
    """f의 한 부정적분(연속): x<0이면 x^3/3+a x^2/2, x>=0이면 x^3/3-a x^2/2"""
    return u**3 / 3 + av * u**2 / 2 if u < 0 else u**3 / 3 - av * u**2 / 2


def f14(u, av):
    return u * (u + av) if u < 0 else u * (u - av)


def g14(tv, av):
    return F14(tv + 1, av) - F14(tv, av)


def gp14(tv, av):
    return f14(tv + 1, av) - f14(tv, av)


def extrema14(av, N=64):
    """g'(t)의 부호 변화(1/N 격자 + 정확한 근)로 극대·극소: 반환 [(t, 종류, 값)]"""
    av = sp.nsimplify(av)
    cand = set()
    tt = sp.symbols('tt', real=True)
    for e, lo, hi in [(2 * tt + 1 - av, 0, 50), (2 * tt + 1 + av, -50, -1), ((1 - av) * (2 * tt + 1), -1, 0)]:
        for s_ in sp.solve(e, tt):
            if lo <= s_ <= hi: cand.add(sp.nsimplify(s_))
    out = []
    for c_ in sorted(cand, key=float):
        e = R(1, 10**4)
        l_, r_ = gp14(c_ - e, av), gp14(c_ + e, av)
        if l_ > 0 > r_: out.append((c_, '극대', sp.nsimplify(g14(c_, av))))
        if l_ < 0 < r_: out.append((c_, '극소', sp.nsimplify(g14(c_, av))))
    return out


E4 = extrema14(4)
check(14, [(c_, ty) for c_, ty, _ in E4] == [(-R(5, 2), '극소'), (-R(1, 2), '극대'), (R(3, 2), '극소')], f'a=4: 극점 {[(c_, ty) for c_, ty, _ in E4]}')
check(14, [v for *_, v in E4] == [-R(47, 12), -R(11, 12), -R(47, 12)], f'a=4: 극값 {[v for *_, v in E4]}')
# 경우별 g'(t) 식 확인
ts = sp.symbols('ts', real=True)
check(14, sp.expand((ts + 1) * (ts + 1 - a) - ts * (ts - a)) == 2 * ts + 1 - a and sp.expand((ts + 1) * (ts + 1 + a) - ts * (ts + a)) == 2 * ts + 1 + a
      and sp.factor((ts + 1) * (ts + 1 - a) - ts * (ts + a)) == sp.factor((1 - a) * (2 * ts + 1)), "g'(t): t>=0이면 2t+1-a, t<=-1이면 2t+1+a, -1<t<0이면 (1-a)(2t+1)")
# a 전수(1/8 격자 1/8..12): t=3/2에서 극소인 a는 4뿐 (a=1이면 [-1,0]에서 g가 일정)
a_ok = [av for av in [R(i, 8) for i in range(1, 97)] if av != 1 and any(c_ == R(3, 2) and ty == '극소' for c_, ty, _ in extrema14(av))]
check(14, a_ok == [4], f'a 전수(1/8 격자 0<a<=12, a≠1): t=3/2에서 극소인 a = {a_ok}')
check(14, all(gp14(R(i, 8), 1) == 0 for i in range(-8, 1)) and gp14(R(3, 2), 1) != 0, 'a=1이면 -1<=t<=0에서 g\'(t)=0(일정), t=3/2는 극점 아님')
M14 = max(v for _, ty, v in E4 if ty == '극대'); m14 = min(v for _, ty, v in E4 if ty == '극소')
check(14, len({v for _, ty, v in E4 if ty == '극소'}) == 1 and len({v for _, ty, v in E4 if ty == '극대'}) == 1, '극솟값·극댓값이 각각 하나의 값')
ans14 = M14 - m14
check(14, ans14 == 3 and sp.simplify((a**2 - a) / 4).subs(a, 4) == 3, f'극댓값 {M14} - 극솟값 {m14} = {ans14} = (a^2-a)/4')
ans_ok(14, ans14)
uu = sp.symbols('uu')
w_onepiece = sp.integrate(uu**2 - 4 * uu, (uu, -R(1, 2), R(1, 2))) - m14          # x<0 조각 무시
w_mid = f14(0, 4) - f14(2, 4)                                                       # 구간 가운데 함숫값으로 어림
w_swap = 2 * sp.integrate(uu**2 + 4 * uu, (uu, 0, R(1, 2))) - m14                  # 2∫_0^{1/2}에 x<0 조각을 넣음
check(14, w_onepiece == 4 and w_mid == 4 and w_swap == 5, f'오답: x<0 조각 무시 {w_onepiece}(가운데 함숫값 어림 {w_mid}), 2∫_0^(1/2)에 x<0 조각 {w_swap}')
wrong_in(14, [w_onepiece, w_swap], 'x<0 조각 무시 / 조각 바꿔 넣기')
# 원문 D32: g(t)=[t, t+1]에서 f의 최댓값, 미분가능하지 않은 t=α에서 g(α)=-3/4
fo = lambda u: -u * (u + 2) if u < 0 else u * (u - 2)
def gmax(tv, n=400):
    return max(fo(tv + R(i, n)) for i in range(n + 1))
kinks = []
for i in range(-40, 40):
    t0 = R(i, 20) + R(1, 40)
    h_ = R(1, 4000)
    sl = (gmax(t0) - gmax(t0 - h_)) / h_; sr = (gmax(t0 + h_) - gmax(t0)) / h_
    if abs(float(sl - sr)) > 0.2: kinks.append(t0)
check('D32', kinks == [R(1, 2) + R(1, 40) - R(1, 40)] or kinks == [R(21, 40)] or all(abs(float(k_ - R(1, 2))) < 0.06 for k_ in kinks),
      f'D32 원문: 최댓값 함수의 꺾인 점 근처 {kinks}')
check('D32', fo(R(1, 2)) == fo(R(3, 2)) == -R(3, 4) and orig_ans('D32') == r'-\dfrac34', f'D32 원문: g(1/2)=f(1/2)=f(3/2)=-3/4 = 원문 정답 {orig_ans("D32")}')
print('--- 14번 조건 빼 보기 ---')
alt14 = []
for av in (2, 3, 4, 5):
    E = extrema14(av)
    alt14.append(max(v for _, ty, v in E if ty == '극대') - min(v for _, ty, v in E if ty == '극소'))
ablation(14, "'t=3/2에서 극소'", alt14, ans14, 'a=2, 3, 4, 5에서 차 (a^2-a)/4')

# ================= 15번 (J57 후보_순위 3: 이등분 → 1:2, 위 곡선 계수 2배) =================
aa = sp.symbols('aa', real=True)
L15 = x**4 - x**3; U15 = -2 * x**4 + 2 * x; H15 = aa * x * (1 - x)
check(15, sorted(sp.solve(U15 - L15, x), key=lambda z: complex(z).real) and [r_ for r_ in sp.solve(U15 - L15, x) if r_.is_real] == [0, 1] or set(r_ for r_ in sp.solve(U15 - L15, x) if r_.is_real) == {0, 1},
      '두 곡선은 x=0, 1에서만 만남')
check(15, sp.factor(U15 - H15 - x * (1 - x) * (2 * x**2 + 2 * x + 2 - aa)) == 0 and sp.factor(H15 - L15 - x * (1 - x) * (x**2 + aa)) == 0,
      '위 곡선-h = x(1-x)(2x^2+2x+2-a), h-아래 곡선 = x(1-x)(x^2+a): 0<a<2이면 h가 두 곡선 사이')
up = sp.integrate(U15 - H15, (x, 0, 1)); lo = sp.integrate(H15 - L15, (x, 0, 1)); tot = sp.integrate(U15 - L15, (x, 0, 1))
check(15, sp.simplify(up - (R(3, 5) - aa / 6)) == 0 and sp.simplify(lo - (aa / 6 + R(1, 20))) == 0 and tot == R(13, 20), f'위쪽 {up}, 아래쪽 {lo}, 전체 {tot}')
s12 = sp.solve(sp.Eq(2 * lo, up), aa); s21 = sp.solve(sp.Eq(lo, 2 * up), aa)
check(15, s12 == [1] and s21 == [R(23, 10)], f'(아래):(위)=1:2 → a={s12}, 2:1 → a={s21}(0<a<2 밖)')
sols15 = [s_ for s_ in s12 + s21 if 0 < s_ < 2]
check(15, sols15 == [1], f'단서 0<a<2를 만족시키는 해 {sols15}')
ans15 = sp.Integer(sols15[0])
ans_ok(15, ans15)
w_nobelow = sp.solve(sp.Eq(2 * aa / 6, R(3, 5) - aa / 6), aa)[0]
w_orig = sp.solve(sp.Eq(2 * (aa / 6 + R(1, 20)), sp.integrate(-x**4 + x - H15, (x, 0, 1))), aa)[0]
check(15, (w_nobelow, w_orig) == (R(6, 5), R(2, 5)), f'오답: x축 아래 부분 1/20 빠뜨림 {w_nobelow}, 위 곡선을 원문 -x^4+x로 {w_orig}')
wrong_in(15, [w_nobelow, w_orig], 'x축 아래 고정 부분 무시 / 원문 곡선으로 계산')
oa = sp.solve(sp.Eq(sp.integrate(-x**4 + x - H15, (x, 0, 1)), sp.integrate(-x**4 + x - (x**4 - x**3), (x, 0, 1)) / 2), aa)
check('J57', oa == [R(3, 4)] and orig_ans('J57') == r'\dfrac34', f'J57 원문: 이등분 a={oa} = 원문 정답 {orig_ans("J57")}')
print('--- 15번 조건 빼 보기 ---')
# 단서가 없으면 2<a<6에서 곡선이 위 곡선 밖으로 나갔다 들어오며 도형을 여전히 두 부분으로 나눔 → (아래):(위)=2:1인 a가 하나 더


def parts15(av):
    av = sp.nsimplify(av)
    rr = [r_ for r_ in sp.solve(2 * x**2 + 2 * x + 2 - av, x) if r_.is_real and 0 < r_ < 1]
    r0 = rr[0] if rr else 0
    upper = sp.integrate(U15 - H15.subs(aa, av), (x, r0, 1))
    lower = sp.integrate(U15 - L15, (x, 0, r0)) + sp.integrate(H15.subs(aa, av) - L15, (x, r0, 1))
    return lower, upper


import mpmath
fz = lambda av: (lambda lu: float(lu[0] - 2 * lu[1]))(parts15(av))
a_star = mpmath.findroot(lambda z: fz(sp.Float(z, 30)), (2.5, 5.5), solver='bisect') if fz(R(5, 2)) * fz(R(11, 2)) < 0 else None
check(15, a_star is not None and 2 < a_star < 6, f'단서 없이: 2<a<6에서 (아래):(위)=2:1이 되는 a≈{float(a_star):.4f}도 있음(곡선이 두 부분으로 나눔)')
ablation(15, '단서 (단, 0<a<2)', [ans15, sp.Float(a_star, 6)], ans15)
ablation(15, '넓이의 비 1:2', [sp.solve(sp.Eq(lo, up), aa)[0], ans15, sp.solve(sp.Eq(lo, 3 * up), aa)[0]], ans15, '이등분이면 33/20 등 비에 따라 a가 바뀜')

# ================= 16번 (M64 결합 1: (가) h'(x)h'(x-4)=0 실근 3개, (나) [-3,3]에서 차 10 → h'(6)) =================
A, B, c, C, b2 = sp.symbols('A B c C b2', real=True)


def H16(Av, Bv, Cv=None, b2v=0, cv=0, vtx=-1):
    """f=A(x-vtx)^2+q (f(0)=cv), g=Bx^3+b2 x^2+Cx+cv (C 기본값 f'(0))"""
    fv = sp.expand(Av * (x - vtx)**2 - Av * vtx**2 + cv)
    Cv = sp.diff(fv, x).subs(x, 0) if Cv is None else Cv
    gv = sp.expand(Bv * x**3 + b2v * x**2 + Cv * x + cv)
    return fv, gv


def roots_h1(fv, gv):
    """h'(x)=0의 실근 집합 (x<=0은 f', x>0은 g')"""
    rs = {r_ for r_ in sp.solve(sp.diff(fv, x), x) if r_.is_real and r_ <= 0}
    rs |= {r_ for r_ in sp.solve(sp.diff(gv, x), x) if r_.is_real and r_ > 0}
    return rs


def count_ga(fv, gv):
    rs = roots_h1(fv, gv)
    return len(rs | {r_ + 4 for r_ in rs})


def diff_on(fv, gv, lo_=-3, hi_=3):
    pts = [fv.subs(x, lo_), fv.subs(x, 0)] + [fv.subs(x, r_) for r_ in sp.solve(sp.diff(fv, x), x) if r_.is_real and lo_ < r_ < 0]
    pts += [gv.subs(x, hi_)] + [gv.subs(x, r_) for r_ in sp.solve(sp.diff(gv, x), x) if r_.is_real and 0 < r_ < hi_]
    return sp.nsimplify(max(pts) - min(pts))


# 미분가능 → g의 일차항 = f'(0) = 2A, 상수항 = f(0)
fA = sp.expand(A * (x + 1)**2 + c - A)
check(16, sp.diff(fA, x).subs(x, 0) == 2 * A and fA.subs(x, 0) == c, "f=A(x+1)^2+q에서 f(0)=c, f'(0)=2A → g=Bx^3+2Ax+c")
check(16, sp.expand(B * (-x)**3 + b2 * x**2 + C * (-x) + c + B * x**3 + b2 * x**2 + C * x + c - 2 * c) == 2 * b2 * x**2, 'g(-x)+g(x)-2g(0) = 2b2 x^2 → 이차항의 계수 0')
# (가) 전수: A<0, B·s 격자
ok_s = sorted({s_ for s_ in [R(i, 4) for i in range(1, 41)] for Av in (-1, -2, -5) if count_ga(*H16(Av, -2 * R(Av) / (3 * s_**2))) == 3})
negB = all(count_ga(*H16(Av, Bv)) == 2 for Av in (-1, -2) for Bv in (0, -1, -R(1, 3)))
check(16, ok_s == [3] and negB, f'(가) 전수: B>0에서 g\'의 양수 근 s(1/4 격자 0..10) 중 실근 3개인 것 s={ok_s}, B<=0이면 실근 2개')
# (나): s=3, B=-2A/27
f16, g16 = H16(A, -2 * A / 27)
check(16, sp.factor(sp.diff(g16, x)) == sp.factor(-2 * A / 9 * (x**2 - 9)), "s=3이면 g'(x)=3B(x^2-9) → (0, 3)에서 감소")
dA = [diff_on(*H16(Av, -2 * R(Av) / 27)) for Av in (-1, -2, -3)]
check(16, dA == [5, 10, 15], f'[-3, 3]에서 최댓값-최솟값 = -5A (A=-1,-2,-3에서 {dA})')
A16 = sp.solve(sp.Eq(-5 * A, 10), A)[0]
B16 = -2 * A16 / 27
f16, g16 = H16(A16, B16)
check(16, A16 == -2 and B16 == R(4, 27) and count_ga(f16, g16) == 3 and diff_on(f16, g16) == 10, f'A={A16}, B={B16}: (가) 실근 {count_ga(f16, g16)}개, (나) 차 {diff_on(f16, g16)}')
mx = max([f16.subs(x, v) for v in (-3, -1, 0)] + [g16.subs(x, 3)]); mn = min([f16.subs(x, v) for v in (-3, -1, 0)] + [g16.subs(x, 3)])
check(16, mn == g16.subs(x, 3) and mn < f16.subs(x, -3) and mx == f16.subs(x, -1), f'최솟값은 g(3)={g16.subs(x, 3)} (f(-3)={f16.subs(x, -3)}보다 작음), 최댓값 f(-1)={f16.subs(x, -1)}')
# 전수: A(1/2 격자 -10..-1/2) × s(1/4 격자) 중 (가)(나) 만족은 A=-2, s=3뿐
pairs = [(Av, s_) for Av in [R(-i, 2) for i in range(1, 21)] for s_ in [R(i, 4) for i in range(1, 25)]
         if count_ga(*H16(Av, -2 * Av / (3 * s_**2))) == 3 and diff_on(*H16(Av, -2 * Av / (3 * s_**2))) == 10]
check(16, pairs == [(-2, 3)], f'(A, s) 전수: {pairs}')
ans16 = sp.diff(g16, x).subs(x, 6)
check(16, ans16 == 12, f"h'(6)=g'(6)={ans16}")
ans_ok(16, ans16)
A_w = sp.solve(sp.Eq(-4 * A, 10), A)[0]                       # 최솟값을 f(-3)=c+3A로
w_end = sp.diff(H16(A_w, -2 * A_w / 27)[1], x).subs(x, 6)
w_nolin = 3 * B16 * 36                                         # g'에서 2A 빠뜨림
check(16, (w_end, w_nolin) == (15, 16), f'오답: 최솟값을 f(-3)으로 {w_end}, 2A 빠뜨림 {w_nolin}')
wrong_in(16, [w_end, w_nolin], '최솟값 끝값 f(-3) / g\'의 일차항 계수 빠뜨림')
# 원문 M64: (가) h(x)=h(0)의 실근의 합 1 → 양근 3 → B=-2A/9, (나) [-2,3] 차 3+4√3 → A=-3, h'(-3)+h'(4)=38
fo16, go16 = H16(A, -2 * A / 9)
d_o = diff_on(*H16(-1, R(2, 9)), lo_=-2, hi_=3)
Ao = sp.solve(sp.Eq(d_o * (-A), 3 + 4 * sp.sqrt(3)), A)[0]
fo, go = H16(Ao, -2 * Ao / 9)
o16 = sp.diff(fo, x).subs(x, -3) + sp.diff(go, x).subs(x, 4)
rt = sorted(set(sp.solve(fo - fo.subs(x, 0), x)) | {r_ for r_ in sp.solve(go - go.subs(x, 0), x) if r_ > 0})
check('M64', sp.simplify(d_o - (1 + R(4, 3) * sp.sqrt(3))) == 0 and Ao == -3 and o16 == 38 == orig_ans('M64') and sum(rt) == 1,
      f'M64 원문: h(x)=h(0)의 근 {rt}(합 1), 차 = ({sp.simplify(d_o)})(-A) → A={Ao}, h\'(-3)+h\'(4)={o16} = 원문 정답 {orig_ans("M64")}')
print('--- 16번 조건 빼 보기 ---')
fv, gv = H16(2, -R(4, 27))      # f(x)<=f(-1) 대신 x=-1에서 극소(A>0)
ablation(16, 'f(x)<=f(-1)', [ans16, sp.diff(gv, x).subs(x, 6)] if count_ga(fv, gv) == 3 and diff_on(fv, gv) == 10 else [], ans16, 'A=2(극소), B=-4/27도 (가)(나) 만족')
# 이차항이 있으면: g'=3B(x-3)(x-r), r=2A/(9B)<0 (양수 근은 3 하나)
Bq = R(1, 9)
Aq_list = []
for Av in [R(-i, 20) for i in range(1, 200)]:
    r_ = 2 * Av / (9 * Bq); b2v = -3 * Bq * (3 + r_) / 2
    fv, gv = H16(Av, Bq, b2v=b2v)
    if count_ga(fv, gv) == 3 and diff_on(fv, gv) == 10: Aq_list.append((Av, sp.diff(gv, x).subs(x, 6)))
check(16, len(Aq_list) >= 1 and all(v_ != ans16 for _, v_ in Aq_list), f'이차항 허용: B=1/9이면 (A, h\'(6)) = {Aq_list}')
ablation(16, 'g(-x)+g(x)=2g(0)', [ans16] + [v_ for _, v_ in Aq_list], ans16)
fv, gv = H16(-1, R(1, 6), Cv=-R(9, 2))   # x=0에서 연속이지만 미분가능하지 않음(C≠2A)
ablation(16, '실수 전체에서 미분가능', [ans16, sp.diff(gv, x).subs(x, 6)] if count_ga(fv, gv) == 3 and diff_on(fv, gv) == 10 else [], ans16, 'A=-1, B=1/6, C=-9/2(연속, 꺾임)')
As = sp.solve(sp.Eq(diff_on(*H16(-1, R(1, 54))) * (-A), 10), A)[0]
fv, gv = H16(As, -As / 54)
ablation(16, '(가) 실근의 개수 3', [ans16, sp.diff(gv, x).subs(x, 6)] if diff_on(fv, gv) == 10 else [], ans16, f's=6(B=-A/54), A={As}이면 실근 {count_ga(fv, gv)}개')
ablation(16, '(나) 차 10', [sp.diff(H16(Av, -2 * Av / 27)[1], x).subs(x, 6) for Av in (-1, -2, -3)], ans16, "h'(6)=-6A")

print('ALL OK' if ok else 'SOME FAIL')
