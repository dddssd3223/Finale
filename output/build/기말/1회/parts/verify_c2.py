# -*- coding: utf-8 -*-
"""10·12·14·16번 검증. --figures를 붙이면 figkit으로 SVG 두 개를 재생성한다.

출력 그림은 원문 J61·D28의 모양을 유지한다. 상용 글꼴이나 PDF는 쓰지 않는다.
"""
from pathlib import Path
from itertools import product
import os
import re
import runpy
import sys
import xml.etree.ElementTree as ET
import sympy as S

HERE = Path(__file__).resolve().parent
IT = runpy.run_path(str(HERE / 'c2.py'))['ITEMS']
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F

x, b = S.symbols('x b', real=True)
WANT = {10: 2, 12: 3, 14: 1, 16: 5}
assert set(IT) == set(WANT)


def number(text):
    m = re.fullmatch(r'(-?)\\(?:dfrac|frac)\{?(\d+)\}?\{?(\d+)\}?', str(text))
    return ((-1 if m[1] else 1)*S.Rational(m[2], m[3])) if m else S.sympify(text)


def check(no, answer, wrong_values=()):
    it = IT[no]
    ch = list(map(number, it['choices']))
    assert len(ch) == len(set(ch)) == 5
    assert {ch[j+1]-ch[j] for j in range(4)} == {1}
    assert it['ans'] == WANT[no] and ch[it['ans']-1] == answer
    assert ch.count(answer) == 1
    assert set(map(number, it['wrong'])) == set(wrong_values)
    assert all(w in ch and w != answer for w in wrong_values)
    assert it['author'] == 'codex' and it['bunseok'] is False
    print(f'{no}: 답 {answer}, 정답 {it["ans"]}, 유일성·등차·오답 근거 OK')


def original(key, answer):
    _, choices, recorded, _ = F.I[key]
    if choices and choices[0].startswith('T:'):
        actual = choices['①②③④⑤'.index(recorded)]
    else:
        actual = number(choices['①②③④⑤'.index(recorded)]) if choices else number(recorded)
    assert answer == actual, (key, answer, actual)
    print(f'ORIGINAL {key}: {answer} = 원문 정답 OK')


# 10: 부호·개별 넓이·넓이 차와 정적분을 모두 확인한다.
k = S.symbols('k', positive=True)
assert r'f(x)=kx(x-3)(x-4)' in IT[10]['body']
f10 = k*x*(x-3)*(x-4)
assert S.solve(f10, x) == [0, 3, 4]
assert f10.subs(x, 1) > 0 and f10.subs(x, S.Rational(7, 2)) < 0
area_a = S.integrate(f10, (x, 0, 3))
area_b = -S.integrate(f10, (x, 3, 4))
assert area_a == 45*k/4 and area_b == 7*k/12
assert S.simplify(area_a-area_b-S.integrate(f10, (x, 0, 4))) == 0
ks = S.solve(area_a-area_b-32, k)
assert ks == [3]
check(10, f10.subs({x: 1, k: ks[0]}))
fo = k*x*(x-2)*(x-3)
original('J61', S.solve(S.integrate(fo, (x, 0, 3))-3, k)[0])


# 12: 서로 다른 실근이 두 개인 삼차식의 두 인수형을 모두 조사한다.
def cubic_candidates(slope, point):
    accepted, rejected = [], []
    for h in (x*(x-b)**2+slope*x, x*x*(x-b)+slope*x):
        for value in S.solve(S.diff(h, x).subs(x, point), b):
            if value == 0:
                continue
            f = S.expand(h.subs(b, value))
            assert len(S.solve(f-slope*x, x)) == 2
            # 후보의 이계도함수가 0이 아니므로 부호로 극대·극소를 판정한다.
            second = S.diff(f, x, 2).subs(x, point)
            assert second != 0
            (accepted if second < 0 else rejected).append(f)
    return list(set(accepted)), list(set(rejected))


assert r'f(x)=4x' in IT[12]['cond'][0][1]
assert r'x=2' in IT[12]['cond'][1][1]
good, rejected = cubic_candidates(4, 2)
assert good == [x**3-8*x**2+20*x]
assert rejected == [x**3-4*x**2+4*x]
check(12, good[0].subs(x, 1))
old, _ = cubic_candidates(9, 3)
assert old == [x**3-12*x**2+45*x]
minpoints = [r for r in S.solve(S.diff(old[0], x), x) if S.diff(old[0], x, 2).subs(x, r) > 0]
assert minpoints == [5]
original('D40', old[0].subs(x, minpoints[0]))


# 14: 도함수의 부호가 실제로 바뀌는 근만 극값으로 센다.
pieces = [(-S.oo, -1, -4*(x+1)), (-1, 2, 4*(1-x*x)), (2, S.oo, 12*(x-3))]
assert pieces[0][2].subs(x, -1) == pieces[1][2].subs(x, -1) == 0
assert pieces[1][2].subs(x, 2) == pieces[2][2].subs(x, 2) == -12


def derivative_at(point):
    return next(p.subs(x, point) for lo, hi, p in pieces if lo <= point <= hi)


def extrema_count(height):
    roots = sorted(set(r for lo, hi, p in pieces for r in S.solve(p-height, x)
                       if r.is_real and lo <= r <= hi))
    changed = []
    for j, r in enumerate(roots):
        left = r-1 if j == 0 else (roots[j-1]+r)/2
        right = r+1 if j == len(roots)-1 else (r+roots[j+1])/2
        if S.sign(derivative_at(left)-height) != S.sign(derivative_at(right)-height):
            changed.append(r)
    return len(changed)


# 양쪽 무한 구간까지 포함해 모든 높이를 경계값 -12,0,4로 분류한다.
cases = [(-13, 0), (-12, 0), (-6, 2), (0, 2), (1, 4), (4, 2), (5, 2)]
for height, count in cases:
    assert extrema_count(S.Integer(height)) == count
assert S.solve(S.diff(pieces[1][2], x), x) == [0]
assert pieces[1][2].subs(x, 0) == 4
# 왼쪽 직선의 치역 [0,∞), 가운데 양쪽의 치역 [0,4],[-12,4], 오른쪽 직선 [-12,∞).
# 교점 수가 달라질 수 있는 높이는 위 세 경계값뿐이므로 무한 구간의 분류도 완전하다.
integer_ks = [v for v in range(0, 5) if extrema_count(S.Integer(v)) == 4]
assert integer_ks == [1, 2, 3]
check(14, sum(integer_ks), [sum(range(1, 5))])
# D28 원문의 가운데 곡선은 식이 없으므로 그림의 부호 정보로 검증한다.
# f'은 모든 점에 정의되고, 부호 +,+,-,+에서 x=1 극대, x=3 극소이다.
# 왼쪽 원시함수는 -x²/2-x+C → -∞, 오른쪽 원시함수는 (x-3)²/2+C → +∞.
c = S.symbols('c', real=True)
assert S.limit(-x*x/2-x+c, x, -S.oo) == -S.oo
assert S.limit((x-3)**2/2+c, x, S.oo) == S.oo
original_signs = [1, 1, -1, 1]
assert original_signs[1:3] == [1, -1]
# f(3)>0이면 [1,∞)에서 양수, (-∞,1)에서는 단조증가하여 영점을 한 번만 지난다.
original('D28', 'T:ㄱ, ㄴ, ㄷ')


# 16: 연속성과 구간 내부 |f|>0에 따라 구간별 부호가 일정하다. 64개 배열을 전수 검사한다.
assert r'|12(x-n+1)(x-n)|' in IT[16]['cond'][0][1]
assert r'g(4)=8' in IT[16]['cond'][1][1]
mass, moment = [], []
for n in range(1, 7):
    hump = 12*(x-n+1)*(n-x)
    assert hump.subs(x, n-1) == hump.subs(x, n) == 0
    mass.append(S.integrate(hump, (x, n-1, n)))
    moment.append(S.integrate(x*hump, (x, n-1, n)))
assert mass == [2]*6 and moment == [1, 3, 5, 7, 9, 11]


def g_values(signs):
    return [2*sum(mass[i]*signs[i] for i in range(j))-sum(m*s for m, s in zip(mass, signs))
            for j in range(7)]


def solutions(local=True, value=True):
    result = []
    for signs in product([-1, 1], repeat=6):
        if local and signs[1:3] != (-1, 1):
            continue
        if value and g_values(signs)[4] != 8:
            continue
        answer = sum(m*s for m, s in zip(moment, signs))
        result.append((signs, answer))
    return result


valid = solutions()
assert valid == [((1, -1, 1, 1, -1, -1), -10)]
assert g_values(valid[0][0]) == [0, 4, 0, 4, 8, 4, 0]
check(16, valid[0][1])
print('16: 64개 부호 배열 전수 확인, 가능한 배열 1개')
for name, result in [('극소 위치', solutions(local=False)), ('g(4)=8', solutions(value=False))]:
    answers = sorted(set(answer for _, answer in result))
    assert len(answers) > 1
    print(f'ABLATION 16 {name}: 필요(가능한 답 {answers})')

# (가)의 크기 조건을 빼면 동일 부호에서 구간 넓이 3,2,2,1,2,2를 갖는 연속함수도 가능.
other_mass = [3, 2, 2, 1, 2, 2]
signs = valid[0][0]
assert sum(other_mass[i]*signs[i] for i in range(4))-sum(other_mass[i]*signs[i] for i in range(4, 6)) == 8
other_answer = sum((S.Rational(2*i+1, 2))*m*s for i, (m, s) in enumerate(zip(other_mass, signs)))
assert other_answer == -13
print('ABLATION 16 (가): 필요(연속인 다른 구간별 이차함수의 답 -13)')

# 연속성을 빼면 둘째 구간 앞뒤에서 +,-, 넷째 구간 앞뒤에서 -,+가 허용된다.
signed_pieces = [(0, 1, 1), (1, S.Rational(3, 2), 1), (S.Rational(3, 2), 2, -1),
                 (2, 3, 1), (3, S.Rational(7, 2), -1), (S.Rational(7, 2), 4, 1),
                 (4, 5, -1), (5, 6, -1)]
g4_without_continuity = 0
answer_without_continuity = 0
for lo, hi, sign in signed_pieces:
    n = int(S.floor(lo))+1
    p = sign*12*(x-n+1)*(n-x)
    g4_without_continuity += (1 if hi <= 4 else -1)*S.integrate(p, (x, lo, hi))
    answer_without_continuity += S.integrate(x*p, (x, lo, hi))
assert g4_without_continuity == 8
assert answer_without_continuity != -10
print(f'ABLATION 16 연속성: 필요(구간 내부 부호 변경 시 답 {answer_without_continuity})')

# 원문 I70: 16개 배열. 구간별 단조이므로 끝값과 x=2 양옆 부호로 전역 최솟값을 판정한다.
old_signs = []
for signs in product([-1, 1], repeat=4):
    gv = [2*sum(signs[:j])-sum(signs) for j in range(5)]
    if signs[1:3] == (-1, 1) and gv[2] == 0 and min(gv) == 0:
        old_signs.append(signs)
assert old_signs == [(1, -1, 1, -1)]
first_half_tail = S.integrate(6*x*(1-x), (x, S.Rational(1, 2), 1))
original('I70', first_half_tail+sum(old_signs[0][1:]))


def figures():
    os.environ.setdefault('MPLCONFIGDIR', '/tmp/finale-codex-mpl')
    sys.path.insert(0, str(HERE.parents[1] / '지침'))
    import figkit as K
    # J61: 원점부터 큰 양의 영역, 다음 근부터 작은 음의 영역, 오른쪽 위로 뻗는 삼차곡선.
    fig, ax = K.new((-0.45, 4.9), (-7, 23), size=(2.9, 2.0), dx=.08, dy=.07)
    f = lambda z: 3*z*(z-3)*(z-4)
    K.shade(ax, f, 0, 3)
    K.shade(ax, f, 3, 4)
    K.curve(ax, f, -.13, 4.6)
    for r in (0, 3, 4):
        K.dot(ax, r, 0, ms=2.4)
    K.label(ax, 1.25, 5, 'A', size=11)
    K.label(ax, 3.52, -1.2, 'B', size=9, bg=True)
    K.label(ax, 3, 1.4, 'P', size=9)
    K.label(ax, 4, -1.7, 'Q', size=9)
    K.label(ax, 4.0, 12, 'y=f(x)', size=9)
    K.save(fig, HERE / 'fig_c_10.svg')
    # D28: 왼쪽 감소 직선, x=-1부터 이어지는 봉우리, x=2의 골, 오른쪽 증가 직선.
    fig, ax = K.new((-3.1, 4.15), (-16, 8), size=(3.1, 2.0), dx=.07, dy=.07)
    K.curve(ax, lambda z: -4*(z+1), -2.8, -1)
    K.curve(ax, lambda z: 4*(1-z*z), -1, 2)
    K.curve(ax, lambda z: 12*(z-3), 2, 3.55)
    K.dash(ax, [0, 2, 2], [-12, -12, 0])
    for r in (-1, 1, 3):
        K.label(ax, r, -1.3, str(r), va='top', size=9)
    K.label(ax, 2, 1.0, '2', va='bottom', size=9)
    K.label(ax, -.18, 4.4, '4', ha='right', size=9)
    K.label(ax, -.18, -12, '-12', ha='right', size=9)
    K.label(ax, 2.1, 6, "y=f'(x)", size=9)
    K.save(fig, HERE / 'fig_c_14.svg')


if '--figures' in sys.argv:
    figures()
for no in (10, 14):
    path = HERE / f'fig_c_{no}.svg'
    assert path.exists()
    assert ET.parse(path).getroot().tag.endswith('svg')
    assert path.name in IT[no]['body']
print('그림 10·14: SVG 파일·본문 연결 OK')
print('ALL OK')
