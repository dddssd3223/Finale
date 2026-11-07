# verify_17.py : 17번 원문(L42)과 시험 문항의 정답·중간값 검증
import sympy as sp

x, p, q, b, c, d = sp.symbols('x p q b c d', real=True)

# ---------- 공통 f (그림에서 복원: 가운데 삼차식 = (x+1/2)(x-1)(x-2)) ----------
f_L = (x + 3) * (x - 3) / 9          # x<0
f_M = (x + sp.Rational(1, 2)) * (x - 1) * (x - 2)   # 0<=x<1
f_R = -x + 3                          # x>=1

# 그림 정보 확인: f(0)=1, f(0-)=-1, f(1-)=0, f(1)=2, 가운데 극대 x~0.107
assert f_M.subs(x, 0) == 1
assert sp.limit(f_L, x, 0, '-') == -1
assert f_M.subs(x, 1) == 0
assert f_R.subs(x, 1) == 2
xm = min(sp.solve(sp.diff(f_M, x), x), key=lambda r: abs(float(r)))
assert 0.09 < float(xm) < 0.12, xm
# (alpha beta gamma 의 곱 조건) f(0) = -alpha*beta*gamma = 1, gamma=1 -> alpha*beta=-1
al, be = sp.Rational(-1, 2), 2
assert -al * be * 1 == 1
# (-3,3)에서 f의 근이 없음: x<0 근 -3(구간 밖), [0,1) 근 없음, x>=1 근 3(구간 밖)
assert [r for r in sp.solve(f_M, x) if 0 <= r < 1] == []

# ---------- 원문: g = x^3+bx^2+cx+d, -3<a<3 모든 a에서 lim g/f 존재 ----------
g = x**3 + b * x**2 + c * x + d
# S2: a=0 좌극한 g(0)/(-1) = 우극한 g(0)/1 -> g(0)=0
eq1 = sp.Eq(g.subs(x, 0) / (-1), g.subs(x, 0) / 1)
# S3: a=1 좌극한 분모->0 이므로 g(1)=0
eq2 = sp.Eq(g.subs(x, 1), 0)
sol = sp.solve([eq1, eq2], [d, c], dict=True)[0]
g1 = sp.expand(g.subs(sol))                      # x^3+bx^2-(1+b)x
# S4: 좌극한 = 우극한(g(1)/2 = 0)
left = sp.limit(g1 / f_M, x, 1, '-')
right = sp.limit(g1 / f_R, x, 1, '+')
bsol = sp.solve(sp.Eq(left, right), b)
assert bsol == [-2], bsol
g_orig = sp.factor(g1.subs(b, -2))
assert sp.expand(g_orig - x * (x - 1)**2) == 0
ans_orig = g_orig.subs(x, 3)
assert ans_orig == 12
# 모든 a in (-3,3) 에서 극한 존재 확인 (0,1에서 좌우 비교; 나머지는 f(a)!=0 연속)
assert sp.limit(g_orig / f_L, x, 0, '-') == sp.limit(g_orig / f_M, x, 0, '+') == 0
assert sp.limit(g_orig / f_M, x, 1, '-') == sp.limit(g_orig / f_R, x, 1, '+') == 0
print('원문: g(x) =', g_orig, ', g(3) =', ans_orig)

# ---------- 시험: g = (x-p)^2+q, lim_{x->t} f(g(x)) 비존재 t 가 정확히 alpha, beta ----------
def F(y):
    y = float(y)
    if y < 0:
        return (y + 3) * (y - 3) / 9
    if y < 1:
        return (y + 0.5) * (y - 1) * (y - 2)
    return -y + 3

def bad_points(pp, qq, h=1e-7):
    """lim_{x->t} f(g(x)) 가 존재하지 않는 t (후보: g(t)=0 또는 1)"""
    gg = lambda t: (t - pp)**2 + qq
    cand = set()
    for cval in (0, 1):
        disc = cval - qq
        if disc >= 0:
            r = disc**0.5
            cand |= {round(pp - r, 9), round(pp + r, 9)}
    out = []
    for t in sorted(cand):
        L, R = F(gg(t - h)), F(gg(t + h))
        if abs(L - R) > 1e-3:
            out.append(t)
    return out

# E2~E4: q 구간별 비존재 점 개수
assert len(bad_points(0.3, -0.5)) == 4      # q<0
assert len(bad_points(1.0, 0.0)) == 2       # q=0 (꼭짓점이 0에 접함 -> 그 점은 존재)
assert len(bad_points(0.5, 0.75)) == 2      # 0<q<1
assert len(bad_points(0.5, 1.0)) == 0       # q=1
assert len(bad_points(0.5, 2.0)) == 0       # q>1
# q=0 꼭짓점 t=p: g->0+ 양쪽 -> f->1 (존재)
assert abs(F((1 + 1e-7 - 1)**2) - 1) < 1e-6 and abs(F((1 - 1e-7 - 1)**2) - 1) < 1e-6

# E5: alpha, beta = g(x)=1 의 두 근, alpha*beta = p^2-(1-q) = 0 -> q = 1-p^2, 0<=q<1 -> 0<p^2<=1
r1, r2 = sp.solve(sp.Eq((x - p)**2 + q, 1), x)
assert sp.simplify(r1 * r2 - (p**2 + q - 1)) == 0
g3 = sp.expand(((3 - p)**2 + q).subs(q, 1 - p**2))
assert g3 == 10 - 6 * p
# E6: p in [-1,0) U (0,1] 에서 최소 -> p=1, g=(x-1)^2
assert g3.subs(p, 1) == 4
# 수치 전수 탐색: 조건 만족 (p,q) 중 g(3) 최소
best = None
import itertools
N = 400
for i in range(-N, N + 1):
    pp = 2 * i / N
    for qq in [1 - pp**2]:                      # alpha*beta=0 필요조건으로 생성 후 조건 직접 검사
        bp = bad_points(pp, qq)
        if len(bp) == 2 and abs(bp[0] * bp[1]) < 1e-6:
            v = (3 - pp)**2 + qq
            if best is None or v < best[0]:
                best = (v, pp, qq, bp)
# 일반 탐색(αβ=0 가정 없이): 격자 (p,q)
for i in range(-40, 41):
    for j in range(-40, 41):
        pp, qq = i / 20, j / 20
        bp = bad_points(pp, qq)
        if len(bp) == 2 and abs(bp[0] * bp[1]) < 1e-6:
            v = (3 - pp)**2 + qq
            assert v >= 4 - 1e-9
assert abs(best[0] - 4) < 1e-9 and abs(best[1] - 1) < 1e-9, best
print('시험: g(x) = (x-1)^2, 비존재 t =', best[3], ', g(3) 최솟값 =', best[0])

# ---------- 선지 분석 ----------
# g(3) = 10-6p (= 10+3b, b=-2p), 허용 p in [-1,0)U(0,1] -> g(3) in [4,10)U(10,16]
# 함정A: q=0(접하는 경우) 를 비존재로 오인하여 배제 -> 0<p^2<1, g(3) in (4,10)U(10,16): 최솟값 없음
#        -> 선지 중 '4 초과 최소' 5를 고르거나, b 정수로 가정하면 b=-1 -> 7
assert (10 - 6 * p).subs(p, sp.Rational(1, 2)) == 7
# 함정B: p=-1 (q=0, g=(x+1)^2) 를 택하면 16 (선지 밖)
assert (10 - 6 * p).subs(p, -1) == 16
# 선지 5,6,7,8 은 p=5/6,2/3,1/2,1/3 에 해당 (모두 조건 만족하는 값이지만 최솟값 아님)
for v, pv in [(5, sp.Rational(5, 6)), (6, sp.Rational(2, 3)), (7, sp.Rational(1, 2)), (8, sp.Rational(1, 3))]:
    assert (10 - 6 * p).subs(p, pv) == v
    assert len(bad_points(float(pv), float(1 - pv**2))) == 2
print('ALL PASS')
