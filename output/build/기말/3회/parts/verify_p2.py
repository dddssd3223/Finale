# -*- coding: utf-8 -*-
# p2.py (3회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, sqrt, oo, limit, factor
x, t, a, C = symbols('x t a C', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 5, 6: 3, 7: 2, 8: 4}
REF = {5: 'M9 후보_순위 1', 6: 'I14 후보_순위 1', 7: 'D34 예상밖 1', 8: 'I32 후보_순위 1'}
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['M9', 'I14', 'D34', 'I32']
OPS = {f'OP{i:02d}' for i in range(1, 56)}
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐')
    assert it['ops'] and all(o in OPS for o in it['ops']) and it['precedent']
    assert '함정 추가' not in it['vtype'] and it['level'] in ('하', '중', '중상', '상', '최상')
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body'):
        assert it[f]
    assert 'class="fig"' not in it['body']                           # 1–8번 그림 없음
    for w in it['wrongs']:                                            # wrong 설명에 선지 번호와 값이 함께 있음
        assert f'{"①②③④⑤"[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)

def cv(c):
    c = str(c)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(c)

def arith(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {ch[1] - ch[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def min_on_ray(f, lo):
    """[lo, ∞)에서 다항식 f(최고차항 양수)의 최솟값: 끝점과 구간 안 정류점 비교"""
    assert Poly(f, x).LC() > 0
    cand = [lo] + [r for r in real_roots(Poly(diff(f, x), x)) if r > lo]
    return min(f.subs(x, c) for c in cand)

def poly_solve(eqs, unknowns):
    sol = solve(eqs, unknowns, dict=True)
    return sol

# ===== 원문 풀이 =====
# M9: f=x^3-x+6, g=x^2+a, x≥0에서 f≥g인 a의 최댓값 5 (⑤)
hm9 = x**3 - x + 6 - x**2
assert min_on_ray(hm9, 0) == 5
# I14: xf=∫_2^x f+3x^4-4x^2 → f(3)=84
def solve_I14(P, lo, deg=6):
    cs = symbols(f'c0:{deg + 1}')
    f = sum(cs[i] * x**i for i in range(deg + 1))
    e = expand(x * f - integrate(f.subs(x, t), (t, lo, x)) - P)
    sol = solve(Poly(e, x).all_coeffs(), cs, dict=True)
    assert len(sol) == 1 and all(c in sol[0] for c in cs)            # 차수 6 이하 다항함수 중 유일
    return expand(f.subs(sol[0]))
f14 = solve_I14(3*x**4 - 4*x**2, 2)
assert expand(f14 - (4*x**3 - 8*x)) == 0 and f14.subs(x, 3) == 84
# D34: f=x^3-11x+8, P(2,-6), Q(-4,-12), -4<a<2에서 R(a,b)와 l의 거리 최대 → a+b=20
f34 = x**3 - 11*x + 8
l34 = diff(f34, x).subs(x, 2) * (x - 2) + f34.subs(x, 2)
assert expand(f34 - l34 - (x - 2)**2 * (x + 4)) == 0 and l34.subs(x, -4) == f34.subs(x, -4) == -12
h34 = f34 - l34                                                      # 거리 = |h|/√2, -4<a<2에서 h>0
cr = [r for r in solve(diff(h34, x), x) if -4 < r < 2]
assert cr == [-2] and f34.subs(x, -2) == 22 and -2 + 22 == 20
# I32: (가) ∫f'=g'+∫6x, (나) ∫f=xg-∫g, f(1)=g(1) → g(2)=27/2
def solve_I32(k2, deg=4, use=('가', '나', 'fg')):
    """(가) f-g'-k2·x^2 = 상수, (나) 미분하면 f = xg' (부정적분 등식 ⇔ 양변 도함수가 같음), f(1)=g(1). 차수 deg 이하 전수"""
    fc = symbols(f'f0:{deg + 1}'); gc = symbols(f'g0:{deg + 1}'); K = symbols('K')
    f = sum(fc[i] * x**i for i in range(deg + 1)); g = sum(gc[i] * x**i for i in range(deg + 1))
    eqs = []
    if '가' in use: eqs += Poly(expand(f - diff(g, x) - k2 * x**2 - K), x).all_coeffs()
    if '나' in use: eqs += Poly(expand(f - x * diff(g, x)), x).all_coeffs()
    if 'fg' in use: eqs += [f.subs(x, 1) - g.subs(x, 1)]
    sol = solve(eqs, list(fc) + list(gc) + [K], dict=True)
    assert len(sol) == 1
    return expand(f.subs(sol[0])), expand(g.subs(sol[0]))
f32o, g32o = solve_I32(3)
assert g32o.subs(x, 2) == Rational(27, 2)
print('원문 풀이 OK (M9=5, I14=84, D34=20, I32=27/2)')

# ===== 5번 (M9) =====
f5, g5 = x**3 + x + 7, x**2 + 2*x
h5 = f5 - g5                                                         # f-g = h5 - a
assert expand(diff(h5, x) - (3*x + 1)*(x - 1)) == 0                  # 숨은 설계 h'=(3x+1)(x-1) 보존
assert expand(diff(hm9, x) - diff(h5, x)) == 0
m5 = min_on_ray(h5, 0)
assert m5 == 6 and h5.subs(x, 1) == 6 and h5.subs(x, 0) == 7
# 전수: a를 1/4 격자로 -20..20 조사, x≥0에서 h5-a≥0 ⇔ a≤6
ok5 = [Rational(j, 4) for j in range(-80, 81) if min_on_ray(h5 - Rational(j, 4), 0) >= 0]
v5 = max(ok5)
assert v5 == 6 and all(q <= 6 for q in ok5)
w5_orig = min_on_ray(hm9, 0)                                         # 원문 답(상수항 6으로 계산)
assert w5_orig == 5
chk(5, v5, [w5_orig])

# ===== 6번 (I14) =====
P6 = 3*x**4 + 2*x**3 - 5*x**2
f6 = solve_I14(P6, 2)                                                # 차수 6 이하 다항함수 전수: 유일
assert expand(f6 - (4*x**3 + 3*x**2 - 10*x - 2)) == 0
assert expand(x*f6 - integrate(f6.subs(x, t), (t, 2, x)) - P6) == 0  # 항등식 확인
assert 2*f6.subs(x, 2) == P6.subs(x, 2) == 44
v6 = f6.subs(x, -1)
assert v6 == 7
w6_noC = (f6 + 2).subs(x, -1)                                       # 적분상수를 정하지 않음(C=0으로 둠)
assert w6_noC == 9
chk(6, v6, [w6_noC])

# ===== 7번 (D34 예상밖 1) =====
f7 = x**3 - 2*x + 4
m7 = diff(f7, x).subs(x, 1)
l7 = m7*(x - 1) + f7.subs(x, 1)
assert f7.subs(x, 1) == 3 and m7 == 1 and expand(l7 - (x + 2)) == 0
assert f7.subs(x, -2) == 0 and l7.subs(x, -2) == 0                   # Q(-2,0)은 곡선과 l의 다른 교점
h7 = expand(f7 - l7)
assert expand(h7 - (x - 1)**2*(x + 2)) == 0
assert solve(h7, x) == [-2, 1]                                       # 곡선과 l의 공통점은 P, Q뿐
# 점 (s, f(s))와 직선 x-y+2=0 사이의 거리 = |h(s)|/√2 (점-직선 거리 공식으로 확인)
s = symbols('s', real=True)
assert sp.simplify(sp.Line(sp.Point(0, 2), sp.Point(1, 3)).distance(sp.Point(s, f7.subs(x, s))) - sp.Abs(h7.subs(x, s))/sqrt(2)) == 0

def N7(c):
    """|h(x)| = c (c ≥ 0)의 서로 다른 실근 개수 = 곡선 위에서 l과의 거리가 c/√2인 점의 개수"""
    rr = set(real_roots(Poly(h7 - c, x))) | set(real_roots(Poly(h7 + c, x)))
    return len(rr)
# |h|의 극값(갈림 높이): h의 극값 h(-1)=4, h(1)=0 → 개수는 (0,4), {4}, (4,∞)에서 각각 일정
crit = sorted({h7.subs(x, r) for r in solve(diff(h7, x), x)})
assert crit == [0, 4]
assert N7(0) == 2 and N7(4) == 3
grid = [Rational(j, 8) for j in range(1, 200)]                       # 0 < c < 24.875 전수(1/8 간격) + 무리수 몇 개
grid += [Rational(4) - Rational(1, 10**6), Rational(4) + Rational(1, 10**6), Rational(1, 10**6), Rational(10**6)]
# 개수가 바뀔 수 있는 높이는 h-c, h+c의 판별식이 0인 c뿐: c(c-4)·c(c+4) → c>0에서는 c=4 하나(격자 사이에서 개수 일정)
cc = symbols('cc')
assert sorted(solve(sp.discriminant(h7 - cc, x), cc)) == [0, 4] and sorted(solve(sp.discriminant(h7 + cc, x), cc)) == [-4, 0]
three = sorted({c for c in grid if N7(c) == 3})
assert three == [4]
assert all(N7(c) == 4 for c in grid if 0 < c < 4) and all(N7(c) == 2 for c in grid if c > 4)
d7 = Rational(4)/sqrt(2)
v7 = sp.simplify(d7**2)
assert v7 == 8
w7_half = (Rational(4)/2)**2                                         # √2 대신 2로 나눔 → d=2
w7_vert = Rational(4)**2                                             # 세로 차 4를 거리로 → d=4
assert (w7_half, w7_vert) == (4, 16)
# 원문식(구간 -2<a<1에서 거리 최대)으로 풀어도 같은 점 x=-1이 나와 d^2=8: 원문 방식은 답을 바꾸지 않음(함정 아님)
assert [r for r in solve(diff(h7, x), x) if -2 < r < 1] == [-1]
chk(7, v7, [w7_half, w7_vert])

# ===== 8번 (I32) =====
f8, g8 = solve_I32(6)                                                # (가) ∫12x dx = 6x^2 + 상수
assert expand(g8 - 3*(x + 1)**2) == 0 and expand(f8 - (6*x**2 + 6*x)) == 0
assert f8.subs(x, 1) == g8.subs(x, 1) == 12
# 부정적분 등식 확인: (가) ∫f' - g' - ∫12x 가 상수, (나) ∫f - xg + ∫g 가 상수
assert diff(expand(f8 - diff(g8, x) - 6*x**2), x) == 0
assert diff(expand(integrate(f8, x) - x*g8 + integrate(g8, x)), x) == 0
v8 = g8.subs(x, 2)
assert v8 == 27
assert solve_I32(6, deg=6)[1].subs(x, 2) == 27                       # 차수 6까지 넓혀도 유일
w8_noD = (g8 - 3).subs(x, 2)                                         # g의 상수항 누락
assert w8_noD == 24
chk(8, v8, [w8_noD])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 5번
assert limit(h5, x, -oo) == -oo
print('ABLATION 5 x≥0: 필요(빼면 실수 전체에서 f-g가 아래로 끝없이 작아져 a의 최댓값이 없음)')
assert min_on_ray(h5 - 6, 0) == 0                                    # a=6이면 x=1에서 등호
print('ABLATION 5 부등식의 등호(≥): 필요(>이면 a<6이라 최댓값이 존재하지 않음)')
# 6번
fC = 4*x**3 + 3*x**2 - 10*x + C                                      # 정적분 대신 부정적분이면 미분한 식만 남음
vals6 = {fC.subs({C: c, x: -1}) for c in (0, -2, 5)}
print(f'ABLATION 6 아래끝 2(정적분 → 부정적분): 필요(적분상수가 정해지지 않음, f(-1)={sorted(vals6)} 등)'); assert len(vals6) > 1
f6b = solve_I14(P6, 1)
print(f'ABLATION 6 아래끝 값 2: 필요(1이면 답 바뀜 {v6} → {f6b.subs(x, -1)})'); assert f6b.subs(x, -1) != v6
# 7번
cnt = {}
for c in grid:
    cnt.setdefault(N7(c), set()).add(c)
print(f'ABLATION 7 점의 개수 3: 필요(개수 4이면 0<√2d<4 전체, 2이면 √2d>4 전체라 d가 정해지지 않음)'); assert len(cnt[4]) > 1 and len(cnt[2]) > 1
# 구간 단서(원문 -4<a<2에 해당하는 -2<a<1)를 두면 '개수 3'은 일어나지 않음(구간 안에서는 h>0, 최대 1개 접점)
inner = lambda c: len([r for r in set(real_roots(Poly(h7 - c, x))) | set(real_roots(Poly(h7 + c, x))) if -2 < r < 1])
assert max(inner(c) for c in grid) == 2
print('ABLATION 7 구간 단서 삭제: 필요(원문 구간 -2<a<1을 두면 거리가 d인 점은 많아야 2개라 조건을 만족시키는 d가 없음)')
f7b = x**3 - 2*x + 4
l7b = diff(f7b, x).subs(x, 0)*x + f7b.subs(x, 0)                     # 접점을 P(1,3) 대신 다른 점(0,4)으로
h7b = expand(f7b - l7b)
crit_b = sorted({abs(h7b.subs(x, r)) for r in solve(diff(h7b, x), x)} - {0})
print(f'ABLATION 7 접점 P(1,3): 필요(접점이 (0,4)이면 차가 x^3이라 개수 3인 d가 없음, 갈림 높이 {crit_b})'); assert crit_b == []
# 8번
def g2_set(use, k2=6):
    fc = symbols('f0:5'); gc = symbols('g0:5'); K = symbols('K')
    f = sum(fc[i]*x**i for i in range(5)); g = sum(gc[i]*x**i for i in range(5))
    eqs = []
    if '가' in use: eqs += Poly(expand(f - diff(g, x) - k2*x**2 - K), x).all_coeffs()
    if '나' in use: eqs += Poly(expand(f - x*diff(g, x)), x).all_coeffs()
    if 'fg' in use: eqs += [f.subs(x, 1) - g.subs(x, 1)]
    sol = solve(eqs, list(fc) + list(gc) + [K], dict=True)
    return [expand(g.subs(sl).subs(x, 2)) for sl in sol]
for drop, name in (('fg', 'f(1)=g(1)'), ('가', '(가)'), ('나', '(나)')):
    r = g2_set([u for u in ('가', '나', 'fg') if u != drop])
    free = any(e.free_symbols for e in r)
    print(f'ABLATION 8 {name}: 필요(빼면 g(2)가 정해지지 않음: {r})'); assert free

print('ALL OK')
