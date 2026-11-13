# -*- coding: utf-8 -*-
# 서답형1 (자체, J69 유형) · 서답형2 (M55 학교식) 검증 · author='claude'
import sympy as sp, os, sys, re, itertools
t, s, x = sp.symbols('t s x', real=True)
A, B, C = sp.symbols('A B C', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


# ================= S1 =================
def second_piece(v1, acc, p):
    """t>=p 에서 v(t) = v1(p) + ∫_p^t acc(s) ds"""
    return sp.expand(v1.subs(t, p) + sp.integrate(acc.subs(t, s), (s, p, t)))

def moved(pieces):
    """pieces=[(식, 시작, 끝)]: 식이 0이 되는 시각에서 나누어 |정적분|을 더한 움직인 거리와 조각별 정적분"""
    tot, parts = 0, []
    for e, lo, hi in pieces:
        rs = sorted(set(r for r in sp.Poly(e, t).real_roots() if lo < r < hi))
        pts = [lo] + rs + [hi]
        for a_, b_ in zip(pts, pts[1:]):
            v = sp.integrate(e, (t, a_, b_)); tot += abs(v); parts.append(v)
    return tot, parts

# --- 원문 J69: 0<=t<=2 v=2t^3-8t, t>=2 a=6t+4, [0,3] 거리 17
v1o = 2 * t**3 - 8 * t; ao = 6 * t + 4
v2o = second_piece(v1o, ao, 2)
assert v2o == 3 * t**2 + 4 * t - 20 and v1o.subs(t, 2) == 0 and sp.diff(v1o, t).subs(t, 2) == ao.subs(t, 2) == 16
do, po = moved([(v1o, 0, 2), (v2o, 2, 3)])
assert do == 17 and po == [-8, 9] and F.I['J69'][2] == '17'
print('J69 원문 OK: v=3t^2+4t-20 (t>=2), 거리 8+9=17 (원문 정답 17)')

# --- S1: 0<=t<=2 v=t^3-3t^2+4t, t>=2 a=-6t+16, [0,6] 거리
v1 = t**3 - 3 * t**2 + 4 * t; acc = -6 * t + 16; P1, T1 = 2, 6
assert r"v(t)=t^3-3t^2+4t" in S1['body'] and r"a(t)=-6t+16" in S1['body'] and r"0\le t\le2" in S1['body'] and r"t\ge2" in S1['body']
assert r"t=6" in S1['subs'][1][0] and r"t=0" in S1['subs'][1][0]
# 이음 시각에서 조건이 어긋나지 않음: 앞 조각의 v'(2) = a(2)
assert sp.diff(v1, t).subs(t, P1) == acc.subs(t, P1) == 4
v2 = second_piece(v1, acc, P1)
assert v2 == -3 * t**2 + 16 * t - 16 and v1.subs(t, P1) == 4 == v2.subs(t, P1)
assert sp.expand(v2 + (3 * t - 4) * (t - 4)) == 0
assert S1['ans'][0] == r'(1) \(v(t)=-3t^2+16t-16\)'
# (1) 적분상수: -3t^2+16t+C, v(2)=4 → C=-16 (하나로 정해짐)
Cc = sp.Symbol('Cc'); solC = sp.solve((-3 * t**2 + 16 * t + Cc).subs(t, 2) - v1.subs(t, 2), Cc)
assert solC == [-16]
# 부호: [0,2] v>=0 (t^2-3t+4 판별식<0), [2,4] v>=0, [4,6] v<=0 → 방향 전환은 t=4 한 번
assert sp.expand(v1 - t * (t**2 - 3 * t + 4)) == 0 and sp.discriminant(t**2 - 3 * t + 4, t) < 0
assert all(v1.subs(t, R(i, 50)) > 0 for i in range(1, 101))
assert all(v2.subs(t, 2 + R(i, 50)) > 0 for i in range(0, 100)) and v2.subs(t, 4) == 0
assert all(v2.subs(t, 4 + R(i, 50)) < 0 for i in range(1, 101))
assert [r for r in sp.Poly(v1, t).real_roots() if 0 < r <= 2] == [] and [r for r in sp.Poly(v2, t).real_roots() if r >= 2] == [4]
d1, p1 = moved([(v1, 0, P1), (v2, P1, T1)])
assert p1 == [4, 8, -24] and d1 == 36
assert S1['ans'][1] == r'(2) \(36\)'
# 부정적분 꼴(빠른 풀이): -t(t-4)^2 의 도함수가 v2
assert sp.expand(sp.diff(-t * (t - 4)**2, t) - v2) == 0 and [(-tv * (tv - 4)**2) for tv in (2, 4, 6)] == [-8, 0, -24]
# 수치 확인: ∫_0^6 |v|
vf1, vf2 = sp.lambdify(t, v1), sp.lambdify(t, v2)
n = 60000; h = 6 / n
num = sum(abs(vf1(i * h) if i * h <= 2 else vf2(i * h)) * (0.5 if i in (0, n) else 1) for i in range(n + 1)) * h
assert abs(num - 36) < 1e-4, num
# 오답 값
assert sp.integrate(v1, (t, 0, 2)) + sp.integrate(v2, (t, 2, 6)) == -12                 # 부호 조사 없이 → 12
assert 4 + abs(sp.integrate(v2, (t, 2, 6))) == 20                                        # t=2 에서만 나눔
assert moved([(v1, 0, 2), (v2, 2, 4)])[0] == 12                                          # t=4 까지만
assert sp.expand(-3 * t**2 + 16 * t - 20 + (3 * t - 10) * (t - 2)) == 0                  # v(2)=0 으로 둔 식
assert moved([(v1, 0, 2), (-3 * t**2 + 16 * t, 2, 6)])[0] != 36                          # 적분상수 누락이면 다른 값
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['4점, 풀이과정을 상세히 쓰시오.', '6점, 풀이과정을 상세히 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S1['rubric'][:2]]
assert [sum(a_) for a_ in pts1] == [4, 6] and sum(map(sum, pts1)) == 10, pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
print("S1 OK: (1) v=-3t^2+16t-16=-(3t-4)(t-4), (2) [0,2] 4 + [2,4] 8 + [4,6] 24 = 36, 방향 전환은 t=4 한 번")

# ----- 조건 빼 보기 S1
def abl1(cname, msg): print(f'ABLATION S1 {cname}: {msg}')
def fmt(v): return str(v) if sp.sympify(v).is_rational else f'{float(v):.3f}'
# (a) 앞 조각의 속도 식 삭제: v(2) 를 모르면 적분상수가 남아 거리가 정해지지 않음
ds = set()
for cv in [-20, -16, -12, 0]:
    ds.add(moved([(-3 * t**2 + 16 * t + cv, 2, 6)])[0])
assert len(ds) == 4
abl1('0≤t≤2일 때 v(t)=t^3-3t^2+4t', '필요(없으면 v(2)를 몰라 적분상수가 남고, 상수에 따라 [2,6] 거리가 ' + ', '.join(fmt(d_) for d_ in sorted(ds, key=float)) + '로 달라짐)')
# (b) 가속도 식의 상수 16 → 다른 값: v(t), 전환 시각, 거리가 모두 바뀜
alt = {}
for kv in [12, 14, 16, 18]:
    vv = second_piece(v1, -6 * t + kv, 2); alt[kv] = moved([(v1, 0, 2), (vv, 2, 6)])[0]
assert alt[16] == 36 and len(set(alt.values())) == 4
abl1('t≥2일 때 a(t)=-6t+16', '필요(상수를 바꾸면 거리가 ' + ', '.join(f'상수 {k_}이면 {fmt(v_)}' for k_, v_ in alt.items()) + '로 달라짐)')
# (c) 가속도 조건의 시작 시각 2 → 3 (앞 조각을 t=3 까지 쓴다고 읽으면): 값이 달라짐
vv3 = second_piece(v1, acc, 3); d3 = moved([(v1, 0, 3), (vv3, 3, 6)])[0]
assert d3 != 36
abl1('식이 바뀌는 시각 2', f'필요(시각을 3으로 바꾸면 거리 {fmt(d3)})')
# (d) 끝 시각 6
ends = {Tv: moved([(v1, 0, 2), (v2, 2, Tv)])[0] for Tv in (4, 5, 6)}
assert ends == {4: 12, 5: 17, 6: 36}
abl1('끝 시각 6', f'필요(끝 시각 4, 5, 6에서 거리 {ends[4]}, {ends[5]}, {ends[6]})')


# ================= S2 =================
def nroots(expr):
    """다항식의 서로 다른 실근의 개수"""
    return len(set(sp.Poly(sp.expand(expr), x).real_roots()))

def solve_two_lines(m1, m2, p, dv, sign=1):
    """g(x)=x(Ax^2+Bx+C) (공통점을 원점으로 옮긴 삼차), g(x)-m1 x=0 과 g(x)-m2 x=0 의 서로 다른 실근이 각각 2개,
    g'(p)=dv, 최고차항 계수의 부호 sign. 네 경우(공통점에서 접함 C=m / 판별식 0)를 전수 조사해 (A,B,C) 목록을 돌려준다."""
    out = set()
    conds = {m: [C - m, B**2 - 4 * A * (C - m)] for m in (m1, m2)}
    for e1, e2 in itertools.product(conds[m1], conds[m2]):
        for so in sp.solve([e1, e2, 3 * A * p**2 + 2 * B * p + C - dv], [A, B, C], dict=True):
            if any(v.free_symbols for v in so.values()) or len(so) < 3: 
                raise RuntimeError(('해가 한없이 많음', e1, e2, so))
            a_, b_, c_ = so[A], so[B], so[C]
            if not all(v.is_real for v in (a_, b_, c_)) or a_ == 0 or sp.sign(a_) != sign: continue
            g = x * (a_ * x**2 + b_ * x + c_)
            if nroots(g - m1 * x) == 2 and nroots(g - m2 * x) == 2: out.add((a_, b_, c_))
    return sorted(out, key=lambda z: float(z[0]))

# --- 원문 M55: f(0)=0, f-x=0·f+x=0 실근 2개씩, f'(1)=1, 최고차항 양수 → f(3)=51
so = solve_two_lines(1, -1, 1, 1)
assert so == [(R(32, 9), -R(16, 3), 1)]
fo = x * (so[0][0] * x**2 + so[0][1] * x + so[0][2])
assert fo.subs(x, 3) == 51 and F.I['M55'][2] == '51'
print('M55 원문 OK: f=(32/9)x^3-(16/3)x^2+x, f(3)=51 (원문 정답 51)')

# --- S2: f(0)=1, f-5x-1=0·f+4x-1=0 실근 2개씩, f'(2)=5, 최고차항 양수
assert r"f(x)-5x-1=0" in S2['body'] and r"f(x)+4x-1=0" in S2['body'] and r"f(0)=1" in S2['body'] and r"f'(2)=5" in S2['body'] and '양수' in S2['body']
M1, M2, PP, DV, LV = 5, -4, 2, 5, 1
sols = solve_two_lines(M1, M2, PP, DV)
assert sols == [(4, -12, 5)], sols                                   # 하나로 정해짐
a2, b2, c2 = sols[0]
f2 = sp.expand(x * (a2 * x**2 + b2 * x + c2) + LV)
assert f2 == 4 * x**3 - 12 * x**2 + 5 * x + 1
# 조건을 직접 다시 확인
assert f2.subs(x, 0) == 1 and sp.diff(f2, x).subs(x, 2) == 5 and sp.LC(f2, x) > 0
assert nroots(f2 - 5 * x - 1) == 2 and nroots(f2 + 4 * x - 1) == 2
assert sp.factor(f2 - 5 * x - 1) == 4 * x**2 * (x - 3) and sp.expand(f2 + 4 * x - 1 - x * (2 * x - 3)**2) == 0
# 격자 전수(경우 나누기와 따로): f'(2)=5 로 C=5-12A-4B 를 정하고 A, B 를 1/4 간격으로 훑어 두 개수 조건을 직접 센다
hits = []
for ai in range(1, 41):
    for bi in range(-120, 121):
        av, bv = R(ai, 4), R(bi, 4); cv = 5 - 12 * av - 4 * bv
        # x(Ax^2+Bx+C-m)=0 의 서로 다른 실근 수를 판별식으로 센다
        def cnt(m):
            q0 = cv - m; D = bv**2 - 4 * av * q0
            if D < 0: return 1
            if D == 0: return 1 if bv == 0 else 2
            return 2 if q0 == 0 else 3
        if cnt(5) == 2 and cnt(-4) == 2: hits.append((av, bv, cv))
assert hits == [(4, -12, 5)], hits
# (1) f'(0)
ANS1 = sp.diff(f2, x).subs(x, 0)
assert ANS1 == 5 and S2['ans'][0] == r'(1) \(5\)'
# (2) 직선 y=-4x+1 과 접하는 점: f+4x-1 = 4x(x-3/2)^2
h2 = sp.expand(f2 + 4 * x - 1)
tang = [r for r in sp.Poly(h2, x).real_roots() if sp.diff(h2, x).subs(x, r) == 0]
assert set(tang) == {R(3, 2)} and sp.diff(f2, x).subs(x, R(3, 2)) == -4 and f2.subs(x, R(3, 2)) == -4 * R(3, 2) + 1
assert S2['ans'][1] == r'(2) \(\dfrac{3}{2}\)'
# (2)는 판별식 없이 b=-3a 만으로 정해짐: -b/(2a) = 3/2
assert sp.simplify((-B / (2 * A)).subs(B, -3 * A)) == R(3, 2)
# (3) f(1)
ANS3 = f2.subs(x, 1)
assert ANS3 == -2 and S2['ans'][2] == r'(3) \(-2\)'
# 묻는 점: b=-3a, c=5 만 쓰면 f(1)=6-2a (a 필요), f(3)=16 (a 없이 나옴 → f(3)을 묻지 않음)
fa = x * (A * x**2 - 3 * A * x + 5) + 1
assert sp.expand(fa.subs(x, 1)) == 6 - 2 * A and sp.expand(fa.subs(x, 3)) == 16
assert r"f(1)" in S2['subs'][2][0] and r"f'(0)" in S2['subs'][0][0] and r"y=-4x+1" in S2['subs'][1][0]
# LIVE1-02-224(기울기 ±2, f'(1)=2, f(1)=-14/9)·원문과 수치가 다름
so224 = solve_two_lines(2, -2, 1, 2)
assert so224 == [(R(64, 9), -R(32, 3), 2)] and (x * (so224[0][0] * x**2 + so224[0][1] * x + 2)).subs(x, 1) == -R(14, 9)
# 오답 값
assert M2 == -4                                                                          # (1) 접선을 y=-4x+1 로 잡음
assert sorted(set(sp.Poly(f2 - 5 * x - 1, x).real_roots())) == [0, 3]                    # (2) y=5x+1 과 다시 만나는 점 3
assert f2.subs(x, 1) - 1 == -3                                                           # (3) +1 빠뜨림
aw = [r for r in sp.solve(9 * A**2 - 20 * A, A) if r > 0][0]
assert aw == R(20, 9) and fa.subs({A: aw, x: 1}) == R(14, 9)                             # b^2=20a
aw2 = [r for r in sp.solve(9 * A**2 - 4 * A, A) if r > 0][0]
assert aw2 == R(4, 9) and fa.subs({A: aw2, x: 1}) == R(46, 9)                            # b^2=4a
# 배점·형식: 소문항 3개 3+3+4, 답만. 조건 상자 없음
assert 'cond' not in S2 and len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['3점, 답만 적으시오.', '3점, 답만 적으시오.', '4점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S2['rubric'][:3]]
assert pts2 == [[3], [3], [4]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert S2['rubric'][0].startswith(r'(1) \(5\)') and S2['rubric'][1].startswith(r'(2) \(\dfrac{3}{2}\)') and S2['rubric'][2].startswith(r'(3) \(-2\)')
assert all('채점자 참고용' in line for line in S2['rubric'][:3])
assert S2['db_ref'] == 'M55 후보_순위 1' and S1['db_ref'] == '자체 (가장 가까운 J69)' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'}
print("S2 OK: f=4x^3-12x^2+5x+1 하나, (1) f'(0)=5 (2) 접점 x=3/2 (3) f(1)=-2")

# ----- 조건 빼 보기 S2
def abl2(cname, msg): print(f'ABLATION S2 {cname}: {msg}')
# (a) 최고차항의 계수가 양수 → 삭제: 음수 쪽 해가 둘 더 생김
neg = solve_two_lines(M1, M2, PP, DV, sign=-1)
assert neg == [(-R(9, 4), 9, -4), (-R(1, 4), 3, -4)]
abl2('최고차항의 계수가 양수', "필요(없으면 음수인 f가 둘 더 생김: " + ', '.join(f"a={a_}, b={b_}, f'(0)={c_}" for a_, b_, c_ in neg) + ')')
# (b) f(0)=1 삭제: 곡선이 두 직선의 교점 (0,1)을 지나지 않아도 되는 예 (두 직선에 각각 접함)
fb = R(9, 8) * (x - 2)**2 * (x - 9) + 5 * x + 1
assert sp.expand(fb + 4 * x - 1 - R(9, 8) * (x - 6)**2 * (x - 1)) == 0
assert nroots(fb - 5 * x - 1) == 2 and nroots(fb + 4 * x - 1) == 2 and sp.diff(fb, x).subs(x, 2) == 5 and sp.LC(sp.expand(fb), x) > 0
assert fb.subs(x, 0) == -R(79, 2) and sp.diff(fb, x).subs(x, 0) == 50
abl2('f(0)=1', "필요(없으면 f=(9/8)(x-2)^2(x-9)+5x+1 도 나머지 조건을 모두 만족시킴: f'(0)=50)")
# (c) f'(2)=5 삭제: c=5, b^2=36a 만 남아 a 가 정해지지 않음
exs = []
for av in [1, 4, 9]:
    bv = -6 * sp.sqrt(av); g = x * (av * x**2 + bv * x + 5)
    assert nroots(g - 5 * x) == 2 and nroots(g + 4 * x) == 2
    exs.append((av, g.subs(x, 1) + 1))
assert len({v for _, v in exs}) == 3
abl2("f'(2)=5", '필요(없으면 a가 정해지지 않음: ' + ', '.join(f'a={a_}일 때 f(1)={v_}' for a_, v_ in exs) + ')')
# (d) 방정식 f(x)-5x-1=0 의 조건 삭제: 직선 y=-4x+1 이 (0,1)에서 접하는 함수도 됨
gd = x * (x**2 - R(3, 4) * x - 4)
assert nroots(gd + 4 * x) == 2 and sp.diff(gd, x).subs(x, 2) == 5 and nroots(gd - 5 * x) == 3
abl2('f(x)-5x-1=0의 실근 2개', "필요(없으면 f=x^3-(3/4)x^2-4x+1 도 됨: f'(0)=-4)")
# (e) 방정식 f(x)+4x-1=0 의 조건 삭제: c=5, b=-3a 만 남아 a 가 정해지지 않음
ge = x * (x**2 - 3 * x + 5)
assert nroots(ge - 5 * x) == 2 and sp.diff(ge, x).subs(x, 2) == 5 and nroots(ge + 4 * x) == 1 and ge.subs(x, 1) + 1 == 4
abl2('f(x)+4x-1=0의 실근 2개', '필요(없으면 f=x^3-3x^2+5x+1 도 됨: f(1)=4, 접점 없음)')
# (f) 개수 2 → 3 으로 바꾸면: c≠5, 판별식>0 인 범위가 남아 정해지지 않음
cnt3 = [(av, bv) for av in (1, 2) for bv in (0, 1, 2) if nroots(x * (av * x**2 + bv * x + (5 - 12 * av - 4 * bv)) - 5 * x) == 3 and nroots(x * (av * x**2 + bv * x + (5 - 12 * av - 4 * bv)) + 4 * x) == 3]
assert len(cnt3) >= 2
abl2('실근의 개수 2', f'필요(개수를 3으로 바꾸면 (a,b)={cnt3[:3]} 등 여러 함수가 됨)')

print('ALL OK')
