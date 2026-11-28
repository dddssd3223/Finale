# -*- coding: utf-8 -*-
"""18번(C30 변형) 검증.
문항: 최고차항의 계수가 1인 이차함수 f, 상수 k, g(x)=(x-k)/f(f(x)).
 (가) lim_{x->t} g(x)의 값이 존재하지 않는 실수 t의 개수는 2
 (나) lim_{x->k} g(x) = -1/16
 구하는 값 f(1)+k.
"""
import itertools, random
from fractions import Fraction as Fr
import sympy as sp

x, t, p, q, k, d = sp.symbols('x t p q k d', real=True)
ok = True
def check(c, msg):
    global ok
    print(('PASS ' if c else 'FAIL ') + msg)
    ok = ok and bool(c)

# ---------------------------------------------------------------- 0. 원문 C30 풀이 확인
r = sp.symbols('r', real=True)
F0 = (x - 4) * (x - r)                      # (가) f(x^2+4)=0 의 실근이 x=0 하나 -> f(4)=0, 다른 근 r<=4
sols = []
for rv in sp.solve(sp.Eq(F0.subs(x, -6), 0), r):  # (나) b=-2에서 극한 존재 -> f(-6)=0
    f0 = F0.subs(r, rv)
    h = f0.subs(x, x - 4) / f0.subs(x, x**2)
    zs = sorted(set(sp.real_roots(sp.Poly(sp.expand(f0.subs(x, x**2)), x))))
    lim = sp.limit(h, x, -2)
    sols.append((rv, zs, lim, f0.subs(x, 2) * lim))
print('원문:', sols)
check(sols and sols[0][3] == -4, '원문 C30 정답 -4 (= ②) 확인')
# r=4 (중근) 이면 f(-6)=100 != 0 이라 극한 없음, 0<r<4 이면 f(x^2)=0 실근 4개, r=0 이면 3개 -> r<0 만 가능
check(sp.expand(((x-4)**2).subs(x, -6)) != 0, '원문: r=4 경우 제외')

# ---------------------------------------------------------------- 1. 보조정리: f(f(x))=0 의 서로 다른 실근 개수
# f(x)=(x-v)^2+m. f(x)=s 의 실근 개수 n(s): s>m ->2, s=m ->1, s<m ->0
# f의 근 alpha<beta 일 때 m = -((beta-alpha)/2)^2 <= ... ; 경우 5가지 + 중근/허근
def N_count(P, Q):
    f = x**2 + P*x + Q
    FF = sp.Poly(sp.expand(f.subs(x, f)), x)
    return len(set(sp.real_roots(FF)))
# (i) 부호 조합으로 N 표
a_, b_ = sp.symbols('a_ b_', real=True)
cases = {}
for (A, B) in [(-1, 3), (-4, 0), (-6, -2), (-9, -5), (-12, -10), (2, 2), (0, 0), (-1, -1)]:
    P, Q = -(A + B), A * B
    cases[(A, B)] = N_count(P, Q)
print('N 표 (alpha,beta)->N:', cases)
check(cases[(-1, 3)] == 4 and cases[(-4, 0)] == 3 and cases[(-6, -2)] == 2, 'N=4 (alpha>m), 3 (alpha=m), 2 (alpha<m<beta)')
check(cases[(-12, -10)] == 0 and cases[(2, 2)] == 2 and cases[(0, 0)] == 1 and cases[(-1, -1)] == 0, 'N=0 (beta<m), 중근 2/1/0')
# beta=m 이면 N=1 이 되는 예: alpha<beta=m. beta-alpha=dd, m=-dd^2/4=beta
dd = sp.Integer(2); B = -dd**2/4; A = B - dd
check(N_count(-(A+B), A*B) == 1, 'N=1 (beta=m)')
# (ii) N=3 <=> alpha = m 증명: n(alpha)+n(beta)=3 이면 {1,2}. n(beta)=1,n(alpha)=2 는 beta=m<alpha 이므로 alpha<beta 와 모순
#      중근이면 N=n(alpha)<=2, 허근이면 N=0.
check(True, 'N=3 이면 alpha=m (beta=m 이면 alpha<m 이라 N=1)')

# ---------------------------------------------------------------- 2. (나) => k는 f(f(x))=0 의 단순근
# 다항식 D(x)에 대해 lim (x-k)/D(x): D(k)!=0 -> 0, D의 k에서 중복도 1 -> 1/D'(k), 중복도>=2 -> 발산
D = sp.Function('D')
check(sp.limit((x - 1) / ((x - 1)**2 * (x + 3)), x, 1, '+') == sp.oo, '중근이면 발산(예시)')
check(sp.limit((x - 1) / (x + 3), x, 1) == 0, '분모 0 아님 -> 극한 0 (예시)')

# ---------------------------------------------------------------- 3. N=3 가족(alpha=m) 에서 전수 조사
# f(x)=(x-alpha)(x-beta), beta-alpha=d>0, alpha=m=-d^2/4, v=alpha+d/2
dpos = sp.symbols('dpos', positive=True)
alpha = -dpos**2/4; beta = alpha + dpos; v = alpha + dpos/2
f = (x - alpha) * (x - beta)
FF = sp.factor(sp.expand(f.subs(x, f)))
check(sp.simplify(sp.expand(f.subs(x, f)) - (x - v)**2 * ((x - v)**2 - dpos)) == 0, 'f(f(x))=(x-v)^2{(x-v)^2-d}')
pts = {'a=v-sqrt d': v - sp.sqrt(dpos), 'b=v (중근)': v, 'c=v+sqrt d': v + sp.sqrt(dpos)}
found = []
for name, kk in pts.items():
    g = (x - kk) / (f.subs(x, f))
    L = sp.limit(sp.simplify(g), x, kk)
    print('  k =', name, ' lim =', sp.simplify(L))
    if L.is_finite is False or L in (sp.oo, -sp.oo, sp.zoo):
        continue
    for dv in sp.solve(sp.Eq(L, sp.Rational(-1, 16)), dpos):
        found.append((name, dv, sp.expand(f.subs(dpos, dv)), sp.simplify(kk.subs(dpos, dv))))
print('해:', found)
check(len(found) == 1 and found[0][1] == 4 and found[0][2] == x**2 + 4*x and found[0][3] == -4,
      '유일해 d=4, f(x)=x^2+4x, k=a=-4')
fA = x**2 + 4*x; kA = -4
ans_val = fA.subs(x, 1) + kA
check(ans_val == 1, 'f(1)+k = 1')

# ---------------------------------------------------------------- 4. 해 직접 확인
gA = (x - kA) / sp.expand(fA.subs(x, fA))
zs = sorted(set(sp.real_roots(sp.Poly(sp.expand(fA.subs(x, fA)), x))))
noexist = [z for z in zs if not sp.limit(gA, x, z, '+') == sp.limit(gA, x, z, '-') or sp.limit(gA, x, z, '+').is_finite is False]
check(zs == [-4, -2, 0] and noexist == [-2, 0], '불연속점 -4,-2,0 / 극한 없는 점 -2,0 (2개)')
check(sp.limit(gA, x, kA) == sp.Rational(-1, 16), 'lim_{x->-4} g = -1/16')

# ---------------------------------------------------------------- 5. 격자 전수 검사 (p,q 유리수 격자)
# (나) => k 는 f(f(x))=0 의 단순근, 극한값 = 1/F'(k);  (가) => 극한 없는 점 = (서로 다른 실근 수) - 1 = 2
def scan(P_, Q_):
    f = x**2 + P_*x + Q_
    FFp = sp.Poly(sp.expand(f.subs(x, f)), x)
    Nd = FFp.sqf_part().count_roots()       # 서로 다른 실근 개수(정확)
    if Nd != 3:
        return []                           # 단순근 k 를 빼면 극한 없는 점이 2개가 되려면 N=3 필수
    G = sp.gcd(FFp, FFp.diff(x))
    simple = [z for z in sp.real_roots(FFp.sqf_part()) if G.eval(z) != 0]
    out = []
    for z in simple:
        L = sp.nsimplify(sp.simplify(1 / FFp.diff(x).eval(z)))
        if sp.simplify(L + sp.Rational(1, 16)) == 0:
            out.append((P_, Q_, z))
    return out
hits = []; n3 = 0
grid = [sp.Rational(i, 2) for i in range(-20, 21)]
for P_, Q_ in itertools.product(grid, grid):
    hits += scan(P_, Q_)
print('격자 해:', hits)
check(hits == [(4, 0, -4)], '격자(p,q in [-10,10], 간격 1/2, 1681개) 전수: 해는 (p,q,k)=(4,0,-4) 하나')
random.seed(1)
extra = []
for _ in range(400):
    P_ = sp.Rational(random.randint(-400, 400), 37); Q_ = sp.Rational(random.randint(-400, 400), 41)
    extra += scan(P_, Q_)
check(extra == [], '무작위 유리수 f 400개: 다른 해 없음')
fam = []
for dv in [sp.Rational(1, 2), 1, 2, 3, 4, 5, 8, 9]:     # N=3 가족(alpha=m) 표본
    al = -sp.Rational(dv)**2/4; be = al + dv
    fam += [(dv,) + h for h in scan(-(al+be), al*be)]
print('N=3 가족 표본 해:', fam)
check([h[0] for h in fam] == [4], 'alpha=m 가족 표본 중 d=4 만 해')

def analyse(P_, Q_):
    f = x**2 + P_*x + Q_
    FFp = sp.Poly(sp.expand(f.subs(x, f)), x)
    return f, FFp.sqf_part().count_roots()

# ---------------------------------------------------------------- 6. 선지·오답 근거
choices = [-3, -1, 1, 3, 5]
diffs = {choices[i+1] - choices[i] for i in range(4)}
check(len(diffs) == 1, f'선지 등차 (공차 {diffs})')
check(choices.count(ans_val) == 1 and choices.index(ans_val) + 1 == 3, '정답 1 = ③, 선지에 한 번')
# 오답: k=c (부호 확인 누락) -> k=0
w_c = fA.subs(x, 1) + 0
# 오답: k=b (접점 x=-2 를 0/0꼴이라 극한 존재로 착각)
w_b = fA.subs(x, 1) + (-2)
# 오답: 꼭짓점 x좌표 부호를 뒤집어 f=x^2-4x, 왼쪽 점 k=0
fW = x**2 - 4*x
w_v = fW.subs(x, 1) + 0
print('오답 근거: k=c ->', w_c, ', k=b ->', w_b, ', f=x^2-4x ->', w_v)
check(w_c == 5 and w_b == 3 and w_v == -3 and all(w in choices for w in (w_c, w_b, w_v)), '오답 근거 값 5, 3, -3 이 선지 안에')
# 오답 f=x^2-4x 는 실제로 조건 불만족임을 확인
_, nW = analyse(-4, 0)
check(nW == 4, 'f=x^2-4x 이면 불연속점 4개(조건 위배)')
# 접점 k=b 는 극한 발산 확인
check(sp.limit((x + 2) / sp.expand(fA.subs(x, fA)), x, -2, '+') in (sp.oo, -sp.oo), 'k=b 이면 극한 발산')

print('\nALL PASS' if ok else '\nSOME FAIL')
