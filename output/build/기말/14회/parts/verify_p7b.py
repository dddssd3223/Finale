# -*- coding: utf-8 -*-
# 14회 서답형2 (M67 후보_순위 2 학교식, 답만 3단계) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a, b, c, p, q, h = sp.symbols('x a b c p q h', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7b.py')).read(), ns)
S2 = ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def kval(f, x0):
    """k(x0)=lim_{h→0+}{|f(x0+h)|-|f(x0-h)|}/h. f(x0)≠0이면 2·sign(f)·f', f(x0)=0이면 |f'|-|f'|=0."""
    v = f.subs(x, x0); d1 = sp.diff(f, x).subs(x, x0)
    return 2 * sp.sign(v) * d1 if v != 0 else sp.Integer(0)


def k_side(f, r, side):
    """k(x)의 x→r± 극한 (r 가까이에서 f≠0)"""
    e = R(1, 10**9) * side
    return 2 * sp.sign(f.subs(x, r + e)) * sp.diff(f, x).subs(x, r)


def g_cont(f, s):
    """g(x)=f(x+s)k(x)가 실수 전체에서 연속 ⇔ k의 불연속점(f의 실근 r 중 k의 좌우 극한·값이 다른 점)마다 f(r+s)=0"""
    for r in set(sp.Poly(f, x).real_roots()):
        if not (k_side(f, r, -1) == k_side(f, r, 1) == kval(f, r)) and f.subs(x, r + s) != 0: return False
    return True


def g_zeros(f, s):
    """g(x)=0의 서로 다른 실근: f(x+s)=0 또는 k(x)=0 (k(x)=0 ⇔ f(x)=0 또는 f'(x)=0)"""
    z = {r - s for r in sp.Poly(f, x).real_roots()} | set(sp.Poly(f, x).real_roots()) | set(sp.Poly(sp.diff(f, x), x).real_roots())
    assert all(kval(f, t) == 0 for t in z if (f.subs(x, t + s) != 0))
    return sorted(z)


def gval(f, s, x0): return f.subs(x, x0 + s) * kval(f, x0)


def localmax(f):
    return [f.subs(x, t) for t in sp.Poly(sp.diff(f, x), x).real_roots() if sp.diff(f, x, 2).subs(x, t) < 0]


def solve_all(lead, s, total, need4=True, cont=True):
    """최고차항 lead인 삼차 f 전부를 실근 배치별로 조사: g 연속, g=0의 서로 다른 실근 4개, 합 total"""
    out = []
    # ① 서로 다른 세 실근 a<b<c (모두 단순근): r+s가 다시 근이어야 하는데 s>0이면 가장 큰 근, s<0이면 가장 작은 근이 걸림 → 연속 불가
    #    기호로 확인: {a+s,b+s,c+s} ⊂ {a,b,c}는 s≠0에서 해 없음
    if cont:
        import itertools
        for im in itertools.product((a, b, c), repeat=3):
            sol = sp.solve([a + s - im[0], b + s - im[1], c + s - im[2]], [a, b, c], dict=True)
            assert sol == [], sol
    # ② 실근 하나(단순근) + 허근 둘: f=lead(x-a)(x²+px+q), p²<4q → r=a에서 k 불연속, f(a+s)=s(…)≠0 → 연속 불가
    if cont:
        v = sp.expand(((x - a) * (x**2 + p * x + q)).subs(x, a + s) / s)   # =(a+s)²+p(a+s)+q, 판별식 p²-4q<0이라 양수
        assert sp.discriminant(v.subs(a, x - s), x) == p**2 - 4 * q
    # ③ 삼중근 f=lead(x-a)³: 연속. g=0의 실근 a-s, a (2개)
    f3 = lead * (x - a)**3
    assert g_cont(f3.subs(a, 2), s) and len(g_zeros(f3.subs(a, 2), s)) == 2
    if not need4:
        for av in sp.solve(sp.Eq(2 * a - s, total), a): out.append(sp.expand(f3.subs(a, av)))
    # ④ f=lead(x-a)²(x-b), b≠a: 단순근 b에서 k 불연속 → f(b+s)=0 ⇔ b+s=a
    f4 = lead * (x - a)**2 * (x - a + s)
    for bv in (a - s, a + s, a - 1, a + 2):      # b=a-s만 연속
        ft = (lead * (x - a)**2 * (x - bv)).subs(a, 1)
        assert g_cont(ft, s) == (bv == a - s), bv
    zs = [a - 2 * s, a - s, a - R(2, 3) * s, a]
    for av in sp.solve(sp.Eq(sum(zs), total), a):
        ff = f4.subs(a, av); z = g_zeros(ff, s)
        assert z == sorted(t.subs(a, av) for t in zs) and len(z) == 4 and g_cont(ff, s)
        out.append(sp.expand(ff))
    return out


def parse(sv):
    m = re.search(r'\\\((.*?)\\\)', sv).group(1)
    m2 = re.fullmatch(r'(-?)\\d?frac\{(\d+)\}\{(\d+)\}', m)
    return (-1 if m2[1] else 1) * R(int(m2[2]), int(m2[3])) if m2 else sp.Integer(m)


# ---- 극한 함수 k의 공식을 수치로 확인 (작은 h)
ftest = (x - 5)**2 * (x + 1)
for x0 in (-3, -2, -1, 0, 1, 3, 5, 7):
    hv = R(1, 10**7)
    num = (abs(ftest.subs(x, x0 + hv)) - abs(ftest.subs(x, x0 - hv))) / hv
    assert abs(sp.N(num - kval(ftest, x0))) < 1e-3, (x0, num)
# 단순근 -1에서 k의 좌우 극한이 다르고 값은 0, 접하는 점 5에서는 연속
assert k_side(ftest, -1, -1) == -72 and k_side(ftest, -1, 1) == 72 and kval(ftest, -1) == 0
assert k_side(ftest, 5, -1) == k_side(ftest, 5, 1) == kval(ftest, 5) == 0

# ---- 변형: 전수 조사로 f가 하나
sols = solve_all(1, 6, -2)
assert len(sols) == 1, sols
f = sols[0]; assert sp.expand(f - (x - 5)**2 * (x + 1)) == 0
A1 = localmax(f); assert len(A1) == 1; A1 = A1[0]
Z = g_zeros(f, 6); assert Z == [-7, -1, 1, 5] and sum(Z) == -2
A2 = Z[0]; A3 = gval(f, 6, -2)
got = [parse(s) for s in S2['ans']]
assert got == [A1, A2, A3], (got, A1, A2, A3)
assert (A1, A2, A3) == (32, -7, -630)
print('S2 답', A1, A2, A3, '· f =', sp.factor(f))
# g의 연속성을 수치로도 확인: 단순근 -1 좌우에서 g→0, g(-1)=0
for e in (R(1, 10**6), -R(1, 10**6)): assert abs(gval(f, 6, -1 + e)) < R(1, 10**3)
assert gval(f, 6, -1) == 0
# 답이 본문에 나온 수(1, 6, 0, -2)와 다르고 서로 다름
assert len({A1, A2, A3}) == 3 and not ({A1, A2, A3} & {1, 6, 0, -2, 4})
# 배점 합 10, (1)이 가장 큼
pts = [int(re.match(r'(\d+)점', t).group(1)) for _, t in S2['subs']]
assert sum(pts) == 10 and pts[0] == max(pts) and len(pts) == 3
assert all('답만' in t for _, t in S2['subs'])
# 본문 점검: '다음' 겹침 없음, 맨 부등호 없음, 금지어 없음
txt = S2['body'] + ''.join(v for _, v in S2.get('cond', [])) + ''.join(s for s, _ in S2['subs'])
assert txt.count('다음') <= 1 and '이러한' not in txt and '이와 같은' not in txt
for fld in ('body', 'fast', 'wrong', 'note'): assert not re.search(r'\\\([^)]*?[<>]', S2[fld]), fld
for fld in ('rubric', 'sol'):
    for t in S2[fld]: assert not re.search(r'\\\((?:(?!\\\)).)*?[<>]', t), fld

# ---- wrong에 적은 값 계산
W = S2['wrong']
fo = (x - a)**2 * (x - a - 6)                                  # 원문에서 외운 꼴
assert localmax(fo.subs(a, 0)) == [0] and fo.subs(a, 0).subs(x, 4) == -32
assert localmax(((x - a)**2 * (x - a + 3)).subs(a, 0)) == [4]
assert sp.solve(sp.Eq(4 * a + 22, -2), a) == [-6]
a2 = sp.solve(sp.Eq(4 * a - 4, -2), a)[0]; assert a2 - 6 == -R(11, 2)
a3 = sp.solve(sp.Eq((a - 12) + (a - 6) + (a - 2) + a, -2), a)[0]; assert a3 - 12 == -R(15, 2)
fp = sp.diff(f, x)
assert 2 * fp.subs(x, -2) * f.subs(x, 4) == 630 and -fp.subs(x, -2) * f.subs(x, 4) == -315 and fp.subs(x, -2) * f.subs(x, 4) == 315
assert f.subs(x, -2) == -49 and f.subs(x, -2) * (-126) == 6174
for wv in (r'\(0\)', r'\(-32\)', r'\(4\)', r'\(-6\)', r'-\dfrac{11}{2}', r'-\dfrac{15}{2}', r'\(5\)', r'\(630\)', r'\(-315\)', r'\(315\)', r'\(6174\)'):
    assert wv in W, wv
assert not ({0, -32, 4, -6, -R(11, 2), -R(15, 2), 5, 630, -315, 315, 6174} & {A1}) and A2 not in (-6, -R(11, 2), -R(15, 2), 5) and A3 not in (630, -315, 315, 6174)

# ---- 원문 M67 직접 풀이: g=f(x-3)×k, 합 7, f(5)=108
so = solve_all(1, -3, 7)
assert len(so) == 1 and sp.expand(so[0] - (x + 1)**2 * (x - 2)) == 0 and so[0].subs(x, 5) == 108 == int(F.I['M67'][2])
# 후보_순위 2의 출처 LIVE1-02-279(대진고 2022 15번): 합 3, f(3)=50
sl = solve_all(1, -3, 3); assert len(sl) == 1 and sl[0].subs(x, 3) == 50
print('원문 M67 f(5)=108, LIVE1-02-279 f(3)=50 확인')

# ---- 조건 빼 보기
def abl(name, msg): print(f'ABLATION S2 {name}: {msg}')
# 최고차항의 계수 1
s2 = solve_all(2, 6, -2); assert len(s2) == 1 and localmax(s2[0]) == [64] and gval(s2[0], 6, -2) == 4 * A3
abl('최고차항의 계수 1', '필요(2이면 극댓값 64, g(-2)=-2520으로 바뀜; 없으면 값이 정해지지 않음)')
# 이동량 6
s3 = solve_all(1, 3, -2); assert len(s3) == 1 and localmax(s3[0]) == [4] and g_zeros(s3[0], 3)[0] != A2
abl('f(x+6)의 6', '필요(3이면 극댓값 4, 네 실근도 달라짐)')
s3b = solve_all(1, -6, -2); assert len(s3b) == 1 and localmax(s3b[0]) == [0] and g_zeros(s3b[0], -6)[0] == -6
abl('f(x+6)의 방향', '필요(f(x-6)이면 가장 작은 근에서 접해 극댓값 0, 가장 작은 실근 -6)')
# 연속: 빼면 다른 f도 가능 — f=(x-5/2)^3-3(x-5/2)+18 (실근 -1/2 하나, 극점 3/2, 7/2)
fc = (x - R(5, 2))**3 - 3 * (x - R(5, 2)) + 18
zc = g_zeros(fc, 6)
assert len(zc) == 4 and sum(zc) == -2 and not g_cont(fc, 6) and localmax(fc) == [20] and zc[0] == -R(13, 2)
abl('g(x)가 실수 전체의 집합에서 연속', '필요(빼면 f=(x-5/2)^3-3(x-5/2)+18도 네 실근·합 -2에 맞아 극댓값 20, 가장 작은 실근 -13/2로 값이 정해지지 않음)')
# 서로 다른 네 실근: 빼고 합만 두면 삼중근도 가능
s5 = solve_all(1, 6, -2, need4=False)
assert len(s5) == 2 and any(localmax(t) == [] for t in s5)
f5 = [t for t in s5 if localmax(t) == []][0]; assert sp.expand(f5 - (x - 2)**3) == 0 and g_zeros(f5, 6) == [-4, 2]
abl('서로 다른 네 실근', '필요(실근 개수를 빼면 f=(x-2)^3도 연속이고 실근 -4, 2의 합이 -2라 극댓값이 없는 경우가 생김)')
# 합 -2
s6 = solve_all(1, 6, 2); assert len(s6) == 1 and localmax(s6[0]) == [32] and g_zeros(s6[0], 6)[0] == -6 != A2 and gval(s6[0], 6, -2) != A3
abl('네 실근의 합 -2', '필요((2)·(3): 합이 2이면 가장 작은 실근 -6, g(-2)도 달라짐; (1)에는 쓰이지 않음)')
print('ALL OK')
