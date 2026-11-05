# -*- coding: utf-8 -*-
# 1회 p2 (Claude 9·11·13·15번) 정답 검증 + 유일성(전수) + 선지 등차 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os
import sympy as sp

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {9: 4, 11: 5, 13: 4, 15: 2}
x, t, s = sp.symbols('x t s', real=True)
a, b, c, k, p, q = sp.symbols('a b c k p q')
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.sympify(str(cc).replace('\\dfrac', '').replace('\\frac', '')) if '\\' not in str(cc) else None for cc in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1 and list(d)[0] > 0, f'선지 {v} 서로 다르고 오름차순 등차(공차 {d})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, IT[no].get('author') == 'claude', "author='claude'")
    for f_ in ('vtype', 'effect', 'bunseok', 'precedent'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')


def wrong_in(no, vals, why):
    v = ch(no)
    check(no, all(sp.sympify(w) in v and sp.sympify(w) != v[IT[no]['ans'] - 1] for w in vals), f'오답 {vals} 선지에 있음 ({why})')


def sign_changes(P, var, lo=None):
    """다항식 P의 부호가 바뀌는 점(홀수 중복 실근). lo가 있으면 var>lo 인 것만."""
    P = sp.Poly(sp.expand(P), var)
    if P.degree() <= 0:
        return []
    rs = P.real_roots()
    out = []
    for r in sorted(set(rs), key=lambda z: float(z)):
        if lo is not None and not (r > lo):
            continue
        if rs.count(r) % 2 == 1:
            out.append(r)
    return out


def ablation(no, cname, vals, ans, why='', undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(vals), key=lambda v: float(v))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


# ================= 원문 직접 풀이 =================
X0 = t**3 + a*t**2 + b*t
V0 = sp.diff(X0, t); A0 = sp.diff(V0, t)
s0 = sp.solve([V0.subs(t, 1), A0.subs(t, 2)], [a, b], dict=True)
check('M50', len(s0) == 1 and s0[0][a] + s0[0][b] == 3 and sign_changes(V0.subs(s0[0]), t, lo=0) == [1, 3],
      f'M50 원문: {s0}, a+b=3 (①), t=1에서 부호 바뀜')

# I36: [0,1)에서 ax^2-1, f(x+1)=f(x)+b, 연속, ∫_2^3 f = 11/3
s1 = sp.solve([(a - 1) - (-1 + b), sp.integrate(a*x**2 - 1, (x, 0, 1)) + 2*b - sp.Rational(11, 3)], [a, b], dict=True)
check('I36', len(s1) == 1 and s1[0][a] + s1[0][b] == 4, f'I36 원문: {s1}, a+b=4 (⑤)')

# D36: f=x^4/4-2x^3+ax^2+bx, x=0 극값, (0,∞) 증가 → f'(1) 최솟값 4
good = []
for av in [sp.Rational(n, 4) for n in range(-40, 81)]:
    fp = sp.diff(x**4/4 - 2*x**3 + av*x**2, x)
    if 0 in sign_changes(fp, x) and all(fp.subs(x, sp.Rational(m, 8)) >= 0 for m in range(1, 120)) and all(r <= 0 for r in sign_changes(fp, x)):
        good.append(av)
check('D36', min(good) == sp.Rational(9, 2) and sp.diff(x**4/4 - 2*x**3 + min(good)*x**2, x).subs(x, 1) == 4, f'D36 원문: 가능한 a 최솟값 {min(good)}, f\'(1)=4 (④)')

# I59: f=4x-1, F=2x^2-x+k, G=x^2+px+q, (FG)'=8x^3+3x^2+1 → ∫_1^3 g = 10
F0 = 2*x**2 - x + k; G0 = x**2 + p*x + q
eqs0 = sp.Poly(sp.expand(sp.diff(F0*G0, x) - (8*x**3 + 3*x**2 + 1)), x).all_coeffs()
s3 = sp.solve(eqs0, [k, p, q], dict=True)
check('I59', len(s3) == 1 and sp.integrate(sp.diff(G0, x).subs(s3[0]), (x, 1, 3)) == 10, f'I59 원문: {s3}, ∫_1^3 g = 10')

# ================= 9번 =================
X = t**3 + a*t**2 + b*t
V = sp.diff(X, t); Acc = sp.diff(V, t)
sol9 = sp.solve([V.subs(t, 2), Acc.subs(t, 3)], [a, b], dict=True)
check(9, sol9 == [{a: -9, b: 24}], f'v(2)=0, a(3)=0 → {sol9} (일차 연립, 해 하나)')
V9 = V.subs(sol9[0]); X9 = X.subs(sol9[0])
sc9 = sign_changes(V9, t, lo=0)
check(9, sp.expand(V9 - 3*(t - 2)*(t - 4)) == 0 and sc9 == [2, 4], f'v={sp.factor(V9)}, 부호가 바뀌는 시각 {sc9} (t=2에서 실제로 방향 전환)')
other = [r for r in sc9 if r != 2]
check(9, other == [4], f'다시 방향을 바꾸는 시각 {other} (하나뿐)')
ans_ok(9, X9.subs(t, 4))
wrong_in(9, [sol9[0][a] + sol9[0][b]], '원본처럼 a+b')
print('--- 9번 조건 빼 보기 ---')
vals = []
for bv in [12, 15, 21, 27, 30]:                         # a(3)=0만: a=-9, b 자유 (판별식 양수인 b)
    Vb = V.subs({a: -9, b: bv}); scb = sign_changes(Vb, t, lo=0)
    if len(scb) == 2:
        vals.append(sp.nsimplify(sp.simplify(X.subs({a: -9, b: bv}).subs(t, scb[1]))))
ablation(9, "'t=2에서 운동 방향을 바꾼다'", vals, 16)
vals = []
for av in [-6, -7, -8, -10, -12]:                        # v(2)=0만: b=-12-4a
    sub = {a: av, b: -12 - 4*av}; scb = sign_changes(V.subs(sub), t, lo=0)
    oth = [r for r in scb if r != 2]
    if 2 in scb and len(oth) == 1:
        vals.append(X.subs(sub).subs(t, oth[0]))
ablation(9, "'t=3에서 가속도가 0'", vals, 16)

# ================= 11번 =================
def f11(av, bv, xv):
    n = sp.floor(xv); u = xv - n
    return av*u**2 + u + n*bv


u = sp.symbols('u', real=True)
# 연속 조건: 모든 정수 n에서 좌극한 a+1+(n-1)b = 함숫값 nb
cont = sp.solve(sp.Eq(a + 1 + (sp.Symbol('n') - 1)*b, sp.Symbol('n')*b), b)
check(11, cont == [a + 1], f'모든 정수에서 연속 ⇔ b = {cont}')
I12 = sp.integrate((a*u**2 + u) + b, (u, 0, 1))      # ∫_1^2 f = ∫_0^1 (f+b)
sol11 = sp.solve([b - (a + 1), I12 - sp.Rational(11, 2)], [a, b], dict=True)
check(11, sol11 == [{a: 3, b: 4}], f'연립 {sol11} (일차, 해 하나)')
av, bv = 3, 4
num = sum(f11(av, bv, 1 + sp.Rational(i, 2000) + sp.Rational(1, 4000)) for i in range(2000)) / 2000
check(11, abs(float(num) - 5.5) < 1e-3 and all(abs(f11(av, bv, n - sp.Rational(1, 10**8)) - f11(av, bv, n)) < 1e-6 for n in range(-3, 4)),
      f'a=3, b=4: 중점 합 ∫_1^2 f ≈ {float(num):.5f}, 정수점 연속 확인')
ans_ok(11, sol11[0][a] + sol11[0][b])
wrong_in(11, [3, 4], 'a만, b만')
print('--- 11번 조건 빼 보기 ---')
ablation(11, "'연속'", [sp.solve(I12.subs(b, bb) - sp.Rational(11, 2), a)[0] + bb for bb in [1, 2, 4]], 7, why='b가 정해지지 않음')
ablation(11, "'∫_1^2 f = 11/2'", [aa + aa + 1 for aa in [1, 2, 3]], 7, why='a가 정해지지 않음')
ablation(11, "'f(x+1)=f(x)+b'", [], 7, undef='구간 [1, 2]에서 f가 정해지지 않고 b가 나오지 않음')

# ================= 13번 =================
def ok13(av, bv):
    f = x**4 - 8*x**3 + av*x**2 + bv*x
    fp = sp.diff(f, x)
    scs = sign_changes(fp, x)
    ext0 = 0 in scs                                     # (가) x=0에서 극값 ⇔ f'의 부호가 0에서 바뀜
    nomax = not any(fp.subs(x, r - sp.Rational(1, 10**6)) > 0 for r in scs)   # (나) 극댓값 없음
    return ext0, nomax


grid_a = [sp.Rational(n, 2) for n in range(-40, 101)]
grid_b = [0, 1, -1, 3, -5, sp.Rational(1, 2)]
valid = [(av, bv) for av in grid_a for bv in grid_b if all(ok13(av, bv))]
check(13, all(bv == 0 for _, bv in valid), "(가)에서 f'(0)=b=0: 격자 전수에서 b≠0은 모두 탈락")
va = sorted({av for av, _ in valid})
check(13, va == [av for av in grid_a if av >= 18], f'조건을 만족시키는 a = 18 이상 (격자 {len(va)}개, 최솟값 {va[0]})')
check(13, ok13(0, 0) == (False, True), 'a=0: 극댓값은 없지만 (가) 실패 (f\'=4x^2(x-6))')
check(13, ok13(17, 0)[1] is False and ok13(18, 0) == (True, True), 'a=17은 극댓값 있음, a=18은 두 조건 만족 (f\'=4x(x-3)^2)')
disc = sp.discriminant(2*x**2 - 12*x + a, x)
check(13, sp.solve(sp.Eq(disc, 0), a) == [18], f'판별식 {sp.expand(disc)} = 0 ⇔ a=18')
f1 = (x**4 - 8*x**3 + a*x**2).subs(x, 1)
check(13, sp.expand(f1) == a - 7, 'f(1)=a-7 (a에 대하여 증가)')
ans_ok(13, f1.subs(a, 18))
wrong_in(13, [f1.subs(a, 19)], '등호 빼고 정수 a=19')
print('--- 13번 조건 빼 보기 ---')
v_noA = sorted({(x**4 - 8*x**3 + av*x**2 + bv*x).subs(x, 1) for av in grid_a for bv in grid_b if ok13(av, bv)[1]}, key=float)
ablation(13, "'(가) x=0에서 극값'", [min(v_noA)], 11, why='x=0에서 극값이 아닌 경우(a=0, b=0이나 b≠0)가 들어와 최솟값이 작아짐, 격자 최솟값')
v_noB = sorted({f1.subs(a, av) for av, bv in [(av, 0) for av in grid_a] if ok13(av, 0)[0]}, key=float)
ablation(13, "'(나) 극댓값 없음'", [], 11, undef=f'a≠0이면 모두 (가)를 만족시켜 f(1)=a-7의 최솟값이 없음; 격자에서 {v_noB[0]}까지 내려감')

# ================= 15번 =================
# f를 4차 이하 일반 다항식으로 두고 (가)를 항등식으로 풀어 유일함을 보임
cf = sp.symbols('c0:5')
fgen = sum(cf[i]*x**i for i in range(5))
rhs = x*fgen - 3*x**2 - 2
idA = sp.Poly(sp.expand(sp.integrate(fgen.subs(x, t), (t, 1, x)) - rhs), x).all_coeffs()
solA = sp.solve(idA, cf, dict=True)
f15 = sp.expand(fgen.subs(solA[0])) if len(solA) == 1 else None
check(15, len(solA) == 1 and f15 == 6*x - 1, f'(가) 항등식 → f = {f15} (해 하나)')
F15 = sp.integrate(f15, x) + k
# G를 4차 이하 일반 다항식으로 두고 (나)를 풂
cg = sp.symbols('d0:5')
Ggen = sum(cg[i]*x**i for i in range(5))
P15 = 12*x**3 + 6*x**2 - 12*x + 3
idB = sp.Poly(sp.expand(f15*Ggen + F15*sp.diff(Ggen, x) - P15), x).all_coeffs()
solB = sp.solve(idB, list(cg) + [k], dict=True)
F2s = {sp.simplify(F15.subs(sl).subs(x, 2)) for sl in solB}
check(15, len(solB) == 1 and F2s == {11}, f'(나) 전수: 해 {solB}, F(2) 값 {F2s}')
Gs = sp.expand(Ggen.subs(solB[0]))
check(15, Gs == x**2 + x - 2 and sp.expand(F15.subs(solB[0])) == 3*x**2 - x + 1, f'G = {Gs}, F = {sp.expand(F15.subs(solB[0]))}')
check(15, sp.expand(sp.diff(F15.subs(solB[0])*Gs, x) - P15) == 0, "(FG)'=12x^3+6x^2-12x+3 확인")
ans_ok(15, 11)
wrong_in(15, [sp.expand(F15.subs(k, 0)).subs(x, 2), sp.integrate(sp.diff(Gs, x), (x, 1, 3))], '상수항 무시 F(2)=10, 원본 대상 ∫_1^3 g=10')
print('--- 15번 조건 빼 보기 ---')
# (가) 제거: G=1(g=0), F=FG=∫P+C 이면 (나) 성립, F(2)=46+C 로 자유
FG_ = sp.integrate(P15, x)
vals = []
for C in [0, 1, -35]:
    Ft = FG_ + C
    if sp.expand(sp.diff(Ft, x)*1 + Ft*0 - P15) == 0:
        vals.append(Ft.subs(x, 2))
vals.append(11)
ablation(15, "'(가)'", vals, 11, why='예: G=1, F=3x^4+2x^3-6x^2+3x+C 도 (나)를 만족시킴')
ablation(15, "'(나)'", [F15.subs(k, kk).subs(x, 2) for kk in [0, 1, 2]], 11, why='F=3x^2-x+k 의 k가 정해지지 않음')
# (가)의 상수 -2 를 다른 값으로: f(1)이 바뀌어 같은 (나)에서 F(2)가 바뀌거나 해가 없음
for cc in [-1, -3]:
    idA2 = sp.Poly(sp.expand(sp.integrate(fgen.subs(x, t), (t, 1, x)) - (x*fgen - 3*x**2 + cc)), x).all_coeffs()
    sA2 = sp.solve(idA2, cf, dict=True)
    fa = sp.expand(fgen.subs(sA2[0])); Fa = sp.integrate(fa, x) + k
    sB2 = sp.solve(sp.Poly(sp.expand(fa*Ggen + Fa*sp.diff(Ggen, x) - P15), x).all_coeffs(), list(cg) + [k], dict=True)
    ablation(15, f"'(가)의 상수 -2'(→ {cc})", [sp.nsimplify(Fa.subs(sl).subs(x, 2)) for sl in sB2 if all(v.is_real for v in sl.values())], 11, why=f'f={fa}')
# (나)의 낮은 차수 항: x항 -12 를 바꾸면 k가 바뀜
for c1 in [-11, -13]:
    sB3 = sp.solve(sp.Poly(sp.expand(f15*Ggen + F15*sp.diff(Ggen, x) - (12*x**3 + 6*x**2 + c1*x + 3)), x).all_coeffs(), list(cg) + [k], dict=True)
    ablation(15, f"'(나)의 x항 -12'(→ {c1})", [F15.subs(sl).subs(x, 2) for sl in sB3] or [], 11)

print('정답 위치:', {n: IT[n]['ans'] for n in sorted(IT)})
print('ALL OK' if ok else 'SOME FAIL')
