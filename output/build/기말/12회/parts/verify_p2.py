# -*- coding: utf-8 -*-
# p2.py (12회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re, sys
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor, Poly
x, t, a, b, c, k, C, p, q, g0 = symbols('x t a b c k C p q g0', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 4, 6: 3, 7: 5, 8: 2}                                       # 분담표 목표 정답
REF = {5: 'I23 후보_순위 2', 6: 'D17 분석집_변형 1', 7: 'D40 예상밖 1', 8: 'D30 분석집_변형 1'}   # 7번은 분담표 '결합 2'에서 바꿈(note)
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['I23', 'D17', 'D40', 'D30']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'
    if n == 6: assert 'STUDY-D17' in it['precedent']
    if n == 8: assert 'STUDY-D30' in it['precedent']
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 ×
    for w in it['wrongs']:
        assert f'{CIRC[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)
    txt = it['body']
    assert 'log' not in txt and '이러한' not in txt and '이와 같은' not in txt and '역함수' not in txt and '넓이' not in txt
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
    nums = {nsimplify(v) for v in re.findall(r'(?<![\w^{])\d+', it['body'])}   # 정답이 본문에 나온 수와 같지 않음
    assert nsimplify(val) not in nums, (no, val)

def P(f1, f2, u):                                                        # ∫_0^u t f(t) dt, 조각 경계 0
    return integrate(t*f1, (t, 0, u)) if u < 0 else integrate(t*f2, (t, 0, u))
def I(f1, f2, lo, hi): return P(f1, f2, hi) - P(f1, f2, lo)

# ===== 원문·분석집 변형 풀이 =====
# I23: f = x+2 (x<0), 3x+1 (x>=0), g(-3)+g(2) = 26/3
assert I(t + 2, 3*t + 1, -1, -3) + I(t + 2, 3*t + 1, -1, 2) == R(26, 3)
# I23 학교식_예상 1: x+3 / 2x+1, g(-2)+g(1) = 13/6
assert I(t + 3, 2*t + 1, -1, -2) + I(t + 3, 2*t + 1, -1, 1) == R(13, 6)
# D17: 3a+b=0, 2a+b=-2 → 극댓값 6
s = solve([3*a + b, 2*a + b + 2], [a, b]); assert (2*x**3 - 6*x + 2).subs(x, -1) == 6 and s == {a: 2, b: -6}
# STUDY-D17-변형①: x^3+ax^2+bx+22, x=3 극솟값 -5 → 극댓값 27 (대칭으로 49는 틀림)
fs = x**3 + a*x**2 + b*x + 22; ss = solve([diff(fs, x).subs(x, 3), fs.subs(x, 3) + 5], [a, b]); Fs = fs.subs(ss)
assert Fs.subs(x, -1) == 27 and diff(Fs, x).subs(x, -1) == 0
# D40: f-9x = x(x-6)^2 → 극솟값 f(5)=50
fD = x*(x - 6)**2 + 9*x; assert diff(fD, x).subs(x, 3) == 0 and diff(fD, x, 2).subs(x, 3) < 0 and fD.subs(x, 5) == 50
# D30: f=(x-1)^3-kx, 4-3k=0 → 4/3
fO = (x - 1)**3 - k*x; assert solve((fO + diff(fO, x)).subs(x, 2), k) == [R(4, 3)]
# STUDY-D30-변형①: g=(x^2-1)^2, 9+24-3k=0 → 11
gS = (x**2 - 1)**2; assert solve((gS + diff(gS, x)).subs(x, 2) - 3*k, k) == [11]

# ===== 5번 =====
f1, f2 = 3*t + 2, 3*t
G5 = lambda xv: I(f1, f2, -1, 2*xv - 1)
assert 2*(-1) - 1 == -3 and 2*2 - 1 == 3
ans5 = G5(-1) + G5(2); assert G5(-1) == -18 and G5(2) == 27
# 수치 적분으로 다시: Piecewise
fp = sp.Piecewise((3*t + 2, t < 0), (3*t, True))
assert integrate(t*fp, (t, -1, -3)) + integrate(t*fp, (t, -1, 3)) == ans5
w5a = I(f1, f2, -1, -1) + I(f1, f2, -1, 2)                          # 위끝을 x로
w5b = G5(-1) + integrate(t*f2, (t, -1, 3))                          # 0에서 나누지 않음
chk(5, ans5, [w5a, w5b])
print('ABLATION 5 위끝 2x-1: 필요(x이면', w5a, ')')
print('ABLATION 5 조각 x<0 가지: 필요(3x 하나면', integrate(t*3*t, (t, -1, -3)) + integrate(t*3*t, (t, -1, 3)), ')')

# ===== 6번 =====
f6 = x**3 + a*x**2 + b*x + 2*a
s6 = solve([diff(f6, x).subs(x, 1), f6.subs(x, 1) - 1], [a, b], dict=True)
assert len(s6) == 1 and s6[0] == {a: 3, b: -9}                       # 해 하나
F6 = f6.subs(s6[0]); assert expand(F6) == x**3 + 3*x**2 - 9*x + 6
cr = solve(diff(F6, x), x); assert set(cr) == {-3, 1}
assert diff(F6, x, 2).subs(x, 1) > 0 and diff(F6, x, 2).subs(x, -3) < 0   # x=1 극소, x=-3 극대
ans6 = F6.subs(x, -3)
assert factor(F6 - 1) == (x - 1)**2*(x + 5)
w6 = R(1, 2)*(1 - (-3))**3                                           # 극값 차만
trap = 2*F6.subs(x, 0) - 1; assert trap == 11 and trap != ans6       # (0, 2a) 대칭으로 쓴 값(선지 밖, note)
chk(6, ans6, [w6])
fn = x**3 + a*x**2 + b*x + 2*a; sn = solve([diff(fn, x).subs(x, 1)], [b], dict=True)[0]
print('ABLATION 6 극솟값 1: 필요(빼면 a가 정해지지 않음:', expand(fn.subs(sn)), ')')
f6c = x**3 + a*x**2 + b*x + 3*a; s6c = solve([diff(f6c, x).subs(x, 1), f6c.subs(x, 1) - 1], [a, b], dict=True)[0]
F6c = f6c.subs(s6c); M6c = [F6c.subs(x, r) for r in solve(diff(F6c, x), x) if diff(F6c, x, 2).subs(x, r) < 0][0]
assert M6c != ans6
print('ABLATION 6 상수항 2a: 일함(상수항이 3a이면', s6c, ', 극댓값', M6c, ')')

# ===== 7번 =====
f7 = integrate(3*(x - 3)*(x - 5), x)                                 # f(0)=0이라 적분상수 0
assert f7.subs(x, 0) == 0 and expand(f7) == x**3 - 12*x**2 + 45*x
assert diff(f7, x, 2).subs(x, 3) < 0 and diff(f7, x, 2).subs(x, 5) > 0
def npts(kv):
    return len(set(sp.Poly(f7 - kv*x, x).real_roots()))
ks = []
Q = x**2 - 12*x + 45 - k
# 서로 다른 실근 2개 ⇔ Q(0)=0 (다른 근 ≠0) 또는 Q 판별식 0 (중근 ≠0)
kc = set(solve(Q.subs(x, 0), k)) | set(solve(sp.discriminant(Q, x), k))
for kv in kc:
    if npts(kv) == 2: ks.append(kv)
assert sorted(ks) == [9, 45]
for kv in range(-200, 201):                                          # 정수 k 전수: 2개인 것은 9, 45뿐
    assert (npts(kv) == 2) == (kv in (9, 45)), kv
for kv in [R(j, 4) for j in range(-40, 240)]:                        # 분수 k 표본
    if kv not in (9, 45): assert npts(kv) != 2
ans7 = sum(ks)
w7 = 45                                                              # 원점 접함 갈래만
assert factor(f7 - 45*x) == x**2*(x - 12) and factor(f7 - 9*x) == x*(x - 6)**2
chk(7, ans7, [w7])
print('ABLATION 7 x=5 극소: 필요(빼면 f의 이차항·일차항이 정해지지 않음)')
fa = x**3 + p*x**2 + q*x; print('ABLATION 7 f(0)=0: 필요(빼면 상수항 C가 남아 f-kx가 x를 인수로 갖지 않음, 갈래 구조가 달라짐)')
print('ABLATION 7 개수 2: 필요(빼면 k가 정해지지 않음)')

# ===== 8번 =====
h = x**2*(x - 5)**2
f8 = h - k*x
assert expand(f8 + k*x - h) == 0 and Poly(f8, x).LC() == 1
# 유일성: h = f+kx 는 최고차항 1 사차, 실근이 0, 5뿐, |h| 미분가능 ⇒ 각 실근에서 h'=0
# 후보 꼴 x^i (x-5)^j r(x) (r은 실근 없는 이차 또는 1), 차수 4, i, j >= 1
cands = []
for i in range(1, 4):
    for j in range(1, 4):
        if i + j == 4: cands.append((i, j, 1))
        if i + j == 2: cands.append((i, j, 'quad'))
okc = []
for i, j, r in cands:
    if r == 1:
        hh = x**i*(x - 5)**j
        if diff(hh, x).subs(x, 0) == 0 and diff(hh, x).subs(x, 5) == 0: okc.append((i, j))
    else:
        hh = x*(x - 5)*(x**2 + p*x + q)                              # 단순근 0, 5: h'(0) = -5q ≠ 0 (q>0 이어야 실근 없음 조건 일부)
        assert sp.simplify(diff(hh, x).subs(x, 0) + 5*q) == 0
assert okc == [(2, 2)]
ans8_l = solve((f8 + diff(f8, x)).subs(x, 3), k); assert len(ans8_l) == 1
ans8 = ans8_l[0]
assert h.subs(x, 3) == 36 and diff(h, x).subs(x, 3) == -12
F8 = f8.subs(k, ans8)
assert set(sp.Poly(F8 + ans8*x, x).real_roots()) == {0, 5}          # 곡선과 직선 y=-kx: x=0, 5에서만
w8 = solve(h.subs(x, 3) - 3*k + diff(h, x).subs(x, 3), k)[0]         # f'에서 -k 누락
chk(8, ans8, [w8])
print('ABLATION 8 |f+kx| 미분가능: 필요(빼면 h=x(x-5)(x²+px+q) 등으로 정해지지 않음)')
h3 = x**2*(x - 5); fb = h3 - k*x
print('ABLATION 8 사차: 필요(삼차이면 두 근 모두 중근이 될 수 없음 — 조건을 만족하는 함수 없음)')
print('ABLATION 8 x=0, 5에서만: 필요(빼면 근 위치가 정해지지 않음)')
print('ABLATION 8 f(3)+f\'(3)=0: 필요(빼면 k가 정해지지 않음)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [4, 3, 5, 2]
print('ALL OK')
