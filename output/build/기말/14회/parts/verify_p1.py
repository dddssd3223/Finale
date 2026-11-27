# -*- coding: utf-8 -*-
# p1.py (14회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성 · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify
x, t, a = symbols('x t a', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 2, 2: 4, 3: 1, 4: 3}            # 분담표 ② ④ ① ③ 그대로
KEY = {1: ('M53', 'M53 후보_순위 2'), 2: ('I10', 'I10 후보_순위 2'), 3: ('J49', 'J49 후보_순위 2'), 4: ('I1', '자체 (가장 가까운 I1)')}
STEP = {2: 1, 3: 2, 4: 2}                 # 1번은 보기형. 공차 1은 둘 이하
assert sum(1 for v in STEP.values() if v == 1) <= 2
assert sorted(IT) == [1, 2, 3, 4]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    assert ('bogi' in it) == (no == 1)
    txt = it['body'] + ''.join(v for _, v in it.get('bogi', []))
    assert '이러한' not in txt and '이와 같은' not in txt
    for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', txt + it['sol'] + it['fast'], re.S):
        assert '<' not in m and '>' not in m, m
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    assert len(set(it['choices'])) == 5

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

def bogi_answer(truth):          # truth: {'ㄱ': bool, ...} → 'T:ㄱ, ㄴ' 꼴
    return 'T:' + ', '.join(k for k in 'ㄱㄴㄷ' if truth[k])

# ===== 원문·뼈대 풀이 =====
X0 = t**3 - t**2 - t + 1                                                               # M53 원문: ㄴ, ㄷ
V0 = diff(X0, t); A0 = diff(V0, t)
tch0 = [r for r in solve(V0, t) if r > 0]
assert tch0 == [1]
assert bogi_answer({'ㄱ': X0.subs(t, 1) == 1, 'ㄴ': V0.subs(t, 1) == 0, 'ㄷ': A0.subs(t, tch0[0]) == 4}) == 'T:ㄴ, ㄷ'
XS = t**3 - 4*t**2 + 4*t                                                               # 학교식_예상 1: ㄱ, ㄴ
VS = diff(XS, t); AS = diff(VS, t)
assert sorted(r for r in solve(VS, t) if r > 0) == [Rational(2, 3), 2] and AS.subs(t, Rational(2, 3)) == -4
F10 = (x - 3)**3                                                                        # I10 원문: f(3)-f(2) = a, a=1
a10 = solve(F10.subs(x, 2) + a, a)[0]; assert a10 == 1
assert (F10 + a10).subs(x, 3) == 1
assert (F10 + a).subs(x, 4) - (F10 + a).subs(x, 1) == 9                                # 학교식_예상 1: 9
assert integrate(2*x**2 - x**3, (x, 0, 2)) == Rational(4, 3)                           # J49 원문: 4/3
assert integrate(-2*x**3 + 4*x**2, (x, 0, 2)) == Rational(8, 3)                        # 학교식_예상 2: 8/3
c = symbols('c')
c1 = solve(c - (2 - c + 4), c)[0]; assert c1 == 3                                       # I1 원문: f(1)=3, f(2)=8
assert (2*x**3 - c1*x**2 + 4).subs(x, 2) == 8
print('원문·뼈대 풀이 OK (M53=ㄴ,ㄷ, 학교식1=ㄱ,ㄴ, I10=1, 학교식1=9, J49=4/3, 학교식2=8/3, I1=8)')

# ===== 1번 =====
X1 = t**3 - 6*t**2 + 9*t
V1 = diff(X1, t); A1 = diff(V1, t)
assert expand(V1 - 3*(t - 1)*(t - 3)) == 0 and expand(A1 - (6*t - 12)) == 0
tch = sorted(r for r in solve(V1, t) if r > 0)
assert tch == [1, 3]
for r in tch:                                                                          # 실제로 부호가 바뀜
    assert V1.subs(t, r - Rational(1, 10)) * V1.subs(t, r + Rational(1, 10)) < 0
T1 = {'ㄱ': bool(X1.subs(t, 3) == 0), 'ㄴ': bool(V1.subs(t, 3) == 0), 'ㄷ': bool(A1.subs(t, tch[0]) == 6)}
assert T1 == {'ㄱ': True, 'ㄴ': True, 'ㄷ': False}
ans1 = bogi_answer(T1)
assert IT[1]['choices'].index(ans1) + 1 == IT[1]['ans'] == WANT[1]
assert A1.subs(t, tch[0]) == -6
Tw = {**T1, 'ㄷ': bool(A1.subs(t, tch[1]) == 6)}                                              # 두 번째 전환 시각 t=3의 가속도로 판정
assert Tw['ㄷ'] is True
w1 = bogi_answer(Tw)
assert w1 == 'T:ㄱ, ㄴ, ㄷ' and IT[1]['wrongs'] == [w1] and w1 != ans1
print(f'1번: 계산 {ans1} (위치 {IT[1]["ans"]}), 오답 {w1} OK')
print('ABLATION 1 ㄷ의 처음으로: 필요(빼면 방향이 바뀌는 시각이 t=1, 3 둘이라 ㄷ이 정해지지 않음)')
assert bogi_answer({**T1, 'ㄷ': bool(A1.subs(t, tch[0]) == -6)}) != ans1
print('ABLATION 1 ㄷ의 가속도 값 6: 필요(-6이면 ㄷ 참으로 답이 바뀜)')

# ===== 2번 =====
fd = (x - 2)**3 + a                                                                    # f(x)-f(0)
a2 = solve(fd.subs(x, 0), a)[0]; assert a2 == 8                                        # x=0 대입: a=8
val2 = fd.subs(x, 4) - fd.subs(x, 1)
assert sp.simplify(val2) == 9 and not val2.has(a)                                      # a와 무관하게 하나로 정해짐
# 실제 다항함수로 확인: f(x) = (x-2)^3 + 8 + C
C = symbols('C')
fx = (x - 2)**3 + a2 + C
assert expand(integrate(diff(fx, x).subs(x, t), (t, 0, x)) - ((x - 2)**3 + a2)) == 0
assert expand(fx.subs(x, 4) - fx.subs(x, 1)) == 9
w2 = (4 - 2)**3 - 1                                                                     # (1-2)^3을 1로
assert w2 == 7
chk(2, val2, [w2])
print('ABLATION 2 아래끝 0: 답에 영향 없음(아래끝은 a만 바꿈) — 원문 꼴 유지, 묻는 두 점이 아래끝이 아님')
assert sp.simplify(fd.subs(x, 4) - fd.subs(x, 2)) != 9
print('ABLATION 2 묻는 점 1: 필요(2로 바꾸면 8)')

# ===== 3번 =====
cur = -3*x**3 + 6*x**2 + 1
dif = cur - 1
assert expand(dif - (-3*x**2*(x - 2))) == 0
roots = sorted(set(solve(dif, x)))
assert roots == [0, 2]
assert all(dif.subs(x, Rational(i, 10)) >= 0 for i in range(0, 21))                   # 0..2에서 곡선이 위
val3 = integrate(dif, (x, 0, 2))
assert val3 == 4 and sp.N(sp.Integral(sp.Abs(dif), (x, 0, 2))) - 4 < 1e-9
w3 = integrate(cur, (x, 0, 2))                                                          # 직선 y=1을 빼지 않음
assert w3 == 6
chk(3, val3, [w3])
print('ABLATION 3 직선 y=1: 필요(x축으로 바꾸면 곡선과 x축 교점이 무리수, 답이 바뀜)')
assert integrate(-x**2*(x - 2), (x, 0, 2)) != val3
print('ABLATION 3 계수 -3: 필요(1로 두면 4/3)')

# ===== 4번 =====
fp = 6*x**2 - 4*x + 3
Cc = symbols('Cc')
F4 = integrate(fp, x) + Cc
Cv = solve(F4.subs(x, 0) - 2, Cc); assert Cv == [2]
F4 = F4.subs(Cc, 2)
assert expand(F4 - (2*x**3 - 2*x**2 + 3*x + 2)) == 0
val4 = F4.subs(x, 2)
assert val4 == 16 == 2 + integrate(fp, (x, 0, 2))
w4 = (F4 - 2).subs(x, 2)                                                                # 적분상수 누락
assert w4 == 14
chk(4, val4, [w4])
print('ABLATION 4 f(0)=2: 필요(빼면 적분상수가 정해지지 않음)')
assert (F4 - 2 + 3).subs(x, 2) != val4
print('ABLATION 4 f(0)의 값: 필요(3으로 바꾸면 17)')
print('ALL OK')
