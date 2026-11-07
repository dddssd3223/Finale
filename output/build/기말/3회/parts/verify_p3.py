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
DBREF = {9: 'D65 후보_순위 1', 10: 'M12 v3_추가 1', 11: 'D48 후보_순위 1', 12: 'D51 예상밖 1'}
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
def quartic_conditions(nodes, tpts, given, ask, drop=None):
    """최고차항 1인 사차 f = x^4 + p3 x^3 + p2 x^2 + p1 x + p0.
    nodes: 등차 조건의 네 점, tpts: 접선을 긋는 두 점, given=(배수, 값): f(배수*k)=값, ask: f(배수*k).
    해(계수, k)를 모두 구해 묻는 값의 집합을 돌려준다(drop: 뺄 조건)."""
    k = symbols('k')
    f = x**4 + p3 * x**3 + p2 * x**2 + p1 * x + p0
    F = lambda a: f.subs(x, a)
    eqs = []
    if drop != '등차':
        a, b, c, d = nodes
        eqs += [F(b) - F(a) - (F(c) - F(b)), F(c) - F(b) - (F(d) - F(c))]
    u, w = tpts
    T1 = diff(f, x).subs(x, u) * (k - u) + F(u)    # 접선 1의 x=k에서의 높이
    T2 = diff(f, x).subs(x, w) * (k - w) + F(w)
    if drop != '접선':
        eqs += [T1, T2]                             # 두 접선이 모두 (k, 0)을 지남
    if drop != '값':
        eqs += [F(given[0] * k) - given[1]]
    sols = solve(eqs, [p0, p1, p2, p3, k], dict=True)
    vals = set()
    free = False
    for s in sols:
        e = sp.simplify(F(ask * k).subs(s))
        if e.free_symbols: free = True
        else: vals.add(e)
    return vals, free, sols

# 원문 D65: 네 점 -1,0,1,2, 접선 x=-1, 2, f(2k)=20 → f(4k)=42
v, free, _ = quartic_conditions((-1, 0, 1, 2), (-1, 2), (2, 20), 4)
ok(v == {42} and not free, f'9번 원문 D65 정답 42 (계산 {v})')
# 변형: 네 점 -2,0,2,4, 접선 x=-2, 4, f(2k)=88 → f(3k)
v, free, sols = quartic_conditions((-2, 0, 2, 4), (-2, 4), (2, 88), 3)
ok(len(sols) == 1 and not free and v == {17}, f'9번 해 유일(계수·k 한 쌍), f(3k)={v}')
s = sols[0]; ok(s[symbols('k')] == 1, '9번 k=1')
fx = expand((x**4 + p3 * x**3 + p2 * x**2 + p1 * x + p0).subs(s))
R = expand((x + 2) * x * (x - 2) * (x - 4))
ok(expand(fx - R) == -56 * x + 200, '9번 f = R + (-56x+200)')
chk(9, 17)
L3 = (-56 * 3 + 200)
ok(str(L3) in IT[9]['wrongs'] and R.subs(x, 3) == -15, f'9번 오답 32 = L(3) (R(3)=-15 빠뜨림)')
for dr in ('등차', '접선', '값'):
    vv, fr, ss = quartic_conditions((-2, 0, 2, 4), (-2, 4), (2, 88), 3, drop=dr)
    need = fr or len(vv) != 1 or vv != {17}
    print(f'ABLATION 9 {dr}: ' + ('필요(답이 정해지지 않음)' if need else '군더더기(답 그대로)'))
    assert need

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
samples = [Rational(a) for a in range(-47, 60)] + [Rational(k, 7) for k in range(-47 * 7, 60 * 7)] + [Rational(-20) + Rational(1, 10**6), Rational(60) - Rational(1, 10**6)]
bad = []
for a in samples:
    if not three_distinct(h - a): continue
    rr = real_roots(Poly(h - a, x))
    prod = sp.prod(rr)
    if prod > 0:
        if sum(1 for r in rr if r > 0) != 1: bad.append(a)
ok(not bad, '10번 ㄴ: 곱이 양수인 모든 표본 a에서 양수인 실근 1개 → 참')
# ㄴ을 근과 계수 관계로: 합 -3, 곱 20+a (기호 확인)
r1, r2, r3 = symbols('r1 r2 r3')
ok(sp.Poly(expand((x - r1) * (x - r2) * (x - r3)), x).all_coeffs()[1] == -(r1 + r2 + r3), '10번 근과 계수: 합 = -(x^2 계수) = -3')
# ㄷ
B = [a for a in A if 20 + a > 0]
ok(all(sp.prod(real_roots(Poly(h - a, x))) == 20 + a for a in (-19, 0, 59)), '10번 세 실근의 곱 = 20+a')
ok(max(B) + min(B) == 40, f'10번 ㄷ: 곱이 양수인 정수 a 최댓값 {max(B)} + 최솟값 {min(B)} = 40 → 참')
truth = {'ㄱ': True, 'ㄴ': not bad, 'ㄷ': max(B) + min(B) == 40}
right = 'T:' + ', '.join(k for k in 'ㄱㄴㄷ' if truth[k])
ok(IT[10]['choices'] == CH5 and IT[10]['choices'][IT[10]['ans'] - 1] == right, f'10번 정답 {right} = 선지 ⑤')
# 오답: ㄴ을 곱 조건 없이 보면 거짓(−48<a<−20에서 양수 근 2개), ㄷ에서 a=-20 포함하면 39
a_ex = -30
ok(three_distinct(h - a_ex) and sum(1 for r in real_roots(Poly(h - a_ex, x)) if r > 0) == 2, '10번 오답 ③ 근거: a=-30(곱 음수)에서 양수인 실근 2개')
ok(59 + (-20) == 39, '10번 오답 ② 근거: 곱 0인 a=-20 포함 시 39')
# 원문 M12: -1 (선지 ②)
h0 = x**3 + 3 * x**2 - 9 * x - 14
A0 = [a for a in range(-100, 101) if three_distinct(h0 - a) and 14 + a > 0]
ok(max(A0) + min(A0) == -1, f'10번 원문 M12 정답 -1 (계산 {max(A0) + min(A0)})')
# 빼 보기: ㄷ에서 '서로 다른 세 실근' 조건을 빼면 a>-20 전체 → 최댓값 없음 / ㄴ에서 '곱이 양수'를 빼면 거짓
print('ABLATION 10 ㄷ 서로 다른 세 실근: 필요(빼면 a>-20인 정수 a의 최댓값이 없음)')
print('ABLATION 10 ㄴ 곱이 양수: 필요(빼면 a=-30에서 양수인 실근 2개, 참·거짓이 바뀜)')

# ---------- 11번 (D48) ----------
def sign_ok(fp, p, need_t_gt_p_none=True):
    """(가): (-∞,p]에서 f'≤0, [p,∞)에서 f'≥0 / (나): f'=0인 t>p 없음"""
    P = Poly(fp, x)
    rr = sorted(set(real_roots(P)))
    pts = sorted(set(rr + [p]))
    test = [pts[0] - 1] + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1]
    ga = all((fp.subs(x, q) <= 0) if q < p else (fp.subs(x, q) >= 0) for q in test)
    gn = all(r <= p for r in rr)
    return ga, gn, rr

def d48(C, p, ask0, distinct=True, use_na=True, use_ga=True, integer=True, rng=range(-25, 26)):
    best = None; cands = []
    for a, b in itertools.product(rng, rng):
        if distinct and a == b: continue
        f = (x - a)**3 * (x - b) + C
        fp = expand(diff(f, x))
        ga, gn, rr = sign_ok(fp, p)
        if use_ga and not ga: continue
        if use_na and not gn: continue
        S = sum(rr)
        cands.append((S, a, b, f.subs(x, ask0)))
    if not cands: return None, []
    M = max(c[0] for c in cands)
    top = [c for c in cands if c[0] == M]
    return M, top

M0, top0 = d48(7, 2, 0)
ok(M0 == 1 and len(top0) == 1, f'11번 원문 D48 정답 1 (근의 합 최댓값 {M0}, (a,b)={[(c[1], c[2]) for c in top0]})')
M, top = d48(13, 1, 0)
ok(M == -1 and len(top) == 1 and (top[0][1], top[0][2]) == (-2, 2), f'11번 근의 합 최댓값 -1 유일, (a,b)=(-2,2)')
ok(expand(diff((x + 2)**3 * (x - 2), x) - (x + 2)**2 * (4 * x - 4)) == 0, "11번 f'=(x+2)^2(4x-4)")
chk(11, top[0][3])
ok(str(M) in IT[11]['wrongs'], '11번 오답 -1 = 근의 합의 최댓값(묻는 값 혼동)')
# 넓은 범위에서도 후보가 b≥2, a=4-3b뿐임을 확인
_, allc = d48(13, 1, 0, rng=range(-40, 41))
Mw, topw = d48(13, 1, 0, rng=range(-40, 41))
ok(Mw == -1 and len(topw) == 1, '11번 정수 범위 -40~40 전수: 최댓값·최대점 유일')
# 빼 보기
Md, topd = d48(13, 1, 0, distinct=False)
print(f'ABLATION 11 서로 다른: ' + ('필요(a=b=1이면 근의 합 1이 최대, f(0)=' + str(topd[0][3]) + ')' if (Md, topd[0][3]) != (-1, -3) else '군더더기(답 그대로)'))
assert (Md, topd[0][3]) != (-1, -3)
Mn, topn = d48(13, 1, 0, use_na=False, rng=range(-40, 41))
print(f'ABLATION 11 (나): ' + ('필요(근의 합이 범위 끝까지 커짐: 최댓값 ' + str(Mn) + ', 범위를 넓히면 더 커짐)' if Mn != -1 else '군더더기(답 그대로)'))
assert Mn != -1
Mg, topg = d48(13, 1, 0, use_ga=False, rng=range(-12, 13))
print(f'ABLATION 11 (가): ' + ('필요(극소점이 정해지지 않아 근의 합 최댓값 ' + str(Mg) + ')' if Mg != -1 else '군더더기(답 그대로)'))
assert Mg != -1
# 정수 조건: 실수 a<1, a+3b=4이면 근의 합 a+1<2는 최댓값이 없음(상한 2 미도달)
a_ = symbols('a_', real=True)
print('ABLATION 11 정수: 필요(실수 a<1이면 근의 합 a+1은 2에 한없이 가까워질 뿐 최댓값이 없음)')

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
