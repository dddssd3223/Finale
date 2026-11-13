# -*- coding: utf-8 -*-
"""17번 후보의 정확한 실근 분할 검증. 실행 위치와 무관하다.

판별식, 두 식의 resultant, 정의역 끝값의 영점을 모두 구한다.
그 밖에서는 근의 개수·끝점 통과·두 식의 근 중복이 변하지 않으므로
각 열린 셀의 유리수 표본과 모든 경계를 Sturm 방법으로 검사하면
실수 매개변수 전체를 빠짐없이 검증한다(수치 격자 추측이 아님).
"""
from pathlib import Path
import html
import re
import runpy
import sys

import sympy as S

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[2]
it = runpy.run_path(str(HERE / 'c17.py'))['ITEMS'][17]
x, a = S.symbols('x a', real=True)
f = 2*x**3 + a*x
line = 27*x + 108
P, Q = f-line, f+line
cut = S.solve(line, x)[0]
assert cut == -4


def nroots(poly, lo=cut):
    """[lo,∞)에서 중복도를 제외한 서로 다른 실근을 정확히 센다."""
    p = S.Poly(poly, x).sqf_part()
    return int(p.count_roots(lo, S.oo)) if p.degree() else 0


def counts(cubic):
    p, q = cubic-line, cubic+line
    common = S.gcd(p, q)
    np, nq, nc = nroots(p), nroots(q), nroots(common)
    return np, nq, nc, np+nq-nc


# 대칭성에서 짝수 차수 항의 계수가 사라지는 것도 확인한다.
b, c, d = S.symbols('b c d', real=True)
general = 2*x**3+b*x**2+c*x+d
odd_coeffs = S.Poly(general+general.subs(x, -x), x).all_coeffs()
assert S.solve(odd_coeffs, (b, d)) == {b: 0, d: 0}
bound = S.solve_univariate_inequality(f.subs(x, 1) >= -35, a, relational=False)
assert bound == S.Interval(-37, S.oo)

# 실근 수가 바뀔 수 있는 모든 매개변수 경계를 대수적으로 추출한다.
projection = [S.discriminant(P, x), S.discriminant(Q, x),
              S.resultant(P, Q, x), P.subs(x, cut), Q.subs(x, cut)]
critical = sorted(set().union(*(S.solveset(p, a, domain=S.S.Reals)
                               for p in projection)))
assert critical == [-81, -32, -27]
print('전수 분할 경계:', critical)
print('판별식:', [S.factor(p) for p in projection[:2]])
assert S.LC(S.Poly(P, x)) == S.LC(S.Poly(Q, x)) == 2

edges = [-S.oo] + critical + [S.oo]
cells = []
for left, right in zip(edges, edges[1:]):
    sample = right-1 if left == -S.oo else left+1 if right == S.oo else (left+right)/2
    cell = S.Interval.open(left, right)
    cells.append((cell, sample))
cells += [(S.FiniteSet(k), k) for k in critical]
expected = {-82: (2, 2, 0, 4), S.Rational(-113, 2): (2, 0, 0, 2),
            S.Rational(-59, 2): (3, 1, 0, 4), -26: (1, 1, 0, 2),
            -81: (2, 1, 0, 3), -32: (3, 1, 1, 3), -27: (2, 1, 0, 3)}
allowed_count = S.S.EmptySet
for cell, sample in cells:
    result = counts(f.subs(a, sample))
    assert result == expected[sample], (sample, result)
    if result[-1] >= 3:
        allowed_count = S.Union(allowed_count, cell)
    print(f'전수 검증 a∈{cell}: P,Q,공통근,교점={result}')
assert allowed_count == S.Union(S.Interval(-S.oo, -81), S.Interval(-32, -27))
feasible = S.Intersection(allowed_count, bound)
assert feasible == S.Interval(-32, -27)

# 학교 해설의 다섯 경우, 포함되는 양 끝값, 공통근 경계.
for av, want in [(-37, 2), (-32, 3), (-30, 4), (-27, 3), (0, 2)]:
    assert counts(f.subs(a, av))[-1] == want
assert S.expand(P.subs(a, -27)-2*(x-6)*(x+3)**2) == 0
assert S.gcd(P.subs(a, -32), Q.subs(a, -32)) == x+4
assert all(p.subs(a, -32) != 0 for p in projection[:2])
print('경계 함정: a=-32는 접하는 경우가 아니며 공통근 -4를 한 번 세어 3교점')

# 해설에서 사용한 Q의 극솟값 하한과 P의 극대점 위치를 확인한다.
assert 108-4*(S.Rational(5, 3))**S.Rational(3, 2) > 0
assert S.Rational(27+37, 6) < 16
objective = S.simplify(S.sqrt(5)*f.subs(x, S.sqrt(5)))
assert objective == 50+5*a and S.diff(objective, a) == 5
answer = objective.subs(a, feasible.start)
assert answer == -110
assert S.solveset(objective-answer, a, domain=feasible) == S.FiniteSet(-32)
assert counts(f.subs(a, -32))[-1] == 3
assert f.subs({x: 1, a: -32}) >= -35
print('정답·유일성: 연속구간 [-32,-27]에서 50+5a는 증가, 유일한 최소점 a=-32, 값 -110')

choices = list(map(S.sympify, it['choices']))
assert len(choices) == len(set(choices)) == 5
assert {choices[i+1]-choices[i] for i in range(4)} == {-25}
assert it['ans'] == 2 and choices[it['ans']-1] == answer
mistakes = {
    -85: objective.subs(a, -27),     # 접하는 경계만 선택
    -135: objective.subs(a, -37),    # (가) 삭제
    -160: S.sqrt(5)*(-32*S.sqrt(5)), # 삼차항 누락
}
for expected_value, computed in mistakes.items():
    assert expected_value == computed and computed in choices and computed != answer
    assert str(expected_value) in it['wrong']
print('선지: 등차 -25, 정답 ②, 오답 3개 계산·선지 포함 확인')

# 조건 빼 보기: 조건을 뺀 문제의 실제 허용범위와 반례를 확인한다.
assert objective.subs(a, bound.start) == -135
assert counts(f.subs(a, -37))[-1] == 2
print('ABLATION 17 (가): 필요(삭제하면 a≥-37, 최솟값 -135=③)')
assert S.limit(objective, a, -S.oo) == -S.oo
assert S.Interval(-S.oo, -81).is_subset(allowed_count)
print('ABLATION 17 (나): 필요(삭제하면 a≤-81도 허용, 아래로 유계가 아니어서 최솟값 없음)')

# 본문의 설정 조건도 개별 삭제 시 답이 달라지는 명시적 반례.
scaled = S.Rational(11, 10)*f.subs(a, -32)
assert counts(scaled)[-1] >= 3 and scaled.subs(x, 1) >= -35
assert S.simplify(S.sqrt(5)*scaled.subs(x, S.sqrt(5))) == -121 < answer
print('ABLATION 17 최고차항 계수 2: 필요(계수 11/5인 반례에서 목적값 -121)')
shifted = f.subs(a, -32)-1
assert counts(shifted)[-1] >= 3 and shifted.subs(x, 1) >= -35
assert S.sqrt(5)*shifted.subs(x, S.sqrt(5)) < answer
print('ABLATION 17 원점 대칭: 필요(2x³-32x-1은 두 상자 조건을 만족, 목적값 -110-√5)')

# 원문 직접 풀이: f=2x³-6p²x, -f(1)=4p³. p>0인 해는 1뿐.
p = S.symbols('p', positive=True)
original_f = 2*x**3-6*p**2*x
height_eq = S.expand(-original_f.subs(x, 1)-4*p**3)
assert S.expand(height_eq+2*(p-1)**2*(2*p+1)) == 0
assert S.solveset(height_eq, p, domain=S.Interval.open(0, S.oo)) == S.FiniteSet(1)
original = original_f.subs(p, 1)
assert original.subs(x, 3) == 36
assert nroots((original-4)*(original+4), -S.oo) == 4
sys.path.insert(0, str(BUILD / '부교재_기말'))
import items_final as F
original_item = F.I['M27']
assert original_item[2] == '②' and S.sympify(original_item[1][1]) == 36
print('원문 M27: p=1, f(3)=36, 정답 ② 확인')

# 길이: HTML·수식 구분자 제거, sqrt/ge를 단일 기호로 치환하고 공백 정리.
text = it['body']+' '+ ' '.join(f'({label}) {v}' for label, v in it['cond'])
plain = html.unescape(re.sub(r'<[^>]*>', '', text))
plain = re.sub(r'\\[()\[\]]', '', plain)
plain = plain.replace(r'\sqrt', '√').replace(r'\ge', '≥')
plain = re.sub(r'\s+', ' ', plain).strip()
assert len(plain) >= 132
assert len(it['cond']) == 2
assert it['author'] == 'codex' and it['cand'] == 'codex17'
assert it['key'] == 'M27' and it['core']['axis'] == '①'
print(f'길이: {len(plain)}자 ≥ 132자(선지·해설 제외), 상자 조건 2개')
print('ALL OK')
