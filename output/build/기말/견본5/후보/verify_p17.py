# -*- coding: utf-8 -*-
# p17.py (견본5 17번 Claude 후보 claude17) 검증
# 원문 I37 풀이(-3) · (가) 함수 결정 유일성 · (나) 구간별 정확 판정 + 유리수 전수 · 선지 등차 · 오답 근거 값 · 조건 빼 보기 · 원문 원리 줄 불통 · 길이
import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy import Rational as R, Poly, real_roots

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p17.py')).read(), ns)
IT = ns['ITEMS']; P = IT[17]
assert list(IT) == [17] and P['author'] == 'claude' and P['cand'] == 'claude17' and P['key'] == 'I37'
assert len(P['cond']) == 2 and [c[0] for c in P['cond']] == ['가', '나']
assert P['core']['axis'] == '①' and all(P['core'][k] for k in ('setting', 'principle', 'new'))
x, a = sp.symbols('x a', real=True)

def tools(f):
    """f의 부정적분 F, 정적분 I(p,q), 절댓값 정적분 A(p,q) (근에서 나눠 정확 계산)"""
    F = sp.integrate(f, x)
    rts = sorted(set(real_roots(Poly(f, x)))) if Poly(f, x).degree() > 0 else []
    I = lambda p, q: sp.nsimplify(F.subs(x, q) - F.subs(x, p))
    def A(p, q):
        pts = [p] + [r for r in rts if p < r < q] + [q]
        return sp.simplify(sum(abs(I(pts[i], pts[i + 1])) for i in range(len(pts) - 1)))
    return F, I, A

def cond_ga(f, av):
    _, I, A = tools(f)
    return sp.simplify(A(0, av) - (I(0, 1) - I(1, av))) == 0

def cond_na(f, av, c=2):
    _, I, A = tools(f)
    return abs(I(0, av)) <= A(av - c, av)     # S = 곡선과 x축, x=a-2, x=a로 둘러싸인 부분의 넓이 = ∫_{a-2}^a |f|

f0 = -4 * x * (x - 1)
F0, I0, A0 = tools(f0)

# ===== 원문 I37: f=-4x(x-1), (나) |∫_0^a f| <= ∫_{1-a}^1 f ⇔ a<=3/2, f(a) 최솟값 -3 =====
sys.path.insert(0, '/home/user/Finale/template/db/parts'); sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
from items_common import COND
import items_final as F
grid = [1 + R(k, 40) for k in range(1, 200)]
orig_ok = [av for av in grid if abs(I0(0, av)) <= I0(1 - av, 1)]
assert orig_ok == [av for av in grid if av <= R(3, 2)]
assert all(I0(1 - av, 1) == I0(0, av) for av in grid[:20])      # 원문 원리: x=1/2 대칭으로 두 적분이 같음
assert f0.subs(x, R(3, 2)) == -3 and F.I['I37'][2] == '②' and F.I['I37'][1][1] == '-3'
print('원문 I37: (나) ⇔ a<=3/2, f(3/2)=-3 = 원문 정답 ② OK')

# ===== (가): f=±4x^2+bx 가운데 (가)를 만족시키는 것은 f=-4x(x-1)뿐 (모든 a>1에서) =====
for s in (4, -4):
    for b in [R(n, 4) for n in range(-48, 49)]:
        f = s * x**2 + b * x
        for av in (R(11, 10), R(3, 2), R(2), R(7, 2), R(5)):
            ok = cond_ga(f, av)
            assert ok == (s == -4 and b == 4), (s, b, av)
# 등호 조건 논리: ∫_0^a|f| - (∫_0^1 f - ∫_1^a f) = ∫_0^1(|f|-f) + ∫_1^a(|f|+f) >= 0, 등호 ⇔ [0,1]에서 f>=0, [1,a]에서 f<=0
print('(가) ⇔ f(x)=-4x(x-1) (b 1/4 간격 전수, 부호 ±) OK')

# ===== (나): f=-4x(x-1)에서 구간별 정확 판정 =====
Fx = sp.expand(F0)                                  # F(x)=2x^2-4x^3/3
assert sp.factor(Fx) == sp.factor(R(2, 3) * x**2 * (3 - 2 * x))
Fa = Fx.subs(x, a); Fs = Fx.subs(x, a - 2)
pos = lambda p, q: (Fx.subs(x, q) - Fx.subs(x, p))   # ∫_p^q f
# 구간별 S(a), |∫_0^a f| 다항식
S1 = -pos(a - 2, 0) + pos(0, 1) - pos(1, a)            # 1<a<2 : [a-2,0] f<0, [0,1] f>0, [1,a] f<0
S2 = pos(a - 2, 1) - pos(1, a)                          # 2<=a<3: [a-2,1] f>=0, [1,a] f<=0
S3 = -pos(a - 2, a)                                     # a>=3  : [a-2,a] f<=0
def positive_on(expr, lo, hi, closed_hi=False):
    p = Poly(sp.expand(expr), a)
    rs = [r for r in real_roots(p) if lo < r < hi or (closed_hi and r == hi)]
    mid = (lo + hi) / 2
    return not rs and expr.subs(a, mid) > 0
assert positive_on(S1 - Fa, 1, R(3, 2), True)           # (i-1) 1<a<=3/2, F(a)>=0
assert positive_on(S1 + Fa, R(3, 2), 2)                 # (i-2) 3/2<a<2,  F(a)<0
assert positive_on(S2 + Fa, 2, 3) and (S2 + Fa).subs(a, 2) > 0   # (ii-1) 2<=a<3
D3 = sp.expand(S3 + Fa)                                 # (ii-2) a>=3: S-|∫_0^a f| = F(a-2)
assert sp.expand(D3 - Fs) == 0
assert sp.factor(D3) == sp.factor(R(2, 3) * (a - 2)**2 * (7 - 2 * a))
assert sp.solve_univariate_inequality(D3 >= 0, a, relational=False).intersect(sp.Interval(3, sp.oo)) == sp.Interval(3, R(7, 2))
print('(나) 구간별: (1,3/2]·(3/2,2)·[2,3) 항상 성립, [3,∞)에서 S-|∫_0^a f| = F(a-2) = (2/3)(a-2)^2(7-2a) → a<=7/2 OK')

# 유리수 전수 (일반 계산과 교차 확인)
grid = sorted(set([1 + R(k, 80) for k in range(1, 561)] + [R(7, 2) - R(1, 1000), R(7, 2) + R(1, 1000), R(3), R(2), R(3, 2)]))
ok = [av for av in grid if cond_na(f0, av)]
assert ok == [av for av in grid if av <= R(7, 2)], [float(v) for v in ok[-3:]]
assert R(7, 2) in ok and R(7, 2) + R(1, 1000) not in ok
assert abs(I0(0, R(7, 2))) == A0(R(3, 2), R(7, 2)) == R(98, 3)   # 경계에서 등호
ans_val = max(ok)
def cval(c):
    m = re.fullmatch(r'\\dfrac(\d)(\d)', c)
    return Fr(int(m[1]), int(m[2])) if m else Fr(int(c))
ch = [cval(c) for c in P['choices']]
assert len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1
assert P['ans'] == 4 and ch[P['ans'] - 1] == Fr(7, 2) == Fr(ans_val.p, ans_val.q)
print(f'정답: (나)를 만족시키는 a = (1, 7/2] → a의 최댓값 7/2, 선지 ④ OK')

# ===== 원문 원리 줄 불통 =====
# x=1/2 대칭이동: [a-2,a] -> [1-a,3-a] ≠ [0,a]  (대칭으로 같아지지 않음)
assert sp.simplify((1 - a) - 0) != 0
assert cond_na(f0, R(3)) and I0(0, R(3)) < 0            # ∫_0^a f<0인데 (나) 성립 → 원문 결론 a<=3/2 불통
print('원문 원리 줄 불통: a=3에서 ∫_0^a f=', I0(0, R(3)), '<0 이어도 (나) 성립 OK')

# ===== 오답 근거 값 (착오 규칙으로 같은 전수) =====
W = {}
s1 = [av for av in grid if A0(0, av) <= A0(av - 2, av)]                     # |∫f|를 ∫|f|로 혼동
assert s1 == [av for av in grid if av <= 2]; W['①'] = max(s1)
Fw = 2 * x**2 - 4 * x**3                                                     # 1/3 누락 적분
s2 = [av for av in grid if av < 2 or Fw.subs(x, av - 2) >= 0]            # a>=2에서 F(a-2)>=0 판정을 틀린 F로
assert max(s2) == R(5, 2); W['②'] = max(s2)
s3 = [av for av in grid if av < 2 or all(f0.subs(x, t) >= 0 for t in [R(k, 50) * (av - 2) for k in range(51)])]   # 피적분함수 부호로 읽음
assert max(s3) == 3; W['③'] = max(s3)
s3b = [av for av in grid if av < 3 and cond_na(f0, av)]                       # a>=3 경우 누락 (상한 3)
assert max(s3b) < 3 and all(cond_na(f0, av) for av in grid if av < 3)
x0 = 2                                                                       # ∫_0^2 f = 0 이라는 착각(근 x=1 대칭)
assert I0(0, 2) != 0 and I0(0, R(3, 2)) == 0
W['⑤'] = x0 + 2
W = {k: Fr(int(sp.numer(v)), int(sp.denom(v))) for k, v in W.items()}
assert W == {'①': Fr(2), '②': Fr(5, 2), '③': Fr(3), '⑤': Fr(4)}, W
pos_ = dict(zip('①②③④⑤', ch))
for kk, v in W.items():
    assert pos_[kk] == v and v != Fr(7, 2) and kk in P['wrong']
print('오답 근거 값', {k: str(v) for k, v in W.items()}, 'OK')

# ===== 조건 빼 보기 =====
# (가) 빼기: f=-4x(x-r) (f(0)=0, |최고차항의 계수|=4)도 허용 → a의 상한이 3r/2+2로 커져 최댓값 없음
for r_, top in ((2, R(5)), (3, R(13, 2)), (5, R(19, 2))):
    fr = -4 * x * (x - r_)
    assert cond_na(fr, top) and not cond_na(fr, top + R(1, 100)), r_
print('ABLATION 17 (가): 필요(빼면 f(x)=-4x(x-2)일 때 a=5도 (나)를 만족시키고, f(x)=-4x(x-r) (r=2, 3, 5)에서 a=3r/2+2까지 가능해 r에 따라 커지므로 a의 최댓값이 없음)')
# (나) 빼기: (가)는 모든 a>1에서 성립 → a의 최댓값 없음
assert all(cond_ga(f0, av) for av in (R(4), R(10), R(100)))
print('ABLATION 17 (나): 필요(빼면 f(x)=-4x(x-1)에서 (가)가 모든 a>1에서 성립해 a의 최댓값이 없음)')

# ===== 길이: 원문 이상 (태그·공백 제거, 조건 포함) =====
plain = lambda t: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', t))
L_new = len(plain(P['body'] + COND(P['cond']))); L_org = len(plain(F.I['I37'][0]))
assert L_org == 265 and L_new >= L_org, (L_new, L_org)
print(f'길이: 변형 {L_new}자 >= 원문 {L_org}자 OK')
print('ALL OK')
