# -*- coding: utf-8 -*-
# p18.py (2회 18번 Claude 후보, 원본 D45) 검증
# 원문 풀이(102) · 설정 줄 불통 · (가)(나) 해석의 기호·격자 전수 조사(유일성) · 정답 = ② · 선지 등차 · 오답 값 · 조건 빼 보기 · 문장 길이 · 골격
import os, re, sys, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
from items_common import COND
import items_final as F
x, t, a = sp.symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claude18' and it['key'] == 'D45' and it['ans'] == 2
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나']
assert it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
CH = [sp.nsimplify(v) for v in it['choices']]

# ---------- 원문 D45 ----------
b2, b1, b0 = sp.symbols('b2 b1 b0')
fo = x**3 + b2*x**2 + b1*x + b0
# (가) 극한 존재 ⇔ f(-2)=2, f'(-2)=0 ; (나) (3,5)에서 f>=f(4) ⇒ f'(4)=0
so = sp.solve([fo.subs(x, -2) - 2, sp.diff(fo, x).subs(x, -2), sp.diff(fo, x).subs(x, 4)], [b2, b1, b0], dict=True)
assert len(so) == 1
fo = fo.subs(so[0])
assert sp.expand(fo - (x**3 - 3*x**2 - 24*x - 26)) == 0
assert sp.limit((fo - 2) / (x + 2)**2, x, -2).is_finite
assert all(fo.subs(x, R(v, 10)) >= fo.subs(x, 4) for v in range(31, 50))      # x=4 극소
assert fo.subs(x, 8) == 102 and F.I['D45'][2] == '102'
print('원문 D45: f=x^3-3x^2-24x-26, f(8)=102 OK')

# ---------- 원리: lim (f(x)-f(a))/(x-a)^2 존재 ⇔ f'(a)=0 (다항함수) ----------
c = sp.symbols('c0:5')
g = sum(c[k] * x**k for k in range(5))
ratio = sp.cancel((g - g.subs(x, a)) / (x - a))           # = f'(a) + (x-a)·(...)
assert sp.expand(ratio.subs(x, a) - sp.diff(g, x).subs(x, a)) == 0
# f'(a)≠0 이면 (f(x)-f(a))/(x-a)^2 = ratio/(x-a) → 좌우 ±∞ ; f'(a)=0 이면 다항식
print("원리: 극한 존재 ⇔ f'(a)=0 (분자 (f(x)-f(a))/(x-a) → f'(a))")

# ---------- 설정 줄 불통 ----------
# 원문 설정 줄: '두 극점이 정해지면 f'가 정해진다'. 사차에서는 f'(1)=f'(4)=0, f(0)=0, 최고차항 1이어도 f'=4(x-1)(x-4)(x-s)로 s가 남는다.
s = sp.symbols('s')
fam = sp.integrate(4*(t - 1)*(t - 4)*(t - s), (t, 0, x))
vals = {sv: sp.expand(fam.subs(s, sv)).subs(x, 5) for sv in (1, 4, 0, 2)}
assert len(set(vals.values())) == 4
# 두 근 1, 4가 모두 극한 존재 점이어도 어느 쪽이 중근인지 두 가지가 남는다
print('설정 줄 불통: 두 근 1, 4와 f(0)=0으로는 f가 정해지지 않음, f(5) =', vals)

# ---------- 모형: f(0)=0, 최고차항 1인 사차함수 ↔ f'(x)=4x^3+3B x^2+2C x+D ----------
def fP(roots_poly):
    """f' (최고차항 4)로부터 f(0)=0인 f"""
    return sp.expand(sp.integrate(roots_poly.subs(x, t), (t, 0, x)))

def crit_set(f):
    return sorted(set(sp.real_roots(sp.Poly(sp.diff(f, x), x))))

def ok_ga(f, need=('개수', '합')):
    S = crit_set(f)
    r = True
    if '개수' in need: r &= (len(S) == 2)
    if '합' in need: r &= (sum(S) == 5)
    return bool(r)

def ok_na(f):
    """열린구간 (2,6)에서 최솟값이 f(4): f-f(4) >= 0 on (2,6) (실근·부호로 정확히 판정)"""
    h = sp.Poly(sp.expand(f - f.subs(x, 4)), x)
    rr = sorted(set(r for r in sp.real_roots(h) if 2 < r < 6))
    pts = [2] + rr + [6]
    for p_, q_ in zip(pts, pts[1:]):
        m = (p_ + q_) / 2
        if sp.N(h.eval(m), 30) < 0: return False
    return True

def ok(f, need=('개수', '합', '나')):
    r = True
    if '개수' in need or '합' in need: r &= ok_ga(f, tuple(k for k in need if k in ('개수', '합')))
    if '나' in need: r &= ok_na(f)
    return bool(r)

# ---------- 기호: (가)의 개수 2 ⇔ f'=4(x-p)^2(x-q), p≠q ----------
# 삼차 f'의 실근 구조: 서로 다른 세 실근(3개) / 이중근+단순근(2개) / 삼중근(1개) / 실근 하나+허근 둘(1개)
for fp, n in ((4*(x+1)*(x-1)*(x-3), 3), (4*(x-1)**2*(x-4), 2), (4*(x-2)**3, 1), (4*(x-1)*(x**2+1), 1)):
    assert len(crit_set(fP(fp))) == n
# (나): x=4가 열린구간 안의 최솟값 → f'(4)=0, x=4에서 극소. f'=4(x-p)^2(x-q)에서
p, q = sp.symbols('p q', real=True)
# p=4(중근)이면 f'=4(x-4)^2(x-q): x=4 좌우에서 f' 부호 같음 → 극소 아님
fpp = 4*(x - 4)**2*(x - q)
e = sp.symbols('e', positive=True)
assert sp.factor(fpp.subs(x, 4 - e) * fpp.subs(x, 4 + e)) == sp.factor(16*e**4*(4 - e - q)*(4 + e - q))   # q≠4이면 작은 e에서 양수: 부호 안 바뀜
for qv in (1, -3, 7, R(5, 2)):
    f_ = fP(4*(x - 4)**2*(x - qv))
    assert not ok_na(f_)
# q=4(단순근)이면 f'=4(x-p)^2(x-4): x<4 감소, x>4 증가 → (나) 성립 (p 무관)
for pv in (-3, 0, 1, 3, 5, 9):
    assert ok_na(fP(4*(x - pv)**2*(x - 4)))
# 합 5 → p=1
assert sp.solve(sp.Eq(p + 4, 5), p) == [1]
fA = fP(4*(x - 1)**2*(x - 4))
assert sp.expand(fA - (x**4 - 8*x**3 + 18*x**2 - 16*x)) == 0
assert sp.expand(fA - ((x - 1)**3*(x - 5) - 5)) == 0
assert ok(fA) and crit_set(fA) == [1, 4]
# 극한값 직접 확인: a=1(0), a=4(존재), 다른 점(없음)
assert sp.limit((fA - fA.subs(x, 1)) / (x - 1)**2, x, 1) == 0
assert sp.limit((fA - fA.subs(x, 4)) / (x - 4)**2, x, 4) == 18
assert sp.limit((fA - fA.subs(x, 2)) / (x - 2)**2, x, 2, '+') == -sp.oo and sp.limit((fA - fA.subs(x, 2)) / (x - 2)**2, x, 2, '-') == sp.oo   # f'(2)=-8≠0
ans = fA.subs(x, 5)
assert ans == -5 and CH[it['ans'] - 1] == ans
print(f'유일한 f(x) = {fA} = (x-1)^3(x-5)-5, f(5) = {ans} = ②')

# ---------- 격자 전수 조사: f'의 근 구조 전부 ----------
G = [R(k, 2) for k in range(-6, 17)]          # -3 ~ 8, 0.5 간격
sols = set(); cnt = 0
for r1, r2, r3 in itertools.combinations_with_replacement(G, 3):
    f_ = fP(4*(x - r1)*(x - r2)*(x - r3)); cnt += 1
    if ok(f_): sols.add((r1, r2, r3))
for r1 in G:                                   # 실근 하나 + 허근 둘 (개수 1이라 (가) 불만족 확인)
    for al in (0, 2, 4):
        for be in (1, 2):
            f_ = fP(4*(x - r1)*((x - al)**2 + be**2)); cnt += 1
            assert not ok_ga(f_)
assert sols == {(1, 1, 4)}, sols
print(f'격자 {cnt}개 f\' 중 (가)(나)를 모두 만족시키는 것은 f\'=4(x-1)^2(x-4) 하나')

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {5}
print('선지', [str(v) for v in CH], '공차 5 (오름차순), 정답 ②')

# ---------- 오답 (선지 안) ----------
W1 = fP(4*(x - 1)*(x - 4)**2)                 # x=4를 f'의 중근으로 (나의 부호 판단 생략)
W2 = sp.expand((x - 1)**2*(x - 4)**2 - 16)    # 원문식: 두 점마다 제곱 인수, 높이 같다고 둠
assert W2.subs(x, 0) == 0
assert ok(W1, ('개수', '합')) and not ok_na(W1) and sp.diff(W1, x).subs(x, 4) == 0       # (가) 만족, (나)만 위반
assert ok_na(W2) and crit_set(W2) == [1, R(5, 2), 4] and not ok_ga(W2, ('개수',))          # (나) 만족, (가) 개수 3
w1, w2 = W1.subs(x, 5), W2.subs(x, 5)
assert (w1, w2) == (5, 0)
assert [str(w) for w in (w2, w1)] == it['wrongs'] and all(sp.nsimplify(w) in CH for w in it['wrongs'])
for s_ in ('5', '0', 'x^4-12x^3+48x^2-64x', '(x-1)^2(x-4)^2-16'):
    assert s_ in it['wrong'], s_
print('오답 (선지 안): 5 (x=4를 중근으로 — (나) 위반), 0 (제곱 인수 두 개 — (가) 개수 3)')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# (가) 개수 빼기: 합 5, (나)만 → 서로 다른 세 근 (예: -1, 2, 4) 등도 가능
alt = fP(4*(x + 1)*(x - 2)*(x - 4))
assert ok(alt, ('합', '나')) and not ok(alt)
print(f"ABLATION 18 (가) 개수 2: 필요(정해지지 않음: 합·(나)만이면 f'=4(x+1)(x-2)(x-4)도 만족, f(5)={alt.subs(x, 5)})")
# (가) 합 빼기: 개수 2, (나)만 → f'=4(x-p)^2(x-4) (p≠4 모두)
altv = {pv: fP(4*(x - pv)**2*(x - 4)).subs(x, 5) for pv in (0, 2, 3)}
assert all(ok(fP(4*(x - pv)**2*(x - 4)), ('개수', '나')) for pv in altv) and len(set(altv.values()) | {ans}) == 4
print(f'ABLATION 18 (가) 합 5: 필요(정해지지 않음: p=0→{altv[0]}, p=2→{altv[2]}, p=3→{altv[3]})')
# (나) 빼기: (가)만 → f'=4(x-p)^2(x-q), p+q=5 (예: 중근 4·단순근 1, 중근 2·단순근 3)
alt2 = fP(4*(x - 2)**2*(x - 3))
assert ok(W1, ('개수', '합')) and ok(alt2, ('개수', '합')) and not ok_na(alt2)
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)만이면 {w1}(x=4 중근), {alt2.subs(x, 5)}(p=2, q=3) 등)')
# f(0)=0 빼기: 상수항 자유 → f(5) 정해지지 않음
assert ok(fA + 3) and (fA + 3).subs(x, 5) != ans
print(f'ABLATION 18 f(0)=0: 필요(정해지지 않음: f+3도 (가)(나) 만족, f(5)={(fA + 3).subs(x, 5)})')
# 어느 조건을 빼도 그 조건만 어긴 자연스러운 오답이 선지 안에 있다: (나)의 부호 판단 → 5, (가)의 개수 → 0
print('조건 하나만 어긴 값: (나) 부호 판단 생략 → 5(④), (가) 개수 확인 생략 → 0(③) — 선지만으로 조건을 건너뛸 수 없음')

# ---------- 문장 길이 (태그·공백 제거, 조건 포함) ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['D45'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 184 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개, 원문 2개)')

# ---------- 원문과의 골격 (dupcheck 방식 6글자 조각 Jaccard) ----------
import dupcheck as DC
A = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond']))))); B = set(DC.shingles(DC.skel(DC.norm(F.I['D45'][0]))))
jd = len(A & B) / len(A | B)
assert jd <= 0.25, jd
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하)')
# 줄 바꾼 식 없음 (원문도 없음)
assert '\\[' not in it['body'] + COND(it['cond'])
print('ALL OK')
