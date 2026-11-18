# -*- coding: utf-8 -*-
# 6회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 5, 14: 1, 15: 3, 16: 4}          # 분담표 목표 13⑤·14①·15③·16④
DBREF = {13: 'D47 후보_순위 3', 14: 'D31 후보_순위 2', 15: 'J62 후보_순위 3', 16: 'D72 후보_순위 3'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: False, 14: True, 15: False, 16: True}   # 분담표 '계수' ● / ○
BOX = {13: False, 14: False, 15: False, 16: False}      # 13·16 '원문대로'(원문에 상자 없음), 14·15 ×
LEVEL = {13: '중상', 14: '중상', 15: '중상', 16: '상'}
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
    check(no, IT[no]['level'] == LEVEL[no], f'level {IT[no]["level"]} (목표 {LEVEL[no]})')


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
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else choice_val(c)


# ================= 13번 (D47 거울상, 원문 설정 그대로 수치·부호 교체) =================
def g13(fp, tt, b=1):
    """닫힌구간 [tt-b, tt+b]에서 f'(위로 볼록 이차)의 최댓값"""
    v = sp.solve(sp.diff(fp, x), x)[0]
    cand = [tt - b, tt + b] + ([v] if tt - b <= v <= tt + b else [])
    return max(fp.subs(x, c) for c in cand)


T13 = [2 + R(i, 8) for i in range(17)]                 # t∈[2, 4] 격자
good = []
for i in range(1, 49):                                 # f'=-3(x-2)(x-c), c∈(2, 8] 격자 (x=2에서 극소 ⇔ c>2)
    c = 2 + R(i, 8); fp = -3 * (x - 2) * (x - c)
    if len({g13(fp, tt) for tt in T13}) == 1: good.append(c)
check(13, good == [4], f'c 격자 전수: g가 [2, 4]에서 일정한 c = {good}')
fp13 = -3 * (x - 2) * (x - 4)
f13 = sp.integrate(fp13, (x, 2, x)) + 1
check(13, sp.expand(f13) == -x**3 + 9 * x**2 - 24 * x + 21 and sp.diff(fp13, x).subs(x, 2) > 0, f'f(x)={sp.expand(f13)}, x=2 극소, f(2)=1')
k13 = g13(fp13, 3)
ans13 = f13.subs(x, 4) + k13
check(13, k13 == 3 and f13.subs(x, 4) == 5 and ans13 == 8, f'k={k13}, f(4)={f13.subs(x, 4)}, f(4)+k={ans13}')
ans_ok(13, ans13)
fp_w = -(x - 2) * (x - 4)
wrong_in(13, [f13.subs(x, 4) + fp13.subs(x, 2), f13.subs(x, 4) + g13(fp_w, 3)], 'k를 f′(2)=0으로 5 · 계수 3 누락 k=1로 6')
fo = x**3 + 6 * x**2 + 9 * x + 6
fpo = sp.diff(fo, x)
gmin = {min(fpo.subs(x, cc) for cc in [tt - 1, tt + 1] + ([-2] if tt - 1 <= -2 <= tt + 1 else [])) for tt in [-3 + R(i, 8) for i in range(17)]}
check(13, fo.subs(x, -1) == 2 and gmin == {-3} and fo.subs(x, 1) - 3 == orig_ans('D47'), f'원문 D47: g=-3 일정, f(1)+k={fo.subs(x, 1) - 3} = 원문 답 {orig_ans("D47")}')
# 빼 보기
ab = set()
for c in (3, 5, 6):
    fp = -3 * (x - 2) * (x - c); ff = sp.integrate(fp, (x, 2, x)) + 1
    ab.add(ff.subs(x, 4) + fp.subs(x, (2 + c) / sp.Integer(2)))
ablation(13, "'[2, 4]에서 g(t)가 일정'", ab, 8, '꼭짓점 위치(c)가 정해지지 않음')
ab2 = set()
for C in (0, 5):
    ff = sp.integrate(fp13, (x, 2, x)) + C
    ab2.add(ff.subs(x, 4) + 3)
ablation(13, "'극솟값 1'", ab2, 8, '적분상수가 정해지지 않음')
ablation(13, "'최댓값'(→ 최솟값)", [] if all(len({min(fp13.subs(x, cc) for cc in (tt - 1, tt + 1)) for tt in T13}) > 1 for _ in [0]) else [8], 8, '위로 볼록한 f′의 최솟값은 늘 구간 끝값이라 [2, 4]에서 일정하지 않음')


# ================= 14번 (D31: LIVE058 뼈대 + p 역산 + 꺾인 점 x좌표의 합) =================
def kink_sum(f):
    """|f|가 미분가능하지 않은 점 = 홀수 중복도 실근. (개수, 합) 반환"""
    rs = sp.roots(sp.Poly(f, x))
    pts = [r for r, m in rs.items() if r.is_real and m % 2 == 1]
    # roots()가 놓친 실근 확인
    nreal = len(set(sp.Poly(f, x).real_roots()))
    assert nreal == len([r for r in rs if r.is_real]), 'roots 누락'
    return len(pts), sp.nsimplify(sum(pts)) if pts else None


def solve14(p_val, kpos=True, need_n2=True, need_tan=True):
    f0 = 3 * x**4 + p_val * x**3 - 24 * x**2
    cps = [r for r in sp.roots(sp.Poly(sp.diff(f0, x), x)) if r.is_real]
    ks = {sp.nsimplify(-f0.subs(x, r)) for r in cps}          # x축에 접하는 k: 극값 = 0
    out = set()
    for k in ks:
        if kpos and not k > 0: continue
        n, s = kink_sum(sp.expand(f0 + k))
        if need_n2 and n != 2: continue
        out.add(s)
    return out


p14 = sp.solve(sp.diff(3 * x**4 + sp.Symbol('p') * x**3 - 24 * x**2, x).subs(x, 1), sp.Symbol('p'))
check(14, p14 == [12], f"f'(1)=0 → p={p14}")
fp14 = sp.diff(3 * x**4 + 12 * x**3 - 24 * x**2, x)
check(14, sp.factor(fp14) == 12 * x * (x - 1) * (x + 4) and sp.diff(fp14, x).subs(x, 1) > 0, f"f'={sp.factor(fp14)}, x=1 극소")
f0 = 3 * x**4 + 12 * x**3 - 24 * x**2
check(14, sorted([f0.subs(x, r) for r in (-4, 0, 1)]) == [-384, -9, 0], '극값 k-384, k, k-9')
for k in (384, 9, 0):
    print(f'      k={k}: f={sp.factor(f0 + k)}, |f| 꺾인 점 (개수, 합)={kink_sum(f0 + k)}')
s14 = solve14(12)
check(14, s14 == {-6}, f'k>0·접함·꺾인 점 2개 → 합 {s14}')
ans_ok(14, -6)
wrong_in(14, [-6 + 1, R(-12, 3)], '접점 x=1 포함 −5 · 네 근의 합(또는 k=0의 3x²+12x−24) −4')
check(14, kink_sum(f0)[1] == -4, 'k=0일 때 꺾인 점의 합 −4(③ 근거 확인)')
# 원문 D31: k=0,5 → ㄱ 참, ㄴ 거짓(k=5 극댓값 5), ㄷ 합 5 참 → ③ ㄱ, ㄷ
fo = 3 * x**4 - 4 * x**3 - 12 * x**2
ko = [k for k in (0, 5, 32) if kink_sum(fo + k)[0] == 2]
check(14, ko == [0, 5] and sum(ko) == 5 and orig_ans('D31') == 'T:ㄱ, ㄷ', f'원문 D31: k={ko}, 합 5, 원문 답 {orig_ans("D31")}')
# 빼 보기
ablation(14, "'x=1에서 극소'", set().union(*[solve14(pv) for pv in (0, 12, -12, 30)]), -6, 'p를 바꾸면 꺾인 점의 합이 달라짐(극점이 유리수인 p=0, 12, −12, 30 확인)')
ablation(14, "'극댓값은 0보다 크다'(k>0)", solve14(12, kpos=False), -6, 'k=0(극댓값 0)도 꺾인 점이 2개')
ablation(14, "'x축에 접한다'", {sp.Float(sp.N(kink_sum(f0 + k)[1], 8), 5) for k in (10, 20, 100) if kink_sum(f0 + k)[0] == 2}, -6, '9<k<384인 k에서도 꺾인 점이 2개')
r_ = solve14(12, need_n2=False)
ablation(14, "'개수가 2'", None, -6, undef=f'k=384도 남고 그때는 꺾인 점이 없어 합이 정해지지 않음(남는 경우의 합 {r_})')


# ================= 15번 (J62 + 접하는 직선 y=mx+2) =================
F15 = 4 * x**3 - 6 * x**2 + x + 4
m, s_ = sp.symbols('m s', real=True)
tan = sp.solve([sp.diff(F15, x).subs(x, s_) - m, F15.subs(x, s_) - (m * s_ + 2)], [s_, m], dict=True)
tan_r = [d for d in tan if d[s_].is_real]
check(15, tan_r == [{s_: 1, m: 1}], f'점 (0, 2)를 지나 곡선에 접하는 직선: 접점·기울기 {tan_r} (실수해 하나)')
T15 = x + 2
H = sp.factor(F15 - T15)
check(15, H == 2 * (x - 1)**2 * (2 * x + 1), f'곡선−직선={H}')
check(15, all((F15 - T15).subs(x, R(i, 20)) >= 0 for i in range(41)) and sp.solve(F15 - T15, x) == [-R(1, 2), 1],
      '0≤x≤2에서 곡선이 직선 위(교점 −1/2, 1뿐) → A·B 모두 곡선이 위')
A15 = sp.integrate(F15 - T15, (x, 0, 1)); B15 = sp.integrate(F15 - T15, (x, 1, 2))
check(15, (A15, B15) == (1, 3), f'A={A15}, B={B15}')
ans_ok(15, B15 - A15)
wrong_in(15, [sp.integrate(F15 - T15, (x, 0, 2)), sp.integrate(H / 2, (x, 1, 2)) - sp.integrate(H / 2, (x, 0, 1))], '원문 습관 ∫₀²(곡선−직선)=A+B=4 · 인수 2 누락 1')
# 원문 J62: B−A=∫₀²(f−(mx+2))=2/3 → m=−4/3
fo = x**3 / 4 + x / 2
mo = sp.solve(sp.Eq(sp.integrate(fo - (m * x + 2), (x, 0, 2)), R(2, 3)), m)
check(15, mo == [orig_ans('J62')], f'원문 J62: m={mo}, 원문 답 {orig_ans("J62")}')
# 빼 보기
abl = set()
for mm in (7, 8, 10):   # '접할 때'를 빼면 m이 자유: 0<x<2에서 한 점에서 교차하는 m이면 B−A=∫₀²(곡선−직선)
    rr = [r for r in sp.Poly(F15 - (mm * x + 2), x).real_roots() if 0 < r < 2]
    if len(rr) == 1: abl.add(sp.integrate(F15 - (mm * x + 2), (x, 0, 2)))
ablation(15, "'직선 y=mx+2가 곡선에 접할 때'", abl, 2, 'm=7, 8, 10(0<x<2에서 한 점에서 교차)마다 B−A가 다름')
A2 = sp.integrate(F15 - T15, (x, -R(1, 2), 1))
ablation(15, "'y축'", {B15 - A2}, 2, f'A가 곡선과 직선만으로 둘러싸인 부분(−1/2≤x≤1, 넓이 {A2})이 됨')
ablation(15, "'x=2'", None, 2, undef='x>1에서 곡선이 계속 직선 위에 있어 B가 닫힌 부분이 되지 않음')


# ================= 16번 (D72 + GEN1-01-172 뒤집기 + 폭 b, 순서쌍 개수) =================
def cnt16(tv, par, cub=2 * x**3 - 6 * x + 1, c0=2):
    s1 = {r for r in sp.Poly(sp.expand(cub - tv), x).real_roots() if r <= c0}
    s2 = {r for r in sp.Poly(sp.expand(par - tv), x).real_roots() if r > c0}
    return len(s1) + len(s2)


def kset16(par, target, cub=2 * x**3 - 6 * x + 1, c0=2):
    """합이 target인 k의 집합(열린 높이 구간에서 성립하면 None = 무수히 많음)"""
    hs = set()
    for r in sp.roots(sp.Poly(sp.diff(cub, x), x)):
        if r.is_real and r <= c0: hs.add(sp.Rational(cub.subs(x, r)))
    for r in sp.roots(sp.Poly(sp.diff(par, x), x)):
        if r.is_real and r > c0: hs.add(sp.Rational(par.subs(x, r)))
    hs |= {sp.Rational(cub.subs(x, c0)), sp.Rational(par.subs(x, c0))}
    hs = sorted(hs); e = R(1, 10**4)
    pts = [hs[0] - 1] + [(hs[i] + hs[i + 1]) / 2 for i in range(len(hs) - 1)] + [hs[-1] + 1]
    if any(3 * cnt16(p_, par, cub, c0) == target for p_ in pts): return None
    return [h for h in hs if cnt16(h - e, par, cub, c0) + cnt16(h, par, cub, c0) + cnt16(h + e, par, cub, c0) == target]


def pairs16(parf, target, cond=lambda K: K is not None and len(K) == 1, A=70, B=10):
    out = []
    for a in range(1, A):
        for b in range(1, B):
            K = kset16(parf(a, b), target)
            if cond(K): out.append((a, b))
    return out


par16 = lambda a, b: -a * (x - 2) * (x - b - 2) - 11
P16 = pairs16(par16, 8)
check(16, P16 == [(1, 8), (4, 4), (16, 2), (64, 1)], f'전수(1≤a≤69, 1≤b≤9): 순서쌍 {P16}')
big = [(a, b) for a in range(70, 260) for b in (1, 2) if (lambda K: K is not None and len(K) == 1)(kset16(par16(a, b), 8))]
check(16, big == [], f'a≥70(b=1, 2)에서 추가 순서쌍 없음 {big} (b≥3이면 ab²/4−11≥5에서 a≤7)')
check(16, all(R(a * b * b, 4) - 11 == 5 for a, b in P16), '모두 꼭짓점 높이 ab²/4−11=5')
e = R(1, 10**4)
trip = [(cnt16(5 - e, par16(16, 2)), cnt16(5, par16(16, 2)), cnt16(5 + e, par16(16, 2)))]
check(16, trip == [(5, 3, 0)], f'(16, 2), k=5: (좌극한, 함숫값, 우극한)={trip[0]}')
for a, b in [(1, 1), (8, 2), (10, 2), (20, 2)]:
    pr = par16(a, b); M = R(a * b * b, 4) - 11
    print(f'      (a, b)=({a}, {b}), M={M}: ' + ', '.join(f'k={h}:({cnt16(h - e, pr)}, {cnt16(h, pr)}, {cnt16(h + e, pr)})' for h in sorted({-11, -3, 5, M})))
ans_ok(16, len(P16))
w1 = len([b for b in range(1, 40) if 32 % (b * b) == 0])     # 꼭짓점을 −3에: ab²=32
w2 = len([b for b in range(1, 40) if 16 % (b * b) == 0])     # 1/4 누락: ab²=16
w3 = len([b for b in range(1, 40) if 8 % (b * b) == 0])      # 둘 다: ab²=8
check(16, (w1, w2, w3) == (3, 3, 2), f'오답 경로 개수: ab²=32 → {w1}, ab²=16 → {w2}, ab²=8 → {w3}')
wrong_in(16, [w1, w3], '꼭짓점을 극솟값 −3에 맞춤(또는 1/4 누락) 3 · 둘 다 2')
# 원문 D72: (48,3),(12,4),(3,6) → a+b 최댓값 51
Po = pairs16(lambda a, b: a * (x - 2) * (x - b) + 9, 9, A=60, B=10)
check(16, Po == [(3, 6), (12, 4), (48, 3)] and max(a + b for a, b in Po) == orig_ans('D72'), f'원문 D72: {Po}, a+b 최댓값 {max(a + b for a, b in Po)} = 원문 답 {orig_ans("D72")}')
# GEN1-01-172와 같은 문항이 아님: 같은 식(두 번째 근 b)이면 (64,3),(16,4),(4,6),(1,10), a+b의 합 108
Pg = pairs16(lambda a, b: -a * (x - 2) * (x - b) - 11, 8, A=70, B=12)
check(16, Pg == [(1, 10), (4, 6), (16, 4), (64, 3)] and sum(a + b for a, b in Pg) == 108, f'GEN1-01-172 원식: {Pg}, 합 108 (본 문항은 폭 b·개수로 바꿈)')
# 빼 보기
ablation(16, "'a는 자연수'", None, 4, undef='a가 양의 실수이면 ab²=64를 만족시키는 (a, b)가 b마다 하나씩 무수히 많음')
ablation(16, "'b는 자연수'", None, 4, undef='b가 양의 실수이면 a마다 b=8/√a로 무수히 많음')
P_t9 = pairs16(par16, 9, A=40, B=6)
ablation(16, "합 '8'(→ 9)", [len(P_t9)], 4, '합을 3의 배수 9로 바꾸면 순서쌍 개수가 달라짐')
P_c = pairs16(lambda a, b: -a * (x - 2) * (x - b - 2) - 7, 8, A=60, B=8)
ablation(16, "포물선 상수 '−11'(→ −7)", [len(P_c)], 4, f'출발 높이를 바꾸면 ab²=48, 순서쌍 {P_c}')

print('ALL OK' if ok else 'SOME FAIL')
