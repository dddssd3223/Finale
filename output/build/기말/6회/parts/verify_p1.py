# -*- coding: utf-8 -*-
# p1.py (6회 1–4번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지(분담표 정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, Abs
x, a, b, C, m, n = symbols('x a b C m n', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 4, 2: 2, 3: 5, 4: 1}                                   # 분담표 정답 ④ ② ⑤ ①
KEY = {1: ('J5', 'J5 분석집_변형 1'), 2: ('I22', 'I22 분석집_변형 1'), 3: ('I26', 'I26 분석집_변형 1'), 4: ('M4', '자체 (가장 가까운 M4)')}
DESC = {4}                                                         # 내림차순 선지 번호
assert sorted(IT) == [1, 2, 3, 4]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
for no in (1, 2, 3):
    assert 'STUDY-' + IT[no]['key'] + '-변형①' in IT[no]['precedent']

def cv(c):
    return nsimplify(re.sub(r'\\dfrac\{(\d+)\}\{(\d+)\}', r'(\1)/(\2)', str(c)))

def arith(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0, list(d)[0]

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    ok_ar, dd = arith(no)
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and ok_ar and ((dd < 0) == (no in DESC))
            and abs(dd) in (1, 2, 5, Rational(1, 2), Rational(1, 5))
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def area_x(f):
    """곡선 y=f(x)와 x축으로 둘러싸인 넓이(실근 사이 |f| 적분)와 실근"""
    r = sorted(set(real_roots(Poly(expand(f), x))))
    return sum(Abs(integrate(f, (x, r[i], r[i + 1]))) for i in range(len(r) - 1)), r

def maxmin(f, lo, hi):
    cs = [z for z in solve(diff(f, x), x) if z.is_real and lo <= z <= hi]
    vals = [f.subs(x, v) for v in [lo, hi] + cs]
    return max(vals), min(vals), cs

# ===== 원문 · 분석집 변형 풀이 =====
# J5: f(0)=0, f'(0)=9, f(3)=f'(3)=0 → f=x(x-3)^2, 넓이 27/4 (④)
p_, q_, r_, s_ = symbols('p_ q_ r_ s_')
F = p_*x**3 + q_*x**2 + r_*x + s_
sJ = solve([F.subs(x, 0), diff(F, x).subs(x, 0) - 9, F.subs(x, 3), diff(F, x).subs(x, 3)], [p_, q_, r_, s_], dict=True)
assert len(sJ) == 1 and expand(F.subs(sJ[0]) - x*(x - 3)**2) == 0 and area_x(F.subs(sJ[0]))[0] == Rational(27, 4)
# 분석집 J5 변형①: f(0)=0, f'(0)=8, f(4)=0, f'(4)=8 → x(x-2)(x-4), 넓이 8
sJ2 = solve([F.subs(x, 0), diff(F, x).subs(x, 0) - 8, F.subs(x, 4), diff(F, x).subs(x, 4) - 8], [p_, q_, r_, s_], dict=True)
assert len(sJ2) == 1 and expand(F.subs(sJ2[0]) - x*(x - 2)*(x - 4)) == 0 and area_x(F.subs(sJ2[0]))[0] == 8
# I22: f'=3(x+1)(x-2), ∫_{-2}^{2} f=0 → f(4)=18 (④)
fI = integrate(3*(x + 1)*(x - 2), x) + C
cI = solve(integrate(fI, (x, -2, 2)), C)
assert cI == [2] and fI.subs(C, 2).subs(x, 4) == 18
# 분석집 I22 변형①: f'=3(x+1)(x-3), ∫_{-3}^{5} f=0 → 극댓값 16
fS = integrate(3*(x + 1)*(x - 3), x) + C
cS = solve(integrate(fS, (x, -3, 5)), C)
assert len(cS) == 1 and fS.subs(C, cS[0]).subs(x, -1) == 16
# I26: ∫_{-3}^{3} x f = ∫ f = 36 → f(2)=11
g = x**2 + a*x + b
sI = solve([integrate(x*g, (x, -3, 3)) - 36, integrate(g, (x, -3, 3)) - 36], [a, b], dict=True)
assert len(sI) == 1 and g.subs(sI[0]).subs(x, 2) == 11
# 분석집 I26 변형①: 삼차 f=x^3+ax^2+bx+c, ∫_{-1}^{1} f = ∫ x^2 f = 4/3 → f(2)+f(-2)=38 (b와 무관)
c_ = symbols('c_')
h = x**3 + a*x**2 + b*x + c_
sH = solve([integrate(h, (x, -1, 1)) - Rational(4, 3), integrate(x**2*h, (x, -1, 1)) - Rational(4, 3)], [a, c_], dict=True)
assert len(sH) == 1 and expand((h.subs(x, 2) + h.subs(x, -2)).subs(sH[0])) == 38
# M4: [-2,2], f=x^3/3+x^2-3x+1 → M-m=9 (④)
M0, m0, _ = maxmin(x**3/3 + x**2 - 3*x + 1, -2, 2)
assert M0 - m0 == 9
print('원문·분석집 풀이 OK (J5=27/4, STUDY-J5=8, I22=18, STUDY-I22=16, I26=11, STUDY-I26=38, M4=9)')

# ===== 1번 =====
f1 = 4*x**3 - 12*x**2 + 8*x
assert expand(f1 - 4*x*(x - 1)*(x - 2)) == 0
A1, r1 = area_x(f1)
assert r1 == [0, 1, 2] and A1 == 2
part = integrate(f1, (x, 0, 1))                                    # 오답: 위쪽 한 부분만
assert part == 1 and integrate(f1, (x, 0, 2)) == 0                 # 참고: 한 번에 ∫0^2 하면 0 (선지 밖)
chk(1, A1, [part])

# ===== 2번 =====
f2 = integrate(3*x*(x - 4), x) + C
assert expand(f2 - (x**3 - 6*x**2 + C)) == 0
I2 = integrate(f2, (x, -1, 5))
assert expand(I2 - (-96 + 6*C)) == 0
c2 = solve(I2, C)
assert c2 == [16]                                                  # C 하나로 정해짐
F2 = f2.subs(C, 16)
assert expand(integrate(F2, (x, -1, 5)) - 6*F2.subs(x, 2)) == 0    # 빠른 풀이: 구간 길이 × 중점값
crit = sorted(solve(diff(F2, x), x))
assert crit == [0, 4] and diff(F2, x, 2).subs(x, 0) < 0 and diff(F2, x, 2).subs(x, 4) > 0
v2 = F2.subs(x, 0)                                                 # 극댓값 (x=0)
assert v2 == 16 and F2.subs(x, 4) == -16
w2 = fI.subs(C, 2).subs(x, 4)                                      # 오답: 원문 I22의 답
assert w2 == 18
chk(2, v2, [w2])

# ===== 3번 =====
s3 = solve([integrate(x*g, (x, -3, 3)) - 54, integrate(g, (x, -3, 3)) - 54], [a, b], dict=True)
assert s3 == [{a: 3, b: 6}]                                        # 하나로 정해짐
assert expand(integrate(x*g, (x, -3, 3)) - 18*a) == 0 and expand(integrate(g, (x, -3, 3)) - (18 + 6*b)) == 0
v3 = g.subs(s3[0]).subs(x, 2)
assert v3 == 16
# 오답 경로: x^n 적분에서 1/(n+1)을 빠뜨린 잘못된 적분 (∫x^2 → x^3)
bad_ax = 2*a*3**3                                                  # ∫_{-3}^{3} a x^2 → a[x^3] = 54a
w3a = g.subs({a: solve(bad_ax - 54, a)[0], b: 6}).subs(x, 2)
assert w3a == 12
bad_b = 2*3**3 + 6*b                                               # ∫_{-3}^{3}(x^2+b) → [x^3+bx] = 54+6b
w3b = g.subs({a: 3, b: solve(bad_b - 54, b)[0]}).subs(x, 2)
assert w3b == 10
chk(3, v3, [w3a, w3b])

# ===== 4번 =====
f4 = x**3 + 6*x**2 + 9*x + 2
assert expand(diff(f4, x) - 3*(x + 1)*(x + 3)) == 0
M4_, m4_, cs4 = maxmin(f4, -2, 1)
assert cs4 == [-1] and (M4_, m4_) == (18, -2)                      # 정류점 -3은 구간 밖
v4 = M4_ - m4_
assert v4 == 20
# 전수: 구간 안 함숫값을 촘촘히 훑어 최댓값·최솟값 확인
grid = [f4.subs(x, Rational(k, 100)) for k in range(-200, 101)]
assert max(grid) == 18 and min(grid) == -2
w4 = f4.subs(x, 1) - f4.subs(x, -2)                                # 오답: 끝값만 비교
assert w4 == 18
chk(4, v4, [w4])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 1번: 계수 4 / 근 배치
A1b = area_x(x**3 - 3*x**2 + 2*x)[0]
print(f'ABLATION 1 최고차항 계수 4: 필요(1이면 넓이 {A1b} ≠ {A1})'); assert A1b != A1
A1c = area_x(4*x*(x - 1)*(x - 3))[0]
print(f'ABLATION 1 등간격 근(8x 계수): 필요(근 0, 1, 3이면 넓이 {A1c} ≠ {A1})'); assert A1c != A1
# 2번
c2b = [solve(integrate(f2, (x, lo, hi)), C)[0] for lo, hi in ((-2, 2), (0, 3))]
print(f'ABLATION 2 적분 구간 [-1, 5]: 필요([-2,2]·[0,3]이면 극댓값 {c2b} ≠ {v2})'); assert all(z != v2 for z in c2b)
print(f'ABLATION 2 정적분 조건: 필요(빼면 극댓값 = 상수 C로 정해지지 않음)')
fx = integrate(3*(x - 0)*(x - 3), x) + C
c2c = solve(integrate(fx, (x, -1, 5)), C)[0]
print(f'ABLATION 2 극값 위치 x=4: 필요(x=3이면 극댓값 {fx.subs(C, c2c).subs(x, 0)} ≠ {v2})'); assert fx.subs(C, c2c).subs(x, 0) != v2
# 3번
sb = solve([integrate(g, (x, -3, 3)) - 54], [a, b], dict=True)
print(f'ABLATION 3 ∫xf=54: 필요(빼면 a가 정해지지 않음 {sb})'); assert a not in sb[0]
sc = solve([integrate(x*g, (x, -3, 3)) - 54], [a, b], dict=True)
print(f'ABLATION 3 ∫f=54: 필요(빼면 b가 정해지지 않음 {sc})'); assert b not in sc[0]
# 4번
print('ABLATION 4 닫힌구간: 필요(빼면 삼차함수의 최댓값·최솟값이 없음)')
M4b, m4b, _ = maxmin(f4, -3, 1)
print(f'ABLATION 4 왼끝 -2: 장치([-3,1]이어도 M-m={M4b - m4b}, 왼끝값 f(-2)=0은 끝값만 비교하는 오답 18을 만드는 자리)'); assert M4b - m4b == v4
M4c, m4c, _ = maxmin(f4, -2, 2)
print(f'ABLATION 4 오른끝 1: 필요([-2,2]이면 M-m={M4c - m4c} ≠ {v4})'); assert M4c - m4c != v4
print(f'ABLATION 4 상수항 2: 장치(M-m은 상수항과 무관 — 원문 M4의 상수 1과 같은 자리)')
print('정답 위치:', [IT[k]['ans'] for k in sorted(IT)])
print('ALL OK')
