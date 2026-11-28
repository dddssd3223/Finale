# -*- coding: utf-8 -*-
# p3.py (7회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, Interval, S, Max, Min, oo

x = symbols('x', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 5, 10: 3, 11: 2, 12: 4}
DBREF = {9: 'M49 v3_추가 1', 10: 'M3 v3_추가 1', 11: 'M37 후보_순위 3', 12: 'M45 v3_추가 1'}
KEYS = {9: 'M49', 10: 'M3', 11: 'M37', 12: 'M45'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

def val(c):
    c = re.sub(r'\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1) if m else Rational(c)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == '중', f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    ok('이러한' not in it['body'] and '이와 같은' not in it['body'], f'{n}번 금지 어구 없음')
    ok(not re.search(r'\\[\(\[][^)\]]*[<>]', it['body']), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')

def chk(n, v0):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    return v

def nroots(P, lo, hi):
    """다항식 P의 [lo, hi]에서의 서로 다른 실근 개수"""
    return len({r for r in real_roots(Poly(P, x)) if lo <= r <= hi})

# ---------- 9번 (M49) ----------
orig9 = [a for a in range(-60, 61) if nroots(2 * x**3 + 6 * x**2 + a, -2, 2) == 2]
ok(len(orig9) == 8 and orig9 == list(range(-8, 0)), f'9번 원문 M49 정답 8개(③), 해집합 {orig9[0]}..{orig9[-1]}')
ok(min(orig9) == -8, 'DB v3_추가 1 스케치(원문 식의 최솟값) −8 확인')
A9 = [a for a in range(-100, 101) if nroots(2 * x**3 + 6 * x**2 + a - 18 * x, -2, 2) == 2]
ok(A9 == list(range(-4, 10)), f'9번 변형 해집합 정수 a = {A9[0]}..{A9[-1]} (조작_보강 1의 14개와 같음)')
H = 2 * x**3 + 6 * x**2 - 18 * x
ok((H.subs(x, -2), H.subs(x, 1), H.subs(x, 2)) == (44, -10, 4) and expand(diff(H, x) - 6 * (x - 1) * (x + 3)) == 0, '9번 h(−2)=44, h(1)=−10, h(2)=4')
# 실수 범위로도 경계 확인: a=-4 두 근, a 조금 작으면 한 근
ok(nroots(H - 4, -2, 2) == 2 and nroots(H - 4 - Rational(1, 100), -2, 2) == 1 and nroots(H + 10, -2, 2) == 1, '9번 경계: −a=4 두 근(포함), −a>4 한 근, −a=−10 한 근')
v9 = chk(9, min(A9))
ok(val(IT[9]['wrongs'][0]) == min(orig9), '9번 오답 −8 = 18x를 넘기지 않은 값')
print('ABLATION 9 우변 18x: 필요(0이면 최솟값 −8)')
B9 = [a for a in range(-200, 201) if nroots(H + a, -oo, oo) == 2]
ok(set(B9) == {10, -54}, f'구간 없으면 두 실근인 정수 a = {B9}')
print(f'ABLATION 9 −2≤x≤2: 필요(없으면 a={sorted(B9)}뿐이라 최솟값 {min(B9)})')
C9 = [a for a in range(-100, 101) if nroots(H + a, -2, 2) >= 1]
print(f'ABLATION 9 서로 다른 두 실근: 필요(실근을 갖기만 하면 최솟값 {min(C9)})')
assert min(C9) == -44

# ---------- 10번 (M3) ----------
def fmax(F, lo, hi):
    cand = [lo, hi] + [r for r in real_roots(Poly(diff(F, x), x)) if lo < r < hi]
    return max(F.subs(x, c) for c in cand)
def fmin(F, lo, hi):
    cand = [lo, hi] + [r for r in real_roots(Poly(diff(F, x), x)) if lo < r < hi]
    return min(F.subs(x, c) for c in cand)
fo = 3 * x**4 - 4 * x**3 - 36 * x**2 + 2
ok(fmax(fo, -1, 1) == 2 and 2 - fmin(fo, -1, 1) == 37, '10번 원문 M3 정답 37(③)')
# v3 스케치: 무리수 답 확인
r3 = solve(3 * x**2 - 4 * x - 36, x)
ok(sp.simplify(2 * min(abs(r) for r in r3) - (8 * sp.sqrt(7) - 4) / 3) == 0, 'DB v3_추가 1 스케치 답 (8√7−4)/3 확인(무리수라 함수 교체)')
g = x**4 - 2 * x**3 - 35 * x**2          # f(x)-a
ok(expand(g - x**2 * (x - 7) * (x + 5)) == 0 and expand(diff(g, x) - 2 * x * (x - 5) * (2 * x + 7)) == 0, '10번 f−a=x²(x+5)(x−7), f′=2x(2x+7)(x−5)')
def good10(av, L=lambda a: -a / 2, R=lambda a: 2 * a):
    return fmax(g, L(av), R(av)) == 0     # 최댓값이 a ⇔ max(f−a)=0
grid = [Rational(j, 8) for j in range(1, 121)]
G10 = [av for av in grid if good10(av)]
ok(G10 == [av for av in grid if av <= Rational(7, 2)], f'10번 조건을 만족시키는 a(1/8 간격 전수)는 0<a≤7/2: 최댓값 {max(G10)}')
ok(not good10(Rational(7, 2) + Rational(1, 1000)) and good10(Rational(7, 2)), '10번 a=7/2 포함, 조금 넘으면 f(2a)>a')
v10 = chk(10, max(G10))
# 오답 5/2: 극소점 5까지만
ok(val(IT[10]['wrongs'][0]) == min(Rational(5, 2), 2 * Rational(7, 2)) == Rational(5, 2), '10번 오답 5/2 = 2a≤5(극소점 기준)')
sym = [av for av in grid if good10(av, R=lambda a: a / 2)]
ok(max(sym) == 10, '원문 구간 [−a/2, a/2]이면 최댓값 10')
print('ABLATION 10 오른끝 2a: 필요(a/2이면 답 10)')
left = [av for av in grid if good10(av, L=lambda a: -a)]
print(f'ABLATION 10 왼끝 −a/2: 군더더기 아님(구간을 정하는 끝, −a로 바꾸면 답 {max(left)} — 왼끝은 판정에서 지는 쪽)')
print('ABLATION 10 양수 a: 필요(a≤0이면 구간이 정해지지 않음)')
print('ABLATION 10 최댓값이 a: 필요(없으면 a에 조건이 없음)')

# ---------- 11번 (M37) ----------
def ext_points(left, right, p):
    """x<p에서 left, x≥p에서 right인 연속함수의 극점(도함수 부호가 바뀌는 점) 목록"""
    pts = []
    dl, dr = diff(left, x), diff(right, x)
    for r in set(real_roots(Poly(dl, x))):
        if r < p and sp.degree(sp.gcd(Poly(dl, x), Poly(diff(dl, x), x))) == 0: pts.append(r)
    for r in set(real_roots(Poly(dr, x))):
        if r > p and Poly(diff(dr, x), x).eval(r) != 0: pts.append(r)
    eps = Rational(1, 10**6)
    sl, sr = sp.sign(dl.subs(x, p - eps)), sp.sign(dr.subs(x, p + eps))
    if sl * sr < 0: pts.append(sp.Integer(p))
    return sorted(pts)
a_, b_ = symbols('a b')
# 원문
ao = solve((-x**3 - x**2 + 8 * x + a_).subs(x, 3), a_)[0]
cand = [bv for bv in [Rational(j, 2) for j in range(-20, 41)] if len(E := ext_points(-x**3 - x**2 + 8 * x + ao, (x - 3) * (x - bv), 3)) == 3 and sum(E) == Rational(10, 3)]
ok(ao == 12 and cand == [5] and ao + 5 == 17, '11번 원문 M37 정답 17')
# LIVE1-02-121
al = solve((x**3 - x**2 + a_ * x + 12).subs(x, -3), a_)[0]
candl = [bv for bv in [Rational(j, 2) for j in range(-40, 41)] if len(E := ext_points((x + 3) * (x + bv), x**3 - x**2 + al * x + 12, -3)) == 3 and sum(E) == Rational(-13, 3)]
ok(al == -8 and candl == [7] and al + 7 == -1, 'LIVE1-02-121 정답 −1(③) 확인')
# 변형
cub = x**3 - 6 * x**2 + a_ * x + 16
a11 = solve(cub.subs(x, -1), a_)
ok(a11 == [9], '11번 연속 조건 a=9 하나')
cub = cub.subs(a_, 9)
ok(expand(diff(cub, x) - 3 * (x - 1) * (x - 3)) == 0, '11번 삼차식의 극점 1, 3(모두 x>−1)')
cand11 = []
for bv in [Rational(j, 4) for j in range(-80, 161)]:
    E = ext_points((x + 1) * (x + bv), cub, -1)
    if bv <= 1: assert E == [-1, 1, 3], (bv, E)
    else: assert E == [-(bv + 1) / 2, 1, 3], (bv, E)
    if len(E) == 3 and sum(E) == 1: cand11.append(bv)
ok(cand11 == [5], f'11번 b 전수(1/4 간격, −20..40): b≤1이면 극점 −1, 1, 3(합 3), b>1이면 −(b+1)/2, 1, 3 → b={cand11}')
bs = solve(-(b_ + 1) / 2 + 4 - 1, b_)
ok(bs == [5], '11번 식으로도 b=5 하나')
v11 = chk(11, 9 + 5)
ok(val('16') == solve(1 - 6 - a_ + 16, a_)[0] + 5 and '16' in IT[11]['wrongs'], '11번 오답 16 = (−1)³ 부호 실수 a=11')
ok(val('17') == ao + 5 and '17' in IT[11]['wrongs'], '11번 오답 17 = 원문 답')
print('ABLATION 11 연속: 필요(없으면 a가 정해지지 않음)')
print('ABLATION 11 합 1: 필요(없으면 b>1인 모든 b)')
E3 = ext_points((x + 1) * (x + 5), cub, -1)
ok(len(E3) == 3, "11번 '세 실수에서만 극값'은 b=5에서 성립(합 조건이 정해 주므로 개수 문구는 원문 문장 그대로)")
print('ABLATION 11 서로 다른 세 실수에서만: 원문 문장 그대로(합 조건의 뜻을 정하는 문장, b≤1·b>1 모두 극점 3개)')

# ---------- 12번 (M45) ----------
fo12 = 2 * x**3 + 3 * x**2 - 12 * x - 8
def kmin(F):
    return max(abs(fmax(F, -2, 2)), abs(fmin(F, -2, 2)))
ok(kmin(fo12) == 15, '12번 원문 M45 정답 15')
c_ = symbols('c')
h0 = 2 * x**3 + 3 * x**2 - 12 * x          # (가운데) − 12x, 상수항 제외
ok(expand((2 * x**3 + 3 * x**2 + c_) - 12 * x) == h0 + c_, '12번 가운데 식 − 12x = 2x³+3x²−12x+c')
ok((h0.subs(x, -2), h0.subs(x, 1), h0.subs(x, 2)) == (20, -7, 4) and fmax(h0, -2, 2) == 20 and fmin(h0, -2, 2) == -7, '12번 h의 최댓값 c+20, 최솟값 c−7')
cands = sorted({s for v_ in (20, -7, 4) for s in (19 - v_, -19 - v_)})
sol12 = [cv for cv in cands if kmin(h0 + cv) == 19]
ok(sol12 == [-12, -1], f'12번 후보 {cands} 중 k의 최솟값이 19인 c = {sol12}')
grid12 = [Rational(j, 4) for j in range(-200, 201)]
ok([cv for cv in grid12 if kmin(h0 + cv) == 19] == [-12, -1], '12번 c 전수(1/4 간격, −50..50)도 −12, −1뿐')
v12 = chk(12, sum(sol12))
sk = [cv for cv in grid12 if kmin(h0 + cv) == 15]
ok(sk == [-8, -5] and sum(sk) == -13, 'DB v3_추가 1 스케치(최솟값 15) c=−8, −5, 합 −13 확인')
g0 = 2 * x**3 + 3 * x**2
w12 = [cv for cv in grid12 if kmin(g0 + cv) == 19]
ok(val(IT[12]['wrongs'][0]) == 7 - 19 == min(sol12), '12번 오답 −12 = 극솟값 쪽 갈래만 구한 값')
ok(sum(w12) != -13, f'12x를 빼면 c={w12}')
print(f'ABLATION 12 양 끝의 12x: 필요(없으면 합 {sum(w12)})')
k20 = [cv for cv in grid12 if kmin(h0 + cv) == 13]
print(f'ABLATION 12 최솟값 19: 필요(없으면 c가 정해지지 않음. 값이 13이면 c={k20}로 개수가 바뀜)')
def kmin_iv(F, lo, hi): return max(abs(fmax(F, lo, hi)), abs(fmin(F, lo, hi)))
w3 = [cv for cv in grid12 if kmin_iv(h0 + cv, -2, 3) == 19]
ok(w3 == [], f'구간을 [−2, 3]으로 바꾸면 c={w3}(최댓값 c+45, 최솟값 c−7이라 k의 최솟값은 26 이상)')
print('ABLATION 12 −2≤x≤2: 필요(구간이 [−2, 3]이면 조건을 만족시키는 c가 없음)')

print(f'{len(OK)} checks')
print('ALL OK')
