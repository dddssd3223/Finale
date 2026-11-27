# -*- coding: utf-8 -*-
# A18 2판 (13회 18번 후보, 원문 I42, db_ref 'I42 킬러 설계A') 검증
# 원문 풀이 · g의 개형(증감·두 극값의 차) · 수평선과의 교점 수 표 · 아래끝 a 전수(음수 1/8 간격 + 후보)로 세 실근이 되는 k의 집합과 합
# · 갈래별 식 · a의 유일성 · 정의대로 직접 세기 · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문·N제 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, a, t = sp.symbols('x a t', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'I42' and it['ans'] == 4 and it['db_ref'] == 'I42 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it and 'bogi' not in it
full = it['body']
for s_ in (r"3x^2+3 & (x\le1)", r"-2x+8 & (x&gt;1)", r"음수 \(a\)", r"\int_a^x tf(t)\,dt", r"\(|g(x)|=k\)",
           r'서로 다른 실근의 개수가 \(3\)이 되도록 하는', r"모든 실수 \(k\)의 값의 합이 \(18\)", r"모든 \(a\)의 값의 합은?"):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값', '<img', '가능한 모든'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for kk in ('setting', 'principle', 'new'):
    assert not re.search(r'\\\([^)]*?[<>]', it['core'][kk]), kk
head = open(os.path.join(HERE, 'p6.py')).read().split('ITEMS = {')[0]
for bad in ('a=-2', 'a=-1', r'\(-3\)', '=-3', r'\frac94', '9/4', r'\frac{81}{4}', '81/4'):
    assert bad not in it['core']['new'] and bad not in head, bad
CH = [sp.Integer(v) for v in it['choices']]

# ---------- 원문 I42 ----------
fo1, fo2 = t**2 + 1, 2*t
go1 = sp.integrate(t*fo1, (t, -1, x)); go2 = go1.subs(x, 1) + sp.integrate(t*fo2, (t, 1, x))
assert go1.subs(x, 1) == 0
assert sp.solve(sp.diff(go1, x), x) == [0] and go1.subs(x, 0) == R(-3, 4)
assert all(sp.diff(go2, x).subs(x, v) > 0 for v in (R(3, 2), 2, 10))
for n in range(1, 8):
    c1 = [r for r in sp.real_roots(sp.Poly(go1 - n, x)) if r <= 1]; c2 = [r for r in sp.real_roots(sp.Poly(sp.expand(go2 - n), x)) if r > 1]
    assert len(set(c1)) + len(set(c2)) == 2
assert F.I['I42'][2] == '③' and F.I['I42'][1][2] == 'T:ㄱ, ㄷ'
print('원문 I42: ㄱ 참(g(1)=0), ㄴ 거짓(극소뿐, -3/4), ㄷ 참 → ③ OK')

# ---------- 변형: f=3x^2+3 (x<=1), -2x+8 (x>1), g=∫_a^x t f ----------
f1, f2 = 3*t**2 + 3, -2*t + 8
assert f1.subs(t, 1) == f2.subs(t, 1) == 6
assert sp.solve(f2, t) == [4] and all(f1.subs(t, v) > 0 for v in (-5, -1, 0, 1))
G1 = sp.integrate(t*f1, (t, 0, x)); G2 = sp.expand(G1.subs(x, 1) + sp.integrate(t*f2, (t, 1, x)))   # G(x)=∫_0^x t f
assert sp.expand(G1 - (R(3, 4)*x**4 + R(3, 2)*x**2)) == 0
Gf = lambda v: (G1 if v <= 1 else G2).subs(x, v)
gp = lambda v: v*(f1 if v <= 1 else f2).subs(t, v)
assert all(gp(v) < 0 for v in (-3, -1, R(-1, 9))) and all(gp(v) > 0 for v in (R(1, 9), 1, 2, R(39, 10))) and gp(4) == 0 and all(gp(v) < 0 for v in (R(41, 10), 5, 50))
T = Gf(4) - Gf(0); assert T == R(81, 4) and Gf(1) == R(9, 4) and Gf(4) - Gf(1) == 18
print('g: x<0 감소, 0<x<4 증가, x>4 감소 → x=0 극소, x=4 극대, g(4)-g(0)=81/4 (=9/4+18) OK')

def cross(L):
    """곡선 y=G(x)와 직선 y=L의 교점 수(정확한 실근으로)"""
    s = set()
    for r in sp.real_roots(sp.Poly(G1 - L, x)):
        if r <= 1: s.add(sp.nsimplify(r))
    for r in sp.real_roots(sp.Poly(G2 - L, x)):
        if r > 1: s.add(sp.nsimplify(r))
    return len(s)
def table(p, m):
    return 1 if p > m + T else 2 if p == m + T else 3 if p > m else 2 if p == m else 1
for L in (R(-7), R(-1, 3), 0, R(1, 5), 1, R(9, 4), 18, 20, R(81, 4), 21, 90):
    assert cross(L) == table(L, 0), L
def nabs(c, kv):
    """|g(x)|=kv 의 서로 다른 실근 수, g=G-c"""
    return cross(c + kv) + (cross(c - kv) if kv != 0 else 0)
def Kset(c):
    """세 실근이 되는 실수 k(>=0)의 집합. 개수는 경계 k∈{0,|c|,|T-c|} 사이 열린 구간에서 일정"""
    th = sorted({sp.Integer(0), abs(c), abs(T - c)})
    pts = list(th) + [(th[i] + th[i + 1])/2 for i in range(len(th) - 1)] + [th[-1] + 1]
    res = [p for p in pts if nabs(c, p) == 3]
    assert all(p in th for p in res), (c, res)
    return res
def Ksum_formula(c):                                                   # c=G(a)>0 (a<0) 일 때 갈래별 식
    assert c > 0
    if c < T: return 0 if 2*c == T else max(c, T - c)                   # m<0<M: k=0과 높은 봉우리
    if c == T: return T                                                # M=0
    return 2*c - T                                                     # M<0
ok = []
grid = sorted(set([R(-i, 8) for i in range(1, 33)]))                    # a=-1/8,…,-4
for av in grid:
    c = Gf(av); Ks = Kset(c); s = sum(Ks)
    assert s == Ksum_formula(c), (av, Ks)
    if s == 18: ok.append(av)
assert ok == [-2, -1], ok
# 기호로: 가운데 갈래 max(c, T-c)=18 → c=18 또는 c=9/4, 셋째 갈래 2c-T=18 → c=153/8 < T (모순), 경계 c=T → 합 81/4
cs = sp.symbols('c', positive=True)
assert sp.solve(sp.Eq(2*cs - T, 18), cs) == [R(153, 8)] and R(153, 8) < T and T != 18
assert 18 < T and T - 18 == R(9, 4) and max(18, T - 18) == 18 and max(R(9, 4), T - R(9, 4)) == 18
# a<0에서 G1은 감소(일대일)이므로 c마다 음수 a는 하나
assert all(sp.diff(G1, x).subs(x, v) < 0 for v in (R(-1, 9), -1, -2, -10))
sol18 = [r for r in sp.real_roots(sp.Poly(G1 - 18, x)) if r < 0]; sol94 = [r for r in sp.real_roots(sp.Poly(G1 - R(9, 4), x)) if r < 0]
assert sol18 == [-2] and sol94 == [-1]
assert sp.factor(4*(G1 - 18)/3) == (x - 2)*(x + 2)*(x**2 + 6) and sp.factor(4*(G1 - R(9, 4))/3) == (x - 1)*(x + 1)*(x**2 + 3)
ans = sum(sol18 + sol94)
# 정의대로 직접 확인
for av, ks in ((-2, [0, 18]), (-1, [0, 18])):
    c = Gf(av); assert Kset(c) == ks and [nabs(c, kv) for kv in (0, 1, R(9, 4), 10, 18, 19)] == [3, 6, 5, 4, 3, 2]
assert Gf(-2) == 18 and Gf(-1) == R(9, 4)
assert ans == CH[it['ans'] - 1] == -3
print(f'세 실근이 되는 k의 합 = 18 ⇔ a ∈ {ok} (음수 a 전수 1/8 간격 + 기호 풀이) → 합 {ans}, 정답 ④ OK')

# ---------- 선지 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] > CH[0]
assert all(w in it['choices'] for w in it['wrongs']) and it['choices'][it['ans'] - 1] not in it['wrongs'] and len(it['wrongs']) >= 2
for w in it['wrongs']: assert rf"\({w}\):" in it['wrong'], w
body_nums = set(re.findall(r'-?\d+', html.unescape(re.sub(r'<[^>]+>', '', full))))
assert str(ans) not in body_nums, body_nums                            # 정답 -3은 본문 수(3, -2, 8, 18, 1)와 다름
# 오답 경로 재현
assert sol18 == [-2] and CH[4] == -2                                    # -2: 극솟값 쪽 높이만
Tw = Gf(4) - Gf(1); assert Tw == 18 and [r for r in sp.real_roots(sp.Poly(G1 - (Tw - 18), x)) if r < 0] == []   # 구간 [0,1] 누락: M=18 → m=0 → 음수 a 없음
assert -1 + (-4) == CH[1] and -4 == CH[2]                               # -5, -4: a^2=4 를 a=-4 로
print('선지 등차·오름차순, 오답 -2·-5·-4 경로 재현 OK')

# ---------- 조건 빼 보기 ----------
allA = lambda c: sorted(set([sp.nsimplify(r) for r in sp.real_roots(sp.Poly(G1 - c, x)) if r <= 1] + [sp.nsimplify(r) for r in sp.real_roots(sp.Poly(G2 - c, x)) if r > 1]))
A18_, A94 = allA(sp.Integer(18)), allA(R(9, 4))
assert len(A18_) == 3 and len(A94) == 3 and 1 in A94 and not all(r.is_rational for r in A18_ + A94)
print(f"ABLATION 18 음수 a: 필요(빼면 a가 {len(A18_) + len(A94)}개: a=1과 x>1 쪽의 무리수 해가 더 생겨 합이 달라짐)")
assert all(table(R(-18) + R(j, 2), R(-18)) == 3 for j in range(1, 40))
print("ABLATION 18 절댓값: 필요(빼면 세 실근이 되는 k가 구간 m<k<M 전체라 합이 정해지지 않음)")
alt = [av for av in grid if sum(Kset(Gf(av))) == 20]; alt_c = [cv for cv in (sp.Integer(20), T - 20) if cv > 0]
assert alt == [] and all(not all(r.is_rational for r in sp.real_roots(sp.Poly(G1 - cv, x))) for cv in alt_c)
print("ABLATION 18 합 18: 필요(20으로 바꾸면 a가 무리수 둘로 바뀜)")
five = [av for av in grid if (lambda c: [p for p in (abs(c), abs(T - c)) if p > 0 and nabs(c, p) == 5])(Gf(av)) == [18]]
assert five == []
print("ABLATION 18 '세 실근': 필요(다섯 실근으로 바꾸면 그런 k는 81/8보다 작아 18이 될 수 없음)")
H2 = sp.expand(G1.subs(x, 1) + sp.integrate(t*6*t, (t, 1, x)))          # x>1 조각을 부호가 일정한 6x로
def cross0(L):
    return len(set(r for r in sp.real_roots(sp.Poly(G1 - L, x)) if r <= 1) | set(r for r in sp.real_roots(sp.Poly(H2 - L, x)) if r > 1))
only = [av for av in grid if [p for p in (sp.Integer(0), Gf(av), Gf(av)/2, Gf(av) + 1) if cross0(Gf(av) + p) + (cross0(Gf(av) - p) if p != 0 else 0) == 3] == [18]]
assert only == [-2]
print("ABLATION 18 x>1 조각 -2x+8: 필요(부호가 일정한 조각이면 극대가 없어 세 실근 k는 |g(0)| 하나, a=-2뿐이라 합이 -2)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
assert f2.subs(t, 5) < 0 and cross(R(1)) == 3
for av in (-2, -1):
    gm = -Gf(av); assert gm != R(-3, 4)
assert Gf(1) - Gf(-2) != 0                                             # a=-2에서 g(1)≠0
print('원문 설정 줄(f>0, 극소 하나, 높이가 수로 정해짐): f(5)<0, 극대 생김, 극값이 a에 따라 움직임 → 불통 OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['I42'][0])); Lm = len(plain(full))
print(f'문장 길이: 원문 {Lo}자(보기 포함), 변형 {Lm}자')
assert Lm >= 0.9 * Lo, (Lo, Lm)

# ---------- 원문 · 인쇄 N제 골격 ----------
import dupcheck as DC
sk = lambda s_: set(DC.shingles(DC.skel(DC.norm(s_))))
A_ = sk(full); B2 = sk(F.I['I42'][0])
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
md = open('/home/user/Finale/output/N제/미적분1_기말_N제_06_부정적분과정적분.md').read()
sec = md.split('## I42 (부교재', 1)[1].split('\n## ', 1)[0]
nje = re.findall(r'\*\*(2\d\d)\.\*\*(.*?)(?=\n\n\*\*|\Z)', sec, re.S)
assert [n for n, _ in nje] == ['287', '288', '289', '290', '291', '292'], [n for n, _ in nje]
for n, body in nje:
    C_ = sk(body); j2 = len(A_ & C_) / len(A_ | C_)
    assert j2 < 0.60
    assert '|g(x)|' not in body and r'\int_a^x' not in body and '-2x+8' not in body
print('인쇄 N제 I42(287–292): 골격 0.60 미만, 절댓값·문자 아래끝·부호가 바뀌는 조각 없음 OK')
print('ALL OK')
