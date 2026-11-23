# -*- coding: utf-8 -*-
# 9회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 1, 14: 5, 15: 3, 16: 2}          # 분담표 목표 13①·14⑤·15③·16② 그대로
DBREF = {13: 'D45 예상밖 1', 14: 'D25 예상밖 1', 15: 'I65 후보_순위 2', 16: 'I68 v3_추가 2'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 '계수' ● / ○
BOX = {13: True, 14: True, 15: False, 16: True}         # 13·14·16 '원문대로'(원문에 상자 있음), 15 ×
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


# ================= 13번 (D45: f−2=(x+1)²(x−r), 3<x<5에서 f(x)≥f(3), f(7)의 최솟값) =================
r_ = sp.symbols('r', real=True)


def holds13(f, lo=3, hi=5):
    """3<x<5인 모든 x에 대하여 f(x) ≥ f(3) (정확: 구간 안 극값 후보 + 격자)"""
    base = f.subs(x, lo)
    pts = [z for z in sp.Poly(sp.diff(f, x), x).real_roots() if lo < z < hi]
    pts += [lo + R(i, 64) for i in range(1, 128)]
    return all(f.subs(x, z) - base >= 0 for z in pts)


def cond_ga13(f, a=-1):
    """(가): lim_{x→a} (f−2)/(x−a)² 수렴 ⇔ (x−a)²이 f−2를 나눔"""
    return sp.rem(sp.expand(f - 2), sp.expand((x - a)**2), x) == 0


rgrid = [R(i, 4) for i in range(-40, 49)]          # r ∈ [−10, 12]
okr = [rv for rv in rgrid if holds13((x + 1)**2 * (x - rv) + 2)]
check(13, okr == [rv for rv in rgrid if rv <= 5], f'r 격자(−10~12, 1/4 간격) 전수: (나) 성립 ⇔ r≤5 (최대 {max(okr)})')
vals13 = [((x + 1)**2 * (x - rv) + 2).subs(x, 7) for rv in okr]
ans13 = min(vals13)
f13 = (x + 1)**2 * (x - 5) + 2
check(13, ans13 == f13.subs(x, 7) == 130 and cond_ga13(f13) and holds13(f13), f'f=(x+1)²(x−5)+2: (가)(나) 만족, f(7)={f13.subs(x, 7)} = 격자 최솟값 {ans13}')
check(13, sp.diff(f13, x).subs(x, 3) == 0, 'r=5에서 f′(3)=0 (극소점이 기준점 x=3과 일치하는 경계)')
ans_ok(13, ans13)
w13a = ((x + 1)**2 * (x - 5)).subs(x, 7)                         # 2를 더하지 않음
w13b = ((x + 1)**2 * (x - 5) - 2).subs(x, 7)                     # 이항 부호 실수
wrong_in(13, [w13a, w13b], '상수 누락 128 · 이항 부호 실수 126')
check(13, 102 not in ch(13), '원문 답 102와 다름')
# 원문 D45: f−2=(x+2)²(x−r), (3,5)에서 f≥f(4) → r=7, f(8)=102
fo = (x + 2)**2 * (x - 7) + 2
check(13, sp.diff(fo, x).subs(x, 4) == 0 and fo.subs(x, 8) == orig_ans('D45') == 102, f'원문 D45: f(8)={fo.subs(x, 8)} = 원문 답')
# 빼 보기
ablation(13, "(나) '3<x<5에서 f(x)≥f(3)'", None, ans13, undef='r가 아무 실수나 되어 f(7)=64(7−r)+2의 최솟값이 없음')
f_alt = x**3 - 1000                                                  # (가) 위반, 증가라 (나) 성립, f(7)이 더 작음
check(13, not cond_ga13(f_alt) and holds13(f_alt) and f_alt.subs(x, 7) < 130, f'(가) 반례 f=x³−1000: (나) 성립, f(7)={f_alt.subs(x, 7)}<130')
ablation(13, "(가) 극한 조건", [ans13, f_alt.subs(x, 7)], ans13, '다른 삼차함수로 f(7)을 더 작게 할 수 있음(최솟값 없음)')
fa2 = 2 * (x + 1)**2 * (x - r_) + 2                                   # 최고차항 2: (나) ⇔ r≤5 그대로, f(7)=128(7−r)+2
okr2 = [rv for rv in rgrid if holds13(fa2.subs(r_, rv))]
ablation(13, "'최고차항의 계수가 1'", [ans13, min(fa2.subs({r_: rv, x: 7}) for rv in okr2)], ans13, '최고차항 2이면 최솟값 258')


# ================= 14번 (D25: (x−1)g=|(x−1)f(x−p)+q(x−1)|, 음수 p, p+q) =================
f14 = x**3 - 6 * x**2 + 9 * x - 20


def nondiff_count14(pv, fx=f14, c=1):
    """연속이 되도록 q=−f(c−p)로 둔 뒤 g=(x−c)|Q(x)|의 미분불가능점 개수(Q의 c가 아닌 홀수 중복 근 개수)"""
    F_ = sp.expand(fx.subs(x, x - pv) - fx.subs(x, c - pv))
    Q = sp.quo(F_, x - c, x)
    roots = sp.roots(sp.Poly(Q, x))
    cnt = 0
    for z, mlt in roots.items():
        if z.is_real and z != c and mlt % 2 == 1: cnt += 1
    if not roots or sum(roots.values()) < 2:      # 무리근·허근 처리
        rr = sp.Poly(Q, x).real_roots()
        cnt = sum(1 for z in set(rr) if z != c and rr.count(z) % 2 == 1)
    return cnt


def g_cont14(pv, qv, fx=f14, c=1):
    F_ = fx.subs(x, x - pv) + qv
    return sp.simplify(F_.subs(x, c)) == 0


pgrid = [R(i, 4) for i in range(-40, 41)]
sol14 = [pv for pv in pgrid if nondiff_count14(pv) == 1]
check(14, sol14 == [-2, 0], f'p 격자(−10~10, 1/4 간격, q=−f(1−p)) 전수: 미분불가능점 1개인 p = {sol14}')
# 연속 조건 확인: q가 −f(1−p)가 아니면 x=1에서 불연속
check(14, g_cont14(-2, 20) and not g_cont14(-2, 19), 'p=−2: q=20이면 연속, q=19이면 x=1에서 불연속')
pv14, qv14 = -2, -f14.subs(x, 3)
check(14, sp.factor(f14.subs(x, x + 2) + qv14) == (x + 2) * (x - 1)**2, f'p=−2, q={qv14}: F=(x+2)(x−1)², g는 x=−2에서만 미분불가능')
# g가 x=1에서 미분가능, x=−2에서 미분불가능 (좌우 미분계수)
gx = lambda xv: (sp.Abs(xv - 1) / (xv - 1) * sp.Abs((f14.subs(x, xv + 2) + 20))) if xv != 1 else 0
hh = R(1, 10**6)
dl = (gx(1) - gx(1 - hh)) / hh; dr = (gx(1 + hh) - gx(1)) / hh
dl2 = (gx(-2) - gx(-2 - hh)) / hh; dr2 = (gx(-2 + hh) - gx(-2)) / hh
check(14, abs(dl - dr) < R(1, 1000) and abs(dl2 - dr2) > 1, f'수치 미분: x=1 좌우 {float(dl):.4f}, {float(dr):.4f} / x=−2 좌우 {float(dl2):.3f}, {float(dr2):.3f}')
ans14 = pv14 + qv14
ans_ok(14, ans14)
w14a = -3 - f14.subs(x, 3)                    # 원문처럼 −p가 극점: p=−3
w14b = -2 - f14.subs(x, 2)                    # q=−f(−p)
w14c = 0 - f14.subs(x, 1)                     # 음수 조건 놓침 p=0
check(14, w14b == w14c == 16, 'q=−f(−p) 경로와 p=0 경로 모두 16')
wrong_in(14, [w14a, w14b], '원문식 −p=3 17 · q=−f(−p) 16')
# 원문 D25: −p가 극점, p>0 → p=1, q=7, p+q=8
fo25 = x**3 - 3 * x**2 - 9 * x - 12
so25 = [pv for pv in [R(i, 2) for i in range(1, 21)] if nondiff_count14(pv, fo25, 0) == 1]
check(14, so25 == [1] and 1 - fo25.subs(x, -1) == orig_ans('D25') == 8, f'원문 D25: 양수 p 격자 → {so25}, p+q={1 - fo25.subs(x, -1)} = 원문 답')
# 빼 보기
ablation(14, "'음수 p'", [ans14, w14c], ans14, 'p=0, q=16도 (가)(나) 만족')
cnt_all = sorted(set(pv - f14.subs(x, 1 - pv) for pv in pgrid if pv < 0 and nondiff_count14(pv) in (0, 2)))
ablation(14, "(나) '미분가능하지 않은 점 1개'", cnt_all[:6], ans14, 'p<0마다 q=−f(1−p)로 연속, p+q가 하나로 정해지지 않음')
ablation(14, "'연속인 함수'", None, ans14, undef='x=1에서 g를 정하는 식이 없어 q가 정해지지 않음(q=19이면 x=1에서 끊겨 (가)만으로는 g(1)을 정할 수 없음)')


# ================= 15번 (I65: f′(1)=f′(5)=0, 조각함수 g, 보기) =================
C = sp.symbols('C', real=True)
p = sp.symbols('p', positive=True)
f15 = x**3 - 9 * x**2 + 15 * x + C
check(15, sp.expand(sp.diff(f15, x) - 3 * (x - 1) * (x - 5)) == 0, "f′=3(x−1)(x−5)")


def g15(fx, pv):
    return (fx - fx.subs(x, 0), sp.expand(fx.subs(x, x + pv) - fx.subs(x, pv)))


def diffable15(fx, pv):
    L, Rr = g15(fx, pv)
    return sp.simplify(sp.diff(L, x).subs(x, 0) - sp.diff(Rr, x).subs(x, 0)) == 0


def integral15(fx, pv):
    L, Rr = g15(fx, pv)
    return sp.simplify(sp.integrate(L, (x, -1, 0)) + sp.integrate(Rr, (x, 0, 1)))


def judge15(fx, pos=True):
    """보기 ㄱ·ㄴ·ㄷ 판정 (pos=False면 p를 0 아닌 실수로)"""
    L2, R2 = g15(fx, 2)
    T1 = sp.simplify(sp.diff(R2, x).subs(x, 1) + 12) == 0
    ps = sp.symbols('ps', real=True)
    dset = [z for z in sp.solve(sp.Eq(sp.diff(fx, x).subs(x, 0), sp.diff(fx, x).subs(x, ps)), ps) if z.is_real and (z > 0 if pos else z != 0)]
    T2 = dset == [5]
    zs = [z for z in sp.solve(integral15(fx, ps), ps) if z.is_real and (z > 0 if pos else z != 0)]
    T3 = all(diffable15(fx, z) for z in zs) and len(zs) > 0
    return 'T:' + ', '.join(n for n, v in zip('ㄱㄴㄷ', (T1, T2, T3)) if v) if (T1 or T2 or T3) else 'T:(없음)', dset, zs


I15 = sp.factor(integral15(f15, p))
check(15, sp.simplify(I15 - (3 * p + 2) * (p - 6) / 2) == 0, f'∫₋₁¹g = {I15} = (3p+2)(p−6)/2 (C와 무관)')
check(15, sp.simplify(sp.diff(g15(f15, 2)[1], x).subs(x, 1)) == -12, "ㄱ: p=2이면 g′(1)=f′(3)=−12 (참)")
check(15, [pv for pv in range(1, 13) if diffable15(f15, pv)] == [6], 'ㄴ: 정수 p 1~12 중 미분가능한 것은 6뿐(거짓: 값은 5가 아님), 일반해 f′(p)=f′(0) ⇔ p=6')
L6, R6 = g15(f15, 6)
check(15, sp.expand(R6 + L6.subs(x, -x)) == 0, 'p=6이면 g는 원점 대칭(x>0 조각 = −(x≤0 조각)(−x))')
ans15, dset, zs = judge15(f15)
check(15, dset == [6] and zs == [6], f'미분가능한 양수 p {dset}, ∫=0인 양수 p {zs}')
ans_ok(15, ans15)
# 오답 경로: '미분가능 ⇔ p가 극점'으로 보면 p=5 → ㄴ 참, ∫=0인 p=6은 미분가능하지 않다고 보아 ㄷ 거짓 → ㄱ, ㄴ
check(15, sp.diff(f15, x).subs(x, 5) == 0 and integral15(f15, 5) != 0, '오답 경로 ②: p=5(극점)에서 ∫≠0이라 ㄷ 거짓으로 판정')
wrong_in(15, ['T:ㄱ, ㄴ', 'T:ㄱ, ㄴ, ㄷ'], 'p=5로 보아 ② · 원문 답 ⑤')
# 원문 I65: f′=3x(x−2) → ㄱ g′(1)=f′(2)=0, ㄴ 개수 1, ㄷ p≥2 → ∫≥0 → ⑤
fo65 = x**3 - 3 * x**2 + C
Io = sp.factor(integral15(fo65, p))
To1 = sp.diff(fo65, x).subs(x, 2) == 0
To2 = [pv for pv in [R(i, 4) for i in range(1, 41)] if diffable15(fo65, pv)] == [2]
To3 = sp.simplify(Io - (3 * p + 2) * (p - 2) / 2) == 0
check(15, To1 and To2 and To3 and orig_ans('I65') == 'T:ㄱ, ㄴ, ㄷ', f'원문 I65: ∫={Io}, ㄱㄴㄷ 모두 참 → 원문 답 {orig_ans("I65")}')
# 빼 보기
judges = set()
for aa in (R(1, 2), 2, -1):
    judges.add(judge15(aa * (x**3 - 9 * x**2 + 15 * x))[0])
ablation(15, "'최고차항의 계수가 1'", sorted(judges | {ans15}), ans15, '계수 a이면 g′(1)=−12a라 ㄱ의 참·거짓이 a에 따라 바뀜')
judges2 = set()
for fx in (x**3 - 3 * x**2, x**3 - 6 * x**2 + 5 * x, x**3 - 12 * x**2 + 21 * x, x**3 + 3 * x):
    judges2.add(judge15(fx)[0])
ablation(15, "'f′(1)=f′(5)=0'", sorted(judges2 | {ans15}), ans15, '다른 삼차함수(예: f′의 근 0·2, 1·7)에서는 보기 판정이 달라짐')
ansneg, _, zsneg = judge15(f15, pos=False)
check(15, sorted(zsneg) == [R(-2, 3), 6], f'p를 0 아닌 실수로 두면 ∫=0인 p = {sorted(zsneg)}')
ablation(15, "'양수 p'", [ansneg], ans15, 'p=−2/3에서도 ∫=0인데 미분가능하지 않아 ㄷ 거짓')


# ================= 16번 (I68: g=∫_{−x}^{kx}(f−|f|), 상자 (1,9), k의 최댓값) =================
# f=x⁴+ax²+b의 음수 영역(양의 쪽): 없음 / (0,β) (b≤0) / (α,β) (0<α<β). k>0이면 감소 집합 D=(α/k,β/k)∪(α,β), 나머지에서 g′=0.
def intervals16(k, al, be):
    return sorted([(al / k, be / k), (al, be)])


def union_cover(ivs):
    """열린구간들의 합집합을 (서로 떨어진) 열린구간 목록으로 (맞닿는 점은 g′=0인 한 점이라 감소가 이어짐)"""
    ivs = sorted(ivs); out = []
    for a_, b_ in ivs:
        if out and a_ <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b_))
        else:
            out.append((a_, b_))
    return out


def box16(k, al, be, s=1, e=9, use=('가', '나', '다')):
    """상자 조건 판정(k>0). 음수 영역이 없으면 g≡0."""
    if be is None:
        D = []
    else:
        D = union_cover(intervals16(k, al, be))
    res = True
    if '가' in use: res &= all(b_ <= 0 or a_ >= s for a_, b_ in D)                  # (0,s)와 D가 겹치지 않음
    if '나' in use: res &= any(a_ <= s and b_ >= e for a_, b_ in D)                  # (s,e) ⊂ D의 한 구간
    if '다' in use: res &= all(b_ <= e for a_, b_ in D)                               # (e,∞)와 겹치지 않음
    return res


def feasible_k(k, use=('가', '나', '다'), s=1, e=9):
    """k>0일 때 상자를 만족시키는 (α,β)가 있는가: 후보 α,β는 경계 s,e를 k배·1배한 값과 격자"""
    cand = sorted(set([R(0)] + [s, e, s * k, e * k, s / k, e / k] + [R(i, 2) for i in range(1, 41)]))
    for al in cand:
        for be in cand:
            if be > al >= 0 and box16(k, al, be, s, e, use):
                return (al, be)
    if box16(k, 0, None, s, e, use):
        return ('없음', None)
    return None


kgrid = sorted(set([R(i, 12) for i in range(1, 73)] + [R(1, 3), 3, R(301, 100), R(299, 100)]))   # 0<k≤6
feas = [kv for kv in kgrid if feasible_k(kv)]
check(16, feas == [kv for kv in kgrid if R(1, 3) <= kv <= 3], f'k 격자(1/12 간격 0<k≤6 + 경계 근처) 전수: 조건 만족 ⇔ 1/3≤k≤3 (최대 {max(feas)}, 최소 {min(feas)})')
check(16, feasible_k(3) == (3, 9) and not feasible_k(R(301, 100)), 'k=3이면 (α,β)=(3,9) 하나, k=3.01은 불가')
# k=3, f=(x²−9)(x²−81): g′ 부호 직접 확인
f16 = (x**2 - 9) * (x**2 - 81)
a16, b16 = sp.Poly(f16, x).all_coeffs()[2], sp.Poly(f16, x).all_coeffs()[4]
mf = lambda v: 2 * f16.subs(x, v) if f16.subs(x, v) < 0 else 0
gp = lambda xv, kv=3: kv * mf(kv * xv) + mf(-xv)
samp = [R(i, 8) for i in range(1, 97)]
check(16, all(gp(z) == 0 for z in samp if z < 1) and all(gp(z) < 0 for z in samp if 1 < z < 9 and z != 3) and gp(3) == 0 and all(gp(z) == 0 for z in samp if z > 9),
      f'k=3, f=x⁴{int(a16):+}x²{int(b16):+}: g′=0 (0<x<1, x>9), g′<0 (1<x<9, x≠3), g′(3)=0')
# 0 이하인 k(최댓값 3과는 무관, 확인만): 음수 k는 상자를 만족시키지 않고, k=0이면 (α,β)=(1,9)로 만족: g′(x)=k·m(kx)+m(−x), m(t)=2f(t)(f(t)<0), 0(그 밖) — 표본점 부호로 판정
def box_sample(kv, al, be):
    m = lambda v: (v * v - al * al) * (v * v - be * be) * 2 if (v * v - al * al) * (v * v - be * be) < 0 else 0
    gpv = lambda z: kv * m(kv * z) + m(-z)
    zs = [R(i, 16) for i in range(1, 16 * 14)]
    if any(gpv(z) != 0 for z in zs if z < 1) or any(gpv(z) != 0 for z in zs if z > 9): return False
    mid = [gpv(z) for z in zs if 1 < z < 9]
    return all(v <= 0 for v in mid) and sum(1 for v in mid if v == 0) <= 2
abl = [R(i, 2) for i in range(0, 25)]
negk = [kv for kv in (-3, -2, -1, -R(1, 2), -R(1, 3), 0) if any(box_sample(kv, al, be) for al in abl for be in abl if be > al)]
check(16, negk == [0] and box_sample(0, 1, 9) and box_sample(3, 3, 9), f'k≤0 표본(−3, −2, −1, −1/2, −1/3, 0) × (α,β) 격자(1/2 간격 0~12): 상자를 만족시키는 k = {negk}(k=0은 (α,β)=(1,9)), 모두 3보다 작음')
ans16 = max(feas)
ans_ok(16, ans16)
# 오답 경로: 이어짐 무시 → α=k<β=9 → 9 / 역할 뒤바꿈(α=1, β=9k, 9k≤9) → 1
noc = [kv for kv in kgrid if kv > 1 and kv < 9]                 # 이어짐을 안 보면 1<k<9 전부 되는 것처럼 보임
check(16, max(noc) < 9 and feasible_k(R(9, 2)) is None, '이어짐 무시: k<9로 보여 9를 고름(실제 k=9/2는 불가)')
check(16, feasible_k(1) and feasible_k(R(1, 2)), '역할 뒤바꿈 경로: k≤1 쪽(α=1, β=9k)만 보면 최댓값 1')
wrong_in(16, [9, 1], '이어짐 놓침 9 · 느린 끝으로 시작 1')
# 원문 I68: [−x,2x], (1,5) → α=2, β=5, f(√2)=46
fo68 = (x**2 - 4) * (x**2 - 25)
check(16, feasible_k(2, s=1, e=5) == (2, 5) and fo68.subs(x, sp.sqrt(2)) == orig_ans('I68') == 46, f'원문 I68: k=2, 상자 (1,5) → (α,β)=(2,5), f(√2)={fo68.subs(x, sp.sqrt(2))} = 원문 답')
# 빼 보기 (각 조건을 빼고 같은 k 격자에서 가능한 k의 최댓값; 격자 끝 6까지 되면 최댓값 없음)
for lab, use in (('(가)', ('나', '다')), ('(나)', ('가', '다')), ('(다)', ('가', '나'))):
    fk = [kv for kv in kgrid if feasible_k(kv, use)]
    if fk and max(fk) == max(kgrid):
        ablation(16, f"{lab}", None, ans16, undef=f'격자 끝 k={max(kgrid)}까지 모두 가능 → 최댓값 없음')
    else:
        ablation(16, f"{lab}", [max(fk)] if fk else [], ans16)
print('ABLATION 16 원문 단서 \'(단, a, b는 상수이다.)\': 원문 그대로 둠(조건 아닌 표기). \'양수 k\'는 최댓값에 일하지 않아 \'실수 k\'로 씀(note)')

print()
print('ALL OK' if ok else 'SOME FAIL')
