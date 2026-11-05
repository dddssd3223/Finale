# -*- coding: utf-8 -*-
# p18.py (1회 18번 Claude 후보, 원본 J33) 검증
# 원문 풀이(38/3) · 설정 줄 불통 · 조건 해석의 전수 조사(유일성) · 정답 = ④ · 선지 등차 · 오답 값 · 조건 빼 보기 · 문장 길이
import os, re, sys
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
from items_common import COND
import items_final as F
x, u, a, b, kk = sp.symbols('x u a b k', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claude18' and it['key'] == 'J33' and it['ans'] == 4
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나', '다']
assert it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
CH = [sp.nsimplify(v) for v in it['choices']]

# ---------- 원문 J33 ----------
fo = -x**2 + a*x                                   # -1 <= x < 1
asol = sp.solve(sp.Eq(fo.subs(x, 1), fo.subs(x, -1) + 4), a)   # x=1에서 연속: f(1-) = f(-1)+4
assert asol == [2]
fo = fo.subs(a, 2)
def fJ(xv):                                        # f(x)=f(x-2)+4 로 확장
    n = sp.floor((xv + 1) / 2)
    return fo.subs(x, xv - 2*n) + 4*n
# [-2,0]: [-2,-1)은 f(x+2)-4, [-1,0]은 기본식. 영점은 x=0 하나(증가함수)
A_ = sp.integrate(-(fo.subs(x, x + 2) - 4), (x, -2, -1)) + sp.integrate(-fo, (x, -1, 0))
B_ = sp.integrate(fo, (x, 0, 1)) + sp.integrate(fo.subs(x, x - 2) + 4, (x, 1, 3))
assert all(fJ(R(v, 4)) < 0 for v in range(-8, 0)) and all(fJ(R(v, 4)) > 0 for v in range(1, 13))
assert (A_, B_, A_ + B_) == (R(14, 3), 8, R(38, 3))
assert F.I['J33'][2] == '②' and F.I['J33'][1][1] == '\\dfrac{38}3'
print('원문 J33: 연속 → a=2, A=14/3, B=8, A+B=38/3 (②) OK')

# ---------- 모형: f(x) = -3x^2 + a x + b (0<=x<2), g(x+2)=g(x)+k ----------
f = lambda av, bv: -3*u**2 + av*u + bv
# 연속 ⇔ x=2에서 연속 ⇔ f(2) = f(0) + k (다른 짝수점은 평행이동으로 같은 식)
ksol = sp.solve(sp.Eq((-3*u**2 + a*u + b).subs(u, 2), b + kk), kk)
assert ksol == [2*a - 12]
K = lambda av: 2*av - 12
# 설정 줄 불통: 연속 조건은 a, b를 정하지 못한다 (서로 다른 (a,b,k)가 모두 연속)
for av, bv in ((12, 0), (8, 0), (10, -1)):
    assert sp.expand(f(av, bv).subs(u, 2) - (bv + K(av))) == 0
print('설정 줄 불통: 연속은 k=2a-12만 준다 (a, b 미정)')

def g_at(av, bv, xv):
    n = sp.floor(sp.nsimplify(xv) / 2)
    return f(av, bv).subs(u, xv - 2*n) + n*K(av)

def zeros(av, bv):
    """곡선 y=g(x)와 x축의 교점 x좌표 집합 (k=0이고 근이 있으면 무한 → None)"""
    k = K(av); fx = f(av, bv)
    if k == 0:
        rr = [r for r in sp.real_roots(sp.Poly(fx, u)) if 0 <= r < 2]
        return None if rr else set()
    # f의 [0,2] 위의 값의 범위
    cands = [0, 2] + ([sp.Rational(av) / 6] if 0 < sp.Rational(av) / 6 < 2 else [])
    vals = [fx.subs(u, c) for c in cands]
    lo, hi = min(vals), max(vals)
    js = range(int(sp.floor(min(-hi / k, -lo / k))) - 1, int(sp.ceiling(max(-hi / k, -lo / k))) + 2)
    Z = set()
    for j in js:
        for r in sp.real_roots(sp.Poly(sp.expand(fx + j*k), u)):
            if 0 <= r < 2:
                Z.add(sp.nsimplify(2*j + r) if r.is_rational else 2*j + r)
    return Z

def count(av, bv):
    Z = zeros(av, bv)
    return sp.oo if Z is None else len(Z)

def min_ge0(av, bv):
    """x>=0에서 g의 최솟값 (없으면 None). k<0이면 g(2n)=b+nk → -∞. k>=0이면 [2j,2j+2)의 값 = f + jk ≥ f."""
    k = K(av); fx = f(av, bv)
    if k < 0:
        return None
    # [0,2)에서 f(위로 볼록)의 하한은 min(f(0), f(2)) = min(b, b+k) = b (x=0에서 달성)
    inf02 = min(fx.subs(u, 0), fx.subs(u, 2))
    assert inf02 == fx.subs(u, 0)
    return fx.subs(u, 0)

def phi(av, bv):
    """∫_{-1}^{0} |g(x)| dx  (-2<=x<0에서 g = f(x+2) - k)"""
    gl = sp.expand(f(av, bv).subs(u, x + 2) - K(av))
    rr = sorted(r for r in sp.real_roots(sp.Poly(gl, x)) if -1 < r < 0)
    pts = [-1] + rr + [0]
    return sp.nsimplify(sum(abs(sp.integrate(gl, (x, p, q))) for p, q in zip(pts, pts[1:])))

def ok(av, bv, need=('가', '나', '다')):
    res = True
    if '가' in need: res &= (min_ge0(av, bv) == 0)
    if '나' in need: res &= (count(av, bv) == 1)
    if '다' in need: res &= (phi(av, bv) == 1)
    return bool(res)

ASK = lambda av, bv: sp.nsimplify(sum(sp.integrate(f(av, bv) + j*K(av), (u, 0, 2)) for j in range(3)))
# ∫_0^6 g = 3∫_0^2 f + 6k = 18a + 6b - 96
assert sp.expand(ASK(a, b) - (18*a + 6*b - 96)) == 0

# ---------- (가) ⇔ b = 0, a ≥ 6 : 기호 + 격자 ----------
# k<0: g(2n)=b+nk → -∞ ; k>=0: f 위로 볼록 → [0,2)의 하한은 끝점 중 작은 값 b
assert sp.simplify(sp.Min((-3*u**2 + a*u + b).subs(u, 0), (-3*u**2 + a*u + b).subs(u, 2)).subs({a: 7, b: 0})) == 0
grid_a = [R(n, 4) for n in range(-8, 81)]
grid_b = [R(n, 4) for n in range(-12, 13)]
for av in grid_a:
    for bv in grid_b:
        assert (min_ge0(av, bv) == 0) == (bv == 0 and av >= 6), (av, bv)
# 검산: 실제 함숫값으로 x>=0에서 g >= b (k>=0)
for av in (6, 8, 12, 15):
    assert all(g_at(av, 0, R(v, 8)) >= 0 for v in range(0, 65))
assert g_at(5, 0, 20) < -5                          # k<0 예
print('(가) ⇔ b=0, a>=6 (k>=0) : 격자', len(grid_a) * len(grid_b), '쌍 일치')

# ---------- b=0, a>=6에서 (나): 교점 1개 ⇔ a >= 12 ----------
# a=6: k=0, g(2n)=0 무수히 많음 / 6<a<12: 원점(꺾여 닿음) + (a-12)/3 ∈ (-2,0) → 2개 이상 / a>=12: 증가 → 원점 하나
for av in [R(n, 4) for n in range(24, 81)]:
    c = count(av, 0)
    if av == 6:
        assert c == sp.oo
    elif av < 12:
        assert c >= 2 and {0, (av - 12) / 3} <= zeros(av, 0), (av, c)
    else:
        assert c == 1 and zeros(av, 0) == {0}, (av, c)
assert all(sp.diff(f(av, 0), u).subs(u, 2) >= 0 for av in (12, 13, 20))    # a>=12: f'(x)=-6x+a>=0 on [0,2]
# 원점은 꺾인 점: 좌미분계수 a-12, 우미분계수 a (6<a<12이면 좌우 모두 g>0 → x축에 닿기만 함)
for av in (8, 10):
    fl = sp.diff(f(av, 0).subs(u, x + 2) - K(av), x).subs(x, 0); fr = sp.diff(f(av, 0), u).subs(u, 0)
    assert (fl, fr) == (av - 12, av) and g_at(av, 0, R(-1, 100)) > 0 and g_at(av, 0, R(1, 100)) > 0
assert zeros(8, 0) == {R(-4, 3), 0}
print('(나) b=0, a>=6: 교점 1개 ⇔ a>=12 (a=6 무수히 많음, 6<a<12 원점에서 꺾여 닿고 (a-12)/3에서 또 만남)')

# ---------- (다): b=0, a>=12 → [-1,0]에서 g<=0 → (a-10)/2=1 → a=12 ----------
gl = sp.expand(f(a, 0).subs(u, x + 2) - K(a))
assert sp.expand(gl + x*(3*x + 12 - a)) == 0
assert sp.simplify(-sp.integrate(gl, (x, -1, 0)) - (a - 10)/2) == 0
assert sp.solve(sp.Eq(-sp.integrate(gl, (x, -1, 0)), 1), a) == [12]
# 참고: a>=6 전체에서 (다)의 해는 a=8(6<=a<=9, g>=0), a=12(a>=12, g<=0); 9<a<12는 e=3√6/2>3 모순
e = sp.symbols('e', positive=True)
P2 = sp.expand(sp.integrate(x*(3*x + e), (x, -1, -e/3)) + sp.integrate(-x*(3*x + e), (x, -e/3, 0)))
assert sp.expand(P2 - (1 - e/2 + e**3/27)) == 0 and sp.solve(sp.Eq(P2, 1), e) == [3*sp.sqrt(6)/2]
assert sp.solve(sp.Eq(sp.integrate(gl, (x, -1, 0)), 1), a) == [8]
for av in grid_a:
    if av >= 6:
        assert (phi(av, 0) == 1) == (av in (8, 12)), av
print('(다) b=0: a>=12에서 (a-10)/2=1 → a=12 (a>=6 전체로는 a=8, 12; a=8은 (나)에서 교점 2개라 제외)')

# ---------- 전수 격자 확인: 세 조건을 모두 만족하는 (a,b)는 (12,0)뿐 ----------
sols = [(av, bv) for av in [R(n, 4) for n in range(-8, 81)] for bv in [R(n, 4) for n in range(-12, 13)] if ok(av, bv)]
assert sols == [(12, 0)], sols
fA = f(12, 0); ans = ASK(12, 0)
assert ans == 120 and CH[it['ans'] - 1] == ans
print(f'유일한 f(x) = {sp.expand(fA.subs(u, x))}, k = 12, ∫_0^6 g = {ans} = ④')

# ---------- 선지: 서로 다름, 등차, 오름차순 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {1}
print('선지', [str(v) for v in CH], '공차 1 (오름차순)')

# ---------- 오답 근거 값 (모두 선지 밖으로 적었는지) ----------
w8 = ASK(8, 0)                                     # 절댓값 무시·(나) 미확인
w_alt = ASK(10, -1)                                # (가) 미사용
w_k = sp.nsimplify(sum(sp.integrate(fA, (u, 0, 2)) + j*12 for j in range(3)))  # 길이 2를 안 곱함
assert (w8, w_alt, w_k) == (48, 78, 84)
assert sp.solve(sp.Eq(sp.integrate(gl, (x, -1, 0)), 1), a) == [8]
assert all(v not in CH for v in (w8, w_alt, w_k))
for s_ in ('48', '78', '84', '-3x^2+10x-1', '선지 밖'):
    assert s_ in it['wrong'], s_
print('오답 근거 값: 48(절댓값 무시·(나) 미확인), 78((가) 미사용), 84(이동량 2k → k) — 모두 선지 밖으로 적음')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# (가) 제거: (나)(다)만 → f=-3x^2+10x-1 (k=8)도 만족 (x>=0에서 최솟값 -1)
assert ok(10, -1, ('나', '다')) and not ok(10, -1) and min_ge0(10, -1) == -1 and count(10, -1) == 1
print(f'ABLATION 18 (가): 필요(정해지지 않음: (나)(다)만이면 f=-3x^2+10x-1도 만족, {ans} 또는 {w_alt})')
# (나) 제거: (가)(다)만 → a=8 도 만족
assert ok(8, 0, ('가', '다')) and count(8, 0) == 2
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)(다)만이면 a=8, 12 → {w8} 또는 {ans})')
# (다) 제거: (가)(나)만 → a>=12 전부
alt = {av: ASK(av, 0) for av in (13, 14, 16)}
assert all(ok(av, 0, ('가', '나')) for av in alt) and len(set(alt.values()) | {ans}) == 4
print(f'ABLATION 18 (다): 필요(정해지지 않음: (가)(나)만이면 a>=12, 예 a=13→{alt[13]}, a=14→{alt[14]})')

# ---------- 문장 길이 (태그·공백 제거, 조건 포함) ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['J33'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 193 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개, 원문 0개)')
print('ALL OK')
