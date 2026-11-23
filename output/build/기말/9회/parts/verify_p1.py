# -*- coding: utf-8 -*-
# p1.py (9회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, factor, limit
x, t, k, p, q, h = symbols('x t k p q h', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 4, 2: 1, 3: 5, 4: 2}            # 분담표 ④ ① ⑤ ② 그대로
KEY = {1: ('J53', 'J53 후보_순위 2'), 2: ('J18', 'J18 분석집_변형 1'), 3: ('M18', 'M18 후보_순위 2'), 4: ('I28', '자체 (가장 가까운 I28)')}
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
    s = str(s)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', s)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(s)

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
xJ = integrate(3*t**2 - 4*t + k, (t, 0, t))                                           # J53: 6
kJ = solve(xJ.subs(t, 1) + 3, k); assert kJ == [-2]
assert (xJ.subs(t, 3) - xJ.subs(t, 1)).subs(k, -2) == 6
xG = integrate(4*t**3 - 6*t**2 + 2*t + k, (t, 0, t))                                  # GEN2-04-108: 32
kG = solve(xG.subs(t, 1) + 2, k); assert kG == [-2]
assert (xG.subs(t, 3) - xG.subs(t, 1)).subs(k, -2) == 32
kJ18 = solve(integrate(x**3 + 2*x - k, (x, 0, 1)), k); assert kJ18 == [Rational(5, 4)]  # J18: 5/4 ②
# STUDY-J18-변형①: 공통 부분 더하기 → k=1 (x로만 확인: 왼쪽 = ∫_0^{c}(k-f) , 오른쪽 = ∫_c^1(f-k)+∫_1^{(4-k)/2}(-2x+4-k))
fS = x**3 + x
def sides(kk):
    c = [r for r in real_roots(Poly(fS - kk, x)) if 0 < r < 1][0]
    L = integrate(kk - fS, (x, 0, c)); R = integrate(fS - kk, (x, c, 1)) + integrate(-2*x + 4 - kk, (x, 1, (4 - kk)/2))
    return sp.N(L - R)
assert abs(sides(1)) < 1e-12 and abs(sides(Rational(3, 4))) > 1e-3
xM = t**3 - 2*t**2 - 3*t                                                              # M18: 12 ④
tM = [r for r in solve(xM, t) if r > 0]; assert tM == [3] and diff(xM, t).subs(t, 3) == 12
fI = x**4 + p*x**2 + q                                                                # I28: 9
sI = solve([fI.subs(x, 0) - 1, diff(fI, x).subs(x, 1)], [p, q], dict=True)
assert fI.subs(sI[0]).subs(x, 2) == 9
print('원문·뼈대 풀이 OK (J53=6, GEN2-04-108=32, J18=5/4, STUDY-J18-변형①=1, M18=12, I28=9)')

# ===== 1번 =====
v1 = 4*t**3 - 6*t**2 + 2*t - 1
X1 = integrate(v1, t)
val1 = integrate(v1, (t, 1, 3))
assert val1 == 34 and X1.subs(t, 3) - X1.subs(t, 1) == 34
w1 = integrate(v1, (t, 0, 3))                                                         # 아래끝 0으로
assert w1 == 33
assert val1 != 32 and val1 != 6 and val1 != 42                                       # GEN·원문·N제 306 답과 다름
chk(1, val1, [w1])
assert integrate(v1 + k, (t, 1, 3)).free_symbols == {k}
print('ABLATION 1 상수항 -1: 필요(미지수로 두면 34+2k로 정해지지 않음)')
for a_, b_ in ((0, 3), (1, 2), (2, 3)):
    assert integrate(v1, (t, a_, b_)) != 34
print('ABLATION 1 구간 t=1~3: 필요(구간을 바꾸면 값이 바뀜)')

# ===== 2번 =====
c2 = 4*x**3 + 2*x; l2 = -6*x + 12
g2 = expand(c2 - l2)
assert expand(g2 - 4*(x - 1)*(x**2 + x + 3)) == 0
assert sorted(set(real_roots(Poly(g2, x)))) == [1]                                    # 교점 하나
assert solve(l2, x) == [2] and solve(c2, x) == [0]
# 전수 확인: 영역 = {0≤x≤2, 0≤y≤min(c2,l2)} (c2 증가·l2 감소), 넓이 = ∫_0^2 min
assert all(diff(c2, x).subs(x, s) > 0 for s in (0, Rational(1, 2), 1, 2))
val2 = integrate(c2, (x, 0, 1)) + integrate(l2, (x, 1, 2))
assert val2 == 5
num = sp.N(sp.Integral(sp.Min(c2, l2), (x, 0, 2)))                                    # 수치 재확인
assert abs(num - 5) < 1e-9
w2a = integrate(l2 - c2, (x, 0, 1))                                                   # y축 쪽 부분
assert w2a == 7 and w2a + val2 == Rational(1, 2)*2*12
w2b = integrate(c2, (x, 0, 1)) + Rational(1, 2)*2*6                                   # 밑변 0~2로
assert w2b == 8
chk(2, val2, [w2a, w2b])
print('ABLATION 2 x축: 필요(없으면 곡선과 직선만으로는 닫힌 부분이 생기지 않음 — 교점이 하나뿐)')
c2b = x**3 + x; l2b = -2*x + 4                                                        # 분석집 변형 수치 그대로면 다른 값
assert integrate(c2b, (x, 0, 1)) + integrate(l2b, (x, 1, 2)) == Rational(7, 4)
print('뼈대 수치(분석집)로는 7/4 — 같은 문항 아님')

# ===== 3번 =====
x3 = t**3 + t**2 - 12*t
assert expand(x3 - t*(t - 3)*(t + 4)) == 0
r3 = [r for r in solve(x3, t) if r > 0]
assert r3 == [3]                                                                      # 다시 원점: 하나
v3 = diff(x3, t).subs(t, 3)
assert v3 == 21 and v3 != 0                                                           # 속도 0이 아니라 '지남'
w3 = diff(x3, t, 2).subs(t, 3)
assert w3 == 20
assert expand(x3 - (t**3 - 2*t**2 - 8*t)) != 0 and expand(x3 - (t**3 - 3*t**2 - 4*t)) != 0   # GEN1-02-042·LIVE1-02-056과 다른 식
chk(3, v3, [w3])
print('ABLATION 3 t>=0·출발 후 다시: 필요(음근 t=-4, 출발 t=0을 버려야 t=3 하나)')

# ===== 4번 =====
cs = symbols('c0:4')                                                                  # 일반 사차(최고차 1)에서 전수
f4 = x**4 + sum(cs[i]*x**i for i in range(4))
eqs = Poly(expand(f4.subs(x, -x) - f4), x).coeffs()
L4 = limit(integrate(diff(f4, x).subs(x, t), (t, 1, x))/(x - 1), x, 1)
assert expand(L4 - diff(f4, x).subs(x, 1)) == 0                                       # 극한 = f'(1)
S4 = solve(list(eqs) + [f4.subs(x, 0) - 1, L4 - 2], cs, dict=True)
assert len(S4) == 1
f4s = f4.subs(S4[0])
assert expand(f4s - (x**4 - x**2 + 1)) == 0
val4 = f4s.subs(x, 2)
assert val4 == 13
sw = solve([fI.subs(x, 0) - 1, fI.subs(x, 1) - 2], [p, q], dict=True)              # 극한을 f(1)로 읽음
w4 = fI.subs(sw[0]).subs(x, 2)
assert w4 == 17
chk(4, val4, [w4])
S4b = solve([f4.subs(x, 0) - 1, L4 - 2], cs, dict=True)                               # 우함수 조건 빼기
assert any(len(f4.subs(s).free_symbols - {x}) > 0 for s in S4b)
print('ABLATION 4 f(-x)=f(x): 필요(없으면 계수가 정해지지 않음)')
assert solve(list(eqs) + [L4 - 2], cs, dict=True) and len(f4.subs(solve(list(eqs) + [L4 - 2], cs, dict=True)[0]).subs(x, 2).free_symbols) > 0
print('ABLATION 4 f(0)=1: 필요(없으면 f(2)=12+q로 정해지지 않음)')
assert len(f4.subs(solve(list(eqs) + [f4.subs(x, 0) - 1], cs, dict=True)[0]).subs(x, 2).free_symbols) > 0
print('ABLATION 4 극한=2: 필요(없으면 f(2)=17+4p... 정해지지 않음)')
print('ALL OK')
