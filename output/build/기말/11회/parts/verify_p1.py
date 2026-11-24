# -*- coding: utf-8 -*-
# p1.py (11회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성 · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots
x, t, a, c = symbols('x t a c', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 5, 3: 1, 4: 4}            # 분담표 ③ ⑤ ① ④
KEY = {1: ('M46', 'M46 후보_순위 2'), 2: ('I29', 'I29 후보_순위 2'), 3: ('I18', 'I18 후보_순위 2'), 4: ('I27', '자체 (가장 가까운 I27)')}
STEP = {1: 1, 2: 1, 3: 1, 4: 1}
assert sorted(IT) == [1, 2, 3, 4]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    assert '이러한' not in it['body'] and '이와 같은' not in it['body']
    for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'] + it['sol'], re.S):
        assert '<' not in m and '>' not in m, m
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(s):
    s = str(s)
    m = re.fullmatch(r'(-?)\\dfrac\{(\d+)\}\{(\d+)\}', s)
    return Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1) if m else nsimplify(s)

def chk(no, val, wrongs):
    ch = [cv(s) for s in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    d = {ch[i + 1] - ch[i] for i in range(4)}
    dd = list(d)[0]
    body_nums = {nsimplify(n) for n in re.findall(r'(?<![\w^])\d+', IT[no]['body'])}
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and len(set(ch)) == 5 and len(d) == 1
            and dd == STEP[no] and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws)
            and nsimplify(val) not in body_nums)
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

# ===== 원문·뼈대 풀이 =====
xM = t**3 - 5*t**2 + 6*t                                                                # M46 원문: 8
assert diff(xM, t, 2).subs(t, 3) == 8
xG = 2*t**3 - 4*t**2 + 3*t + 1                                                          # GEN1-02-095: 16
assert diff(xG, t, 2).subs(t, 2) == 16
# I29 원문: 기함수 f, ∫_0^1 xf=3 → ∫_{-1}^1 (x+2)^2 f = 8·3 = 24 (예: f=9x, f=15x^3 둘 다)
for fo in (9*x, 15*x**3):
    assert integrate(x*fo, (x, 0, 1)) == 3 and integrate((x + 2)**2*fo, (x, -1, 1)) == 24
# LIVE2-03-109: f 우, g 기, ∫_{-2}^2 (x-3)h' = 12 → h(2) = -2 (예: h = c·x)
hL = c*x
assert solve(integrate((x - 3)*diff(hL, x), (x, -2, 2)) - 12, c) == [-1] and hL.subs({c: -1, x: 2}) == -2
assert integrate(x**2 - x, (x, 0, 1)) + integrate(x + 1, (x, 1, 0)) + integrate(x**2 - 2*x - 1, (x, 1, 3)) == -3   # I18 원문
rI = solve(integrate(x**5 - 2*x**3 + 3*x**2 - 7, (x, -a, a)) + 12, a)                  # I27 원문: 양수 1, 2 → 3
assert sorted(rI) == [-3, 1, 2] and sum(r for r in rI if r > 0) == 3
print('원문·뼈대 풀이 OK (M46=8, GEN1-02-095=16, I29=24, LIVE2-03-109=-2, I18=-3, I27=3)')

# ===== 1번 =====
x1 = t**3 - 3*t**2 + 7*t
v1 = diff(x1, t); a1 = diff(v1, t)
val1 = a1.subs(t, 2)
assert val1 == 6
w1 = v1.subs(t, 2)                                                                      # 한 번만 미분(속도)
assert w1 == 7 and x1.subs(t, 2) not in (6,)                                           # 위치 x(2)=10도 정답과 다름
assert val1 not in (8, 16)                                                              # 원문·GEN 답과 다름
chk(1, val1, [w1])
assert all(a1.subs(t, T) != val1 for T in (1, 3, 4))
print('ABLATION 1 시각 t=2: 필요(시각을 바꾸면 가속도가 바뀜)')

# ===== 2번 =====
f2 = 2*x**3 - x; g2 = x**2 + 1
assert expand(f2.subs(x, -x) + f2) == 0 and expand(g2.subs(x, -x) - g2) == 0           # 기함수·우함수(LIVE 설정 그대로)
h2 = expand(f2*g2)
val2 = integrate((x + 2)*diff(h2, x), (x, -1, 1))
assert val2 == 8 and val2 == 4*h2.subs(x, 1)
assert integrate(x*diff(h2, x), (x, -1, 1)) == 0                                        # xh'은 기함수
w2b = integrate(20*x**4 + 6*x**2 - 2, (x, 0, 1))                                       # 짝수차항만 남긴 뒤 2배 누락
w2c = 2*(h2.subs(x, 1) - 0)                                                             # h(-1)을 0으로
assert w2b == 4 and w2c == 4
chk(2, val2, [w2b])
for cc in (1, 3, -2):
    assert integrate((x + cc)*diff(h2, x), (x, -1, 1)) != val2
print('ABLATION 2 가중 (x+2): 필요(상수를 바꾸면 값이 바뀜)')
assert integrate((x + 2)*diff(h2, x), (x, 0, 1)) != val2 and integrate((x + 2)*diff(h2, x), (x, -2, 2)) != val2
print('ABLATION 2 구간 [-1,1]: 필요(구간을 바꾸면 값이 바뀜)')
assert integrate((x + 2)*diff(f2, x), (x, -1, 1)) != val2 and integrate((x + 2)*diff(expand(f2*(x**2 + 2)), x), (x, -1, 1)) != val2
print('ABLATION 2 g(x)=x^2+1: 필요(g를 빼거나 바꾸면 값이 바뀜)')

# ===== 3번 =====
p3, q3, d3 = x**2 + x, 3*x - 2, x**2 - 2*x + 2
assert expand(p3 - q3 - d3) == 0                                                        # 앞의 두 식의 차 = 셋째 식(원문 설계 관계)
I1, I2, I3 = integrate(p3, (x, 0, 2)), integrate(q3, (x, 2, 0)), integrate(d3, (x, 2, 3))
val3 = I1 + I2 + I3
assert (I1, I2, I3) == (Rational(14, 3), -2, Rational(10, 3)) and val3 == 6 == integrate(d3, (x, 0, 3))
w3 = I1 - I2 + I3                                                                       # 둘째 적분 방향을 바꾸지 않음
assert w3 == 10
assert val3 != -3
chk(3, val3, [w3])
assert I1 + I3 != val3
print('ABLATION 3 둘째 적분: 필요(빼면 8)')
assert integrate(p3, (x, 0, 2)) + integrate(q3, (x, 2, 0)) != val3
print('ABLATION 3 셋째 적분: 필요(빼면 8/3)')

# ===== 4번 =====
F4 = integrate(4*x**3 + 3*x**2 - 2*x - 21, (x, -a, a))
assert expand(F4 - (2*a**3 - 42*a)) == 0
r4 = solve(F4 + 40, a)
assert sorted(r4) == [-5, 1, 4]
assert expand(a**3 - 21*a + 20 - (a - 1)*(a - 4)*(a + 5)) == 0
val4 = sum(r for r in r4 if r > 0)
assert val4 == 5
w4 = 3                                                                                  # 원문 I27 답(1+2)
assert w4 == sum(r for r in rI if r > 0)
assert sum(r4) == 0 and 0 not in [cv(s) for s in IT[4]['choices']]                     # 음수 근까지 더한 0은 선지 밖
chk(4, val4, [w4])
print('ABLATION 4 양수 조건: 필요(빼면 모든 실수 a의 합 0)')
for rhs in (-36, -44):
    assert sum(r for r in solve(F4 - rhs, a) if r.is_real and r > 0) != val4
print('ABLATION 4 우변 -40: 필요(바꾸면 근이 바뀜)')
print('ALL OK')
