# -*- coding: utf-8 -*-
# 4회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 4, 14: 2, 15: 3, 16: 1}
DBREF = {13: 'D38 후보_순위 1', 14: 'D9 후보_순위 2', 15: 'I62 후보_순위 2', 16: 'D67 결합 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
x, t = sp.symbols('x t', real=True)
R = sp.Rational
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.Rational(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and COEF & set(IT[no].get('ops') or []),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {sorted(COEF & set(IT[no].get("ops") or []))}) bunseok=False')
    check(no, ('cond' in IT[no]) == (no == 16), f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(상자는 16번만)')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [sp.Rational(z) for z in IT[no]['wrongs']]
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


def choice_val(s):
    s = re.sub(r'\s', '', s)
    m = re.fullmatch(r'(-?)\\dfrac\{?(\d+)\}?\{?(\d+)\}?', s)
    if m:
        return sp.Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    return sp.Rational(s)


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    return o[1]['①②③④⑤'.index(o[2])]


# ================= 13번 (D38 후보_순위 1 + GEN1-01-066: 동전 n개, f=x(x-a1)(x-a2), 극솟값의 최솟값 g(n)<=-32) =================
def loc_ext(f, kind):
    """다항식 f의 극솟값(kind='min') 또는 극댓값('max') 목록 — f'의 실근에서 부호 변화로 판정"""
    fp = sp.diff(f, x); out = []
    for r_ in set(sp.real_roots(fp)):
        e = R(1, 1000)
        l_, r2 = fp.subs(x, r_ - e), fp.subs(x, r_ + e)
        if kind == 'min' and l_ < 0 < r2: out.append(sp.nsimplify(f.subs(x, r_)))
        if kind == 'max' and l_ > 0 > r2: out.append(sp.nsimplify(f.subs(x, r_)))
    return out


def g13(n):
    """동전 n개: (a1, a2) 전수 → 극솟값을 갖는 경우의 극솟값 가운데 최솟값과 그때의 순서쌍.
    f=x(x-i)(x-j), f'=3x^2-2(i+j)x+ij. 판별식 D/4=(i+j)^2-3ij>0이면 큰 근에서 극소(실수 계산으로 고르고 최소인 쌍만 정확히 계산)."""
    cand = []
    for i in range(n + 1):
        for j in range(n + 1):
            D = (i + j)**2 - 3 * i * j
            if D <= 0: continue            # i=j=0뿐: 극값 없음
            s_ = ((i + j) + D**0.5) / 3
            cand.append((s_ * (s_ - i) * (s_ - j), i, j))
    lo = min(c[0] for c in cand)
    arg = [(i, j) for v, i, j in cand if abs(v - lo) < 1e-9]
    exact = {loc_ext(sp.expand(x * (x - i) * (x - j)), 'min')[0] for i, j in arg}
    return (exact.pop() if len(exact) == 1 else None), arg


G13 = {n: g13(n) for n in range(1, 10)}
check(13, all(G13[n][0] == -R(4 * n**3, 27) and sorted(G13[n][1]) == [(0, n), (n, 0)] for n in G13),
      'n=1..9 순서쌍 전수: g(n) = -4n^3/27, 최소는 (a1, a2)=(0, n), (n, 0)뿐')
check(13, loc_ext(x**3, 'min') == [] and loc_ext(sp.expand(x * (x - 3)**2), 'min') == [0], 'a1=a2=0이면 극값 없음, a1=a2=3이면 극솟값 0')
s_, n_ = sp.symbols('s_ n_', positive=True)
check(13, sp.solve(sp.diff(s_**2 * (n_ - s_), s_), s_) == [2 * n_ / 3] and sp.simplify((s_**2 * (n_ - s_)).subs(s_, 2 * n_ / 3) - 4 * n_**3 / 27) == 0,
      'y=x^2(n-x)의 최댓값은 x=2n/3에서 4n^3/27')
ok13 = [n for n in range(1, 60) if -R(4 * n**3, 27) <= -32]
ans13 = sp.Integer(min(ok13))
check(13, ans13 == 6 and G13[6][0] == -32 and G13[5][0] > -32 and ok13 == list(range(6, 60)), f'g(n)<=-32 ⇔ n>=6 (g(5)={G13[5][0]}, g(6)={G13[6][0]}), 최솟값 {ans13}')
ans_ok(13, ans13)
w_mid = min(n for n in range(1, 60) if (x**2 * (x - n)).subs(x, R(n, 2)) <= -32)      # 극소점을 중점 n/2로
w_third = min(n for n in range(1, 60) if (x**2 * (x - n)).subs(x, R(n, 3)) <= -32)   # 극소점을 n/3으로(원문 x(x-2)^2의 내분점)
check(13, w_mid == 7 and w_third == 8, f'오답: 중점 습관 -n^3/8 → {w_mid}, 내분점 n/3 습관 -2n^3/27 → {w_third}')
wrong_in(13, [w_mid, w_third], '극소점 중점 / 극소점 n/3')
# 원문 D38: 동전 2개, f=(x-a1)(x-a2)(x-2), 극댓값의 최댓값 32/27 → 59
o13 = max(m for i in range(3) for j in range(3) for m in loc_ext(sp.expand((x - i) * (x - j) * (x - 2)), 'max'))
check('D38', o13 == R(32, 27) and o13.p + o13.q == 59 == orig_ans('D38'), f'D38 원문: 극댓값의 최댓값 {o13}, p+q={o13.p + o13.q} = 원문 정답 {orig_ans("D38")}')
print('--- 13번 조건 빼 보기 ---')
ablation(13, "부등식의 등호(g(n)<-32로)", [min(n for n in range(1, 60) if -R(4 * n**3, 27) < -32)], 6, 'n=6에서 g(6)=-32로 등호 성립')
ablation(13, "'동전 n개'(n을 2로 고정, 원문)", [], 6, undef=f'g가 수 {G13[2][0]} 하나가 되어 n에 대한 부등식이 서지 않음')

# ================= 14번 (D9 후보_순위 2 + 조작_보강 2: 전환점 t, 3a-b의 최댓값 18 → t) =================
a, b = sp.symbols('a b', real=True)
tn = sp.symbols('tn', negative=True)
L14 = -x**3 - a * x**2 - b * x            # x<0
R14 = x**3 / 3 + a * x**2 - b * x         # x>=0
check(14, sp.diff(L14, x).subs(x, 0) == sp.diff(R14, x).subs(x, 0) == -b and L14.subs(x, 0) == R14.subs(x, 0) == 0, "x=0에서 연속, 좌·우미분계수 모두 -b(미분가능)")
b_t = sp.solve(sp.diff(L14, x).subs(x, tn), b)[0]
check(14, sp.expand(b_t - (-3 * tn**2 - 2 * a * tn)) == 0, f"f'(t)=0 → b={sp.expand(b_t)}")
dL = sp.factor(sp.diff(L14, x).subs(b, b_t)); dR = sp.expand(sp.diff(R14, x).subs(b, b_t))
check(14, sp.expand(dL + (x - tn) * (3 * x + 3 * tn + 2 * a)) == 0, f"x<0: f'(x)={dL} → 3t+2a<=0, a<=-3t/2")
vtx = sp.factor(dR.subs(x, -a))
check(14, sp.expand(vtx + (a - 3 * tn) * (a + tn)) == 0, f"x>0, a<0: 꼭짓점 값 f'(-a)={vtx} >= 0 → 3t<=a<=-t")


from fractions import Fraction as Fr


def feas14(av, tv, N=160):
    """a=av, 전환점 tv, b=-3t^2-2at에서 조건(감소·증가)을 도함수 부호로 직접 확인(분수 계산)"""
    av, tv = Fr(str(av)), Fr(str(tv))
    bv = -3 * tv**2 - 2 * av * tv
    d1 = lambda u: -3 * u * u - 2 * av * u - bv          # x<0
    d2 = lambda u: u * u + 2 * av * u - bv               # x>0
    if any(d1(tv - Fr(i, 16)) > 0 for i in range(1, N)): return False
    if any(d1(tv * (1 - Fr(i, N))) < 0 for i in range(1, N)): return False
    return not any(d2(Fr(i, 32)) < 0 for i in range(0, 32 * 20))


def range14(tv):
    fs = [R(i, 4) for i in range(-80, 80) if feas14(R(i, 4), tv)]
    return min(fs), max(fs), max(3 * av - (-3 * tv**2 - 2 * av * tv) for av in fs)


def H14(tv):
    """3a-b = 3t^2+(3+2t)a 의 3t<=a<=-3t/2 에서의 최댓값"""
    return max((3 * tv**2 + (3 + 2 * tv) * av) for av in (3 * tv, -R(3, 2) * tv))


grid_ok = True
for tv in (R(-1, 2), -1, R(-3, 2), -2, -3, -4, -5):
    lo_, hi_, mx_ = range14(tv)
    good = lo_ == 3 * tv and hi_ == -R(3, 2) * tv and mx_ == H14(tv)
    grid_ok &= good
    print(f'    t={tv}: 가능한 a(1/4 격자) [{lo_}, {hi_}], 3a-b 최댓값 {mx_}' + ('' if good else '  ← 불일치'))
check(14, grid_ok, 'a 격자 전수(도함수 부호 직접 확인): 범위 3t<=a<=-3t/2, 최댓값이 식과 일치')
check(14, not feas14(R(-25, 4), -2) and feas14(-6, -2) and feas14(3, -2) and not feas14(R(13, 4), -2), 't=-2: a=-6, 3은 가능, a=-25/4, 13/4는 불가능(양 끝 확인)')
tt = sp.symbols('tt', real=True)
sol1 = [s for s in sp.solve(sp.Eq(9 * tt**2 + 9 * tt, 18), tt) if s < -R(3, 2)]        # t<-3/2: a=3t에서 최대
sol2 = [s for s in sp.solve(sp.Eq(-R(9, 2) * tt, 18), tt) if -R(3, 2) <= s < 0]          # -3/2<=t<0: a=-3t/2에서 최대
check(14, sol1 == [-2] and sol2 == [] and H14(-2) == 18, f't<-3/2: 9t^2+9t=18 → {sol1}, -3/2<=t<0: -9t/2=18 → {sol2}(최댓값 <= 27/4)')
mono = all(H14(R(-i, 8)) < H14(R(-i - 1, 8)) for i in range(1, 80))
check(14, mono and [tv for tv in [R(-i, 8) for i in range(1, 81)] if H14(tv) == 18] == [-2], '최댓값은 t가 작아질수록 커지고(1/8 격자 -10..0), 18이 되는 t는 -2뿐')
ans14 = sp.Integer(-2)
ans_ok(14, ans14)
w_amax = sp.solve(sp.Eq(-R(9, 2) * tt, 18), tt)[0]                                      # 원문 습관: a의 최댓값 -3t/2 대입(b=0)
w_disc = [s for s in sp.solve(sp.Eq(3 * tt**2 + (3 + 2 * tt) * (-tt), 18), tt) if s < 0][0]   # 판별식을 실수 전체에: a<=-t, a=-t 대입
check(14, w_amax == -4 and w_disc == -3 and b_t.subs({a: -R(3, 2) * tn}) == 0, f'오답: a의 최댓값 대입 {w_amax}, 판별식 전체 적용 후 a=-t 대입 {w_disc}')
wrong_in(14, [w_amax, w_disc], 'a의 최댓값 대입 / 판별식을 실수 전체에 적용')
# 원문 D9: 계수 1/3, 전환점 -1 → b=2a-1, -1-sqrt2<=a<=1/2, a+b=3a-1 → M-m=9/2+3sqrt2 (③)
o_lo = min(sp.solve(-a**2 - 2 * a + 1, a)); o14 = sp.simplify(3 * (R(1, 2) - o_lo))
check('D9', o_lo == -1 - sp.sqrt(2) and sp.simplify(o14 - (R(9, 2) + 3 * sp.sqrt(2))) == 0 and orig_ans('D9') == r'\dfrac92+3\sqrt2',
      f'D9 원문: a∈[{o_lo}, 1/2], M-m={o14} = 원문 정답 {orig_ans("D9")}')
print('--- 14번 조건 빼 보기 ---')
# x>0에서의 증가 조건이 없으면 a>=3t가 사라짐: t<-3/2에서는 3a-b가 한없이 커지고, -3/2<=t<0에서는 최댓값 -9t/2<=27/4
no_right = [s_ for s_ in sp.solve(sp.Eq(-R(9, 2) * tt, 18), tt) if -R(3, 2) <= s_ < 0]
ablation(14, "'[t, ∞)에서 증가' 가운데 x>0 부분", no_right, -2, 'a>=3t가 없어져 t<-3/2에서는 3a-b의 최댓값이 없고, -3/2<=t<0에서는 최댓값이 27/4 이하라 18이 되는 t가 없음')
# 감소 조건이 없으면 f'(t)=0이 필요 없어 b를 한없이 작게 잡아도 [t, ∞)에서 증가(예: a=0, b=-100)
bigb = all(-3 * Fr(-2 * i, 100)**2 + 100 >= 0 for i in range(0, 101)) and all(Fr(i, 10)**2 + 100 >= 0 for i in range(0, 200))   # t=-2, a=0, b=-100: (-2, 0)과 x>0에서 f'>=0
check(14, bigb, '감소 조건을 빼면 t=-2, a=0, b=-100도 [t, ∞)에서 증가(3a-b=100>18)')
ablation(14, "'(-∞, t]에서 감소'", [], -2, undef="f'(t)=0이 필요 없어 b를 한없이 작게 잡을 수 있고(예: t=-2, a=0, b=-100) 3a-b의 최댓값이 없음")
ablation(14, "'최댓값이 18'", [sp.Integer(-2), sp.Integer(-3), sp.Integer(-4)], -2, 't가 정해지지 않음')

# ================= 15번 (I62 후보_순위 2 + GEN2-03-132 꼴에 계수 2) =================
A_, B_ = sp.symbols('A_ B_', real=True)
cs = sp.symbols('c0:5', real=True)


def solve15(coef=2, kx=3, sgn=-1, cond=True, diff=2, lower=1):
    """coef∫_lower^x t f = x^4 + sgn·a x^3 + kx·a x + b + ∫_lower^x x f, (cond) ∫_0^1 f - f(1) = diff. f는 4차 이하 일반 다항식으로 두고 계수 비교"""
    f = sum(c * x**i for i, c in enumerate(cs))
    ft = f.subs(x, t)
    lhs = coef * sp.integrate(t * ft, (t, lower, x))
    rhs = x**4 + sgn * A_ * x**3 + kx * A_ * x + B_ + x * sp.integrate(ft, (t, lower, x))
    eqs = sp.Poly(sp.expand(lhs - rhs), x).all_coeffs()
    if cond: eqs.append(sp.integrate(f, (x, 0, 1)) - f.subs(x, 1) - diff)
    sol = sp.solve(eqs, list(cs) + [A_, B_], dict=True)
    return [(s.get(A_, A_), s.get(B_, B_), sp.expand(f.subs(s))) for s in sol]


s15 = solve15()
check(15, len(s15) == 1 and s15[0][0] == 2 and s15[0][1] == -5 and sp.expand(s15[0][2] - (6 * x**2 - 12 * x + 10)) == 0, f'항등식 + 차 조건 → (a, b, f)={s15}(유일, 4차 이하 일반 다항식 계수 비교)')
a15, b15, f15 = s15[0]
ft15 = f15.subs(x, t)
check(15, sp.expand(2 * sp.integrate(t * ft15, (t, 1, x)) - (x**4 - a15 * x**3 + 3 * a15 * x + b15 + x * sp.integrate(ft15, (t, 1, x)))) == 0
      and sp.integrate(f15, (x, 0, 1)) - f15.subs(x, 1) == 2, '구한 f, a, b가 항등식과 차 조건을 만족')
# 풀이 단계: 한 번 미분 → xf(x)=4x^3-3ax^2+3a+∫_1^x f, f(1)=4, ∫_0^1 f=3a
check(15, sp.expand(x * f15 - (4 * x**3 - 3 * a15 * x**2 + 3 * a15 + sp.integrate(ft15, (t, 1, x)))) == 0 and f15.subs(x, 1) == 4 and sp.integrate(f15, (x, 0, 1)) == 3 * a15,
      '한 번 미분한 식 xf(x)=4x^3-3ax^2+3a+∫_1^x f 성립, f(1)=4, ∫_0^1 f=3a=6')
ans15 = a15 + f15.subs(x, 2)
check(15, ans15 == 12, f'a+f(2) = {a15}+{f15.subs(x, 2)} = {ans15}')
ans_ok(15, ans15)
# 오답: ⑤ 14 (x=1 대입에서 상수항 3a 누락: f(1)=4-3a → 3a-(4-3a)=2, a=1, f'=12x-6, f(1)=1) / ① 10 (a를 더하지 않음)
aw = sp.solve(sp.Eq(3 * A_ - (4 - 3 * A_), 2), A_)[0]
fw = 6 * x**2 - 6 * aw * x + ((4 - 3 * aw) - (6 - 6 * aw))
w_noc = aw + fw.subs(x, 2); w_om = f15.subs(x, 2)
check(15, aw == 1 and sp.expand(fw - (6 * x**2 - 6 * x + 1)) == 0 and w_noc == 14 and w_om == 10, f'오답: 상수항 3a 누락 a={aw}, f={sp.expand(fw)} → {w_noc}, a를 더하지 않음 {w_om}')
wrong_in(15, [w_noc, w_om], 'x=1 대입에서 3a 누락 / a 누락')
# 원문 I62: xf=2x^3+ax^2+3a+∫_1^x f, f(1)=∫_0^1 f → a=-2, f=3x^2-4x-5, a+f(3)=8 (④)
fo = sum(c * x**i for i, c in enumerate(cs[:4]))
eo = sp.Poly(sp.expand(x * fo - (2 * x**3 + A_ * x**2 + 3 * A_ + sp.integrate(fo.subs(x, t), (t, 1, x)))), x).all_coeffs() + [fo.subs(x, 1) - sp.integrate(fo, (x, 0, 1))]
so = sp.solve(eo, list(cs[:4]) + [A_], dict=True)
o15 = so[0][A_] + fo.subs(so[0]).subs(x, 3)
check('I62', len(so) == 1 and o15 == 8 and orig_ans('I62') == '8', f'I62 원문: a={so[0][A_]}, f={sp.expand(fo.subs(so[0]))}, a+f(3)={o15} = 원문 정답 {orig_ans("I62")}')
print('--- 15번 조건 빼 보기 ---')
fam = solve15(cond=False)
vals = [sp.expand(fa + ff.subs(x, 2)).subs(B_, bv) for fa, fb, ff in fam for bv in (-3, -5, -7)]
ablation(15, "'∫_0^1 f(t)dt-f(1)=2'", vals, 12, f'a가 정해지지 않음(a=-(b+1)/2): a+f(2)={sp.expand(fam[0][0] + fam[0][2].subs(x, 2))}')
ablation(15, "계수 2(∫_1^x t f(t)dt의 앞)", [fa + ff.subs(x, 2) for fa, fb, ff in solve15(coef=1)], 12, '계수가 1이면 0=4x^3-3ax^2+3a+∫_1^x f에서 a=4, f=-12x^2+24x가 되어 차 조건 ∫_0^1 f-f(1)=-4와 맞지 않음')
ablation(15, "'+3ax' 항", [fa + ff.subs(x, 2) for fa, fb, ff in solve15(kx=0)], 12, 'f의 상수항이 바뀜')
ablation(15, "아래끝 1(0으로)", [fa + ff.subs(x, 2) for fa, fb, ff in solve15(lower=0)], 12, 'x=0 대입에서 a=0, f=6x^2+C가 되어 차 조건과 맞지 않음')
ablation(15, "'-ax^3'의 부호(+로)", [fa + ff.subs(x, 2) for fa, fb, ff in solve15(sgn=1)], 12)
k15 = [sp.simplify(fa + fb + ff.subs(x, 2)) for kk in (0, 3, 5) for fa, fb, ff in solve15(kx=kk)]
check(15, len(set(k15)) == 1, f'(참고) a+b+f(2)는 3ax의 계수와 무관({set(k15)}) → 구하는 값을 a+f(2)로 둠')

# ================= 16번 (D67 결합 1: D47의 f' 최솟값 장치 + 폭 매개변수 k) =================
# f'(x) = 3/2((x-p)^2 - q): q>0이면 두 근 p±sqrt(q)(q는 유리수의 제곱만 씀), q=0이면 한 근, q<0이면 근 없음
def rt16(p_, q_):
    p_, q_ = Fr(str(p_)), Fr(str(q_))
    if q_ < 0: return []
    if q_ == 0: return [p_]
    w = Fr(sp.sqrt(sp.Rational(q_.numerator, q_.denominator)).p, sp.sqrt(sp.Rational(q_.numerator, q_.denominator)).q)
    assert w * w == q_
    return [p_ - w, p_ + w]


def fp16(u, p_, q_):
    return Fr(3, 2) * ((Fr(str(u)) - Fr(str(p_)))**2 - Fr(str(q_)))


def g16(tv, p_, q_, k_):
    tv, k_ = Fr(str(tv)), Fr(str(k_))
    return sum(1 for r_ in rt16(p_, q_) if tv <= r_ <= tv + k_)


def h16(tv, p_, q_, k_):
    tv, k_, pf = Fr(str(tv)), Fr(str(k_)), Fr(str(p_))
    if tv <= pf <= tv + k_: return fp16(pf, p_, q_)
    return min(fp16(tv, p_, q_), fp16(tv + k_, p_, q_))


def limsum16(p_, q_, k_):
    """(가)의 좌변 lim_{t→a+}g + lim_{t→a-}g 의 최댓값: g가 변하는 점(근, 근-k)과 그 사이 점에서 좌우 가까운 값의 합"""
    k_ = Fr(str(k_)); bp = sorted({r_ - d for r_ in rt16(p_, q_) for d in (0, k_)})
    if not bp: return 0
    pts = bp + [(u + w) / 2 for u, w in zip(bp, bp[1:])] + [bp[0] - 1, bp[-1] + 1]
    e = Fr(1, 10**6)
    return max(g16(c + e, p_, q_, k_) + g16(c - e, p_, q_, k_) for c in pts)


def ndisc16(p_, q_, k_):
    k_ = Fr(str(k_)); e = Fr(1, 10**6)
    return sum(1 for c in {r_ - d for r_ in rt16(p_, q_) for d in (0, k_)} if not (g16(c - e, p_, q_, k_) == g16(c, p_, q_, k_) == g16(c + e, p_, q_, k_)))


def hconst(p_, q_, k_, lo=2, hi=3, val=Fr(-3, 2)):
    return all(h16(lo + Fr(hi - lo) * Fr(i, 40), p_, q_, k_) == val for i in range(41))


def fcubic(p_, q_, c3, at=3):
    """f' = 3/2((x-p)^2-q), f(at)=c3"""
    Fx = sp.integrate(R(3, 2) * ((x - sp.nsimplify(p_))**2 - sp.nsimplify(q_)), x)
    return sp.expand(Fx - Fx.subs(x, at) + sp.nsimplify(c3))


def fv(f_, u):
    v = f_.subs(x, u)
    return Fr(v.p, v.q)


# (가)(나): 간격과 폭의 대소에 따른 극한의 합의 최댓값과 g=2인 t의 존재
tab = {name: (limsum16(4, q_, k_), any(g16(Fr(i, 8), 4, q_, k_) == 2 for i in range(0, 80)), ndisc16(4, q_, k_))
       for name, q_, k_ in [('간격<폭', 1, 3), ('간격=폭', 1, 2), ('간격>폭', 1, 1), ('근 하나', 0, 2), ('근 없음', -1, 2), ('간격=폭(4)', 4, 4), ('간격<폭(2)', Fr(1, 4), 2)]}
for nm, (ls, g2, nd) in tab.items(): print(f'    {nm}: 극한의 합의 최댓값 {ls}, g=2인 t {"있음" if g2 else "없음"}, 불연속점 {nd}개')
check(16, [nm for nm, (ls, g2, nd) in tab.items() if ls <= 2 and g2] == ['간격=폭', '간격=폭(4)'], '(가)이면서 g(t)=2인 t가 있는 것은 두 근의 간격 = k일 때뿐(이때 불연속점 3개)')
# 전수: q(최솟값 -3q/2), k, p 격자에서 (가)(다)를 만족시키고 g=2인 t가 있는 경우
QS = [-1, 0, Fr(1, 4), 1, Fr(9, 4), 4]; KS = [Fr(1, 2), 1, Fr(3, 2), 2, 3, 4, 5]; PS = [Fr(i, 4) for i in range(0, 37)]
s_gd = [(p_, q_, k_) for q_ in QS for k_ in KS for p_ in PS if limsum16(p_, q_, k_) <= 2 and hconst(p_, q_, k_)]
check(16, s_gd and {q_ for p_, q_, k_ in s_gd} == {1} and {k_ for p_, q_, k_ in s_gd} == {1, Fr(3, 2), 2} and all(3 <= p_ <= k_ + 2 for p_, q_, k_ in s_gd),
      f'(가)(다) 격자 전수(q 6개 × k 7개 × p 37개): q=1(최솟값 -3/2, 간격 2), k<=2, 3<=p<=k+2 ({len(s_gd)}개)')
surv = [(p_, q_, k_) for p_, q_, k_ in s_gd if any(g16(r_ - d, p_, q_, k_) == 2 for r_ in rt16(p_, q_) for d in (0, k_))]
check(16, {k_ for p_, q_, k_ in surv} == {2} and sorted(p_ for p_, q_, k_ in surv) == [Fr(i, 4) for i in range(12, 17)], f'여기에 (나)의 g=2인 t가 있어야 하므로 k=2, 3<=p<=4만 남음({len(surv)}개)')
# (나): g(t)=2 ⇔ t=α=p-1 → f(3)=f(6)=p-1
pp = sp.symbols('pp', real=True)
d36 = sp.factor(sp.integrate(R(3, 2) * ((x - pp)**2 - 1), (x, 3, 6)))
psol = sorted(sp.solve(d36, pp))
check(16, sp.expand(d36 - R(9, 2) * (pp - 4) * (pp - 5)) == 0 and psol == [4, 5], f'f(6)-f(3)={d36}=0 → p={psol}')
check(16, [tv for tv in [Fr(i, 8) for i in range(0, 60)] if g16(tv, 4, 1, 2) == 2] == [3], 'p=4, k=2: g(t)=2인 t는 작은 근 3뿐(1/8 격자)')


def all_ok(p_, q_, k_, f_, use=('가', '나3', '나6', '다')):
    if '가' in use and limsum16(p_, q_, k_) > 2: return False
    if '나3' in use and g16(fv(f_, 3), p_, q_, k_) != 2: return False
    if '나6' in use and g16(fv(f_, 6), p_, q_, k_) != 2: return False
    if '다' in use and not hconst(p_, q_, k_): return False
    return True


final = [(p_, fcubic(p_, 1, p_ - 1)) for p_ in psol if all_ok(p_, 1, 2, fcubic(p_, 1, p_ - 1))]
f16 = final[0][1]
check(16, len(final) == 1 and final[0][0] == 4 and sp.expand(f16 - (R(1, 2) * (x - 3)**2 * (x - 6) + 3)) == 0 and sp.LC(f16, x) == R(1, 2),
      f'조건을 모두 만족시키는 f는 하나: p=4, f={sp.factor(f16 - 3)}+3')
ans16 = 2 + f16.subs(x, 5)
check(16, ans16 == 3, f'k+f(5) = 2+{f16.subs(x, 5)} = {ans16}')
ans_ok(16, ans16)
# 오답: ⑤ 7 (다른 후보 p=5, α=4) / ③ 5 (g(t)=2인 t를 큰 근 β=5로: f(3)=f(6)=5)
fB = fcubic(5, 1, 4); fb_ = fcubic(4, 1, 5)
w_B = 2 + fB.subs(x, 5); w_beta = 2 + fb_.subs(x, 5)
check(16, sp.expand(fB - (R(1, 2) * (x - 3) * (x - 6)**2 + 4)) == 0 and not hconst(5, 1, 2) and all_ok(5, 1, 2, fB, use=('가', '나3', '나6')) and w_B == 7 and fb_.subs(x, 6) == 5 and w_beta == 5,
      f'오답: 다른 후보 p=5(f(3)=f(6)=4, (가)(나)는 만족·(다) 불성립) → {w_B}, t=큰 근 착각 f(3)=f(6)=5 → {w_beta}')
wrong_in(16, [w_B, w_beta], '(다)로 거르지 않은 다른 후보 / g(t)=2인 t를 큰 근으로')
# 원문 D67: [t,t+2], f(1)=f(4)=α, g(f(0))=1 → f(5)=9
oc = []
for al in sp.solve(sp.integrate(R(3, 2) * (x - pp) * (x - pp - 2), (x, 1, 4)), pp):
    fo_ = fcubic(al + 1, 1, al, at=1)
    if g16(fv(fo_, 1), al + 1, 1, 2) == g16(fv(fo_, 4), al + 1, 1, 2) == 2 and g16(fv(fo_, 0), al + 1, 1, 2) == 1 and limsum16(al + 1, 1, 2) <= 2: oc.append(fo_.subs(x, 5))
check('D67', oc == [9] and orig_ans('D67') == 9, f'D67 원문: f(5)={oc} = 원문 정답 {orig_ans("D67")}')
print('--- 16번 조건 빼 보기 ---')
check(16, all_ok(4, 1, 2, f16), '정답 함수는 (가)(나)(다)를 모두 만족')
# (가) 없음: k=3, p=4, f(3)=f(6)=c (2<=c<=3) 등도 가능
vals = [k_ + fcubic(4, 1, c).subs(x, 5) for k_, c in [(2, 3), (3, 2), (3, R(5, 2)), (3, 3)] if all_ok(4, 1, k_, fcubic(4, 1, c), use=('나3', '나6', '다'))]
ablation(16, '(가)', vals, 3, 'k=3이면 g(t)=2인 t가 2<=t<=3 전체가 되어 f(3)=f(6)의 값과 k가 정해지지 않음')
# g(f(3))=2 없음: f(6)=p-1, 3<=p<=4
vals = [2 + f_.subs(x, 5) for p_ in (3, R(7, 2), 4) for f_ in [fcubic(p_, 1, p_ - 1, at=6)] if all_ok(p_, 1, 2, f_, use=('가', '나6', '다'))]
ablation(16, "(나) 'g(f(3))=2'", vals, 3, 'p가 3<=p<=4에서 정해지지 않음')
vals = [2 + f_.subs(x, 5) for p_ in (3, R(7, 2), 4) for f_ in [fcubic(p_, 1, p_ - 1)] if all_ok(p_, 1, 2, f_, use=('가', '나3', '다'))]
ablation(16, "(나) 'g(f(6))=2'", vals, 3, 'p가 3<=p<=4에서 정해지지 않음')
# (다) 없음: 폭 k와 간격이 같으면 (가)를 만족. k=2(α=3, 4) 말고도 k=3(α=3±sqrt(6)/2) 등에서 f(3)=f(6)=α
al_ = sp.symbols('al_', real=True)
vals = []
for k_ in (2, 3):
    for al in sp.solve(sp.integrate(R(3, 2) * (x - al_) * (x - al_ - k_), (x, 3, 6)), al_):
        Fx = sp.integrate(R(3, 2) * (x - al) * (x - al - k_), x); f_ = sp.expand(Fx - Fx.subs(x, 3) + al)
        good = sp.simplify(f_.subs(x, 6) - al) == 0          # f(3)=f(6)=α(작은 근), 간격 = k → g(α)=2, (가) 성립
        if good: vals.append(sp.nsimplify(sp.simplify(k_ + f_.subs(x, 5))))
ablation(16, '(다)', vals, 3, 'k와 두 근의 위치가 정해지지 않음')
vals = [2 + f_.subs(x, 5) for p_, f_ in [(4, f16), (5, fB)] if all_ok(p_, 1, 2, f_, use=('가', '나3', '나6'))]
ablation(16, "(다)의 구간 [2, 3](최솟값 -3/2만 남김)", vals, 3, '두 후보 p=4, 5를 거르지 못함')
# (다)의 값: 최솟값이 -6이면 간격 4, k=4, 3<=p<=6 → f(3)=f(6)=p-2를 만족시키는 p가 범위에 없음
c4 = [al + 2 for al in sp.solve(sp.integrate(R(3, 2) * (x - al_) * (x - al_ - 4), (x, 3, 6)), al_) if 3 <= al + 2 <= 6]
ablation(16, "(다)의 값 -3/2(-6으로)", c4, 3, '간격 4, k=4, 3<=p<=6에서 f(3)=f(6)=p-2인 p가 없음')
# 폭을 원문처럼 2로 고정해도 답은 같지만, k를 문자로 두면 (다)의 간격 2와 (가)(나)의 '간격 = k'를 이어야 k가 정해짐
check(16, {k_ for p_, q_, k_ in surv} == {2}, '(참고) 폭 k는 (가)(나)(다)를 함께 써야 2로 정해짐(k<2는 (나), k>2는 (가)에 어긋남)')

print('ALL OK' if ok else 'SOME FAIL')
