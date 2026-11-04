# -*- coding: utf-8 -*-
"""I37 변형: 기호식으로 전 함수족을 분류하고 연속 매개변수 구간을 검증한다."""
from pathlib import Path
import html
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / '부교재_기말'))
import items_final as original
it = runpy.run_path(str(HERE / 'c17.py'))['ITEMS'][17]
x, r = s.symbols('x r', real=True)
a = s.symbols('a', positive=True)
R = s.Rational
BOUND = R(256, 3)

def abs_integral(p, end):
    lo, hi = sorted([s.S.Zero, end])
    roots = sorted(set(s.real_roots(p, x)))
    cuts = [lo] + [z for z in roots if lo < z < hi] + [hi]
    val = sum(s.sign(p.subs(x, (u+v)/2)) * s.integrate(p, (x, u, v))
              for u, v in zip(cuts, cuts[1:]))
    return s.simplify(val if end >= 0 else -val)

def cost(p, end):
    return s.simplify(abs(s.integrate(p, (x, 0, end))) + abs_integral(p, end))

def two_roots(p, end):
    return len(set(s.real_roots(s.integrate(p, (x, end, x)), x))) == 2

# 모든 이차함수는 아래 둘 중 한 부호이다. a>1이므로 판별식의 a 인자는 0이 아니다.
base = 4*x*(x-r)
F = s.integrate(base, (x, a, x))
assert s.factor(s.discriminant(F, x)) == 64*a**2*(-2*a+3*r)*(r-a)**2*(2*a+r)/3
roots = s.solve(s.discriminant(F, x), r)
assert set(roots) == {2*a/3, a, -2*a}
assert len(set(roots)) == 3
families = [(2*a/3, R(32,81), 6), (a, R(4,3), 4), (-2*a, R(32,3), 2)]
minima = []
attainers = []
for root, coefficient, upper in families:
    for sign in [1, -1]:
        f = s.expand(sign*base.subs(r, root))
        ff = s.factor(s.integrate(f, (x, a, x)))
        # a>1에서 근은 두 개이다. 각 근의 차수도 확인하여 한 근만 남는 경우를 제외한다.
        rr = s.roots(ff, x)
        assert sorted(rr.values()) == [1, 2]
        if root == 2*a/3:
            area = -s.integrate(base.subs(r, root), (x, 0, root)) + s.integrate(base.subs(r, root), (x, root, a))
        else:
            area = abs(s.integrate(base.subs(r, root), (x, 0, a)))
        c = s.simplify(abs(s.integrate(f, (x, 0, a))) + area)
        assert s.simplify(c - coefficient*a**3) == 0
        assert coefficient*upper**3 == BOUND
        # a^3는 a>1에서 엄격히 증가하므로 이 범위가 필요충분하다.
        assert s.diff(c, a).is_positive
        value = f.subs(x, 1)
        slope = s.diff(value, a)
        assert slope != 0 and not slope.has(a)
        end = upper if slope < 0 else 1
        infimum = s.simplify(value.subs(a, end))
        assert infimum >= -20
        minima.append(infimum)
        if infimum == -20:
            assert slope < 0  # 열린 아래끝의 하한을 최솟값으로 오인하지 않는다.
            attainers.append((s.expand(f.subs(a, end)), end))
        print(f'FAMILY r={root}, sign={sign}: F={ff}, 1<a<={upper}, f(1)의 하한={infimum}')
assert min(minima) == -20
assert attainers == [(-4*x**2-16*x, 2)]
fstar, astar = attainers[0]
assert two_roots(fstar, astar) and cost(fstar, astar) == BOUND
assert fstar.subs(x, 1) == -20

# 정답·선지 및 실제 계산으로 재현되는 오답.
choices = list(map(s.sympify, it['choices']))
assert len(choices) == len(set(choices)) == 5
assert len(set(choices[j+1]-choices[j] for j in range(4))) == 1
assert it['ans'] == 4 and choices[3] == -20
wrong = {
    -8: 4*(1-R(6,2)),             # 첫 가족의 r를 a/2로 오인
    -12: (4*x*(x-4)).subs(x, 1),  # r=a 가족만 남김
    -16: (-16*x).subs(x, 1),      # 최종 함수의 이차항 누락
    -24: s.diff(fstar,x).subs(x,1) # 함숫값 대신 미분계수
}
assert all(k == v and k in choices and k != -20 for k,v in wrong.items())
assert set(wrong) == set(choices)-{-20}
print('CHOICES 정답 ④ -20, 공차 -4, 오답 4개 계산 OK')

# 조건마다 다른 답을 주는 정확한 반례. 지우지 않은 조건은 모두 재검산한다.
def ablation(label, p, end, omitted):
    checks = {
        '이차함수': s.degree(p,x) == 2,
        '최고차항': abs(s.LC(s.Poly(p,x))) == 4,
        'f(0)=0': p.subs(x,0) == 0,
        'a>1': end > 1,
        '(가)': two_roots(p,end),
        '(나)': cost(p,end) <= BOUND,
    }
    assert all(v for k,v in checks.items() if k != omitted), (label, checks)
    assert not checks[omitted]
    assert p.subs(x,1) < -20
    print(f'ABLATION 17 {label}: 필요(f={s.factor(p)}, a={end}, f(1)={p.subs(x,1)}, 비용={cost(p,end)})')

ablation('(가) 두 실근', -4*x*(x+8), R(3,2), '(가)')
ablation('(나) 넓이 상한', -4*x*(x+6), s.Integer(3), '(나)')
ablation('a>1', -4*x*(x+6), s.Integer(-9), 'a>1')
ablation('f(0)=0', -4*(x+5)*(x+R(13,15)), R(6,5), 'f(0)=0')
ablation('최고차항 계수의 절댓값 4', -12*x*(x+R(8,3)), R(4,3), '최고차항')
ablation('이차함수', 4*x*(x*x-R(25,4)), R(5,2), '이차함수')

# 원문은 두 구간의 부호가 달라지는 1이 영점이므로 이 함수만 남는다.
fo = -4*x*(x-1)
assert fo.subs(x,R(1,2)) > 0 and fo.subs(x,2) < 0
P = s.integrate(fo,(x,0,a))
assert s.simplify(s.integrate(fo,(x,1-a,1))-P) == 0
assert s.factor(P) == -2*a*a*(2*a-3)/3
# |P|<=P ⇔ P>=0, a>1에서 a<=3/2. f는 이 구간에서 감소.
assert s.diff(fo,x).subs(x,a).subs(a,1) < 0
assert fo.subs(x,R(3,2)) == -3
assert original.I['I37'][2] == '②' and original.I['I37'][1][1] == '-3'
print('ORIGINAL I37 정답 ② -3 OK')

# HTML와 수식 구분자만 제거, TeX 명령·공백은 보존하는 재현 가능한 길이.
def length(t):
    t = html.unescape(re.sub(r'<[^>]*>', '', t))
    t = re.sub(r'\\[()\[\]]', '', t)
    return len(re.sub(r'\s+', ' ', t).strip())
text = it['body'] + ''.join('('+k+')'+v for k,v in it['cond'])
old_len, new_len = length(original.I['I37'][0]), length(text)
assert new_len >= old_len and new_len >= 265
assert it['author'] == 'codex' and it['cand'] == 'codex17'
assert it['core']['axis'] == '①'
print(f'LENGTH 동일 기준 원문 {old_len}자 → 변형 {new_len}자; 지시서 265자 이상 OK')
print('ALL OK')
