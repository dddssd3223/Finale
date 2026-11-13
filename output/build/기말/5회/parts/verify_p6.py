# -*- coding: utf-8 -*-
# A18 (5회 18번 후보, 원문 M27, db_ref 'M27 킬러 설계A') 검증
# 원문 풀이(f(3)=36) · 판정 원리(|f|와 수평선 교점 3·6·4·2) · (나)를 만족시키는 f 전수(p 격자 + 정확한 풀이)
# · 갈래마다 정의대로 센 t의 집합(실근 4개인 t) · 정답 = ④ · 선지 등차 · 오답(선지 안) · 조건 빼 보기 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, t, m, c = sp.symbols('x t m c', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M27' and it['ans'] == 4 and it['db_ref'] == 'M27 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert [k for k, _ in it['cond']] == ['가', '나'] and 'f(4+x)=-f(4-x)' in it['cond'][0][1] and '|f(8)|' in it['cond'][1][1]
assert '양수' in it['body'] and '4\\)가 되도록' in it['body'] and '최고차항' not in it['body']
assert 'OP12' in it['ops']
CH = [sp.Integer(v) for v in it['choices']]

def nroots(f_, L):
    """방정식 |f(x)|=L 의 서로 다른 실근의 개수 (L>=0, 정확 계산)"""
    if L < 0: return 0
    Z = set(sp.real_roots(sp.Poly(f_ - L, x))) | set(sp.real_roots(sp.Poly(f_ + L, x)))
    return len(Z)

def T4(f_):
    """정의대로: 방정식 |f(x)|=|f(t)| 의 실근이 4개인 실수 t 전부.
    실근의 개수는 L=|f(t)| 에만 달려 있고, L의 후보는 극값의 절댓값뿐임을 아래에서 격자로도 확인한다.
    후보 t: f(t)=±(극값) 의 실근 전부."""
    fp = sp.diff(f_, x)
    crit = sp.real_roots(sp.Poly(fp, x)) if sp.degree(fp, x) == 2 else []
    cand = set()
    for cr in crit:
        v = f_.subs(x, cr)
        cand |= set(sp.real_roots(sp.Poly(f_ - v, x))) | set(sp.real_roots(sp.Poly(f_ + v, x)))
    return sorted(tv for tv in cand if nroots(f_, abs(f_.subs(x, tv))) == 4)

# ---------- 원문 M27 ----------
# f=2x^3+cx (가: 기함수), (나) |f|와 y=-f(1)이 네 점
good = []
for cv in [R(k, 2) for k in range(-40, 21)]:
    fo = 2*x**3 + cv*x
    if nroots(fo, -fo.subs(x, 1)) == 4: good.append(cv)
assert good == [-6], good
# 정확히: c<0, -f(1)=극값 크기 → c=-6 하나
mm = sp.sqrt(-c/6)
sol_c = [s for s in sp.solve(sp.Eq(-(2 + c), 4*mm**3), c) if s < 0]
assert sol_c == [-6]
assert (2*x**3 - 6*x).subs(x, 3) == 36 and F.I['M27'][2] == '②' and F.I['M27'][1][1] == '36'
print('원문 M27: c=-6, f(3)=36 = ② OK')

# ---------- 판정 원리 ----------
f2 = x**3 - 12*x
H = 16
cnt = {L: nroots(f2, L) for L in [0, 1, 8, 15, 16, 17, 40]}
assert cnt == {0: 3, 1: 6, 8: 6, 15: 6, 16: 4, 17: 2, 40: 2}, cnt
# 같은 높이의 점: f(x)-f(-m) = (x+m)^2 (x-2m)  (k=1, 중심 0)
assert sp.expand((x**3 - 3*m**2*x) - (2*m**3) - (x + m)**2*(x - 2*m)) == 0
print('판정 원리: |f|와 y=L 교점 3·6·4·2, |f|=H 인 점 ±m, ±2m OK')

# ---------- (가)(나)를 만족시키는 f 전수 ----------
# (가) ⇔ f(x)=k(x-4)^3+p(x-4)  (k≠0)
def fam(k, p): return k*(x - 4)**3 + p*(x - 4)
# p/k 격자 전수: (나)가 성립하는 p/k
ok = []
for pp in [R(j, 4) for j in range(-4*80, 4*10 + 1)]:
    f_ = fam(1, pp)
    if nroots(f_, abs(f_.subs(x, 8))) == 4: ok.append(pp)
assert ok == [-48, -12], ok
# 정확히: p=-3m^2k, |f(8)|=|k||64-12m^2|, H=2|k|m^3
s1 = [s for s in sp.solve(64 - 12*m**2 - 2*m**3, m) if s.is_real and s > 0]
s2 = [s for s in sp.solve(64 - 12*m**2 + 2*m**3, m) if s.is_real and s > 0]
assert sorted(set(s1 + s2)) == [2, 4], (s1, s2)
assert sp.factor(m**3 + 6*m**2 - 32) == (m - 2)*(m + 4)**2 and sp.factor(m**3 - 6*m**2 + 32) == (m - 4)**2*(m + 2)
# k의 부호·크기와 무관
for k in [1, -1, 2, R(-1, 3), 5]:
    assert [pp for pp in (-48*k, -12*k, -27*k, 0, 3*k) if nroots(fam(k, pp), abs(fam(k, pp).subs(x, 8))) == 4] == [-48*k, -12*k]
print('(나): m=4 (p=-48k) 또는 m=2 (p=-12k), k 무관, p 격자 전수 OK')

# ---------- 갈래마다 t의 집합과 S ----------
Svals = {}
for mv in (4, 2):
    for k in [1, -1, 2, R(-1, 3)]:
        f_ = fam(k, -3*mv**2*k)
        T = T4(f_)
        assert T == sorted([4 - 2*mv, 4 - mv, 4 + mv, 4 + 2*mv]), T
        # 격자 확인: 후보 밖 t에서는 실근 4개가 아님
        for tv in [R(j, 4) for j in range(-40, 81)]:
            if tv not in T: assert nroots(f_, abs(f_.subs(x, tv))) != 4, (mv, tv)
        S = sum(tv for tv in T if tv > 0)
        Svals.setdefault(mv, set()).add(S)
assert Svals == {4: {20}, 2: {16}}, Svals
ans = 20 + 16
assert ans == 36 and CH[it['ans'] - 1] == ans
print('갈래: m=4 → t=-4,0,8,12, S=20 / m=2 → t=0,2,6,8, S=16, 합 36 = ④ OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and len({CH[i + 1] - CH[i] for i in range(4)}) == 1 and CH[1] > CH[0]
right_only = sum(v for v in [8, 12] if v > 4) + sum(v for v in [0, 2, 6, 8] if v > 4)   # 중심 오른쪽만
with_neg = (8 + 12 + 0 - 4) + (0 + 2 + 6 + 8)                                          # 음수 t까지 (m=4에서 -4)
assert right_only == 34 and with_neg == 32
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert set(map(int, it['wrongs'])) == {right_only, with_neg}
print('선지 등차(공차 2, 오름차순), 오답 34(중심 오른쪽만)·32(음수 t 포함) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
# (가) 없음: 대칭 중심이 다른 삼차함수도 (나)를 만족시켜 S가 여러 값 → '모든 S의 합'이 정해지지 않음
alt = {}
for a0 in [0, 1, 2, 6]:
    u0 = 8 - a0
    for mv in (u0, R(u0, 2)):
        f_ = (x - a0)**3 - 3*mv**2*(x - a0)
        assert nroots(f_, abs(f_.subs(x, 8))) == 4
        alt[(a0, mv)] = sum(tv for tv in T4(f_) if tv > 0)
assert len(set(alt.values())) > 2
print(f'ABLATION 18 (가): 필요(정해지지 않음: 중심 0·1·2·6에서도 (나)가 성립, S={sorted(set(map(str, alt.values())))} 등 무수히 많음)')
# (나) 없음: m이 자유 → S가 연속으로 바뀜
altm = {mv: sum(tv for tv in T4(fam(1, -3*mv**2)) if tv > 0) for mv in (1, 3, 5)}
assert len(set(altm.values())) == 3
print(f'ABLATION 18 (나): 필요(정해지지 않음: m=1, 3, 5이면 S={list(map(str, altm.values()))}, m마다 다름)')
# '양수' 없음: 모든 t의 합
allsum = sum(sum(T4(fam(1, -3*mv**2))) for mv in (4, 2))
assert allsum == 32 and allsum != ans
print(f'ABLATION 18 양수: 필요(답 바뀜: 모든 실수 t의 합이면 16+16={allsum})')
# 개수 4 → 다른 개수: 실근 6개인 t는 구간 → 합이 없음
f4 = fam(1, -48)
assert nroots(f4, abs(f4.subs(x, 1))) == 6 and nroots(f4, abs(f4.subs(x, R(3, 2)))) == 6
print('ABLATION 18 실근의 개수 4: 필요(정해지지 않음: 6으로 바꾸면 t=1, 3/2 등 구간 전체가 맞아 합 S가 없음)')
# (나)의 8 → 중심 왼쪽 점이나 다른 점: 갈래가 바뀜
f_b = lambda mv: fam(1, -3*mv**2)
alt8 = sum(sum(tv for tv in T4(f_b(mv)) if tv > 0) for mv in (3, R(3, 2)))
assert alt8 != ans
print(f'ABLATION 18 |f(8)|: 필요(답 바뀜: |f(7)|이면 m=3, 3/2로 합 {alt8})')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M27'][0])); Lm = len(plain(it['body'] + COND(it['cond'])))
assert Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond'])))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M27'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하, 관문 0.60 미만)')
assert jd < 0.60
assert '\\[' not in it['body'] and '(단,' not in it['body']
print('ALL OK')
