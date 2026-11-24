# -*- coding: utf-8 -*-
# 17번 후보 A17 2판 (J41: 평행이동한 두 삼차곡선, 한 교점의 x좌표 a-4, 두 교점의 좌표가 모두 0 이상 → 둘러싸인 넓이의 최댓값) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a, b = sp.symbols('x a b', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def meet(fx, av, bv):
    """두 곡선 y=f(x), y=f(x-a)+b 의 실수 교점 목록(정확). 일치하면 None."""
    h = sp.expand(fx - fx.subs(x, x - av) - bv)
    if h == 0:
        return None
    if sp.Poly(h, x).degree() == 0:
        return []
    return sorted({t for t in sp.solve(h, x) if t.is_real}, key=float)


def area(fx, av, bv):
    P = meet(fx, av, bv)
    if P is None or len(P) != 2:
        return None
    h = sp.expand(fx - fx.subs(x, x - av) - bv)
    return sp.nsimplify(sp.Abs(sp.integrate(h, (x, P[0], P[1]))))


def feasible(fx, av, shift=4, xc=True, yc=True, closed=True):
    """(나): 한 교점의 x좌표 a-shift → b 결정. (가): 서로 다른 두 교점, 두 좌표 조건(닫힘/열림)."""
    if av == 0:
        return None
    bv = fx.subs(x, av - shift) - fx.subs(x, -shift)
    P = meet(fx, av, bv)
    if P is None or len(P) != 2:
        return None
    ge = (lambda t: t >= 0) if closed else (lambda t: t > 0)
    for t in P:
        if xc and not ge(t): return None
        if yc and not ge(fx.subs(x, t)): return None
    return bv


# ---------- 1) 함수와 풀이 줄
f = -x**3 - 3*x**2 + 10*x + 24
assert sp.factor(f) == sp.factor(-(x + 4)*(x + 2)*(x - 3)) and f.subs(x, -4) == 0 and f.subs(x, 2) == 24
h = sp.expand(f - f.subs(x, x - a) - b)
assert sp.expand(h - (-3*a*x**2 + (3*a**2 - 6*a)*x - a**3 + 3*a**2 + 10*a - b)) == 0
hb = sp.expand(h.subs(b, f.subs(x, a - 4)))
assert sp.factor(hb) == sp.factor(-3*a*(x - a + 4)*(x - 2))
print('h(x) = -3a(x-a+4)(x-2): 다른 교점은 a와 관계없이 (2, 24)')
Sa = sp.expand(a*(6 - a)**3 / 2)
assert sp.expand(sp.integrate(hb, (x, a - 4, 2)) - Sa) == 0
dS = sp.expand(sp.diff(Sa, a))
assert sp.expand(dS - (-4*a**3 + 54*a**2 - 216*a + 216)/2) == 0 and sp.factor(dS) == sp.factor(-(a - 6)**2*(2*a - 3))

# ---------- 2) 조건을 만족시키는 a의 범위 (정확 전수: a 눈금 1/8)
grid = [R(n, 8) for n in range(-160, 161)]
ok = [av for av in grid if feasible(f, av) is not None]
assert ok == [av for av in grid if 4 <= av <= 7 and av != 6], (ok[:3], ok[-3:])
assert feasible(f, R(6)) is None and len(meet(f, 6, f.subs(x, 2))) == 1   # a=6: (2,24)에서 접함
print('조건 ⇔ 4≤a≤7, a≠6 (a=6은 접함)')

# ---------- 3) 넓이와 최댓값
for av in [R(4), R(9, 2), R(5), R(13, 2), R(7)]:
    assert area(f, av, feasible(f, av)) == sp.nsimplify(av*abs(6 - av)**3 / 2), av
vals = {av: area(f, av, feasible(f, av)) for av in ok}
mx = max(vals.values()); arg = [av for av in ok if vals[av] == mx]
assert mx == 16 and arg == [4]
assert sp.solve(dS, a) == [R(3, 2), 6] and not (4 <= R(3, 2) <= 7)          # 극대는 범위 밖
assert all(dS.subs(a, t) < 0 for t in [R(n, 10) for n in range(40, 60)])     # [4,6)에서 감소
S2 = sp.expand(a*(a - 6)**3 / 2)
assert all(sp.diff(S2, a).subs(a, t) > 0 for t in [R(n, 10) for n in range(61, 71)]) and S2.subs(a, 7) == R(7, 2)
ANS = 16
print('S = a|6-a|^3/2, 극대 a=3/2는 범위 밖 → 끝점 a=4에서 최댓값', ANS, '(b=f(0)=24), 오른쪽 끝 7/2')

# ---------- 4) 선지
ch = IT['choices']; vs = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ①, 선지 오름차순 등차', vs[1] - vs[0])

# ---------- 5) 오답
okx = [av for av in grid if av > 0 and feasible(f, av, xc=False) is not None]   # x좌표 조건을 놓치고 a>0(오른쪽 이동)으로만 본 경우
assert okx == [av for av in grid if 2 <= av <= 7 and av != 6]
w1 = max(area(f, av, feasible(f, av, xc=False)) for av in okx)
w2 = max(sp.nsimplify(3*av*abs(6 - av)**3 / 12) for av in okx)
assert w1 == 64 and w2 == 32
assert set(IT['wrongs']) == {'64', '32'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 64(x좌표 조건 놓침 → 2≤a≤7, a=2), 32(그 범위에서 원문 1/12 공식)')
assert ANS not in {3, 10, 24, 4, 0} and R(ANS) != R(27, 32)
print('정답은 본문의 수·원문 답 27/32와 다름')

# ---------- 6) 원문 J41: 27/32
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J41']; assert o[2] == '①' and o[1][0] == r'\dfrac{27}{32}'
f0 = -x**3 + x
a0 = 1; b0 = 2*f0.subs(x, R(1, 2))
assert b0 == R(3, 4) and len(meet(f0, a0, b0)) == 1
Px, Py = R(1, 2), f0.subs(x, R(1, 2))
line = Py/(Px + 1)*(x + 1)
pts = set(sp.solve(f0 - line, x)) | set(sp.solve(f0.subs(x, x - a0) + b0 - line, x))
assert len(pts) == 3
S1 = sp.integrate(sp.Abs(f0 - line), (x, -1, R(1, 2)))
S2o = sp.integrate(sp.Abs(f0.subs(x, x - a0) + b0 - line), (x, R(1, 2), 2))
assert sp.nsimplify(S1 + S2o) == R(27, 32)
for av in [R(n, 4) for n in range(1, 8) if n != 4]:
    bv = av - av**3/4; p = av/2; ln = f0.subs(x, p)/(p + 1)*(x + 1)
    q = set(sp.solve(f0 - ln, x)) | set(sp.solve(f0.subs(x, x - av) + bv - ln, x))
    assert len([t for t in q if t.is_real]) != 3, av
print('원문 J41 OK: a=1, b=3/4, S1+S2=27/32')
assert meet(f, 4, 24) == [0, 2] and area(f, 6, 24) is None
print('원문 줄 불통: 답이 나오는 a=4에서 교점 x=0, 2(중근 아님), 접하는 a=6은 둘러싸인 부분이 없음')

# ---------- 7) 문장 길이(원문의 90% 이상)
pl = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))
new_len = len(pl(IT['body'] + ' '.join(c for _, c in IT['cond']))); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def best(fx, **kw):
    G = grid
    V = {}
    for av in G:
        bv = feasible(fx, av, **kw)
        if bv is not None:
            s = area(fx, av, bv)
            if s is not None:
                V[av] = s
    if not V:
        return '조건을 만족시키는 a 없음'
    m = max(V.values()); am = [t for t in V if V[t] == m]
    if am[0] in (G[0], G[-1]):
        return f'최댓값 없음(a={am[0]}에서 {m}, 끝으로 갈수록 커짐)'
    return m


ablation('(가) 좌표 조건 전체', best(f, xc=False, yc=False))
ablation('(가)의 x좌표 조건', best(f, xc=False))
ablation('(가)의 y좌표 조건', best(f, yc=False))
# (가) 열린 조건(양수): 4<a<7 → a=4 제외, 상한 16에 닿지 않음
op = [av for av in grid if feasible(f, av, closed=False) is not None]
assert min(op) > 4 and all(area(f, av, feasible(f, av, closed=False)) < 16 for av in op)
ablation("(가)의 '0 이상'(→양수)", '최댓값 없음(a→4+에서 16에 다가가기만 함)')
sup = 0
for av in [R(n, 4) for n in range(1, 60)]:
    for r1 in [R(n, 8) for n in range(0, 25)]:
        r2 = av - 2 - r1
        if r2 > r1 and f.subs(x, r1) >= 0 and f.subs(x, r2) >= 0:
            sup = max(sup, 3*av*(r2 - r1)**3/6)
assert sup > 16
ablation('(나) 한 교점의 x좌표 a-4', f'상한이 커짐 {sp.N(sup, 6)}')
ablation('(나)의 a-4(→a-3)', best(f, shift=3))
ablation('(나)의 a-4(→a-2)', best(f, shift=2))
print('ALL OK')
