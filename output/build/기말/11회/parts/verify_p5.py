# -*- coding: utf-8 -*-
# 17번 후보 A17 (J41: 평행이동한 두 삼차곡선, 한 교점의 x좌표 a-1, 두 교점이 제1사분면 → 둘러싸인 넓이의 최댓값) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a, b = sp.symbols('x a b', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def meet(fx, av, bv):
    """두 곡선 y=f(x), y=f(x-a)+b 의 교점 목록(정확). 차가 0이면 None(일치)."""
    h = sp.expand(fx - fx.subs(x, x - av) - bv)
    if h == 0:
        return None
    return sorted(set(sp.solve(h, x)), key=lambda t: float(t)) if sp.Poly(h, x).degree() > 0 else []


def area(fx, av, bv):
    """두 곡선으로 둘러싸인 부분의 넓이(교점 2개일 때), 아니면 None"""
    P = meet(fx, av, bv)
    if P is None or len(P) != 2 or not all(t.is_real for t in P):
        return None
    h = sp.expand(fx - fx.subs(x, x - av) - bv)
    return sp.nsimplify(sp.Abs(sp.integrate(h, (x, P[0], P[1]))))


def feasible(fx, av, shift=1, quad=True):
    """(나): 한 교점의 x좌표가 a-shift → b 결정. (가): 서로 다른 두 교점, (quad이면) 모두 제1사분면."""
    if av == 0:
        return None
    bv = fx.subs(x, av - shift) - fx.subs(x, -shift)
    P = meet(fx, av, bv)
    if P is None or len(P) != 2:
        return None
    if quad and not all(t > 0 and fx.subs(x, t) > 0 for t in P):
        return None
    return bv


# ---------- 1) 함수와 풀이 줄
f = -x**3 + 9*x**2 + 10*x
assert sp.factor(f) == sp.factor(-x*(x + 1)*(x - 10)) and f.subs(x, -1) == 0 and f.subs(x, 7) == 168
h = sp.expand(f - f.subs(x, x - a) - b)
assert sp.expand(h - (-3*a*x**2 + (3*a**2 + 18*a)*x - a**3 - 9*a**2 + 10*a - b)) == 0
hb = sp.expand(h.subs(b, f.subs(x, a - 1)))
assert sp.factor(hb) == sp.factor(-3*a*(x - a + 1)*(x - 7))
print('h(x) = -3a(x-a+1)(x-7): 다른 교점은 a와 관계없이 (7, 168)')
Sa = sp.expand(a*(8 - a)**3 / 2)
assert sp.expand(sp.integrate(hb, (x, a - 1, 7)) - Sa) == 0
assert sp.factor(sp.diff(Sa, a)) == sp.factor(2*(8 - a)**2*(2 - a))

# ---------- 2) 조건을 만족시키는 a의 범위 (정확 전수: a 눈금 1/8)
grid = [R(n, 8) for n in range(-160, 161)]
ok = [av for av in grid if feasible(f, av) is not None]
expect = [av for av in grid if 1 < av < 11 and av != 8]
assert ok == expect, (ok[:5], ok[-5:])
assert feasible(f, R(8)) is None and len(meet(f, 8, 168)) == 1   # a=8: 한 점(7,168)에서 접함
print('조건 ⇔ 1<a<11, a≠8 (a=8은 접함, a≤1·a≥11은 교점이 제1사분면 밖)')

# ---------- 3) 넓이와 최댓값
for av in [R(3, 2), R(2), R(5), R(19, 2), R(21, 2)]:
    bv = feasible(f, av)
    assert area(f, av, bv) == sp.nsimplify(av*abs(8 - av)**3 / 2), av
vals = {av: area(f, av, feasible(f, av)) for av in ok}
mx = max(vals.values()); arg = [av for av in ok if vals[av] == mx]
assert mx == 216 and arg == [2]
# 연속 a: 1<a<8 에서 극대 a=2 하나, 8<a<11 에서 증가(상한 297/2), a→1+ 상한 343/2
assert sp.solve(sp.diff(Sa, a), a) == [2, 8]
assert sp.limit(Sa, a, 1, '+') == R(343, 2) and R(343, 2) < 216
S2 = sp.expand(a*(a - 8)**3 / 2)
assert all(sp.diff(S2, a).subs(a, t) > 0 for t in [R(n, 10) for n in range(81, 110)])
assert S2.subs(a, 11) == R(297, 2) and R(297, 2) < 216
ANS = 216
print('S = a|8-a|^3/2, 최댓값', ANS, '(a=2, b=f(1)=18), 끝 상한 343/2·297/2')

# ---------- 4) 선지
ch = IT['choices']; vs = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs, reverse=True)
print('정답 = 선지 ①, 선지', vs, '공차 36 내림차순')

# ---------- 5) 오답
w1 = sp.Max(*[sp.expand(3*a*(8 - a)**3 / 12).subs(a, av) for av in ok if av < 8])   # 원문 1/12 공식
L = sp.expand(f.subs(x, 1) + sp.diff(f, x).subs(x, 1)*(x - 1))                      # a=2: 직선 A'P = (1,18)에서의 접선
assert sp.expand(L.subs(x, 7) - 168) == 0 and sp.integrate(f - L, (x, 1, 7)) == 108
w2 = sp.Max(*[sp.expand(a*(8 - a)**3 / 6).subs(a, av) for av in ok if av < 8])      # 3 누락
assert w1 == 108 and w2 == 72
assert set(IT['wrongs']) == {'108', '72'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 108(1/12 공식, 직선 A\'P와 곡선 사이 넓이와 같음), 72(이차항 계수 3 누락)')
assert ANS not in {9, 10, 1} and sp.Rational(ANS) != R(27, 32)
print('정답은 본문의 수(9, 10, 1)·원문 답 27/32와 다름')

# ---------- 6) 원문 J41: 27/32
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J41']; assert o[2] == '①' and o[1][0] == r'\dfrac{27}{32}'
f0 = -x**3 + x
a0 = 1; b0 = 2*f0.subs(x, R(1, 2))
assert b0 == R(3, 4) and len(meet(f0, a0, b0)) == 1                 # (가) 오직 한 점 P(1/2, 3/8)
Px, Py = R(1, 2), f0.subs(x, R(1, 2))
line = Py/(Px + 1)*(x + 1)
pts = set(sp.solve(f0 - line, x)) | set(sp.solve(f0.subs(x, x - a0) + b0 - line, x))
assert len(pts) == 3                                                  # (나) 서로 다른 점 3개
S1 = sp.integrate(sp.Abs(f0 - line), (x, -1, R(1, 2)))
S2o = sp.integrate(sp.Abs(f0.subs(x, x - a0) + b0 - line), (x, R(1, 2), 2))
assert sp.nsimplify(S1 + S2o) == R(27, 32)
# 다른 a(눈금)에서는 (나)가 성립하지 않음(원문 정답 유일)
for av in [R(n, 4) for n in range(1, 8) if n != 4]:
    bv = av - av**3/4; p = av/2; ln = f0.subs(x, p)/(p + 1)*(x + 1)
    q = set(sp.solve(f0 - ln, x)) | set(sp.solve(f0.subs(x, x - av) + bv - ln, x))
    assert len([t for t in q if t.is_real]) != 3, av
print('원문 J41 OK: a=1, b=3/4, S1+S2=27/32')
# 원문 원리 줄 불통: 답이 나오는 a=2에서 두 곡선은 서로 다른 두 점(1, 7)에서 만나고(중근 아님), 접하는 a=8은 넓이가 없다
assert meet(f, 2, 18) == [1, 7] and area(f, 8, 168) is None
print('원문 줄 불통: a=2에서 교점 x=1, 7(중근 아님), 접하는 a=8은 둘러싸인 부분이 없음')

# ---------- 7) 문장 길이(원문의 90% 이상)
pl = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))
new_len = len(pl(IT['body'] + ' '.join(c for _, c in IT['cond']))); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def best(fx, shift=1, quad=True, lo=-160, hi=161, den=8):
    """눈금 위 최댓값. 눈금 끝에서 최대이면 '최댓값 없음(커짐)'"""
    G = [R(n, den) for n in range(lo, hi)]
    V = {}
    for av in G:
        bv = feasible(fx, av, shift, quad)
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


# (가) 전체 삭제: (나)만 → a≠0, 8 이면 모두 가능, S=|a||8-a|^3/2 → 끝없이 커짐
ablation('(가) 전체', best(f, quad=False))
# (가)의 '제1사분면'만 삭제(서로 다른 두 점은 둠): 위와 같음
ablation('(가)의 제1사분면', best(f, quad=False))
# (나) 삭제: (a, b) 두 문자 → 두 교점이 제1사분면인 경우 넓이 상한이 216보다 큼(근의 합 a+6으로 두 근 r1<r2를 잡아 셈)
sup = 0
for av in [R(n, 4) for n in range(1, 60)]:
    for r1 in [R(n, 8) for n in range(1, 80)]:
        r2 = av + 6 - r1
        if r2 > r1 and f.subs(x, r1) > 0 and f.subs(x, r2) > 0:
            sup = max(sup, 3*av*(r2 - r1)**3/6)
assert sup > 216
ablation('(나) 한 교점의 x좌표 a-1', f'상한이 커짐 {sp.N(sup, 6)}')
ablation('(나)의 a-1(→a-2)', best(f, shift=2))
ablation('(나)의 a-1(→a)', best(f, shift=0))
ablation('f의 9x^2(→6x^2)', best(-x**3 + 6*x**2 + 10*x))
ablation('f의 9x^2(→0, 기함수 -x^3+10x)', best(-x**3 + 10*x))
ablation('원문 f=-x^3+x', best(-x**3 + x))
print('ALL OK')
