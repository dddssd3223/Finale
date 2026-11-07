# -*- coding: utf-8 -*-
# 견본5 p6 (Claude 팀 B: 9·11·13·15번) 정답 검증 + 유일성(전수) + 선지 + 오답 + 원문 + 조건 빼 보기(ABLATION)
import os, itertools
import sympy as sp

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p6.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {9: 3, 11: 5, 13: 4, 15: 5}
x, t, u = sp.symbols('x t u', real=True)
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.sympify(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, IT[no].get('author') == 'claude', "author='claude'")


def wrong_in(no, vals, why):
    v = ch(no)
    check(no, all(sp.sympify(w) in v and sp.sympify(w) != v[IT[no]['ans'] - 1] for w in vals),
          f'오답 {vals} 선지에 있음 ({why})')


def ablation(no, cname, vals, ans, why=''):
    vals = [sp.nsimplify(v) for v in vals]
    sv = sorted(set(vals), key=lambda z: float(z))
    if not sv:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    elif sv == [ans]:
        msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    elif len(sv) >= 2:
        msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
    else:
        msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')
    return msg


# ======================= 원문 직접 풀이 =======================
x1o, x2o = t**3 - 2*t**2 + 3*t, t**2 + 12*t
T = [r for r in sp.solve(sp.diff(x1o - x2o, t), t) if r >= 0]
check('M48', T == [3] and abs((x1o - x2o).subs(t, 3)) == 27, f'M48 원문: 속도 같은 시각 {T}, 거리 27')

Ms = []
for a1, a2 in itertools.product(range(3), repeat=2):
    f0 = (x - a1)*(x - a2)*(x - 2)
    cr = sp.Poly(sp.diff(f0, x), x).real_roots()
    if len(set(cr)) == 2:
        al = min(cr)
        Ms.append(sp.nsimplify(f0.subs(x, al)))
Mmax = max(Ms)
check('D38', Mmax == sp.Rational(32, 27) and Mmax.p + Mmax.q == 59, f'D38 원문: M의 최댓값 {Mmax}, p+q=59')

m_, n_, b_, c_ = sp.symbols('m n b c')
fo = m_*x + n_; go = x**2 + b_*x + c_
lim0 = sp.limit(sp.integrate(fo.subs(x, t), (t, 0, x))/x, x, 0)
solo = sp.solve([lim0, sp.integrate(fo*go, (x, -1, 1)), sp.integrate(fo*sp.diff(go, x), (x, -1, 1)) - 8], [m_, n_, b_], dict=True)
valo = [fo.subs(s).subs(x, sp.diff(go, x).subs(s).subs(x, 1)) for s in solo]
check('I45', valo == [12], f'I45 원문: f(g\'(1)) = {valo} (⑤ 12)')

C_, K_ = sp.symbols('C K')
fI = 4*x - 1; FI = 2*x**2 - x + C_
HI = sp.integrate(8*x**3 + 3*x**2 + 1, x) + K_
q_, r_ = sp.div(sp.Poly(HI, x), sp.Poly(FI, x))
solI = sp.solve(sp.Poly(r_.as_expr(), x).all_coeffs(), [C_, K_], dict=True)
valI = set()
for s in solI:
    GI = q_.as_expr().subs(s)
    valI.add(sp.expand(GI.subs(x, 3) - GI.subs(x, 1)))
lhs = sp.integrate(fI.subs(x, t), (t, 1, x)); rhs = x*fI - 2*x**2 - 1
check('I59', sp.expand(lhs - rhs) == 0 and valI == {10}, f'I59 원문: (가) f=4x-1 성립, ∫_1^3 g = {valI}')

# ======================= 9번 =======================
X1, X2 = t**3 - 3*t**2 - 6*t, 3*t**2 - 6*t - 40


def item9(X1, X2, first=True, after_start=True):
    v1, v2 = sp.diff(X1, t), sp.diff(X2, t)
    P = sp.Poly(sp.expand(v1**2 - v2**2), t)          # 속력이 같다 <=> v1^2 = v2^2 (전수: 다항식의 모든 실근)
    rs = sorted({r for r in P.real_roots() if (r > 0 if after_start else r >= 0)}, key=float)
    if not rs:
        return [], rs
    pick = rs[:1] if first else rs
    return [abs(sp.nsimplify((X1 - X2).subs(t, r))) for r in pick], rs


val9, rs9 = item9(X1, X2)
check(9, rs9 == [2, 4], f'속력이 같은 양의 시각(전수) {rs9}, 처음은 t=2')
v1, v2 = sp.diff(X1, t), sp.diff(X2, t)
check(9, v1.subs(t, 2) == -v2.subs(t, 2) != 0 and v1.subs(t, 0) == v2.subs(t, 0), 't=2는 반대 방향(v1=-v2), t=0에서도 속도 같음(출발 순간 제외 함정)')
ans_ok(9, val9[0])
d4 = abs((X1 - X2).subs(t, 4)); d0 = abs((X1 - X2).subs(t, 0)); d2n = abs(X1.subs(t, 2))
wrong_in(9, [d4, d0, val9[0] + d4, d2n], f'속도만 t=4 → {d4}, t=0 포함 → {d0}, 두 순간 합 → {val9[0] + d4}, x2 상수항 누락 → {d2n}')
ablation(9, "'출발한 후'(t>0)", item9(X1, X2, after_start=False)[0], val9[0], 't=0 이 처음 순간이 됨')
# '속력' 대신 '속도'로 읽으면(원문 조건)
rv = sorted([r for r in sp.solve(v1 - v2, t) if r > 0]); ablation(9, "'속력'(→ 속도로 바꿈)", [abs((X1 - X2).subs(t, r)) for r in rv[:1]], val9[0])
ablation(9, "'처음으로'", item9(X1, X2, first=False)[0], val9[0])
ablation(9, 'x2의 상수항 -40', item9(X1, X2 + 40)[0], val9[0])

# ======================= 11번 =======================


def item11(S=range(4), fixed=3, use_diff=True):
    data = {}
    for a1, a2 in itertools.product(S, repeat=2):
        f0 = sp.expand((x - a1)*(x - a2)*(x - fixed))
        cr = sp.Poly(sp.diff(f0, x), x).real_roots()
        if len(set(cr)) != 2:
            continue                                  # 극값 없음 (삼중근)
        al, be = min(cr), max(cr)
        M, m = sp.nsimplify(f0.subs(x, al)), sp.nsimplify(f0.subs(x, be))
        data[f0] = (M - m) if use_diff else M
    top = max(data.values())
    fs = [f for f, v in data.items() if v == top]
    return top, fs


top11, fs11 = item11()
check(11, top11 == 4 and {sp.factor(f) for f in fs11} == {sp.factor(x**2*(x - 3)), sp.factor(x*(x - 3)**2)},
      f'M-m 최댓값 {top11}, 그때 함수(전수 16 순서쌍) {[sp.factor(f) for f in fs11]}')
val11 = max(f.subs(x, 5) for f in fs11)
ans_ok(11, val11)
_, fsM = item11(use_diff=False)
w11a = max(f.subs(x, 5) for f in fsM)
w11b = [((x)*(x - 1)*(x - 3)).subs(x, 5), (x*(x - 2)*(x - 3)).subs(x, 5)]
wrong_in(11, [w11a] + w11b, f'극댓값 최대 함수만 → {w11a}, 서로 다른 세 근 x(x-1)(x-3), x(x-2)(x-3) → {w11b}')
f5all = sorted({sp.expand((x - a1)*(x - a2)*(x - 3)).subs(x, 5) for a1 in range(4) for a2 in range(4)})
check(11, min(ch(11)) >= 0 and max(ch(11)) <= max(f5all) and min(ch(11)) < min(f5all) + 5, f'선지 범위가 가능한 f(5) 값 {f5all} 범위 안(계산 없이 지워지는 값 없음)')
top_b, fs_b = item11(S=range(5))
ablation(11, "a, b의 범위 '3 이하'(→ 4 이하)", [max(f.subs(x, 5) for f in fs_b)], val11)
top_b2, fs_b2 = item11(S=range(-1, 4))
ablation(11, "a, b의 범위 '0 이상'(→ -1 이상)", [max(f.subs(x, 5) for f in fs_b2)], val11)
top_c, fs_c = item11(use_diff=False)
ablation(11, "'M-m'(→ M)", [max(f.subs(x, 5) for f in fs_c)], val11)

# ======================= 13번 =======================
al_, be_, p_, q_ = sp.symbols('alpha beta p q')
f13 = al_*x + be_; g13 = x**2 + p_*x + q_
expr = sp.integrate(f13.subs(x, t), (t, 2, x))/(x - 2)**2
# (가): 극한이 존재하려면 분자의 (x-2)^1 항이 0 → 전개해서 확인
num = sp.expand(sp.integrate(f13.subs(x, t), (t, 2, x)))
ser = sp.Poly(sp.expand(num.subs(x, u + 2)), u).all_coeffs()[::-1]   # u^0, u^1, u^2
condA = [ser[1], ser[2] - 1] if len(ser) > 2 else None
E1 = sp.integrate(f13*g13, (x, -1, 5)); E2 = sp.integrate(g13, (x, -1, 5)) - 12


def solve13(eqs, unknowns=(al_, be_, p_, q_)):
    sols = sp.solve(eqs, list(unknowns), dict=True)
    out = []
    for s in sols:
        if s.get(al_, al_) == 0:
            continue
        ff = f13.subs(s); gg = g13.subs(s)
        val = sp.simplify(gg.subs(x, ff.subs(x, 5)))
        out.append(val)
    return out, sols


v13, s13 = solve13(condA + [E1, E2])
check(13, len(s13) == 1 and sp.expand(f13.subs(s13[0]) - 2*(x - 2)) == 0 and sp.expand(g13.subs(s13[0]) - ((x - 2)**2 - 1)) == 0,
      f'해 유일 {s13}: f=2(x-2), g=(x-2)^2-1')
check(13, sp.limit(expr.subs(s13[0]), x, 2) == 1, '(가) 극한값 1 확인')
ans_ok(13, v13[0])
w13 = [((x - 2)**2 + 2).subs(x, 6), ((x - 2)**2 - 7).subs(x, 6), (2*(x - 2)).subs(x, ((x - 2)**2 - 1).subs(x, 5)), 6]
wrong_in(13, w13, f'짝수항도 소거(q=2) {w13[0]}, 1/3 누락(q=-7) {w13[1]}, f(g(5)) {w13[2]}, f(5) {w13[3]}')
for name, eqs in [('(가)', [E1, E2]), ('(나) ∫fg=0', condA + [E2]), ('(나) ∫g=12', condA + [E1])]:
    sols = sp.solve(eqs, [al_, be_, p_, q_], dict=True)
    free = set().union(*[{al_, be_, p_, q_} - set(s) for s in sols]) if sols else set()
    vals = {sp.simplify(g13.subs(s).subs(x, f13.subs(s).subs(x, 5))) for s in sols}
    sample = set()
    for s in sols:
        e = sp.simplify(g13.subs(s).subs(x, f13.subs(s).subs(x, 5)))
        for k in [0, 1, 2]:
            sample.add(e.subs({fv: k + 1 for fv in e.free_symbols}))
    ablation(13, name, list(sample), v13[0], f'자유 문자 {sorted(map(str, free))}')

# ======================= 15번 =======================
cs = sp.symbols('c0:5')
fgen = sum(cs[i]*x**i for i in range(5))                 # 4차 이하 다항식 전수(차수 비교로 충분: 최고차 n이면 n*c_n = c_n → n=1)
idA = sp.expand(sp.integrate(fgen.subs(x, t), (t, 1, x)) - (x*fgen - x**2 - 2))
solA = sp.solve(sp.Poly(idA, x).all_coeffs(), cs, dict=True)
check(15, len(solA) == 1 and sp.expand(fgen.subs(solA[0]) - (2*x + 1)) == 0, f'(가) → f 유일 {fgen.subs(solA[0])}')
hB = 5*x**4 + 4*x**3 + 6*x**2 + 2*x + 1


def item15(f, h, a=-1, b=2):
    """F=∫f+C. (나) ⟺ (FG)'=h ⟺ FG = H + K (H=∫h). G가 다항식 ⟺ F | H+K. C, K 전수로 풀어 가능한 ∫_a^b g 목록."""
    F = sp.integrate(f, x) + C_
    H = sp.integrate(h, x) + K_
    qq, rr = sp.div(sp.Poly(H, x), sp.Poly(F, x))
    sols = sp.solve(sp.Poly(rr.as_expr(), x).all_coeffs(), [C_, K_], dict=True)
    res = []
    for s in sols:
        if not all(v.is_real for v in s.values()):
            continue
        G = sp.expand(qq.as_expr().subs(s))
        Fs = F.subs(s)
        assert sp.expand(sp.diff(Fs, x)*G + Fs*sp.diff(G, x) - h) == 0
        res.append((s, G, sp.expand(G.subs(x, b) - G.subs(x, a))))
    return res


r15 = item15(2*x + 1, hB)
Cs = sorted(s[C_] for s, _, _ in r15)
check(15, Cs == [1, 2], f'F의 상수 C 후보(전수, F | H+K 조건) {Cs}: G = {[g for _, g, _ in r15]}')
vals15 = [v for _, _, v in r15]
val15 = sum(vals15)
ans_ok(15, val15)
G0 = sp.symbols('g0:4')
Gg = sum(G0[i]*x**i for i in range(4))
# C=0으로 두고 x^3 계수만 비교한 오답
b_wrong = sp.solve(sp.Poly(sp.expand((x**2 + x)*Gg), x).coeff_monomial(x**3) - 2, G0[1])[0].subs(G0[2], 0)   # x^3 계수만, a=0
w15c0 = sp.expand((x**3 + b_wrong*x).subs(x, 2) - (x**3 + b_wrong*x).subs(x, -1))
w15K0 = [v for s, _, v in r15 if s[K_] == 0]
w15C2 = [v for s, _, v in r15 if s[C_] == 2]
wrong_in(15, [w15c0, w15K0[0], w15C2[0], 18], f'C=0 → {w15c0}, K=0(→C=1만) {w15K0}, C=2만 {w15C2}, 일차항 누락 9+9=18')
# ---- 조건 빼 보기 ----
alt = []
for cc in [0, 2, 3, -1]:                                  # (가)를 빼면 f가 정해지지 않음: f=2x+cc 등으로 (나)를 만족시키는 예
    rr = item15(2*x + cc, hB)
    if rr:
        alt.append(sum(v for _, _, v in rr))
for fe in [x**2, 3*x**2 + 2*x]:
    rr = item15(fe, hB)
    if rr:
        alt.append(sum(v for _, _, v in rr))
ablation(15, '(가)', [val15] + alt if alt else [], val15, 'f를 2x+1이 아닌 다항식으로 두어도 (나)를 만족시키는 경우가 있음' if alt else '')
# (나)를 빼면 G는 임의의 다항식 → ∫g 정해지지 않음
exG = [x, x**3 + x, x**3 + 1, x**2]
ablation(15, '(나)', [sp.expand(G.subs(x, 2) - G.subs(x, -1)) for G in exG], val15, 'G 임의: ' + ', '.join(map(str, exG)))
# (나)의 '모든 실수 x' 대신 C=0(=F(0)=0) 같은 단서가 없으므로 두 경우 모두 셈: '모든 값의 합' → 한 값만이면
ablation(15, "'될 수 있는 모든 값의 합'(→ 한 값)", vals15, val15, '두 경우 C=1, C=2')
# (가)의 상수 -2 (f(1)을 정하는 대입점 조건)
vv = []
for kk in [1, 3]:
    ff = (2*x + (kk - 1))
    rr = item15(ff, hB)
    vv.append(sum(v for _, _, v in rr) if rr else None)
ablation(15, '(가)의 상수 -2(→ -1, -3으로 바꿈)', [v for v in vv if v is not None], val15, '(가)에서 x=1 대입이 f의 상수항을 정함')

print('ALL OK' if ok else 'SOME FAIL')
