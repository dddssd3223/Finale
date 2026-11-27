# -*- coding: utf-8 -*-
# A18 (13회 18번 후보, 원문 I42, db_ref 'I42 킬러 설계A') 검증
# 원문 풀이 · g의 개형(증감·두 극값의 차) · 수평선과의 교점 수 표 · 극솟값 m 전수(1/4 간격)로 세 실근이 되는 k의 집합과 합
# · 갈래별 식 · 양수 a로 후보 거르기 · a의 유일성 · 정의대로 직접 세기 · 선지 등차 · 오답 경로 재현 · 조건 빼 보기
# · 원문 설정 줄 시험 · 문장 길이 · 원문·N제 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, a, t, k = sp.symbols('x a t k', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'I42' and it['ans'] == 4 and it['db_ref'] == 'I42 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it and 'bogi' not in it                           # 상자 없음, 보기형 아님(회차 1개 이하)
full = it['body']
for s_ in (r"2x^2+1 & (x\le1)", r"-3x+6 & (x&gt;1)", r"양수 \(a\)", r"\int_a^x tf(t)\,dt", r"\(|g(x)|=k\)",
           r'서로 다른 실근의 개수가 \(3\)이 되도록 하는', r"모든 실수 \(k\)의 값의 합이 \(5\)", r"\(g(2)\)의 값은?"):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값', '<img', '가능한 모든'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for kk in ('setting', 'principle', 'new'):
    assert not re.search(r'\\\([^)]*?[<>]', it['core'][kk]), kk
# core·머리 주석에 정답·풀이 요지가 없는지
head = open(os.path.join(HERE, 'p6.py')).read().split('ITEMS = {')[0]
for bad in ('m=1', 'a=3', '2m+3', 'm+3', r'\(4\)', '=4', '차 3', r'차 \(3\)'):
    assert bad not in it['core']['new'] and bad not in head, bad
CH = [sp.Integer(v) for v in it['choices']]

# ---------- 원문 I42 ----------
fo1, fo2 = t**2 + 1, 2*t
go1 = sp.integrate(t*fo1, (t, -1, x))                                  # x<=1
go2 = go1.subs(x, 1) + sp.integrate(t*fo2, (t, 1, x))                  # x>1
assert go1.subs(x, 1) == 0                                             # ㄱ 참
assert sp.solve(sp.diff(go1, x), x) == [0] and go1.subs(x, 0) == R(-3, 4)   # 극소 하나, 극대 없음 → ㄴ 거짓
assert all(sp.diff(go2, x).subs(x, v) > 0 for v in (R(3, 2), 2, 10))
for n in range(1, 8):                                                  # ㄷ 참
    c1 = [r for r in sp.real_roots(sp.Poly(go1 - n, x)) if r <= 1]; c2 = [r for r in sp.real_roots(sp.Poly(sp.expand(go2 - n), x)) if r > 1]
    assert len(set(c1)) + len(set(c2)) == 2
assert F.I['I42'][2] == '③' and F.I['I42'][1][2] == 'T:ㄱ, ㄷ'
print('원문 I42: ㄱ 참(g(1)=0), ㄴ 거짓(극소뿐, -3/4), ㄷ 참 → ③ OK')

# ---------- 변형: f=2x^2+1 (x<=1), -3x+6 (x>1), g=∫_a^x t f ----------
f1, f2 = 2*t**2 + 1, -3*t + 6
assert f1.subs(t, 1) == f2.subs(t, 1) == 3                              # x=1에서 이어짐(원문 관계 보존)
assert sp.solve(f2, t) == [2] and all(f1.subs(t, v) > 0 for v in (-5, -1, 0, 1))
G1 = sp.integrate(t*f1, (t, 0, x)); G2 = sp.expand(G1.subs(x, 1) + sp.integrate(t*f2, (t, 1, x)))   # G(x)=∫_0^x t f
assert sp.expand(G1 - (x**4/2 + x**2/2)) == 0 and sp.expand(G2 - (-x**3 + 3*x**2 - 1)) == 0
Gf = lambda v: (G1 if v <= 1 else G2).subs(x, v)
gp = lambda v: v*(f1 if v <= 1 else f2).subs(t, v)                      # g'(x)=x f(x)
assert all(gp(v) < 0 for v in (-3, -1, R(-1, 9))) and all(gp(v) > 0 for v in (R(1, 9), 1, R(3, 2), R(19, 10))) and gp(2) == 0 and all(gp(v) < 0 for v in (R(21, 10), 3, 50))
D = Gf(2) - Gf(0); assert D == 3                                       # 두 극값의 차(아래끝과 무관)
print('g: x<0 감소, 0<x<2 증가, x>2 감소 → x=0 극소, x=2 극대, g(2)-g(0)=3 OK')

def cross(L):
    """곡선 y=G(x)와 직선 y=L의 교점 수(정확한 실근으로)"""
    s = set()
    for r in sp.real_roots(sp.Poly(G1 - L, x)):
        if r <= 1: s.add(sp.nsimplify(r))
    for r in sp.real_roots(sp.Poly(G2 - L, x)):
        if r > 1: s.add(sp.nsimplify(r))
    return len(s)
def table(p, m):                                                       # g의 극솟값 m일 때 y=p와의 교점 수(풀이의 표)
    return 1 if p > m + 3 else 2 if p == m + 3 else 3 if p > m else 2 if p == m else 1
for L in (R(-7), R(-1, 3), 0, R(1, 5), 1, 2, R(29, 10), 3, R(31, 10), 9):
    assert cross(L) == table(L, 0), L                                  # m=0(곧 g=G)에서 표 확인
def nabs(m, kv):
    """|g(x)|=kv 의 서로 다른 실근 수, g=G+m"""
    return cross(kv - m) + (cross(-kv - m) if kv != 0 else 0)
def Kset(m):
    """세 실근이 되는 실수 k(>=0)의 집합. 개수는 경계 k∈{0,|m|,|m+3|} 사이 열린 구간에서 일정하므로 경계와 구간 표본을 모두 본다"""
    th = sorted({sp.Integer(0), abs(m), abs(m + 3)})
    pts = list(th) + [(th[i] + th[i + 1])/2 for i in range(len(th) - 1)] + [th[-1] + 1]
    res = [p for p in pts if nabs(m, p) == 3]
    assert all(p in th for p in res), (m, res)                          # 구간 전체가 세 실근이면 합이 정해지지 않음(없어야 함)
    return res
def Ksum_formula(m):                                                   # 갈래별 식(풀이)
    if m > 0: return 2*m + 3
    if m == 0 or m == -3: return 3
    if m < -3: return -2*m - 3
    return 0 if m == R(-3, 2) else max(-m, m + 3)                       # -3<m<0: k=0(더해도 0)과 큰 쪽 하나
cand = []
for i in range(-40, 41):
    m = R(i, 4); Ks = Kset(m); s = sum(Ks)
    assert s == Ksum_formula(m), (m, Ks)
    if -3 < m < 0: assert s < 3 and 0 in Ks
    if s == 5: cand.append(m)
assert cand == [-4, 1]
ms = sp.symbols('m', real=True)
assert sp.solve(sp.Eq(2*ms + 3, 5), ms) == [1] and sp.solve(sp.Eq(-2*ms - 3, 5), ms) == [-4]
print('세 실근이 되는 k의 합 = 5 → 극솟값 후보 m = 1, -4 (부호가 다른 갈래는 합 < 3) OK')

# 양수 a: m=g(0)=-G(a). a>0에서 G(a)<=3 → m>=-3
assert all(Gf(R(i, 20)) <= 3 for i in range(1, 400)) and Gf(2) == 3
assert sp.solve(sp.diff(G2, x), x) == [0, 2] and all(sp.diff(G1, x).subs(x, v) > 0 for v in (R(1, 9), R(1, 2), 1))
ap_m4 = [r for r in sp.real_roots(sp.Poly(G1 - 4, x)) if 0 < r <= 1] + [r for r in sp.real_roots(sp.Poly(G2 - 4, x)) if r > 1]
assert ap_m4 == []                                                     # m=-4: 양수 a 없음
an_m4 = [r for r in sp.real_roots(sp.Poly(G1 - 4, x)) if r < 0]; assert len(an_m4) == 1   # 음수 a는 있음(빼 보기용)
ap_m1 = sorted(set([r for r in sp.real_roots(sp.Poly(G1 + 1, x)) if 0 < r <= 1] + [r for r in sp.real_roots(sp.Poly(G2 + 1, x)) if r > 1]))
assert ap_m1 == [3]                                                    # m=1: a=3 하나
av = ap_m1[0]
g = lambda v: Gf(v) - Gf(av)
assert g(0) == 1 and g(2) == 4
ans = g(2)
# 정의대로 직접: g(2)=∫_3^2 t f(t)dt
assert sp.integrate(t*f2, (t, 3, 2)) == ans
# a=3에서 |g|=k 실근 수 직접 확인
assert [nabs(1, kv) for kv in (0, R(1, 2), 1, 2, 4, 5)] == [1, 2, 3, 4, 3, 2] and Kset(sp.Integer(1)) == [1, 4]
assert ans == CH[it['ans'] - 1] == 4
print(f'a={av}, g(0)=1, g(2)={ans} → 정답 ④, 유일 OK')

# ---------- 선지 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] > CH[0]
assert all(w in it['choices'] for w in it['wrongs']) and it['choices'][it['ans'] - 1] not in it['wrongs'] and len(it['wrongs']) >= 2
for w in it['wrongs']: assert rf"\({w}\):" in it['wrong'], w
# 정답이 본문에 나온 수와 다름
nums = set(re.findall(r'\d+', html.unescape(re.sub(r'<[^>]+>', '', full))))
assert str(ans) not in nums, nums
# 오답 경로 재현
assert sp.solve(sp.Eq(ms + 3, 5), ms) == [2] and 2 + 3 == 5 == CH[4]          # 5: k를 극댓값 높이 하나로만
assert Gf(1) == 1 and Gf(2) - Gf(1) == 2 == CH[1]                              # 2: ∫_0^a=1 → a=1, g(2)=∫_1^2
assert D == 3 == CH[2]                                                         # 3: 두 극값의 차
assert g(0) == 1 == CH[0]                                                      # 1: 극솟값
print('선지 등차·오름차순, 오답 5·2·3·1 경로 재현 OK')

# ---------- 조건 빼 보기 ----------
vals = sorted({-4 + 3, 1 + 3}); assert vals == [-1, 4]
print(f"ABLATION 18 양수 a: 필요(빼면 m=-4도 됨: 음수 a 존재, g(2)가 {vals} 두 값)")
# 절댓값을 빼면: g(x)=k 세 실근 ⇔ m<k<m+3 (구간) → k의 합이 정해지지 않음
assert all(table(m_ + R(j, 4), m_) == 3 for m_ in (R(1), R(-4)) for j in range(1, 12))
print("ABLATION 18 절댓값: 필요(빼면 세 실근이 되는 k가 구간 m<k<m+3 전체라 합이 정해지지 않음)")
alt = sp.solve(sp.Eq(2*ms + 3, 7), ms); assert alt == [2] and Ksum_formula(sp.Integer(2)) == 7 and 2 + 3 != ans
print("ABLATION 18 합 5: 필요(7로 바꾸면 m=2, g(2)=5)")
assert [m_ for m_ in [R(i, 4) for i in range(-40, 41)] if (lambda S: len(S) > 0 and sum(S) == 5)([p for p in (abs(m_), abs(m_ + 3)) if p > 0 and nabs(m_, p) == 5])] == []
print("ABLATION 18 '세 실근': 필요(다섯 실근으로 바꾸면 그런 k는 3보다 작은 값 하나뿐이라 합 5가 될 수 없음)")
# x>1 조각을 원문 2x 꼴(부호 일정, 여기서는 3x)로 되돌리면 극대가 없어 세 실근 k는 |g(0)| 하나 → m=±5, g(2)가 하나로 정해지지 않음
H2 = sp.expand(G1.subs(x, 1) + sp.integrate(t*3*t, (t, 1, x)))
def cross0(L):
    s = set(r for r in sp.real_roots(sp.Poly(G1 - L, x)) if r <= 1) | set(r for r in sp.real_roots(sp.Poly(H2 - L, x)) if r > 1)
    return len(s)
for m_ in (5, -5, 1):
    ks_ = [p for p in (sp.Integer(0), sp.Integer(abs(m_)), R(abs(m_), 2), sp.Integer(abs(m_) + 1)) if cross0(p - m_) + (cross0(-p - m_) if p != 0 else 0) == 3]
    assert ks_ == ([abs(m_)] if m_ < 0 else [])
print("ABLATION 18 x>1 조각 -3x+6: 필요(부호가 일정한 조각이면 세 실근 k는 극솟값이 음수일 때 그 절댓값 하나, 극대가 없어 g(2)가 극값이 아니고 a>0에서 g(0)<=0이라 m=-5 → 다른 값)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
assert f2.subs(t, 3) < 0                                               # f>0 아님
assert g(-1) == 2 and g(1) == 2 and g(-1) != 0                         # g(±1)=0 아님
assert cross(R(1)) == 3                                                # 수평선과 세 점에서 만나는 높이가 있음(원문: 많아야 두 점)
print('원문 설정 줄(f>0, 극소 하나, g(±1)=0, 최솟값이 수로 정해짐): f(3)<0, 극대 생김, g(±1)=2 → 불통 OK')

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
    print(f'  N제 {n}: 골격 {j2:.2f}')
    assert '|g(x)|' not in body and r'\int_a^x' not in body and '-3x+6' not in body
print('인쇄 N제 I42(287–292): 절댓값·문자 아래끝·부호가 바뀌는 조각 없음 OK')
print('ALL OK')
