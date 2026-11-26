# -*- coding: utf-8 -*-
# 12회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re, itertools
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 4, 14: 1, 15: 3, 16: 2}          # 분담표 13③·14①·15④·16② → 13④·15③ 맞바꿈(묶음 그대로)
DBREF = {13: 'D46 후보_순위 3', 14: 'J16 v3_추가 2', 15: 'I62 v3_추가 1', 16: 'M58 예상밖 1'}   # 16은 분담표 'M58 v3_추가 1'에서 바꿈(note에 이유)
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 계수 13●·14●·15○·16●
BOX = {13: True, 14: False, 15: False, 16: True}         # 13·16 '원문대로'(원문에 상자 있음), 14·15 ×
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t, k, a = sp.symbols('x t k a', real=True)
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
    nums = set(re.findall(r'(?<![\w.])\d+(?![\w.])', re.sub(r'<[^>]*>|style="[^"]*"', '', body)))
    if not IT[no]['choices'][0].startswith('T:'):
        check(no, str(abs(val)) not in nums, f'정답 {val}이 본문에 나온 수 {sorted(nums, key=int)}와 다름')


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
    global ok
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = f'필요(남은 조건을 만족시키는 경우가 없음{"; " + why if why else ""})'
    else:
        sv = sorted(set(vals), key=str)
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:5]))}{" 등" if len(sv) > 5 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else choice_val(c)


# ================= 13번 (D46: f(1)=0인 f=x²+ax+b, g=(x²−x)f, (가) 영점 2개, (나) x축 접점 1개, g(−1)) =================
def tangent_count(g):
    """곡선 y=g(x)가 x축에 접하는 점의 개수: g(c)=0이고 g'(c)=0인 실수 c의 개수"""
    gp = sp.diff(g, x)
    return len([c for c in set(sp.Poly(g, x).real_roots()) if gp.subs(x, c) == 0])


def zero_count(g):
    return len(set(sp.Poly(g, x).real_roots()))


def cands13(need_f1=True, use_ga=True, use_na=True):
    """f=x²+ax+b의 모양을 전수: 근이 {0,1}과 관련된 경우와 일반 근(정수 격자)·실근 없는 경우까지"""
    fs = []
    for r1, r2 in itertools.combinations_with_replacement([-3, -1, 0, R(1, 2), 1, 2, 3, 5], 2):
        fs.append(sp.expand((x - r1) * (x - r2)))
    for c in [1, 2, 5]:   # 실근이 없는 f
        fs.append(sp.expand(x**2 + c))
        fs.append(sp.expand((x - 1)**2 + c))
    out = []
    for f in fs:
        if need_f1 and f.subs(x, 1) != 0:
            continue
        g = sp.expand((x**2 - x) * f)
        if use_ga and zero_count(g) != 2:
            continue
        if use_na and tangent_count(g) != 1:
            continue
        out.append((sp.factor(g), g.subs(x, -1)))
    return out


C13 = cands13()
check(13, len({v for _, v in C13}) == 1, f'f(1)=0이고 (가)(나)를 만족시키는 g 전수: {sorted(set(str(gg) for gg, _ in C13))} → g(−1) {sorted({v for _, v in C13})}')
rr = sp.symbols('r', real=True)
gen13 = sp.expand(x * (x - 1)**2 * (x - rr))
check(13, all(zero_count(gen13.subs(rr, v)) == (2 if v in (0, 1) else 3) for v in [-2, 0, R(1, 3), 1, 4]), 'g=x(x−1)²(x−r): 영점 개수 2 ⇔ r∈{0,1}')
check(13, tangent_count(sp.expand(x**2 * (x - 1)**2)) == 2 and tangent_count(sp.expand(x * (x - 1)**3)) == 1, '접점 개수: x²(x−1)²은 2, x(x−1)³은 1(삼중근 x=1에서 접함)')
ans13 = C13[0][1]
check(13, ans13 == 8, f'g(−1) = {ans13}')
ans_ok(13, ans13)
w13a = sp.expand(x**3 * (x - 1)).subs(x, -1)        # 원문 f(0)=0 → x³(x−1)
w13b = sp.expand(x**2 * (x - 1)**2).subs(x, -1)     # (나) 무시/삼중근 접함 오판 → x²(x−1)²
wrong_in(13, [w13a, w13b], '원문 f(0)=0 꼴 x³(x−1) → 2 · 버린 후보 x²(x−1)² → 4')
# 원문 D46: f(0)=0, g=(x²−2x)f, (가) 영점 2개 (나) 극댓값 없음 → 극솟값 −27/16
og = []
for pp in [-3, -2, -1, 0, 1, 2, 3]:
    g = sp.expand((x**2 - 2 * x) * x * (x + pp))
    if zero_count(g) != 2:
        continue
    gp = sp.diff(g, x); crit = sorted(set(sp.Poly(gp, x).real_roots()))
    gpp = sp.diff(g, x, 2)
    has_max = any((gp.subs(x, c - R(1, 1000)) > 0 and gp.subs(x, c + R(1, 1000)) < 0) for c in crit)
    if not has_max:
        mins = [g.subs(x, c) for c in crit if gp.subs(x, c - R(1, 1000)) < 0 and gp.subs(x, c + R(1, 1000)) > 0]
        og.append(mins)
check(13, og == [[orig_ans('D46')]] and orig_ans('D46') == R(-27, 16), f'원문 D46 극솟값 {og} = 원문 답 {orig_ans("D46")}')
ablation(13, '(가) 영점 개수 2', [v for _, v in cands13(use_ga=False)], ans13, 'r이 0, 1이 아니면 접점은 x=1 하나')
ablation(13, '(나) 접점 개수 1', [v for _, v in cands13(use_na=False)], ans13, 'x²(x−1)²도 남음')
ablation(13, "'f(1)=0'", [v for _, v in cands13(need_f1=False)], ans13, 'x³(x−1)도 남음(실근 없는 f는 접점 0개)')

# ================= 14번 (J16: f=(x−4)², g=−2x+k, S₂=2S₁, H′=f−g, H(t)=H(0)인 양수 t 중 가장 큰 값) =================
h14 = sp.expand((x - 4)**2 - (-2 * x + k))


def S12(kv):
    al, be = sorted(sp.solve(h14.subs(k, kv), x), key=lambda z: float(z))
    S1 = sp.integrate(h14.subs(k, kv), (x, 0, al))
    S2 = sp.integrate(-h14.subs(k, kv), (x, al, be))
    return sp.simplify(S1), sp.simplify(S2), al, be


ksol = [kv for kv in sp.solve(sp.Eq(sp.integrate(h14, (x, 0, 3)), 0), k)]
check(14, ksol == [10], f'S₂=2S₁ ⇔ ∫₀³(f−g)=0 → k={ksol}')
S1, S2, al, be = S12(10)
check(14, sp.simplify(S2 - 2 * S1) == 0 and 0 < al < be, f'k=10: 교점 {al}, {be}, S₁={S1}, S₂={S2} (S₂=2S₁ 직접 확인)')
# k의 유일성: (7,16)에서 S₂−2S₁의 부호 변화 한 번(수치 전수)
vals = []
for i in range(1, 90):
    kv = 7 + R(9 * i, 90)
    s1, s2, _, _ = S12(kv)
    vals.append((kv, sp.N(s2 - 2 * s1)))
roots = [vals[i][0] for i in range(len(vals) - 1) if vals[i][1] == 0 or vals[i][1] * vals[i + 1][1] < 0]
check(14, roots == [10], f'7<k<16에서 S₂=2S₁인 k는 하나({roots})')
Hd = sp.integrate(h14.subs(k, 10), (x, 0, t))
tpos = sorted(r for r in sp.solve(Hd, t) if r > 0)
check(14, sp.factor(Hd) == sp.factor(t * (t - 3) * (t - 6) / 3) and tpos == [3, 6], f'H(t)−H(0) = {sp.factor(Hd)} → 양수 t {tpos}')
ans14 = max(tpos)
ans_ok(14, ans14)
wrong_in(14, [sum(tpos), 10], '두 양수 t의 합 9 · 원문 답 k=10에서 멈춤')
check(14, orig_ans('J16') == 10, f'원문 J16 답 {orig_ans("J16")} = 10')
# 빼 보기: S₂=2S₁ 없음 → 가장 큰 근이 k에 따라 달라짐
alt = []
for kv in [R(19, 2), 10, 11, 12, 15]:
    rts = [r for r in sp.solve(sp.integrate(h14.subs(k, kv), (x, 0, t)), t) if r.is_real and r > 0]
    if rts:
        alt.append(sp.nsimplify(max(rts)))
ablation(14, "'S₂=2S₁'", alt, ans14, '가장 큰 근 (9+√(12k−111))/2')
check(14, all(os.path.exists(os.path.join(HERE, p_)) for p_ in ['fig_14.svg', '../fig_14.svg', '../figs/fig14.py']) and 'fig_14.svg' in IT[14]['body'], '그림 parts/fig_14.svg·회차 fig_14.svg·figs/fig14.py 있음, 본문에 그림')

# ================= 15번 (I62: xf=2x³+ax²+ka+∫₁ˣf, ∫₀¹{f−f(1)}=−4, 보기) =================
c0, c1, c2, C = sp.symbols('c0 c1 c2 C')


def solve15(cond=True, kv=None):
    """f=c2x²+c1x+c0 (차수 확인: xf와 2x³ 비교로 f는 이차) — 항등식 계수 비교로 전수"""
    kk = k if kv is None else kv
    f = c2 * x**2 + c1 * x + c0
    eq = sp.expand(x * f - (2 * x**3 + a * x**2 + kk * a + sp.integrate(f.subs(x, t), (t, 1, x))))
    eqs = sp.Poly(eq, x).all_coeffs()
    if cond:
        eqs.append(sp.integrate(f - f.subs(x, 1), (x, 0, 1)) + 4)
    sol = sp.solve(eqs, [c0, c1, c2, a], dict=True)
    return [(s, f.subs(s)) for s in sol]


S15 = solve15()
check(15, len(S15) == 1, f'항등식+조건의 해 {S15}')
s15, f15 = S15[0]
a15 = s15[a]
check(15, a15 == 2 and sp.expand(f15) == sp.expand(3 * x**2 + 4 * x + 2 * k - 3), f'a={a15}, f={sp.expand(f15)} (a는 k와 무관)')
# 차수 확인: f가 삼차 이상이면 xf의 최고차항이 ∫의 최고차항과 상쇄되지 않음
f3 = sp.symbols('d3') * x**3 + c2 * x**2 + c1 * x + c0
eq3 = sp.Poly(sp.expand(x * f3 - (2 * x**3 + a * x**2 + k * a + sp.integrate(f3.subs(x, t), (t, 1, x)))), x).all_coeffs()
check(15, sp.solve(eq3, [sp.Symbol('d3'), c0, c1, c2], dict=True)[0][sp.Symbol('d3')] == 0, 'f가 삼차라 두면 삼차항 계수 0(f는 이차)')
I01 = sp.integrate(f15, (x, 0, 1))
T = {'ㄱ': a15 == 2,
     'ㄴ': sp.diff(I01, k) == 0,
     'ㄷ': sp.diff(f15, x).subs(x, a15) == 16}
check(15, T == {'ㄱ': True, 'ㄴ': False, 'ㄷ': True}, f'보기 참거짓 {T} (∫₀¹f = {sp.expand(I01)})')
ans15 = 'T:' + ', '.join(z for z in 'ㄱㄴㄷ' if T[z])
ans_ok(15, ans15)
# 오답: ㄴ을 참으로(∫가 정해진다고 봄) → ㄱ,ㄴ,ㄷ / 원문 a=−2로 f′=6x−4, f′(−2)=−16 → ㄷ 거짓 → ㄱ
fo = solve15(cond=False, kv=3)
fprime_o = sp.diff(3 * x**2 - 4 * x - 5, x)
check(15, fprime_o.subs(x, -2) != 16, f"원문 a=−2 기억: f′(x)={fprime_o}, f′(a)={fprime_o.subs(x, -2)} ≠ 16 → ㄷ 거짓")
wrong_in(15, ['T:ㄱ, ㄴ, ㄷ', 'T:ㄱ'], 'ㄴ 함정 · 원문 a=−2로 ㄷ 거짓')
# 원문 I62: k=3, f(1)=∫₀¹f → a+f(3)=8
fo_ = sp.symbols('fo')
f = c2 * x**2 + c1 * x + c0
eqo = sp.Poly(sp.expand(x * f - (2 * x**3 + a * x**2 + 3 * a + sp.integrate(f.subs(x, t), (t, 1, x)))), x).all_coeffs()
eqo.append(f.subs(x, 1) - sp.integrate(f, (x, 0, 1)))
so = sp.solve(eqo, [c0, c1, c2, a], dict=True)[0]
check(15, so[a] + f.subs(so).subs(x, 3) == orig_ans('I62') == 8, f'원문 I62 a+f(3) = {so[a] + f.subs(so).subs(x, 3)} = 원문 답')
# 빼 보기: 적분 조건 없음 → a가 정해지지 않음
S15n = solve15(cond=False)
free = [s for s in S15n if a not in s]
ablation(15, "'∫₀¹{f(t)−f(1)}dt=−4'", None, ans15, undef=f'a가 정해지지 않음(해 {S15n}) → ㄱ·ㄷ 참거짓 미정' if free or not S15n else '')

# ================= 16번 (M58: f=x³−3px²+q, (가) |f| 극점 5개, (나) [−1,1]과 [−1,2p]에서 |f| 최댓값 같음, 25 이하 자연수 쌍 개수) =================
def fM(p, q):
    return x**3 - 3 * p * x**2 + q


def absmax(f, lo, hi):
    crit = [c for c in sp.Poly(sp.diff(f, x), x).real_roots() if lo <= c <= hi]
    return max(abs(f.subs(x, z)) for z in [lo, hi] + crit)


def ga(p, q):
    """|f|가 극대 또는 극소가 되는 점의 개수 = (서로 다른 실근 수) + (f≠0인 극점 수)"""
    f = fM(p, q)
    rts = set(sp.Poly(f, x).real_roots())
    crit = set(sp.Poly(sp.diff(f, x), x).real_roots())
    return len(rts) + len([c for c in crit if f.subs(x, c) != 0])


def nb(p, q, I2=lambda p: (-1, 2 * p), I1=(-1, 1)):
    f = fM(p, q)
    lo, hi = I2(p)
    return absmax(f, *I1) == absmax(f, lo, hi)


def count16(use_a=True, use_b=True, I2=lambda p: (-1, 2 * p), I1=(-1, 1), N=25):
    out = []
    for p in range(1, N + 1):
        for q in range(1, N + 1):
            if use_a and not (0 < q < 4 * p**3):   # 빠른 거름(아래에서 정의대로 다시 확인)
                continue
            if use_a and ga(p, q) != 5:
                continue
            if use_b and not nb(p, q, I2, I1):
                continue
            out.append((p, q))
    return out


# (가)의 빠른 거름이 정의와 같음을 작은 범위에서 확인
check(16, all((ga(p, q) == 5) == (0 < q < 4 * p**3) for p in range(1, 4) for q in range(1, 40)), '(가) ⇔ 0<q<4p³ (p≤3, q<40 전수)')
P16 = count16()
ans16 = len(P16)
check(16, ans16 == 13 and sorted(P16) == [(1, 1), (1, 2), (1, 3)] + [(2, q) for q in range(16, 26)], f'순서쌍 {P16} → {ans16}개')
ans_ok(16, ans16)
w16a = len([pq for pq in P16 if pq[0] != 1])                              # p=1 버림 → 10
w16b = len([pq for pq in P16 if pq[1] >= 2 * pq[0]**3])                   # p=1에도 q≥2p³ 적용 → 12
w16c = len(P16) + 1                                                         # p=1에서 q=4 포함 → 14 (원문 답 14와 같음)
check(16, nb(1, 4) and ga(1, 4) != 5, 'p=1, q=4는 (나)는 만족하나 (가)에서 빠짐(q<4)')
wrong_in(16, [w16a, w16b, w16c], 'p=1 버림 10 · p=1에도 q≥2p³ 12 · q=4 포함(=원문 답) 14')
check(16, len(count16(I2=lambda p: (-2, 2))) == orig_ans('M58') == 14, f'원문 M58([−2,2]) 개수 {len(count16(I2=lambda p: (-2, 2)))} = 원문 답 {orig_ans("M58")}')
ablation(16, '(가) |f| 극점 5개', [len(count16(use_a=False))], ans16)
ablation(16, '(나) 최댓값 같음', [len(count16(use_b=False))], ans16)
ablation(16, "(나)의 구간 끝 2p(→ 원문 2)", [len(count16(I2=lambda p: (-1, 2)))], ans16, '장치가 답을 바꿈')

print()
print('ALL OK' if ok else 'SOME FAIL')
