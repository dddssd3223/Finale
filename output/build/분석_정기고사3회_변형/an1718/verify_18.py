# verify_18.py : 18번 (원문 C30 / 시험 18번) 정답·중간값 검증
import itertools
from sympy import symbols, Poly, roots, Rational, limit, cancel, together, oo, S, sqrt, expand, factor

x = symbols('x')

def real_zero_set(expr):
    """expr(x) 다항식의 서로 다른 실근 집합"""
    rs = roots(Poly(expand(expr), x))
    return sorted({r for r in rs if r.is_real}, key=lambda v: float(v))

def mult(expr, r):
    rs = roots(Poly(expand(expr), x))
    return rs.get(r, 0) if r in rs else next((m for k, m in rs.items() if (k - r).equals(0)), 0)

def lim_exists(num, den, p):
    """p 에서 num/den 의 극한(유한값) 존재 여부 = num 의 근 차수 >= den 의 근 차수"""
    return mult(num, p) >= mult(den, p)

# ---------------- 원문 C30 ----------------
print("== 원문 C30 ==")
sols = []
cands = []
for r1, r2 in itertools.combinations_with_replacement(range(-12, 13), 2):
    cands.append((x - r1) * (x - r2))
cands += [x**2 + 1, x**2 + 2*x + 5, x**2 - 8*x + 20]   # 실근 없는 경우
for f in cands:
    F = lambda t: f.subs(x, t)
    gD = real_zero_set(F(x**2 + 4))               # g=x/f(x^2+4) 불연속점
    if len(gD) != 1:
        continue
    hD = real_zero_set(F(x**2))                    # h=f(x-4)/f(x^2) 불연속점
    if len(hD) != 2:
        continue
    b, c = hD
    if not lim_exists(F(x - 4), F(x**2), b):
        continue
    L = limit(F(x - 4) / F(x**2), x, b)
    sols.append((factor(f), gD, b, c, F(c), L, F(c) * L))
for s in sols:
    print("f =", s[0], "| a =", s[1], "| b,c =", s[2], s[3], "| f(c) =", s[4], "| lim_b h =", s[5], "| 답 =", s[6])
assert len(sols) == 1 and sols[0][6] == -4
assert sols[0][5] == Rational(1, 4) and sols[0][4] == -16 and sols[0][1] == [0]
# (가)만 만족하는 f 의 꼴: (x-4)(x-s), s<=4  (참고: s=4, s<0 이면 (나) 불연속점 2개)
ga = []
for f in cands:
    if len(real_zero_set(f.subs(x, x**2 + 4))) == 1:
        ga.append(factor(f))
assert all(f.subs(x, 4) == 0 for f in ga)
print("(가)만 만족: 모두 f(4)=0, 개수", len(ga))
# s=4 인 경우 (나)의 불연속점은 ±2 둘이지만 lim_{x->-2} 가 존재하지 않음
f4 = (x - 4)**2
assert real_zero_set(f4.subs(x, x**2)) == [-2, 2] and not lim_exists(f4.subs(x, x - 4), f4.subs(x, x**2), -2)
print("원문 정답 -4 (②) 확인")

# ---------------- 시험 18번 ----------------
print("== 시험 18번 ==")
R = list(range(-6, 7)) + [9]
quarts = [ (x-a)*(x-b)*(x-c)*(x-d) for a, b, c, d in itertools.combinations_with_replacement(R, 4)]
irr = [x**2 + 1, x**2 + 2*x + 5]
quarts += [(x-a)*(x-b)*q for a, b in itertools.combinations_with_replacement(R, 2) for q in irr]
quarts += [irr[0]*irr[1], irr[0]**2]

def check(f, use_da=True):
    F = lambda t: f.subs(x, t)
    D = real_zero_set(F(x**2))
    if len(D) != 3:                        # (가)
        return None
    bad = [p for p in D if not lim_exists(F(x), F(x**2), p)]
    if len(bad) != 1:                      # (나)  (연속점에서는 극한 존재)
        return None
    if use_da:
        if limit(cancel(F(x) / F(x**2)), x, -3) != 0:   # (다)
            return None
    return D, bad

ga_na = []
sols = []
for f in quarts:
    r = check(f, use_da=False)
    if r is None:
        continue
    ga_na.append((factor(f), r))
    if limit(cancel(f / f.subs(x, x**2)), x, -3) == 0:
        sols.append((factor(f), r, f.subs(x, 2)))
print("(가)(나) 만족 f:")
for f, r in ga_na:
    print("  ", f, "| 불연속점", r[0], "| 극한X", r[1], "| f(2) =", expand(f).subs(x, 2))
# (가)(나) 만족 f 는 모두 x(x-1)(x+1)(x-t), t<=0 꼴
for f, r in ga_na:
    e = expand(f)
    assert e.subs(x, 0) == 0 and e.subs(x, 1) == 0 and e.subs(x, -1) == 0
    assert r[0] == [-1, 0, 1] and r[1] == [0]
print("(가)(나)+(다) 만족:", sols)
assert len(sols) == 1 and sols[0][2] == 30
assert expand(sols[0][0] - x*(x-1)*(x+1)*(x+3)) == 0
f = x*(x-1)*(x+1)*(x+3)
g = cancel(f / f.subs(x, x**2))
print("약분된 g =", g)
assert limit(g, x, 0, '+') == oo and limit(g, x, 0, '-') == -oo
print("lim_{x->1} g =", limit(g, x, 1), ", lim_{x->-1} g =", limit(g, x, -1), ", g(-3) =", g.subs(x, -3))
assert limit(g, x, -3) == 0
# 선지 대응: f(2) = 6(2-t)
t = symbols('t')
for v in [24, 26, 28, 30, 32]:
    from sympy import solve
    print("f(2) =", v, "<- t =", solve(6*(2 - t) - v, t))
# 오답 후보 계산
print("t=-2 (다를 x->-2로 착각):", expand(x*(x-1)*(x+1)*(x+2)).subs(x, 2))
print("t=0  (x^2(x^2-1)):", expand(x**2*(x**2-1)).subs(x, 2), " t=-1 (x(x-1)(x+1)^2):", expand(x*(x-1)*(x+1)**2).subs(x, 2))
print("(-1 조건 누락) x(x-1)(x+3)(x-u): f(2)=10(2-u), (나)에서 u=-1 강제 → 30")
print("시험 정답 30 (④) 확인")
