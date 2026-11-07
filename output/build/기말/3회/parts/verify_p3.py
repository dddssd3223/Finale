# -*- coding: utf-8 -*-
# p3.py (3회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re, itertools
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, nsimplify, sqrt

x, t = symbols('x t', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 1, 10: 5, 11: 3, 12: 2}
DBREF = {9: 'D65 학교식_예상 1', 10: 'M12 v3_추가 1', 11: 'D48 후보_순위 1', 12: 'D51 예상밖 1'}
KEYS = {9: 'D65', 10: 'M12', 11: 'D48', 12: 'D51'}
CH5 = ['T:ㄱ', 'T:ㄱ, ㄴ', 'T:ㄱ, ㄷ', 'T:ㄴ, ㄷ', 'T:ㄱ, ㄴ, ㄷ']
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n], f'{n}번 정답 번호 {it["ans"]}·db_ref·key 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'level'):
        assert it[f], (n, f)

def cv(c):
    return nsimplify(str(c))

def arith(n):
    v = [cv(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    good = len(set(v)) == 5 and len(d) == 1
    ok(good, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    return v

def chk(n, val):
    v = arith(n)
    ok(v[IT[n]['ans'] - 1] == val, f'{n}번 계산 정답 {val} = 선지 {IT[n]["ans"]}번')

# ---------- 9번 (D65) ----------
p0, p1, p2, p3 = symbols('p0 p1 p2 p3')
k_ = symbols('k')
def quartic_conditions(nodes, tpts, given, ask, base=lambda k: 0, drop=None, pins=()):
    """최고차항 1인 사차 f = x^4 + p3 x^3 + p2 x^2 + p1 x + p0.
    nodes: 등차(차의 등식) 조건의 네 점, tpts: 접선을 긋는 두 점, base(k): 교점의 y좌표(원문 0, 변형 k+4),
    given=(배수, 값): f(배수*k)=값, ask: f(배수*k). 해(계수, k)를 모두 구해 묻는 값의 집합을 돌려준다(drop: 뺄 조건, pins: 빼 보기용 고정값)."""
    f = x**4 + p3 * x**3 + p2 * x**2 + p1 * x + p0
    F = lambda a: f.subs(x, a)
    eqs = []
    if drop != '등차':
        a, b, c, d = nodes
        eqs += [F(b) - F(a) - (F(c) - F(b)), F(c) - F(b) - (F(d) - F(c))]
    u, w = tpts
    T1 = diff(f, x).subs(x, u) * (k_ - u) + F(u)    # 접선 1의 x=k에서의 높이
    T2 = diff(f, x).subs(x, w) * (k_ - w) + F(w)
    if drop != '접선':
        eqs += [T1 - base(k_), T2 - base(k_)]          # 두 접선이 모두 (k, base(k))를 지남
    if drop != '값':
        eqs += [F(given[0] * k_) - given[1]]
    eqs += [sym - val for sym, val in pins]
    sols = solve(eqs, [p0, p1, p2, p3, k_], dict=True)
    vals = set(); free = False
    for so in sols:
        e = sp.simplify(F(ask * k_).subs(so))
        if e.free_symbols: free = True
        else: vals.add(e)
    return vals, free, sols

# 원문 D65: 네 점 -1,0,1,2, 접선 x=-1, 2, 교점 (k,0), f(2k)=20 → f(4k)=42
v, free, _ = quartic_conditions((-1, 0, 1, 2), (-1, 2), (2, 20), 4)
ok(v == {42} and not free, f'9번 원문 D65 정답 42 (계산 {v})')
# 변형: f(0)-f(-2)=f(2)-f(0)=f(4)-f(2), 접선 x=-2, 4, 교점 (k, k+4), f(2k)=90 → f(3k)
B9 = lambda k: k + 4
v, free, sols = quartic_conditions((-2, 0, 2, 4), (-2, 4), (2, 90), 3, base=B9)
ok(len(sols) == 1 and not free and v == {16}, f'9번 해 유일(계수·k 한 쌍), f(3k)={v}')
so = sols[0]; ok(so[k_] == 1, '9번 k=1, 교점 (1, 5)')
fx = expand((x**4 + p3 * x**3 + p2 * x**2 + p1 * x + p0).subs(so))
R = expand((x + 2) * x * (x - 2) * (x - 4))
ok(expand(fx - R) == -59 * x + 208, '9번 f = R + (-59x+208)')
chk(9, 16)
# 오답: 교점 높이를 원문처럼 0으로(x축) → 21, R(3) 누락 → L(3)=31
v0, _, _ = quartic_conditions((-2, 0, 2, 4), (-2, 4), (2, 90), 3)
ok(v0 == {21} and '21' in IT[9]['wrongs'], f'9번 오답 21 = 교점 높이를 0으로 둔 값 {v0}')
ok(-59 * 3 + 208 == 31 and '31' in IT[9]['wrongs'] and R.subs(x, 3) == -15, '9번 오답 31 = L(3) (R(3)=-15 빠뜨림)')
# 빼 보기: 조건 하나를 빼면 남은 조건을 만족시키는 사차함수가 여럿이고 f(3k)가 달라짐(예를 두 개 만들어 보임)
PINS = {'등차': [[(p3, 0), (p2, 0)], [(p3, 1), (p2, 0)]], '접선': [[(p1, 0), (k_, 1)], [(p1, 0), (k_, 2)]], '값': [[(p0, 0)], [(p0, 8)]]}
for dr in ('등차', '접선', '값'):
    vals = set()
    for pin in PINS[dr]: vals |= quartic_conditions((-2, 0, 2, 4), (-2, 4), (2, 90), 3, base=B9, drop=dr, pins=pin)[0]
    need = len(vals) >= 2
    print(f'ABLATION 9 {dr}: ' + (f'필요(남은 조건만으로 f(3k)={sorted(vals)[:3]} 등 여럿)' if need else '군더더기(답 그대로)'))
    assert need
print('ABLATION 9 교점 y좌표 k+4: 필요(x축 위 (k, 0)이면 답 21)')

# ---------- 10번 (M12) ----------
def three_distinct(poly):
    P = Poly(poly, x)
    return sp.discriminant(P) > 0          # 삼차: 판별식 > 0 ⇔ 서로 다른 세 실근

h = x**3 + 3 * x**2 - 24 * x - 20
ok(expand((x**3 + 4 * x**2 - 24 * x - 20) - x**2) == h, '10번 방정식 ⇔ h(x)=a')
ok(h.subs(x, -4) == 60 and h.subs(x, 2) == -48 and h.subs(x, 0) == -20, '10번 극댓값 60, 극솟값 -48, h(0)=-20')
A = [a for a in range(-300, 301) if three_distinct(h - a)]
ok(len(A) == 107 and min(A) == -47 and max(A) == 59, f'10번 ㄱ: 세 실근 정수 a {len(A)}개 (-47~59) → 참')
# ㄴ: 곱이 양수(20+a>0) + 세 실근이면 양수인 실근 1개 (정수·유리수 표본 전수 + 경계 근처)
samples = [Rational(k, 7) for k in range(-48 * 7, 60 * 7 + 1)] + [Rational(-20) + Rational(1, 10**6), Rational(60) - Rational(1, 10**6)]
bad = []
for a in samples:
    if not three_distinct(h - a): continue
    if 20 + a > 0:                                  # 세 실근의 곱 = 20+a (근과 계수)
        if Poly(h - a, x).count_roots(0, None) - (1 if (h - a).subs(x, 0) == 0 else 0) != 1: bad.append(a)
ok(not bad, '10번 ㄴ: 곱이 양수인 모든 표본 a에서 양수인 실근 1개 → 참')
# ㄴ을 근과 계수 관계로: 합 -3, 곱 20+a (기호 확인)
r1, r2, r3 = symbols('r1 r2 r3')
ok(sp.Poly(expand((x - r1) * (x - r2) * (x - r3)), x).all_coeffs()[1] == -(r1 + r2 + r3), '10번 근과 계수: 합 = -(x^2 계수) = -3')
# ㄷ
B = [a for a in A if 20 + a > 0]
ok(all(abs(sp.N(sp.prod(real_roots(Poly(h - a, x))), 30) - (20 + a)) < 1e-20 for a in (-47, -19, 0, 59)) and Poly(h - symbols('a'), x).all_coeffs()[-1] == -20 - symbols('a'), '10번 세 실근의 곱 = 20+a (상수항 -(20+a))')
ok(max(B) + min(B) == 40, f'10번 ㄷ: 곱이 양수인 정수 a 최댓값 {max(B)} + 최솟값 {min(B)} = 40 → 참')
truth = {'ㄱ': True, 'ㄴ': not bad, 'ㄷ': max(B) + min(B) == 40}
right = 'T:' + ', '.join(k for k in 'ㄱㄴㄷ' if truth[k])
ok(IT[10]['choices'] == CH5 and IT[10]['choices'][IT[10]['ans'] - 1] == right, f'10번 정답 {right} = 선지 ⑤')
# 오답: ㄴ을 곱 조건 없이 보면 거짓(−48<a<−20에서 양수 근 2개), ㄷ에서 a=-20 포함하면 39
a_ex = -30
ok(three_distinct(h - a_ex) and Poly(h - a_ex, x).count_roots(0, None) == 2, '10번 오답 ③ 근거: a=-30(곱 음수)에서 양수인 실근 2개')
ok(59 + (-20) == 39, '10번 오답 ② 근거: 곱 0인 a=-20 포함 시 39')
# 원문 M12: -1 (선지 ②)
h0 = x**3 + 3 * x**2 - 9 * x - 14
A0 = [a for a in range(-100, 101) if three_distinct(h0 - a) and 14 + a > 0]
ok(max(A0) + min(A0) == -1, f'10번 원문 M12 정답 -1 (계산 {max(A0) + min(A0)})')
# 빼 보기: ㄷ에서 '서로 다른 세 실근' 조건을 빼면 a>-20 전체 → 최댓값 없음 / ㄴ에서 '곱이 양수'를 빼면 거짓
print('ABLATION 10 ㄷ 서로 다른 세 실근: 필요(빼면 a>-20인 정수 a의 최댓값이 없음)')
print('ABLATION 10 ㄴ 곱이 양수: 필요(빼면 a=-30에서 양수인 실근 2개, 참·거짓이 바뀜)')

# ---------- 11번 (D48) ----------
from fractions import Fraction as Fr
import numpy as np
def peval(c, q):
    v = Fr(0)
    for co in c: v = v * q + co
    return v
def exact_real_roots(c):
    """정수 계수 c(높은 차수부터)의 서로 다른 실근(정확값). 인수분해로 일차 인수의 근을 모으고, 나머지 인수에 실근이 없음을 확인"""
    P = Poly([sp.Integer(int(v)) for v in c], x)
    rr = []
    for g, m in P.factor_list()[1]:
        if g.degree() == 1:
            r = -g.all_coeffs()[1] / g.all_coeffs()[0]
            rr.append(Fr(int(sp.fraction(r)[0]), int(sp.fraction(r)[1])))
        else:
            assert g.count_roots() == 0, ('일차가 아닌 인수에 실근', c)
    return sorted(set(rr))
_a, _b = symbols('_a _b')
FP = Poly(expand(diff((x - _a)**3 * (x - _b), x)), x)
FPC = [sp.lambdify((_a, _b), co) for co in FP.all_coeffs()]
def sign_ok(c, p, side='>'):
    """(가): (-∞,p]에서 f'≤0, [p,∞)에서 f'≥0 / (나): f'=0인 t>p(side='>') 또는 t<p(side='<') 없음"""
    rr = exact_real_roots(c)
    pts = sorted(set(rr + [Fr(p)]))
    test = [pts[0] - 1] + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1]
    ga = all((peval(c, q) <= 0) if q < p else (peval(c, q) >= 0) for q in test)
    gn = all((r <= p) if side == '>' else (r >= p) for r in rr)
    return ga, gn, rr

def d48(C, p, ask0, distinct=True, use_na=True, use_ga=True, integer=True, rng=range(-25, 26), side='>', best=max):
    cands = []
    for a, b in itertools.product(rng, rng):
        if distinct and a == b: continue
        c = [int(g(a, b)) for g in FPC]
        ga, gn, rr = sign_ok(c, p, side)
        if use_ga and not ga: continue
        if use_na and not gn: continue
        S = sum(rr)
        cands.append((S, a, b, (ask0 - a)**3 * (ask0 - b) + C))
    if not cands: return None, []
    M = best(c[0] for c in cands)
    top = [c for c in cands if c[0] == M]
    return M, top

M0, top0 = d48(7, 2, 0)
ok(M0 == 1 and len(top0) == 1, f'11번 원문 D48 정답 1 (근의 합 최댓값 {M0}, (a,b)={[(c[1], c[2]) for c in top0]})')
K11 = dict(side='<', best=min)
M, top = d48(4, -2, 0, **K11)
ok(M == -1 and len(top) == 1 and (top[0][1], top[0][2]) == (1, -3), f'11번 근의 합 최솟값 -1 유일, (a,b)=(1,-3)')
ok(expand(diff((x - 1)**3 * (x + 3), x) - (x - 1)**2 * (4 * x + 8)) == 0, "11번 f'=(x-1)^2(4x+8)")
chk(11, top[0][3])
ok(str(M) in IT[11]['wrongs'], '11번 오답 -1 = 근의 합의 최솟값(묻는 값 혼동)')
Mw, topw = d48(4, -2, 0, rng=range(-40, 41), **K11)
ok(Mw == -1 and len(topw) == 1, '11번 정수 범위 -40~40 전수: 최솟값·최소점 유일')
# 원문 방향 (나)(t>-2)로 두면 근의 합의 최솟값이 없음(범위 끝까지 작아짐) → 거울상이 일함
Mo, _ = d48(4, -2, 0, rng=range(-40, 41), side='>', best=min)
print('ABLATION 11 (나)의 방향 t<-2: ' + ('필요(원문 방향 t>-2면 근의 합이 범위 끝까지 작아짐: ' + str(Mo) + ')' if Mo != -1 else '군더더기(답 그대로)'))
assert Mo != -1
# 빼 보기
Md, topd = d48(4, -2, 0, distinct=False, **K11)
print(f'ABLATION 11 서로 다른: ' + ('필요(a=b=-2이면 근의 합 -2가 최소, f(0)=' + str(topd[0][3]) + ')' if (Md, topd[0][3]) != (-1, 1) else '군더더기(답 그대로)'))
assert (Md, topd[0][3]) != (-1, 1)
Mn, topn = d48(4, -2, 0, use_na=False, rng=range(-40, 41), **K11)
print(f'ABLATION 11 (나): ' + ('필요(근의 합이 범위 끝까지 작아짐: 최솟값 ' + str(Mn) + ', 범위를 넓히면 더 작아짐)' if Mn != -1 else '군더더기(답 그대로)'))
assert Mn != -1
Mg, topg = d48(4, -2, 0, use_ga=False, rng=range(-12, 13), **K11)
print(f'ABLATION 11 (가): ' + ('필요(극소점이 정해지지 않아 근의 합 최솟값 ' + str(Mg) + ')' if Mg != -1 else '군더더기(답 그대로)'))
assert Mg != -1
print('ABLATION 11 정수: 필요(실수 a>-2이면 근의 합 a-2는 -4에 한없이 가까워질 뿐 최솟값이 없음)')

# ---------- 12번 (D51) ----------
def d51(f, line_c, lo, hi, lo_closed=True, hi_closed=True):
    """곡선 y=f(x) (lo≤x≤hi)와 직선 x-y-line_c=0 사이 거리 최소점. lo/hi=None이면 그쪽 끝 없음.
    반환: (최소 거리, 최소점 x 목록) — 곡선이 직선과 만나면 거리 0"""
    g = expand(f - x + line_c)          # 거리 = |g|/sqrt2
    rr = [r for r in real_roots(Poly(g, x)) if (lo is None or r >= lo) and (hi is None or r <= hi)]
    if rr: return 0, rr
    crit = [r for r in real_roots(Poly(diff(g, x), x)) if (lo is None or r > lo) and (hi is None or r < hi)]
    cand = crit + [e for e, c in ((lo, lo_closed), (hi, hi_closed)) if e is not None and c]
    vals = {c: abs(g.subs(x, c)) for c in cand}
    m = min(vals.values())
    # 열린 끝에서 더 작아지면 최솟값 없음
    for e, c in ((lo, lo_closed), (hi, hi_closed)):
        if e is not None and not c and abs(g.subs(x, e)) < m: return None, []
    return m, [c for c in cand if vals[c] == m]

f0 = x**3 / 3 + Rational(11, 3)
m0, P0 = d51(f0, 10, 0, None, lo_closed=False)
ok(P0 == [1] and P0[0] + f0.subs(x, 1) == 5, f'12번 원문 D51 정답 5 (P({P0[0]}, {f0.subs(x, P0[0])}))')
f12 = x**3 - 2 * x**2 - 3 * x + 5
m, P = d51(f12, 10, -1, 1)
ok(len(P) == 1 and P[0] == 1 and m == 10, f'12번 최소점 유일 x={P}, 세로 차 {m}')
val12 = P[0] + f12.subs(x, P[0])
chk(12, val12)
ok(sp.solve(sp.Eq(diff(f12, x), 1), x) == [Rational(-2, 3), 2], "12번 기울기 1인 접점 x=-2/3, 2 (둘 다 거리의 최소 아님)")
ok(2 + f12.subs(x, 2) == 1 and -1 + f12.subs(x, -1) == 4, '12번 오답 1(x=2 접점), 4(x=-1 끝점)')
# 빼 보기
mA, PA = d51(f12, 10, 0, None, lo_closed=False)            # 원문 정의역 x>0
print('ABLATION 12 위 끝(x≤1): ' + (f'필요(빼면 x={PA}, a+b={PA[0] + f12.subs(x, PA[0])})' if PA != [1] else '군더더기(답 그대로)'))
assert PA != [1]
mB, PB = d51(f12, 10, None, 1)                               # x≤1
print('ABLATION 12 아래 끝(-1≤x): ' + (f'필요(빼면 곡선이 직선과 만나 거리 최솟값 {mB}, 교점 x={[sp.N(r, 4) for r in PB]})' if mB == 0 else '군더더기(답 그대로)'))
assert mB == 0
mC, PC = d51(f12, 10, -1, 1, hi_closed=False)
print('ABLATION 12 닫힌 끝(≤1): ' + ('필요(열면 최솟값이 없음)' if mC is None else '군더더기(답 그대로)'))
assert mC is None

print(f'검사 {len(OK)}개')
print('ALL OK')
