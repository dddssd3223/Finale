# -*- coding: utf-8 -*-
# 14회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 3, 14: 5, 15: 2, 16: 4}          # 분담표 13③·14⑤·15②·16④
DBREF = {13: 'D43 예상밖 1', 14: 'D25 결합 1', 15: 'J54 후보_순위 1', 16: 'I75 후보_순위 2 (다시)'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 계수 13●·14●·15○·16●
BOX = {13: True, 14: True, 15: False, 16: True}           # 원문대로(D43·D25·I75 상자 있음, J54 상자 없음)
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t, a, b, p = sp.symbols('x t a b p', real=True)
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
    return [choice_val(z) for z in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    cf = sorted(COEF & set(IT[no].get('ops') or []))
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and (cf or not NEED_COEF[no]),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {cf}) bunseok=False')
    check(no, ('cond' in IT[no]) == BOX[no] and 'bogi' not in IT[no], f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(분담표 상자 칸대로), 보기형 아님')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs', 'level'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')
    check(no, IT[no]['level'] == LEVEL[no], f'level {IT[no]["level"]} (목표 {LEVEL[no]})')
    body = IT[no]['body'] + ''.join(c for _, c in IT[no].get('cond', [])) + (IT[no].get('after') or '')
    check(no, '이러한' not in body and '이와 같은' not in body, "'이러한'·'이와 같은' 없음")
    nums = set(re.findall(r'(?<![\w.])\d+(?![\w.])', re.sub(r'<[^>]*>|style="[^"]*"|&[lg]t;', ' ', body)))
    check(no, str(abs(val)) not in nums, f'정답 {val}이 본문에 나온 수 {sorted(nums, key=int)}와 다름')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [choice_val(z) for z in IT[no]['wrongs']]
    vals = [sp.nsimplify(z) for z in vals]
    check(no, all(z in v and z != v[IT[no]['ans'] - 1] for z in vals) and sorted(w) == sorted(set(vals)) and len(set(vals)) >= 2,
          f'오답 {vals} 선지에 있음, wrongs {IT[no]["wrongs"]}와 같음 ({why})')


def ablation(no, cname, vals, ans, why='', undef=None):
    global ok
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = f'필요(남은 조건을 만족시키는 경우가 없음{"; " + why if why else ""})'
    else:
        sv = sorted(set(vals), key=lambda z: float(z))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:6]))}{" 등" if len(sv) > 6 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else sp.nsimplify(choice_val(c)) if re.fullmatch(r'-?\d+|-?\\dfrac.*', c) else c



# ================= 13번 (D43: 세 실수 a,b,c, x≤0: −x²+ax+b, x>0: x³+3cx−6|x−c|, 증가, f(−1)의 최댓값) =================
def make13(av, bv, cv, m=3, k=6):
    def f(z):
        return -z**2 + av * z + bv if z <= 0 else z**3 + m * cv * z - k * abs(z - cv)
    return f


def inc13(av, bv, cv, m=3, k=6, cont=False):
    """엄격 증가 판정: 조각별 도함수 ≥0(표본 + 꺾인 점 바로 오른쪽) + x=0에서 b ≤ f(0+). cont=True면 b = f(0+)도 요구."""
    f0p = -k * abs(cv)
    if cont and bv != f0p:
        return False
    if bv > f0p:
        return False
    if av < 0:          # x<0에서 f'=−2x+a, x→0−에서 a<0이면 음수
        return False
    dfr = lambda z: 3 * z**2 + m * cv + (k if z < cv else -k)       # x>0 조각의 도함수(꺾인 점 제외)
    zs = [R(j, 64) for j in range(1, 64 * 6)] + ([cv + R(1, 10**6)] if cv > 0 else []) + [R(1, 10**6)]
    if any(dfr(z) < 0 for z in zs if z > 0 and z != cv):
        return False
    return True


C13 = sorted(set([R(j, 8) for j in range(-24, 41)] + [1 - R(1, 1000)]))
A13 = [R(j, 4) for j in range(-4, 9)]
feas = [(av, cv) for av in A13 for cv in C13 if inc13(av, -6 * abs(cv), cv)]
check(13, sorted({cv for _, cv in feas}) == [cv for cv in C13 if cv >= 1] and sorted({av for av, _ in feas}) == [av for av in A13 if av >= 0],
      'c∈[−3,5]·a 전수(b=f(0+)): 증가 ⇔ c≥1, a≥0 (c≤0, c=1−1/1000 탈락)')
# b는 b ≤ f(0+)에서 자유: 최댓값은 b=f(0+)에서
best = max(make13(av, -6 * abs(cv), cv)(-1) for av, cv in feas)
ans13 = best
check(13, ans13 == -7 and inc13(0, -6, 1), f'f(−1)의 최댓값 {ans13} (a=0, b=−6, c=1)')
check(13, all(make13(av, bv, cv)(-1) <= -7 for av in A13 for cv in C13 for bv in [-6 * abs(cv) - d for d in (0, R(1, 2), 3)] if inc13(av, bv, cv)),
      'b<f(0+)(불연속)까지 넣어도 f(−1) ≤ −7')
fz = make13(0, -6, 1)
vals = [fz(R(j, 50)) for j in range(-200, 300)]
check(13, all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)), 'a=0,b=−6,c=1에서 표본 수열이 엄격 증가')
ans_ok(13, ans13)
w13a = -1 - 0 - 6 * 2                                  # (선지 밖) x→0+에서 판정해 c≥2
w13b = make13(0, 0, 0)(-1)                             # (선지 밖) c=0을 버리지 않음
check(13, not inc13(0, 0, 0) and inc13(0, -12, 2) and w13a == -13 and w13b == -1, 'c=0은 실제로 증가하지 않음, 선지 밖 경로 값 −13·−1 확인')
w13c = max(-av + (-6 * abs(cv)) for av, cv in feas)          # −x² 항 빠뜨림: f(−1)=−a+b
w13d = max(1 - av + (-6 * abs(cv)) for av, cv in feas)       # −(−1)²을 +1로
wrong_in(13, [w13c, w13d], '−x² 항 빠뜨림 → −6 · −(−1)²을 +1로 → −5')
# 원문 D43: 양수 c, x³+cx−2|x−c|, 연속 → f(−1)의 최댓값 −7/3
Co = sorted(set([R(j, 24) for j in range(1, 97)]))
fo = [(av, cv) for av in A13 for cv in Co if inc13(av, -2 * cv, cv, m=1, k=2, cont=True)]
ob = max(make13(av, -2 * cv, cv, m=1, k=2)(-1) for av, cv in fo)
check(13, min(cv for _, cv in fo) == R(2, 3) and ob == R(-7, 3) == orig_ans('D43'), f'원문 D43: c≥2/3, f(−1)의 최댓값 {ob} = 원문 답 {orig_ans("D43")}')
# 빼 보기
ablation(13, '증가 조건', [], ans13, undef='a, b가 자유로워 f(−1)=−1−a+b의 최댓값이 없음')
cont_best = max(make13(av, -6 * abs(cv), cv)(-1) for av, cv in feas if inc13(av, -6 * abs(cv), cv, cont=True))
check(13, cont_best == ans13, f"원문 (가) '연속'을 다시 넣어도 답 {cont_best} 그대로 → 원문 (가)는 이 구조에서 군더더기라 뺌(note)")
check(13, all(not inc13(0, -6 * abs(cv), cv) for cv in C13 if cv <= 0), "'양수 c'를 지워도 c≤0은 증가 조건이 버림(예상밖 1: 단서가 판단으로 바뀜)")

# ================= 14번 (D25: xg(x)=|x{f(x−p)−f(−p)}|, g 연속, 미분가능하지 않은 점 2개, 정수 p의 개수) =================
f14 = x**3 - 3 * x**2 - 9 * x - 12


def nondiff14(pv, fx=f14, g0=0):
    """g(x)=x|Q(x)| (F=f(x−p)−f(−p)=xQ). 실제 g를 좌우 미분계수로 판정: 후보는 F의 실근과 0"""
    F = sp.expand(fx.subs(x, x - pv) - fx.subs(x, -pv))
    Q = sp.cancel(F / x)
    g = lambda z: (g0 if z == 0 else sp.Abs(z * F.subs(x, z)) / z)
    cands = sorted(set(sp.Poly(F, x).real_roots()) | {sp.Integer(0)}, key=float)
    bad = []
    h = R(1, 10**7)
    for r in cands:
        gr = g(r)
        if abs(sp.N(g(r + h) - gr)) > 1e-3 or abs(sp.N(g(r - h) - gr)) > 1e-3:   # 불연속이면 미분가능하지 않음
            bad.append(r); continue
        dl = sp.N((gr - g(r - h)) / h, 30)
        dr = sp.N((g(r + h) - gr) / h, 30)
        if abs(dl - dr) > 1e-4:
            bad.append(r)
    return bad


check(14, sp.factor(f14 + 7) == sp.factor((x + 1)**2 * (x - 5)) and sp.factor(f14 + 39) == sp.factor((x - 3)**2 * (x + 3)), 'f+7=(x+1)²(x−5), f+39=(x−3)²(x+3)')
P14 = list(range(-12, 13))
cnt14 = {pv: len(nondiff14(pv)) for pv in P14}
sel14 = [pv for pv in P14 if cnt14[pv] == 2]
check(14, sel14 == [-4, -2, -1, 0, 2], f'정수 p∈[−12,12] 전수: 미분가능하지 않은 점이 2개인 p = {sel14} (p=1,−3은 {cnt14[1]}개, p=3·−5는 {cnt14[3]}·{cnt14[-5]}개)')
# 실수 p 표본으로 범위 확인: (−5,3)\{1,−3}
Pr = [R(j, 4) for j in range(-28, 21)]
selr = [pv for pv in Pr if len(nondiff14(pv)) == 2]
check(14, selr == [pv for pv in Pr if -5 < pv < 3 and pv not in (1, -3)], '실수 p 표본(간격 1/4): 조건 ⇔ −5<p<3, p≠1, p≠−3')
ans14 = len(sel14)
ans_ok(14, ans14)
w14a = len([pv for pv in sel14 if pv > 0])                   # 원문처럼 p>0
w14b = len([pv for pv in P14 if -3 < pv < 1])                 # 두 극점 사이 −1<−p<3
wrong_in(14, [w14a, w14b], 'p를 양수로만 → 1 · 두 극점 사이로 → 3')
# 원문 D25: 두 양수 p, q, xg=|xf(x−p)+qx|, 미분가능하지 않은 점 1개 → p+q=8
orig14 = []
for pv in range(1, 10):
    qv = -f14.subs(x, -pv)
    if qv > 0 and len(nondiff14(pv)) == 1:
        orig14.append(pv + qv)
check(14, orig14 == [8] == [orig_ans('D25')], f'원문 D25: 개수 1인 양수 p(q=−f(−p)>0)에서 p+q = {orig14} = 원문 답')
# 빼 보기
ablation(14, '(나) 개수 2', [], ans14, undef='(나)가 없으면 모든 정수 p가 되어 개수가 정해지지 않음')
ablation(14, '(나)의 개수 2 → 1', [len([pv for pv in P14 if cnt14[pv] == 1])], ans14, '개수 1이면 p=1, −3')
ablation(14, "'연속인 함수 g'", [len([pv for pv in P14 if len(nondiff14(pv, g0=1)) == 2]), ans14], ans14, 'g(0)≠0으로 두면 x=0도 미분가능하지 않아 개수가 달라짐')

# ================= 15번 (J54: v=3t²+2at+a (a>0), t=1·t=3에서 A까지 거리 같음, t=2에서 거리 8, A의 좌표) =================
s_ = sp.symbols('s_', real=True)
kA = sp.symbols('kA', real=True)


def pos15(vexpr):
    return sp.integrate(vexpr.subs(t, s_), (s_, 0, t))


def solve15(vexpr, d=8, apos=True, t1=1, t2=3, t3=2):
    X = pos15(vexpr)
    out = set()
    for s1 in (1, -1):          # |X(t1)−k| = |X(t2)−k| ⇔ X(t1)−k = ±(X(t2)−k)
        for s2 in (1, -1):      # |X(t3)−k| = d
            eqs = [sp.expand((X.subs(t, t1) - kA) - s1 * (X.subs(t, t2) - kA)), sp.expand(X.subs(t, t3) - kA - s2 * d)]
            for so in sp.solve(eqs, [a, kA], dict=True):
                av, kv = so.get(a, a), so.get(kA, kA)
                if av.free_symbols or kv.free_symbols:
                    out.add(('무수히 많음', s1, s2)); continue
                if apos and not av > 0:
                    continue
                out.add((av, kv))
            if not sp.solve(eqs, [a, kA], dict=True) and s1 == 1:
                # X(t1)=X(t2)이면 k가 X(t3)±d로 두 값
                for av in sp.solve(sp.expand(X.subs(t, t1) - X.subs(t, t2)), a):
                    if (not apos) or av > 0:
                        out.add((av, X.subs({t: t3, a: av}) - s2 * d))
    return out


v15 = 3 * t**2 + 2 * a * t + a
X15 = sp.expand(pos15(v15))
check(15, X15 == t**3 + a * t**2 + a * t, f'x(t) = {X15}')
check(15, all(v15.subs({a: av, t: tv}) > 0 for av in [R(1, 10), 1, 2, 5] for tv in [R(1, 100), 1, 3]), 'a>0이면 t>0에서 v>0(한 방향)')
S15 = solve15(v15)
check(15, S15 == {(2, 28)}, f'a>0에서 가능한 (a, A) = {S15}')
ans15 = 28
check(15, X15.subs({a: 2, t: 1}) == 5 and X15.subs({a: 2, t: 3}) == 51 and X15.subs({a: 2, t: 2}) == 20, 'x(1)=5, x(3)=51(중점 28), x(2)=20(거리 8)')
ans_ok(15, ans15)
w15a = [kv for av, kv in solve15(3 * t**2 + 4 * a * t + a)]            # 2at → 2at² (적분하면 t³+2at²+at)
w15b = [kv for av, kv in solve15(3 * t**2 + 2 * a * t)]                # 상수항 a의 적분 빠뜨림
check(15, w15a == [26] and w15b == [24], f'적분 실수 경로: 2at²로 → {w15a}, at 빠뜨림 → {w15b}')
wrong_in(15, w15a + w15b, '2at를 2at²로 적분 → 26 · a의 적분 at를 빠뜨림 → 24')
# 원문 J54: v=3t²+at (a>0), A(6), t=2에서 거리 10 → a=4
Xo = pos15(3 * t**2 + a * t)
ao = [r for r in sp.solve(sp.Abs(Xo.subs(t, 2) - 6) - 10, a) if r > 0]
check(15, ao == [4] == [orig_ans('J54')], f'원문 J54: a = {ao} = 원문 답 {orig_ans("J54")}')
# 빼 보기
S_nopos = solve15(v15, apos=False)
ablation(15, "'a>0'", [kv for av, kv in S_nopos if not isinstance(av, str)], ans15, f'(a, A) = {sorted(S_nopos, key=lambda z: str(z))}')
ablation(15, "'t=1·t=3에서 거리가 같음'", [], ans15, undef='a와 A의 좌표가 거리 조건 하나로 정해지지 않음')
ablation(15, "'t=2에서 거리 8'", [], ans15, undef='a가 정해지지 않아 A의 좌표 14+7a가 정해지지 않음')

# ================= 16번 (I75: 상수항 0인 삼차, (가) ∫_{2p−1}^{2p+1}, 1<p<2 (나) ∫_0^3 |f+q|, −8<q<0, f(1)) =================
def sign_change_roots(fx):
    return sorted({r for r in sp.Poly(fx, x).real_roots() if sp.sign(fx.subs(x, r - R(1, 10**6))) * sp.sign(fx.subs(x, r + R(1, 10**6))) < 0}, key=float)


def changes_in(fx, lo, hi):
    """열린구간 (lo, hi)에서 fx의 부호가 바뀌는가 ⇔ ∫|fx| ≠ |∫fx|"""
    return any(lo < r < hi for r in sign_change_roots(fx))


def p_set(fx):
    """(가)를 만족시키는 p의 집합 = 부호가 바뀌는 근 r마다 ((r−1)/2, (r+1)/2)의 합집합 → 구간 목록"""
    return sorted([((r - 1) / 2, (r + 1) / 2) for r in sign_change_roots(fx)], key=lambda z: float(z[0]))


def q_set(fx, lo=0, hi=3):
    """(나)를 만족시키는 q: −q가 (lo,hi)에서 fx 값 범위의 '건너는' 값 → (−M, −m) 꼴 열린구간으로 표본 확인"""
    crit = [r for r in sp.Poly(sp.diff(fx, x), x).real_roots() if lo < r < hi]
    vals = [fx.subs(x, z) for z in [lo, hi] + crit]
    return (-max(vals), -min(vals))


# (가) 판정을 직접 적분으로도 확인
def ga_direct(fx, pv):
    lo, hi = 2 * pv - 1, 2 * pv + 1
    return sp.integrate(sp.Abs(fx), (x, lo, hi)).evalf(20) - abs(sp.integrate(fx, (x, lo, hi)).evalf(20))


cc = sp.symbols('cc', real=True)
# 상수항 0인 삼차함수: 부호가 바뀌는 근이 3뿐 → 근 배치 전수(0의 중복도 1·2·3, 다른 근 r, s 표본)
fams = []
for r_ in [R(j, 2) for j in range(-8, 13)]:
    for s_v in [R(j, 2) for j in range(-8, 13)]:
        for cv in [1, -1]:
            fx = cv * x * (x - r_) * (x - s_v)
            if p_set(fx) == [(1, 2)]:
                fams.append(sp.factor(fx))
check(16, all(sp.expand(fm.subs(x, 0)) == 0 and sp.degree(sp.gcd(sp.Poly(fm, x), sp.Poly(x**2, x)), x) == 2 for fm in fams) and len(fams) > 0
      and all(sp.expand(fm).subs(x, 3) == 0 for fm in fams),
      f'근 표본 전수: (가)의 p 범위가 1<p<2인 f는 모두 x²(x−3)의 상수배 ({len(fams)}개 표본: {sorted(set(map(str, fams)))})')
fc = cc * x**2 * (x - 3)
for cv in [2, -2, R(1, 2)]:
    fx = fc.subs(cc, cv)
    check(16, all((ga_direct(fx, pv) > 1e-12) == (1 < pv < 2) for pv in [R(j, 8) for j in range(-8, 32)] if pv not in (1, 2)), f'c={cv}: 직접 적분으로 (가)의 부등식 ⇔ 1<p<2 (p 간격 1/8)')
qs = {cv: q_set(fc.subs(cc, cv)) for cv in [-2, 2, -1, -3]}
check(16, qs[-2] == (-8, 0) and qs[2] == (0, 8) and qs[-1] == (-4, 0), f'(나)의 q 범위: c=−2 → {qs[-2]}, c=2 → {qs[2]}(양수 쪽), c=−1 → {qs[-1]}')
f16 = fc.subs(cc, -2)
# q 범위를 직접 적분 표본으로 확인
def gb_direct(fx, qv):
    return sp.integrate(sp.Abs(fx + qv), (x, 0, 3)).evalf(20) - abs(sp.integrate(fx + qv, (x, 0, 3)).evalf(20))
check(16, all((gb_direct(f16, qv) > 1e-12) == (-8 < qv < 0) for qv in [R(j, 2) for j in range(-20, 6)]), 'f=−2x²(x−3): 직접 적분으로 (나)의 부등식 ⇔ −8<q<0 (q 간격 1/2)')
ans16 = f16.subs(x, 1)
check(16, ans16 == 4, f'f(1) = {ans16}')
ans_ok(16, ans16)
w16a = fc.subs({cc: 2, x: 1})                               # q 범위 부호를 안 봄 → c=2
fsw = 2 * x * (x - 3)**2                                     # 3을 중근으로
check(16, q_set(fsw) == (-8, 0) and p_set(fsw) != [(1, 2)], f'바꾼 근 배치 2x(x−3)²: (나)는 만족({q_set(fsw)}), (가)는 p 범위 {p_set(fsw)}로 불만족')
wrong_in(16, [w16a, fsw.subs(x, 1)], 'c의 부호를 안 봄 → −4 · 3을 중근으로 → 8')
# 원문 I75: ∫_p^{p+3}, 0<p<3, ∫_0^3, 0<q<1 → f=x²(x−3)/4, f(6)=27
fo16 = R(1, 4) * x**2 * (x - 3)
check(16, sorted([(r - 3, r) for r in sign_change_roots(fo16)]) == [(0, 3)] and q_set(fo16) == (0, 1) and fo16.subs(x, 6) == orig_ans('I75') == 27,
      f'원문 I75: f=x²(x−3)/4, f(6) = {fo16.subs(x, 6)} = 원문 답')
# 빼 보기
alt16 = [fx.subs(x, 1) for fx in [2 * x * (x - 3)**2, -2 * x**2 * (x - 3)] if q_set(fx) == (-8, 0)]
ablation(16, '(가)', alt16, ans16, '(나)만 두면 2x(x−3)²도 됨')
ablation(16, '(나)', [fc.subs({cc: cv, x: 1}) for cv in [-2, -1, 1, 3]], ans16, 'c가 정해지지 않음, f(1)=−2c')

print()
print('ALL OK' if ok else 'SOME FAIL')
