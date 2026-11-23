# -*- coding: utf-8 -*-
# 서답형1 (자체, M9 유형) · 서답형2 (I63 학교식, 부호 거울상) 검증 · author='claude'
import sympy as sp, os, sys, re
x, t, a = sp.symbols('x t a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def min_on_ray(h, lo):
    """[lo, ∞)에서 다항식 h(최고차 양수)의 최솟값 — 끝점과 구간 안 정류점 전수"""
    pts = [sp.Integer(lo)] + [c for c in sp.Poly(sp.diff(h, x), x).real_roots() if c > lo]
    return min(sp.simplify(h.subs(x, c)) for c in pts)

def amax(f, g, lo):
    """x≥lo 에서 f≥g 가 성립하는 a 의 최댓값 (h=f-g 는 상수항에만 -a)"""
    h0 = sp.expand((f - g).subs(a, 0))
    return min_on_ray(h0, lo)

# ================= S1 =================
# --- 원문 M9
fo, go = x**3 - x + 6, x**2 + a
assert amax(fo, go, 0) == 5 and F.I['M9'][2] == '⑤' and F.I['M9'][1][4] == '5'
print('M9 원문 OK: a의 최댓값 5 (원문 정답 ⑤)')

# --- S1
assert r"f(x)=x^3-4x+10" in S1['body'] and r"g(x)=2x^2+a" in S1['body'] and r"\(x\ge0\)" in S1['body']
f1, g1 = x**3 - 4 * x + 10, 2 * x**2 + a
h1 = sp.expand(f1 - g1)
assert sp.expand(sp.diff(h1, x) - (3 * x + 2) * (x - 2)) == 0
A = amax(f1, g1, 0)
assert A == 2
# 전수: 정수 a 에 대해 x≥0 에서 h≥0 인지 (구간 [0, 50] 촘촘히 + 정확 최솟값)
ok_a = [av for av in range(-20, 21) if min_on_ray(h1.subs(a, av), 0) >= 0]
assert max(ok_a) == 2 and ok_a == list(range(-20, 3))
# (2) a=2 에서 h=(x-2)^2(x+2), 접점 x=2 하나
hA = h1.subs(a, 2)
assert sp.factor(hA) == (x - 2)**2 * (x + 2)
tang = [r for r in sp.solve([hA, sp.diff(hA, x)], x, dict=True)]
assert tang == [{x: 2}]
fA, gA = f1, g1.subs(a, 2)
assert fA.subs(x, 2) == gA.subs(x, 2) == 10 and sp.diff(fA, x).subs(x, 2) == sp.diff(gA, x).subs(x, 2) == 8
line = sp.expand(8 * (x - 2) + 10)
assert line == 8 * x - 6
assert S1['ans'] == [r'(1) \(2\)', r'(2) \(y=8x-6\)']
# x=-2 에서는 접하지 않음(부호 바뀜)
assert sp.diff(fA, x).subs(x, -2) != sp.diff(gA, x).subs(x, -2)
# 오답 값
assert sp.solve(h1.subs(x, 0), a) == [10]
assert h1.subs({x: R(-2, 3), a: 0}) == R(310, 27)
assert sp.expand(sp.diff(f1, x).subs(x, -2) * (x + 2) + f1.subs(x, -2)) == 8 * x + 26
assert sp.expand(8 * (x - 2) + (2 * x**2).subs(x, 2)) == 8 * x - 8
for w in (r'a=10', r'\dfrac{310}{27}', r'y=8x+26', r'y=8x-8'): assert w in S1['wrong'], w
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 M9)'
print('S1 OK: (1) a의 최댓값 2 (2) 접점 (2, 10), 접선 y=8x-6')

def abl1(c, m): print(f'ABLATION S1 {c}: {m}')
# x≥0 삭제(모든 실수): h → -∞ 라 a 가 정해지지 않음
assert sp.limit(h1.subs(a, 0), x, -sp.oo) == -sp.oo
abl1('x≥0', '필요(없으면 모든 실수 x에서 h(x)=f(x)-g(x)가 -∞로 가 a의 최댓값이 없음)')
# x≥0 → x≥3: 끝값이 최소가 되어 a 가 바뀜
assert amax(f1, g1, 3) == 7
abl1('x≥0의 끝 0', '필요(x≥3이면 최솟값이 끝값 h(3)=7-a가 되어 a=7, 접하지 않음)')
# g 의 2x^2 → x^2: 접하는 구조가 깨짐(최댓값이 무리수 근에서)
hx = sp.expand(f1 - x**2)
cr = [c for c in sp.Poly(sp.diff(hx, x), x).real_roots() if c > 0]
assert len(cr) == 1 and not cr[0].is_rational
Ax = amax(f1, x**2 + a, 0); assert Ax != 2
abl1('g(x)의 2x^2', f'필요(x^2이면 최소가 무리수 x={sp.N(cr[0], 5)}에서 나와 a의 최댓값이 {sp.N(Ax, 6)}로 바뀜)')
abl1('부등식 f(x)≥g(x)', '필요((1)·(2)가 묻는 대상)')


# ================= S2 =================
def gfun(fx, k, mirror, av):
    """g(x)=∫_a^x {f(t)-f(x)}{f(t)}^k dt (mirror) 또는 {f(x)-f(t)}{f(t)}^k dt"""
    ft = fx.subs(x, t)
    ig = (ft - fx) * ft**k if mirror else (fx - ft) * ft**k
    return sp.expand(sp.integrate(sp.expand(ig), (t, av, x)))

def extrema(gp):
    """g'(x) 다항식에서 부호가 바뀌는 점(홀수 중복 근)과 극대/극소"""
    out = []
    P = sp.Poly(gp, x)
    rr = {}
    for r in P.real_roots():
        rr[r] = rr.get(r, 0) + 1
    for r in sorted(rr):
        if rr[r] % 2 == 1:
            eps = R(1, 10**6)
            left = sp.sign(sp.N(P.eval(r - eps), 50)); right = sp.sign(sp.N(P.eval(r + eps), 50))
            out.append((r, '극대' if left > 0 > right else '극소'))
    return out

# --- 원문 I63: 합 8
fo2 = x**3 - 12 * x**2 + 45 * x + 3
assert sp.expand(sp.diff(gfun(fo2, 4, False, a), x) - sp.diff(fo2, x) * sp.integrate(fo2.subs(x, t)**4, (t, a, x))) == 0
one = [av for av in range(-5, 12) if len(extrema(sp.diff(gfun(fo2, 4, False, av), x))) == 1]
assert one == [3, 5] and sum(one) == 8 and F.I['I63'][2] == '8'
print('I63 원문 OK: a=3, 5, 합 8')

# --- S2
assert r"f(x)=x^3-6x^2-15x+1" in S2['body'] and r"\{f(t)\}^2\{f(t)-f(x)\}" in S2['body'] and 'cond' not in S2
q1, q2, q3 = [q[0] for q in S2['subs']]
assert r"g'(x)=h(x)" in q1 and r"\{f(t)\}^2" in q1
assert r"a=0" in q2 and '극솟값을 갖는' in q2
assert '극솟값을 갖지 않도록' in q3 and '모든 \\(a\\)의 값의 합' in q3
f2 = x**3 - 6 * x**2 - 15 * x + 1
fp2 = sp.diff(f2, x)
assert sp.expand(fp2 - 3 * (x - 5) * (x + 1)) == 0
# (1) g'(x) = -f'(x) ∫_a^x f^2 (a 기호 그대로)
G = gfun(f2, 2, True, a)
J = sp.integrate(sp.expand(f2.subs(x, t)**2), (t, a, x))
assert sp.expand(sp.diff(G, x) - (-fp2) * J) == 0
H = sp.expand(-fp2); assert H == -3 * x**2 + 12 * x + 15
# f 는 영다항식이 아니고 f^2 의 근은 유한 → J 는 증가, J(a)=0 → 부호 = x-a
assert sp.expand(sp.diff(J, x) - f2**2) == 0
# (2) a=0
e0 = extrema(sp.diff(gfun(f2, 2, True, 0), x))
assert e0 == [(-1, '극대'), (0, '극소'), (5, '극대')], e0
ANS2 = [r for r, s in e0 if s == '극소']; assert ANS2 == [0]
# (3) 전수: a 를 1/4 간격 [-10, 10] + f'의 근·f''의 근에서 극솟값이 없는 a
grid = sorted(set([R(i, 4) for i in range(-40, 41)] + [sp.Integer(-1), sp.Integer(5), sp.Integer(2)]))
nomin = []
for av in grid:
    ex = extrema(sp.diff(gfun(f2, 2, True, av), x))
    assert len(ex) in (1, 3)
    if not any(s == '극소' for _, s in ex): nomin.append(av)
    if av not in (-1, 5): assert [s for _, s in ex] == ['극대', '극소', '극대']
assert nomin == [-1, 5]
# a=-1, 5 에서 남는 극값의 위치
assert extrema(sp.diff(gfun(f2, 2, True, -1), x)) == [(5, '극대')]
assert extrema(sp.diff(gfun(f2, 2, True, 5), x)) == [(-1, '극대')]
# f 의 근(무리수)과 a 가 겹쳐도 J'=f^2 ≥ 0 이고 0 인 점이 셋뿐 → J 는 순증가, 부호 변화는 a 한 곳
assert len(set(sp.Poly(f2, x).real_roots())) == 3 and sp.degree(f2, x) == 3
ANS3 = sum(nomin)
assert ANS3 == 4
assert S2['ans'] == [r'(1) \(h(x)=-3x^2+12x+15\)', r'(2) \(0\)', r'(3) \(4\)']
print('S2 OK: (1) h=-3x^2+12x+15 (2) 극소 x=0 (3) a=-1, 5, 합 4 (a 격자 전수)')

# 오답 값
assert sp.expand(fp2) == 3 * x**2 - 12 * x - 15                                       # 거울상 놓침
e0w = extrema(sp.diff(gfun(f2, 2, False, 0), x))
assert [r for r, s in e0w if s == '극소'] == [-1, 5]                                   # 부호 안 뒤집음
assert [r for r, s in extrema(-fp2) if s == '극소'] == [-1]                            # 적분을 늘 양수로
nominw = [av for av in grid if not any(s == '극소' for _, s in extrema(sp.diff(gfun(f2, 2, False, av), x)))]
assert nominw == []                                                                    # 부호 안 뒤집으면 그런 a 없음
assert sp.solve(sp.diff(f2, x, 2), x) == [2] and -1 + 2 + 5 == 6
for w in (r'3x^2-12x-15', r'\(x=-1\), \(x=5\)', r'극소를 \(x=-1\)로', "'없음'", r'=6\)'): assert w in S2['wrong'], w
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['2점, 답만 적으시오.', '4점, 답만 적으시오.', '4점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S2['rubric'][:3]]
assert pts2 == [[2], [4], [4]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line_ for line_ in S2['rubric'][:3])
assert S2['db_ref'] == 'I63 후보_순위 3' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
for it in (S1, S2):
    tx = it['body'] + ''.join(q[0] for q in it['subs'])
    assert '이러한' not in tx and '이와 같은' not in tx
    assert not [m for m in re.findall(r'\\\(.*?\\\)', tx) if '<' in m or '>' in m]
print('S2 형식 OK')

def abl2(c, m): print(f'ABLATION S2 {c}: {m}')
# (a) 거울상 f(t)-f(x) → f(x)-f(t)
abl2('적분 안의 순서 f(t)-f(x)', f'필요(f(x)-f(t)이면 (1) h=f\'(x), (2) 극소 x=-1, 5, (3) 극솟값이 없는 a가 없음)')
# (b) 지수 2 → 1 (홀수): 적분 부호가 x-a 가 아님 → (2) 답이 바뀜
e1 = extrema(sp.diff(gfun(f2, 1, True, 0), x))
m1 = [sp.N(r, 6) for r, s in e1 if s == '극소']
assert [r for r, s in e1 if s == '극소'] != [0]
abl2('{f(t)}^2의 지수 2', f'필요(지수 1이면 ∫_0^x f의 부호가 x의 부호가 아니어서 (2)의 극소가 {m1}로 바뀜)')
# (c) (2)의 a=0 → a=2
e2 = extrema(sp.diff(gfun(f2, 2, True, 2), x))
assert [r for r, s in e2 if s == '극소'] == [2]
abl2('(2)의 a=0', '필요(a=2이면 극소가 x=2)')
# (d) f 의 -6x^2 → -3x^2 (f'=3(x+1)(x-3)) → (3) 합 2
f9 = x**3 - 3 * x**2 - 9 * x + 1
assert sp.expand(sp.diff(f9, x) - 3 * (x + 1) * (x - 3)) == 0
n9 = [av for av in grid if not any(s_ == '극소' for _, s_ in extrema(sp.diff(gfun(f9, 2, True, av), x)))]
assert n9 == [-1, 3] and sum(n9) != 4
abl2('f(x)의 계수(-6x^2, -15x)', f"필요(x^3-3x^2-9x+1이면 극솟값이 없는 a가 {n9}, 합 {sum(n9)})")
# (e) (3)의 '극솟값을 갖지 않도록' → '극댓값을 갖지 않도록'
nomax = [av for av in grid if not any(s == '극대' for _, s in extrema(sp.diff(gfun(f2, 2, True, av), x)))]
assert nomax == []
abl2('(3)의 극솟값', '필요(극댓값으로 바꾸면 그런 a가 없음: 거울상이라 남는 극값이 늘 극대)')

print('ALL OK')
