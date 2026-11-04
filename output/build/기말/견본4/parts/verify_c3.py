# -*- coding: utf-8 -*-
"""18번: 일반 사차함수의 정지점 유형 전수 분류, 유일성, 세 조건 빼 보기."""
from pathlib import Path
import html
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
it = runpy.run_path(str(HERE / 'c3.py'))['ITEMS'][18]
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F
x, y, t, u, v, h, k = s.symbols('x y t u v h k', real=True)


def kink_count(poly):
    """|poly|가 미분불가능한 점은 poly의 단순 실근뿐이다."""
    return sum(mult == 1 for _, mult in s.Poly(poly, x).real_roots(multiple=False))


def integral(poly):
    return s.simplify(15 * s.integrate(poly, (x, -1, 1)))


def profile(poly):
    """정지점의 높이와 사이 구간을 모두 검사. 정지 높이 밖에서는 개수 불변.

    반환: (높이, 왼쪽 구간의 g, 그 높이의 g, 오른쪽 구간의 g).
    사용 예들의 계수와 정지 높이는 모두 유리수이므로 근을 정확하게 센다.
    """
    critical = s.Poly(s.diff(poly, x), x).real_roots(multiple=False)
    levels = sorted({s.simplify(poly.subs(x, root)) for root, _ in critical})
    samples = [levels[0] - 1]
    samples += [(a + b) / 2 for a, b in zip(levels, levels[1:])]
    samples += [levels[-1] + 1]
    counts = [kink_count(poly - sample) for sample in samples]
    return [(z, counts[j], kink_count(poly - z), counts[j + 1])
            for j, z in enumerate(levels)]


def conditions(poly, p):
    rows = profile(poly)
    discontinuities = {z for z, left, at, right in rows if left != at or at != right}
    at_p = kink_count(poly - p)
    if p in {row[0] for row in rows}:
        right_p = next(row[3] for row in rows if row[0] == p)
    else:
        # 정지 높이가 아니면 그 근방에서 g가 일정하다.
        right_p = at_p
    return (discontinuities == {s.Integer(0), s.sympify(p)},
            right_p == at_p,
            s.simplify(poly.subs(x, -1) + poly.subs(x, 1)) == 0)


# ===== 전수 분류: 실계수 삼차식 f'의 가능한 실근 유형은 아래 네 가지뿐이다.
# A1. 단순 실근 하나 + 비실수 켤레근: 유일한 극소점.
# A2. 세 번 겹친 실근 하나: 유일한 극소점.
# B. 두 번 겹친 실근 하나 + 단순 실근 하나: 정지변곡점 + 극소점.
# C. 서로 다른 실근 셋: 극소, 극대, 극소. 두 극솟값의 같음/다름을 분류.
# 최고차항이 양수이므로 A의 유일한 정지 높이 m에서 g(m)=0, 우극한=2.
# 따라서 (가)가 p=0인 한 점 집합인 경우까지 포함해 A는 (나)에 모순이다.
q, z = s.symbols('q z', real=True)
quadratic = y**2 + q*y + z
assert s.expand(quadratic - ((y + q/2)**2 + z - q*q/4)) == 0
# 비실수 켤레근이면 z-q²/4>0: f'=4(y-r)*quadratic의 부호는 y-r의 부호.
assert profile(x**4 + x*x) == [(0, 0, 0, 2)]
assert profile(x**4) == [(0, 0, 0, 2)]
print('EXHAUSTIVE A1/A2: 유일한 극소 높이 (g, 우극한)=(0,2), 불가능')

# B형 전체를 평행이동한 표준형. r!=0, k는 임의의 실수.
# 두 정지점의 가중평균을 원점으로 옮기면 모든 B형이 이 식으로 표시된다.
r = s.symbols('r', real=True, nonzero=True)
B = y**4 - 6*r*r*y*y + 8*r**3*y + k
assert s.expand(s.diff(B, y) - 4*(y-r)**2*(y+2*r)) == 0
low, shoulder = B.subs(y, -2*r), B.subs(y, r)
assert s.simplify(low) == k - 24*r**4
assert s.simplify(shoulder - low) == 27*r**4  # 항상 양수
assert s.expand(B-shoulder - (y-r)**3*(y+3*r)) == 0
assert s.expand(B-low - (y+2*r)**2*(y*y-4*r*y+6*r*r)) == 0
assert s.discriminant(y*y-4*r*y+6*r*r, y) == -8*r*r
# 정지변곡 높이에서 단순 실근은 하나이고 양옆 높이에서는 두 개.
assert profile(x**4-6*x*x+8*x+24) == [(0, 0, 0, 2), (27, 2, 1, 2)]
print('EXHAUSTIVE B: 최소 (0,2), 정지변곡 (1,2), 모두 (나)에 모순')

# C형 전체: 왼쪽 극소점을 y=0으로 옮기고 두 인접 간격을 a,b>0으로 둔다.
# 임의의 수평/수직 이동이 허용되므로 특정 계수의 사차함수에 국한되지 않는다.
a, b = s.symbols('a b', positive=True)
C = s.integrate(4*y*(y-a)*(y-a-b), y)
assert s.expand(s.diff(C, y)-4*y*(y-a)*(y-a-b)) == 0
min_left, maximum, min_right = [s.factor(C.subs(y, rr)) for rr in (0, a, a+b)]
assert min_left == 0
assert s.simplify(maximum-a**3*(a+2*b)/3) == 0
assert s.simplify(maximum-min_right-b**3*(2*a+b)/3) == 0
assert s.factor(min_right-min_left) == (a-b)*(a+b)**3/3
# 두 극솟값이 다르면 아래쪽 최소, 위쪽 최소, 최대의 서로 다른 높이 셋.
# 각 높이에서 (좌극한,g,우극한)은 (0,0,2), (2,2,4), (4,2,2).
# 두 최소 높이가 같으면 (0,0,4), (4,2,2)의 두 높이.
# 아래는 두 최소 높이 순서를 모두 확인하는 정확한 대표 사례이고,
# 위의 양수 간격 공식/단조구간 논증이 모든 a,b>0를 포괄한다.
unequal = s.expand(C.subs({y:x, a:1, b:2}))
assert profile(unequal) == [(-9, 0, 0, 2), (0, 2, 2, 4), (s.Rational(5,3), 4, 2, 2)]
reflected = s.expand(unequal.subs(x, 3-x))
assert profile(reflected) == profile(unequal)
assert min_right.subs({a:1, b:2}) < min_left
assert min_right.subs({a:2, b:1}) > min_left
assert s.expand(C.subs(b, a) - y**2*(2*a-y)**2) == 0
print('EXHAUSTIVE C: 최소 높이 다름 -> 불연속 3개; 같음 -> 최소 (0,4), 최대 (2,2)')

# (가)(나)로 C의 같은 두 극솟값=0, 극댓값=p>0만 남는다.
# f=(x-u)²(x-v)², u!=v; (다)의 두 항은 비음수이므로 각각 0.
# 아래 검사는 u,v의 위치 조합 전부를 상징적으로 푼다. 격자 탐색이 아니다.
square = (x-u)**2 * (x-v)**2
minus_one = s.factor(square.subs(x, -1))
plus_one = s.factor(square.subs(x, 1))
solutions = s.solve([minus_one, plus_one], [u, v], dict=True)
assert {tuple(sol[z] for z in (u,v)) for sol in solutions} == {(-1,1), (1,-1)}
candidates = {s.expand(square.subs(sol)) for sol in solutions}
assert candidates == {x**4-2*x*x+1}
f = candidates.pop()
assert profile(f) == [(0, 0, 0, 4), (1, 4, 2, 2)]
assert conditions(f, 1) == (True, True, True)
print('UNIQUE 18: f=(x²-1)², p=1; 모든 실계수 사차함수 중 유일')

# ===== 지정 정답, 선지 등차와 오답 근거: 4개 모두 실제 계산값을 대조.
answer = integral(f)
choices = list(map(s.sympify, it['choices']))
assert it['author'] == 'codex' and it['ans'] == 1
assert answer == choices[it['ans']-1] == 16
assert len(choices) == len(set(choices)) == 5
assert len({choices[j+1]-choices[j] for j in range(4)}) == 1
wrong = [integral(x**4+c*x*x+1) for c in (-1,0,1,2)]
assert wrong == choices[1:] == [26,36,46,56]
written_wrong = [s.Integer(value) for value in re.findall(r'[②③④⑤]\s*\\\((\d+)\\\)', it['wrong'])]
assert written_wrong == wrong
assert profile((x*x+1)**2) == [(1,0,0,2)]
print(f'ANSWER 18: {answer}, position=1, AP={choices}, wrong={wrong}: OK')

# ===== 조건을 하나씩 삭제. 남은 조건은 함수의 정확한 g 표로 재확인.
# (가) 삭제: 불연속점은 -1만, p=1에서 g는 국소적으로 상수 2.
# (나) 삭제: 극댓값이 0, 극솟값이 p=-1/4인 경우가 살아남는다.
# (다) 삭제: 두 극소점 사이 거리가 달라지는 다른 사차함수가 남는다.
ablations = [
    ('(가)', x**4-1, s.Integer(1), (False,True,True), -24),
    ('(나)', x**4-x*x, -s.Rational(1,4), (True,False,True), -4),
    ('(다)', (x*x-2)**2, s.Integer(4), (True,True,False), 86),
]
for label, poly, p, expected, value in ablations:
    assert conditions(poly, p) == expected
    assert integral(poly) == value != answer
    print(f'ABLATION 18 {label}: 필요(f={s.expand(poly)}, p={p}, 조건={expected}, 답 {value})')

# 본문의 최고차항 계수와 사차 조건도 실제로 필요하다.
scaled = 2*(x*x-1)**2
assert conditions(scaled, 2) == (True,True,True)
assert integral(scaled) == 32 != answer
print('ABLATION 18 최고차항 계수 1: 필요(2(x²-1)², p=2, 답 32)')
higher = (x*x-1)**4
assert s.Poly(higher,x).LC() == 1 and s.degree(higher,x) == 8
assert conditions(higher,1) == (True,True,True)
assert integral(higher) == s.Rational(256,21) != answer
print('ABLATION 18 사차함수: 필요((x²-1)⁴, p=1, 답 256/21)')

# ===== 원문 I44 직접 풀이 및 저장된 선지/정답과 대조. 자료 원문은 복사하지 않는다.
A, Bc, D, z = s.symbols('A B D z', real=True)
original = x**3 + A*x*x + Bc*x + D
symmetry = s.Poly(s.expand(original.subs(x,-z)+original.subs(x,z+2)-2*original.subs(x,1)),z)
sol_A = s.solve(symmetry.all_coeffs(), A)
assert sol_A == {A:-3}
sol_B = s.solve(s.diff(original.subs(sol_A),x).subs(x,-1), Bc)
assert sol_B == [-9]
original = original.subs({A:-3, Bc:-9})
assert s.solve(s.diff(original,x),x) == [-1,3]
sol_D = s.solve(original.subs(x,3),D)
assert sol_D == [27]
original = original.subs(D,27)
assert profile(original) == [(0,1,1,3), (32,3,1,1)]
original_answer = s.integrate(original,(x,-1,1))
original_data = F.I['I44']
assert original_answer == 52
assert original_data[2] == '④'
assert s.sympify(original_data[1]['①②③④⑤'.index(original_data[2])]) == original_answer
print('ORIGINAL I44: 정적분=52, 저장된 정답 ④의 선지=52: OK')

# ===== 원문과 같은 기준: HTML 태그와 공백 제거, 수식 소스와 조건 라벨 포함.
def text_length(text):
    return len(re.sub(r'\s', '', html.unescape(re.sub(r'<[^>]+>', '', text))))

assert [label for label,_ in it['cond']] == ['가','나','다']
problem = it['body'] + ''.join(f'({label}){text}' for label,text in it['cond']) + it.get('after','')
old_length, new_length = text_length(original_data[0]), text_length(problem)
assert old_length == 301
assert old_length <= new_length <= 330
assert 'x^4+ax^2+bx+1' not in it['body']
print(f'LENGTH 18: 원문 {old_length}자 / 재작성 {new_length}자; 조건 3개: OK')
print('ALL OK')
