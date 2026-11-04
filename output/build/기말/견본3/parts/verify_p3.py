# -*- coding: utf-8 -*-
# p3.py (견본3 9–12번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(후보 전수) · 선지 등차·서로 다름 · 오답 값이 선지에 있음
import os
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, Poly, limit, sqrt, nroots
x, t, k, a, p, q, r = symbols('x t k a p q r', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 3, 10: 5, 11: 2, 12: 4}

def arith(no):
    v = [sp.nsimplify(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs=()):
    ch = [sp.nsimplify(c) for c in IT[no]['choices']]
    good = (IT[no]['ans'] == WANT[no] and sp.nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and all(sp.nsimplify(w) in ch and sp.nsimplify(w) != sp.nsimplify(val) for w in wrongs))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {list(wrongs)} {"OK" if good else "FAIL"}')
    assert good

def nreal(expr):
    """다항식의 서로 다른 실근 개수"""
    P = Poly(expand(expr), x)
    return len(set(sp.real_roots(P)))

# ===== 원문 풀이 =====
# M42: x^3-3x^2-9x+k=0 서로 다른 실근 2개인 k의 합 = 22 (④)
ks = [kv for kv in range(-60, 61) if nreal(x**3 - 3*x**2 - 9*x + kv) == 2]
assert ks == [-5, 27]
# 비정수 k에서는 2개가 될 수 없음(판별식 = 0 ⇔ k=-27 또는 5)
assert sorted(solve(sp.discriminant(x**3 - 3*x**2 - 9*x + k, x), k)) == [-5, 27]
assert sum(ks) == 22
# D58: f=x^3+px^2+qx, f(a)=1, f'(a)=3, 1-3a=4 → f(1)=-5 (⑤)
f = x**3 + p*x**2 + q*x
s = solve([f.subs(x, a) - 1, diff(f, x).subs(x, a) - 3, 1 - 3*a - 4], [a, p, q], dict=True)
assert len(s) == 1 and f.subs(s[0]).subs(x, 1) == -5
# I46: f=-k(x^2-4), ∫0^3|f|=23 → k=3, f(1)=9 (④)
K = symbols('K', positive=True)
fo = -K*(x**2 - 4)
I = integrate(fo, (x, 0, 2)) - integrate(fo, (x, 2, 3))
ko = solve(I - 23, K); assert ko == [3] and fo.subs(K, 3).subs(x, 1) == 9
# D41: f=x^2(px+q), 점 -2에서 기울기 1인 접선이 (2,f(2)) 지남 → f(4)=24 (④)
f = x**2*(p*x + q); L = diff(f, x).subs(x, -2)*(x + 2) + f.subs(x, -2)
s = solve([diff(f, x).subs(x, -2) - 1, (f - L).subs(x, 2)], [p, q], dict=True)
assert len(s) == 1 and f.subs(s[0]).subs(x, 4) == 24
print('원문 4개 정답 확인 OK')

# ===== 9번 =====
h = 2*x**3 - 3*x**2 - 12*x
crit = sorted(solve(diff(h, x), x)); assert crit == [-1, 2]
assert (h.subs(x, -1), h.subs(x, 2)) == (7, -20)
def cnt9(kv):
    # |h|=k ⇔ h=k 또는 h=-k (k>0), k=0이면 h=0
    if kv < 0: return 0
    if kv == 0: return nreal(h)
    rs = set(sp.real_roots(Poly(expand(h - kv), x))) | set(sp.real_roots(Poly(expand(h + kv), x)))
    return len(rs)
table = {kv: cnt9(kv) for kv in range(-3, 31)}
assert table[0] == 3 and table[7] == 5 and table[20] == 3 and table[21] == 2
assert all(table[kv] == 6 for kv in range(1, 7)) and all(table[kv] == 4 for kv in range(8, 20))
# k>20 이면 항상 2개 (|h|의 최댓값 없음, 극댓값 20 위) — 큰 k 표본
assert all(cnt9(kv) == 2 for kv in (25, 100, 1000))
good9 = [kv for kv, c in table.items() if c >= 5]
assert good9 == list(range(1, 8))
ans9 = len(good9)
w9a = len([kv for kv in good9 if kv != 7])          # k=7 제외
w9b = len(good9) + 1                                  # k=0 포함
chk(9, ans9, [w9a, w9b])

# ===== 10번 =====
f = x**3 + p*x**2 + q*x
assert f.subs(x, 0) == 0
eqs = [f.subs(x, a) - 8, diff(f, x).subs(x, a) - 4*a, (f.subs(x, a) - a*diff(f, x).subs(x, a)) - (-8)]
cands = solve(eqs, [a, p, q], dict=True)
cands = sorted(cands, key=lambda d: d[a])
assert [c[a] for c in cands] == [-2, 2]
info = []
for c in cands:
    fc = f.subs(c)
    # 극한값 실제로 2인지
    assert limit((fc - 8)/(x**2 - c[a]**2), x, c[a]) == 2
    # 접선 y절편
    tan = diff(fc, x).subs(x, c[a])*(x - c[a]) + fc.subs(x, c[a]); assert tan.subs(x, 0) == -8
    D = sp.discriminant(diff(fc, x), x)
    info.append((c[a], expand(fc), D, fc.subs(x, 1)))
# a=0 불가: f(0)=8 필요 → 모순
assert f.subs(x, 0) != 8
noext = [i for i in info if i[2] <= 0]      # 극값 없음 ⇔ f'의 판별식 ≤ 0
assert len(noext) == 1 and noext[0][0] == 2 and noext[0][1] == x**3 - 2*x**2 + 4*x
ans10 = noext[0][3]
w10 = [i[3] for i in info if i[2] > 0][0]   # a=-2 후보
assert w10 == 11
chk(10, ans10, [w10])

# ===== 11번 =====
Kp = symbols('Kp', real=True)
fi = Kp*(x + 1)*(x - 3)
g = integrate(fi.subs(x, t), (t, 0, x))
# (가): x=-1 극대, x=3 극소 → g'' (-1)<0, g''(3)>0 ⇔ Kp>0 (Kp<0이면 반대, Kp=0 불가)
gpp = diff(g, x, 2)
assert sp.simplify(gpp.subs(x, -1)) == -4*Kp and sp.simplify(gpp.subs(x, 3)) == 4*Kp
# 이차함수 f의 근이 정확히 -1, 3 이어야 g'=f의 부호 변화가 그 두 곳 → f=Kp(x+1)(x-3) 꼴이 유일
diffv = sp.simplify(g.subs(x, -1) - g.subs(x, 3))
ksol = [kv for kv in solve(diffv - 32, Kp) if kv > 0]
assert ksol == [3]
G = expand(g.subs(Kp, 3)); assert G == x**3 - 3*x**2 - 9*x
ans11 = G.subs(x, 3)
w11a = integrate(fi.subs(Kp, 3), (x, -1, 3))            # 차를 극솟값으로: -32
w11b = -G.subs(x, -1) - 32                              # g(-1) 부호 실수: -5-32 = -37
assert (G.subs(x, -1), w11a, w11b) == (5, -32, -37)
chk(11, ans11, [w11a, w11b])

# ===== 12번 =====
# (가) 판정: 삼차 f의 실근 구조 전수 — 실근마다 f'=0 이어야 |f| 미분가능
#   (i) 서로 다른 세 실근 / (ii) 단근+두 허근: 단근에서 f'≠0 → 불가
#   (iii) 중근 α + 단근 β: β에서 f'≠0 → 불가 / (iv) 삼중근: 가능
al, be = symbols('al be', real=True)
assert sp.simplify(diff(p*(x - al)**2*(x - be), x).subs(x, be) - p*(be - al)**2) == 0   # ≠0 (p≠0, α≠β)
# 표본으로 |f| 미분가능성 수치 확인: 좌우 미분계수
def lr(fe, x0):
    return (limit((sp.Abs(fe) - sp.Abs(fe.subs(x, x0)))/(x - x0), x, x0, '-'),
            limit((sp.Abs(fe) - sp.Abs(fe.subs(x, x0)))/(x - x0), x, x0, '+'))
L1, R1 = lr((x - 1)**2*(x + 2), -2); assert L1 != R1
L2, R2 = lr((x - 1)**3, 1); assert L2 == R2 == 0
# 일반 삼차 f = p(x-r)^3 + c1(x-r) + c0 꼴 대신, 계수 비교로 (나) 풀기
f = p*(x - r)**3
tan = diff(f, x).subs(x, -1)*(x + 1) + f.subs(x, -1)
sol12 = solve([diff(f, x).subs(x, -1) - 4, (f - tan).subs(x, 5)], [p, r], dict=True)
sol12 = [s_ for s_ in sol12 if s_[p] != 0]
assert len(sol12) == 1 and sol12[0] == {p: Rational(1, 3), r: 1}
F12 = f.subs(sol12[0])
assert sp.factor(expand(F12 - tan.subs(sol12[0]))) == sp.factor(Rational(1, 3)*(x + 1)**2*(x - 5))
ans12 = F12.subs(x, 4)
w12 = (x - 1)**3                                     # 최고차항 계수 1로 착각
chk(12, ans12, [w12.subs(x, 4)])

# 배점대 단원·출처
assert [IT[n]['key'] for n in (9, 10, 11, 12)] == ['M42', 'D58', 'I46', 'D41']
print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
