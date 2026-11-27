# -*- coding: utf-8 -*-
# p1.py (13회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성 · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, oo, limit, real_roots, Poly
x, t, a, k = symbols('x t a k', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 5, 3: 1, 4: 2}            # 분담표 ③ ① ⑤ ② 에서 2·3번 맞바꿈 → ③ ⑤ ① ②
KEY = {1: ('M17', 'M17 후보_순위 2'), 2: ('J56', 'J56 후보_순위 2'), 3: ('M43', 'M43 후보_순위 2'), 4: ('I2', '자체 (가장 가까운 I2)')}
STEP = {1: 2, 2: 1, 3: 1, 4: 2}           # 공차 1은 둘 이하
assert sum(1 for v in STEP.values() if v == 1) <= 2
assert sorted(IT) == [1, 2, 3, 4]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    assert '이러한' not in it['body'] and '이와 같은' not in it['body']
    for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'] + it['sol'] + it['fast'], re.S):
        assert '<' not in m and '>' not in m, m
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(s):
    return nsimplify(str(s))

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

def pos_root_count(poly):
    return len({r for r in real_roots(Poly(poly, x)) if r > 0})

# ===== 원문·뼈대 풀이 =====
X = -Rational(1, 3)*t**3 + 3*t**2 + k                                                  # M17 원문: 22
ta = solve(diff(X, t, 2), t); assert ta == [3]
assert solve(X.subs(t, 3) - 40, k) == [22]
XG = Rational(1, 2)*t**3 - 3*t**2 + k                                                   # GEN1-02-041: 40
assert solve(diff(XG, t, 2), t) == [2] and solve(XG.subs(t, 2) - 32, k) == [40]
v0 = t**2 - a*t                                                                         # J56 원문: 3
assert [r for r in solve(integrate(a*t - t**2, (t, 0, a)) - Rational(9, 2), a) if r.is_real and r > 0] == [3]
v0s = 2*t**2 - a*t                                                                      # 학교식_예상 1: 6
assert [r for r in solve(integrate(a*t - 2*t**2, (t, 0, a/2)) - 9, a) if r.is_real and r > 0] == [6]
assert sum(1 for kk in range(-50, 50) if pos_root_count(2*x**3 - 6*x**2 + kk) == 2) == 7      # M43 원문: 7
assert sum(1 for kk in range(-50, 50) if pos_root_count(x**3 - 3*x**2 + kk) == 2) == 3        # GEN1-02-088: 3
assert integrate(4*x**3 + 6*x, (x, 0, 1)) == 4                                          # I2 원문: 4
print('원문·뼈대 풀이 OK (M17=22, GEN1-02-041=40, J56=3, 학교식_예상1=6, M43=7, GEN1-02-088=3, I2=4)')

# ===== 1번 =====
x1 = -t**3 + 3*t**2 + k
v1 = diff(x1, t); a1 = diff(v1, t)
assert expand(v1 - (-3*t**2 + 6*t)) == 0 and expand(a1 - (-6*t + 6)) == 0
ta1 = [r for r in solve(a1, t) if r >= 0]
assert ta1 == [1]                                                                       # 가속도 0인 시각 유일
sol1 = solve(x1.subs(t, ta1[0]) - 15, k)
assert sol1 == [13]
val1 = sol1[0]
tv0 = [r for r in solve(v1, t) if r > 0]; assert tv0 == [2]
w1 = solve(x1.subs(t, tv0[0]) - 15, k)[0]                                              # 속도 0인 시각과 혼동
assert w1 == 11
chk(1, val1, [w1])
print('ABLATION 1 가속도 0 조건: 필요(빼면 어느 시각의 위치인지 정해지지 않아 k가 정해지지 않음)')
print('ABLATION 1 위치 15: 필요(값을 바꾸면 k가 바뀜)')
assert solve(x1.subs(t, 1) - 16, k) != [13]

# ===== 2번 =====
v2 = 3*t**2 - a*t
A = symbols('A', positive=True)
v2A = v2.subs(a, A)
tz = [r for r in solve(v2A, t) if r != 0]
assert tz == [A/3]                                                                      # 방향이 바뀌는 시각 a/3 (부호 - → +)
assert v2A.subs(t, A/6) < 0 and v2A.subs(t, A/2) > 0
D = integrate(-v2A, (t, 0, A/3))
assert sp.simplify(D - A**3/54) == 0
r2 = [r for r in solve(D - 4, A) if r.is_real and r > 0]
assert r2 == [6]
val2 = r2[0]
# 수치 확인: a=6이면 0..2 거리 4
assert integrate(-v2.subs(a, 6), (t, 0, 2)) == 4 and all(v2.subs({a: 6, t: Rational(i, 10)}) < 0 for i in range(1, 20))
w2 = [r for r in solve(integrate(v2A, (t, 0, A)) - 4, A) if r.is_real and r > 0]       # 원문처럼 전환 시각 t=a
assert w2 == [2]
chk(2, val2, [w2[0]])
print('ABLATION 2 a>0: 필요(빼면 a<0일 때 방향이 바뀌는 시각이 음수가 되어 조건이 성립하지 않으나, a의 범위가 원문 단서라 그대로 둠 — 정답 유일성은 a>0에서 확인)')
assert [r for r in solve(D - 5, A) if r.is_real and r > 0] != [6]
print('ABLATION 2 거리 4: 필요(값을 바꾸면 a가 바뀜)')

# ===== 3번 =====
h3 = x**3 - 6*x**2
assert expand(diff(h3, x) - 3*x*(x - 4)) == 0
assert h3.subs(x, 0) == 0 and h3.subs(x, 4) == -32
ks = [kk for kk in range(-200, 200) if pos_root_count(h3 + kk) == 2]                   # 전수: 정수 k
assert ks == list(range(1, 32))
val3 = len(ks)
assert val3 == 31
assert pos_root_count(h3 + 0) == 1 and pos_root_count(h3 + 32) == 1                    # 경계 두 개는 양근 1개
w3a = val3 + 1                                                                          # 경계 하나 포함
w3b = val3 + 2                                                                          # 경계 둘 포함
chk(3, val3, [w3a, w3b])
assert sum(1 for kk in range(-200, 200) if len(set(real_roots(Poly(h3 + kk, x)))) == 2) == 2
print('ABLATION 3 양의: 필요(빼면 서로 다른 실근 2개인 정수 k는 0, 32의 2개)')
assert sum(1 for kk in range(-200, 200) if pos_root_count(h3 + kk) == 1) != val3
print('ABLATION 3 개수 2: 필요(1로 바꾸면 개수가 바뀜)')

# ===== 4번 =====
fp = 3*x**2 - 2*x + 1
F = integrate(fp, x)
assert expand(F - (x**3 - x**2 + x)) == 0
val4 = F.subs(x, 3) - F.subs(x, 1)
assert val4 == integrate(fp, (x, 1, 3)) == 20
w4 = integrate(3*x**2 - 2*x, (x, 1, 3))                                                 # 상수항 적분 누락
assert w4 == 18
chk(4, val4, [w4])
assert integrate(fp, (x, 0, 3)) != val4
print('ABLATION 4 아래끝 1: 필요(0으로 바꾸면 21)')
print('ALL OK')
