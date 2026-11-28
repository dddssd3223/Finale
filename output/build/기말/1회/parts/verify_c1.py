# -*- coding: utf-8 -*-
"""2·4·6·8번: 정답, 유일성, 경계, 선지, 오답 근거, 원문 정답.

실행 위치에 관계없이 python3 verify_c1.py로 실행한다.
"""
from pathlib import Path
import re
import runpy
import sys
import sympy as S

HERE = Path(__file__).resolve().parent
IT = runpy.run_path(str(HERE / 'c1.py'))['ITEMS']
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as F

x, t, a = S.symbols('x t a', real=True)
WANT = {2: 5, 4: 4, 6: 5, 8: 1}
assert set(IT) == set(WANT)


def number(text):
    m = re.fullmatch(r'(-?)\\(?:dfrac|frac)\{?(\d+)\}?\{?(\d+)\}?', str(text))
    if m:
        return (-1 if m[1] else 1) * S.Rational(m[2], m[3])
    return S.sympify(text)


def check(no, value, wrong_values):
    it = IT[no]
    ch = list(map(number, it['choices']))
    assert len(ch) == len(set(ch)) == 5
    assert len({ch[j+1] - ch[j] for j in range(4)}) == 1
    assert ch[1] - ch[0] == 1
    assert it['ans'] == WANT[no]
    assert value == ch[it['ans']-1]
    assert ch.count(value) == 1
    assert set(map(number, it['wrong'])) == set(wrong_values)
    assert all(w in ch and w != value for w in wrong_values)
    assert it['author'] == 'codex' and it['bunseok'] is False
    assert it['effect'] in ('같음', '쉬워짐')
    print(f'{no}: 답 {value}, 정답 {it["ans"]}, 유일성·등차·오답 근거 OK')


def original(key, computed):
    _, choices, answer, _ = F.I[key]
    value = number(choices['①②③④⑤'.index(answer)]) if choices else number(answer)
    assert computed == value, (key, computed, value)
    print(f'ORIGINAL {key}: {computed} = 원문 정답 OK')


# 2: 이차 도함수의 최솟값으로 필요충분조건을 직접 확인한다.
assert r'f(x)=x^3+3ax^2+(6a+9)x+2' in IT[2]['body']
f2 = x**3 + 3*a*x**2 + (6*a+9)*x + 2
d2 = S.diff(f2, x)
minimum = S.factor(d2.subs(x, -a))
assert S.expand(minimum + 3*(a-3)*(a+1)) == 0
allowed = S.solve_univariate_inequality(minimum >= 0, a, relational=False)
assert allowed == S.Interval(-1, 3)
assert S.factor(d2.subs(a, 3)) == 3*(x+3)**2
# 등호일 때에도 상수 함수 구간이 없으므로 엄격한 증가이다.
assert S.degree(d2.subs(a, 3), x) == 2
check(2, allowed.end, [allowed.start, S.ceiling(allowed.end)-1])
fo = x**3 + a*x**2 + (2*a+S.Rational(7, 3))*x - 5
disc = S.discriminant(S.diff(fo, x), x)
interval = S.solve_univariate_inequality(disc <= 0, a, relational=False)
assert interval == S.Interval(-1, 7)
original('D11', S.floor(interval.end)-S.ceiling(interval.start)+1)

# 4: 속도 일치의 모든 실근 중 시간 조건을 만족하는 것을 전수 확인한다.
assert r'x_1=t^3-t^2+2t' in IT[4]['body']
assert r'x_2=2t^2+11t+1' in IT[4]['body']
p, q = t**3-t**2+2*t, 2*t**2+11*t+1
roots = S.solve(S.diff(p-q, t), t)
assert roots == [-1, 3]
times = [r for r in roots if r >= 0]
assert times == [3]
distance = abs((p-q).subs(t, times[0]))
omitted_constant = abs((p-(q-1)).subs(t, times[0]))
assert omitted_constant == 27
check(4, distance, [omitted_constant])
po, qo = t**3-2*t**2+3*t, t**2+12*t
ro = [r for r in S.solve(S.diff(po-qo, t), t) if r >= 0]
assert ro == [3]
original('M48', abs((po-qo).subs(t, ro[0])))

# 6: 모든 임계점과 양 끝의 극한을 비교하고 인수분해로 전역 상한을 재확인한다.
assert r'f(x)=-x^4+3x^3-x^2+1' in IT[6]['body']
f6 = -x**4 + 3*x**3 - x**2 + 1
critical = S.solve(S.diff(f6, x), x)
assert critical == [0, S.Rational(1, 4), 2]
values = [f6.subs(x, c) for c in critical]
assert values == [1, S.Rational(251, 256), 5]
assert S.limit(f6, x, S.oo) == S.limit(f6, x, -S.oo) == -S.oo
assert S.expand(5-f6-(x-2)**2*(x*x+x+1)) == 0
assert S.discriminant(x*x+x+1, x) < 0
maximum = max(values)
wrong6 = 2*(maximum-1)
assert wrong6 == 8
check(6, 2*maximum, [wrong6])
fo = x**4-3*x**3+x**2
assert S.limit(fo, x, S.oo) == S.limit(fo, x, -S.oo) == S.oo
original('M16', 2*min(fo.subs(x, c) for c in S.solve(S.diff(fo, x), x)))

# 8: v(0)>0, 유일한 내부 극소점, 등호일 때의 부호를 기호 계산으로 확인한다.
assert r'v(t)=4t^3-12at^2+16a' in IT[8]['body']
v = 4*t**3-12*a*t**2+16*a
assert S.factor(S.diff(v, t)) == 12*t*(t-2*a)
minimum = S.factor(v.subs(t, 2*a))
assert S.expand(minimum + 16*a*(a-1)*(a+1)) == 0
allowed = S.solve_univariate_inequality(minimum >= 0, a, relational=False).intersect(S.Interval.open(0, S.oo))
assert allowed == S.Interval.Lopen(0, 1)
assert S.factor(v.subs(a, 1)) == 4*(t-2)**2*(t+1)
distance = S.integrate(v, (t, 0, 1))
assert distance == 12*a+1 and S.diff(distance, a) > 0
wrong8 = v.subs({a: 1, t: 0})
assert wrong8 == 16
check(8, distance.subs(a, allowed.end), [wrong8])
vo = t**3/3-a*t**2+3*a
assert S.factor(S.diff(vo, t)) == t*(t-2*a)
old_allowed = S.solve_univariate_inequality(vo.subs(t, 2*a) >= 0, a, relational=False).intersect(S.Interval.open(0, S.oo))
assert old_allowed == S.Interval.Lopen(0, S.Rational(3, 2))
old_distance = S.integrate(vo, (t, 0, 2))
assert S.diff(old_distance, a) > 0
original('J30', old_distance.subs(a, old_allowed.end))

print('ALL OK')
