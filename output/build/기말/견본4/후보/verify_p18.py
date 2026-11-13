# -*- coding: utf-8 -*-
# p18.py (견본4 18번 Claude 후보, 원본 I44) 검증
# 원문 풀이(52) · 조건 해석의 전수 조사(유일성) · 정답 = ① · 선지 등차 · 오답 값 · 조건 빼 보기 · 문장 길이
import os, re, sys
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '부교재_기말'))
from items_common import COND
import items_final as F
x, t, a, b, c, d, s = sp.symbols('x t a b c d s', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claude18' and it['key'] == 'I44' and it['ans'] == 1
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나', '다']
CH = [sp.nsimplify(v) for v in it['choices']]

# ---------- 도구: g(t) = |f(x)-t|가 미분가능하지 않은 x의 개수 = f(x)-t의 단순 실근 개수 ----------
def g_of(f, tv):
    P = sp.Poly(sp.expand(f - tv), x)
    cnt = 0
    for fac, m in sp.sqf_list(P)[1]:
        if m == 1:
            cnt += len(sp.real_roots(fac))
    return cnt

def crit_values(f):
    fp = sp.Poly(sp.diff(f, x), x)
    pts = sorted(set(sp.real_roots(fp)))
    return pts, sorted(set(sp.nsimplify(sp.expand(f.subs(x, p))) for p in pts))

def disc_points(f):
    """g(t)가 불연속인 t 전부. g는 임계값 사이에서 상수이므로 임계값과 그 좌우만 보면 된다."""
    _, cv = crit_values(f)
    gap = min([cv[i + 1] - cv[i] for i in range(len(cv) - 1)] + [1])
    e = sp.nsimplify(gap) / 4
    return [v for v in cv if not (g_of(f, v) == g_of(f, v - e) == g_of(f, v + e))]

def h_increasing(f):
    """h(x)=∫_0^x t f'(t)dt 증가 ⇔ x f'(x) ≥ 0 (영점 유한). x f'(x)의 실근 사이·바깥 부호를 전부 확인"""
    hp = sp.expand(x * sp.diff(f, x))
    if hp == 0:
        return False
    rr = sorted(set(sp.real_roots(sp.Poly(hp, x))))
    probes = ([rr[0] - 1] + [(rr[i] + rr[i + 1]) / 2 for i in range(len(rr) - 1)] + [rr[-1] + 1]) if rr else [0]
    return all(hp.subs(x, sp.nsimplify(q)) > 0 for q in probes)

def ok_all(f, need=('가', '나', '다')):
    res = True
    if '가' in need: res &= sp.expand(sp.diff(f, x).subs(x, 1)) == 12
    if '나' in need: res &= h_increasing(f)
    if '다' in need:
        dp = disc_points(f)
        res &= (len(dp) == 2 and dp[0] == 0 and dp[1] > 0)
    return bool(res)

ASK = lambda f: 5 * sp.integrate(f, (x, -1, 1))

# ---------- 원문 I44 ----------
fo = x**3 - 3*x**2 - 9*x + 27
assert sp.diff(fo, x).subs(x, -1) == 0
A_ = sp.symbols('A_', real=True)
assert sp.simplify(sp.integrate(sp.diff(fo, x), (x, 1, -A_)) + sp.integrate(sp.diff(fo, x), (x, 1, A_ + 2))) == 0
assert disc_points(fo) == [0, 32]
# 원문 유일성: x^3+ax^2+bx+c, (나) 항등식 → 계수 비교, (가), (다) 극솟값 0
fc = x**3 + a*x**2 + b*x + c
idn = sp.Poly(sp.expand(fc.subs(x, -A_) + fc.subs(x, A_ + 2) - 2*fc.subs(x, 1)), A_).all_coeffs()
sol_o = sp.solve(idn + [sp.diff(fc, x).subs(x, -1)], [a, b], dict=True)
assert sol_o == [{a: -3, b: -9}]
fco = fc.subs(sol_o[0])
cands_o = [cv for cv in sp.solve(sp.Eq(fco.subs(x, 3), 0), c)]  # 극솟값 0 (극댓값 = p > 0)
assert cands_o == [27] and sp.integrate(fco.subs(c, 27), (x, -1, 1)) == 52
assert F.I['I44'][2] == '④' and F.I['I44'][1][3] == '52'
print('원문 I44: f=x^3-3x^2-9x+27, g 불연속 t=0, 32, ∫_{-1}^{1} f = 52 (④) OK')

# ---------- 전수 조사: f = 3x^4 + a x^3 + b x^2 + c x + d ----------
f = 3*x**4 + a*x**3 + b*x**2 + c*x + d
fp = sp.diff(f, x)
# (나) x f'(x) ≥ 0: x f'(x) = c x + (2b) x^2 + ...  → c ≠ 0이면 x=0 좌우에서 부호가 바뀜 → c = 0
xfp = sp.expand(x * fp)
assert xfp.coeff(x, 1) == c and xfp.coeff(x, 0) == 0
for cv in (R(1), R(-1), R(1, 7)):           # c≠0 예: 0 근처 양쪽 부호가 반대
    hp = xfp.subs({c: cv, a: 0, b: 0})
    eps = R(1, 10**4)
    assert sp.sign(hp.subs(x, eps)) == -sp.sign(hp.subs(x, -eps))
# c = 0이면 x f'(x) = x^2 q(x), q(x) = 12x^2 + 3a x + 2b ≥ 0 ⇔ 판별식 ≤ 0
q = sp.expand(fp.subs(c, 0) / x)
assert sp.expand(q - (12*x**2 + 3*a*x + 2*b)) == 0
# (가) f'(1) = 12 → b = -3a/2
bsol = sp.solve(sp.Eq(fp.subs({c: 0, x: 1}), 12), b)
assert bsol == [-3*a/2]
Dn = sp.expand(sp.discriminant(q.subs(b, -3*a/2), x))   # (3a)^2 - 4·12·2b, b=-3a/2
assert Dn == 9*a**2 + 144*a
amin, amax = sp.solve(sp.Eq(Dn, 0), a)
assert sorted([amin, amax]) == [-16, 0]
# 판별식 < 0 (−16 < a < 0): q > 0 → 임계점 x=0 하나 → 불연속점 1개.  a = 0: f'=12x^3 → 1개.  a = −16: 2개
fam = lambda av, dv: f.subs({c: 0, b: -3*sp.nsimplify(av)/2, a: sp.nsimplify(av), d: dv})
for av in [R(k, 4) for k in range(-64, 1)]:      # a ∈ [−16, 0]을 1/4 간격으로 전수
    fa = fam(av, 0)
    assert h_increasing(fa) and sp.diff(fa, x).subs(x, 1) == 12
    n = len(disc_points(fa))
    assert n == (2 if av == -16 else 1), (av, n)
# 판별식 < 0 이면 q의 실근이 없음(기호)
assert all(not sp.real_roots(sp.Poly(q.subs({b: -3*av/2, a: av}), x)) for av in (R(-15), R(-8), R(-1, 3)))
# a = −16: f = 3x^4 − 16x^3 + 24x^2 + d, 임계값 d (x=0), d+16 (x=2) → (다) {d, d+16} = {0, p}, p>0 → d = 0
f16 = fam(-16, d)
assert sp.expand(sp.diff(f16, x) - 12*x*(x - 2)**2) == 0
dsols = [dv for dv in sp.solve(sp.Eq(f16.subs(x, 0), 0), d) + sp.solve(sp.Eq(f16.subs(x, 2), 0), d)]
valid = []
for dv in dsols:
    fx = f16.subs(d, dv)
    dp = disc_points(fx)
    if len(dp) == 2 and 0 in dp and [v for v in dp if v != 0][0] > 0 and ok_all(fx):
        valid.append(dv)
assert valid == [0]
fA = sp.expand(f16.subs(d, 0))
assert fA == 3*x**4 - 16*x**3 + 24*x**2 and disc_points(fA) == [0, 16]
# g(t) 표: t<0:0, t=0:0, 0<t<16:2, t=16:1, t>16:2 (삼중근 x=2는 꺾이지 않음)
assert [g_of(fA, v) for v in (-1, 0, 8, 16, 20)] == [0, 0, 2, 1, 2]
assert sp.expand(fA - 16 - (x - 2)**3 * (3*x + 2)) == 0
ans = ASK(fA)
assert ans == 86 and CH[it['ans'] - 1] == ans
print(f'유일한 f = {fA}, p = 16, 5∫_{{-1}}^1 f = {ans} = ①')

# ---------- 선지: 서로 다름, 등차 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and len(dif) == 1 and list(dif)[0] != 0
print('선지', [str(v) for v in CH], '공차', list(dif)[0])

# ---------- 오답 근거 값 ----------
w_odd = 5 * 2 * sp.integrate(fA, (x, 0, 1))          # 홀수차항을 지우지 않고 2∫_0^1 f
fQ = 3*x**4                                          # (가)의 경계근 r=0
fN = fA - 16                                         # p>0 무시: 변곡점 높이를 0으로
assert sp.diff(fQ, x).subs(x, 1) == 12 and h_increasing(fQ) and disc_points(fQ) == [0]
assert sp.diff(fN, x).subs(x, 1) == 12 and h_increasing(fN) and disc_points(fN) == [-16, 0]
fR = 3*x**4 - 8*x**3 + 6*x**2                         # (1-r)^2=1을 r=1로 잘못 풂
assert sp.expand(sp.diff(fR, x) - 12*x*(x-1)**2) == 0 and sp.diff(fR, x).subs(x, 1) == 0
wv = dict(odd=w_odd, Q=ASK(fQ), R=ASK(fR), N=ASK(fN))
assert wv == dict(odd=46, Q=6, R=26, N=-74)
assert all(v in CH and v != ans for v in (46, 6, 26))
assert [CH.index(v) + 1 for v in (46, 26, 6)] == [3, 4, 5]
assert all(v > 0 for v in CH)                         # f>=0이므로 음수 선지 없음
for v, lab in ((46, '③'), (26, '④'), (6, '⑤')):
    assert lab in it['wrong'] and str(v) in it['wrong']
print('오답 근거 값: ③46(홀수차항 미소거) ④26(r=1로 잘못 풂) ⑤6(경계 r=0, f=3x^4) — 모두 선지에 있음, 음수 선지 없음 (참고: p>0 무시 -74는 선지 밖)')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# (가) 제거: (나)(다)만 → f' = 12x(x-r)^2 (r≠0), 최솟값 0: r마다 다른 값
fr = lambda rv: sp.expand(sp.integrate(12*x*(x - rv)**2, (x, 0, x)))
alt_a = {rv: ASK(fr(rv)) for rv in (1, 2, -1, 3)}
assert all(ok_all(fr(rv), ('나', '다')) for rv in alt_a) and len(set(alt_a.values())) >= 2
print(f'ABLATION 18 (가): 필요(정해지지 않음: (나)(다)만이면 f\'=12x(x-r)^2, r=1→{alt_a[1]}, r=2→{alt_a[2]}, r=3→{alt_a[3]})')
# (나) 제거: (가)(다)만 → W형 3x^2(x-3)^2도 만족 (원문 원리 줄 '불연속점=극솟값·극댓값' 그대로)
fW = sp.expand(3*x**2*(x - 3)**2)
assert ok_all(fW, ('가', '다')) and not h_increasing(fW) and disc_points(fW) == [0, R(243, 16)]
assert ok_all(fA, ('가', '다'))
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)(다)만이면 W형 3x^2(x-3)^2도 만족, {ans} 또는 {ASK(fW)})')
# (다) 제거: (가)(나)만 → 상수 d, q 모두 자유
fD1 = fA + 1; fD2 = sp.expand(sp.integrate(12*x*(x**2 - x + 1), (x, 0, x)))   # q=x^2-x+1>0, q(1)=1
assert ok_all(fD1, ('가', '나')) and ok_all(fD2, ('가', '나'))
assert len({ASK(fA), ASK(fD1), ASK(fD2)}) == 3
print(f'ABLATION 18 (다): 필요(정해지지 않음: (가)(나)만이면 {ans}, {ASK(fD1)}(상수 +1), {ASK(fD2)}(q=x^2-x+1) 등)')
# (다)의 '양수 p' 제거
assert len(disc_points(fN)) == 2 and 0 in disc_points(fN)
print(f'ABLATION 18 (다)의 p>0: 필요(답 바뀜 {ans} → {ASK(fN)} 도 가능)')

# ---------- 문장 길이 (태그·공백 제거, 조건 포함) ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['I44'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 301 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개)')
print('ALL OK')
