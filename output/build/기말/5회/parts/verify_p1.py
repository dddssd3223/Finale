# -*- coding: utf-8 -*-
# p1.py (5회 1–4번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지(분담표 정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차(오름차순) · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, sqrt
x, t, a, b, m, n = symbols('x t a b m n', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 1, 3: 1, 4: 2}                                   # 분담표 정답 ③ ① ⑤ ②
KEY = {1: ('J52', 'J52 분석집_변형 1'), 2: ('I21', 'I21 분석집_변형 1'), 3: ('I56', 'I56 분석집_변형 1'), 4: ('M23', '자체 (가장 가까운 M23)')}
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
    return nsimplify(re.sub(r'\\dfrac\{(\d+)\}\{(\d+)\}', r'\1/\2', str(c)))

def arith(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0, list(d)[0]

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    ok_ar, dd = arith(no)
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and ok_ar and (dd > 0 or no == 3)
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def area_line(f, g):
    """두 그래프로 둘러싸인 넓이(교점 2개)와 교점, 이등분선 x=k의 후보(교점 사이)"""
    r = sorted(set(real_roots(Poly(expand(f - g), x))))
    assert len(r) == 2
    A = sp.simplify(integrate(-(f - g) if (f - g).subs(x, (r[0] + r[1]) / 2) < 0 else (f - g), (x, r[0], r[1])))
    return A, r

def bisector(f, g):
    A, r = area_line(f, g)
    s = -(f - g) if (f - g).subs(x, (r[0] + r[1]) / 2) < 0 else (f - g)
    kk = symbols('kk', real=True)
    sols = [z for z in solve(integrate(s, (x, r[0], kk)) - A / 2, kk) if z.is_real and r[0] < z < r[1]]
    return A, r, sols

# ===== 원문 · 분석집 변형 풀이 =====
A0, r0, k0 = bisector(x**2 - 5*x, x)                               # J52: k=3 (①)
assert k0 == [3]
fJ = x**2 + 2*x - 8                                                # 분석집 J52 변형①: f(3)=7
AJ, rJ, kJ = bisector(fJ, 4*x)
assert AJ == 36 and kJ == [1] and fJ.subs(x, 3) == 7
f_ = m*x + n                                                       # I21: ∫1^3 3f+(3x-1)f'=0 → f(3)/f(1)=1/4 (①)
s0 = solve(integrate(3*f_ + (3*x - 1)*diff(f_, x), (x, 1, 3)), n)
assert [sp.simplify(f_.subs(n, z).subs(x, 3) / f_.subs(n, z).subs(x, 1)) for z in s0] == [Rational(1, 4)]
sI = solve(integrate(2*f_ + (3*x - 1)*diff(f_, x), (x, 1, 3)), n)  # 분석집 I21 변형①: 3/7
assert [sp.simplify(f_.subs(n, z).subs(x, 3) / f_.subs(n, z).subs(x, 1)) for z in sI] == [Rational(3, 7)]
assert solve(integrate(3*x**2 + 2*x, (x, -a, a)) - Rational(1, 4), a) == [Rational(1, 2)]   # I56: 50a=25
sS = solve(integrate(3*x**2 + 2*x - 7, (x, -a, a)) + 12, a)        # 분석집 I56 변형①: 곱 -6
assert sorted(sS) == [-3, 1, 2] and sp.prod(sS) == -6
d0 = sp.factor(t**3 - 5*t**2 - (-2*t**2 + 10*t))                   # M23: t=5, p-q=35
assert [z for z in solve(d0, t) if z > 0] == [5] and diff(t**3 - 5*t**2 + 2*t**2 - 10*t, t).subs(t, 5) == 35
print('원문·분석집 풀이 OK (J52=3, STUDY-J52=7, I21=1/4, STUDY-I21=3/7, I56=25, STUDY-I56=-6, M23=35)')

# ===== 1번 =====
g1 = x**2 + a*x
r1s = solve(g1 + 4*x, x)
assert sorted(r1s, key=str) == sorted([0, -a - 4], key=str)          # 교점 x=0, x=-(a+4)
s1 = solve(sp.Eq((0 + (-a - 4)) / 2, 2), a)                         # 이등분선 = 차의 축(두 교점의 중점)
assert s1 == [-8]
v1 = s1[0]
A1, rr1, k1 = bisector(g1.subs(a, v1), -4*x)                         # 실제 넓이 이등분선 다시 확인
assert rr1 == [0, 4] and k1 == [2] and A1 == Rational(32, 3)
for aa in range(-30, 31):                                           # 전수: 정수 a 가운데 x=2가 이등분선인 것은 -8 하나
    if aa == -4: continue                                           # a=-4이면 접해서 둘러싸인 부분 없음
    assert (bisector(g1.subs(a, aa), -4*x)[2] == [2]) == (aa == -8), aa
w1 = solve(sp.Eq(-a / 2, 2), a)[0]                                  # 오답: 곡선의 축을 이등분선으로
assert w1 == -4
chk(1, v1, [w1])

# ===== 2번 =====
L2 = integrate(2*f_ + (3*x - 3)*diff(f_, x), (x, 2, 4))
assert expand(L2 - (24*m + 4*n)) == 0
s2 = solve(L2, n)
assert s2 == [-6*m]                                                # f=m(x-6) (m≠0, f(2)=-4m≠0)
ratio = sp.simplify(f_.subs(n, s2[0]).subs(x, 4) / f_.subs(n, s2[0]).subs(x, 2))
assert ratio == Rational(1, 2)
# 곱의 미분 풀이 경로 확인: [(3x-3)f]_2^4 - ∫f = 9f(4)-3f(2) - (f(2)+f(4))
f4, f2 = f_.subs(x, 4), f_.subs(x, 2)
assert expand(L2 - (9*f4 - 3*f2 - (f2 + f4))) == 0
# 전수: f(2)=0이면 f(4)=0까지 (n=-2m과 n=-6m 동시 → m=0), 단서 f(2)≠0으로 비가 정해짐
assert solve([L2, f2], [m, n], dict=True) == [{m: 0, n: 0}]
v2 = ratio
w2_inv = 1 / ratio                                                 # 오답: 비를 거꾸로
assert w2_inv == 2
w2_drop = Rational(3, 9)                                           # 참고: 남는 ∫f를 빼먹으면 9f(4)=3f(2) → 1/3 (선지 밖)
assert cv(r'\dfrac{1}{3}') not in [cv(c) for c in IT[2]['choices']]
chk(2, v2, [w2_inv])

# ===== 3번 =====
I3 = integrate(3*x**2 + 4*x + 11, (x, -a, a))
assert expand(I3 - (2*a**3 + 22*a)) == 0
s3 = [z for z in solve(I3 - 60, a) if z.is_real]
assert s3 == [2]                                                    # 실근 하나 (a^2+2a+15>0)
assert expand(I3 - 60 - 2*(a - 2)*(a**2 + 2*a + 15)) == 0
v3 = s3[0]
w3_half = [z for z in solve(a**3 + 11*a - 60, a) if z.is_real]     # 오답: 2배를 빠뜨림
assert w3_half == [3]
chk(3, v3, w3_half)

# ===== 4번 =====
x1 = t**3 - 2*t**2 - 2*t; x2 = 3*t**2 - 8*t
dd4 = expand(x1 - x2)
assert sp.factor(dd4) == t*(t - 2)*(t - 3)
meet = sorted(z for z in solve(dd4, t) if z > 0)
assert meet == [2, 3]                                              # t>0에서 만나는 시각 정확히 두 개
v1_, v2_ = diff(x1, t), diff(x2, t)
p4, q4 = v1_.subs(t, meet[1]), v2_.subs(t, meet[1])
assert (p4, q4) == (13, 10)
v4 = p4 - q4
assert v4 == 3
w4_first = (v1_ - v2_).subs(t, meet[0])                            # 오답: 처음 만나는 순간
w4_p = p4                                                          # 오답: p만
assert (w4_first, w4_p) == (-2, 13)
assert arith(4)[1] == 5
chk(4, v4, [w4_first, w4_p])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 1번
k_alt = [solve(sp.Eq((-a - 4) / 2, kk), a)[0] for kk in (1, 2, 3)]
print(f'ABLATION 1 이등분선 x=2: 필요(빼면 a가 정해지지 않음, x=1, 2, 3이면 a={k_alt})'); assert len(set(k_alt)) == 3
s1b = solve(sp.Eq((0 + (4 - a)) / 2, 2), a)
print(f'ABLATION 1 직선 y=-4x: 필요(y=4x이면 a={s1b} ≠ {v1})'); assert s1b[0] != v1

# 2번
s2b = solve(integrate(3*f_ + (3*x - 3)*diff(f_, x), (x, 2, 4)), n)
rb = sp.simplify(f_.subs(n, s2b[0]).subs(x, 4) / f_.subs(n, s2b[0]).subs(x, 2))
print(f'ABLATION 2 계수 2: 필요(3이면 곱의 미분만 남아 비 {rb} ≠ {v2})'); assert rb != v2
s2c = solve(integrate(2*f_ + (3*x - 3)*diff(f_, x), (x, 1, 3)), n)
rc = sp.simplify(f_.subs(n, s2c[0]).subs(x, 3) / f_.subs(n, s2c[0]).subs(x, 1))
print(f'ABLATION 2 적분 구간 [2, 4]: 필요([1, 3]이면 f(3)/f(1)={rc}, 구간이 달라 묻는 비도 달라짐)'); assert rc != v2
q_ = symbols('q_', real=True)
g2 = m*x**2 + n*x + q_
L2q = integrate(2*g2 + (3*x - 3)*diff(g2, x), (x, 2, 4))
r_list = {sp.simplify((g2.subs(x, 4) / g2.subs(x, 2)).subs({n: nn, q_: solve(L2q.subs({m: 1, n: nn}), q_)[0], m: 1})) for nn in (0, 1, -3)}
print(f'ABLATION 2 일차함수: 필요(이차함수까지 허용하면 비 {sorted(r_list)}…로 정해지지 않음)'); assert len(r_list) >= 2
# 3번
s3b = [z for z in solve(integrate(3*x**2 + 4*x + 11, (x, -a, a)) - 30, a) if z.is_real]
print(f'ABLATION 3 우변 60: 필요(30이면 a≈{[round(float(z), 3) for z in s3b]} ≠ {v3})'); assert s3b[0] != v3
s3c = [z for z in solve(integrate(3*x**2 + 4*x, (x, -a, a)) - 60, a) if z.is_real]
print(f'ABLATION 3 상수항 11: 필요(빼면 2a^3=60, a={s3c} ≠ {v3})'); assert s3c[0] != v3
assert [z for z in solve(integrate(3*x**2 + 11, (x, -a, a)) - 60, a) if z.is_real] == s3
print(f'ABLATION 3 일차항 4x: 장치(빼도 답 그대로 — 원문 I56의 2x와 같은 자리, 대칭 구간에서 홀수 차수 항이 지워짐을 보는 판단)')

# 4번
print(f'ABLATION 4 두 번째로: 필요(빼면 만나는 순간이 t={meet} 둘이라 p-q가 {w4_first}, {v4}로 정해지지 않음)')
print(f'ABLATION 4 t>0: 필요(t=0도 넣으면 t=0이 처음, t=2가 두 번째 → p-q={w4_first} ≠ {v4})'); assert (v1_ - v2_).subs(t, 0) != v4
print('정답 위치:', [IT[k]['ans'] for k in sorted(IT)])
print('ALL OK')
