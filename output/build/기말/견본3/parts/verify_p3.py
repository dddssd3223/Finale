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
# ===== 조건 제거 검사(ABLATION) =====
import itertools
# 조건을 하나씩 지우고, 남은 조건을 만족시키는 경우를 다시 구해 답이 그대로인지 / 바뀌는지 / 정해지지 않는지 본다.
# 군더더기는 FAIL로 처리하지 않고 보고만 한다(아래 검사는 assert를 걸지 않는다).
def ablation(no, cname, vals, ans, why='', est=False, undef=None):
    """vals: 조건을 지웠을 때 가능한 답(표본 포함) 목록, undef: 답이 없거나 정해지지 않는 이유(문자열)"""
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(sp.nsimplify(v) for v in vals), key=lambda v: float(v))
        if sv == [sp.nsimplify(ans)]:
            msg = f'성립 조건(답 그대로 {ans}; {why})' if est else f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')

print('--- 조건 제거 검사 ---')
# ----- 9번: 조건 = [정수 k], [서로 다른 실근], [5 이상] -----
h9 = 2*x**3 - 3*x**2 - 12*x
# '정수' 제거: 0<k≤7 인 실수 k가 모두 해당 → 개수가 유한하지 않음
fr = [Rational(1, 2), Rational(13, 2), Rational(7, 3)]
assert all(cnt9(kv) >= 5 for kv in fr)
ablation(9, "'정수'", [], ans9, undef=f'0<k≤7인 모든 실수 k가 해당(예: k={fr}) → 개수가 유한하지 않음')
# '서로 다른' 제거: 중근을 겹쳐 센다
def cnt9_mult(kv):
    if kv < 0: return 0
    if kv == 0: return sum(m for r_, m in sp.roots(Poly(h9, x)).items() if r_.is_real)
    tot = 0
    for e_ in (h9 - kv, h9 + kv):
        P_ = Poly(expand(e_), x)
        tot += len(sp.real_roots(P_))          # real_roots 는 중복도만큼 나열
    return tot
g9m = [kv for kv in range(-3, 31) if cnt9_mult(kv) >= 5]
ablation(9, "'서로 다른'", [len(g9m)], ans9, est=True,
         why=f'중근을 겹쳐 세도 k={g9m[0]}~{g9m[-1]}; 실근 개수를 세는 기준을 정하는 관용 표현')

# ----- 10번: 조건 = [최고차항 계수 1], [f(0)=0], [극값 없음], [극한 = 2], [접선 y절편 -8] -----
c3, rr = symbols('c3 rr', real=True)
F10 = c3*x**3 + p*x**2 + q*x + rr
V10 = [c3, p, q, rr, a]
C10 = {
    '최고차항의 계수 1': ([c3 - 1], lambda d: d[c3] == 1),
    'f(0)=0': ([rr], lambda d: d[rr] == 0),
    '극값을 갖지 않는다': ([], lambda d: 4*d[p]**2 - 12*d[c3]*d[q] <= 0),
    '극한값 2': ([F10.subs(x, a) - 8, diff(F10, x).subs(x, a) - 4*a],
                lambda d: d[a] != 0 and F10.subs(d).subs(x, d[a]) == 8 and diff(F10.subs(d), x).subs(x, d[a]) == 4*d[a]),
    '접선의 y절편 -8': ([(F10 - x*diff(F10, x)).subs(x, a) + 8],
                     lambda d: (F10 - x*diff(F10, x)).subs(d).subs(x, d[a]) == -8),
}
def solve10(drop):
    keep = [k_ for k_ in C10 if k_ != drop]
    eqs = sum((C10[k_][0] for k_ in keep), [])
    out = set()
    grid = [Rational(n, 2) for n in range(-12, 13)]
    sols = []
    for vs_ in itertools.combinations([c3, rr, q, p, a], len(eqs)):   # 앞쪽 미지수부터 풀어 나머지를 자유 변수로
        sols = solve(eqs, list(vs_), dict=True)
        if sols and all(len(s_) == len(eqs) for s_ in sols): break
    for s_ in sols:
        free = [v for v in V10 if v not in s_]
        for vals in itertools.product(grid, repeat=len(free)):
            d = dict(zip(free, vals))
            try:
                d.update({k_: sp.sympify(e).subs(d) for k_, e in s_.items()})
            except Exception:
                continue
            if any(not d[v].is_finite for v in V10) or d[c3] == 0:
                continue
            if all(C10[k_][1](d) for k_ in keep):
                out.add(F10.subs(d).subs(x, 1))
                if len(out) > 6: return out
    return out
for drop in C10:
    v10 = solve10(drop)
    ablation(10, f"'{drop}'", v10, ans10)
# 극한값을 실제 limit 로 한 번 더 확인(극한값 조건을 남긴 경우의 대표 해)
assert limit((x**3 - 2*x**2 + 4*x - 8)/(x**2 - 4), x, 2) == 2

# ----- 11번: 조건 = [이차함수], (가) 극대 x=-1, (가) 극소 x=3, (가) 극대/극소 구분, (나) 차 32 -----
def gfun(fe):
    return integrate(fe.subs(x, t), (t, 0, x))
def ext11(fe):
    """g'=f 의 부호 변화로 극대점·극소점과 값"""
    rs = sorted(set(r_ for r_ in sp.real_roots(Poly(expand(fe), x))), key=float)
    G_ = gfun(fe); mx, mn = [], []
    for r_ in rs:
        L_, R_ = fe.subs(x, r_ - Rational(1, 10**6)), fe.subs(x, r_ + Rational(1, 10**6))
        if L_ > 0 > R_: mx.append((r_, G_.subs(x, r_)))
        if L_ < 0 < R_: mn.append((r_, G_.subs(x, r_)))
    return mx, mn
def ok11(fe, need_max=True, need_min=True, need_order=True, need_diff=True):
    mx, mn = ext11(fe)
    pts = [r_ for r_, _ in mx + mn]
    if need_order:
        if need_max and [r_ for r_, _ in mx] != [-1]: return None
        if need_min and [r_ for r_, _ in mn] != [3]: return None
    else:
        if sorted(pts) != [-1, 3]: return None
    if len(mx) != 1 or len(mn) != 1: return None
    if need_diff and mx[0][1] - mn[0][1] != 32: return None
    return mn[0][1]
# 극대/극소 구분 제거: 'x=-1, x=3에서 극값' → K=±3
v = [ok11(Kv*(x + 1)*(x - 3), need_order=False) for Kv in (3, -3)]
ablation(11, "(가)의 '극대·극소 구분'", [w for w in v if w is not None], ans11)
# 'x=-1에서 극대' 제거: f=K(x-s)(x-3), s<3, K>0 를 (나)로 맞춤
vs = []
for sv in (-1, 0, 1, -3):
    Kv = solve(K*(3 - sv)**3/6 - 32, K)[0]
    w = ok11(Kv*(x - sv)*(x - 3), need_max=False)
    if w is not None: vs.append(w)
ablation(11, "(가)의 'x=-1에서 극대'", vs, ans11)
vs = []
for sv in (3, 2, 1, 5):
    Kv = solve(K*(sv + 1)**3/6 - 32, K)[0]
    w = ok11(Kv*(x + 1)*(x - sv), need_min=False)
    if w is not None: vs.append(w)
ablation(11, "(가)의 'x=3에서 극소'", vs, ans11)
vs = [ok11(Kv*(x + 1)*(x - 3), need_diff=False) for Kv in (1, 2, 3)]
ablation(11, "(나) '극댓값과 극솟값의 차 32'", vs, ans11)
# '이차함수' 제거(다항함수): f=K(x+1)(x-3)(x^2+1) 도 (가)(나)를 만족
m4 = (x + 1)*(x - 3)*(x**2 + 1)
Kv = solve(K*(-integrate(m4, (x, -1, 3))) - 32, K)[0]
vs = [ok11(3*(x + 1)*(x - 3)), ok11(Kv*m4)]
ablation(11, "'이차함수'", vs, ans11, why=f'예: f={Kv}(x+1)(x-3)(x^2+1)')

# ----- 12번: 조건 = [삼차함수], (가) |f| 미분가능, (나) 접점 -1·기울기 4, (나) 통과점 (5,f(5)) -----
def ok12(fe, need_a=True, need_slope=True, need_pass=True, deg=3):
    P_ = Poly(expand(fe), x)
    if deg is not None and P_.degree() != deg: return None
    if need_a:   # |f| 미분가능 ⇔ 모든 실근에서 f'=0 ⇔ 중복도 1인 실근이 없음
        from collections import Counter
        if any(m == 1 for m in Counter(sp.real_roots(P_)).values()): return None
    sl = diff(fe, x).subs(x, -1)
    if need_slope and sl != 4: return None
    L_ = sl*(x + 1) + fe.subs(x, -1)
    if need_pass and (fe - L_).subs(x, 5) != 0: return None
    return fe.subs(x, 4)
# (가) 제거: f = 4(x+1)+m + P(x+1)^2(x-5)
vs = [ok12(4*(x + 1) + mv + pv*(x + 1)**2*(x - 5), need_a=False)
      for mv, pv in ((Rational(-8, 3), Rational(1, 3)), (0, 1), (1, -2))]
ablation(12, "(가) '|f(x)|가 실수 전체에서 미분가능'", [w for w in vs if w is not None], ans12)
# 기울기 4 제거: f=p(x-r)^3 이 통과 조건을 만족 ⇔ r=1, p 자유
rsol = solve(expand(((x - r)**3 - (3*(-1 - r)**2*(x + 1) + (-1 - r)**3)).subs(x, 5)), r)
assert rsol == [1]
vs = [ok12(pv*(x - 1)**3, need_slope=False) for pv in (Rational(1, 3), 1, -2)]
ablation(12, "(나)의 '기울기가 4'", [w for w in vs if w is not None], ans12)
# 통과점 제거: f=p(x-r)^3, 3p(1+r)^2=4, r 자유
vs = []
for rv in (1, 0, 2):
    pv = Rational(4, 3)/(1 + rv)**2
    w = ok12(pv*(x - rv)**3, need_pass=False)
    if w is not None: vs.append(w)
ablation(12, "(나)의 '점 (5, f(5))를 지난다'", vs, ans12)
# '삼차함수' 제거: 사차 f=4x+5+(x+1)^2(x-5)^2 (실근 없음 → |f|=f 미분가능) 도 (가)(나)를 만족
f4 = 4*x + 5 + (x + 1)**2*(x - 5)**2
assert sp.real_roots(Poly(expand(f4), x)) == []
vs = [ok12(F12), ok12(f4, deg=4)]
ablation(12, "'삼차함수'", [w for w in vs if w is not None], ans12, why='예: f=4x+5+(x+1)^2(x-5)^2')

print('ALL OK')
