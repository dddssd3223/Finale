# -*- coding: utf-8 -*-
# p3.py (6회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, nsimplify, factor, integrate, Abs, sqrt

x, u = symbols('x u', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 1, 10: 3, 11: 4, 12: 2}
DBREF = {9: 'D60 결합 1', 10: 'D29 예상밖 1', 11: 'D41 예상밖 1', 12: 'D59 예상밖 2'}
KEYS = {9: 'D60', 10: 'D29', 11: 'D41', 12: 'D59'}
LEVEL = {9: '중', 10: '중', 11: '중', 12: '중'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == LEVEL[n], f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')

def arith(n):
    v = [nsimplify(str(c)) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    return v

def chk(n, val):
    v = arith(n)
    ok(v[IT[n]['ans'] - 1] == val, f'{n}번 계산 정답 {val} = 선지 {IT[n]["ans"]}번')

def tri_area(L1, L2):
    """두 직선 y=L1, y=L2(x의 일차식)와 y축으로 둘러싸인 삼각형 넓이"""
    xi = solve(sp.Eq(L1, L2), x)
    if not xi: return None
    return Abs(Rational(1, 2) * (L1.subs(x, 0) - L2.subs(x, 0)) * xi[0])

def tangent(F, p):
    return expand(diff(F, x).subs(x, p) * (x - p) + F.subs(x, p))

# ---------- 9번 (D60) ----------
# 원문: f=x^2-4x-3, g=(x^3-2x)f, (1,-6)·(1,6) 접선과 y축 → 49
fo = x**2 - 4 * x - 3; go = (x**3 - 2 * x) * fo
ok(fo.subs(x, 1) == -6 and go.subs(x, 1) == 6 and tri_area(tangent(fo, 1), tangent(go, 1)) == 49, '9번 원문 D60 정답 49 (선지 ⑤)')
# LIVE1-01-122: g=x^3 f, m: y=3x-5 → 넓이 3
fl1, fl2 = symbols('fl1 fl2')
sl = solve([fl1 + 2, 3 * fl1 + fl2 - 3], [fl1, fl2])   # g(1)=f(1)=-2, g'(1)=3f(1)+f'(1)=3
ok(tri_area(sl[fl2] * (x - 1) + sl[fl1], 3 * x - 5) == 3, 'LIVE1-01-122 정답 3 확인')
# 결합 1 스케치: g=(x^3-2x)f, 일치 → f=(x-1)^2, f(3)=4
b, c, a = symbols('b c a')
f9 = x**2 + b * x + c
def coincide(fx, gx):
    return [fx.subs(x, 1) - gx.subs(x, 1), diff(fx, x).subs(x, 1) - diff(gx, x).subs(x, 1)]
s0 = solve(coincide(f9, (x**3 - 2 * x) * f9), [b, c], dict=True)
ok(len(s0) == 1 and f9.subs(s0[0]).subs(x, 3) == 4, 'DB 결합 1 스케치 f(3)=4 확인')
# 변형: a≠0, g=(x^3-ax)f, 일치 + g'(2)=8 → 전수(연립의 모든 해)
g9 = (x**3 - a * x) * f9
eqs = coincide(f9, g9) + [diff(g9, x).subs(x, 2) - 8]
sols = solve(eqs, [a, b, c], dict=True)
good = [s for s in sols if s[a] != 0]
ok(len(good) == 1 and good[0] == {a: 4, b: -2, c: 1}, f'9번 a≠0인 해 하나: {good}')
F9 = f9.subs(good[0]); G9 = g9.subs(good[0])
mline = tangent(F9, 1); nline = tangent(G9, 2)
ok(mline == 0 and tangent(G9, 1) == 0, '9번 두 접선이 모두 y=0 (x축)')
ok(nline == 8 * x - 16 and G9.subs(x, 2) == 0, '9번 직선 n: y=8x-16')
A9 = tri_area(mline, nline)
ok(A9 == 16, f'9번 넓이 {A9}')
chk(9, A9)
# a 값 일반으로도: 일치 조건의 해 집합
gen = solve(coincide(f9, g9), [b, c], dict=True)
ok(all(sp.simplify(f9.subs(s) - (x - 1)**2) == 0 for s in gen if s), f'9번 a≠0이면 일치 조건만으로 f=(x-1)^2 (해 {gen})')
ok(2 * A9 == 32 and '32' in IT[9]['wrongs'], '9번 오답 32 = ½ 누락')
# 빼 보기
bad0 = [s for s in sols if s[a] == 0]
s_a0 = solve([e.subs(a, 0) for e in eqs], [b, c], dict=True)
area_a0 = [tri_area(tangent(f9.subs(s), 1), tangent(((x**3) * f9).subs(s), 2)) for s in s_a0]
ok(area_a0 == [Rational(289, 18)], f'a=0이면 f={[f9.subs(s) for s in s_a0]}, 넓이 {area_a0}')
print(f'ABLATION 9 0이 아닌: 필요(a=0이면 넓이 {area_a0[0]}도 나와 답이 둘)')
s_noslope = solve(coincide(f9, g9), [b, c], dict=True)
print('ABLATION 9 기울기 8: 필요(없으면 a가 정해지지 않아 넓이가 a마다 다름)')
assert len({tri_area(0 * x, tangent(((x**3 - av * x) * (x - 1)**2), 2)) for av in (1, 2, 3)}) > 1
d0, d1, d2 = symbols('d0 d1 d2')
f9c = x**3 + d2 * x**2 + d1 * x + d0
s_cub = solve(coincide(f9c, (x**3 - a * x) * f9c) + [diff((x**3 - a * x) * f9c, x).subs(x, 2) - 8], [a, d0, d1, d2], dict=True)
s_cub = [s for s in s_cub if s.get(a, 1) != 0]
ok(s_cub and any(len(s) < 4 for s in s_cub), f'삼차함수로 바꾸면 a≠0 해가 매개변수족: {s_cub}')
print('ABLATION 9 이차함수: 필요(삼차이면 f가 하나로 정해지지 않음)')

# ---------- 10번 (D29) ----------
def kinks(F, av):
    """y=|F(x)-F(a)|의 미분가능하지 않은 점(부호가 바뀌는 실근)"""
    P = Poly(expand(F - F.subs(x, av)), x)
    out = []
    for r in set(real_roots(P)):
        mult = 0; Q = P
        while Q.eval(r) == 0:
            mult += 1; Q = Poly(sp.quo(Q.as_expr(), x - r), x)
        if mult % 2 == 1: out.append(r)
    return sorted(out)
def good_a(F, av):
    return kinks(F, av) == [av]
fD = x**3 - 3 * x**2 + 8
# 원문: |f-f(a)|, a>0 최솟값 m=3, m+f(m)=11
grid = [Rational(j, 4) for j in range(1, 41)]
m0 = min(av for av in grid if good_a(fD, av))
ok(m0 == 3 and m0 + fD.subs(x, m0) == 11, '10번 원문 D29 정답 11')
# 조작_보강 1: |f-9x-f(a)+9a|
F10 = fD - 9 * x
ok(expand(diff(F10, x) - 3 * (x - 3) * (x + 1)) == 0 and F10.subs(x, -1) == 13 and F10.subs(x, 3) == -19, '10번 F 극댓값 13(x=-1), 극솟값 -19(x=3)')
ok(expand(F10 - 13 - (x + 1)**2 * (x - 5)) == 0 and expand(F10 + 19 - (x - 3)**2 * (x + 3)) == 0, '10번 F-13=(x+1)²(x-5), F+19=(x-3)²(x+3)')
G = [Rational(j, 8) for j in range(1, 81)]   # 0<a≤10, 간격 1/8 전수
okset = [av for av in G if good_a(F10, av)]
ok(okset == [av for av in G if av >= 5], f'10번 양수 a 격자 전수: 조건 ⇔ a≥5 (최소 {okset[0]})')
ok(kinks(F10, 3) == [-3] and kinks(F10, Rational(49, 10)) != [Rational(49, 10)], '10번 a=3은 x=-3에서만 꺾임(x=a 아님), a=4.9는 탈락')
m10 = okset[0]
line = 9 * x + fD.subs(x, m10) - 9 * m10
ok(line == 9 * x + 13, '10번 직선 y=9x+13')
xs = sorted(set(real_roots(Poly(fD - line, x))))
S = integrate(Abs(fD - line), (x, xs[0], xs[-1]))
S2 = integrate(line - fD, (x, -1, 5))
ok(xs == [-1, 5] and S2 == 108 and sp.simplify(S - 108) == 0, f'10번 넓이 S={S2}')
chk(10, m10 + S2)
# 오답: m=3(극점 포함)
line3 = 9 * x + fD.subs(x, 3) - 27
S3 = integrate(fD - line3, (x, -3, 3))
ok(S3 == 108 and 3 + S3 == 111 and '111' in IT[10]['wrongs'], '10번 오답 111 = 극점 a=3을 넣은 m=3 (+넓이 108)')
# 원문 방식(수평선) m=3, 넓이 27/4 → 선지 밖
ok(integrate(8 - fD, (x, 0, 3)) == Rational(27, 4), '10번 원문 방식(수평선) 넓이 27/4 → 선지 밖')
# 빼 보기
neg = [av for av in [Rational(-j, 2) for j in range(1, 41)] if good_a(F10, av)]
ok(neg and min(neg) == -20, '음수 a도 허용하면 a≤-3 전체가 조건을 만족 → 최솟값 없음')
print('ABLATION 10 양의: 필요(없으면 a≤-3이 모두 만족해 최솟값이 없음)')
print(f'ABLATION 10 기울기 9 직선: 필요(수평선이면 m+넓이 = 3+27/4)')

# ---------- 11번 (D41) ----------
p, q = symbols('p q')
def solve11(P, Q, slope=1):
    """f=px^3+qx^2, 점 (P,f(P))에서 기울기 slope인 접선이 점 (Q,f(Q))를 지남"""
    f = p * x**3 + q * x**2
    eqs = [diff(f, x).subs(x, P) - slope, f.subs(x, Q) - (f.subs(x, P) + slope * (Q - P))]
    s = solve(eqs, [p, q], dict=True)
    return [f.subs(z) for z in s if z[p] != 0]
s0 = solve11(-2, 2)
ok(len(s0) == 1 and s0[0].subs(x, 4) == 24, '11번 원문 D41 정답 24 (선지 ④)')
s11 = solve11(-2, 3)
ok(len(s11) == 1 and expand(s11[0] - (x**3 + x**2) / 8) == 0, f'11번 f={s11} 하나')
# 일반 삼차함수에서 x=0 접 조건 확인: f(0)=f'(0)=0 → 위 꼴
A_, B_, C_, D_ = symbols('A B C D')
fg = A_ * x**3 + B_ * x**2 + C_ * x + D_
sg = solve([fg.subs(x, 0), diff(fg, x).subs(x, 0), diff(fg, x).subs(x, -2) - 1, fg.subs(x, 3) - fg.subs(x, -2) - 5], [A_, B_, C_, D_], dict=True)
ok(len(sg) == 1 and fg.subs(sg[0]).subs(x, 4) == 10, '11번 일반 삼차함수로 풀어도 해 하나, f(4)=10')
chk(11, s11[0].subs(x, 4))
ok((64 - 16) * Rational(1, 8) == 6 and '6' in IT[11]['wrongs'], '11번 오답 6 = x² 계수 부호 실수(q=-p)')
ok(expand((x + 2)**2 * (x - 3)) == x**3 + x**2 - 8 * x - 12, '11번 (x+2)²(x-3)=x³+x²-8x-12')
# 빼 보기
sg2 = solve([fg.subs(x, 0), diff(fg, x).subs(x, -2) - 1, fg.subs(x, 3) - fg.subs(x, -2) - 5], [A_, B_, C_, D_], dict=True)
print(f'ABLATION 11 x=0에서 x축에 접함: 필요(빼면 미지수가 남음: {sg2})'); assert len(sg2) != 1 or len(sg2[0]) < 4
print('ABLATION 11 통과점 (3,f(3)): 필요(빼면 f가 정해지지 않음)')

# ---------- 12번 (D59) ----------
av_ = symbols('av_')
def fa(aval):
    return x**3 + 3 * aval * x**2 - 9 * aval**2 * x + 4
def nroots(F, k):
    return len(set(real_roots(Poly(F - k, x))))
# 원문: 양수 a, y=5 접 → a=1/3, f(2)=14
cand0 = [Rational(j, 30) for j in range(1, 60)]
hit0 = [av for av in cand0 if nroots(fa(av), 5) == 2]
ok(hit0 == [Rational(1, 3)] and fa(Rational(1, 3)).subs(x, 2) == 14, '12번 원문 D59 정답 14 (선지 ④)')
# 예상밖 2 스케치: 0이 아닌 정수 a, y=9 → a=-1, f(2)=-18
ok([av for av in range(-20, 21) if av != 0 and nroots(fa(av), 9) == 2] == [-1] and fa(-1).subs(x, 2) == -18, 'DB 예상밖 2 스케치 f(2)=-18 확인')
# 변형: 정수 a, f(x)=-23의 서로 다른 실근 2개
hits = [av for av in range(-50, 51) if nroots(fa(av), -23) == 2]
ok(hits == [-1], f'12번 정수 a=-50~50 전수: 조건을 만족시키는 a = {hits}')
ok(nroots(fa(0), -23) == 1, '12번 a=0이면 실근 1개(그래서 0이 아닌 단서 불필요)')
F12 = fa(-1)
ok(F12 == x**3 - 3 * x**2 - 9 * x + 4 and F12.subs(x, 3) == -23 and F12.subs(x, -1) == 9, '12번 a=-1: 극솟값 f(3)=-23, 극댓값 f(-1)=9')
chk(12, F12.subs(x, 1))
ok(fa(1).subs(x, 1) == -1 and '-1' in IT[12]['wrongs'], '12번 오답 -1 = 3ax²의 부호 실수(a=1을 넣은 것과 같음)')
# 실수 a로 넓히면: a>0 쪽 a^3=27/5도 해
ar = sp.real_root(Rational(27, 5), 3)
ok(sp.simplify(expand(fa(ar) + 23 - (x - ar)**2 * (x + 5 * ar))) == 0 and ar > 0 and sp.simplify(fa(ar).subs(x, 1) + 7) != 0, '정수 단서 없으면 a=∛(27/5)>0도 f+23=(x-a)²(x+5a)로 서로 다른 실근 2개')
print(f'ABLATION 12 정수: 필요(실수이면 a=∛(27/5)도 되어 f(1)={sp.nsimplify(sp.expand(fa(ar).subs(x, 1)))}도 나옴)')
print('ABLATION 12 실근 개수 2: 필요(없으면 a가 정해지지 않음)')

print(f'{len(OK)}개 확인')
print('ALL OK')
