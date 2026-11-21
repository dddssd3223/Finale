"""이 폴더의 문항과 그림 정보만 이용하는 기호 검증."""
from pathlib import Path
import importlib.util
import re
import sympy as S

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('p17', HERE / 'p17.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
item = module.ITEMS[17]
x, t, r, a, b = S.symbols('x t r a b', real=True)
oo = S.oo
P = t**2 + a*t + b
av = -(5 + 2*b)/3
assert S.expand((P.subs(t, 1) + P.subs(t, 2)).subs(a, av)) == 0
assert S.simplify(P.subs({a: av, t: S.Rational(3, 2)})) == -S.Rational(1, 4)
assert S.simplify((a+b).subs(a, av) - (b-5)/3) == 0
# P(3/2)<0이고 최고차항 계수가 1이므로 모든 b에서 서로 다른 실근 r<3/2<s가 있다.
sv = (3*r - 5)/(2*r - 3)
assert S.simplify(2*r*sv - 3*r - 3*sv + 5) == 0
domain = S.Interval.open(-oo, S.Rational(3, 2))
assert S.solve_univariate_inequality(sv > S.Rational(3, 2), r, relational=False).intersect(domain) == domain

# 그래프에서 읽은 모든 높이 구간. 끝점의 포함 여부도 따로 검증한다.
levels = [
    (S.Interval(-oo, -1), 1),
    (S.Interval.Lopen(-1, 0), 2),
    (S.Interval.Lopen(0, 1), 3),
    (S.Interval.Lopen(1, 2), 2),
    (S.Interval.open(2, oo), 1),
]
assert S.Union(*(region for region, _ in levels)) == S.S.Reals

def N(value):
    matches = [n for region, n in levels if region.contains(value) == S.true]
    assert len(matches) == 1
    return matches[0]

assert [N(v) for v in [-1, 0, 1, 2]] == [1, 2, 3, 2]

def preimage(region):
    result = domain
    if region.start != -oo:
        rel = sv > region.start if region.left_open else sv >= region.start
        result = result.intersect(S.solve_univariate_inequality(rel, r, relational=False))
    if region.end != oo:
        rel = sv < region.end if region.right_open else sv <= region.end
        result = result.intersect(S.solve_univariate_inequality(rel, r, relational=False))
    return result

# 높이 구간의 조합 5×5개를 정확한 집합 연산으로 전수 검증한다.
cases = []
for r_region, nr in levels:
    for s_region, ns in levels:
        region = domain.intersect(r_region).intersect(preimage(s_region))
        if region != S.EmptySet:
            cases.append((region, nr + ns))
assert cases == [
    (S.Interval(-oo, -1), 3),
    (S.Interval.Lopen(-1, 0), 4),
    (S.Interval.Lopen(0, 1), 5),
    (S.Interval.open(1, S.Rational(3, 2)), 3),
]
assert S.Union(*(region for region, _ in cases)) == domain
for region, count in cases:
    print(f'CASE r in {region}: {count} roots')
valid = S.Union(*(region for region, count in cases if count == 5))
assert valid == S.Interval.Lopen(0, 1)

# b(r)는 연속이고 엄격히 증가한다. 전체 해가 0<b≤2를 빠짐없이 움직인다.
b_of_r = r*sv
positive_numerator = 2*(r-S.Rational(3, 2))**2 + S.Rational(1, 2)
assert S.simplify(S.diff(b_of_r, r) - 3*positive_numerator/(2*r-3)**2) == 0
assert S.limit(b_of_r, r, 0, dir='+') == 0
assert b_of_r.subs(r, 1) == 2
assert not valid.contains(S.Rational(3, 2))
objective = S.simplify(-r-sv+b_of_r)
assert S.simplify(objective - (b_of_r-5)/3) == 0
assert [root for root in S.solve(S.together(objective+1), r) if valid.contains(root)] == [1]
assert objective.subs(r, 1) == -1
assert N(1)+N(2) == 5
assert S.expand(P.subs({a: -3, b: 2})) == S.expand((t-1)*(t-2))
print('UNIQUE MAX: a=-3, b=2, a+b=-1; continuous range 0<b<=2')

choices = list(map(S.sympify, item['choices']))
assert len(choices) == 5
assert len(set(choices[i+1]-choices[i] for i in range(4))) == 1
assert choices.count(S.Integer(-1)) == 1
assert choices[item['ans']-1] == -1
# 해설에 적은 오답 발생 과정을 식으로 재현한다.
wrong = {
    'a만 답함': S.Integer(-3),
    'b를 작은 높이로 오인': S.Integer(-3)+1,
    'g(0)의 상수 1 누락': S.solve(S.Symbol('z'), S.Symbol('z'))[0],
    '이항 부호 오류': S.Integer(1),
}
assert set(wrong.values()) == set(choices)-{-1}
for reason, value in wrong.items():
    print(f'DISTRACTOR {value}: {reason}')

# 조건을 각각 삭제. 본문에는 함수 정의와 실수 계수 소개 외 추가 조건이 없다.
# (가) 삭제: (나)만 만족시키는 b=k, a=-(5+2k)/3에서 목적식은 무한 증가.
k = S.symbols('k', real=True)
assert S.simplify((P.subs(t, 1)+P.subs(t, 2)).subs({a: -(5+2*k)/3, b: k})) == 0
assert S.limit((k-5)/3, k, oo) == oo
print('ABLATION (가): 필요((나)만 있으면 a+b=(b-5)/3가 위로 유계가 아니므로 최댓값 없음)')
# (나) 삭제: r=e, s=-1+e (0<e<1)에서 5개, 목적식은 1-4e+e² → 1.
e = S.symbols('e', positive=True)
family_a, family_b = 1-2*e, e*(e-1)
assert S.expand((t-e)*(t+1-e) - P.subs({a: family_a, b: family_b})) == 0
assert N(S.Rational(1, 2))+N(-S.Rational(1, 2)) == 5
assert (family_a+family_b).subs(e, S.Rational(1, 2)) == -S.Rational(1, 4) > -1
print('ABLATION (나): 필요(a=0, b=-1/4이면 (가)를 만족하면서 a+b=-1/4>-1)')

# 원문: x=0의 좌우 극한에서 G(0)=0.
# x=1의 우극한은 G(1)/2이고 좌분모가 0으로 수렴하므로 G(1)=0.
# 가운데 분모의 1은 단순근이므로 공통 극한 0을 얻으려면 G'(1)=0.
c2, c1, c0 = S.symbols('c2 c1 c0')
G = x**3 + c2*x**2 + c1*x + c0
original_solutions = S.solve([G.subs(x, 0), G.subs(x, 1), S.diff(G, x).subs(x, 1)], [c2, c1, c0], dict=True)
assert original_solutions == [{c0: 0, c1: 1, c2: -2}]
G = S.factor(G.subs(original_solutions[0]))
assert G == x*(x-1)**2
# 중간 조각은 (x-1)(x²+u x-1), u≠0으로 일반화해 충분성까지 확인.
u = S.symbols('u', nonzero=True, real=True)
f_left = (x+3)*(x-3)/9
f_mid = (x-1)*(x*x+u*x-1)
f_right = -x+3
assert S.limit(G/f_left, x, 0, dir='-') == 0
assert S.limit(G/f_mid, x, 0, dir='+') == 0
assert S.limit(G/f_mid, x, 1, dir='-') == 0
assert S.limit(G/f_right, x, 1, dir='+') == 0
assert G.subs(x, 3) == 12
original = {}
exec((HERE/'original_L42.py').read_text(), {'I': original, 'FIG': lambda *args: ''})
assert original['L42'][2] == str(G.subs(x, 3))
print('ORIGINAL: G=x(x-1)^2, G(3)=12; necessary and sufficient')

# 제공 지침 범위의 자체 형식 검사. 외부 공식 검사기를 대체한다고 주장하지 않는다.
assert item['author'] == 'codex'
assert item['body'].startswith(r'함수 \(y=f(x)\)의 그래프가 그림과 같다.')
assert 'fig_L42.svg' in item['body'] and (HERE/'fig_L42.svg').exists()
assert len(item['cond']) == 2 and item['after'] == ''
assert '[5.2점]' in item['body']
for field in ['body', 'sol', 'fast', 'note', 'wrong']:
    assert not re.search(r'<(?!/?(?:div|img)\b)', item[field])
problem = item['body'] + ''.join(text for _, text in item['cond'])
assert not any(word in problem for word in ['속한다', '생각하자', '마다', '중근'])
print('LOCAL FORMAT: OK (공식 dupcheck/stylecheck/fmtcheck 미실행)')
print('ALL OK')
