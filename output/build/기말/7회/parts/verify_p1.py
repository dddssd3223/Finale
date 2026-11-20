# -*- coding: utf-8 -*-
# p1.py (7회 1–4번) 검증: 원문 풀이 · 계산 정답 = 지정 선지(분담표 정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots
x, a, t, C1, C2 = symbols('x a t C1 C2', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 2, 2: 4, 3: 1, 4: 5}                                   # 분담표 정답 ② ④ ① ⑤
KEY = {1: ('I52', 'I52 후보_순위 2'), 2: ('I7', 'I7 후보_순위 2'), 3: ('D55', 'D55 후보_순위 2'), 4: ('D49', '자체 (가장 가까운 D49)')}
DESC = {3}                                                         # 내림차순 선지 번호
assert sorted(IT) == [1, 2, 3, 4]
for no, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[no], no
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent'] and it['level'] == '하'
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype']
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body']   # 1–4번: 상자·그림 없음
    assert '이러한' not in it['body'] and '이와 같은' not in it['body']
    assert not re.search(r'\\\([^)]*?[<>]', it['body'])              # 수식 안 맨 부등호 없음
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(c):
    return nsimplify(str(c))

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    d = {ch[i + 1] - ch[i] for i in range(4)}
    dd = list(d)[0]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and len(set(ch)) == 5 and len(d) == 1
            and ((dd < 0) == (no in DESC)) and abs(dd) == 1
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def piece(gl, gr, cut):
    """x<cut에서 f'=gl, x>=cut에서 f'=gr인 연속함수 f의 두 조각(왼쪽 적분상수 C1), C2는 연속으로 유일하게 정해짐"""
    L = integrate(gl, x) + C1
    R = integrate(gr, x) + C2
    s = solve(L.subs(x, cut) - R.subs(x, cut), C2)
    assert len(s) == 1
    return L, R.subs(C2, s[0])

def tangents(curve, px, py):
    """점 (px,py)를 지나는 접선의 접점 t(실수 전부)"""
    line0 = diff(curve, x).subs(x, t)*(px - t) + curve.subs(x, t)
    return sorted(set(real_roots(Poly(expand(line0 - py), t))))

# ===== 원문 풀이 =====
assert integrate(6*x**2 - 2*x + 1, (x, 0, 2)) == 14                                    # I52 ②
L0, R0 = piece(3*x**2 - 4, -4*x + 3, 1)                                                # I7: f(0)=0 → f(1)+f(2)=-9 ④
c0 = solve(L0.subs(x, 0), C1)
assert c0 == [0] and (R0.subs(x, 1) + R0.subs(x, 2)).subs(C1, 0) == -9
fD = x**3 + a*x + 9                                                                    # D55: x=-1 극대 → 극솟값 7 ②
aD = solve(diff(fD, x).subs(x, -1), a)
assert aD == [-3] and fD.subs(a, -3).subs(x, 1) == 7 and diff(fD, x, 2).subs(x, -1) < 0
tD = tangents(x**3 - x + 2, 0, 4)                                                      # D49: 접점 -1, 접선 y=2x+4, x절편 -2 ④
assert tD == [-1]
mD = diff(x**3 - x + 2, x).subs(x, -1)
assert mD == 2 and solve(mD*x + 4, x) == [-2]
# LIVE 선례: 화성고 f(3)-f(0)=13/2, 인창고 극댓값 6
Lh, Rh = piece(3*x**2 - x, x + 1, 1)
assert sp.simplify(Rh.subs(x, 3) - Lh.subs(x, 0)) == Rational(13, 2)
fi = x**3 - 3*x**2 + a*x + 1
ai = solve(diff(fi, x).subs(x, 3), a)
assert ai == [-9] and fi.subs(a, -9).subs(x, -1) == 6
print('원문·선례 풀이 OK (I52=14, I7=-9, D55=7, D49=-2, LIVE2-03-029=13/2, LIVE1-01-117=6)')

# ===== 1번 =====
g1 = 3*x**2 - 4*x + 2
assert expand(integrate(g1, x) - (x**3 - 2*x**2 + 2*x)) == 0
v1 = integrate(g1, (x, 0, 3))
assert v1 == 15
chk(1, v1, [integrate(6*x**2 - 2*x + 1, (x, 0, 2))])               # 오답: 원문 답 14

# ===== 2번 =====
gl, gr = 3*x**2 + 2*x, 4*x + 1
assert gl.subs(x, 1) == gr.subs(x, 1) == 5                         # 숨은 관계: 경계에서 기울기 일치(원문 -1=-1)
L2, R2 = piece(gl, gr, 1)
v2 = sp.simplify(R2.subs(x, 2) - L2.subs(x, 0))
assert v2 == 9 and not v2.free_symbols                             # C1과 무관하게 하나로 정해짐
assert v2 == integrate(gl, (x, 0, 1)) + integrate(gr, (x, 1, 2))   # 빠른 풀이
w2 = integrate(gr, x).subs(x, 2) - integrate(gl, x).subs(x, 0)     # 오답: 연속 안 씀(적분상수 같게)
assert w2 == 10
chk(2, v2, [w2])
# 조건 빼 보기
free = (integrate(gr, x) + C2).subs(x, 2) - (integrate(gl, x) + C1).subs(x, 0)
assert free.free_symbols == {C1, C2}
print('ABLATION 2 연속: 필요(연속이 없으면 f(2)-f(0)=10+C2-C1로 정해지지 않음)')

# ===== 3번 =====
f3 = x**3 + a*x + 7
a3 = solve(diff(f3, x).subs(x, 1), a)
assert a3 == [-3]                                                  # a 하나로 정해짐
F3 = f3.subs(a, -3)
cr = sorted(solve(diff(F3, x), x))
assert cr == [-1, 1] and diff(F3, x, 2).subs(x, 1) > 0 and diff(F3, x, 2).subs(x, -1) < 0   # x=1 극소 확인, x=-1 극대
v3 = F3.subs(x, -1)
assert v3 == 9
w3a = F3.subs(x, 1)                                                # 오답: 극솟값
w3b = fD.subs(a, -3).subs(x, 1)                                    # 오답: 원문 답 7
assert (w3a, w3b) == (5, 7)
chk(3, v3, [w3a, w3b])
assert f3.subs(x, -sp.sqrt(-a/3)).free_symbols == {a}
print('ABLATION 3 x=1에서 극소: 필요(없으면 a가 정해지지 않아 극댓값이 a의 식으로 남음)')

# ===== 4번 =====
c4 = x**3 + 2*x
assert c4.subs(x, 0) != -2                                         # 점 (0,-2)는 곡선 위에 있지 않음
t4 = tangents(c4, 0, -2)
assert t4 == [1]                                                   # 접점 하나(전수: -2t^3=-2의 실근)
v4 = diff(c4, x).subs(x, 1)
assert v4 == 5
line = v4*(x - 1) + c4.subs(x, 1)
assert line.subs(x, 0) == -2
w4a = diff(c4, x).subs(x, 0)                                       # 오답: (0,-2)를 접점으로 봄
w4b = c4.subs(x, 1)                                                # 오답: 접점의 y좌표
assert (w4a, w4b) == (2, 3)
chk(4, v4, [w4a, w4b])
k = symbols('k', real=True)
assert len(tangents(c4, 0, 0)) == 1 and diff(c4, x).subs(x, tangents(c4, 0, 0)[0]) == 2
print('ABLATION 4 점 (0,-2): 필요(점을 (0,0)으로 바꾸면 접점 0, 기울기 2로 답이 바뀜)')
print('ALL OK')
