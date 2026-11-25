# -*- coding: utf-8 -*-
# 10.5회 새 6–10번(hB.py) 검증: 정답 유일성 · 선지 등차 · 오답 실수 경로 · 조건 빼 보기 · 원래 문항과 다른 답 · 목표 정답 위치
import os, re, sys, math, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'hB.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
x, a, k, t = sp.symbols('x a k t', real=True)
WANT = {6: 3, 7: 4, 8: 1, 9: 5, 10: 2}
ORIG_ANS = {6: '7', 7: 'T:ㄱ, ㄴ', 8: '-27', 9: '6', 10: '3'}


def ablation(no, name, res, ans):
    print(f'ABLATION {no} {name}: 필요({res})'); assert res != ans


def nroots(e):
    return len(set(sp.real_roots(sp.Poly(sp.expand(e), x))))


# ---------- 공통 형식
assert set(IT) == set(WANT)
for n, it in IT.items():
    for kk in ('body', 'choices', 'ans', 'sol', 'fast', 'wrong', 'wrongs', 'level', 'key', 'src', 'note'):
        assert kk in it, (n, kk)
    assert it['ans'] == WANT[n], (n, it['ans'])
    assert all(w in it['choices'] for w in it['wrongs']) and it['choices'][it['ans'] - 1] not in it['wrongs']
    assert it['choices'][it['ans'] - 1] != ORIG_ANS[n]
    texts = [it[kk] for kk in ('body', 'sol', 'fast', 'wrong', 'note')] + [c for _, c in it.get('cond', [])] + [c for _, c in it.get('bogi', [])]
    for s_ in texts:
        assert '이러한' not in s_
        assert not re.search(r'\\\((?:(?!\\\)).)*?[<>](?:(?!\\\)).)*?\\\)', s_, re.S), (n, s_[:60])
    if not it['choices'][0].startswith('T:'):
        v = [int(c) for c in it['choices']]
        assert len({v[i + 1] - v[i] for i in range(4)}) == 1 and len(set(v)) == 5
print('형식 OK: 목표 정답 위치', WANT, '· 원래 답과 다름 · 부등호 &lt;&gt; · 숫자 선지 등차')

# ================= 6번 (9회 12번, I37) =================
it = IT[6]; C6, L6, W6, M6, P6 = 1, 6, 2, 3, 4


def I(g, lo, hi):
    return sp.integrate(g, (x, lo, hi))


def absint(g, lo, hi):
    cuts = [lo] + sorted(p for p in sp.Poly(sp.expand(g), x).real_roots() if lo < p < hi) + [hi]
    return sum(abs(I(g, cuts[i], cuts[i + 1])) for i in range(len(cuts) - 1))


def ga_ok(g, av, L=L6):
    return sp.simplify(absint(g, 0, L) - (I(g, 0, av) - I(g, av, L))) == 0


def na_ok(g, av, m=M6, w=W6, L=L6):
    X = I(g, 0, L); Y = m * I(g, av - w, av)
    return abs(X) <= Y


grid_a = [R(j, 4) for j in range(1, 24)]
grid_r = sorted(set([R(j, 4) for j in range(-24, 49)]))
for av in grid_a[::2]:
    sols = [(kk, rv) for kk in (C6, -C6) for rv in set(grid_r) | {av} if ga_ok(kk * x * (x - rv), av)]
    assert sols == [(-C6, av)], (av, sols)
print('6: (가) → f = -x(x-a) 유일(격자)')
f6 = -C6 * x * (x - a)
Y = sp.expand(I(f6, a - W6, a)); assert Y == sp.expand(I(f6, 0, W6)) == 2 * a - R(8, 3)
X = sp.expand(I(f6, 0, L6)); assert X == 18 * a - 72
S = sp.Intersection(sp.solve_univariate_inequality(M6 * Y - X >= 0, a, relational=False),
                    sp.solve_univariate_inequality(M6 * Y + X >= 0, a, relational=False), sp.Interval.open(0, L6))
assert S == sp.Interval(R(10, 3), R(16, 3)), S
good = [R(j, 60) for j in range(1, 360) if na_ok(f6.subs(a, R(j, 60)), R(j, 60))]
assert good[0] == R(10, 3) and good[-1] == R(16, 3) and len(good) == 121
fP = sp.expand(f6.subs(x, P6)); assert fP == 4 * a - 16


def cnt6(Sa, g=fP):
    img = sp.Interval(g.subs(a, Sa.inf), g.subs(a, Sa.sup), Sa.left_open, Sa.right_open)
    ii = sp.Intersection(img, sp.S.Integers)
    return len(list(ii)) if ii.is_finite_set else 'inf'


A6 = cnt6(S); assert A6 == 8 and str(A6) == it['choices'][it['ans'] - 1]
for v in range(-2, 6):
    av = sp.solve(fP - v, a)[0]; assert av in S and na_ok(f6.subs(a, av), av)
w_ge0 = cnt6(sp.Interval(sp.solve(X, a)[0], R(16, 3)))
w_noup = cnt6(sp.Interval.Ropen(R(10, 3), L6))
assert (w_ge0, w_noup) == (6, 10) and set(it['wrongs']) == {'6', '10'}
assert it['choices'].index('10') == 4                                  # 위 끝 빼먹은 값 ⑤(원래 학생 자리)
print('6: 10/3 ≤ a ≤ 16/3, f(4)=4a-16 → 정답 OK, 오답 6(적분≥0)·10(위 끝 빼먹음)')
# 빼 보기
gw = C6 * x * (x - L6); aw = R(1, 100)
assert not ga_ok(gw, aw) and na_ok(gw, aw) and gw.subs(x, P6) != 0 and gw.subs(x, P6) < -R(8, 3)
ablation(6, '(가)', f'정해지지 않음: f=x(x-6), a=1/100이 (나)를 만족, f(4)={gw.subs(x, P6)}', A6)
g = -C6 * (x - a) * (x + 1)
vals = [g.subs({x: P6, a: av}) for av in [R(j, 30) for j in range(1, 180)] if ga_ok(g.subs(a, av), av) and na_ok(g.subs(a, av), av)]
assert vals and (min(vals) < -R(8, 3) or max(vals) > R(16, 3))
ablation(6, 'f(0)=0', f'정해지지 않음: f=-(x-a)(x+1)이면 f(4) 범위 [{min(vals)}, {max(vals)}]', A6)
g2 = -2 * x * (x - a)
S2 = sp.Intersection(sp.solve_univariate_inequality(M6 * I(g2, a - W6, a) - I(g2, 0, L6) >= 0, a, relational=False),
                     sp.solve_univariate_inequality(M6 * I(g2, a - W6, a) + I(g2, 0, L6) >= 0, a, relational=False), sp.Interval.open(0, L6))
ablation(6, '계수의 절댓값 1(→2)', cnt6(S2, sp.expand(g2.subs(x, P6))), A6)
ablation(6, '(나)의 절댓값', cnt6(sp.Intersection(sp.solve_univariate_inequality(M6 * Y - X >= 0, a, relational=False), sp.Interval.open(0, L6))), A6)
ablation(6, '(나)의 바깥 계수 3(→1)', cnt6(sp.Intersection(sp.solve_univariate_inequality(Y - X >= 0, a, relational=False),
                                                     sp.solve_univariate_inequality(Y + X >= 0, a, relational=False), sp.Interval.open(0, L6))), A6)
for wv in (1, 3):
    Yw = sp.expand(I(f6, a - wv, a))
    ablation(6, f'(나)의 구간 끝 a-2(→a-{wv})', cnt6(sp.Intersection(sp.solve_univariate_inequality(M6 * Yw - X >= 0, a, relational=False),
                                                     sp.solve_univariate_inequality(M6 * Yw + X >= 0, a, relational=False), sp.Interval.open(0, L6))), A6)
ablation(6, '(나) 전체', cnt6(sp.Interval.open(0, L6)), A6)
# 범위 선언 0<a<6 삭제: a ≥ 6에서 f=x(x-r), a=3r/2 (r≥6)가 (가)·(나)를 만족 → f(4)=4(4-r) 아래로 유계 아님
for rv in (6, 8, 20):
    g = C6 * x * (x - rv); av = R(3, 2) * rv
    assert av >= 6 and ga_ok(g, av) and na_ok(g, av)
ablation(6, '범위 선언 0<a<6', 'inf: f=x(x-r), a=3r/2(r≥6)에서 f(4)=4(4-r)', A6)
# 원래 수치(9회 12번)로 되돌리면 7
f0 = -2 * x * (x - a)
S0 = sp.Intersection(sp.solve_univariate_inequality(3 * I(f0, a - 1, a) - I(f0, 0, 3) >= 0, a, relational=False),
                     sp.solve_univariate_inequality(3 * I(f0, a - 1, a) + I(f0, 0, 3) >= 0, a, relational=False), sp.Interval.open(0, 3))
assert cnt6(S0, sp.expand(f0.subs(x, 3))) == 7
print('6: 원래 수치로 7(9회 12번 답) 재현, 새 답과 다름')

# ================= 7번 (10회 12번, M60) =================
it = IT[7]
A_, B_ = sp.symbols('A B', real=True)
assert [b[0] for b in it['bogi']] == ['ㄱ', 'ㄴ', 'ㄷ'] and it['choices'] == ['T:ㄱ', 'T:ㄱ, ㄴ', 'T:ㄱ, ㄷ', 'T:ㄴ, ㄷ', 'T:ㄱ, ㄴ, ㄷ']
CONST, BOUND, ABOUND = 2, 14, 4


def ok7(av, bv, const=CONST, bound=BOUND, neg_only=True):
    fpp = 3 * x**2 + 2 * av * x + bv
    rts = sp.Poly(fpp, x).real_roots()
    if not rts: return False
    if neg_only and not all(r_ < 0 for r_ in rts): return False
    ff = x**3 + av * x**2 + bv * x + const
    return I(sp.diff(ff, x), -1, 1) > bound


def stmts(av, bv, const=CONST):
    ff = x**3 + av * x**2 + bv * x + const
    s1 = nroots(ff - bv * x) == 2
    s2 = all(r_ < 0 for r_ in sp.Poly(ff, x).real_roots())
    s3 = av > ABOUND
    return (s1, s2, s3)


samples = [(R(i, 2), R(j, 2)) for i in range(0, 41) for j in range(0, 61)]
adm = [(av, bv) for av, bv in samples if ok7(av, bv)]
assert len(adm) > 100
res = {stmts(av, bv) for av, bv in adm}
assert res == {(False, True, True)}, res
# 문장 ㄷ 경계: a^2 ≥ 3b > 18 이므로 a > 3√2 > 4, 그러나 a > 5는 참이 아님(예 a=9/2, b=13/2)
assert ok7(R(9, 2), R(13, 2)) and R(9, 2) <= 5
print('7: 허용 (a,b)', len(adm), '개 모두 ㄱ 거짓·ㄴ 참·ㄷ 참 → ㄴ, ㄷ(④)')
# 오답 경로
av, bv = 6, 7
assert ok7(av, bv)
assert nroots(x**2 * (x + av)) == 2                         # 원문처럼 x^2(x+a) → ㄱ 참 → ⑤
assert stmts(av, bv, const=0) == (True, False, True)        # 상수항 놓침 → ㄱ 참, ㄴ 거짓 → ③
print('7: 오답 ⑤(x^2(x+a)로 실근 2개), ③(상수항 놓침) 재현')
# 빼 보기
r_c0 = {stmts(a_, b_, const=0) for a_, b_ in adm[::7]}
ablation(7, '상수항 2(→0)', r_c0, {(False, True, True)})
adm_nn = [(a_, b_) for a_, b_ in [(R(i, 2), R(j, 2)) for i in range(-20, 21, 2) for j in range(-10, 40, 3)] if ok7(a_, b_, neg_only=False)]
ablation(7, "'x좌표가 음수인 점에서만'", {stmts(a_, b_) for a_, b_ in adm_nn}, {(False, True, True)})
adm_lo = [(a_, b_) for a_, b_ in samples[::3] if ok7(a_, b_, bound=2)]
ablation(7, '정적분 조건 &gt;14(→&gt;2)', {stmts(a_, b_) for a_, b_ in adm_lo}, {(False, True, True)})
print('7: 원래 그림(아래로 볼록, 두 근 음수)과 같은 모양: 예 a=6, b=7 →', sp.Poly(3 * x**2 + 12 * x + 7, x).nroots())

# ================= 8번 (10회 15번, I75) =================
it = IT[8]


def p_set(fx, lo=-6, hi=10):
    """∫_{3p}^{3p+3}|f| ≠ |∫f| ⇔ (3p,3p+3)에서 부호가 바뀜 → 그런 p의 집합(부호 변화점 r마다 ((r-3)/3, r/3))"""
    P = sp.Poly(sp.expand(fx), x)
    sc = [r_ for r_ in set(P.real_roots()) if sp.sign(fx.subs(x, r_ - R(1, 1000))) != sp.sign(fx.subs(x, r_ + R(1, 1000)))]
    return sp.Union(*[sp.Interval.open((r_ - 3) / 3, r_ / 3) for r_ in sc]) if sc else sp.S.EmptySet


def q_set(fx, lo=0, hi=6):
    cr = [lo, hi] + [r_ for r_ in sp.Poly(sp.diff(fx, x), x).real_roots() if lo < r_ < hi]
    vals = [fx.subs(x, z) for z in cr]
    return sp.Interval.open(-max(vals), -min(vals))


cc = sp.symbols('cc', real=True)
# 상수항 0인 삼차함수 c·x·(x-r)(x-s): 근 격자 전수에서 p 집합이 (1,2)인 것은 c x^2 (x-6)뿐
found = set()
for r_, s_ in itertools.combinations_with_replacement([R(j, 2) for j in range(-8, 21)], 2):
    for c_ in (1, -1):
        g = c_ * x * (x - r_) * (x - s_)
        if p_set(g) == sp.Interval.open(1, 2):
            found.add((r_, s_))
assert found == {(0, 6)}, found
f8 = cc * x**2 * (x - 6)
cands = []
for c_ in [R(j, 4) for j in range(-16, 17) if j]:
    if q_set(f8.subs(cc, c_)) == sp.Interval.open(-64, 0):
        cands.append(c_)
assert cands == [-2], cands
A8 = (-2 * x**2 * (x - 6)).subs(x, 3); assert A8 == 54 and str(A8) == it['choices'][it['ans'] - 1]
print('8: f = -2x^2(x-6) 유일(근·계수 격자) → f(3) =', A8)
assert (f8.subs({cc: -2})).subs(x, 4) == 64 and it['wrongs'] == ['64']
print('8: 오답 64(최댓값 f(4)=64를 구간 가운데 f(3)으로 착각)')
assert p_set(-2 * (x - 6) * (x**2 + 1)) == sp.Interval.open(1, 2)
g_alt = -2 * (x - 6) * (x**2 + 1)
ablation(8, '상수항 0', f'정해지지 않음(f=-2(x-6)(x^2+1)도 p 범위 (1,2), q 범위 {q_set(g_alt)})', A8)
g_p = -x * (x - 3) * (x - 6); assert p_set(g_p) != sp.Interval.open(1, 2)
g_p2 = -R(16, 27) * x**2 * (x - 9); assert q_set(g_p2) == sp.Interval.open(-64, 0) and g_p2.subs(x, 3) != A8
ablation(8, 'p 범위(1<p<2) 삭제', f'정해지지 않음(f=-16/27·x^2(x-9)도 q 범위 (-64,0), f(3)={g_p2.subs(x, 3)})', A8)
for c_ in (-1, -3):
    assert q_set(f8.subs(cc, c_)) != sp.Interval.open(-64, 0)
ablation(8, 'q 범위(-64<q<0) 삭제', f'계수 c 미정: f(3)=-27c', A8)
# 창 폭 3 < 근 간격 6: 0이 단순근이면 (-1,0)이 더 생김
assert p_set(-x * (x - 6) * (x + 5)).contains(R(-1, 2))
# 원래 수치(10회 15번)
f0 = x**2 * (x - 6); assert f0.subs(x, 3) == -27
print('8: 원래 답 -27과 다름, 0 단순근이면 (-1,0) 추가 확인')

# ================= 9번 (10회 17번, M32) =================
it = IT[9]
N9, S9 = 18, 4
f9 = x**2 * (x - N9); fp9 = sp.diff(f9, x)
for rv in [R(n, 2) for n in range(-40, 41)]:
    g = x * (x - rv)
    assert all(g.subs(x, z) >= 0 for z in [R(n, 4) for n in range(-80, 81)]) == (rv == 0)
h = f9 - (x - k + S9) * fp9.subs(x, k)
assert sp.factor(sp.diff(h, x)) == sp.factor(3 * (x - k) * (x + k - 12))
hk = sp.factor(h.subs(x, k)); hs = sp.factor(sp.expand(h.subs(x, 12 - k)))
assert sp.expand(hk - k * (k - 6) * (k - 24)) == 0 and sp.expand(hs - (k - 12) * (k - 6) * (5 * k - 12)) == 0
assert sp.expand(fp9.subs(x, 12 - k) - fp9.subs(x, k)) == 0
S3 = sp.solve_univariate_inequality(sp.expand(hk * hs) < 0, k, relational=False)
assert S3 == sp.Union(sp.Interval.open(0, R(12, 5)), sp.Interval.open(12, 24)), S3
assert sp.factor(h.subs(k, 6)) == sp.factor((x - 6)**3)          # k=6: 변곡점에서의 접선, 실근 1개
for kv in (0, R(12, 5), 12, 24):
    assert nroots(h.subs(k, kv)) == 2
for kv in [R(n, 5) for n in range(-50, 160)]:
    assert (nroots(h.subs(k, kv)) == 3) == bool(S3.contains(kv)), kv


def count9(f_, s_, want=3, lo=-80, hi=80):
    fp_ = sp.diff(f_, x)
    out = [kv for kv in range(lo, hi + 1) if nroots(f_ - (x - kv + s_) * fp_.subs(x, kv)) == want]
    return 'inf' if out and (out[0] == lo or out[-1] == hi) else out


ints = count9(f9, S9); assert ints == [1, 2] + list(range(13, 24)), ints
A9 = len(ints); assert A9 == 13 and str(A9) == it['choices'][it['ans'] - 1]
v = [int(c) for c in it['choices']]; assert v == sorted(v, reverse=True) and v[0] - v[1] == 1
w_ge2 = [kv for kv in range(-80, 81) if nroots(h.subs(k, kv)) >= 2]
S_le = sp.solve_univariate_inequality(sp.expand(hk * hs) <= 0, k, relational=False)
w_le = [kv for kv in range(-80, 81) if S_le.contains(kv)]
assert len(w_ge2) == 16 and 6 in w_le and len(w_le) == 17 and set(it['wrongs']) == {'16', '17'}
print('9: 정수 k', ints, '→', A9, '· 오답 16(끝점 포함)·17(곱≤0, k=6 포함) · k=6은 실근 1개')


def a9(f_, s_=S9, want=3):
    L = count9(f_, s_, want); return L if L == 'inf' else len(L)


alts = {str(g): a9(g) for g in (x**3, x**2 * (x - 9), x * (x - 6) * (x - 18), f9)}
assert len(set(alts.values())) > 1
ablation(9, '(가)', f'정해지지 않음 {alts}', A9)
alts = {str(g): a9(g) for g in ((x - 18)**3, (x - 18) * (x - 6)**2, (x - 18) * x**2)}
assert len(set(alts.values())) > 1
ablation(9, '(나)', f'정해지지 않음 {alts}', A9)
ablation(9, '(가)의 18(→9)', a9(x**2 * (x - 9)), A9)
ablation(9, '직선의 +4(→2)', a9(f9, 2), A9)
ablation(9, '직선의 +4(→0)', a9(f9, 0), A9)
ablation(9, '개수 3(→2)', a9(f9, S9, 2), A9)
assert a9(x**2 * (x - 9), 2) == 6
print('9: 원래 수치(9, +2)로 6 재현, 새 답과 다름')

# ================= 10번 (10회 18번, M34) =================
it = IT[10]
SUM, J, V, ASK = R(1, 2), -1, 3, 1


def crit_levels(f_):
    return sorted(set(f_.subs(x, r_) for r_ in sp.Poly(sp.diff(f_, x), x).real_roots()))


def simple_roots(g):
    P = sp.Poly(sp.expand(g), x)
    return [r_ for r_ in set(P.real_roots()) if P.diff(x).eval(r_) != 0]


def tset_h1(f_):
    """h(t)=1인 t 전체: 임계 높이가 아니면 실근이 모두 단순이고 개수가 짝수 → h≠1. 임계 높이 y마다 단순근이 1개인지 보고 f(t)=y인 t를 모음"""
    out = set()
    for y in crit_levels(f_):
        if len(simple_roots(f_ - y)) == 1:
            out |= set(sp.Poly(sp.expand(f_ - y), x).real_roots())
    return out


def h_def(f_, tv):          # 정의대로: |f(x)-f(t)|가 미분가능하지 않은 점 = 단순근
    return len(simple_roots(f_ - f_.subs(x, tv)))


def fmin(f_):
    return min(f_.subs(x, r_) for r_ in sp.Poly(sp.diff(f_, x), x).real_roots())


# 일반 사차식 x^4 + A x^3 + B x^2 + d (f'(0)=0) 격자 전수(수치, 근을 1e-4로 묶어 중복도 판정): 합 조건을 만족시키는 (A,B)는 두 갈래뿐
import numpy as np


def tsum_num(Av, Bv, tol=1e-4):
    co = [1.0, float(Av), float(Bv), 0.0, 0.0]
    dco = [4.0, 3 * float(Av), 2 * float(Bv), 0.0]
    crit = [z.real for z in np.roots(dco) if abs(z.imag) < 1e-7]
    levels = sorted(set(round(np.polyval(co, z), 9) for z in crit))
    ts = []
    for y in levels:
        rr = sorted(z.real for z in np.roots([1.0, float(Av), float(Bv), 0.0, -y]) if abs(z.imag) < 1e-3)
        cl = []
        for z in rr:
            if cl and abs(z - cl[-1][-1]) < tol * 30: cl[-1].append(z)
            else: cl.append([z])
        simple = [c_ for c_ in cl if len(c_) == 1]
        if len(simple) == 1:
            ts += [sum(c_) / len(c_) for c_ in cl]
    return ts


hits = []
for Ai in range(-24, 25):
    for Bi in range(-24, 25):
        Av, Bv = R(Ai, 8), R(Bi, 8)
        ts = tsum_num(Av, Bv)
        if ts and abs(sum(ts) - 0.5) < 1e-6:
            hits.append((Av, Bv))
br1 = sp.Poly(sp.expand(x**3 * (x - R(1, 2))), x).all_coeffs()
br2 = sp.Poly(sp.expand((x - R(3, 4))**3 * (x + R(1, 4))), x).all_coeffs()
want_hits = {(br1[1], br1[2]), (br2[1], br2[2])}
assert set(hits) == want_hits, (hits, want_hits)
assert sum(tset_h1(sp.expand((x - R(3, 4))**3 * (x + R(1, 4))))) == SUM
print('10: (가)+f\'(0)=0 → 두 갈래 x^3(x-1/2)+c, (x-3/4)^3(x+1/4)+c (격자 전수)')
sols = []
for f0_ in (x**3 * (x - R(1, 2)), (x - R(3, 4))**3 * (x + R(1, 4))):
    c_ = V - f0_.subs(x, J); f_ = sp.expand(f0_ + c_)
    assert sp.diff(f_, x).subs(x, 0) == 0 and f_.subs(x, J) == V and sum(tset_h1(f_)) == SUM
    for tv in tset_h1(f_):
        assert h_def(f_, tv) == 1
    sols.append((c_, fmin(f_), f_.subs(x, ASK)))
assert sols[0][0] == R(3, 2) and sols[1][0] == -R(261, 256)
assert sols[0][1] == R(3, 2) - R(27, 4096) and sols[0][1] > 0 and sols[1][1] == -R(9, 8)
surv = [s_ for s_ in sols if s_[1] > 0]; assert len(surv) == 1
A10 = surv[0][2]; assert A10 == 2 and str(A10) == it['choices'][it['ans'] - 1]
print('10: (다)로 극소점 갈래 지움 → f(1) =', A10)
# 오답
assert sols[1][2] == -1
fh = (x - 1)**3 * (x + R(1, 2)); ch_ = V - fh.subs(x, J); assert (fh + ch_).subs(x, 1) == -1 and sp.diff(fh, x).subs(x, 0) != 0
c_sign = V + R(3, 2)                                  # f(-1)의 (-1)^3(-3/2)를 -3/2로 계산
assert (x**3 * (x - R(1, 2)) + c_sign).subs(x, 1) == 5
assert set(it['wrongs']) == {'-1', '5'}
print('10: 오답 -1(버려지는 갈래, (x-1)^3 습관)·5(상수 계산 부호 실수)')
# 빼 보기
ablation(10, '(다)', {s_[2] for s_ in sols}, {A10})
qq = sp.symbols('qq')
fq = x**3 * (x - qq); cq = V - fq.subs(x, J)
vals = {sp.simplify((fq + cq).subs(x, ASK)).subs(qq, qv) for qv in (R(1, 2), 1, 2)}
ablation(10, '(가)의 합 조건', f'정해지지 않음 {vals}', A10)
vals_p = set()
for pv in (0, R(1, 4), -R(1, 4), R(1, 8)):
    g0 = (x - pv)**3 * (x - (SUM - pv)); g_ = sp.expand(g0 + V - g0.subs(x, J))
    if fmin(g_) > 0: vals_p.add(g_.subs(x, ASK))
assert len(vals_p) > 1
ablation(10, "f'(0)=0", f'정해지지 않음 {vals_p}', A10)
vals_c = {(x**3 * (x - SUM) + cv).subs(x, ASK) for cv in (1, R(3, 2), 2) if fmin(x**3 * (x - SUM) + cv) > 0}
assert len(vals_c) > 1
ablation(10, 'f(-1)=3', f'정해지지 않음 {vals_c}', A10)
ablation(10, '합 1/2(→1, 원래 수치)', sp.expand(x**3 * (x - 1) + (V - (J**3) * (J - 1))).subs(x, ASK), A10)
# 원래 수치(합 1, f(-1)=5)로 3
assert (x**3 * (x - 1) + 3).subs(x, -1) == 5 and (x**3 * (x - 1) + 3).subs(x, 1) == 3
print('10: 원래 수치로 3(10회 18번 답) 재현, 새 답과 다름')

print('ALL OK')
