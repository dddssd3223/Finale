# -*- coding: utf-8 -*-
# A18 (5회 18번 후보, 원문 M27, db_ref 'M27 킬러 설계A', 재설계 1회) 검증
# 원문 풀이(f(3)=36) · 판정 원리(높이가 다른 두 봉우리: 교점 6·5·4·3·2) · (가)(나)를 만족시키는 (a, b) 전수(정확한 가지 풀이 + 격자)
# · 정의대로 센 교점의 x좌표 합 · 정답 = ④ · 선지 등차 · 오답(선지 안) · 조건 빼 보기 · 문장 길이 · 원문 골격 · 흔한 패턴 단어
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, a, c = sp.symbols('x a c', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M27' and it['ans'] == 4 and it['db_ref'] == 'M27 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert 'x^3-3ax^2+b' in it['body'] and [k for k, _ in it['cond']] == ['가', '나']
assert {'OP51', 'OP28'} & set(it['ops'])
full = it['body'] + COND(it['cond'])
assert 'f(t)' not in full and r'\(t\)' not in full          # 자기참조 높이·t 없음
CH = [sp.Integer(v) for v in it['choices']]
H1, H2, X0 = 4, 28, 2                                       # (가) 높이, (나) 높이, (나)의 근

def roots_abs(f_, L):
    """방정식 |f(x)|=L 의 서로 다른 실근 (L>0, 정확)"""
    return set(sp.real_roots(sp.Poly(f_ - L, x))) | set(sp.real_roots(sp.Poly(f_ + L, x)))
def fam(av, bv): return x**3 - 3*av*x**2 + bv
def ok(av, bv):
    f_ = fam(av, bv)
    Z = roots_abs(f_, H2)
    return len(roots_abs(f_, H1)) == 5 and len(Z) == 3 and any(sp.simplify(z - X0) == 0 for z in Z)
def exact_sum(rs):
    v = sp.N(sum(rs), 60); n = sp.Integer(round(float(v)))
    assert abs(v - n) < sp.Float('1e-40'); return n   # 근의 합(근과 계수의 관계 값)은 정수
def answer(av, bv):
    return exact_sum(roots_abs(fam(av, bv), H1))

# ---------- 원문 M27 ----------
good = [cv for cv in [R(k, 2) for k in range(-40, 21)]
        if len(roots_abs(2*x**3 + cv*x, -(2 + cv))) == 4 and -(2 + cv) > 0]
assert good == [-6], good
assert (2*x**3 - 6*x).subs(x, 3) == 36 and F.I['M27'][2] == '②' and F.I['M27'][1][1] == '36'
print('원문 M27: c=-6, f(3)=36 = ② OK')

# ---------- 판정 원리: 높이가 다른 두 봉우리 ----------
f0 = fam(-2, -4)
tab = {L: len(roots_abs(f0, L)) for L in [1, 3, 4, 5, 20, 27, 28, 29, 50]}
assert tab == {1: 6, 3: 6, 4: 5, 5: 4, 20: 4, 27: 4, 28: 3, 29: 2, 50: 2}, tab
assert sp.expand(fam(a, sp.Symbol('b')).subs(x, 0) - fam(a, sp.Symbol('b')).subs(x, 2*a) - 4*a**3) == 0
assert sp.factor(f0 - 28) == (x - 2)*(x + 4)**2 and sp.factor(f0 + 4) == x**2*(x + 6)
print('판정 원리: |f|와 y=L 교점 6·5·4·3·2 (봉우리 4, 28), 극값의 차 4a^3, x=2는 극댓점 -4와 같은 높이 OK')

# ---------- (가)(나)를 만족시키는 (a, b) 전수 ----------
# (가) 교점 5개 ⇔ 한 극값의 절댓값이 4 → b ∈ {4, -4, 4a^3+4, 4a^3-4} (f(0)=b, f(2a)=b-4a^3)
# (나) x=2가 |f(x)|=28의 근 ⇔ f(2)=8-12a+b=±28. 가지마다 a를 정확히 풀고 두 조건을 직접 센다.
sols = set()
for bb in (sp.Integer(4), sp.Integer(-4), 4*a**3 + 4, 4*a**3 - 4):
    for s in (28, -28):
        e = sp.expand(8 - 12*a + bb - s)
        for r in sp.Poly(e, a).real_roots():
            if r == 0: continue
            bv = bb.subs(a, r)
            if r.is_Rational:
                if ok(r, bv): sols.add((r, bv))
            else:   # 무리수 a: 극값 두 개로 판정(교점 표) — 두 조건을 동시에 만족시키지 못함을 수치로 확인
                p1, p2 = float(bv), float(bv - 4*r**3)
                mx, mn = max(p1, p2), min(p1, p2)
                both = mx > 0 > mn and abs(mx + mn) > 1e-9 and abs(min(mx, -mn) - H1) < 1e-9 and abs(max(mx, -mn) - H2) < 1e-9
                assert not both, (r, bv)
assert sols == {(-2, -4)}, sols
# 격자 확인: a를 1/12 간격으로 두고 (가)를 만족시키는 b 후보 전부에서 두 조건을 센다
grid = set()
for j in range(-72, 73):
    av = R(j, 12)
    if av == 0: continue
    for bv in {4, -4, 4*av**3 + 4, 4*av**3 - 4}:
        if ok(av, bv): grid.add((av, bv))
assert grid == {(-2, -4)}, grid
print('(가)(나): a=-2, b=-4 하나뿐 (정확한 가지 풀이 + a 격자 전수) OK')

# ---------- 정답 ----------
pts = sorted(roots_abs(f0, H1), key=lambda v: float(v))
assert len(pts) == 5 and 0 in pts and -6 in pts
ans = answer(-2, -4)
assert sp.simplify(ans) == -12 and CH[it['ans'] - 1] == -12
print(f'정답: 교점 x좌표 {[round(float(v), 4) for v in pts]}, 합 -12 = ④ OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] < CH[0]
w1 = exact_sum(sp.real_roots(sp.Poly(f0 - 4, x)))                     # 접점 쪽(f=-4) 누락
w2 = sp.simplify(answer(-2, -28))                               # 큰 봉우리를 극솟값 쪽으로
assert sp.simplify(w1) == -6 and w2 == -8
# a=-2, b=-28 은 (나)의 x=2가 맞지 않음(오답 근거 확인)
assert not ok(-2, -28) and fam(-2, -28).subs(x, 2) == 4
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != -12
assert set(map(int, it['wrongs'])) == {-6, -8}
print('선지 등차(공차 -2, 내림차순), 오답 -6(접점 누락)·-8(큰 봉우리 반대쪽) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
# (가) 없음: (나)만 → x=2가 |f(x)|=28의 근이고 실근이 3개인 (a, b)가 여럿 → 직선 y=4와의 교점(개수·합)이 정해지지 않음
alt = {}
for j in range(-48, 49):
    av = R(j, 8)
    if av == 0: continue
    for bv in (28 - 8 + 12*av, -28 - 8 + 12*av):
        f_ = fam(av, bv)
        if len(roots_abs(f_, H2)) == 3: alt[(av, bv)] = (len(roots_abs(f_, H1)), round(float(sp.N(sum(roots_abs(f_, H1)), 30)), 4))
assert len(alt) >= 3 and len(set(alt.values())) >= 2
ex = list(alt.items())[:3]
print(f'ABLATION 18 (가): 필요(정해지지 않음: (나)만이면 (a, b)={[str(k) for k, _ in ex]} 등 {len(alt)}개, 직선 y=4와 교점 (개수, 합)={[v for _, v in ex]})')
# (나) 없음: (가)만 → a 자유
alt4 = {}
for av, bv in ((2, 4), (3, 4), (-3, -4), (R(5, 2), 4)):
    assert len(roots_abs(fam(av, bv), H1)) == 5
    alt4[(av, bv)] = answer(av, bv)
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)만이면 (a, b)=(2,4),(3,4),(-3,-4),(5/2,4) 등 무수히 많고 합이 {[str(v) for v in alt4.values()]})')
assert len(set(alt4.values())) >= 2
# (나)의 '실근 2' 없음: 네 경우가 모두 맞아 답이 넷
four = {(av, bv): sp.simplify(answer(av, bv)) for av, bv in ((2, 28), (2, 4), (-2, -4), (-2, -28))}
for (av, bv) in four:
    f_ = fam(av, bv); assert len(roots_abs(f_, H1)) == 5 and len(roots_abs(f_, H2)) == 3
assert sorted(four.values()) == [-12, -8, 8, 12]
print(f'ABLATION 18 실근 2: 필요(정해지지 않음: 빼면 (a, b)=(2,28),(2,4),(-2,-4),(-2,-28) 모두 맞아 합이 {sorted(four.values())})')
# (나)의 개수 3 → 4: 28이 두 봉우리 사이 높이 → 극값의 차 조건이 사라져 a 미정
print('ABLATION 18 실근의 개수 3: 필요(정해지지 않음: 4로 바꾸면 28이 두 봉우리 사이 높이일 뿐이라 극값의 차 4|a|^3=32가 나오지 않음)')
f_alt = fam(-3, -4)
assert len(roots_abs(f_alt, 28)) == 4 and len(roots_abs(f_alt, 4)) == 5
# (가)의 다섯 → 여섯: 4가 작은 봉우리보다 낮을 뿐 → a 미정
print('ABLATION 18 다섯 점: 필요(정해지지 않음: 여섯으로 바꾸면 작은 봉우리 높이가 4보다 크기만 하면 됨)')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M27'][0])); Lm = len(plain(full))
assert Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(full))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M27'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하, 관문 0.60 미만)')
assert jd < 0.60
assert '\\[' not in it['body'] and '(단,' not in it['body']
print('ALL OK')
