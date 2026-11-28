# 검증: 18번 (C30 구조 변경) — g(x)=x/f(x^2+4), h(x)=f(x-4)/f(x^2), 합성 g(h(x))의 불연속점 개수
# 불연속점은 '정의되지 않는 점'까지 포함(원본과 같은 관례). 약분하지 않고 정의역을 그대로 따진다.
import sympy as sp
from fractions import Fraction as Fr
x, t, p, q, k = sp.symbols('x t p q k', real=True)

def real_roots(poly_expr, var=x):
    P = sp.Poly(sp.expand(poly_expr), var)
    if P.degree() <= 0:
        return set()
    return set(sp.real_roots(P))  # 정확한 실근(중복 제거는 set)

def disc_g(f):
    """g(x)=x/f(x^2+4)의 불연속점 = f(x^2+4)=0의 실근"""
    return real_roots(f.subs(x, x**2 + 4))

def disc_gh(f):
    """g(h(x))의 불연속점 = h가 정의되지 않는 점 ∪ (h는 정의되나 f(h^2+4)=0인 점)"""
    den = sp.expand(f.subs(x, x**2))       # h의 분모
    num = sp.expand(f.subs(x, x - 4))      # h의 분자
    P = real_roots(den)
    # f(h^2+4)=0  ⇔  f((num^2+4 den^2)/den^2)=0, 분모 den^4를 곱한 다항식의 실근 중 den≠0인 것
    ft = sp.Poly(f, x)
    a2, a1, a0 = [ft.coeff_monomial(x**i) for i in (2, 1, 0)]
    U = num**2 + 4*den**2                  # (h^2+4) = U/den^2
    G = sp.expand(a2*U**2 + a1*U*den**2 + a0*den**4)
    Z = {r for r in real_roots(G) if sp.simplify(den.subs(x, r)) != 0}
    return P | Z

# ---------- 1) 격자 전수: f(x)=x^2+px+q, p,q 정수 -30..30 (실근 없는 경우 포함) ----------
sols = []
for P_ in range(-30, 31):
    for Q_ in range(-30, 31):
        f = x**2 + P_*x + Q_
        Dg = disc_g(f)
        if len(Dg) != 1:
            continue
        if len(disc_gh(f)) == 3:
            sols.append((P_, Q_, sorted(Dg), sorted(disc_gh(f))))
print('격자 전수 (가)(나) 만족:', [(s[0], s[1], sp.factor(x**2 + s[0]*x + s[1]), s[2], s[3]) for s in sols])

# ---------- 2) (가)의 완전 판정 ----------
# f(x^2+4)=0 의 실근: f의 실근 r 에 대하여 x^2=r-4. r>4 → 2개, r=4 → 1개(x=0), r<4 → 0개.
# 개수 1 ⇔ f(4)=0 이고 다른 근 k ≤ 4  (a=0).  임의 유리 (r1,r2) 표본으로 재확인
import itertools, random
random.seed(1)
cand = [Fr(n, d) for n in range(-40, 41) for d in (1, 2, 3)]
bad = 0
for _ in range(3000):
    r1, r2 = random.choice(cand), random.choice(cand)
    f = sp.expand((x - sp.Rational(r1.numerator, r1.denominator))*(x - sp.Rational(r2.numerator, r2.denominator)))
    one = len(disc_g(f)) == 1
    pred = (max(r1, r2) == 4)
    bad += (one != pred)
print('(가) 판정 불일치 수 (실근 있는 f 표본 3000개):', bad)
# 실근 없는 f: f(x^2+4) 실근 없음 → 연속 → (가) 위반 (격자 전수에서 확인됨)

# ---------- 3) f=(x-4)(x-k), k ≤ 4 에서 g(h(x)) 불연속점 개수 N(k) ----------
# 일치가 일어날 수 있는 k: k+4 ∈ {±2, ±√k, 0}, 그리고 경계 k=0, 4  → 임계값과 그 사이 표본 모두 검사
crit = set([sp.Integer(-6), sp.Integer(-2), sp.Integer(-4), sp.Integer(0), sp.Integer(4)])
for eq in [k + 4 - sp.sqrt(k), k + 4 + sp.sqrt(k)]:
    crit |= {s for s in sp.solve(eq, k) if s.is_real}
crit = sorted(crit)
print('임계 k:', crit)
samples = set(crit)
grid = [sp.Rational(n, 4) for n in range(-60, 17)]       # -15 .. 4, 간격 1/4
samples |= set(grid)
samples |= {sp.Rational(random.randint(-4000, 1600), 400) for _ in range(300)}
samples |= {(crit[i] + crit[i+1]) / 2 for i in range(len(crit) - 1)}
samples |= {crit[0] - 1, crit[0] - 10}
res = {}
for kk in sorted(samples):
    if kk > 4: continue
    f = sp.expand((x - 4)*(x - kk))
    assert len(disc_g(f)) == 1 and disc_g(f) == {0}
    res[kk] = len(disc_gh(f))
three = sorted(kk for kk, n in res.items() if n == 3)
print('N(k)=3 인 표본 k:', three)
from collections import Counter
def region(kk):
    if kk < 0: return 'k<0' if kk not in (-6, -2) else f'k={kk}'
    if kk == 0: return 'k=0'
    if kk < 4: return '0<k<4'
    return 'k=4'
print('구간별 N(k) 값:', {r: sorted(set(n for kk, n in res.items() if region(kk) == r)) for r in ['k<0', 'k=-6', 'k=-2', 'k=0', '0<k<4', 'k=4']})

# 기호 검사: k<0 이면 불연속점 {±2, 8, k+4}, 0<k<4 이면 {±2, ±√k, 8, k+4} (모두 서로 다름)
print("k+4가 2, -2, 8과 겹치는 k (8은 k=4 이중근):", sp.solve(k + 4 - 2, k), sp.solve(k + 4 + 2, k), sp.solve(k + 4 - 8, k))
print('0<k<4에서 k+4=±√k 실근:', [s for s in sp.solve(k + 4 - sp.sqrt(k), k) if s.is_real], ' (k+4>4>√k 이므로 없음)')

# ---------- 4) 정답 ----------
vals = {}
for kk in three:
    f = (x - 4)*(x - kk)
    vals[kk] = f.subs(x, 1)
    print(f'k={kk}: f(x)={sp.factor(f)}, 불연속점 {sorted(disc_gh(sp.expand(f)))}, f(1)={vals[kk]}')
ans = sum(vals.values())
print('정답 f(1)의 합 =', ans)
assert set(three) == {-6, -2, 4} and ans == -21

# ---------- 5) 오답 선지 근거 ----------
print('k=4(이중근) 누락:', vals[-6] + vals[-2])
print('k=-2 누락(원본 쪽 상쇄만):', vals[-6] + vals[4])
print('k=-6 누락:', vals[-2] + vals[4])
print('겹침(상쇄) 둘 다 누락, k=4만:', vals[4])
choices = [-30, -21, -12, 0, 9]
assert choices == sorted(choices) and choices.index(ans) == 1
print('선지', choices, '정답 위치', choices.index(ans) + 1)

# ---------- 6) 수치 확인: 불연속점 근처 g(h(x)) 거동 (원리 설명용) ----------
for kk in three:
    f = lambda u, kk=float(kk): (u - 4)*(u - kk)
    g = lambda u, kk=float(kk): 1/(u*(u*u + (4 - kk)))   # f(u^2+4)=u^2(u^2+4-k), u≠0
    h = lambda u, f=f: f(u - 4)/f(u*u)
    for x0 in (-2, 2, 8):
        l, r = g(h(x0 - 1e-3)), g(h(x0 + 1e-3))
        print(f'  k={kk}, x->{x0}: 좌 {l:.6g}, 우 {r:.6g}')
