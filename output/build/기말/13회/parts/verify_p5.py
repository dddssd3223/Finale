# -*- coding: utf-8 -*-
# 17번 후보 A17 2판 (J38: 이어 붙인 함수 g의 극댓값·극솟값의 합, 수평선과 둘러싸인 넓이) 검증 · author='claude'
import sympy as sp, os, sys, re
x, c = sp.symbols('x c', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]

# 연속 → f(x) = x + c(x-1)(x-3)
p_, q_ = sp.symbols('p q')
fg = c*x**2 + p_*x + q_
s = sp.solve([fg.subs(x, 1) - 1, fg.subs(x, 3) - 3], [p_, q_], dict=True)[0]
f = x + c*(x - 1)*(x - 3)
assert sp.expand(fg.subs(s) - f) == 0
pole = sp.solve(sp.diff(f, x), x)[0]
vtx = sp.simplify(f.subs(x, pole))
assert sp.simplify(pole - (2 - 1/(2*c))) == 0 and sp.simplify(vtx - (2 - c - 1/(4*c))) == 0
print('연속 → f = x+c(x-1)(x-3), 극점 2-1/(2c), 그 값 2-c-1/(4c)')


def extrema(cv):
    """g의 (극댓값 목록, 극솟값 목록) — 정확 판정: x=1, 극점, x=3의 좌우 증감"""
    fv = f.subs(c, cv); d = sp.diff(fv, x)
    pv = pole.subs(c, cv)
    mx, mn = [], []
    # x=1: 왼쪽 증가. 오른쪽 f'(1+)
    r1 = d.subs(x, 1)
    if r1 < 0: mx.append(sp.Integer(1))
    # x=3: 오른쪽 증가. 왼쪽 f'(3-)
    l3 = d.subs(x, 3)
    if l3 < 0: mn.append(sp.Integer(3))
    if 1 < pv < 3:
        (mn if cv > 0 else mx).append(fv.subs(x, pv))
    return mx, mn


def extrema_brute(cv, N=6000):
    """눈금으로 직접 찾기(검산용): [-1, 5]에서 이웃보다 큰/작은 점"""
    fv = sp.lambdify(x, f.subs(c, cv))
    g = lambda t: t if (t < 1 or t > 3) else fv(t)
    xs = [-1 + 6*j/N for j in range(N + 1)]; ys = [g(t) for t in xs]
    mx = [ys[i] for i in range(1, N) if ys[i] > ys[i - 1] and ys[i] > ys[i + 1]]
    mn = [ys[i] for i in range(1, N) if ys[i] < ys[i - 1] and ys[i] < ys[i + 1]]
    return mx, mn


for cv in [R(-3), R(-1), R(-3, 5), R(-1, 2), R(-1, 4), R(1, 10), R(1, 4), R(1, 2), R(3, 5), R(1), R(5, 4), R(2), R(4)]:
    a1, b1 = extrema(cv); a2, b2 = extrema_brute(cv)
    assert len(a1) == len(a2) and len(b1) == len(b2), cv
    assert all(abs(float(u) - v) < 1e-3 for u, v in zip(a1, a2)) and all(abs(float(u) - v) < 1e-3 for u, v in zip(b1, b2)), cv
print('극값 판정 OK: |c|≤1/2 없음 · c<-1/2 극대(조각 안)·극소 3(이음점) · c>1/2 극대 1(이음점)·극소(조각 안)')

# 합 조건: 경우별 방정식
K = R(7, 4)
neg = [t for t in sp.solve(sp.Eq(vtx + 3, K), c) if t.is_real and t < R(-1, 2)]
pos_all = sp.solve(sp.Eq(1 + vtx, K), c)
pos = [t for t in pos_all if t > R(1, 2)]
assert neg == [] and sorted(pos_all) == [R(1, 4), 1] and pos == [1]
# c<-1/2이면 합 > 6
u = sp.symbols('u', positive=True)
assert sp.simplify((vtx + 3).subs(c, -u) - (5 + u + 1/(4*u))) == 0 and sp.minimum(u + 1/(4*u), u, sp.Interval.open(0, sp.oo)) == 1
# 눈금 전수: 극댓값·극솟값을 모두 갖고 합이 7/4인 c
grid = [R(n, 40) for n in range(-200, 201) if n != 0]
sol = []
for cv in grid:
    a_, b_ = extrema(cv)
    if len(a_) == 1 and len(b_) == 1 and a_[0] + b_[0] == K: sol.append(cv)
    assert len(a_) <= 1 and len(b_) <= 1
assert sol == [1]
c0 = sp.Integer(1); f0 = sp.expand(f.subs(c, c0))
assert f0 == x**2 - 3*x + 3
print('조건 → c =', c0, ', f =', f0, '(c=1/4은 극값이 없어 버림, c<0은 합>6)')

# 넓이: 그래프와 직선 y=1
inter = sorted(sp.solve(sp.Eq(f0, 1), x)); assert inter == [1, 2]
assert all(f0.subs(x, 1 + R(j, 20)) < 1 for j in range(1, 20)) and all(f0.subs(x, 2 + R(j, 20)) > 1 for j in range(1, 21))
S = sp.integrate(1 - f0, (x, 1, 2))
ANS = 12*S
print('S =', S, ', 12S =', ANS)
assert S == R(1, 6)

# 선지
ch = IT['choices']; vs = [int(t) for t in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ②, 선지 오름차순 등차', vs[1] - vs[0])

# 오답
fq = f.subs(c, R(1, 4)); rq = sorted(sp.solve(sp.Eq(fq, 1), x)); assert rq == [-1, 1]
w4 = 12*R(1, 4)*(rq[1] - rq[0])**3/6                       # c=1/4을 거르지 않음 + 공식
w4b = 12*R((2 - 1)**3, 3)                                  # c=1에서 분모 3
w1 = 12*sp.integrate(1 - f0, (x, 1, R(3, 2)))              # 극소점까지만 적분
assert w4 == 4 and w4b == 4 and w1 == 1 and extrema(R(1, 4)) == ([], [])
cc = sp.solve(sp.Eq(1 + f.subs(x, 2), K), c)[0]            # 꼭짓점 x=2로 잡는 원문 습관
assert cc == R(5, 4) and 12*cc*(2 - 1/cc)**3/6 == R(108, 25)
assert set(IT['wrongs']) == {'1', '4'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 4(c=1/4을 거르지 않음 · 분모 3), 1(극소점까지만 적분) · 꼭짓점 습관은 108/25로 선지 밖')
assert ANS not in {1, 3, R(7, 4), 12} and ANS != 28
print('정답은 본문의 수·원문 답 28과 다름')

# 원문 J38
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J38']; assert o[2] == '28'
So = sp.integrate(x, (x, 0, 4)) + sp.integrate(f - x, (x, 1, 3))
co = sp.solve(sp.Eq(So, R(34, 3)), c)[0]
xm = pole.subs(c, co); M = f.subs({c: co, x: xm})
assert co == R(-5, 2) and xm == R(11, 5) and M == R(23, 5) and M.p + M.q == 28
print('원문 J38 OK: c=-5/2, 최댓값 23/5, 28')
# 원문 줄 불통: 원문의 자리(c<0)는 조건에서 빠지고, 묻는 넓이는 조각 넓이 4|c|/3과 다름
assert neg == [] and S != R(4, 3)*c0
print('원문 줄 불통: c<0은 모두 조건 밖 · 묻는 넓이 1/6 ≠ 조각 넓이 4/3')

# 문장 길이(원문의 90% 이상)
pl = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'])); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9*org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def solve_K(Kv, line=1):
    out = []
    for t in sp.solve(sp.Eq(1 + vtx, Kv), c):
        if t.is_real and t > R(1, 2): out.append(t)
    for t in sp.solve(sp.Eq(vtx + 3, Kv), c):
        if t.is_real and t < R(-1, 2): out.append(t)
    res = []
    for t in out:
        ft = f.subs(c, t)
        rs = sorted(r for r in sp.solve(sp.Eq(ft, line), x) if r.is_real and 1 <= r <= 3)
        res.append(12*sp.Abs(sp.integrate(line - ft, (x, rs[0], rs[-1]))) if len(rs) == 2 else '둘러싸인 부분 없음')
    return res


assert solve_K(K) == [ANS]
ablation('합 7/4(→3/2)', solve_K(R(3, 2))[0])
ablation('합 7/4(→25/4, 위로 볼록한 쪽)', solve_K(R(25, 4))[0])
ablation('직선 y=1(→y=3)', solve_K(K, line=3)[0])
# 합 조건 전체를 빼면 c가 정해지지 않음: c=1, 2에서 넓이가 다름
A1 = [12*sp.integrate(1 - f.subs(c, t), (x, 1, 3 - 1/sp.Integer(t))) for t in (1, 2)]
assert A1[0] != A1[1]
ablation('극값의 합 조건 전체', f'정해지지 않음(c=1이면 {A1[0]}, c=2이면 {A1[1]})')
# 연속을 빼면 f가 정해지지 않음: f=x^2-3x+3+q (1<x<3에서만 바뀜)도 q가 작으면 극댓값·극솟값이 달라져 조건식이 바뀜
ablation('연속', '정해지지 않음(f(1), f(3)이 자유여서 이음점의 값과 조각의 꼴이 정해지지 않음)')
print('ALL OK')
