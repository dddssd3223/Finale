# -*- coding: utf-8 -*-
# 10회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import numpy as np
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 3, 14: 5, 15: 2, 16: 4}          # 분담표 목표 13③·14⑤·15②·16④ 그대로
DBREF = {13: 'D36 학교식_예상 1', 14: 'D19 후보_순위 2', 15: 'M60 v3_추가 1', 16: 'M62 후보_순위 2'}   # 13은 분담표 'D36 v3_추가 1'에서 바꿈(note: 9번 I57과 같은 틀, 측정 B로 갈래 줄임)
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: False, 14: True, 15: False, 16: False}   # 분담표 계수 13●·14●·15○·16●(16은 자연스러운 자리가 없어 빠짐, note에 적음)
BOX = {13: True, 14: False, 15: False, 16: True}         # 13·16 '원문대로'(원문에 상자 있음), 14·15 ×
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t, k = sp.symbols('x t k', real=True)
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
        check(no, str(val) not in nums, f'정답 {val}이 본문에 나온 수 {sorted(nums, key=int)}와 다름')


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
        sv = sorted(set(vals), key=str)
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


# ================= 13번 (D36: f=¼x⁴−2x³+ax²+bx, (가) x=0 극값, (나) (a,∞)에서 증가, f′(5)의 최솟값) =================
def fp13(a, b, p=6):
    return x**3 - p * x**2 + 2 * a * x + b


def ga13(a, b):
    """(가) x=0에서 극값 ⇔ f′(0)=0이고 x=0의 좌우에서 f′의 부호가 바뀜"""
    g = fp13(a, b); e = R(1, 10**6)
    return g.subs(x, 0) == 0 and g.subs(x, -e) * g.subs(x, e) < 0


def na13(a, b, lo=None):
    """(나) 구간 (lo,∞)에서 증가(lo 기본값 a) ⇔ x>lo에서 f′(x)≥0 (삼차 f′: 끝 x=lo의 값과 lo보다 큰 극소점의 값)"""
    lo = a if lo is None else lo
    g = fp13(a, b)
    pts = [z for z in sp.Poly(sp.diff(g, x), x).real_roots() if z > lo]
    return g.subs(x, lo) >= 0 and all(g.subs(x, z) >= 0 for z in pts)


agrid = [R(i, 4) for i in range(-40, 49)]          # a ∈ [−10, 12]
bgrid = [R(i, 2) for i in range(-6, 7)]            # b ∈ [−3, 3]
feas13 = [(a, b) for a in agrid for b in bgrid if ga13(a, b) and na13(a, b, lo=4)]
check(13, all(b == 0 for _, b in feas13) and sorted({a for a, _ in feas13}) == [a for a in agrid if a >= 4],
      f'(a, b) 격자(a −10~12 1/4 간격 × b −3~3 1/2 간격) 전수: 조건 ⇔ b=0, a≥4 (a의 최솟값 {min(a for a, _ in feas13)})')
check(13, not na13(R(39, 10), 0, lo=4) and na13(4, 0, lo=4) and sp.factor(fp13(4, 0)) == x * (x - 2) * (x - 4), 'a=3.9는 (나) 불가, a=4이면 f′=x(x−2)(x−4)로 열린 끝 x=4에서 f′=0')
vals13 = [fp13(a, b).subs(x, 5) for a, b in feas13]
ans13 = min(vals13)
check(13, ans13 == 15, f"f′(5)=10a−25의 격자 최솟값 {ans13}")
ans_ok(13, ans13)
w13a = fp13(R(9, 2), 0).subs(x, 5)          # 원문처럼 꼭짓점 판정 a≥9/2
w13b = fp13(5, 0).subs(x, 5)                # 열린 끝 경계 a=4를 빼고 정수 a=5
check(13, na13(R(9, 2), 0, lo=4) and na13(5, 0, lo=4), 'a=9/2, a=5는 가능하지만 최소 아님(오답 경로 값)')
wrong_in(13, [w13a, w13b], '꼭짓점 판정 a≥9/2 → 20 · 경계 a=4 제외 a=5 → 25')
# 원문 D36: 구간 (0,∞), f′(1)의 최솟값 4
feas_o = [a for a in agrid if ga13(a, 0) and na13(a, 0, lo=0)]
check(13, min(feas_o) == R(9, 2) and fp13(min(feas_o), 0).subs(x, 1) == orig_ans('D36') == 4, f'원문 D36: a≥{min(feas_o)}, f′(1)의 최솟값 {fp13(min(feas_o), 0).subs(x, 1)} = 원문 답')
check(13, fp13(min(feas_o), 0).subs(x, 5) == 20, '구간을 원문 (0,∞)로 두면 f′(5)의 최솟값 20(장치가 답을 바꿈)')
# 빼 보기
ablation(13, "(나) '구간 (4,∞)에서 증가'", None, ans13, undef='a는 0이 아닌 아무 실수, f′(5)=10a−25의 최솟값이 없음')
a_, b_ = 1, 24                               # (가) 없이: f′(4)=0, x>4에서 f′>0
check(13, na13(a_, b_, lo=4) and not ga13(a_, b_), f'(가) 반례 a=4, b={b_}: (나) 성립, (가) 불성립')
ablation(13, "(가) 'x=0에서 극값'", [ans13, fp13(a_, b_).subs(x, 5)], ans13, f'b가 자유로우면 f′(5)={fp13(a_, b_).subs(x, 5)}처럼 더 작아짐')


# ================= 14번 (D19: y=f(x)와 y=3x²−3x−8이 접하는 k의 합) =================
f14 = x**3 - 3 * x**2 - 9 * x + k
g14 = 3 * x**2 - 3 * x - 8
h14 = sp.expand(f14 - g14)
D14 = sp.factor(sp.discriminant(h14, x))
ks = sp.solve(D14, k)
check(14, len(ks) == 2 and all(z.is_real for z in ks), f'접함 ⇔ h=f−g가 중근 ⇔ 판별식 {D14}=0 ⇔ k={ks} (모든 k 전수)')
for kv in ks:
    hh = h14.subs(k, kv)
    cr = [z for z in sp.solve(sp.diff(hh, x), x) if sp.simplify(hh.subs(x, z)) == 0]
    check(14, len(cr) == 1 and sp.simplify(sp.diff(f14, x).subs(x, cr[0]) - sp.diff(g14, x).subs(x, cr[0])) == 0,
          f'k={kv}: x={cr[0]}에서 두 그래프가 만나고 기울기 같음(접함)')
ans14 = sp.simplify(sum(ks))
crit = sp.solve(sp.diff(h14, x), x)
check(14, all(not z.is_rational for z in crit), f'차함수 극점 {crit}는 무리수, 합은 정수')
ans_ok(14, ans14)
f0 = x**3 - 3 * x**2 - 9 * x
w14a = sum((g14 - f0).subs(x, z) for z in (-1, 3))                # 원문 f의 극점 −1, 3 그대로
w14b = -(h14 - k).subs(x, 2)                                       # 가운데 x=2 하나만
wrong_in(14, [w14a, w14b], '원문 극점 사용 30 · 가운데 하나 20')
fo19 = x**3 - 3 * x**2 - 9 * x + k
so19 = sp.solve(sp.discriminant(fo19, x), k)
check(14, sum(so19) == orig_ans('D19') == 22, f'원문 D19: k={so19}, 합 {sum(so19)} = 원문 답')
ablation(14, "'곡선 y=3x²−3x−8'(원문 x축으로 되돌림)", [sum(so19)], ans14, '원문 답 22')


# ================= 15번 (M60: f=x³+ax²+bx+1, f′의 근이 모두 음수, ∫₋₁¹f′>8, 보기) =================
def count_k15(a, b, c=1):
    """방정식 f(x)−f′(k)x=0의 서로 다른 실근이 2개인 실수 k의 개수 (수치 60자리: m=f′(k)에 대한 판별식의 실근 m → 그 m에서 실근 2개 확인 → f′(k)=m의 실근 k)"""
    import mpmath as mp
    mp.mp.dps = 40
    A, B, C = [mp.mpf(sp.Rational(v).p) / sp.Rational(v).q for v in (a, b, c)]
    if c == 0:                     # 원점을 지나면 x{x²+ax+b−m}=0: 실근 2개 ⇔ m=b(이차식이 근 0) 또는 이차식이 0 아닌 중근(m=b−a²/4, a≠0)
        ms = [B] + ([B - A**2 / 4] if A != 0 else [])
        kset = []
        for mv in ms:
            for kv in mp.polyroots([3, 2 * A, B - mv], maxsteps=200, extraprec=100):
                if abs(mp.im(kv)) < mp.mpf(10)**-20 and all(abs(mp.re(kv) - z) > mp.mpf(10)**-20 for z in kset): kset.append(mp.re(kv))
        return len(kset)
    m = sp.symbols('m')
    disc = sp.Poly(sp.discriminant(x**3 + R(a) * x**2 + (R(b) - m) * x + c, x), m)
    co = [mp.mpf(sp.Rational(v).p) / sp.Rational(v).q for v in disc.all_coeffs()]
    ms = [z for z in mp.polyroots(co, maxsteps=200, extraprec=200) if abs(mp.im(z)) < mp.mpf(10)**-30]
    ms = [mp.re(z) for z in ms]
    kset = []
    for mv in ms:
        r = mp.polyroots([1, A, B - mv, C], maxsteps=200, extraprec=200)
        rr = sorted(mp.re(z) for z in r if abs(mp.im(z)) < mp.mpf(10)**-12)
        dist = []
        for z in rr:
            if all(abs(z - w) > mp.mpf(10)**-12 for w in dist): dist.append(z)
        if len(dist) != 2: continue
        for kv in mp.polyroots([3, 2 * A, B - mv], maxsteps=200, extraprec=200):
            if abs(mp.im(kv)) < mp.mpf(10)**-20 and all(abs(mp.re(kv) - z) > mp.mpf(10)**-20 for z in kset): kset.append(mp.re(kv))
    return len(kset)


def judge15(a, b, c=1, bogi='new'):
    a, b = R(a), R(b)
    f = x**3 + a * x**2 + b * x + c
    if bogi == 'new':
        T1 = a > 3
        rr = sp.Poly(f, x).real_roots()
        T2 = all(z < 0 for z in rr)
        T3 = len(set(sp.Poly(sp.expand(f - b * x), x).real_roots())) == 2     # f(x)−f′(0)x=0의 서로 다른 실근 2개
    else:                          # 원문 보기
        T1 = a**2 - 3 * b > 0
        T2 = all(sp.diff(f, x).subs(x, z) >= 0 for z in [R(i, 20) for i in range(-19, 20)])
        T3 = count_k15(a, b, c) == 4
    return 'T:' + ', '.join(n for n, v in zip('ㄱㄴㄷ', (T1, T2, T3)) if v) if (T1 or T2 or T3) else 'T:(없음)'


def cond15(a, b, neg=True, meet=True, integ=True):
    """본문 조건: f′=3x²+2ax+b가 x축과 만남(판별식 ≥0), 만나는 점의 x좌표가 모두 음수, ∫₋₁¹f′=2b+2>8"""
    a, b = R(a), R(b)
    roots = sp.Poly(3 * x**2 + 2 * a * x + b, x).real_roots()
    return (not meet or len(roots) > 0) and (not neg or all(z < 0 for z in roots)) and (not integ or 2 * b + 2 > 8)


samp = [(R(i, 2), R(j, 2)) for i in range(1, 41, 4) for j in range(7, 41, 4)]
samp += [(R(31, 10), R(32, 10)), (sp.Rational(7, 2), R(4)), (R(11, 2), R(10)), (R(3) + R(1, 50), R(301, 100))]
S15 = [(a, b) for a, b in samp if cond15(a, b)]
J15 = {judge15(a, b) for a, b in S15}
check(15, len(S15) >= 20 and J15 == {'T:ㄱ, ㄴ'}, f'조건을 만족시키는 (a,b) 표본 {len(S15)}개 전부에서 판정 {J15}')
check(15, all(len(set(sp.Poly(x**3 + a * x**2 + 1, x).real_roots())) == 1 for a, b in S15), 'ㄷ: 표본마다 f(x)−f′(0)x=x³+ax²+1=0의 실근 1개')
# ㄷ 일반: a>0이면 h=x³+ax²+1의 극댓값 4a³/27+1>0, 극솟값 h(0)=1>0 → 실근 1개
aa_ = sp.symbols('aa', positive=True)
check(15, sp.simplify((x**3 + aa_ * x**2 + 1).subs(x, -2 * aa_ / 3) - (4 * aa_**3 / 27 + 1)) == 0, 'ㄷ: a>0이면 극댓값 4a³/27+1>0, 극솟값 1>0 → 실근 1개(거짓)')
ans15 = 'T:ㄱ, ㄴ'
ans_ok(15, ans15)
wrong_in(15, ['T:ㄱ, ㄴ, ㄷ', 'T:ㄱ, ㄷ'], 'ㄷ을 원문처럼 x²(x+a)로 보아 ⑤ · 상수항을 놓쳐 원문 답 ③')
# 원문 M60: f=x³+ax²+bx, a>b>3 → ③
So = [(a, b) for a, b in [(R(i, 2), R(j, 2)) for i in range(7, 30, 2) for j in range(7, 30, 2)] if a > b > 3]
Jo = {judge15(a, b, 0, 'orig') for a, b in So[:15]}
check(15, Jo == {orig_ans('M60')}, f'원문 M60 표본 {len(So[:15])}개 판정 {Jo} = 원문 답 {orig_ans("M60")}')
# 빼 보기
wide = [(R(i, 2), R(j, 2)) for i in range(-20, 41, 4) for j in range(-6, 41, 4)] + [(R(2), R(1)), (R(1), R(1, 4)), (R(5, 2), R(2)), (R(-4), R(4)), (R(1), R(4)), (R(0), R(5))]
for cname, kw, why in (("'x좌표가 음수인 점에서만'", dict(neg=False), 'a<0이면 a>3·실근 음수가 깨짐'),
                       ("'x축과 만난다'", dict(meet=False), '판별식<0이면 a가 작아도 됨'),
                       ("'∫₋₁¹f′(x)dx>8'", dict(integ=False), 'b≤3이면 a>3이 아닐 수 있음')):
    Sx = [(a, b) for a, b in wide if cond15(a, b, **kw)]
    ablation(15, cname, sorted({judge15(a, b) for a, b in Sx}), ans15, why)
ablation(15, "상수항 '+1'(원점 통과)", sorted({judge15(a, b, 0) for a, b in S15[:10]}), ans15, 'f(0)=0이면 ㄴ 거짓(근 0), ㄷ 참(x²(x+a), 실근 2개)')


# ================= 16번 (M62: 계수 10·3, 접점 (0,0)·(−2,0), 넓이를 y=ax³이 이등분) =================
s16, r16, p16 = 10, 3, -2
g16 = r16 * (x - p16)**2


def f16(c):
    return s16 * x**2 * (x - c)


def ntan16(c):
    """점 (−2,0)에서 곡선 y=f(x)에 그은 접선의 개수(접점의 서로 다른 개수; 접점이 다르면 접선도 다름)"""
    f = f16(c)
    eq = sp.expand(sp.diff(f, x).subs(x, t) * (p16 - t) + f.subs(x, t))
    return len(set(sp.Poly(eq, t).real_roots()))


def nroot16(c):
    return len(set(sp.Poly(sp.expand(f16(c) - g16), x).real_roots()))


cgrid = sorted(set([R(i, 2) for i in range(-60, 21)] + [0, -2, -18]))
cand_na = [c for c in cgrid if ntan16(c) == 2]
check(16, cand_na == [-18, -2, 0], f'c 격자(−30~10, 1/2 간격) 전수: (나) 접선 2개 ⇔ c ∈ {cand_na}')
cand = [c for c in cand_na if nroot16(c) == 1]
check(16, cand == [0], f'(다) 실근 1개: c=−18 → {nroot16(-18)}개, c=−2 → {nroot16(-2)}개, c=0 → {nroot16(0)}개 ⇒ c=0, f=10x³')
f16_ = f16(0)
T16 = sp.integrate(g16 - f16_, (x, -2, 0))
a = sp.symbols('a')
sol16 = sp.solve(sp.integrate(g16 - a * x**3, (x, -2, 0)) - T16 / 2, a)
check(16, T16 == 48 and sol16 == [4], f'넓이 {T16}, 이등분 8+4a=24 → a={sol16}')
xs = [R(i, 40) for i in range(-80, 1)]
check(16, all(f16_.subs(x, z) <= 4 * z**3 <= g16.subs(x, z) for z in xs), '곡선 y=4x³은 −2≤x≤0에서 두 곡선 사이(영역을 실제로 둘로 나눔)')
ans16 = sol16[0]
ans_ok(16, ans16)
w16a = sp.solve(a * 4 - T16 / 2, a)[0]                       # ax³과 x축 사이를 전체의 절반으로
w16b = sp.solve(a * 4 - sp.integrate(-f16_, (x, -2, 0)) / 2, a)[0]   # x축 아래 부분만 이등분
wrong_in(16, [w16a, w16b], '이등분 뜻 오독 6 · 아래쪽만 이등분 5')
# 원문 M62: f=x²(x−c), g=−(x−2)², c∈{0,2,18} → c=0, α=3, β=4−2√2, α−β=−1+2√2 → a²+b²=5
fo = lambda c: x**2 * (x - c); go = -(x - 2)**2
def ntan_o(c):
    eq = sp.expand(sp.diff(fo(c), x).subs(x, t) * (2 - t) + fo(c).subs(x, t))
    return len(set(sp.Poly(eq, t).real_roots()))
co = [c for c in sorted(set([R(i, 2) for i in range(-10, 41)])) if ntan_o(c) == 2 and len(set(sp.Poly(sp.expand(fo(c) - go), x).real_roots())) == 1]
xp = sp.symbols('xp', positive=True)
al = sp.minimum(xp**2 + 2 / xp, xp, sp.Interval.open(0, sp.oo)); be = sp.maximum(4 - xp - 2 / xp, xp, sp.Interval.open(0, sp.oo))
dd = sp.nsimplify(al - be)
aa, bb = dd.as_coeff_add()[0], sp.simplify((dd - dd.as_coeff_add()[0]) / sp.sqrt(2))
check(16, co == [0] and aa**2 + bb**2 == orig_ans('M62') == 5, f'원문 M62: c={co}, α={al}, β={be}, a²+b²={aa**2 + bb**2} = 원문 답')
# 빼 보기
ablation(16, "(다) '오직 하나의 실근'", None, ans16, undef=f'(가)(나)만으로 c={cand_na} 셋이 남아 f가 정해지지 않음(c=−2이면 −2<x<0에서 두 곡선이 만나 영역부터 달라짐)')
cand_nb = [c for c in cgrid if nroot16(c) == 1]
ablation(16, "(나) '접선의 개수 2'", None, ans16, undef=f'(가)(다)만 만족시키는 c가 격자에만 {len(cand_nb)}개(예: {[str(z) for z in cand_nb[:4]]}) → f가 정해지지 않음')
ablation(16, "(가) '두 접선이 모두 x축'", None, ans16, undef='f의 꼴 10x²(x−c)와 g=3(x+2)²가 정해지지 않음')
check(16, nroot16(R(1, 2)) == 1 and ntan16(R(1, 2)) != 2, 'c=1/2은 (다)는 만족하지만 (나) 불만족(빼 보기 예)')

print()
print('ALL OK' if ok else 'SOME FAIL')
