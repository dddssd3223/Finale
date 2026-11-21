# -*- coding: utf-8 -*-
# 7회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 1, 14: 5, 15: 3, 16: 2}          # 분담표 목표 13①·14⑤·15③·16②
DBREF = {13: 'M33 후보_순위 3', 14: 'M1 v3_추가 2', 15: 'J64 후보_순위 3', 16: 'I73 후보_순위 3'}
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


def ans_ok(no, val, integer=True):
    v = ch(no)
    if not IT[no]['choices'][0].startswith('T:'):
        d = {v[i + 1] - v[i] for i in range(4)}
        check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
        if integer:
            check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
        else:
            print(f'[{no}] 참고 정답 {val}: 분수(원문 답·선지도 분수, note에 이유)')
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


# ================= 13번 (M33: 오른쪽 조각 m − q·f(x), S = 미분가능하게 하는 k의 집합) =================
def S_set(a, b, c, m=8, q=3):
    """g=f (x<c), m−q·f (x≥c)에 대하여 S를 정확히 구한다. g의 치역은 실수 전체(x→−∞에서 +∞, x→+∞에서 −∞)라
    k∈S ⇔ g(x)=k인 모든 x에서 g가 미분가능하고 g'(x)=0. 후보 k는 기울기가 0인 점(이음점 포함)의 함숫값뿐이다."""
    f = x**4 + a * x**3 + b
    fp = sp.diff(f, x)
    L, Rr = fp.subs(x, c), -q * fp.subs(x, c)
    pieces = [(f, fp, lambda r: r < c), (m - q * f, -q * fp, lambda r: r > c)]
    cand = {m - q * f.subs(x, c)}
    for g_, gp_, dom in pieces:
        for r in sp.Poly(gp_, x).real_roots():
            if dom(r): cand.add(sp.together(g_.subs(x, r)))
    S = set()
    for k in cand:
        good = True
        if m - q * f.subs(x, c) == k:
            good &= (L == 0 and Rr == 0)
        elif L != Rr:
            good = False                      # g가 x=c에서 꺾이고 g(c)≠k → |g−k|도 x=c에서 꺾임
        for g_, gp_, dom in pieces:
            for r in set(sp.Poly(g_ - k, x).real_roots()):
                if dom(r) and abs(sp.N(gp_.subs(x, r), 30)) > 1e-12: good = False
        if good: S.add(k)
    return S


def b_cont(a, c, m=8, q=3):
    return R(m, 1 + q) - c**4 - a * c**3      # 연속: f(c)=m−q·f(c)


# f'(c)≠0이면 S=∅ (격자), f'(c)=0이면 S={b, 2}
emp = all(S_set(a, b_cont(a, c), c) == set() for c in (1, 2, 3) for a in (-5, -4, -3, -2, -1, 0, 1, 2) if 4 * c + 3 * a != 0)
check(13, emp, "f'(c)≠0인 (a, c) 격자 24−α개 전부 S=∅")
sols = []
for i in range(1, 41):                         # c∈(0, 5] 격자(1/8 간격), a=−4c/3
    c = R(i, 8); a = -R(4, 3) * c; b = b_cont(a, c)
    S = S_set(a, b, c)
    if len(S) != 2 or S != {b, 2}: check(13, False, f'c={c}: S={S}')
    if len(S) == 2 and sum(S) == 31: sols.append((a, b, c))
check(13, sols == [(-4, 29, 3)], f'S의 원소 2개·합 31 → (a, b, c)={sols} (c 격자 전수, 일반식 b+2=4+c⁴/3=31에서 c=3뿐)')
cc = sp.symbols('c', positive=True)
check(13, sp.solve(sp.Eq(4 + cc**4 / 3, 31), cc) == [3], '4+c⁴/3=31의 양수 해 c=3 하나')
f13 = x**4 - 4 * x**3 + 29
check(13, f13.subs(x, 3) == 2 and sp.diff(f13, x).subs(x, 3) == 0 and S_set(-4, 29, 3) == {29, 2}, f'f={f13}: f(3)=2, f′(3)=0, S={S_set(-4, 29, 3)}')
ans13 = f13.subs(x, 1)
ans_ok(13, ans13)
wrong_in(13, [1 + 4 + 29, 1 + 29], 'a 부호 실수(a=4) 34 · ax³ 항 누락 30')
# 원문 M33: 8−f, 합 25/3 → f(2)=29/3
so = [(a, b, c) for c in (R(1, 2), 1, R(3, 2), 2) for a in [-R(4, 3) * c] for b in [b_cont(a, c, 8, 1)] if sum(S_set(a, b, c, 8, 1)) == R(25, 3) and len(S_set(a, b, c, 8, 1)) == 2]
check(13, len(so) == 1 and (x**4 + so[0][0] * x**3 + so[0][1]).subs(x, 2) == orig_ans('M33') == R(29, 3), f'원문 M33: (a, b, c)={so}, f(2)={orig_ans("M33")}')
# 빼 보기
ablation(13, "'모든 원소의 합은 31'", {(x**4 - R(4, 3) * c * x**3 + b_cont(-R(4, 3) * c, c)).subs(x, 1) for c in (1, 2, 3)}, 26, 'c가 정해지지 않음')
ablation(13, "'8−3f(x)'의 계수 3(→ 원문 8−f(x))", [] if not [c for c in [R(i, 8) for i in range(1, 41)] if 8 + c**4 / 3 == 31] else [0], 26, '8−f이면 S={b, 4}, 4+4+c⁴/3=31에서 c⁴=69라 값이 달라짐')
c69 = sp.root(69, 4); f69 = x**4 - R(4, 3) * c69 * x**3 + 27
print(f'      (계수 3을 빼면 f(1)={sp.nsimplify(f69.subs(x, 1))} ≈ {sp.N(f69.subs(x, 1), 5)} ≠ 26)')
print("ABLATION 13 '원소의 개수는 2': 군더더기(답 그대로; 합 조건이 있으면 S≠∅이라 따라 나옴 — 원문 M33도 같음, 원문 상자 문장이라 그대로 둠)")


# ================= 14번 (M1: 일반 계수 + 두 상수 사이 양끝 접합) =================
a_, b_, c_, d_, k_ = sp.symbols('a b c d k', real=True)
f14 = a_ * x**3 + b_ * x**2 + c_ * x + d_
sol14 = sp.solve([f14.subs(x, 0) - R(1, 2), sp.diff(f14, x).subs(x, 0), f14.subs(x, 2) - k_, sp.diff(f14, x).subs(x, 2)], [b_, c_, d_, k_], dict=True)[0]
check(14, sol14 == {b_: -3 * a_, c_: 0, d_: R(1, 2), k_: R(1, 2) - 4 * a_}, f'미분가능 → {sol14}')
ff = f14.subs(sol14)
check(14, sp.factor(sp.diff(ff, x)) == 3 * a_ * x * (x - 2), "f'(x)=3ax(x−2): 0<x<2에서 부호 일정 → 구간에서 f는 1/2과 k 사이")


def gmin(av):
    """g의 최솟값(a=av): x<0에서 1/2, [0, 2]에서 f, x>2에서 k"""
    fv = ff.subs(a_, av)
    return min([R(1, 2), fv.subs(x, 2)] + [fv.subs(x, R(i, 20)) for i in range(41)])


grid = [R(i, 16) for i in range(-48, 49) if i != 0]
check(14, all((gmin(av) < R(1, 2)) == (av > 0) for av in grid), '격자 전수: 최솟값<1/2 ⇔ a>0 (a<0이면 최솟값이 정확히 1/2)')
T1 = True                                                             # ㄱ: g(0)=1/2, g'(0)=0
T2 = all(sol14[b_].subs(a_, av) < 0 for av in grid if av > 0)          # ㄴ: b=−3a<0
a0 = sp.solve(sp.Eq(R(1, 2) - 4 * a_, 0), a_)
T3 = a0 == [R(1, 8)] and gmin(R(1, 8)) == 0 and ff.subs({a_: R(1, 8), x: 1}) == R(1, 4)   # ㄷ
check(14, T1 and T2 and T3, f'ㄱ 참, ㄴ 참(b=−3a<0), ㄷ 참(a={a0}, g(1)={ff.subs({a_: R(1, 8), x: 1})})')
ans14 = 'T:' + ', '.join(n for n, v in zip('ㄱㄴㄷ', (T1, T2, T3)) if v)
ans_ok(14, ans14)
wrong_in(14, ['T:ㄱ, ㄴ', 'T:ㄱ, ㄷ'], 'ㄷ 계산 실수 → ㄱ, ㄴ · a의 부호를 정하지 못해 ㄴ 거짓 → ㄱ, ㄷ')
# 원문 M1: f=x³+ax²+1/2 (a<0), ㄱ 참, ㄴ g(1)=3/2+a<3/2 참, ㄷ 극솟값 4a³/27+1/2=0 → a=−3/2, g(2)=5/2 참
fo = x**3 + a_ * x**2 + R(1, 2)
ao = [r for r in sp.solve(sp.Eq(fo.subs(x, -2 * a_ / 3), 0), a_) if r.is_real]
check(14, ao == [-R(3, 2)] and fo.subs({a_: ao[0], x: 2}) == R(5, 2) and orig_ans('M1') == 'T:ㄱ, ㄴ, ㄷ', f'원문 M1: a={ao}, g(2)=5/2, 원문 답 {orig_ans("M1")}')
# 빼 보기
print("ABLATION 14 '최솟값이 1/2보다 작을 때': 필요(a<0도 남아 b=−3a>0이 되므로 ㄴ의 참·거짓이 정해지지 않음)")
ok &= any(sol14[b_].subs(a_, av) > 0 for av in grid)
fr = f14.subs({c_: 0, d_: R(1, 2)})      # x=2 접합을 빼면 b가 자유
print(f"ABLATION 14 'x>2에서 상수 k(x=2에서 미분가능)': 필요(b가 a와 무관해져 ㄴ·ㄷ이 정해지지 않음: f={fr})")
print("ABLATION 14 'x=0에서 미분가능': 필요(c, d가 정해지지 않아 ㄱ g(0)+g′(0)=d+c가 1/2로 정해지지 않음)")


# ================= 15번 (J64: 두 곡선 + 넓이의 차 9) =================
kk = sp.symbols('k', real=True)
f15 = 4 * x**2 - 17 * x + 14
g15 = -2 * x**2 + 9 * x - 6
d15 = sp.expand(f15 - g15)
check(15, sp.expand(d15 - 2 * (x - 1) * (3 * x - 10)) == 0 and f15.subs(x, 1) == g15.subs(x, 1), f'f−g={sp.factor(d15)}: 교점 x=1, 10/3')
G15 = sp.integrate(d15, (x, 0, kk))
rts = sp.roots(sp.Poly(G15 - 9, kk))
check(15, sp.factor(G15 - 9) == (kk - 1)**2 * (2 * kk - 9) and [r for r in rts if r > R(10, 3)] == [R(9, 2)], f'∫₀ᵏ(f−g)=9: {sp.factor(G15 - 9)}=0, k>10/3인 해 {[r for r in rts if r > R(10, 3)]}')
A15 = sp.integrate(d15, (x, 0, 1)); B15 = -sp.integrate(d15, (x, 1, R(10, 3))); C15 = sp.integrate(d15, (x, R(10, 3), R(9, 2)))
check(15, A15 > 0 and B15 > 0 and C15 > 0 and A15 + C15 == B15 + 9, f'넓이 직접 계산: A={A15}, B={B15}, C={C15}, A+C−B={A15 + C15 - B15}')
check(15, sp.diff(G15, kk).subs(kk, 4) > 0 and all(sp.diff(G15, kk).subs(kk, R(10, 3) + R(i, 10)) > 0 for i in range(1, 40)), 'k>10/3에서 ∫₀ᵏ(f−g)는 증가 → 해 하나')
ans15 = R(9, 2)
ans_ok(15, ans15, integer=False)
w1 = [r for r in sp.roots(sp.Poly(G15, kk)) if r > R(10, 3)]
w2 = [r for r in sp.roots(sp.Poly(sp.cancel(G15 / kk) - 9, kk)) if r > R(10, 3)]
check(15, w1 == [4] and w2 == [R(11, 2)], f'오답 경로: ∫₀ᵏ=0 → {w1}, k 약분 2k²−13k+20=9 → {w2}')
wrong_in(15, w1 + w2, '원문 방식(+9 놓침) 4 · k 약분 11/2')
# 원문 J64: ∫₀ᵏ(3x²−7x+2−x/3+2/3)dx=0, k>2 → 8/3
Go = sp.integrate(3 * x**2 - 7 * x + 2 - (x / 3 - R(2, 3)), (x, 0, kk))
ko = [r for r in sp.solve(Go, kk) if r > 2]
check(15, ko == [orig_ans('J64')], f'원문 J64: k={ko}, 원문 답 {orig_ans("J64")}')
# 빼 보기
ablation(15, "'+9'", w1, ans15, '(A)+(C)=(B)이면 k=4')
ablation(15, "단서 'k>10/3'", [r for r in rts if r > 0], ans15, 'k=1도 ∫₀ᵏ(f−g)=9를 만족(이때는 A만 있어 영역 C가 없음)')
ablation(15, "'y축으로 둘러싸인 영역 A'(A 없이 C=B+9)", [sp.N(r, 6) for r in sp.Poly(G15 - A15 - 9, kk).real_roots() if r > R(10, 3)], ans15, '적분 구간의 시작이 달라짐')


# ================= 16번 (I73: 삼차 조각이 왼쪽, 일차 조각 3x−4k, g(4)=0, g(k−1)의 최댓값) =================
p_ = sp.symbols('p', real=True)
# k 결정: 4>k이면 12−4k=0 → k=3. 4≤k이면 g(4)≤g(k)=−k≤−4<0이라 불가
kc = [kv for kv in sp.solve(sp.Eq(12 - 4 * kk, 0), kk) if kv < 4]
check(16, kc == [3], f'g(4)=0: 일차 조각(4>k)에서 k={kc}, 삼차 조각(k≥4)에서는 g(4)≤g(k)=−k≤−4라 불가')
u = x - 3
f16 = u**3 + p_ * u**2 + 3 * u - 3
check(16, f16.subs(x, 3) == -3 and sp.diff(f16, x).subs(x, 3) == 3 and sp.Poly(f16, x).LC() == 1, 'f(3)=−3, f′(3)=3, 최고차항 1 → f=(x−3)³+p(x−3)²+3(x−3)−3')


def inc16(pv):
    """x<3에서 f'≥0 (정확히: f'의 x≤3에서의 최솟값 ≥ 0)"""
    fp = sp.diff(f16.subs(p_, pv), x)
    v = sp.solve(sp.diff(fp, x), x)[0]
    return (fp.subs(x, v) if v < 3 else fp.subs(x, 3)) >= 0


pg = [R(i, 8) for i in range(-80, 81)]
okp = [pv for pv in pg if inc16(pv)]
check(16, okp == [pv for pv in pg if pv <= 3], f'p 격자 전수(−10~10, 1/8 간격): 증가 ⇔ p≤3 (최대 {max(okp)})')
val16 = sp.expand(f16.subs(x, 2))
check(16, val16 == p_ - 7, f'g(k−1)=f(2)={val16}')
ans16 = max(val16.subs(p_, pv) for pv in okp)
f3 = sp.expand(f16.subs(p_, 3))
check(16, sp.factor(sp.diff(f3, x)) == 3 * (x - 2)**2, f"p=3: f′={sp.factor(sp.diff(f3, x))}≥0 (x=2에서만 0) → 증가, 최댓값 달성")
ans_ok(16, ans16)
wrong_in(16, [val16.subs(p_, 0), f16.subs({p_: 0, x: 3})], 'p≤0만 생각 −7 · 이음점 값 g(k)=−3')
# 원문 I73 (학교식_예상 1 수치 확인 겸): 2x−k, x>k 삼차, k=2, f=u³+pu²+2u+2, u>0에서 f′≥0 ⇔ p≥−√6 → 5−√6
po = sp.solve(sp.Eq(sp.discriminant(3 * t**2 + 2 * p_ * t + 2, t), 0), p_)
check(16, min(po) == -sp.sqrt(6) and F.I['I73'][1]['①②③④⑤'.index(F.I['I73'][2])] == '5-\\sqrt6', f'원문 I73: p≥{min(po)}, g(k+1)=5+p의 최솟값 5−√6 = 원문 답')
# 빼 보기
ablation(16, "(가) '증가'", [val16.subs(p_, pv) for pv in (3, 5, 10)], ans16, 'p에 제한이 없어 최댓값이 없음')
ablation(16, "(가) '미분가능'", [(u**3 + pv * u**2 + s * u - 3).subs(x, 2) for pv, s in ((3, 3), (0, 0), (2, 1))], ans16, "f′(3)이 정해지지 않아 증가 조건이 달라짐(예: f′(3)=0이면 p≤0)")
ablation(16, "(나) 'g(4)=0'", [-kv + 3 - 4 for kv in (1, 2, 3)], ans16, 'k가 정해지지 않음: g(k−1)의 최댓값은 −k−1')
ablation(16, "'3x−4k'의 계수 4(→ 3x−k)", None, ans16, undef='g(k)=2k>0이 되어 g(4)=0인 점이 삼차 조각에 올 수 있고(k≥4) k가 정해지지 않음')

print('ALL OK' if ok else 'SOME FAIL')
