# -*- coding: utf-8 -*-
# 견본4 p2 (Claude 9·11·13·15번) 정답 검증 + 조건 빼 보기(ABLATION)
import os
import sympy as sp

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {9: 4, 11: 5, 13: 1, 15: 3}
x, t, s = sp.symbols('x t s', real=True)
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
    check(no, all(sp.sympify(w) in v and sp.sympify(w) != v[IT[no]['ans'] - 1] for w in vals), f'오답 {vals} 선지에 있음 ({why})')


def sign_changes(P, var, lo=None):
    """다항식 P의 부호가 바뀌는 점(홀수 중복 실근) 목록. lo가 있으면 var>lo 인 것만."""
    P = sp.Poly(sp.expand(P), var)
    rs = P.real_roots()
    out = []
    for r in sorted(set(rs), key=lambda z: float(z)):
        if lo is not None and not (r > lo):
            continue
        if rs.count(r) % 2 == 1:
            out.append(r)
    return out


def ablation(no, cname, vals, ans, why='', est=False, undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(vals), key=lambda v: float(v))
        if sv == [ans]:
            msg = f'성립 조건(답 그대로 {ans}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


# ================= 원문 직접 풀이 =================
X0 = t**3 - sp.Rational(3, 2)*t**2 - 6*t
V0 = sp.diff(X0, t)
ch0 = sign_changes(V0, t, lo=0)
check('M52', ch0 == [2] and sp.diff(V0, t).subs(t, 2) == 9, f'M52 원문: 방향 전환 {ch0}, 가속도 9 (②)')

cands = []
for pv in [0, -2]:                       # g=x^2(x-2)(x+p) 의 영점 {0,2,-p} 가 2개
    g0 = (x**2 - 2*x)*x*(x + pv)
    gp = sp.diff(g0, x)
    chg = sign_changes(gp, x)
    mx = [r for r in chg if gp.subs(x, r - sp.Rational(1, 1000)) > 0]
    if not mx:
        cands.append(g0)
check('D46', len(cands) == 1 and sp.factor(cands[0]) == sp.factor(x**3*(x - 2))
      and cands[0].subs(x, sp.Rational(3, 2)) == sp.Rational(-27, 16), 'D46 원문: g=x^3(x-2), 극솟값 -27/16 (②)')

D0 = (t**3 + 2*t**2 - 3*t) - (t**2 + 5*t)
tt0 = [r for r in sp.solve(D0 - 12, t) + sp.solve(D0 + 12, t) if r.is_real and r >= 0]
v10 = sp.diff(t**3 + 2*t**2 - 3*t, t); v20 = sp.diff(t**2 + 5*t, t)
check('M38', tt0 == [3] and (v10 + v20).subs(t, 3) == 47, f'M38 원문: 거리 12인 시각 {tt0}, p+q=47 (①)')

f0 = x**3 - 12*x**2 + 45*x + 3
good = []
for av in range(-20, 21):
    H0 = sp.integrate(f0.subs(x, t)**4, (t, av, x))
    gpp = sp.diff(f0, x)*H0
    if len(sign_changes(gpp, x)) == 1:
        good.append(av)
check('I63', good == [3, 5] and sum(good) == 8, f'I63 원문: 극값 1개인 정수 a {good} (실수 a도 f\'의 근 3, 5뿐), 합 8')

# ================= 9번 =================
r = sp.symbols('r', real=True)


def item9(conds):
    """conds: 사용할 조건 집합. 후보 속도 v 를 전수로 만들어 답(방향 전환 시각의 위치) 목록 반환.
    v 는 최고차항 계수 4인 삼차식(위치 t^4+at^3+bt^2+ct 에서)."""
    res = []
    samples = [sp.Rational(k, 2) for k in range(-8, 13)] + [sp.Rational(1, 3), sp.Rational(7, 3)]
    if 'v1' in conds and 'v4' in conds:
        fams = [4*(t - 1)*(t - 4)*(t - rv) for rv in samples]
    elif 'v1' in conds:
        fams = [4*(t - 1)*(t - u)*(t - w) for u in samples for w in samples] + [4*(t - 1)*(t**2 + 1), 4*(t - 1)*(t**2 + 4*t + 8)]
    elif 'v4' in conds:
        fams = [4*(t - 4)*(t - u)*(t - w) for u in samples for w in samples] + [4*(t - 4)*(t**2 + 1)]
    else:
        fams = [4*(t - u)*(t - w)*(t - z) for u in samples[::3] for w in samples[::3] for z in samples[::3]] + [4*(t - 3)*(t**2 + 1), 4*(t - 1)*(t**2 + 1)]
    for v in fams:
        if 'v2' in conds and not (v.subs(t, 2) > 0):
            continue
        chs = sign_changes(v, t, lo=0)
        if 'once' in conds and len(chs) != 1:
            continue
        if not chs:
            continue
        X = sp.integrate(v.subs(t, s), (s, 0, t))
        res.append(tuple(X.subs(t, c) for c in chs))
    return res


ALL9 = {'v1', 'v4', 'v2', 'once'}
r9 = item9(ALL9)
check(9, set(r9) == {(-27,)}, f'조건 전부: 가능한 (방향 전환 시각의 위치) {set(r9)}')
# r 기호로 논리 확인: r≠1,4 이면 t=1,4 가 모두 홑근 → 방향 전환 2번 이상
vr = 4*(t - 1)*(t - 4)*(t - r)
check(9, sp.factor(sp.diff(vr, t).subs(t, 1)) == sp.factor(-12*(1 - r)) and sp.factor(sp.diff(vr, t).subs(t, 4)) == sp.factor(12*(4 - r)),
      "v'(1)=12(r-1), v'(4)=12(4-r): r∉{1,4}이면 두 시각 모두 홑근")
V9 = 4*(t - 1)*(t - 4)**2
X9 = sp.integrate(V9.subs(t, s), (s, 0, t))
cf = sp.Poly(sp.expand(X9), t).all_coeffs()
check(9, sp.factor(X9) == t*(t - 4)**3 and cf[0] == 1 and cf[-1] == 0, f'x = {sp.expand(X9)} = {sp.factor(X9)} (최고차 1, 상수항 0: 위치식 꼴 맞음)')
check(9, sign_changes(V9, t, lo=0) == [1] and V9.subs(t, 2) == 16, 'v=4(t-1)(t-4)^2: 방향 전환 t=1뿐, v(2)=16>0')
ans_ok(9, X9.subs(t, 1))
Vw = 4*(t - 1)**2*(t - 4)
Xw = sp.integrate(Vw.subs(t, s), (s, 0, t))
check(9, sign_changes(Vw, t, lo=0) == [4] and Vw.subs(t, 2) == -8 and Xw.subs(t, 4) == -32, '다른 후보 v=4(t-1)^2(t-4): v(2)=-8, 전환 t=4, x(4)=-32')
wrong_in(9, [-32], 'v(2)>0 무시')
print('--- 9번 조건 빼 보기 ---')
for c, name in [('v2', "'v(2)>0'"), ('once', "'운동 방향을 한 번만 바꾼다'"), ('v1', "'v(1)=0'"), ('v4', "'v(4)=0'")]:
    rr = item9(ALL9 - {c})
    flat = sorted({p for tup in rr for p in tup}, key=float)
    if any(len(tup) != 1 for tup in rr):
        ablation(9, name, [], -27, undef=f'방향을 두 번 이상 바꾸는 경우가 생겨 \'방향을 바꾸는 시각\'이 하나로 정해지지 않음; 위치 후보 {flat[:4]} 등')
    else:
        ablation(9, name, flat, -27)
ablation(9, "'출발한 후'", [p for tup in r9 for p in tup], -27, est=True, why='t=0에서 v(0)=c=-64≠0이라 출발 시각은 전환 시각이 아님, 원문 서술 틀')

# ================= 11번 =================
p = sp.symbols('p', real=True)


def has_max(g):
    gp = sp.diff(g, x)
    return any(gp.subs(x, rr - sp.Rational(1, 10**6)) > 0 for rr in sign_changes(gp, x))


def zero_count(g):
    return len(set(sp.Poly(sp.expand(g), x).real_roots()))


# (가): g=x^2(x-4)(x+p) 의 영점 {0,4,-p}: 개수 2 ⇔ p∈{0,-4} (p 기호로)
check(11, set(sp.solve((p) * (p + 4), p)) == {0, -4}, '(가) 영점 {0,4,-p}이 2개 ⇔ -p=0 또는 -p=4')
c11 = []
for pv in [0, -4]:
    g = (x**2 - 4*x)*x*(x + pv)
    check(11, zero_count(g) == 2, f'p={pv}: 영점 {sorted(set(sp.Poly(g, x).real_roots()))}')
    if has_max(g):
        c11.append(g)
check(11, len(c11) == 1 and sp.factor(c11[0]) == x**2*(x - 4)**2, f'(나) 극댓값 존재 → g={sp.factor(c11[0])}')
G11 = c11[0]
check(11, G11.subs(x, 2) == 16 and not has_max(x**3*(x - 4)), 'g=x^2(x-4)^2 극댓값 16(x=2), x^3(x-4)는 극댓값 없음')
ans_ok(11, G11.subs(x, 1))
wrong_in(11, [-3, 0], '(나) 뒤집어 x^3(x-4) 택 → g(1)=-3, 극솟값 0 혼동')
print('--- 11번 조건 빼 보기 ---')
ablation(11, "'(나) 극댓값을 갖는다'", [((x**2 - 4*x)*x*(x + pv)).subs(x, 1) for pv in [0, -4]], 9)
vals = []
for pv in [1, 2, -1, -6, sp.Rational(1, 2)]:
    g = (x**2 - 4*x)*x*(x + pv)
    if has_max(g):
        vals.append(g.subs(x, 1))
ablation(11, "'(가) 영점 2개'", vals, 9)
vals = []
for (b_, c_) in [(0, 0), (-4, 0), (0, 1), (2, 5), (-4, 8), (0, 4), (-4, 5), (-4, sp.Rational(9, 2))]:   # f=x^2+bx+c (f(0)=0 제거). 영점 2개면 f의 실근이 {0,4} 안이거나 없음
    f = x**2 + b_*x + c_
    g = (x**2 - 4*x)*f
    if zero_count(g) == 2 and has_max(g):
        vals.append(g.subs(x, 1))
ablation(11, "'f(0)=0'", vals, 9)
vals = [(cc*(x**2 - 4*x)*x*(x - 4)).subs(x, 1) for cc in [1, 2, 3]]
ablation(11, "'최고차항의 계수가 1'", vals, 9)

# ================= 13번 =================
v1 = 3*t**2 - 6*t
v2 = sp.Integer(9)
P0, Q0 = 0, -11                                   # 출발점: P는 원점, Q는 -11
x1 = P0 + sp.integrate(v1.subs(t, s), (s, 0, t))
x2 = Q0 + sp.integrate(v2, (s, 0, t))
check(13, sp.expand(x1) == t**3 - 3*t**2 and sp.expand(x2) == 9*t - 11, f'적분상수 반영: x1={sp.expand(x1)}, x2={sp.expand(x2)}')


def first16(D):
    """t>=0 에서 |D|=16 이 되는 시각 목록(오름차순)과 처음 시각."""
    rr = sorted({r_ for r_ in sp.Poly(sp.expand((D - 16)*(D + 16)), t).real_roots() if r_ >= 0}, key=float)
    return rr


D13 = sp.expand(x1 - x2)
roots = first16(D13)
check(13, D13 == t**3 - 3*t**2 - 9*t + 11 and roots == [3, 5], f'd=x1-x2={D13}, |d|=16 인 시각 {roots}')
check(13, sp.factor(D13 + 16) == (t - 3)**2*(t + 3) and sp.factor(D13 - 16) == (t - 5)*(t + 1)**2, 'd+16=(t-3)^2(t+3), d-16=(t-5)(t+1)^2')
check(13, sp.expand(sp.diff(D13, t) - 3*(t - 3)*(t + 1)) == 0 and D13.subs(t, 0) == 11 and D13.subs(t, 3) == -16
      and all(abs(D13.subs(t, sp.Rational(k, 10))) < 16 for k in range(0, 30)),
      "d'=3(t+1)(t-3): 0≤t≤3 감소, d(0)=11, d(3)=-16 → 0≤t<3 에서 -16<d≤11, |d|<16")
check(13, D13.subs(t, 1) == 0, 't=1에서 두 점이 만남(d=0) 뒤 t=3에서 거리 16')
T13 = roots[0]
check(13, v1.subs(t, T13) == 9 and v2 == 9, 't=3에서 p=q=9 (d\'(3)=0)')
ans_ok(13, (v1 + v2).subs(t, T13))
wrong_in(13, [(v1 + v2).subs(t, 5), v1.subs(t, 5), (v1 - v2).subs(t, 5)], 't=5 사용: p+q=54, p=45, p-q=36')
print('--- 13번 조건 빼 보기 ---')
ablation(13, "'처음으로'", [(v1 + v2).subs(t, T) for T in roots], 18)
allr = sorted({r_ for r_ in sp.Poly(sp.expand((D13 - 16)*(D13 + 16)), t).real_roots()}, key=float)
ablation(13, "'(t≥0)'", [(v1 + v2).subs(t, allr[0])], 18, why=f't<0을 허용하면 t={allr[0]}에서 이미 거리 16')
D0 = sp.expand(D13 - D13.subs(t, 0))             # 두 점 모두 원점 출발로 보면
r0 = first16(D0)
val0 = (v1 + v2).subs(t, r0[0])
check(13, not r0[0].is_rational and sp.nsimplify(val0) not in ch(13), f'원점 출발로 보면 처음 시각 t≈{float(r0[0]):.4f}(무리수), p+q≈{float(val0):.4f} (선지에 없음)')
ablation(13, "'점 Q는 좌표가 -11인 점을 출발'(→ 원점 출발)", [sp.N(val0, 6)], 18, why='적분상수를 0으로 두면 d=t^3-3t^2-9t, 극솟값 -27')
D1 = sp.expand(D13 - 22)                         # 출발점 부호를 바꿔 x1-x2 의 상수항을 -11 로 두면
r1 = first16(D1)
ablation(13, "'-11'의 부호(→ 11)", [sp.N((v1 + v2).subs(t, r1[0]), 6)], 18, why=f'd=t^3-3t^2-9t-11, 처음 시각 t≈{float(r1[0]):.4f}')

# ================= 15번 =================
k = sp.symbols('k', real=True)


def g15_prime(fx, expo=2):
    """g(x)=∫_1^x {f(x)-f(t)}{f(t)}^expo dt 를 그대로 미분 (라이프니츠)."""
    G = fx*sp.integrate(fx.subs(x, t)**expo, (t, 1, x)) - sp.integrate(fx.subs(x, t)**(expo + 1), (t, 1, x))
    return sp.expand(sp.diff(G, x))


def nextrema(fx, expo=2):
    return len(sign_changes(g15_prime(fx, expo), x))


# 미분식 확인: g'=f'(x)∫_1^x f^2
fk = x**3 - 6*x**2 + 7*x
check(15, sp.expand(g15_prime(fk) - sp.diff(fk, x)*sp.integrate(fk.subs(x, t)**2, (t, 1, x))) == 0, "g'(x)=f'(x)∫_1^x f(t)^2 dt (k=7에서 직접 미분)")
cnt = {kv: nextrema(x**3 - 6*x**2 + kv*x) for kv in range(1, 16)}
OK15 = [kv for kv, n in cnt.items() if n == 1]
check(15, OK15 == [9, 12, 13, 14, 15], f'k=1..15 극값 개수 {cnt} → 1개인 k {OK15}')
# 실수 k 전체 논리: f'(1)=k-9, 판별식/4=36-3k
fpk = sp.diff(x**3 - 6*x**2 + k*x, x)
check(15, sp.solve(fpk.subs(x, 1), k) == [9] and sp.solve(sp.discriminant(fpk, x), k) == [12], "f'(1)=0 ⇔ k=9, 판별식 0 ⇔ k=12")
check(15, all(nextrema(x**3 - 6*x**2 + kv*x) == 1 for kv in [12, 13, 20, 37]) and nextrema(x**3 - 6*x**2 + sp.Rational(23, 2)*x) == 3,
      'k≥12 이면 항상 1개, k=23/2 는 3개 (k<12, k≠9 는 3개)')
ans_ok(15, len(OK15))
wrong_in(15, [4, 3], 'k=12 또는 k=9 누락 → 4, 둘 다 누락 → 3')
print('--- 15번 조건 빼 보기 ---')
ablation(15, "'오직 하나의'(→ 극값을 갖도록)", [sum(1 for n in cnt.values() if n >= 1)], 5)
ablation(15, "'15 이하'", [], 5, undef='k≥12인 모든 자연수가 조건을 만족시켜 개수가 무한')
ablation(15, "'자연수'", [], 5, undef='12 이상 15 이하의 모든 실수 k가 조건을 만족시켜 개수가 무한')
cnt1 = {kv: nextrema(x**3 - 6*x**2 + kv*x, expo=1) for kv in range(1, 16)}
n1 = sum(1 for n in cnt1.values() if n == 1)
ablation(15, "'{f(t)}^2의 짝수 지수'(→ {f(t)}^1)", [n1], 5, why=f'적분 부분 ∫_1^x f(t)dt의 부호가 x-1과 달라짐, 극값 개수 {cnt1}')
cnt0 = {kv: len(sign_changes(sp.diff(x**3 - 6*x**2 + kv*x, x)*(x - 1), x)) for kv in range(1, 16)}
ablation(15, "'{f(t)}^2 인자'(→ 1)", [sum(1 for n in cnt0.values() if n == 1)], 5, est=True,
         why='정의식의 일부(원문 I63의 짝수 거듭제곱 장치): 적분 부분의 부호가 x-1과 같음을 판단하는 단계 자체이고 조건이 아님')

print('정답 위치:', {n: IT[n]['ans'] for n in sorted(IT)})
print('ALL OK' if ok else 'SOME FAIL')
