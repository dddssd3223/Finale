"""L42 변형 17번: 정확한 유리수와 구간별 다항식으로 전수 검증한다."""
from pathlib import Path
import re
import sympy as sp

from p17 import ITEMS, DESIGN


a, b, x = sp.symbols('a b x', real=True)
J0 = sp.Abs(-1-a) - sp.Abs(1-a) - 2*b  # 0에서 좌극한 - 함숫값
J1 = sp.Abs(-a) - sp.Abs(2-a) - 2*b    # 1에서 좌극한 - 함숫값
NUM = sp.Abs(1-a) - sp.Abs(2-a) - b + 1


def discontinuities(av, bv):
    return sum(sp.simplify(j.subs({a: av, b: bv})) != 0 for j in (J0, J1))


# 모든 절댓값의 부호가 고정되는 열린구간과 모든 경계점을 따로 검사한다.
cuts = [-sp.oo, -1, 0, 1, 2, sp.oo]
cells = []
for left, right in zip(cuts, cuts[1:]):
    sample = right-1 if left == -sp.oo else left+1 if right == sp.oo else (sp.Rational(left)+right)/2
    cells.append((sp.Interval.open(left, right), sample))
    if right != sp.oo:
        cells.append((sp.FiniteSet(right), sp.Integer(right)))
assert sp.Union(*(cell for cell, _ in cells)) == sp.S.Reals


def on_cell(expr, cell, sample):
    if isinstance(cell, sp.FiniteSet):
        return sp.simplify(expr.subs(a, sample))
    replacements = {}
    for term in expr.atoms(sp.Abs):
        inner = term.args[0]
        # 구간 내부에 절댓값 내부 식의 영점이 없는지도 확인한다.
        roots = sp.solveset(inner, a, domain=sp.S.Reals)
        assert sp.Intersection(roots, cell) == sp.EmptySet
        replacements[term] = sp.sign(inner.subs(a, sample))*inner
    return sp.expand(expr.xreplace(replacements))


solutions = set()
for cell, sample in cells:
    equation = on_cell(NUM, cell, sample)
    b_value, = sp.solve(equation, b)
    jumps = [sp.simplify(on_cell(j, cell, sample).subs(b, b_value)) for j in (J0, J1)]
    if isinstance(cell, sp.FiniteSet):
        candidates = {sample}
    else:
        # 둘 중 하나가 0이어야 하므로, 두 일차식의 모든 영점을 후보로 잡는다.
        assert all(j != 0 for j in jumps), '구간 전체가 해가 되는 경우를 별도 처리해야 함'
        candidates = set()
        for j in jumps:
            roots = sp.solveset(j, a, domain=cell)
            assert roots == sp.EmptySet or isinstance(roots, sp.FiniteSet)
            candidates.update(roots)
    found = []
    for av in candidates:
        bv = sp.simplify(b_value.subs(a, av))
        assert sp.simplify(NUM.subs({a: av, b: bv})) == 0
        if discontinuities(av, bv) == 1:
            solutions.add((av, bv))
            found.append((av, bv))
    print(f'CASE {cell}: b={b_value}; jumps={jumps}; solutions={sorted(found)}')

expected = {(sp.Integer(0), sp.Integer(0)), (sp.Integer(1), sp.Integer(0)), (sp.Rational(3, 2), sp.Integer(1))}
assert solutions == expected
values = {2*av+1 for av, _ in solutions}
assert values == {1, 3, 4}
answer = sum(values)
assert answer == 8
print(f'UNIQUE ANSWER: pairs={sorted(solutions)}, values={sorted(values)}, sum={answer}')

# f는 그림의 0, 1 이외에서 연속이고 절댓값과 선형결합은 연속성을 보존한다.
# 그림의 특성을 만족시키는 삼차 조각의 한 예로 극한 계산도 교차 확인한다.
# 전수 증명 자체는 위에서 조각의 구체적인 식과 무관하게 수행했다.
f_left = (x+3)*(x-3)/9
f_mid = x**3-2*x**2+1
f_right = -x+3
assert f_mid.subs(x, 0) == 1 and f_mid.subs(x, 1) == 0
assert sp.discriminant(f_mid, x) != 0
for av, bv in solutions:
    def transformed(expr):
        return sp.Abs(expr-av)+bv*expr
    l0 = sp.limit(transformed(f_left), x, 0, dir='-')
    r0 = sp.limit(transformed(f_mid), x, 0, dir='+')
    l1 = sp.limit(transformed(f_mid), x, 1, dir='-')
    r1 = sp.limit(transformed(f_right), x, 1, dir='+')
    g0 = transformed(sp.Integer(1))
    g1 = transformed(sp.Integer(2))
    assert r0 == g0 and r1 == g1
    assert int(l0 != g0)+int(l1 != g1) == 1
    assert g0-g1 == -1
print('LIMITS: all solution pairs checked at 0 and 1')

# (가)를 지우면 모든 실수 a에 대해 b를 정할 수 있다.
b_without_count = 1+sp.Abs(1-a)-sp.Abs(2-a)
assert sp.simplify(NUM.subs(b, b_without_count)) == 0
for av in [-2, -1, 2, 3]:
    bv = b_without_count.subs(a, av)
    assert discontinuities(av, bv) == 2
assert sp.limit(2*a+1, a, sp.oo) == sp.oo
print('ABLATION (가): 필요(삭제하면 모든 실수 a가 가능하여 유한한 값의 합이 정해지지 않음)')

# (나)를 지우면 0<a<1, b=a에서 연속점은 0, 불연속점은 1이다.
unit_interval = sp.Interval.open(0, 1)
assert on_cell(J0.subs(b, a), unit_interval, sp.Rational(1, 2)) == 0
assert on_cell(J1.subs(b, a), unit_interval, sp.Rational(1, 2)) == -2
assert on_cell(NUM.subs(b, a), unit_interval, sp.Rational(1, 2)) == -a
assert sp.solveset(2*a+1-x, a) == sp.FiniteSet((x-1)/2)
print('ABLATION (나): 필요(삭제하면 0<a<1, b=a가 모두 가능하여 유한한 값의 합이 정해지지 않음)')
print('BODY: a,b는 실수인 매개변수이며 추가 범위·부호·정수 조건 없음; 그래프와 g의 식은 정의 자료')

# 원문: 중간 조각의 1에서의 기울기를 0이 아닌 기호 k로 둔다.
# 원문의 세 인수가 서로 다르고 1이 영점이므로 k != 0이다.
u, v, w = sp.symbols('u v w', real=True)
k = sp.symbols('k', real=True, nonzero=True)
original_g = x**3+u*x**2+v*x+w
original_mid = x**3+(k-1)*x**2-(k+1)*x+1
assert original_mid.subs(x, 0) == 1
assert original_mid.subs(x, 1) == 0
assert sp.diff(original_mid, x).subs(x, 1) == k
l0 = sp.limit(original_g/f_left, x, 0, dir='-')
r0 = sp.limit(original_g/original_mid, x, 0, dir='+')
assert sp.solve(l0-r0, w) == [0]
g_after_zero = original_g.subs(w, 0)
assert sp.solve(g_after_zero.subs(x, 1), v) == [-u-1]
g_after_one = g_after_zero.subs(v, -u-1)
l1 = sp.limit(sp.cancel(g_after_one/original_mid), x, 1, dir='-')
r1 = sp.limit(g_after_one/f_right, x, 1, dir='+')
assert sp.simplify(l1-(u+2)/k) == 0 and r1 == 0
assert sp.solve(l1-r1, u) == [-2]
original_answer_g = sp.factor(g_after_one.subs(u, -2))
assert original_answer_g == x*(x-1)**2
assert original_answer_g.subs(x, 3) == 12
# 그림에서 (-3,3) 내부에는 분모의 영점이 없고 1의 좌극한만 0이다.
assert sp.solveset(f_left, x, domain=sp.Interval.open(-3, 0)) == sp.EmptySet
assert sp.solveset(f_mid, x, domain=sp.Interval.Ropen(0, 1)) == sp.EmptySet
assert sp.solveset(f_right, x, domain=sp.Interval.Ropen(1, 3)) == sp.EmptySet
print('ORIGINAL: g(0)=0, g(1)=0, g\'(1)=0; g(x)=x(x-1)^2; g(3)=12')

item = ITEMS[17]
choices = [sp.Rational(c) for c in item['choices']]
assert len(choices) == 5 and len(set(choices)) == 5
assert len(set(choices[i+1]-choices[i] for i in range(4))) == 1
assert choices.count(answer) == 1 and choices[item['ans']-1] == answer
wrong_values = {
    '1<a<2 경우 누락': sum(2*av+1 for av in [0, 1]),
    '경계 a=1 제외': sum(2*av+1 for av in [0, sp.Rational(3, 2)]),
    '상수항을 한 번만 합함': 2*sum(av for av, _ in solutions)+1,
    'a=0 누락': sum(2*av+1 for av in [1, sp.Rational(3, 2)]),
}
assert set(wrong_values.values()) == set(choices)-{answer}
for reason, value in wrong_values.items():
    print(f'DISTRACTOR {value}: {reason}')
print('CHOICES: 4, 5, 6, 7, 8; common difference 1; answer index 5')

# 이 폴더에서 수행할 수 있는 형식·말투 확인. 공식 검사 도구를 대신한 점수는 내지 않는다.
assert item['author'] == 'codex' and item['key'] == 'L42'
assert item['body'].startswith(r'함수 \(y=f(x)\)의 그래프가 그림과 같다.')
assert 'fig_L42.svg' in item['body'] and Path(__file__).with_name('fig_L42.svg').is_file()
assert '[5.2점]' in item['body'] and item['body'].rstrip().endswith('[5.2점]')
assert item['after'] == '' and len(item['cond']) == 2
student_text = item['body']+' '.join(text for _, text in item['cond'])
for word in ['속한다', '생각하자', '마다', '중근']:
    assert word not in student_text
for field in ['body', 'sol', 'fast', 'note', 'wrong']:
    text = item[field]
    text_without_tags = re.sub(r'</?(?:div|img|br)\b[^>]*>', '', text)
    assert '<' not in text_without_tags, f'{field}: 이스케이프하지 않은 부등호'
assert DESIGN['unchanged_steps'] == 0
print('LOCAL FORMAT: figure, opening, score, two conditions, arithmetic choices, wording, HTML OK')
print('ALL OK')
