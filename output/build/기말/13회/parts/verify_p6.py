# -*- coding: utf-8 -*-
# A18 (13회 18번 후보, 원문 I36, db_ref 'I36 킬러 설계A') 검증
# 원문 풀이 · 연속 조건 · 칸의 정적분 식 · 정수 a 전수(칸마다 방정식을 정의대로 풀어 실근 세기) · 갈래별 세는 식 · 범위 밖 a의 기호 논증
# · 정답 유일 · 선지 등차 · 오답 경로 재현 · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문·N제 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, t, a, b = sp.symbols('x t a b', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'I36' and it['ans'] == 4 and it['db_ref'] == 'I36 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it and 'bogi' not in it                           # 분담표: 상자 원문대로(원문에 상자 없음)
full = it['body']
for s_ in (r"정수 \(a\)와 상수 \(b\)", "실수 전체의 집합에서 연속", r"\(f(x+1)=f(x)+b\)", r"\(0\le x&lt;1\)일 때 \(f(x)=ax^2-14x\)",
           r"방정식 \(f(x)=0\)의 서로 다른 실근의 개수가 \(6\)", r"\int_{-2}^{1}f(x)\,dx\)의 값은?"):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값', '<img', '가능한 모든', '합은', '넓이', '접선', '수직선'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for kk in ('setting', 'principle', 'new'):
    assert not re.search(r'\\\([^)]*?[<>]', it['core'][kk]), kk
# core·머리 주석에 정답·풀이 요지가 없는지(정해지는 계수·개수 표·경계 판단·정답)
head = open(os.path.join(HERE, 'p6.py')).read().split('ITEMS = {')[0]
for bad in ('a=13', '=-5', r'\(-5\)', 'b=-1', r'{49}', r'\frac{14}', 't=1', r'8,\ 4', '하나뿐', '같은 점', '비대칭'):
    assert bad not in it['core']['new'] and bad not in head, bad
CH = [sp.Integer(v) for v in it['choices']]
D_ = 14; T_ = 6; LO, HI = -2, 1                                        # 본문 수치

# ---------- 원문 I36 ----------
fo = a*x**2 - 1
eo = sp.solve([sp.Eq(fo.subs(x, 1), fo.subs(x, 0) + b), sp.Eq(sp.integrate(fo, (x, 0, 1)) + 2*b, R(11, 3))], [a, b], dict=True)
assert eo == [{a: 2, b: 2}] and F.I['I36'][2] == '⑤' and F.I['I36'][1][4] == '4'
# 원문을 정의대로: 2≤x<3에서 f(x)=f(x-2)+2b
assert sp.integrate((fo.subs(x, x - 2) + 2*b).subs({a: 2, b: 2}), (x, 2, 3)) == R(11, 3)
print('원문 I36: a=b=2, a+b=4 (⑤) OK')

# ---------- 변형: 0≤x<1에서 f=ax^2-14x, f(x+1)=f(x)+b ----------
g = a*t**2 - D_*t
# 연속: x=1에서 좌극한 g(1)=a-14, f(1)=f(0)+b=b. 다른 정수에서도 같은 식
bb = sp.solve(sp.Eq(g.subs(t, 1), g.subs(t, 0) + b), b)[0]
assert sp.expand(bb - (a - D_)) == 0
k = sp.symbols('k', integer=True)
assert sp.simplify((g.subs(t, 1) + k*bb) - (g.subs(t, 0) + (k + 1)*bb)) == 0      # 모든 정수 k+1에서 이어짐
# 원리 줄: 칸 [k,k+1]의 정적분 = ∫_0^1 g + kb
I0 = sp.integrate(g, (t, 0, 1)); assert sp.expand(I0 - (a/3 - R(D_, 2))) == 0
assert sp.expand(sp.integrate(g.subs(t, x - k) + k*b, (x, k, k + 1)) - (I0 + k*b)) == 0
print('연속 ⇔ b=a-14, 칸의 정적분 = ∫_0^1 f + kb OK')

def block_roots(av, bv, kv):
    """k≤x<k+1에서 f(x)=0의 실근(정의대로: g(t)+kb=0, 0≤t<1)을 x값으로"""
    e = sp.Poly(av*t**2 - D_*t + kv*bv, t)
    if e.is_zero: return None
    rs = set(sp.roots(e, multiple=True)) if e.degree() > 0 else set()
    return {sp.nsimplify(r + kv) for r in rs if r.is_real and r >= 0 and r < 1}
def allroots(av, bv=None):
    av = sp.sympify(av); bv = av - D_ if bv is None else sp.sympify(bv)
    if bv == 0: return None                                            # 주기함수: f(정수)=0, 무수히 많음
    K = int(sp.ceiling((abs(av) + D_) / abs(bv))) + 2                 # |kb| > |a|+14 ≥ sup|g| 이면 근 없음
    out = set()
    for kv in range(-K, K + 1):
        out |= block_roots(av, bv, kv)
    return out
def N(av, bv=None):
    r = allroots(av, bv); return sp.oo if r is None else len(r)
# a=14: 주기, 정수마다 근
assert all((14*t**2 - 14*t).subs(t, 0) == 0 for _ in [0]) and N(14) == sp.oo
tab = {n: N(n) for n in range(-40, 81)}
ok = [n for n, v in tab.items() if v == T_]
assert ok == [13], ok
assert all(tab[n] == 1 for n in range(-40, 8)) and tab[14] == sp.oo
assert [tab[n] for n in range(8, 14)] == [2, 2, 2, 2, 4, 6] and [tab[n] for n in range(15, 19)] == [8, 4, 2, 2]
assert all(tab[n] == 2 for n in range(17, 81))
print('정수 a 전수(-40–80, 칸마다 정의대로): a≤7 → 1개, 8–11 → 2개, 12 → 4개, 13 → 6개, 14 → 무수히 많음, 15 → 8개, 16 → 4개, a≥17 → 2개 OK')
# 범위 밖 a(기호 논증): a≤7이면 조각이 [0,1)에서 감소(g'(t)=2at-14<0)·b<0 → f 감소, a≥17이면 b≥3>49/a
assert sp.solve(sp.diff(g, t), t) == [7/a]
for n in range(-40, 8):
    assert all(sp.diff(g, t).subs({a: n, t: R(j, 20)}) < 0 for j in range(0, 20)) and n - D_ < 0
assert sp.simplify(g.subs(t, 7/a) + 49/a) == 0                         # 조각의 최솟값 -49/a
aa = sp.symbols('aa', positive=True)
assert sp.solve_univariate_inequality((aa - D_) > 49/aa, aa, relational=False).contains(17) and (17 - D_)*17 > 49
# 갈래별 세는 식(해설 문장 확인)
def n_up(n):     # a≥15: 2 + 2·#{k≥1 : kb < 49/a}
    return 2 + 2*sum(1 for kv in range(1, 200) if kv*(n - D_)*n < 49)
def n_down(n):   # 8≤a≤13: 1 + 1 + 2·#{m≥2 : -mb < 49/a}
    return 2 + 2*sum(1 for m in range(2, 200) if m*(D_ - n)*n < 49)
assert all(tab[n] == n_up(n) for n in range(15, 81)) and all(tab[n] == n_down(n) for n in range(8, 14))
assert all(kv*(n - D_)*n != 49 for n in range(8, 81) for kv in range(-200, 200))   # 등호(꼭짓점이 x축 위)인 정수 a 없음
# 내려가는 쪽: 바로 왼쪽 칸의 근은 하나(t=1 제외), 기본 칸의 근은 x=0 하나
assert sp.factor(g - (a - D_)) == (t - 1)*(a*t + a - 14)
for n in range(8, 14):
    assert block_roots(n, n - D_, 0) == {0} and block_roots(n, n - D_, -1) == {R(D_, n) - 2}
    assert all(block_roots(n, n - D_, kv) == set() for kv in range(1, 6))
for n in range(15, 30):
    assert block_roots(n, n - D_, 0) == {0, R(D_, n)} and all(block_roots(n, n - D_, kv) == set() for kv in range(-6, 0))
R13 = sorted(allroots(13), key=lambda v: float(v)); assert len(R13) == 6 and R13[-1] == 0 and R13[-2] == R(14, 13) - 2 and all(v <= 0 for v in R13)
print('갈래: 올라가는 쪽 2+2·#{k≥1: kb<49/a} / 내려가는 쪽 1+1+2·#{m≥2: -mb<49/a}(바로 왼쪽 칸은 t=1이 빠져 1개) OK')
A = 13; B = A - D_
def val(av, bv, shifts):
    return sum(sp.integrate(g.subs(a, av), (t, 0, 1)) + s*bv for s in shifts)
true_shifts = list(range(LO, HI))                                       # 칸 -2, -1, 0
ans = val(A, B, true_shifts)
# 정의대로 직접 적분(칸마다 f(x)=g(x-k)+kb)
direct = sum(sp.integrate((g.subs(t, x - kv) + kv*B).subs(a, A), (x, kv, kv + 1)) for kv in range(LO, HI))
assert ans == direct == -5 and CH[it['ans'] - 1] == ans
print(f'a={A}, b={B}, ∫_{{-2}}^{{1}} f = {ans} OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {2}        # 오름차순, 공차 2
# -3: b<0에서도 대칭으로 셈(기본 칸 2개, 바로 왼쪽 칸부터 2개씩) → a=12
naive = {n: (2 + 2*sum(1 for m in range(1, 200) if m*abs(n - D_)*n < 49)) for n in range(8, 81) if n != D_}
assert [n for n, v in naive.items() if v == T_] == [12]
w1 = val(12, 12 - D_, true_shifts)
# -11: 왼쪽 칸도 +|k|b
w2 = val(A, B, [abs(s) for s in true_shifts])
# -7: 칸 번호가 하나씩 밀림([-1,0]을 기본 칸으로)
w3 = val(A, B, [s + 1 if s < 0 else s for s in true_shifts])
# -9: 기본 칸의 두 근을 빼고 옮겨진 칸의 근만 셈 → a=15
omit = {n: tab[n] - 2 for n in range(8, 81) if n != D_}
assert [n for n, v in omit.items() if v == T_] == [15]
w4 = val(15, 15 - D_, true_shifts)
assert [w1, w2, w3, w4] == [-3, -11, -7, -9] == [int(v) for v in it['wrongs']]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert set(CH) == {ans, w1, w2, w3, w4}
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+|&[a-z]+;|<[^>]+>|\^2', ' ', full))}
assert nums == {0, 1, 6, -14, -2}, nums
assert ans not in nums and -ans not in nums
print('정답이 본문의 수와 같지 않음 OK')
print('정답 = ④ -5, 선지 등차(공차 2, 오름차순), 오답 -3(내려가는 쪽을 대칭으로 세어 a=12)·-11(왼쪽 칸에 +b)·-7(칸 번호 밀림)·-9(기본 칸의 근을 빼고 세어 a=15) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
# 정수: 실수 a이면 개수 6인 a가 구간으로 남음
extra = [v for v in (R(64, 5), R(129, 10), R(151, 10), R(31, 2)) if N(v) == T_]
assert len(extra) == 4 and len({val(v, v - D_, true_shifts) for v in extra} | {ans}) == 5
print(f"ABLATION 18 정수: 필요(빼면 a={[str(v) for v in extra]} 등에서도 개수 6, 값이 정해지지 않음)")
# 개수 6
assert [n for n, v in tab.items() if v == 4] == [12, 16] and [n for n, v in tab.items() if v == 8] == [15]
print("ABLATION 18 개수 6: 필요(4로 바꾸면 a=12, 16 두 개라 값이 정해지지 않음, 8로 바꾸면 a=15 → -9)")
# 연속: b가 a와 묶이지 않음 — (a, b)=(15, 6/5)도 개수 6
assert N(15, R(6, 5)) == T_ and val(15, R(6, 5), true_shifts) != ans
print("ABLATION 18 연속: 필요(빼면 (a, b)=(15, 6/5)도 개수 6, 값 -48/5)")
# 조각의 계수 14
for dv in (10, 12):
    D_keep = D_; D_ = dv; g2 = g
    g = a*t**2 - dv*t
    cand = [n for n in range(-20, 60) if n != dv and N(n) == T_]
    vals = {val(n, n - dv, true_shifts) for n in cand}
    assert vals != {ans}
    print(f"ABLATION 18 계수 14: 필요({dv}로 바꾸면 개수 6인 정수 a={cand}, 값 {sorted(vals)})")
    D_ = D_keep; g = g2
# 구간 [-2, 1]
assert val(A, B, [0, 1, 2]) != ans and val(A, B, [-1, 0, 1]) != ans
print("ABLATION 18 구간 [-2, 1]: 필요(구간을 옮기면 값이 달라짐)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
# 원문 줄: 조각이 한 방향 + 정적분의 값 한 식으로 a 결정. 변형에는 정적분의 값이 없고, 조각이 한 방향인 a≤7은 실근 1개,
# 원문처럼 올라가는 그래프(b>0)만 보면 개수는 8, 4, 2뿐
assert r'=\dfrac' not in full and all(tab[n] == 1 for n in range(-40, 8)) and T_ not in {tab[n] for n in range(15, 81)}
print('원문 설정 줄(조각이 한 방향, 정적분의 값 한 식): 값 조건 없음 · 한 방향인 a≤7은 1개 · b>0 쪽은 8, 4, 2개뿐(불통) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['I36'][0])); Lm = len(plain(full))
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')
assert Lm >= 0.9 * Lo, (Lo, Lm)

# ---------- 원문 · 인쇄 N제 골격 ----------
import dupcheck as DC
sk = lambda s_: set(DC.shingles(DC.skel(DC.norm(s_))))
A_ = sk(full); B2 = sk(F.I['I36'][0])
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만, 학교 17–18 범위 0.25 이하)')
assert jd <= 0.25
md = open('/home/user/Finale/output/N제/미적분1_기말_N제_06_부정적분과정적분.md').read()
sec = md.split('## I36 (부교재', 1)[1].split('\n## ', 1)[0]
nje = re.findall(r'\*\*(2\d\d)\.\*\*(.*?)(?=\n\n\*\*2\d\d\.\*\*|\Z)', sec, re.S)
assert [n for n, _ in nje] == ['246', '247', '248', '249', '250', '251', '252', '253'], [n for n, _ in nje]
for n, body in nje:
    C_ = sk(body); j2 = len(A_ & C_) / len(A_ | C_)
    assert j2 < 0.60, (n, j2)
    assert '실근' not in body and '정수' not in body and r'\int_{-2}^{1}' not in body
print('인쇄 N제 I36(246–253): 골격 0.60 미만, 실근의 개수 조건·정수 계수·구간 [-2, 1] 없음 OK')
print('ALL OK')
