# -*- coding: utf-8 -*-
# p1.py (12회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성 · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, nsimplify, oo, limit
x, t, a, k, C = symbols('x t a k C', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 5, 2: 3, 3: 2, 4: 1}            # 분담표 ⑤ ③ ② ①
KEY = {1: ('M41', 'M41 후보_순위 2'), 2: ('I51', 'I51 후보_순위 3'), 3: ('M11', 'M11 후보_순위 2'), 4: ('I50', '자체 (가장 가까운 I50)')}
STEP = {1: 1, 2: 1, 3: 1, 4: 2}
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
    return nsimplify(str(s))

def chk(no, val, wrongs):
    ch = [cv(s) for s in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    d = {ch[i + 1] - ch[i] for i in range(4)}
    dd = list(d)[0]
    body_nums = {nsimplify(n) for n in re.findall(r'-?(?<![\w^])\d+', IT[no]['body'])}
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and len(set(ch)) == 5 and len(d) == 1
            and dd == STEP[no] and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws)
            and nsimplify(val) not in body_nums)
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def minmax(f, lo, hi):
    """닫힌구간에서 다항함수의 최댓값·최솟값(끝점 + 구간 안 임계점 전수)"""
    cps = [r for r in solve(diff(f, x), x) if r.is_real and lo <= r <= hi]
    vals = [f.subs(x, p) for p in [lo, hi] + cps]
    return sp.Max(*vals), sp.Min(*vals)

# ===== 원문·뼈대 풀이 =====
fM = x**3 - 3*x**2 + a                                                                  # M41 원문: 4
Mx, mn = minmax(fM, 1, 4)
assert solve(Mx + mn - 20, a) == [4]
fL = -2*x**3 + 6*x**2 + a                                                               # LIVE1-02-136: 4
Mx, mn = minmax(fL, -1, 2)
assert solve(Mx + mn - 16, a) == [4]
assert [r for r in solve(integrate(3*x**2 - 4, (x, 0, a)), a) if r > 0] == [2]          # I51 원문: 2
assert [r for r in solve(integrate(2*x - 7, (x, 0, 2)) + integrate(2*t - 7, (t, 2, a)) - 18, a) if r > 0] == [9]   # LIVE2-03-175: 9
h0 = 2*x**3 - 6*x**2 + 14                                                               # M11 원문: 정수 a < 최솟값 6 → 5
_, mn0 = minmax(h0, 0, 50)
assert mn0 == 6 and max(n for n in range(-20, 20) if n < mn0) == 5
hL = x**3 + 3*x**2 - 24*x + 25                                                          # LIVE1-02-030: -3
assert minmax(hL, 0, 50)[1] == -3
F0 = integrate(4*x**3 - 2*x, x) + C                                                     # I50 원문: 16
assert F0.subs({C: solve(F0.subs(x, 0) - 4, C)[0], x: 2}) == 16
print('원문·뼈대 풀이 OK (M41=4, LIVE1-02-136=4, I51=2, LIVE2-03-175=9, M11=5, LIVE1-02-030=-3, I50=16)')

# ===== 1번 =====
f1 = x**3 - 6*x**2 + 9*x + a
assert expand(diff(f1, x) - 3*(x - 1)*(x - 3)) == 0
vals1 = {p: f1.subs(x, p) for p in (0, 1, 3, 4)}
assert vals1[1] == vals1[4] == a + 4 and vals1[0] == vals1[3] == a                      # 숨은 동률
M1, m1 = minmax(f1, 0, 4)
sol1 = solve(M1 + m1 - 14, a)
assert sol1 == [5]
val1 = sol1[0]
w1a = solve(2*(a + 4) + a - 14, a)[0]                                                    # M을 두 번 더함
w1b = 4                                                                                  # 원문 답
assert w1a == 2
chk(1, val1, [w1a, w1b])
assert solve(sum(minmax(f1, 1, 4)) - 14, a) == [5]
print('ABLATION 1 구간 [0,4]: [1,4]에서도 최솟값 a(x=3)·최댓값 a+4라 답 그대로 — 구간 끝 0은 동률을 숨기는 자리(LIVE1-02-136 장치), 구간을 [0,5]로 늘리면 바뀜')
assert solve(sum(minmax(f1, 0, 5)) - 14, a) != [5]
print('ABLATION 1 M+m=14: 필요(우변을 바꾸면 a가 바뀜)')

# ===== 2번 =====
G2 = integrate(2*x - 5, (x, 0, 1)) + integrate(2*t - 5, (t, 1, a))
assert expand(G2 - (a**2 - 5*a)) == 0
r2 = solve(G2 - 14, a)
assert sorted(r2) == [-2, 7]
val2 = [r for r in r2 if r > 0]
assert len(val2) == 1
val2 = val2[0]
w2 = [r for r in solve(4 + integrate(2*t - 5, (t, 1, a)) - 14, a) if r > 0][0]           # 첫째 적분 위·아래끝을 거꾸로 대입(+4)
assert w2 == 6
chk(2, val2, [w2])
print('ABLATION 2 양수 조건: 필요(빼면 a=-2도 해)')
assert [r for r in solve(integrate(2*t - 5, (t, 1, a)) - 14, a) if r > 0] != [7]
print('ABLATION 2 첫째 적분: 필요(빼면 a가 정수가 아님)')

# ===== 3번 =====
h3 = 2*x**3 - 3*x**2 - 12*x + 9
assert expand(diff(h3, x) - 6*(x - 2)*(x + 1)) == 0
assert limit(h3, x, oo) == oo
_, mn3 = minmax(h3, 0, 100)                                                              # x≥0: 끝점 0, 임계점 2, 이후 증가
assert mn3 == h3.subs(x, 2) == -11 and h3.subs(x, 0) == 9
val3 = mn3
assert all(h3.subs(x, Rational(i, 10)) >= val3 for i in range(0, 400))                 # k=-11이면 항상 성립
assert h3.subs(x, 2) < val3 + Rational(1, 100)                                          # k>-11이면 x=2에서 깨짐
w3 = val3 - 1                                                                            # 원문식 '엄격·정수'로 한 칸 내림
chk(3, val3, [w3])
assert limit(h3, x, -oo) == -oo
print('ABLATION 3 x≥0: 필요(빼면 아래로 유계가 아니라 k의 최댓값 없음)')
_, mn3b = minmax(h3, -1, 100)
assert mn3b == val3
print('ABLATION 3 x≥0 끝점 위치: 정의역을 x≥-1로 넓혀도 최솟값 -11 그대로 — 구간 밖 극대 x=-1은 버리는 자리(LIVE1-02-030 장치), x≥3으로 옮기면 바뀜')
assert minmax(h3, 3, 100)[1] != val3

# ===== 4번 =====
f4 = -8*x**3 + 24*x**2 - 16*x
assert expand(f4 + 8*x*(x - 1)*(x - 2)) == 0
F4 = integrate(f4, x) + C
assert expand(F4 - (-2*(x**2)*(x - 2)**2 + C)) == 0
assert limit(F4, x, oo) == -oo and limit(F4, x, -oo) == -oo                              # 최댓값 존재
cps = solve(f4, x)
assert sorted(cps) == [0, 1, 2]
mx4 = sp.Max(*[F4.subs(x, p) for p in cps])
assert sp.simplify(mx4 - C) == 0                                                         # 최댓값 C (x=0, 2), 극솟값 C-2 (x=1)
Cv = solve(C - 3, C)[0]
val4 = F4.subs({C: Cv, x: 3})
assert val4 == -15
w4 = F4.subs({C: solve(F4.subs(x, 1) - 3, C)[0], x: 3})                                 # 극솟값을 최댓값으로
assert w4 == -13
chk(4, val4, [w4])
print('ABLATION 4 최댓값 3: 필요(값을 바꾸면 C가 바뀜, 없으면 C를 정할 수 없음)')
print('ABLATION 4 묻는 점 x=3: 필요(x=0,2를 물으면 3 그대로 본문 수, x=1이면 극솟값 1)')
assert F4.subs({C: Cv, x: 0}) == 3 and F4.subs({C: Cv, x: 1}) == 1
print('ALL OK')
