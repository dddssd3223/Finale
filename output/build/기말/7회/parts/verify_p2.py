# -*- coding: utf-8 -*-
# p2.py (7회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, factor, sqrt, oo, Interval, S
x, t, c, d, m = symbols('x t c d m', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 3, 6: 1, 7: 4, 8: 2}                                       # 분담표 목표 정답
REF = {5: 'M13 후보_순위 2', 6: 'D14 분석집_변형 1', 7: 'M30 후보_순위 2', 8: 'M15 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['M13', 'D14', 'M30', 'M15']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'       # 분담표 목표 수준
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 ×
    for w in it['wrongs']:
        assert f'{CIRC[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)
    txt = it['body']
    assert 'log' not in txt and '이러한' not in txt and '이와 같은' not in txt
    for mm in re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', txt, re.S):
        assert '<' not in ''.join(mm) and '>' not in ''.join(mm), (n, mm)

def chk(no, val, wrongs):
    it = IT[no]; chv = [nsimplify(c_) for c_ in it['choices']]; ws = [nsimplify(w) for w in it['wrongs']]
    dd = {chv[i + 1] - chv[i] for i in range(4)}
    good = (it['ans'] == WANT[no] and nsimplify(val) == chv[it['ans'] - 1] and len(set(chv)) == 5 and len(dd) == 1 and 0 not in dd
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {chv[it["ans"] - 1]} (위치 {it["ans"]}), 공차 {chv[1] - chv[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def posneg(expr):
    """다항방정식 expr=0의 (서로 다른 양의 실근 수, 음의 실근 수)"""
    rs = set(sp.real_roots(sp.Poly(expr, x)))
    return len([r for r in rs if r > 0]), len([r for r in rs if r < 0])

def ab_values(h, target):
    """h(x)=v에서 ab=target인 v: 경계값(극값·h(0))과 그 사이 구간을 전수 조사 → (낱값 목록, 구간 목록)"""
    crit = sorted({h.subs(x, r) for r in sp.real_roots(sp.Poly(diff(h, x), x))} | {h.subs(x, 0)})
    pts = [v for v in crit if (lambda p: p[0] * p[1])(posneg(h - v)) == target]
    mids = [crit[0] - 1] + [(crit[i] + crit[i + 1]) / 2 for i in range(len(crit) - 1)] + [crit[-1] + 1]
    ends = [-oo] + crit + [oo]
    ivs = [(ends[i], ends[i + 1]) for i, v in enumerate(mids) if (lambda p: p[0] * p[1])(posneg(h - v)) == target]
    return pts, ivs

# ===== 원문 풀이 =====
# M13: 2x^3+3x^2-12x=k, ab=2인 정수 k의 개수 25
pts, ivs = ab_values(2*x**3 + 3*x**2 - 12*x, 2)
assert pts == [] and ivs == [(-7, 0), (0, 20)] and sum(b_ - a_ - 1 for a_, b_ in ivs) == 25
# GEN1-02-032: 같은 식, ab=1인 k의 합 13
pts, ivs = ab_values(2*x**3 + 3*x**2 - 12*x, 1); assert sorted(pts) == [-7, 0, 20] and ivs == [] and sum(pts) == 13
# D14: f=x^3+ax^2+3x, a^2<=9, f(2)=14+4a → 2+26=28
a = symbols('a', real=True)
fD = x**3 + a*x**2 + 3*x
assert sp.discriminant(diff(fD, x), x) == 4*a**2 - 36 and fD.subs({x: 2, a: 3}) + fD.subs({x: 2, a: -3}) == 28
# 분석집 D14 변형①: f=(x-1)^2(x+a)+3x, 증가 (a+4)(a-2)<=0, f(3)=4a+21 → 34
fS = (x - 1)**2*(x + a) + 3*x
assert sp.solve_univariate_inequality(sp.discriminant(diff(fS, x), x) <= 0, a, relational=False) == Interval(-4, 2)
assert fS.subs({x: 3, a: -4}) + fS.subs({x: 3, a: 2}) == 34
# M30: x^2(3-x)<n on (0,3): 최댓값 4(x=2) → n=5
assert sp.maximum(x**2*(3 - x), x, Interval.open(0, 3)) == 4 and (x**2*(3 - x)).subs(x, 2) == 4
# M15: m<=2x^2-9x+12 최솟값 15/8, m>=-1 → 7/8
assert sp.minimum(2*x**2 - 9*x + 12, x, Interval.open(0, oo)) == Rational(15, 8) and Rational(15, 8) - 1 == Rational(7, 8)
# 분석집 M15 변형①: 5/2 + 1 = 7/2
assert sp.minimum(2*x**2 - 6*x + 7, x, Interval.open(0, oo)) + sp.maximum(-x**2 - 4*x - 3, x, Interval.open(-oo, 0)) == Rational(7, 2)
print('원문·DB 풀이 OK')

# ===== 5번 =====
h5 = x**3 - 12*x + 2
pts, ivs = ab_values(h5, 1)                                             # 2k의 값
assert ivs == [] and sorted(pts) == [-14, 2, 18]                         # 구간 해 없음 → 낱값 셋뿐(유일)
ks = [Rational(v, 2) for v in pts]; assert all(k_.is_integer for k_ in ks)
for v in pts: assert posneg(h5 - v) == (1, 1)
assert factor(h5 - 18) == (x - 4)*(x + 2)**2 and factor(h5 + 14) == (x - 2)**2*(x + 4)
chk(5, sum(ks), [sum(ks) - 1])                                          # 오답 2: 근 0이 생기는 k=1 누락
p2_, i2_ = ab_values(h5, 2)
print('ABLATION 5 ab=1 → ab=2: 필요(2k의 범위', i2_, '가 되어 값의 합이 정해지지 않음)')
assert i2_ == [(-14, 2), (2, 18)]
pts0, _ = ab_values(x**3 - 12*x, 1)
print('ABLATION 5 상수 2 빼기: 필요(답', sum(Rational(v, 2) for v in pts0), '로 바뀜)'); assert sum(pts0) == 0
print('ABLATION 5 계수 2 빼기(-2k → -k): 필요(답', sum(pts), '로 바뀜)'); assert sum(pts) == 6

# ===== 6번 =====
f6 = (x - 2)**2*(x - c) + 2*x
# 극한 조건: f(2)=4, f'(2)=2 ⇔ f-2x가 (x-2)^2을 인수로 가짐 (일반 삼차로 확인)
p, q, r = symbols('p q r', real=True)
g6 = x**3 + p*x**2 + q*x + r
sol6 = solve([g6.subs(x, 2) - 4, diff(g6, x).subs(x, 2) - 2], [q, r], dict=True)[0]
assert sp.rem(sp.Poly(g6.subs(sol6) - 2*x, x), sp.Poly((x - 2)**2, x)).is_zero
# f'(2)≠2이면 좌우 극한이 ±|f'(2)-2|로 다름: 예 f=(x-2)(x^2+1)+2x → 좌 -5, 우 5
ex = ((x - 2)*(x**2 + 1))
assert sp.limit(sp.Abs(ex)/(x - 2), x, 2, '+') == 5 and sp.limit(sp.Abs(ex)/(x - 2), x, 2, '-') == -5
for cv in (0, 2, 5):                                                    # 인수 꼴이면 좌우 극한 모두 0
    e = (x - 2)**2*(x - cv)
    assert sp.limit(sp.Abs(e)/(x - 2), x, 2, '+') == 0 and sp.limit(sp.Abs(e)/(x - 2), x, 2, '-') == 0
disc = sp.discriminant(diff(f6, x), x)
assert expand(disc/4 - ((c - 2)**2*1 - 6)) == 0 or expand(disc - 4*((c - 2)**2 - 6)) == 0
rng = sp.solve_univariate_inequality(disc <= 0, c, relational=False)
assert rng == Interval(2 - sqrt(6), 2 + sqrt(6))
area = sp.simplify(integrate((x - 2)**2*(x - c), (x, 2, c)))            # 부호 일정: 절댓값 = (c-2)^4/12
assert expand(area + (c - 2)**4/12) == 0
A = (c - 2)**4/12
amax = sp.maximum(A, c, rng); assert amax == 3 and A.subs(c, 2 + sqrt(6)) == 3 and A.subs(c, 2 - sqrt(6)) == 3
chk(6, amax, [6])                                                       # 오답 6: (c-2)^4/6 또는 (c-2)^2의 최댓값
assert sp.maximum((c - 2)**4/6, c, rng) == 6 and sp.maximum((c - 2)**2, c, rng) == 6
print('ABLATION 6 증가 조건: 필요(c에 제한이 없어 넓이 (c-2)^4/12의 최댓값이 없음)'); assert sp.limit(A, c, oo) == oo
print('ABLATION 6 극한 조건: 필요(접하지 않아 f가 미정계수 셋으로 남고 넓이가 정해지지 않음)')
A1 = (c - 2)**4/12; d1 = sp.discriminant(diff((x - 2)**2*(x - c) + 3*x, x), x)
print('ABLATION 6 직선 2x → 3x: 필요(답', sp.maximum(A1, c, sp.solve_univariate_inequality(d1 <= 0, c, relational=False)), '로 바뀜)')

# ===== 7번 =====
f7 = integrate(8*t - 3*t**2, (t, 0, x)); assert expand(f7 - x**2*(4 - x)) == 0
I7 = Interval.open(0, 4)
def ok7(n, I=I7, rhs=lambda n: n*(4 - x)):
    return sp.solve_univariate_inequality(f7 - rhs(n) < 0, x, relational=False).is_superset(I)
good = [n for n in range(1, 40) if ok7(n)]
assert good == list(range(16, 40)) and not ok7(15) and ok7(16)           # n>=16에서 계속 성립(단조)
assert factor(f7 - 16*(4 - x)) == -(x - 4)**2*(x + 4)                    # (0,4)에서 음수
chk(7, min(good), [17])
orig_way = sp.maximum(f7, x, I7); assert orig_way == Rational(256, 27)   # 원문 방식이면 10
print('ABLATION 7 직선 n(4-x) → 상수 n: 필요(답', sp.floor(orig_way) + 1, '로 바뀜)'); assert sp.floor(orig_way) + 1 == 10
print('ABLATION 7 정의역 (0,4) → (0,3): 필요(답', min(n for n in range(1, 40) if ok7(n, I=Interval.open(0, 3))), '로 바뀜)')

# ===== 8번 =====
R8 = x**3 - 2*x**2 + 4*x + 1; L8 = -x**3 - 2*x**2 - 4*x + 1
assert expand(R8.subs(x, -x) - L8) == 0 and R8.subs(x, 0) == 1           # y축 대칭, f(0)=g(0)=1
up = sp.minimum(sp.cancel((R8 - 1)/x), x, Interval.open(0, oo))          # m <= 이 값
lo = sp.maximum(sp.cancel((L8 - 1)/x), x, Interval.open(-oo, 0))         # m >= 이 값
assert (up, lo) == (3, -3)
def ok8(mv):
    return (sp.solve_univariate_inequality(R8 - mv*x - 1 >= 0, x, relational=False).is_superset(Interval(0, oo))
            and sp.solve_univariate_inequality(L8 - mv*x - 1 >= 0, x, relational=False).is_superset(Interval.open(-oo, 0)))
assert ok8(3) and ok8(-3) and ok8(0) and not ok8(Rational(31, 10)) and not ok8(Rational(-31, 10))
chk(8, up - lo, [up - diff(L8, x).subs(x, 0)])                           # 오답 7: 하한을 x=0에서의 기울기 -4로
print('ABLATION 8 x<0 조각: 필요(없으면 m의 최솟값이 없음)')
print('ABLATION 8 x<0 조각 → 원문 꼴 1-x: 필요(답', up - (-1), '로 바뀜)')
print('ABLATION 8 x>=0 조각: 필요(없으면 m의 최댓값이 없음)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [3, 1, 4, 2]
print('ALL OK')
