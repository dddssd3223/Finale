# -*- coding: utf-8 -*-
# p2.py (8회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor, oo, Interval, S
x, t, a, b, c, p, m = symbols('x t a b c p m', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 1, 6: 3, 7: 5, 8: 2}                                       # 분담표 목표 정답
REF = {5: 'D12 후보_순위 3', 6: 'M5 v3_추가 1', 7: 'D44 분석집_변형 1', 8: 'D13 후보_순위 2'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['D12', 'M5', 'D44', 'D13']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'       # 분담표 목표 수준
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 ×
    for w in it['wrongs']:
        assert f'{CIRC[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)
    txt = it['body']
    assert 'log' not in txt and '이러한' not in txt and '이와 같은' not in txt
    for mm in re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', txt, re.S):
        assert '<' not in ''.join(mm) and '>' not in ''.join(mm), (n, mm)

def num(s_):
    s_ = re.sub(r'\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', r'(\1)/(\2)', s_)
    return nsimplify(sp.sympify(s_))

def chk(no, val, wrongs):
    it = IT[no]; chv = [num(c_) for c_ in it['choices']]; ws = [num(w) for w in it['wrongs']]
    dd = {chv[i + 1] - chv[i] for i in range(4)}
    good = (it['ans'] == WANT[no] and nsimplify(val) == chv[it['ans'] - 1] and len(set(chv)) == 5 and len(dd) == 1 and 0 not in dd
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {chv[it["ans"] - 1]} (위치 {it["ans"]}), 공차 {chv[1] - chv[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def dec_set(fp):
    """f'(x)<=0인 x의 집합"""
    return sp.solve_univariate_inequality(fp <= 0, x, relational=False)

# ===== 원문 풀이 =====
# D12: f'=-6(x+1)(x-4)>0 on (-1,4) → 5
fD12 = -2*x**3 + 9*x**2 + 24*x - 3
assert sp.solve_univariate_inequality(diff(fD12, x) >= 0, x, relational=False) == Interval(-1, 4)
# LIVE1-01-026: x^3-3x+1이 [a,b]에서 감소 → 2
assert dec_set(diff(x**3 - 3*x + 1, x)) == Interval(-1, 1)
# M5: y'=8x^3-6x-2, x>0 최소 x=1/2, 기울기 -4, y절편 35/8 → 43
yM = 2*x**4 - 3*x**2 - 2*x + 4; sM = diff(yM, x)
assert sp.minimum(sM, x, Interval.open(0, oo)) == -4 and sM.subs(x, R(1, 2)) == -4
icp = yM.subs(x, R(1, 2)) - R(1, 2)*sM.subs(x, R(1, 2)); assert icp == R(35, 8) and 35 + 8 == 43
# D44: m<1, 극점 (1-m)/2,1,2-m/2,3,…, 합 19-2m=18 → m=1/2, g'(11/3)=f'(2/3)-1/2=-5/6
# D13: a>=-9/5 → f(0)=16+2a 최솟값 62/5 → 67 ; GEN1-01-014: 극댓값 81/5
fD = x**3 + a*x**2 + b*x + c
s13 = solve([fD.subs(x, 1) - 5, fD.subs(x, 2)], [b, c], dict=True)[0]; f13 = fD.subs(s13); d13 = diff(f13, x)
lo13 = max(solve(d13.subs(x, -1), a)[0], solve(d13.subs(x, 1), a)[0]); assert lo13 == R(-9, 5)
assert f13.subs({x: 0, a: lo13}) == R(62, 5) and 62 + 5 == 67 and f13.subs({x: -1, a: lo13}) == R(81, 5)
print('원문·DB 풀이 OK (D44는 아래 극점 함수로)')

# ===== 5번 =====
q = symbols('q0:4', real=True)
g5 = x**3 + q[2]*x**2 + q[1]*x + q[0]                                  # 최고차항 1인 일반 삼차
eqs = sp.Poly(expand(g5.subs(x, 2 + x) + g5.subs(x, 2 - x)), x).all_coeffs()
sol5 = solve(list(eqs) + [diff(g5, x).subs(x, 5)], q[:3], dict=True)
assert len(sol5) == 1                                                  # 조건을 만족시키는 f는 하나
f5 = expand(g5.subs(sol5[0])); assert expand(f5 - ((x - 2)**3 - 27*(x - 2))) == 0
assert expand(diff(f5, x) - 3*(x - 5)*(x + 1)) == 0
G5 = f5.subs(x, 2*x + 1); D5 = dec_set(diff(G5, x)); assert D5 == Interval(-1, 2)
# [a,b]에서 감소 ⇔ [a,b]⊂D5 (g'은 [-1,2] 밖에서 양수, 안에서 0은 끝점뿐) → b-a 최댓값 = 길이
assert sp.solve(diff(G5, x), x) == [-1, 2]
ans5 = D5.measure
chk(5, ans5, [dec_set(diff(f5, x)).measure])                           # 오답 6: f 자신의 감소 구간 길이
print('ABLATION 5 점대칭 조건: 필요(빼면 f\'의 다른 근이 정해지지 않아 답이 정해지지 않음)')
fr = x**3 + q[2]*x**2 + q[1]*x; frs = solve(diff(fr, x).subs(x, 5), q[1], dict=True)[0]
lens = {dec_set(diff(fr.subs(frs).subs(q[2], v).subs(x, 2*x + 1), x)).measure for v in (-6, -9, 0)}
assert len(lens) > 1; print('   (점대칭 없이 f\'(5)=0만: 길이', sorted(lens), '등으로 바뀜)')
print('ABLATION 5 f\'(5)=0: 필요(빼면 f=(x-2)^3+p(x-2)의 p가 남아 길이가', [dec_set(diff(((x-2)**3 + pv*(x-2)).subs(x, 2*x+1), x)).measure for pv in (-3, -12, -27)], '등으로 바뀜)')
print('ABLATION 5 인자 2x+1 → x: 필요(답', dec_set(diff(f5, x)).measure, '로 바뀜)')
neg = -f5
assert dec_set(diff(neg.subs(x, 2*x + 1), x)) == sp.Union(Interval(-oo, -1), Interval(2, oo))
print('ABLATION 5 최고차항의 계수의 부호(양수): 필요(음수면 감소 구간이 두 반직선이라 최댓값이 없음)')

# ===== 6번 =====
F6 = integrate(4*t**3 - 6*t**2 + 1, (t, 0, x)) + 5; assert expand(F6 - (x**4 - 2*x**3 + x + 5)) == 0
s6 = diff(F6, x); assert s6 == 4*x**3 - 6*x**2 + 1
mn = sp.minimum(s6, x, Interval.open(0, oo)); assert mn == -1
tp = [r for r in solve(s6 - mn, x) if r > 0]; assert tp == [1]         # 기울기 최소인 접점은 x=1 하나(유일)
yint = F6.subs(x, 1) - 1*s6.subs(x, 1); assert yint == 6
chk(6, yint, [F6.subs(x, 1) + 1*s6.subs(x, 1), F6.subs(x, 1)])         # 오답 4(부호), 5(접점 y좌표)
assert sp.limit(s6, x, -oo) == -oo
print('ABLATION 6 x좌표가 양수: 필요(실수 전체에서는 기울기가 한없이 작아져 최솟값이 없음)')
print('ABLATION 6 상수 +5: 필요(빼면 답', yint - 5, '로 바뀜)')

# ===== 7번 =====
f0 = [(-x**2 + x, 0, 1), (-x**2 + 4*x - 3, 1, 3)]                     # (가) 한 주기 조각
def pieces(k, A):
    """둘째 이후 주기: f(x)=A^k f0(x-3k) (A=2이면 f(x+3)=2f(x), A=1이면 원문 주기)"""
    return [(A**k*e.subs(x, x - 3*k), lo + 3*k, hi + 3*k) for e, lo, hi in f0]
def fval(xv, A):
    k = 0
    while xv > 3*(k + 1): k += 1
    for e, lo, hi in pieces(k, A):
        if lo < xv <= hi or (lo == 0 and 0 < xv < hi): return e.subs(x, xv)
    raise ValueError(xv)
def extrema(mv, A, N=4):
    """g=f-mx의 극대·극소점 (0, 3N]: 조각 안 정류점과 조각 경계(꺾인 점)를 정확한 유리수 ε로 판정"""
    cand = set()
    for k in range(N):
        for e, lo, hi in pieces(k, A):
            for r in solve(diff(e, x) - mv, x):
                if lo < r < hi: cand.add(r)
            cand.add(hi)
    eps = R(1, 10**6); out = []
    for c0 in sorted(cand):
        if c0 >= 3*N: continue
        g = lambda v: fval(v, A) - mv*v
        l, rr = g(c0 - eps) - g(c0), g(c0 + eps) - g(c0)
        if l*rr > 0: out.append(c0)
    return out
assert all(fval(R(v), 2) == 0 for v in (1, 3, 4, 6, 7)) and fval(R(3), 2) == 0   # 연속(경계값 0)
# 원문 확인: A=1, m=1/2 → α7<6≤α8, 합 18, g'(11/3)=-5/6
E = extrema(R(1, 2), 1, N=3); assert E[6] < 6 <= E[7] and sum(E[:7]) == 18
assert diff(f0[0][0], x).subs(x, R(2, 3)) - R(1, 2) == R(-5, 6)
# 7번: A=2, x=4에서 극값을 갖지 않는 m (전수: 꺾인 점 판정을 정확한 ε로)
def ext_at(mv, c0, A=2):
    eps = R(1, 10**6); g = lambda v: fval(v, A) - mv*v
    return (g(c0 - eps) - g(c0))*(g(c0 + eps) - g(c0)) > 0
lt, rt = sp.limit(diff(pieces(1, 2)[0][0], x), x, 4, '-'), sp.limit(diff(pieces(1, 2)[1][0], x), x, 4, '+')
assert (lt, rt) == (-2, 4)
grid = sorted({R(i, 20) for i in range(1, 200)} | {R(4)})
noext = [mv for mv in grid if not ext_at(mv, 4)]
assert noext and min(noext) == 4 and all(mv >= 4 for mv in noext) and all(not ext_at(mv, 4) for mv in grid if mv >= 4)
assert ext_at(R(399, 100), 4) and not ext_at(R(4), 4)                     # 경계 m=4는 포함(극값 없음)
ans7 = min(noext)
w1 = sp.limit(diff(f0[1][0], x), x, 1, '+')                              # 주기로 착각: 2-m≤0 → 2
chk(7, ans7, [w1])
print('ABLATION 7 f(x+3)=2f(x) → f(x+3)=f(x): 필요(답', min(mv for mv in grid if not ext_at(mv, 4, A=1)), '로 바뀜)')
print('ABLATION 7 계수 2 → 3: 필요(답', min(mv for mv in sorted(set(grid) | {R(6)}) if not ext_at(mv, 4, A=3)), '로 바뀜)')
print('ABLATION 7 x=4 → x=1: 필요(답', min(mv for mv in grid if not ext_at(mv, 1)), '로 바뀜)')

# ===== 8번 =====
s8 = solve([fD.subs(x, 1) - 10, fD.subs(x, 2)], [b, c], dict=True)[0]; f8 = fD.subs(s8)
assert s8 == {b: -3*a - 17, c: 2*a + 26}
h8 = f8 - x; d8 = diff(h8, x)
# 아래로 볼록한 h'이 (-1,1)에서 ≤0 ⇔ 양 끝값 ≤0 (일반 a 전수: 꼭짓점 판정 불필요 확인)
r1 = sp.solve_univariate_inequality(d8.subs(x, -1) <= 0, a, relational=False)
r2 = sp.solve_univariate_inequality(d8.subs(x, 1) <= 0, a, relational=False)
rng8 = r1.intersect(r2); assert rng8 == Interval(-3, oo)
for av in (-4, R(-31, 10)):                                               # a<-3이면 (-1,1) 안에 h'>0인 점이 있음
    assert sp.maximum(d8.subs(a, av), x, Interval.open(-1, 1)) > 0
f0min = sp.minimum(f8.subs(x, 0), a, rng8); assert f0min == 20
amin = solve(f8.subs(x, 0) - 20, a); assert amin == [-3]                 # f(0)이 최소인 함수는 하나
H = h8.subs(a, -3); assert expand(diff(H, x) - 3*(x - 3)*(x + 1)) == 0
crit = solve(diff(H, x), x); mx = [r for r in crit if diff(H, x, 2).subs(x, r) < 0]; assert mx == [-1]
ans8 = H.subs(x, -1); assert ans8 == 25
chk(8, ans8, [f8.subs({a: -3, x: -1})])                                  # 오답 24: f(-1)
s8b = solve([fD.subs(x, 1) - 10, fD.subs(x, 2)], [b, c], dict=True)[0]
d8b = diff(fD.subs(s8b), x); ab = max(solve(d8b.subs(x, -1), a)[0], solve(d8b.subs(x, 1), a)[0])
print('ABLATION 8 f(x)-x → f(x) 감소: 필요(a≥', ab, '가 되어 f(x)-x의 극댓값이 무리수', sp.N(sp.maximum(fD.subs(s8b).subs(a, ab) - x, x, Interval(-2, sp.Rational(-1, 2))), 6), '로 바뀜)')
print('ABLATION 8 f(0)이 최소일 때: 필요(빼면 a≥-3의 모든 a가 가능해 극댓값이 정해지지 않음)')
print('ABLATION 8 A(1,10): 필요(원문 A(1,5)면 a≥-2, 극댓값', (fD.subs(solve([fD.subs(x, 1) - 5, fD.subs(x, 2)], [b, c], dict=True)[0]) - x).subs({a: -2, x: -1}), '로 바뀜)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [1, 3, 5, 2]
print('ALL OK')
