# -*- coding: utf-8 -*-
# A18 (12회 18번 후보, 원문 J48, db_ref 'J48 킬러 설계A') 검증
# 원문 풀이 · 세 넓이를 정의대로(구간마다 |f| 적분) 직접 계산해 자연수 a 전수 · 갈래별 판정식 · a≥13 모두 탈락(기호 증명) · 정답 유일
# · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문·N제 골격
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
assert it['cand'] == 'A18' and it['key'] == 'J48' and it['ans'] == 1 and it['db_ref'] == 'J48 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it                                                # 분담표: 상자 원문대로(원문에 상자 없음)
full = it['body']
for s_ in (r"\(2\), \(7\)이 아닌 자연수 \(a\)", r"최고차항의 계수가 \(1\)인 삼차함수 \(f(x)\)",
           r"\((2,\ 0)\), \((7,\ 0)\), \((a,\ 0)\)", r"\(S_1&gt;S_2&gt;S_3\)", r"\(a\)의 개수는?", 'fig_18.svg'):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for kk in ('setting', 'principle', 'new'):
    assert not re.search(r'\\\([^)]*?[<>]', it['core'][kk]), kk
# core·머리 주석에 정답·풀이 요지가 없는지(갈래 경계값·정답 집합)
head = open(os.path.join(HERE, 'p6.py')).read().split('ITEMS = {')[0]
for bad in ('21', 'a&lt;12', '9/2', r'\frac9', '5,\\ 6', '8,\\ 9', '5개', '중점', '평균'):
    assert bad not in it['core']['new'] and bad not in head, bad
assert os.path.exists(os.path.join(HERE, 'fig_18.svg')) and os.path.exists(os.path.join(HERE, '..', 'fig_18.svg')) and os.path.exists(os.path.join(HERE, '..', 'figs', 'fig18.py'))
CH = [sp.Integer(v) for v in it['choices']]

# ---------- 원문 J48 ----------
fo = (x - 1)*(x - 5)*(x - a)
eqo = sp.factor(-sp.integrate(fo, (x, 0, a)) - a**2)                 # S1-S2+S3 = -∫_0^a f = a^2
ao = [s for s in sp.solve(eqo, a) if s.is_real and s > 5]
assert ao == [6 + 3*sp.sqrt(2)]
assert sp.simplify(fo.subs({x: 6, a: ao[0]}) + 15*sp.sqrt(2)) == 0 and F.I['J48'][2] == '②' and F.I['J48'][1][1] == r'-15\sqrt2'
# 원문을 넓이 정의대로도 확인
av = ao[0]; fv = fo.subs(a, av)
S1o = -sp.integrate(fv, (x, 0, 1)); S2o = sp.integrate(fv, (x, 1, 5)); S3o = -sp.integrate(fv, (x, 5, av))
assert sp.simplify(2*(S2o + av**2) - 2*S1o - 2*S3o) == 0 and S1o > 0 and S2o > 0 and sp.simplify(S3o) > 0
print('원문 J48: a=6+3√2, f(6)=-15√2 (②) OK')

# ---------- 변형: f=(x-2)(x-7)(x-a) ----------
f = (x - 2)*(x - 7)*(x - a)
def areas(av):
    """넓이를 정의대로: 근으로 나눈 구간마다 |∫f| (부호도 확인)"""
    fv = f.subs(a, av); r = sorted([sp.Integer(2), sp.Integer(7), sp.sympify(av)])
    assert 0 < r[0] < r[1] < r[2]
    I1 = sp.integrate(fv, (x, 0, r[0])); I2 = sp.integrate(fv, (x, r[0], r[1])); I3 = sp.integrate(fv, (x, r[1], r[2]))
    assert I1 < 0 and I2 > 0 and I3 < 0                                # 부호 (-,+,-)
    return -I1, I2, -I3
ok, tab = [], {}
for n in range(1, 61):
    if n in (2, 7): continue
    S = areas(n); tab[n] = S
    if S[0] > S[1] > S[2]: ok.append(n)
assert ok == [5, 6, 8, 9, 10], ok
# 등호(경계) 사례: a=12 에서만 S2=S3, S1=S2 인 자연수는 없음
assert [n for n, S in tab.items() if S[1] == S[2]] == [12] and [n for n, S in tab.items() if S[0] == S[1]] == []
# a≥13: 기호로 S2<S3 (가운데 근 7 < (2+a)/2), 따라서 a>60도 모두 탈락
I13 = sp.factor(sp.integrate(f, (x, 2, a)))                            # a>7에서 S2-S3
assert sp.simplify(I13 - (a - 2)**3*(12 - a)/12) == 0
print('자연수 a 전수(1–60, 정의대로): S1>S2>S3 ⇔ a ∈ {5,6,8,9,10}; a>12이면 S2-S3=(a-2)^3(12-a)/12<0 OK')
# 갈래별 판정식(해설 문장 확인)
Ft = sp.integrate(f, (x, 0, t))
assert sp.expand(Ft - (t**4/4 - (a + 9)*t**3/3 + (9*a + 14)*t**2/2 - 14*a*t)) == 0
assert sp.simplify(Ft.subs(t, a) - (-a**2*((a - 9)**2 + 3)/12)) == 0   # 2<a<7: 항상 음
assert sp.simplify(Ft.subs(t, 7) - 49*(2*a - 21)/12) == 0             # a>7
assert sp.simplify(Ft.subs(t, 2) - (24 - 38*a)/3) == 0                 # a<2 (a=1: 음 → S1>S2, 그러나 S2<S3)
al, be, ga, m = sp.symbols('alpha beta gamma m', real=True)
gen = sp.integrate((x - al)*(x - be)*(x - ga), (x, al, ga))
assert sp.simplify(gen - (be - (al + ga)/2)*(ga - al)**3/6) == 0       # S2-S3 = (β-m)(γ-α)^3/6
assert sp.simplify(sp.integrate((x - al)*(x - ga), (x, al, ga)) + (ga - al)**3/6) == 0
for n, S in tab.items():
    r = sorted([2, 7, n])
    assert (S[1] > S[2]) == (r[1] > R(r[0] + r[2], 2)) and (S[0] > S[1]) == (Ft.subs({a: n, t: r[1]}) < 0)
S1 = tab[1]; assert S1[0] > S1[1] and S1[1] < S1[2]                     # a=1: S2<S3로 탈락
assert all(tab[n][0] > tab[n][1] and tab[n][1] < tab[n][2] for n in (3, 4))
assert tab[11][0] < tab[11][1] and tab[11][1] > tab[11][2] and Ft.subs({a: 11, t: 7}) == R(49, 12)
print('갈래: a=1 (S2<S3) / 2<a<7 (S1>S2 항상, a>9/2 → 5,6) / a>7 (a<21/2, a<12 → 8,9,10) OK')
ans = len(ok)
assert ans == 5 and CH[it['ans'] - 1] == ans

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {1}      # 오름차순, 공차 1
NAT = [n for n in range(1, 61) if n not in (2, 7)]
w8 = [n for n in NAT if n < R(21, 2) and n < 12]            # 원문 배치(a가 가장 큰 근)의 두 조건을 모든 a에
w6 = [n for n in NAT if (n < 7 and tab[n][0] > tab[n][1] > tab[n][2]) or (n > 7 and n < 12)]
w7 = [n for n in NAT if (2 < n < 7 and tab[n][0] > tab[n][1]) or (n > 7 and tab[n][0] > tab[n][1] > tab[n][2])]   # 2<a<7에서 S2>S3 미확인
w9 = [n for n in NAT if n < 12]                              # a<12 하나만 모든 a에
assert w8 == [1, 3, 4, 5, 6, 8, 9, 10] and w6 == [5, 6, 8, 9, 10, 11] and w7 == [3, 4, 5, 6, 8, 9, 10] and w9 == [1, 3, 4, 5, 6, 8, 9, 10, 11]
assert [len(w8), len(w6), len(w7), len(w9)] == [int(v) for v in it['wrongs']]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+|&[a-z]+;|S_\d|fig_18|130pt|<[^>]+>', ' ', full))}
assert nums == {0, 1, 2, 7} and ans not in nums and -ans not in nums, nums
print('정답이 본문의 수(0, 1, 2, 7)와 같지 않음 OK')
print('정답 = ① 5, 선지 등차(공차 1, 오름차순), 오답 8(원문 배치 조건을 모든 a에)·6(a>7에서 S1>S2 미확인)·7(2<a<7에서 S2>S3 미확인)·9(a<12만) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
only23 = [n for n in NAT if tab[n][1] > tab[n][2]]; only12 = [n for n in NAT if tab[n][0] > tab[n][1]]
assert only23 == [5, 6, 8, 9, 10, 11] and only12 == [1, 3, 4, 5, 6, 8, 9, 10]
print(f"ABLATION 18 S1>S2: 필요(빼면 a={only23}, {len(only23)}개)")
print(f"ABLATION 18 S2>S3: 필요(빼면 a={only12}, {len(only12)}개)")
half = [R(k, 2) for k in range(1, 40) if R(k, 2) not in (2, 7)]
okh = [v for v in half if (lambda S: S[0] > S[1] > S[2])(areas(v))]
assert len(okh) > 5 and R(21, 2) not in okh
print(f"ABLATION 18 자연수: 필요(빼면 실수 a가 구간으로 남아 개수가 정해지지 않음, 1/2 간격 표본만 {len(okh)}개)")
print("ABLATION 18 '2, 7이 아닌': 필요(a=2, 7이면 x축과 만나는 점이 두 개라 둘러싸인 부분이 하나)")
for pq, exp in (((1, 5), None), ((2, 8), None)):
    g = (x - pq[0])*(x - pq[1])*(x - a); c = 0
    for n in range(1, 61):
        if n in pq: continue
        r = sorted([pq[0], pq[1], n]); gv = g.subs(a, n)
        A1 = -sp.integrate(gv, (x, 0, r[0])); A2 = sp.integrate(gv, (x, r[0], r[1])); A3 = -sp.integrate(gv, (x, r[1], r[2]))
        c += bool(A1 > A2 > A3)
    assert c != ans
    print(f"ABLATION 18 x절편 2, 7: 필요({pq}로 바꾸면 {c}개)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
# 원문 줄: a가 가장 큰 근(적분의 위끝이 a). 정답에 드는 a=5, 6은 가운데 근이고, 그 배치의 조건을 모든 a에 쓰면 8개
assert all(2 < n < 7 for n in ok[:2]) and len(w8) == 8 != ans
print('원문 설정 줄(a가 가장 큰 근): 정답 집합의 a=5, 6은 가운데 근, 그 배치 조건을 모든 a에 쓰면 8개(불통) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['J48'][0])); Lm = len(plain(full))
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')
assert Lm >= 0.9 * Lo, (Lo, Lm)

# ---------- 원문 · 인쇄 N제 골격 ----------
import dupcheck as DC
sk = lambda s_: set(DC.shingles(DC.skel(DC.norm(s_))))
A_ = sk(full); B2 = sk(F.I['J48'][0])
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
md = open('/home/user/Finale/output/N제/미적분1_기말_N제_07_정적분의활용.md').read()
sec = md.split('## J48 (부교재', 1)[1].split('\n## ', 1)[0]
nje = re.findall(r'\*\*(28\d)\.\*\*(.*?)(?=\n\n)', sec, re.S)
assert [n for n, _ in nje] == ['280', '281', '282', '283', '284', '285']
for n, body in nje:
    C_ = sk(body); j2 = len(A_ & C_) / len(A_ | C_)
    assert j2 < 0.60, (n, j2)
    assert 'S_1&gt;S_2' not in body and 'S_1>S_2' not in body and '개수' not in body
print('인쇄 N제 J48(280–285): 골격 0.60 미만, 대소 조건·개수 질문 없음 OK')
print('ALL OK')
