# -*- coding: utf-8 -*-
# 11회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import numpy as np
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 4, 14: 2, 15: 5, 16: 3}          # 분담표 목표 13④·14②·15⑤·16③ 그대로
DBREF = {13: 'J40 결합 1', 14: 'J19 후보_순위 3', 15: 'J65 v3_추가 2', 16: 'M61 결합 1'}   # 분담표 그대로
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 계수 13●·14●·15○·16●
BOX = {13: False, 14: False, 15: False, 16: False}       # 13·16 '원문대로'(원문에 상자 없음), 14·15 ×
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


# ================= 13번 (J40: P는 A(k), Q는 B(2k), v₁=3t²−14t+5, v₂=−2t−k, 한 번만 만나는 최소 k에서 거리 감소 동안 Q가 움직인 거리) =================
def D13(k, p1=(-14, 5), q1=(-2, None)):
    """위치 차 x_P−x_Q (기본: 본문 수치, v₂의 상수항은 −k)"""
    v1 = 3 * t**2 + p1[0] * t + p1[1]
    v2 = q1[0] * t + (-k if q1[1] is None else q1[1])
    return sp.expand(k + sp.integrate(v1, (t, 0, t)) - (2 * k + sp.integrate(v2, (t, 0, t))))


def meets13(k, **kw):
    """출발 후(t>0) 만나는 서로 다른 시각의 개수"""
    return len({r for r in sp.Poly(D13(k, **kw), t).real_roots() if r > 0})


def dec_set13(k):
    """t>0에서 거리 |D|가 감소하는 구간들: D·D′<0 (근과 D′의 근으로 나눈 구간마다 판정)"""
    D = D13(k); Dp = sp.diff(D, t)
    cuts = sorted({0} | {r for r in sp.Poly(D, t).real_roots() if r > 0} | {r for r in sp.Poly(Dp, t).real_roots() if r > 0})
    cuts.append(cuts[-1] + 10)
    out = []
    for lo, hi in zip(cuts, cuts[1:]):
        m = (lo + hi) / 2
        if (D * Dp).subs(t, m) < 0:
            out.append((lo, hi))
    return out


check(13, sp.factor(D13(k)) == sp.factor((t - 1) * (t**2 - 5 * t + k)), f'위치 차 = {sp.factor(D13(k))} (인수 t−1 유지)')
mk = {kk: meets13(kk) for kk in range(1, 201)}
k13 = min(kk for kk in mk if mk[kk] == 1)
check(13, k13 == 7 and all(mk[kk] == 1 for kk in range(7, 201)) and mk[4] == 2 and mk[6] == 3, f'자연수 k=1~200 전수: 한 번만 만나는 k의 최솟값 {k13} (k=4: {mk[4]}번, k=6: {mk[6]}번)')
ds = dec_set13(k13)
check(13, ds == [(0, 1)], f'k=7: 거리가 감소하는 구간 {ds} (위치 차의 도함수 {sp.factor(sp.diff(D13(7), t))})')
v2_13 = -2 * t - k13
ans13 = sum(sp.integrate(sp.Abs(v2_13), (t, lo, hi)) for lo, hi in ds)
check(13, ans13 == 8, f'Q가 움직인 거리 {ans13}')
ans_ok(13, ans13)
w13a = sp.integrate(2 * t + 5, (t, 0, 1))      # 원문 답 k=5 기억
w13b = sp.Integer(k13)                         # k값 그대로 / 2t 빠뜨림
wrong_in(13, [w13a, w13b], '원문 답 k=5 → 6 · k=7 그대로(또는 ∫7dt) → 7')
# 원문 J40: v₁=3t²−12t+k, v₂=−2t−4 → k의 최솟값 5
def Do13(k):
    return sp.expand(k + sp.integrate(3 * t**2 - 12 * t + k, (t, 0, t)) - (2 * k + sp.integrate(-2 * t - 4, (t, 0, t))))
ko = min(kk for kk in range(1, 50) if len({r for r in sp.Poly(Do13(kk), t).real_roots() if r > 0}) == 1)
check(13, ko == orig_ans('J40') == 5, f'원문 J40 k의 최솟값 {ko} = 원문 답')
check(13, all(sp.integrate(2 * t + 4, (t, 0, 1)) == 5 for _ in [0]), 'DB 스케치(원문 수치) 그대로면 Q의 거리는 k와 무관하게 5 → 매개변수 자리를 옮긴 이유')
# 빼 보기
ablation(13, "'한 번만 만나도록 하는 k의 값이 최소'", [1 + kk for kk in range(7, 12)], ans13, 'k가 정해지지 않아 Q의 거리 1+k가 여럿')
ablation(13, "'자연수 k'", None, ans13, undef='k>25/4인 실수에서 최솟값이 없음(k=25/4이면 t=1, 5/2 두 번 만남)')
check(13, meets13(sp.Rational(25, 4)) == 2, 'k=25/4는 두 번 만남(자연수 조건의 근거)')
ablation(13, "'거리가 감소하는 동안'(→ 만날 때까지가 아닌 출발 후 t=2까지 등)", [ans13, sp.integrate(2 * t + 7, (t, 0, 2))], ans13, '구간이 바뀌면 거리가 바뀜')


# ================= 14번 (J19: f=x³−3x²+3x+3과 y=mx로 둘러싸인 두 부분의 넓이가 같을 때 넓이의 합) =================
f14 = x**3 - 3 * x**2 + 3 * x + 3
check(14, sp.expand((x - 1)**3 + 4 - f14) == 0, 'f(x)=(x−1)³+4 (대칭점 (1,4))')


def parts14(m):
    """세 교점이면 (두 부분 넓이) 아니면 None"""
    rs = sorted(set(sp.Poly(f14 - m * x, x).real_roots()))
    if len(rs) != 3:
        return None
    a_, b_, c_ = [sp.nsimplify(r) if r.is_rational else r for r in rs]
    I1 = sp.integrate(f14 - m * x, (x, rs[0], rs[1])); I2 = sp.integrate(f14 - m * x, (x, rs[1], rs[2]))
    return abs(sp.N(I1, 30)), abs(sp.N(I2, 30))


eqm = []
for i in range(-40, 241):
    m = R(i, 10)
    pr = parts14(m)
    if pr and abs(pr[0] - pr[1]) < 1e-20:
        eqm.append(m)
check(14, eqm == [4], f'm=-4~24(0.1 간격) 전수: 세 점에서 만나고 두 넓이가 같은 m = {eqm}')
mm = sp.symbols('mm', real=True)
gap = sp.Poly(f14 - mm * x, x)
check(14, sp.factor(f14 - 4 * x) == (x - 3) * (x - 1) * (x + 1), f'm=4: f−4x = {sp.factor(f14 - 4 * x)}')
P1 = sp.integrate(f14 - 4 * x, (x, -1, 1)); P2 = -sp.integrate(f14 - 4 * x, (x, 1, 3))
ans14 = P1 + P2
check(14, P1 == P2 == 4 and ans14 == 8, f'두 부분 {P1}, {P2}, 합 {ans14}')
ans_ok(14, ans14)
wrong_in(14, [P1, 2 * ans14], '한 부분만 4 · 원문처럼 2배 16')
o19 = 4 * sp.integrate(x - x**3 / 4, (x, 0, 2))
check(14, o19 == orig_ans('J19') == 4, f'원문 J19: 4∫₀²(x−x³/4)dx = {o19} = 원문 답')
pr1, pr2 = parts14(5), parts14(7)
ablation(14, "'두 부분의 넓이가 서로 같다'", [sp.Float(pr1[0] + pr1[1], 8), sp.Float(pr2[0] + pr2[1], 8)], ans14, 'm이 정해지지 않음(m=5, 7 예)')


# ================= 15번 (J65: f=±x³−6x²(y축 대칭), 기준선 y=50, A=2B인 k) =================
c15 = 50
fr = x**3 - 6 * x**2                       # x≥0
fl = -x**3 - 6 * x**2                      # x<0
check(15, sp.expand(fl.subs(x, -x) - fr) == 0, 'y축 대칭(f(−x)=f(x))')
qs = [r for r in sp.Poly(fr - c15, x).real_roots() if r > 0]
check(15, len(qs) == 1 and 7 < qs[0] < 8, f'Q의 x좌표 q 하나, 약 {sp.N(qs[0], 6)} (7과 8 사이)')
q15 = qs[0]
xs = np.linspace(-float(q15) + 1e-6, float(q15) - 1e-6, 2001)
check(15, all(-(abs(z))**3 * 0 + (abs(z)**3 - 6 * z**2) < c15 for z in xs), '−q<x<q에서 f<50 (A는 한 덩어리)')
qn = sp.N(q15, 40)
A15 = 2 * sp.integrate(c15 - fr, (x, 0, qn))


def B15(kk):
    return sp.integrate(fr - c15, (x, qn, kk))


G = sp.integrate(fr - c15, (x, 0, k))
check(15, sp.factor(G) == sp.factor(k * (k - 10) * (k**2 + 2 * k + 20) / 4), f'∫₀^k(f−50) = {sp.factor(G)}')
sols15 = [r for r in sp.Poly(sp.expand(4 * G), k).real_roots() if r > qn]
ans15 = sols15[0]
check(15, sols15 == [10] and abs(A15 - 2 * B15(10)) < 1e-25, f'k>q에서 A=2B의 해 {sols15} (A={sp.N(A15, 8)}, 2B={sp.N(2 * B15(10), 8)})')
# k>q 구간 전수(수치): A−2B 부호가 바뀌는 곳은 10 하나
grid = [qn + R(i, 4) for i in range(1, 80)]
sg = [sp.sign(A15 - 2 * B15(z)) for z in grid]
check(15, sum(1 for i in range(len(sg) - 1) if sg[i] != sg[i + 1]) == 1, 'k∈(q, q+20) 수치 격자: A−2B 부호 바뀜 1번(유일)')
ans_ok(15, ans15)
w15a = [r for r in sp.Poly(sp.expand(sp.integrate(fr, (x, 0, k))), k).real_roots() if r > 0][0]   # 기준선 무시
w15b = orig_ans('J65')
wrong_in(15, [w15a, w15b], '기준선을 x축으로 둔 ∫₀^k(x³−6x²)=0 → 8 · 원문 답 6')
check(15, w15a > qn, f'오답 8은 단서(R이 Q보다 오른쪽)로 지워지지 않음(q≈{sp.N(qn, 5)})')
# 원문 J65
fo = -x**2 + 2 * x + 6
ko15 = [r for r in sp.solve(sp.integrate(fo, (x, 0, k)), k) if r > 4]
check(15, ko15 == [orig_ans('J65')] == [6], f'원문 J65: ∫₀^k f=0, k>4 → {ko15} = 원문 답')
# 빼 보기: 'R이 Q보다 오른쪽' 단서가 없으면 0<k<q(R이 선분 PQ 위)도 가능: B=∫_k^q(50−f) = A/2 ⇔ k=0
Bin = sp.integrate(c15 - fr, (x, 0, qn))
ablation(15, "'점 Q의 x좌표보다 큰 (상수 k)'", [0, ans15], ans15, 'k=0이면 R이 선분 PQ 위에 있고 B=A/2')
check(15, abs(A15 - 2 * Bin) < 1e-25, 'k=0일 때 B(=곡선과 선분 QR, 직선 x=0으로 둘러싸인 부분)=A/2 확인')
ablation(15, "기준선 직선 y=50(→ 원문처럼 x축)", [w15a], ans15, '장치가 답을 바꿈')
ablation(15, "'점 P의 x좌표는 음수'", [0], ans15, 'Q가 왼쪽 점 (−q, 50)이면 k=0일 때 B(왼쪽 절반)=A/2')


# ================= 16번 (M61: (f∘f)(x)=x의 모든 실근 0,2,a,3,b, 두 부분 넓이 같음, f(−1)) =================
a_, b_, K_ = sp.symbols('a_ b_ K_')
LAB = [('0', sp.Integer(0)), ('2', sp.Integer(2)), ('a', a_), ('3', sp.Integer(3)), ('b', b_)]


def solve16(pos=True, order=True, area=True, exact_set=True):
    """짝 10가지 × (넓이 조건이면 가운데 고정점 3가지) 전수. 조건을 만족시키는 (a, b, K, f(−1)) 목록"""
    out = set()
    for i in range(5):
        for j in range(i + 1, 5):
            Fx = [LAB[z][1] for z in range(5) if z not in (i, j)]
            p_, q_ = LAB[i][1], LAB[j][1]
            ff = x + K_ * (x - Fx[0]) * (x - Fx[1]) * (x - Fx[2])
            base = [sp.Eq(ff.subs(x, p_), q_), sp.Eq(ff.subs(x, q_), p_)]
            mids = [None] if not area else [0, 1, 2]
            for mi in mids:
                eqs = list(base)
                if mi is not None:
                    o = [Fx[z] for z in range(3) if z != mi]
                    eqs.append(sp.Eq(2 * Fx[mi], o[0] + o[1]))
                unk = [s for s in (a_, b_, K_) if any(e.has(s) for e in eqs)]
                if not area:
                    continue
                for s in sp.solve(eqs, unk, dict=True):
                    if len(s) < len(unk) or not all(v.is_real for v in s.values()):
                        continue
                    A, B, KK = s.get(a_, a_), s.get(b_, b_), s[K_]
                    if A.free_symbols or B.free_symbols or KK == 0:
                        continue
                    vals = [0, 2, A, 3, B]
                    if len(set(vals)) != 5:
                        continue
                    if pos and not KK > 0:
                        continue
                    if order and not (2 < A < 3 < B):
                        continue
                    F_ = ff.subs(s)
                    fv = sorted([sp.nsimplify(v.subs(s)) for v in Fx], key=lambda v: float(sp.N(v)))
                    if sp.simplify(2 * fv[1] - fv[0] - fv[2]) != 0:       # 실제 가운데 고정점이 중점인지
                        continue
                    if exact_set:
                        P9 = sp.Poly(sp.expand(F_.subs(x, F_) - x), x)
                        rr = sorted({round(float(sp.re(z)), 9) for z in P9.nroots(n=30, maxsteps=200) if abs(sp.im(z)) < 1e-12})
                        if rr != sorted(round(float(sp.N(v)), 9) for v in vals):
                            continue
                    out.add((A, B, KK, sp.nsimplify(F_.subs(x, -1))))
    return sorted(out, key=str)


S16 = solve16()
check(16, len(S16) == 1, f'짝 10가지 × 가운데 고정점 3가지 전수: 해 {S16}')
A16, B16, K16, ans16 = S16[0]
check(16, (A16, B16, K16) == (R(5, 2), 5, R(1, 3)), f'a={A16}, b={B16}, 최고차항의 계수 {K16}')
f16 = x + K16 * x * (x - A16) * (x - B16)
rr16 = sorted(set(sp.Poly(sp.expand(f16.subs(x, f16) - x), x).real_roots()))
check(16, rr16 == [0, 2, R(5, 2), 3, 5] and f16.subs(x, 2) == 3 and f16.subs(x, 3) == 2, f'(f∘f)(x)=x의 실근 {rr16}, f(2)=3, f(3)=2')
I1 = sp.integrate(f16 - x, (x, 0, A16)); I2 = sp.integrate(f16 - x, (x, A16, B16))
check(16, I1 == -I2 and I1 != 0, f'두 부분 넓이 {abs(I1)}, {abs(I2)} 같음')
ans_ok(16, ans16)
w16a = sp.nsimplify((f16 - x).subs(x, -1))       # +x 누락
w16b = sp.nsimplify(1 + (f16 - x).subs(x, -1))   # 앞의 x에 1을 넣음
wrong_in(16, [w16a, w16b], '+x 누락 −7 · 앞 x 부호 실수 −6')
fo16 = x + x * (x - R(3, 2)) * (x - 3)
check(16, fo16.subs(x, 5) == orig_ans('M61') == 40 and sp.diff(fo16, x).subs(x, 0) - sp.diff(fo16, x).subs(x, 1) == 6, '원문 M61: f=x+x(x−3/2)(x−3), f′(0)−f′(1)=6, f(5)=40 = 원문 답')
# 두 근 a=5/2, 7/5 확인
aa = sp.symbols('aa')
check(16, sp.factor(sp.expand(2 * (2 - aa) * (2 - 2 * aa) + 3 * (3 - aa) * (3 - 2 * aa))) == sp.factor(10 * aa**2 - 39 * aa + 35), '1=2k(2−a)(2−2a), −1=3k(3−a)(3−2a) → 10a²−39a+35=0')
# 빼 보기
S_no_order = solve16(order=False)
ablation(16, "단서 '2<a<3<b'", [s[3] for s in S_no_order], ans16, f'해 {[(str(s[0]), str(s[1]), str(s[2])) for s in S_no_order]}')
S_no_pos = solve16(pos=False)
ablation(16, "'최고차항의 계수가 양수'", [s[3] for s in S_no_pos], ans16, f'해 {[(str(s[0]), str(s[1]), str(s[2])) for s in S_no_pos]}')
# 넓이 조건 없이: a를 정하면 b, k가 정해지는 한 매개변수 꼴(예: 고정점 0, a, b, 짝 2↔3)
def fam16(aval):
    s = sp.solve([sp.Eq(2 + K_ * 2 * (2 - aval) * (2 - b_), 3), sp.Eq(3 + K_ * 3 * (3 - aval) * (3 - b_), 2)], [b_, K_], dict=True)
    return [(sp.nsimplify(z[b_]), z[K_]) for z in s if z[K_] > 0 and z[b_] > 3]
fa, fb = fam16(R(9, 4)), fam16(R(11, 4))
va = [sp.nsimplify((x + K * x * (x - R(9, 4)) * (x - B)).subs(x, -1)) for B, K in fa]
vb = [sp.nsimplify((x + K * x * (x - R(11, 4)) * (x - B)).subs(x, -1)) for B, K in fb]
ablation(16, "'두 부분의 넓이가 서로 같다'", va + vb, ans16, f'a=9/4 → (b, k)={fa}, a=11/4 → {fb}')

print()
print('ALL OK' if ok else 'SOME FAIL')
