# -*- coding: utf-8 -*-
# p1.py (8회 1–4번) 검증: 원문 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, factor
x, a, b, c, k, t = symbols('x a b c k t', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 4, 2: 5, 3: 2, 4: 3}            # 분담표 ③ ⑤ ② ④ → 1·4번 맞바꿈(1번 ④, 4번 ③), 1–4번 정답 분포는 그대로
KEY = {1: ('J12', 'J12 분석집_변형 1'), 2: ('I51', 'I51 후보_순위 2'), 3: ('I3', 'I3 후보_순위 2'), 4: ('M44', '자체 (가장 가까운 M44)')}
STEP = {1: 3, 2: Rational(1, 2), 3: 1, 4: 1}
assert sorted(IT) == [1, 2, 3, 4]
assert sorted(WANT.values()) == [2, 3, 4, 5]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    assert '이러한' not in it['body'] and '이와 같은' not in it['body']
    for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'] + it['sol'], re.S):
        assert '<' not in m and '>' not in m, m                 # 수식 안 맨 부등호 없음
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(s):
    s = str(s)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', s)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(s)

def chk(no, val, wrongs):
    ch = [cv(s) for s in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    d = {ch[i + 1] - ch[i] for i in range(4)}
    dd = list(d)[0]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and len(set(ch)) == 5 and len(d) == 1
            and dd == STEP[no] and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def area_tangent(f, x0):
    """곡선 y=f와 x=x0에서의 접선으로 둘러싸인 넓이(교점 전수)"""
    l = diff(f, x).subs(x, x0)*(x - x0) + f.subs(x, x0)
    g = expand(f - l)
    rs = sorted(set(real_roots(Poly(g, x))))
    return sum(abs(integrate(g, (x, rs[i], rs[i + 1]))) for i in range(len(rs) - 1)), g, rs

# ===== 원문·뼈대 풀이 =====
A0, g0, _ = area_tangent(x**3 - 2*x**2 + k, 0)                                     # J12: 4/3 ③
assert sp.simplify(A0 - Rational(4, 3)) == 0
fS = x**3 + a*x**2 + b*x + c                                                         # 분석집 변형①: 계수 1, 평행 0·2 → 27/4
aS = solve(diff(fS, x).subs(x, 0) - diff(fS, x).subs(x, 2), a)
assert aS == [-3]
AS, gS, _ = area_tangent(fS.subs(a, -3).subs({b: 5, c: -7}), 0)
assert AS == Rational(27, 4)
sI = [r for r in solve(integrate(3*x**2 - 4, (x, 0, a)), a) if r > 0]                # I51: 2 ①
assert sI == [2]
P, Q, R = symbols('P Q R')                                                           # I3: 근의 합 2 ①
fI = P*x**2 + Q*x + R
sol0 = solve(sp.Poly(expand(fI - diff(fI, x) - (6*x**2 - 14*x)), x).coeffs(), [P, Q, R], dict=True)
fI0 = fI.subs(sol0[0])
assert expand(fI0 - (6*x**2 - 2*x - 2)) == 0
rI = solve(fI0 - 5*x**2, x)
assert len(rI) == 2 and all(r.is_real for r in rI) and sp.simplify(sum(rI)) == 2
gM = x**3 - 3*x**2 + 1                                                               # M44: -(k+1)... k=-x^3+3x^2-1, 극값 -1, 3 → 양수 3 ③
hM = -x**3 + 3*x**2 - 1
cM = solve(diff(hM, x), x)
kM = sorted(hM.subs(x, r) for r in cM)
assert kM == [-1, 3]
for kk in kM:
    assert len(set(real_roots(Poly(expand(2*x**2 - 1 - (x**3 - x**2 + kk)), x)))) == 2
print('원문·뼈대 풀이 OK (J12=4/3, STUDY-J12-변형①=27/4, I51=2, I3=2, M44=3)')

# ===== 1번 =====
f1 = 4*x**3 + a*x**2 + b*x + c
a1 = solve(diff(f1, x).subs(x, 0) - diff(f1, x).subs(x, 2), a)
assert a1 == [-12]                                                                   # a 하나로 정해짐, b·c는 자유
F1 = f1.subs(a, -12)
l1 = diff(F1, x).subs(x, 0)*x + F1.subs(x, 0)
g1 = expand(F1 - l1)
assert g1 == 4*x**3 - 12*x**2 and factor(g1) == 4*x**2*(x - 3)                       # b, c와 무관
v1 = integrate(-g1, (x, 0, 3))
assert v1 == 27
import random
for _ in range(20):                                                                  # b, c를 바꿔도 넓이 같음(전수 대신 임의 표본 + 기호 확인)
    bb, cc = random.randint(-9, 9), random.randint(-9, 9)
    assert area_tangent(F1.subs({b: bb, c: cc}), 0)[0] == 27
w1 = Rational(4, 6)*3**3                                                             # 이차함수 공식 오적용
assert w1 == 18
assert v1 != AS                                                                      # 분석집 변형 답(27/4)과 다름
chk(1, v1, [w1])
# 빼 보기
A_free = {area_tangent(4*x**3 + aa*x**2 + 2*x + 1, 0)[0] for aa in (-4, -8, -12)}
assert len(A_free) == 3
print('ABLATION 1 두 접선 평행: 필요(없으면 이차항 계수 a가 정해지지 않아 넓이가 a에 따라 바뀜)')
assert area_tangent(x**3 - 3*x**2 + 2*x + 1, 0)[0] == Rational(27, 4)
print('ABLATION 1 최고차항의 계수 4: 필요(계수 1이면 27/4로 답이 바뀜)')

# ===== 2번 =====
G2 = integrate(3*x**2 - 4*x - 8, (x, 0, a))
assert factor(G2) == a*(a - 4)*(a + 2)
r2 = solve(G2, a)
assert sorted(r2) == [-2, 0, 4]
pos = [r for r in r2 if r > 0]
assert pos == [4]                                                                    # 양수 해 하나
chk(2, pos[0], [2])                                                                  # 오답: 원문 답 2 = |음수 근|
assert -min(r2) == 2 and sI == [2]
print('ABLATION 2 양수: 필요(없으면 a=0, -2, 4로 정해지지 않음)')

# ===== 3번 =====
# f의 차수를 4까지 열어 전수: f - f' = 6x^2 - 18x를 만족시키는 다항식은 하나뿐
cs = symbols('d0:5')
fg = sum(cs[i]*x**i for i in range(5))
s3 = solve(Poly(expand(fg - diff(fg, x) - (6*x**2 - 18*x)), x).all_coeffs(), cs, dict=True)
assert len(s3) == 1
f3 = expand(fg.subs(s3[0]))
assert f3 == 6*x**2 - 6*x - 6
F3 = f3 + 2*x**3 - 9*x**2
assert expand(diff(F3, x) - f3) == 0                                                 # F는 실제로 f의 부정적분
eq3 = expand(f3 - 4*x**2)
assert eq3 == 2*x**2 - 6*x - 6 and sp.discriminant(eq3, x) > 0
r3 = solve(eq3, x)
assert len(r3) == 2
v3 = sp.simplify(sum(r3))
assert v3 == 3
# 오답 6: f'을 ax+b로(2 빠뜨림) → b=a-18
aa = 6; bb = aa - 18
w3 = sp.simplify(sum(solve(aa*x**2 + bb*x + bb - 4*x**2, x)))
assert w3 == 6
chk(3, v3, [2, w3])
fo = solve(Poly(expand(fg - diff(fg, x) - (6*x**2 - 14*x)), x).all_coeffs(), cs, dict=True)
assert sp.simplify(sum(solve(expand(fg.subs(fo[0])) - 4*x**2, x))) != 3
print('ABLATION 3 항등식 계수 -9: 필요(원문 -7이면 f=6x^2-2x-2, 근의 합이 1로 바뀜)')

# ===== 4번 =====
d4 = expand((x**3 + 2*x**2 + 1) - (2*x**2 + 3*x + k))
assert d4 == x**3 - 3*x + 1 - k
g4 = x**3 - 3*x + 1
ks = []
for kk in [Rational(n, 4) for n in range(-40, 41)] + [g4.subs(x, r) for r in solve(diff(g4, x), x)]:   # 전수: 교점 2개인 k
    if len(set(real_roots(Poly(d4.subs(k, kk), x)))) == 2:
        ks.append(kk)
ks = sorted(set(ks))
assert ks == [-1, 3]
v4 = [q for q in ks if q > 0]
assert v4 == [3]
w4a = sorted((-g4).subs(x, r) for r in solve(diff(g4, x), x))                       # 부호 실수: k=-g
w4b = sorted((g4 - 1).subs(x, r) for r in solve(diff(g4, x), x))                    # 상수항 1 누락
assert w4a == [-3, 1] and w4b == [-2, 2]
chk(4, v4[0], [1, 2])
print('ABLATION 4 양수: 필요(없으면 k=-1도 답이 되어 하나로 정해지지 않음)')
print('ALL OK')
