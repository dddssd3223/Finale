# -*- coding: utf-8 -*-
# p1.py (10회 1–4번) 검증: 원문·뼈대 풀이 · 계산 정답 = 지정 선지(정답 번호) · 유일성 · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, Abs, Piecewise
x, t, k, a = symbols('x t k a', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 1, 2: 4, 3: 2, 4: 5}            # 분담표 ② ④ ① ⑤ 에서 1·3번을 맞바꿈
KEY = {1: ('J13', 'J13 분석집_변형 1'), 2: ('J26', 'J26 후보_순위 2'), 3: ('I25', 'I25 후보_순위 2'), 4: ('I55', '자체 (가장 가까운 I55)')}
STEP = {1: Rational(1, 5), 2: 2, 3: 1, 4: 1}
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
fJ = x**3 - 4*x**2 + 3*x; gJ = -x**2 + a*x                                             # J13: 27/4 ④
aJ = solve(diff(fJ, x).subs(x, 0) - diff(gJ, x).subs(x, 0), a); assert aJ == [3]
dJ = expand(fJ - gJ.subs(a, 3)); assert expand(dJ - x**2*(x - 3)) == 0
assert integrate(-dJ, (x, 0, 3)) == Rational(27, 4)
# STUDY-J13-변형①: y=x^4-3x^2, y=-x^2+k 가 서로 다른 두 점에서 접함 → k=-1, 넓이 16/15
dS = x**4 - 2*x**2 - k
kS = solve(sp.discriminant(t**2 - 2*t - k, t), k)                                      # x^2=t 의 이차식이 양의 중근
assert kS == [-1] and expand(dS.subs(k, -1) - (x**2 - 1)**2) == 0
assert integrate((x**2 - 1)**2, (x, -1, 1)) == Rational(16, 15)
vL = a*t - 3*t**2                                                                       # LIVE2-04-072: a=6 ②
assert solve(integrate(vL, (t, 0, 4)) + 16, a) == [6]
vO = t**4 - 50*t + a                                                                    # J26 원문: a=3 ③
assert solve(integrate(vO, (t, 0, 5)) - 15, a) == [3]
fI = sp.cancel((3*x**4 - 3*x)/(x - 1))                                                  # I25 원문: 16 ②
assert expand(fI - (3*x**3 + 3*x**2 + 3*x)) == 0 and integrate(fI, (x, -2, 2)) == 16
fL = sp.cancel((5*x**4 - 5*x)/(x - 1))                                                  # LIVE2-03-101: 64 ②
assert integrate(x**2*fL, (x, -2, 2)) == 64
assert integrate(x + Abs(x - 3), (x, 1, 4)) == 10                                       # I55 원문: 10
print('원문·뼈대 풀이 OK (J13=27/4, STUDY-J13-변형①=16/15, J26=3, LIVE2-04-072=6, I25=16, LIVE2-03-101=64, I55=10)')

# ===== 1번 =====
c1 = 3*x**4 - 6*x**2; l1 = -3
d1 = expand(c1 - l1)
assert expand(d1 - 3*(x**2 - 1)**2) == 0
assert sorted(set(real_roots(Poly(d1, x)))) == [-1, 1]                                  # 교점 두 개(둘 다 접점)
assert all(d1.subs(x, Rational(i, 10)) >= 0 for i in range(-10, 11))                    # 구간에서 곡선이 직선 위
val1 = integrate(d1, (x, -1, 1))
assert val1 == Rational(16, 5)
assert abs(sp.N(sp.Integral(Abs(d1), (x, -1, 1))) - Rational(16, 5)) < 1e-12
w1 = Rational(3 * 2**4, 12)                                                            # 삼차 넓이 공식 1/12 오적용
assert w1 == 4
assert val1 != Rational(16, 15) and val1 != Rational(27, 4) and val1 != 27             # 분석집·원문·8회 1번 답과 다름
chk(1, val1, [w1])
for ll in (-2, -1, 0):                                                                  # 직선을 바꾸면 접하지 않거나 넓이가 바뀜
    rr = sorted(set(real_roots(Poly(c1 - ll, x))))
    vv = integrate(Abs(c1 - ll), (x, rr[0], rr[-1])) if len(rr) >= 2 else None
    assert vv is None or sp.N(vv) != sp.N(val1)
print('ABLATION 1 직선 y=-3: 필요(다른 수평선이면 교점·넓이가 바뀜)')

# ===== 2번 =====
v2 = 10*t - 3*t**2
x2 = integrate(v2, (t, 0, t))
val2 = x2.subs(t, 2)
assert val2 == 12
assert all(v2.subs(t, Rational(i, 10)) >= 0 for i in range(0, 21))                     # 0~2에서 방향 전환 없음(위치 = 움직인 거리)
w2 = v2.subs(t, 2)                                                                     # 속도에 대입
assert w2 == 8
assert val2 not in (-16, 6, 3, 15)                                                      # LIVE·원문 값과 다름
chk(2, val2, [w2])
assert (x2 + k).subs(t, 2).free_symbols == {k}
print('ABLATION 2 원점 출발: 필요(없으면 위치가 12+x(0)로 정해지지 않음)')
assert all(x2.subs(t, T) != 12 for T in (1, 3, 4))
print('ABLATION 2 시각 t=2: 필요(시각을 바꾸면 값이 바뀜)')

# ===== 3번 =====
f3 = 3*x**3 + 5*x**2 + 4*x
val3 = integrate(x**2*f3, (x, -1, 1))
assert val3 == 2
assert val3 == 2*integrate(5*x**4, (x, 0, 1))
w3 = 2*integrate(x**2*f3, (x, 0, 1))                                                   # 홀수차항까지 2배
assert w3 == 5
assert val3 != 16 and val3 != 64
chk(3, val3, [w3])
assert integrate(f3, (x, -1, 1)) != val3
print('ABLATION 3 적분 대상 x^2 f(x): 필요(f(x)만 적분하면 10/3)')
assert integrate(x**2*f3, (x, 0, 1)) != val3 and integrate(x**2*f3, (x, -1, 2)) != val3
print('ABLATION 3 구간 [-1,1]: 필요(구간을 바꾸면 값이 바뀜)')

# ===== 4번 =====
g4 = 2*x + Abs(x - 1)
val4 = integrate(Piecewise((x + 1, x < 1), (3*x - 1, True)), (x, -1, 3))
assert val4 == 12 and integrate(g4, (x, -1, 3)) == 12
w4 = integrate(3*x - 1, (x, -1, 3))                                                    # 절댓값을 그대로 벗김
assert w4 == 8 and integrate(x + 1, (x, -1, 3)) == 8
chk(4, val4, [w4])
print('ABLATION 4 절댓값: 필요(없으면 8)')
print('ALL OK')
