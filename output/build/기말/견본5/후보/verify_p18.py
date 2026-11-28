# -*- coding: utf-8 -*-
# p18.py (견본5 18번 Claude 후보 claude18, 원본 D40) 검증
# 원문 풀이(50) · 조건 해석 전수(유일성) · 정답 ③ · 선지 등차 · 오답 값 · 조건 빼 보기 · 문장 길이
import os, re, sys, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '부교재_기말'))
from items_common import COND
import items_final as F
x, a, b, c, p, q, r, s = sp.symbols('x a b c p q r s', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claude18' and it['key'] == 'D40' and it['ans'] == 3
assert it['src'] == F.I['D40'][3] and it['level'] == '상'
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나', '다']
CH = [sp.nsimplify(v) for v in it['choices']]
M = 32                                   # 직선 y = 32x

# ---------- 도구 ----------
def nreal(poly):
    """서로 다른 실근의 개수 (정확한 계산)"""
    P = sp.Poly(sp.expand(poly), x)
    return len(set(sp.real_roots(P)))

def realset(poly):
    return sorted(set(sp.real_roots(sp.Poly(sp.expand(poly), x))))

def nonneg(f):
    """모든 실수 x에서 f(x) >= 0 (실근 사이·바깥 점 검사, 실근 유한)"""
    rr = realset(f)
    probes = ([rr[0] - 1] + [(rr[i] + rr[i + 1]) / 2 for i in range(len(rr) - 1)] + [rr[-1] + 1]) if rr else [0]
    return all(sp.nsimplify(f.subs(x, t)) >= 0 for t in probes)

def ok(f, need=('가', '나', '다')):
    f = sp.expand(f)
    assert sp.Poly(f, x).degree() == 4 and sp.Poly(f, x).LC() == 1
    res = True
    if '가' in need: res &= nonneg(f) and nreal(f) == 2
    if '가f' in need: res &= nonneg(f)              # (가)의 앞부분만
    if '가2' in need: res &= nreal(f) == 2           # (가)의 뒷부분만
    if '나' in need: res &= sp.diff(f, x).subs(x, 0) == 0
    if '다' in need: res &= nreal(f - M * x) == 3
    return bool(res)

ASK = lambda f: sum(realset(f - M * x))           # 직선과 곡선의 모든 교점의 x좌표의 합

# ---------- 원문 D40 ----------
fo = x**3 - 12*x**2 + 45*x
assert fo.subs(x, 0) == 0 and nreal(fo - 9*x) == 2
assert sp.expand(sp.diff(fo, x) - 3*(x - 5)*(x - 3)) == 0
assert sp.expand(fo - 9*x - x*(x - 6)**2) == 0
# 원문 유일성: f = x^3 + p x^2 + q x, f - 9x = x(x^2 + p x + q - 9). 교점 2개 ⇔ Q(0)=0(원점 접함) 또는 Q가 0 아닌 중근
fpq = x**3 + p*x**2 + q*x
# (A) Q(0)=0: q=9 → f'(3)=0 → p=-6 → f'=3(x-1)(x-3): x=3 극소 → 버림
fA = fpq.subs(q, 9); pA = sp.solve(sp.diff(fA, x).subs(x, 3), p); assert pA == [-6]
assert sp.expand(sp.diff(fA.subs(p, -6), x) - 3*(x - 3)*(x - 1)) == 0     # 극대는 x=1, x=3은 극소
# (B) Q=(x-s)^2 (s≠0): f'(3)=(s-6)^2=0 → s=6
fB = x*(x - s)**2 + 9*x
assert sp.expand(sp.diff(fB, x).subs(x, 3) - (s - 6)**2) == 0
assert sp.expand(fB.subs(s, 6) - fo) == 0
assert fo.subs(x, 5) == 50 and F.I['D40'][2] == '50'
print('원문 D40: f-9x=x(x-6)^2 (x^2(x-p)형은 x=3 극소로 버림), f=x^3-12x^2+45x, 극솟값 f(5)=50 OK')

# ---------- (가) ⇒ f=(x-a)^2(x-b)^2 ----------
# 최고차항의 계수 1인 사차함수가 서로 다른 실근 2개를 가질 때 중복도는 (1,1)+허근 이차식, (1,3), (3,1), (2,2)뿐이다.
# 홀수 중복도의 근에서는 부호가 바뀌므로 f>=0이면 (2,2)만 남는다. 대표 예로 부호 변화를 확인한다.
pats = {'(1,1)q': (x + 1)*(x - 2)*(x**2 + 1), '(1,3)': (x + 1)*(x - 2)**3, '(3,1)': (x + 1)**3*(x - 2), '(2,2)': (x + 1)**2*(x - 2)**2}
for k, fp_ in pats.items():
    assert nreal(fp_) == 2
    assert nonneg(fp_) == (k == '(2,2)'), k
print('(가): f>=0이고 실근 2개 ⇔ f=(x-a)^2(x-b)^2 (홀수 중복도는 부호 변화) OK')

# ---------- (나): f'(0)=0 ⇔ 0∈{a, b, (a+b)/2} ----------
fab = (x - a)**2*(x - b)**2
assert sp.factor(sp.diff(fab, x) - 2*(x - a)*(x - b)*(2*x - a - b)) == 0
assert sp.expand(sp.diff(fab, x).subs(x, 0) + 2*a*b*(a + b)) == 0
assert set(sp.solve(sp.diff(fab, x).subs({x: 0, a: 1}), b)) == {0, -1}
print("(나): f'(0)=-2ab(a+b)=0 ⇔ a=0 또는 b=0 또는 a+b=0 OK")

# ---------- 경우 (i) a+b=0: f=(x^2-r^2)^2 (r>0) → 교점 항상 2개 ----------
hR = sp.expand((x**2 - r**2)**2 - M*x)
DR = sp.factor(sp.discriminant(hR, x))
posR = [z for z in sp.Poly(DR, r).nroots(n=30) if abs(sp.im(z)) < 1e-20 and sp.re(z) > 0]
assert posR == [], posR                     # r>0에서 판별식이 0이 되지 않음 → 서로 다른 실근 개수가 일정
for rv in [R(1, 3), R(1), R(2), R(3), R(5), R(10)]:
    assert nreal(hR.subs(r, rv)) == 2
    assert not ok((x**2 - rv**2)**2)
# 원리 확인: 원점을 지나는 직선이 접하려면 접점 t에서 f(t)=t f'(t) → (3t^2+r^2)(t^2-r^2)=0 → t=±r, 기울기 f'(±r)=0
tt = sp.symbols('t', real=True)
fr = (tt**2 - r**2)**2
assert sp.expand(fr - tt*sp.diff(fr, tt) + (tt - r)*(tt + r)*(3*tt**2 + r**2)) == 0
print('경우 (i) 원점이 가운데 극대점: 판별식', DR, '→ r>0에서 교점 항상 2개, (다) 불만족 OK')

# ---------- 경우 (ii) a=0 또는 b=0: f=x^2(x-c)^2 (c≠0) ----------
g = sp.expand(x*(x - c)**2 - M)                 # f-32x = x·g(x), g(0)=-32≠0 → 원점은 단순 교점
assert sp.expand(x**2*(x - c)**2 - M*x - x*g) == 0 and g.subs(x, 0) == -32
assert sp.expand(sp.diff(g, x) - (x - c)*(3*x - c)) == 0
assert sp.expand(g.subs(x, c)) == -32                                   # x=c는 중근 후보가 아님 (f'(c)=0≠32)
assert sp.expand(g.subs(x, c/3) - (R(4, 27)*c**3 - 32)) == 0
Dg = sp.factor(sp.discriminant(g, x))
cr = sorted(set(sp.real_roots(sp.Poly(Dg, c))))
assert cr == [6], (Dg, cr)
# 교점 개수 = 1 + (g의 서로 다른 실근 개수). 판별식 0인 c=6에서만 g가 중근 → 3개. 나머지에선 2개(판별식<0) 또는 4개(판별식>0)
for cv in [R(-9), R(-6), R(-1), R(1, 2), R(1), R(3), R(5), R(59, 10), R(6), R(61, 10), R(7), R(9), R(12)]:
    n = nreal(x**2*(x - cv)**2 - M*x)
    sgn = sp.sign(Dg.subs(c, cv))
    assert n == {-1: 2, 0: 3, 1: 4}[sgn], (cv, n, sgn)
    assert ok(x**2*(x - cv)**2) == (cv == 6)
print('경우 (ii) 원점이 중근: g=x(x-c)^2-32, 판별식', Dg, '→ 실수 c는 6뿐 (c=6에서만 교점 3개) OK')

# ---------- 결론 ----------
fA6 = sp.expand(x**2*(x - 6)**2)
assert ok(fA6)
assert sp.expand(fA6 - M*x - x*(x - 8)*(x - 2)**2) == 0
assert realset(fA6 - M*x) == [0, 2, 8]
ans = ASK(fA6)
assert ans == 10 and CH[it['ans'] - 1] == ans
print(f'유일한 f = x^2(x-6)^2, f-32x = x(x-2)^2(x-8), 교점 x = 0, 2, 8, 합 {ans} = ③')

# 보조: 정수 격자 전수 (a<b, -12..12) — 조건을 모두 만족하는 (a,b)는 (0,6)뿐
hits = [(av, bv) for av, bv in itertools.combinations(range(-12, 13), 2) if ok((x - av)**2*(x - bv)**2)]
assert hits == [(0, 6)], hits
print('정수 격자 전수 (a,b) =', hits, 'OK')

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and len(dif) == 1 and list(dif)[0] != 0
print('선지', [str(v) for v in CH], '공차', list(dif)[0])

# ---------- 오답 근거 ----------
f6 = sp.expand(x**2*(x**2 - 10*x + 32))                  # ① (가)의 '실근 2개' 누락
assert nonneg(f6) and nreal(f6) == 1 and sp.diff(f6, x).subs(x, 0) == 0
assert sp.expand(f6 - M*x - x*(x - 2)*(x - 4)**2) == 0 and ASK(f6) == 6
assert ok(f6, ('가f', '나', '다')) and not ok(f6)
w_tangent_dropped = 0 + 8                                 # ② 접점 x=2를 뺌
w_vieta = -sp.Poly(fA6 - M*x, x).all_coeffs()[1]          # ④ 근과 계수의 관계(중복 포함) 12
w_confuse = 0 + 6 + 8                                     # ⑤ f의 중근 6을 접점으로 혼동
assert w_vieta == 12
wv = {'①': ASK(f6), '②': w_tangent_dropped, '④': w_vieta, '⑤': w_confuse}
for lab, v in wv.items():
    assert v in CH and v != ans and CH.index(v) + 1 == '①②③④⑤'.index(lab) + 1, (lab, v)
    assert lab in it['wrong'] and f'\\({v}\\)' in it['wrong']
print('오답 근거: ①6(실근 2개 누락: x^2(x^2-10x+32)) ②8(접점 누락) ④12(중근 중복, 근과 계수) ⑤14(f의 중근 6 혼동) — 모두 선지에 있음')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
fB3 = sp.expand(x**3*(x + 6))                            # f>=0을 빼면: x축과 두 점(0, -6), f'(0)=0, y=32x와 x=-4(접), 0, 2
assert ok(fB3, ('가2', '나', '다')) and not nonneg(fB3)
assert sp.expand(fB3 - M*x - x*(x - 2)*(x + 4)**2) == 0 and ASK(fB3) == -2
alt_ga = {ASK(fA6), ASK(f6), ASK(fB3)}
assert all(ok(ff, ('나', '다')) for ff in (fA6, f6, fB3)) and len(alt_ga) == 3
print(f'ABLATION 18 (가): 필요(정해지지 않음: (나)(다)만이면 x^2(x-6)^2→10, x^2(x^2-10x+32)→6, x^3(x+6)→-2)')
print(f'ABLATION 18 (가)의 f>=0: 필요(답 바뀜: x^3(x+6)도 만족, 10 → -2)')
print(f'ABLATION 18 (가)의 실근 2개: 필요(답 바뀜: x^2(x^2-10x+32)도 만족, 10 → 6)')
# (나) 제거: (가)(다)만 → 원점을 지나지 않는 W도 가능. 폭 6(근 s±3)인 W를 옮기면 원점 아닌 위치에서도 접함
hs = sp.expand(((x - s)**2 - 9)**2 - M*x)
Ds = sp.factor(sp.discriminant(hs, x))
s1 = [z for z in sp.solve(32*s**2 + 15*s - 279, s) if z > 0][0]          # (-15+33√33)/64
assert sp.simplify(Ds.subs(s, s1)) == 0 and s1 != 3
fw = ((x - s1)**2 - 9)**2
KQ = sp.QQ.algebraic_field(sp.sqrt(33))
HW = sp.Poly(sp.expand(fw - M*x), x, domain=KQ)
GW = sp.gcd(HW, HW.diff(x))                                               # 중근 인수 (정확)
assert GW.degree() == 1
tw = sp.nsimplify(sp.simplify(-GW.all_coeffs()[1] / GW.all_coeffs()[0]))
QW, RW = sp.div(HW, sp.Poly((x - tw)**2, x, domain=KQ))
assert RW.is_zero
QW = QW.as_expr(); dQ = sp.simplify(sp.discriminant(QW, x))
assert dQ.is_positive and sp.simplify(QW.subs(x, tw)) != 0                # 나머지 두 근은 서로 다르고 중근과도 다름 → 교점 3개
sum_w = sp.simplify(tw + sum(sp.solve(QW, x)))
assert sp.N(sum_w - 10) > 0.5 and sp.N(sp.diff(fw, x).subs(x, 0)) != 0    # 합≠10, f'(0)≠0
assert sp.expand(fw - (x - s1 + 3)**2*(x - s1 - 3)**2) == 0                # (가): 두 제곱의 곱이라 f>=0, 서로 다른 실근 s1±3 두 개
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)(다)만이면 f=((x-s)^2-9)^2, s=(-15+33√33)/64도 x={sp.N(tw, 6)}에서 접해 교점 3개, 합 {sum_w}≈{sp.N(sum_w, 6)}≠10)')
# (다) 제거: (가)(나)만 → c 자유
alt_da = {cv: (nreal(x**2*(x - cv)**2 - M*x), ASK(x**2*(x - cv)**2)) for cv in (3, 6, 9)}
assert alt_da[3][0] == 2 and alt_da[9][0] == 4 and len({v[1] for v in alt_da.values()}) == 3
assert all(ok(x**2*(x - cv)**2, ('가', '나')) for cv in (3, 6, 9))
print(f'ABLATION 18 (다): 필요(정해지지 않음: (가)(나)만이면 x^2(x-c)^2 모두 가능, c=3: 교점 2개, c=9: 교점 4개, 합 {[round(float(sp.N(v[1])), 4) for v in alt_da.values()]})')

# ---------- 문장 길이 (태그·공백 제거, 조건 포함) ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['D40'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 142 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자(조건 2개), 변형 {Lm}자(조건 {len(it["cond"])}개)')
print('ALL OK')
