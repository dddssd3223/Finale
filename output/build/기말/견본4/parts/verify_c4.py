# -*- coding: utf-8 -*-
"""서답형1: 위치·거리, 채점 배점, 오답, 원문, 조건 빼 보기."""
from pathlib import Path
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
SI = runpy.run_path(str(HERE / 'c4.py'))['SITEMS']
assert set(SI) == {'S1'}
it = SI['S1']
assert it['author'] == 'codex' and it['src'] == '학교 자체 출제'
assert [sub[1] for sub in it['subs']] == ['4점, 풀이과정을 상세히 쓰시오.', '6점, 풀이과정을 상세히 쓰시오.']
assert len(it['ans']) == len(it['sol']) == 2 and len(it['rubric']) == 3
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F
t = s.symbols('t', real=True)
v = t*t-4*t+3
assert s.factor(v) == (t-1)*(t-3)
assert s.solve(v, t) == [1, 3]
position = s.integrate(v, (t, 0, 1))
displacement = s.integrate(v, (t, 0, 2))
distance = s.integrate(v, (t, 0, 1))-s.integrate(v, (t, 1, 2))
assert position == s.Rational(4, 3) and displacement == s.Rational(2, 3)
assert distance == s.integrate(s.Abs(v), (t, 0, 2)) == 2
assert s.sign(v.subs(t, s.Rational(1, 2))) == 1
assert s.sign(v.subs(t, s.Rational(3, 2))) == -1
assert it['ans'] == [r'(1) \(\dfrac43\)', r'(2) \(2\)']
# 미분식과 초기 위치는 원시함수의 상수까지 유일하게 결정한다.
C = s.symbols('C')
X = s.integrate(v, t)+C
initial_C = s.solve(X.subs(t, 0), C)
assert initial_C == [0]
assert s.diff(X.subs(C, 0), t) == v
wrong_p = v.subs(t, 0)
wrong_long = s.integrate(v, (t, 0, 1))-s.integrate(v, (t, 1, 3))
assert wrong_p == 3 and wrong_long == s.Rational(8, 3)
print(f'S1: unique position={position}, distance={distance}; wrong values={wrong_p}, {displacement}, {position}, {wrong_long}: OK')

# 초기 위치를 지우면 (1)이 바뀐다. 다른 조건은 모두 유지된다.
assert 1+position == s.Rational(7, 3) != position
print('ABLATION S1 원점 출발: 필요(초기 위치1이면 (1)은 7/3, 거리는2)')
# 속도식을 지우면 원점 출발을 만족하는 v=1도 가능하다.
alternative_position = s.integrate(1, (t, 0, 1))
assert alternative_position == 1 != position
print('ABLATION S1 속도식: 필요(v=1이면 (1)은1, (2)는2)')
# 질문 구간 경계의 역할도 별도로 검사한다.
assert wrong_long != distance
print('BOUNDARY S1: 종료 시각3이면 거리8/3, 종료 시각2이면 거리2')

# 원문 J72의 세 보기 참·거짓을 각각 독립 계산한다.
vo_a = t*t+4
claim_a = s.integrate(vo_a, (t, 0, 1)) == s.Rational(13, 3)
vo_b = t*t-3*t+4
assert s.discriminant(vo_b, t) == -7
claim_b = False  # 항상 양수: 방향 전환0회
vo_c = t*t-5*t+4
assert s.factor(vo_c) == (t-1)*(t-4)
claim_c = s.integrate(vo_c, (t, 0, 1))-s.integrate(vo_c, (t, 1, 2)) == 3
assert (claim_a, claim_b, claim_c) == (True, False, True)
assert F.I['J72'][2] == '③'
print('ORIGINAL J72: ㄱ=True, ㄴ=False, ㄷ=True, stored answer ③: OK')
print('ALL OK')
