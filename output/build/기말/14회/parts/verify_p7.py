# -*- coding: utf-8 -*-
# 서답형1 (자체, D16 방향) 검증 · author='claude'
import sympy as sp, os, sys, re, itertools
x, a, b, r1, r2 = sp.symbols('x a b r1 r2', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1 = ns['SITEMS']['S1']
assert set(ns['SITEMS']) == {'S1'}
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

# --- 원문 D16: 정수 계수, (-2,1) 감소, (1,2) 증가 → f(3)-f(2) 최솟값 22 (원문 표기 ② 24는 전사 오류, DB 메모와 같음)
best = None
for A in range(-30, 31):
    for B in range(-60, 61):
        g = lambda t: 3 * t * t + 2 * A * t + B
        ok = g(1) == 0 and all(g(i / 10) <= 0 for i in range(-19, 10)) and all(g(i / 10) >= 0 for i in range(11, 20))
        if ok:
            v = 19 + 5 * A + B
            best = v if best is None else min(best, v)
assert best == 22 and F.I['D16'][1] == ['22', '24', '26', '28', '30']
print('D16 원문 OK: 최솟값 22')

# --- S1
assert r"f(x)=x^3+ax^2+bx" in S1['body']
f = x**3 + a * x**2 + b * x
fp = sp.diff(f, x)

from fractions import Fraction as Fr
GA = [Fr(i, 20) for i in range(-79, 40)] + [2 - Fr(1, 10**k) for k in range(2, 7)] + [-4 + Fr(1, 10**k) for k in range(2, 7)]
NA = [Fr(i, 20) for i in range(41, 60)] + [2 + Fr(1, 10**k) for k in range(2, 7)]
def cond_ok(fpv, ga=True, na=True):
    """(가) (-4,2)에서 감소 ⇔ f'<=0 (등호 고립), (나) (2,3)에서 증가 ⇔ f'>=0. 격자 검사(정확한 유리수)"""
    c2, c1, c0 = [Fr(str(sp.Poly(fpv, x).coeff_monomial(x**k))) for k in (2, 1, 0)]
    g = lambda t: c2 * t * t + c1 * t + c0
    if ga and any(g(t) > 0 for t in GA): return False
    if na and any(g(t) < 0 for t in NA): return False
    return True

# (1) 조건 ⇒ f'(2)=0 : 실수 계수 격자 전수에서 조건을 만족시키는 (a,b)는 모두 b=-4a-12
sols = []
for A2 in range(-20, 41):          # a = A2/2
    for B in range(-150, 151):
        av = sp.Rational(A2, 2)
        if cond_ok(fp.subs({a: av, b: B})): sols.append((av, B))
assert sols and all(B == -4 * av - 12 for av, B in sols)
assert sp.solve(fp.subs(x, 2), b) == [-4 * a - 12]
print('S1 (1) OK: b=-4a-12 (격자', len(sols), '개 모두)')

# (2) b=-4a-12 대입 → 인수분해, a>=3, f(4)-f(2)=4a+32, 최솟값 44
fpb = fp.subs(b, -4 * a - 12)
assert sp.expand(fpb - (x - 2) * (3 * x + 2 * a + 6)) == 0
assert min(av for av, _ in sols) == 3
for av in [sp.Rational(k, 4) for k in range(-20, 60)]:
    assert cond_ok(fpb.subs(a, av)) == (av >= 3), av
D = sp.expand((f.subs(x, 4) - f.subs(x, 2)).subs(b, -4 * a - 12))
assert D == 4 * a + 32
ans2 = D.subs(a, 3); assert ans2 == 44
assert min(56 + 12 * av + 2 * B for av, B in sols) == 44
print('S1 (2) OK: a>=3, f(4)-f(2)=4a+32, 최솟값 44')

assert S1['ans'] == [r'(1) \(b=-4a-12\)', r'(2) \(44\)']
txt = S1['body'] + ''.join(c[1] for c in S1['cond']) + ''.join(q[0] for q in S1['subs'])
assert '44' not in set(re.findall(r'\d+', txt))

# 오답 값
assert sp.solve(f.subs(x, 2), b) == [-2 * a - 4]                       # f(2)=0 착각
assert D.subs(a, 0) == 32                                              # 다른 근 -2 착각 → a=0
assert sp.solve(sp.Eq(-(2 * a + 6) / 3, -2), a) == [0]
for w in (r'b=-2a-4', r'\(32\)', r'a\le3', '최솟값이 없다'): assert w in S1['wrong'], w

# 빼 보기
def abl(cn, m_): print(f'ABLATION S1 {cn}: {m_}')
# (나) 빼기: f'=3(x-r1)(x-r2), r1<=-4, r2>=2 이면 (가) 성립. r2>4이면 f(4)-f(2)는 얼마든지 작아짐
G = sp.integrate(3 * (x - r1) * (x - r2), (x, 2, 4))
vals = [G.subs({r1: -4, r2: t}) for t in (2, 5, 10, 100)]
assert vals[0] == 44 and vals[-1] < -1000 and all(vals[i] > vals[i + 1] for i in range(3))
fp_t = 3 * (x + 4) * (x - 10)
assert cond_ok(sp.expand(fp_t), True, False) and not cond_ok(sp.expand(fp_t), True, True)
abl('(나) 증가 조건', '필요(빼면 x=2가 경계가 아니어서 f(4)-f(2)가 한없이 작아짐, 최솟값 없음)')
# (가) 빼기: b=-4a-12만 남기 위해 (나)만으로는 f'(2)=0 이 강제되지 않음 + a 아래로 열림
assert cond_ok(sp.expand(3 * (x - 1) * (x - 2) + 0), False, True) is True    # 다른 근 1도 허용 → a=-9/2
assert D.subs(a, -sp.Rational(9, 2)) < 44
abl('(가) 감소 조건', '필요(빼면 a가 아래로 열려 4a+32가 44보다 작아짐 — 예 a=-9/2에서 14)')
# 감소 구간 왼끝 -4: 바꾸면 답이 바뀜
abl('감소 구간 왼끝 -4', '필요(-2이면 a>=0, 최솟값 32)')

# 배점·형식
assert len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2 and len(S1['cond']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts] == [5, 5], pts
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D16)' and S1['key'] == 'D16' and S1['bunseok'] is False
assert '이러한' not in txt and '이와 같은' not in txt
flds = [S1['body']] + [c[1] for c in S1['cond']] + [q[0] for q in S1['subs']] + S1['rubric'] + S1['sol'] + \
       [S1['fast'], S1['wrong'], S1['note'], S1['var']] + S1['ans']
for fld in flds:
    for m in re.findall(r'\\\(.*?\\\)', fld, re.S): assert '<' not in m and '>' not in m, m
    for m in re.findall(r'\\\[.*?\\\]', fld, re.S): assert '<' not in m and '>' not in m, m
for bad in ['D33', 'D34', 'D37', 'D39', 'D41', 'D49', 'D50', 'D51', 'D52', 'D57', 'D58', 'D60', 'D63', 'D65', 'D68', 'M65']:
    assert bad not in S1['note'] + S1['precedent'] + S1['key'], bad
print('ALL OK')
