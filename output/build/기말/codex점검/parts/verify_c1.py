# -*- coding: utf-8 -*-
"""1번: 정답·유일성·등차 선지·모든 오답 근거·I49 원문 정답 검증."""
from pathlib import Path
import re
import runpy
import sys

from sympy import diff, integrate, simplify, solve, symbols, sympify

HERE = Path(__file__).resolve().parent
items = runpy.run_path(str(HERE / 'c1.py'))['ITEMS']
assert set(items) == {1}
item = items[1]
assert item['author'] == 'codex' and item['key'] == 'I49'
assert item['level'] == '하' and item['ans'] == 3

# 검증식이 실제 문항의 도함수·초깃값·질문과 일치하는지 확인한다.
body = item['body']
derivative_text = re.search(r"f'\(x\)=([^\\]+)\\\)", body).group(1)
initial_text = re.search(r'f\(0\)=([^\\]+)\\\)', body).group(1)
assert r'\(f(1)\)의 값은?' in body
x, C = symbols('x C', real=True)
derivative = sympify(re.sub(r'(\d)x', r'\1*x', derivative_text), locals={'x': x}, convert_xor=True)
initial = sympify(initial_text)
primitive = integrate(derivative, x) + C
constants = solve(primitive.subs(x, 0) - initial, C)
assert len(constants) == 1
f = primitive.subs(C, constants[0])
assert simplify(diff(f, x) - derivative) == 0
assert f.subs(x, 0) == initial
answer = f.subs(x, 1)
assert answer == initial + integrate(derivative, (x, 0, 1)) == 8
print(f'정답·유일성: f(x)={f}, f(1)={answer}, 적분상수 후보={constants} OK')

choices = [sympify(c) for c in item['choices']]
assert len(choices) == len(set(choices)) == 5
assert len(set(choices[i + 1] - choices[i] for i in range(4))) == 1
assert choices[1] - choices[0] == 2
assert [i + 1 for i, v in enumerate(choices) if v == answer] == [3]
print('선지: 4, 6, 8, 10, 12 / 공차 2 / 정답 ③ OK')

wrong_values = {
    1: initial + integrate(derivative - derivative.subs(x, 0), (x, 0, 1)),
    2: integrate(derivative, (x, 0, 1)),
    4: 2 * initial + integrate(derivative, (x, 0, 1)),
    5: initial + derivative.subs(x, 1),
}
labels = {1: '①', 2: '②', 4: '④', 5: '⑤'}
for pos, value in wrong_values.items():
    assert value == choices[pos - 1] and value != answer
    assert f'{labels[pos]} \\({value}\\)' in item['wrong']
print(f'모든 오답 근거·선지 일치: {wrong_values} OK')

# 원문은 저장소의 원문 데이터에서 읽고, 해답은 별도로 직접 적분한다.
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F

original_body, original_choices, original_answer, original_source = F.I['I49']
original_body = original_body.replace('\\\\', '\\')
original_derivative_text = re.search(r"f'\(x\)=([^\\]+)\\\)", original_body).group(1)
original_initial_text = re.search(r'f\(0\)=([^\\]+)\\\)', original_body).group(1)
assert r'\(f(1)\)' in original_body
original_derivative = sympify(re.sub(r'(\d)x', r'\1*x', original_derivative_text), locals={'x': x}, convert_xor=True)
original_initial = sympify(original_initial_text)
original_value = original_initial + integrate(original_derivative, (x, 0, 1))
assert original_choices is None
assert original_value == sympify(original_answer) == 10
assert item['src'] == original_source
print(f'I49 원문 직접 풀이: {original_value}, 등록 정답과 일치 OK')
print('ALL OK')
