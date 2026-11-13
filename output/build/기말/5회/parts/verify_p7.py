# -*- coding: utf-8 -*-
# 서답형1 (자체, D56 유형) · 서답형2 (D66 학교식) 검증 · author='claude'
import sympy as sp, os, sys, re, itertools
x, a, b, k, p, r = sp.symbols('x a b k p r', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def crit(f):
    """f의 극대·극소 (x좌표, 종류) 목록"""
    d = sp.diff(f, x); out = []
    for c in sorted(set(sp.Poly(d, x).real_roots())):
        s2 = sp.diff(d, x).subs(x, c)
        if s2 < 0: out.append((c, 'max'))
        elif s2 > 0: out.append((c, 'min'))
    return out

def solve_d56(lead, lin, xm, maxv):
    """f=lead x^3+a x^2+lin x+b, x=xm 에서 극소, 극댓값 maxv 인 (a,b) 전부"""
    f = lead * x**3 + a * x**2 + lin * x + b
    res = []
    for av in sp.solve(sp.diff(f, x).subs(x, xm), a):
        fa = f.subs(a, av)
        cr = crit(fa.subs(b, 0))
        if (xm, 'min') not in cr: continue
        for c, kind in cr:
            if kind == 'max':
                for bv in sp.solve(fa.subs(x, c) - maxv, b): res.append((av, bv))
    return res

def nreal(f):
    return len(set(sp.Poly(sp.expand(f), x).real_roots()))

def two_root_ks(f):
    """f(x)=k 의 서로 다른 실근이 2개인 k: 후보는 극값뿐(그 밖에서는 개수가 1 또는 3). 극값 사이·밖도 표본으로 확인"""
    ext = sorted({f.subs(x, c) for c, _ in crit(f)})
    ks = [kv for kv in ext if nreal(f - kv) == 2]
    probes = [ext[0] - 5, ext[-1] + 5] + [(u + v) / 2 for u, v in zip(ext, ext[1:])]
    assert all(nreal(f - kv) != 2 for kv in probes)
    return ks

# ================= S1 =================
# --- 원문 D56: x^3+ax^2-9x+b, x=1 극소, 극댓값 28 → a+b=4
so = solve_d56(1, -9, 1, 28)
assert so == [(3, 1)] and sum(so[0]) == 4 and F.I['D56'][2] == '4'
print('D56 원문 OK: a=3, b=1, a+b=4 (원문 정답 4)')

# --- S1: 2x^3+ax^2-12x+b, x=1 극소, 극댓값 25
assert r"f(x)=2x^3+ax^2-12x+b" in S1['body'] and r"\(x=1\)에서 극소" in S1['body'] and r"극댓값이 \(25\)" in S1['body']
s1 = solve_d56(2, -12, 1, 25)
assert s1 == [(3, 5)], s1                                         # 하나로 정해짐
f1 = 2 * x**3 + 3 * x**2 - 12 * x + 5
assert sp.expand(sp.diff(f1, x) - 6 * (x - 1) * (x + 2)) == 0
assert crit(f1) == [(-2, 'max'), (1, 'min')] and f1.subs(x, -2) == 25 and f1.subs(x, 1) == -2
assert S1['ans'][0] == r'(1) \(a=3\), \(b=5\)'
ks = two_root_ks(f1)
assert sorted(ks) == [-2, 25] and sum(ks) == 23
# k 를 정수로 -10..35 훑어 직접 세기
assert [kv for kv in range(-10, 36) if nreal(f1 - kv) == 2] == [-2, 25]
assert S1['ans'][1] == r'(2) \(23\)'
# GEN1-01-100(x=2 극소, 극댓값 85 → a+b=8)과 수치가 다름
assert solve_d56(1, -24, 2, 85) == [(3, 5)] and (2, -12, 1, 25) != (1, -24, 2, 85)
# 오답 값
assert sp.solve((2 * x**3 + 3 * x**2 - 12 * x + b).subs(x, 1) - 25, b) == [32]          # 극댓값을 x=1에서의 값으로
assert sp.solve(6 + a - 12, a) == [6]                                                     # 미분 실수
fw = 2 * x**3 + 3 * x**2 - 12 * x + 32
assert sorted(two_root_ks(fw)) == [25, 52] and sum(two_root_ks(fw)) == 77                 # b=32 를 그대로
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5] and sum(map(sum, pts1)) == 10, pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D56)'
print('S1 OK: (1) a=3, b=5 하나, (2) 극댓값 25 + 극솟값 -2 = 23')

# ----- 조건 빼 보기 S1
def abl1(cname, msg): print(f'ABLATION S1 {cname}: {msg}')
# (a) x=1에서 극소 삭제: a 가 정해지지 않음
outs = []
for av in [3, -3, R(21, 2)]:
    fa = 2 * x**3 + av * x**2 - 12 * x + b
    cm = [c for c, kd in crit(fa.subs(b, 0)) if kd == 'max'][0]
    bv = sp.solve(fa.subs(x, cm) - 25, b)[0]
    outs.append((av, bv, sum(two_root_ks(fa.subs(b, bv)))))
assert len({o[:2] for o in outs}) == 3 and len({o[2] for o in outs}) >= 2
abl1('x=1에서 극소', '필요(없으면 ' + ', '.join(f'a={o[0]}이면 b={o[1]}, (2)={o[2]}' for o in outs) + ')')
# (b) 극댓값 25 삭제: b 가 남음
outb = [(bv, sum(two_root_ks(2 * x**3 + 3 * x**2 - 12 * x + bv))) for bv in (0, 5, 10)]
assert len({o[1] for o in outb}) == 3
abl1('극댓값 25', '필요(없으면 b가 정해지지 않아 (2)가 ' + ', '.join(f'b={o[0]}이면 {o[1]}' for o in outb) + ')')
# (c) '극소'를 '극대'로 바꾸면(극점 종류의 조건): x=1 은 극소일 수밖에 없어 a=3 에서 해가 없음 → 종류 조건은 x=1이 극점이라는 정보와 함께 일함
assert solve_d56(2, -12, 1, 25) and all(kd == 'min' for c, kd in crit((2 * x**3 + 3 * x**2 - 12 * x)) if c == 1)
abl1('개수 2', '필요(개수를 3으로 바꾸면 -2<k<25인 모든 k가 되어 합이 정해지지 않음, 1이면 k<-2 또는 k>25)')
assert all(nreal(f1 - kv) == 3 for kv in (-1, 0, 10, 24)) and nreal(f1 - 30) == 1


# ================= S2 =================
def roots_mult(poly):
    P = sp.Poly(sp.expand(poly), x)
    return sp.roots(P, multiple=False) if P.degree() > 0 else {}

def g_diffable(fx, av):
    """|f(x)f(a-x)| 가 실수 전체에서 미분가능 ⇔ 곱의 실근 중 단순근(부호가 바뀌고 도함수 ≠0)이 없음"""
    h = sp.expand(fx * fx.subs(x, av - x))
    for rt, m in roots_mult(h).items():
        if rt.is_real and m == 1: return False
    return True

def count_crit(fx, side, c0):
    """f'(x)=0 의 서로 다른 실근 중 side('le' 또는 'ge') c0 인 것의 개수"""
    rs = set(sp.Poly(sp.diff(fx, x), x).real_roots())
    return len([u for u in rs if (u <= c0 if side == 'le' else u >= c0)])

# --- 원문 D66: f(1)=f(3)=0, {x>=1, f'=0} 1개 → a=2, q=-1, 답 105
fo = (x + 1) * (x - 1) * (x - 3)
assert count_crit(fo, 'ge', 1) == 1 and g_diffable(fo, 2)
ratio_o = sp.simplify((fo.subs(x, 8))**2 / (fo.subs(x, 0) * fo.subs(x, 8)))
assert ratio_o == 105 and F.I['D66'][2] == '105'
print('D66 원문 OK: f=p(x+1)(x-1)(x-3), a=2, g(8)/(f(0)f(8))=105 (원문 정답 105)')
# LIVE1-01-143: g(2k)/(f(0)f(4k)) = 5/21
assert sp.Abs(fo.subs(x, 4) * fo.subs(x, 2 - 4)) / (fo.subs(x, 0) * fo.subs(x, 8)) == R(5, 21)

# --- S2: (가) f(2)=f(3)=0, (나) {x<=3, f'=0} 1개
assert r"f(2)=f(3)=0" in S2['cond'][0][1] and r"\(3\) 이하인 것의 개수는 \(1\)이다" in S2['cond'][0][1] and '미분가능' in S2['cond'][1][1]
assert r"g(x)=|f(x)f(a-x)|" in S2["body"] and not S2.get("after")
def survivors(r_list, a_list, need_nab=True, ab_cond=None):
    out = []
    for rv in r_list:
        fx = sp.expand((x - 2) * (x - 3) * (x - rv))
        if need_nab and count_crit(fx, 'le', 3) != 1: continue
        for av in a_list:
            if g_diffable(fx, av): out.append((rv, av))
    return out
# 세 번째 근 r 와 a 를 1/2 간격 격자로 전수 (근이 반정수일 때 대칭 a 도 정수·반정수)
r_grid = [R(i, 2) for i in range(-12, 25)]
a_grid = [R(i, 2) for i in range(-20, 41)]
sv = survivors(r_grid, a_grid)
assert sv == [(4, 6)], sv
# (나)만으로 r>3 확인 (r 연속 범위의 표본)
for rv in [R(-3), R(1), R(2), R(5, 2), R(3), R(31, 10), R(4), R(7)]:
    fx = (x - 2) * (x - 3) * (x - rv)
    assert (count_crit(fx, 'le', 3) == 1) == (rv > 3), rv
# r>3 일반: 집합 {2,3,r} = {a-2,a-3,a-r} 의 대응을 전부 풀어 봄
sols = set()
for perm in itertools.permutations([a - 2, a - 3, a - r]):
    for so in sp.solve([2 - perm[0], 3 - perm[1], r - perm[2]], [a, r], dict=True):
        if len(so) == 2 and so[r] > 3: sols.add((so[a], so[r]))
assert sols == {(6, 4)}, sols
f2 = (x - 2) * (x - 3) * (x - 4)              # p 는 약분되므로 1로 두고, 아래에서 p 기호로도 확인
A6 = 6
assert sp.expand(f2.subs(x, A6 - x) + f2) == 0   # f(6-x)=-f(x) → g=f^2
fp = p * f2
ANS1 = A6
ANS2 = sp.simplify(fp.subs(x, A6 + 2) / fp.subs(x, 0))
ANS3 = sp.simplify(sp.Abs(fp.subs(x, A6 + 1) * fp.subs(x, A6 - (A6 + 1))) / (fp.subs(x, 0) * fp.subs(x, 1)))
assert ANS2 == -5 and ANS3 == 25, (ANS2, ANS3)
assert [fp.subs(x, v) / p for v in (0, 1, -1, 7, 8)] == [-24, -6, -60, 60, 120]
assert S2['ans'] == [r'(1) \(6\)', r'(2) \(-5\)', r'(3) \(25\)']
assert r"\(a\)의 값" in S2['subs'][0][0] and r"\dfrac{f(a+2)}{f(0)}" in S2['subs'][1][0] and r"\dfrac{g(a+1)}{f(0)\times f(1)}" in S2['subs'][2][0]
# p 부호와 무관 (음수 p 도 같은 값)
for pv in (-3, R(1, 2), 5):
    fq = pv * f2
    assert fq.subs(x, 8) / fq.subs(x, 0) == -5
    assert abs(fq.subs(x, 7) * fq.subs(x, -1)) / (fq.subs(x, 0) * fq.subs(x, 1)) == 25
# 오답 값
fl = (x - 1) * (x - 2) * (x - 3)                                     # 원문처럼 왼쪽 근: r=1, a=4
assert g_diffable(fl, 4) and count_crit(fl, 'le', 3) == 2           # (나)를 어김
assert fl.subs(x, 6) / fl.subs(x, 0) == -10                          # (2) -10
assert fl.subs(x, 1) == 0                                            # (3) 분모 0 으로 막힘
assert -ANS2 == 5                                                    # f(0) 부호 실수
assert (f2.subs(x, 7) * f2.subs(x, -1)) / (f2.subs(x, 0) * f2.subs(x, 1)) == -25    # 절댓값 누락
assert (f2.subs(x, 7) * f2.subs(x, 5)) / (f2.subs(x, 0) * f2.subs(x, 1)) == R(5, 2)  # g(a+1)=f(a+1)f(a-1) 로 읽음
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3 and [c[0] for c in S2['cond']] == ['가', '나']
assert [q[1] for q in S2['subs']] == ['4점, 답만 적으시오.', '3점, 답만 적으시오.', '3점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S2['rubric'][:3]]
assert pts2 == [[4], [3], [3]], pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line for line in S2['rubric'][:3])
assert S2['db_ref'] == 'D66 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
print('S2 OK: f=p(x-2)(x-3)(x-4) 하나, (1) a=6 (2) -5 (3) 25')

# ----- 조건 빼 보기 S2
def abl2(cname, msg): print(f'ABLATION S2 {cname}: {msg}')
# (a) (나) 삭제
sa = survivors(r_grid, a_grid, need_nab=False)
assert len({av for _, av in sa}) > 1 and (4, 6) in sa
abl2('(가)의 f\'(x)=0 조건', '필요(없으면 (r, a)=' + ', '.join(f'({u}, {v})' for u, v in sa) + ' 가 모두 되어 a가 정해지지 않음)')
# (b) (나)의 x≤3 을 원문 방향 x≥2 로 되돌리면 답이 바뀜
sb = []
for rv in r_grid:
    fx = (x - 2) * (x - 3) * (x - rv)
    if count_crit(fx, 'ge', 2) != 1: continue
    sb += [(rv, av) for av in a_grid if g_diffable(fx, av)]
assert sb == [(1, 4)]
abl2('(가)의 방향 3 이하', '필요(원문처럼 2 이상이면 r=1, a=4로 바뀌고 (3)의 분모 f(1)=0)')
# (c) (가) 의 f(3)=0 삭제 (f(2)=0 만): 다른 두 근이 자유 → a 가 여럿
sc = []
for s_ in [R(i, 2) for i in range(-6, 13)]:
    for rv in [R(i, 2) for i in range(-6, 13)]:
        if len({2, s_, rv}) < 3: continue
        fx = (x - 2) * (x - s_) * (x - rv)
        if count_crit(fx, 'le', 3) != 1: continue
        for av in range(-4, 16):
            if g_diffable(fx, av): sc.append(av)
assert len(set(sc)) > 1
abl2('(가)의 f(3)=0', f'필요(없으면 a가 {sorted(set(sc))[:6]} 등 여럿)')
# (d) 미분가능 조건 삭제: a 가 아무 값
assert not g_diffable(f2, 5) and not g_diffable(f2, 7)
abl2('(나) g(x)가 미분가능', '필요(없으면 a에 대한 조건이 없어 a가 정해지지 않음: a=5, 7 등에서는 미분가능하지 않으므로 이 조건이 a=6을 고름)')
# (e) (나)의 개수 1 → 2: r<=3 쪽이 남아 여러 경우
se = []
for rv in r_grid:
    fx = (x - 2) * (x - 3) * (x - rv)
    if count_crit(fx, 'le', 3) != 2: continue
    se += [(rv, av) for av in a_grid if g_diffable(fx, av)]
assert se and (4, 6) not in se
abl2("(가)의 개수 1", '필요(2로 바꾸면 (r, a)=' + ', '.join(f'({u}, {v})' for u, v in se) + ')')

print('ALL OK')
