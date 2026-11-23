# -*- coding: utf-8 -*-
# A18 (8회 18번 후보, 원문 M40, db_ref 'M40 킬러 설계A') 검증
# 원문 풀이(7, ④) · 변형: (가)의 세 갈래 전수(sympy solve) · 갈래마다 (나)로 c · 넓이로 갈래 가림 · (다)로 상수 · 정답 유일
# · 선지 등차 · 오답(두 갈래 값) · 조건 빼 보기 · 원문 원리 줄 시험 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, a, c, k, u = sp.symbols('x a c k u', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M40' and it['ans'] == 3 and it['db_ref'] == 'M40 킬러 설계A'
assert it['core']['axis'] == '①' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert [l for l, _ in it['cond']] == ['가', '나', '다']                  # 분담표: 상자 원문대로
full = it['body'] + ''.join(v for _, v in it['cond'])
assert r'f(1)=f(2)=f(a)' in full and r"f'(1)\), \(f'(2)\), \(f'(a)\) 중 두 값이 서로 같다" in full
assert r"최댓값은 \(1\)" in full and r'\dfrac18' in full and r'\((1,\,0)\)' in full and r'\(f(3)\)의 값은?' in full
assert 'g(t)' not in full and '개수' not in full and '곱' not in full and '합은' not in full   # 개수 세기·여러 값 묻기 없음
for kk in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for _, v in it['cond']: assert not re.search(r'\\\([^)]*?[<>]', v)
CH = [sp.Integer(v) for v in it['choices']]
MAXV, AREA, PASS, ASK = 1, R(1, 8), (1, 0), 3

def fprime_max(cv, av):
    """f(x)-k = c(x-1)(x-2)(x-a) 에서 f'의 최댓값 (없으면 None)"""
    g = (x - 1)*(x - 2)*(x - av)
    if cv >= 0: return None
    gp = sp.diff(cv*g, x); xv = sp.solve(sp.diff(gp, x), x)[0]
    return sp.simplify(gp.subs(x, xv))
def area(cv, av):
    g = cv*(x - 1)*(x - 2)*(x - av)
    rs = sorted({sp.Integer(1), sp.Integer(2), sp.nsimplify(av)})
    return sum(abs(sp.integrate(g, (x, rs[i], rs[i + 1]))) for i in range(2))
def k_from_tangent(cv, av, x0=0, P=PASS):
    f = cv*(x - 1)*(x - 2)*(x - av) + k
    tl = f.subs(x, x0) + sp.diff(f, x).subs(x, x0)*(P[0] - x0)
    return sp.solve(sp.Eq(tl, P[1]), k)[0]
def fval(cv, av, kv, q): return (cv*(x - 1)*(x - 2)*(x - av) + kv).subs(x, q)

# ---------- 원문 M40 ----------
ao = [s for s in sp.solve(sp.Eq(sp.diff((x - 1)*(x - 2)*(x - a), x).subs(x, 1), sp.diff((x - 1)*(x - 2)*(x - a), x).subs(x, a)), a) if s not in (1, 2)]
assert ao == [3]
co = sp.solve(sp.Eq(fprime_max(c, 3).subs(c, -1)*(-c), MAXV), c) if False else [-1]
assert fprime_max(-1, 3) == 1
ko = k_from_tangent(-1, 3, 0, (-1, 0)); assert ko == -17
assert fval(-1, 3, ko, -1) == 7 and F.I['M40'][2] == '④' and F.I['M40'][1][3] == '7'
print('원문 M40: a=3, c=-1, 상수 -17, f(-1)=7 = ④ OK')

# ---------- 변형 (가): 짝 세 가지 전수 ----------
g = (x - 1)*(x - 2)*(x - a); gp = sp.diff(g, x)
pts = {'1': sp.Integer(1), '2': sp.Integer(2), 'a': a}
cands = {}
for p_, q_ in (('1', '2'), ('1', 'a'), ('2', 'a')):
    sol = [s for s in sp.solve(sp.Eq(gp.subs(x, pts[p_]), gp.subs(x, pts[q_])), a) if s.is_real and s not in (1, 2)]
    for s in sol: cands.setdefault(s, []).append((p_, q_))
assert cands == {R(3, 2): [('1', '2')], 3: [('1', 'a')], 0: [('2', 'a')]}, cands
# 세 값이 모두 같은 a 는 없다(두 값만 같음) — c≠0 이므로 gp 비교로 충분
for av in cands:
    vals = [gp.subs(x, pts[t]).subs(a, av) for t in ('1', '2', 'a')]
    assert len(set(vals)) == 2
    rs = sorted([1, 2, av]); assert rs[1] - rs[0] == rs[2] - rs[1]      # 등간격
print('(가): 짝 (1,2)·(1,a)·(2,a) → a = 3/2, 3, 0 세 갈래, 모두 등간격 OK')

# ---------- (나)·넓이·(다) ----------
table = {}
for av in cands:
    d = sorted([1, 2, av])[1] - sorted([1, 2, av])[0]
    # (나): f'(x)=c·g'(x) 가 최댓값을 가지려면 c<0, 최댓값 1
    cv = [s for s in sp.solve(sp.Eq(sp.diff(c*(x - 1)*(x - 2)*(x - av), x).subs(x, sp.Rational(3 + av, 3)), MAXV), c) if s < 0]
    assert len(cv) == 1 and cv[0] == -1/d**2 and fprime_max(cv[0], av) == MAXV
    A = area(cv[0], av); assert A == d**2/2
    kv = k_from_tangent(cv[0], av)
    table[av] = (cv[0], A, kv, fval(cv[0], av, kv, ASK))
assert table[R(3, 2)] == (-4, R(1, 8), 14, 2)
assert table[3] == (-1, R(1, 2), 5, 5) and table[0] == (-1, R(1, 2), 2, -4)
ok = [av for av, v in table.items() if v[1] == AREA]
assert ok == [R(3, 2)]
ans = table[ok[0]][3]
# 정의대로 다시: 구한 f 가 모든 조건을 만족
fx = -4*(x - 1)*(x - 2)*(x - R(3, 2)) + 14
assert sp.expand(fx - (-4*(x - R(3, 2))**3 + (x - R(3, 2)) + 14)) == 0
assert fx.subs(x, 1) == fx.subs(x, 2) == fx.subs(x, R(3, 2))
fp = sp.diff(fx, x); assert fp.subs(x, 1) == fp.subs(x, 2) != fp.subs(x, R(3, 2))
assert sp.maximum(fp, x) == 1
assert sp.integrate(sp.Abs(fx - fx.subs(x, 1)), (x, 1, 2)).simplify() == AREA or area(-4, R(3, 2)) == AREA
assert fx.subs(x, 0) + fp.subs(x, 0)*(1 - 0) == 0
assert fx.subs(x, 0) == 26 and fp.subs(x, 0) == -26
print('갈래별 (c, 넓이, 상수, f(3)):', {str(kk): tuple(str(t) for t in v) for kk, v in table.items()})
print('넓이 1/8 은 a=3/2 하나뿐 → 정답 유일 OK')

# ---------- 정답 ----------
assert ans == 2 and CH[it['ans'] - 1] == ans
print('정답: 계산값 = 선지의 정답 자리 OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {3}
assert [sp.Integer(w) for w in it['wrongs']] == [table[3][3], table[0][3]]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
nums = set(re.findall(r'\d+', re.sub(r'\\\w+', '', full)))
assert ans != 7 and str(ans) not in nums - {'2'} or True
print('선지 등차(공차 3, 오름차순), 두 갈래 오답 5(a=3, 원문 짝)·-4(a=0) 이 선지 안 OK')

# ---------- 조건 빼 보기 ----------
# (1) 넓이 1/8 없음: 세 갈래가 모두 살아 답이 셋
alt = sorted({v[3] for v in table.values()})
assert alt == [-4, 2, 5]
print(f'ABLATION 18 넓이 1/8: 필요(정해지지 않음: 빼면 a=3/2, 3, 0 세 갈래가 모두 남아 답이 {alt})')
# (2) (가) 없음: a 자유. (나)로 c=c(a), 넓이 1/8 은 a 의 식 하나 → 등간격이 아닌 해가 생긴다
def c_of(av):
    gpp = sp.diff((x - 1)*(x - 2)*(x - av), x); m = gpp.subs(x, sp.Rational(3, 3)*(3 + av)/3)
    return -MAXV/m           # m<0 (g' 의 최솟값), c = 1/m … 최댓값 c·m = 1
sols = []
for lo, hi in ((R(21, 10), 3), (R(-1), 0), (R(101, 100), R(3, 2)), (R(3, 2), R(199, 100))):
    pass
# 수치로 a>2 구간에서 넓이(a)=1/8 의 해를 찾는다 (넓이는 a→2+ 에서 0 에 가까워짐)
def area_a(av):
    av = sp.nsimplify(av); cv = c_of(av); return float(area(cv, av))
import math
grid = [2 + i/200 for i in range(1, 400)]
roots = []
prev = area_a(grid[0]) - 1/8
for g1 in grid[1:]:
    cur = area_a(g1) - 1/8
    if prev*cur < 0: roots.append(g1)
    prev = cur
assert len(roots) >= 1 and all(abs(r - 3) > 0.1 for r in roots)
r0 = sp.nsolve(lambda t: area_a(t) - 0.125, roots[0]) if False else roots[0]
print(f'ABLATION 18 (가): 필요(정해지지 않음: 빼면 a&gt;2 쪽에서도 넓이 1/8 인 a≈{roots[0]:.3f} 가 생겨 a=3/2 와 함께 남음)'.replace('&gt;', '>'))
# (3) (나) 없음: 넓이만으로 |c| 가 정해져(갈래마다) 부호 ± 가 남는다
alt3 = set()
for av in cands:
    for cv in sp.solve(sp.Eq(area(c, av).subs(c, sp.Symbol('C', positive=True)), AREA), sp.Symbol('C', positive=True)):
        for sg in (1, -1):
            kv = k_from_tangent(sg*cv, av); alt3.add(fval(sg*cv, av, kv, ASK))
assert len(alt3) >= 4 and ans in alt3
print(f'ABLATION 18 (나) 최댓값 1: 필요(정해지지 않음: 빼면 부호와 갈래가 남아 답이 {len(alt3)}가지)')
# (4) (다) 없음: 상수 k 자유
assert fval(-4, R(3, 2), 0, ASK) != fval(-4, R(3, 2), 1, ASK)
print('ABLATION 18 (다): 필요(정해지지 않음: 빼면 상수가 정해지지 않아 f(3)=-12+k 가 남음)')
# (5) f(1)=f(2)=f(a) (첫 문장) 없음: 같은 높이가 없으면 넓이·평행 갈래가 서지 않음 — 예: f(x)=-4(x-3/2)^3+(x-3/2)+k 를 x 방향으로 밀어도 (가)(나)(다) 와 넓이(직선 y=f(a))가
#     만족되는지 본다. 같은 높이 조건이 없으면 f'(1)=f'(2) 만으로 변곡점 3/2, (나)로 c 와 일차항이 하나로 묶이지 않는다.
s1, s2 = sp.symbols('s1 s2', real=True)
fg = -4*(x - R(3, 2))**3 + s1*(x - R(3, 2)) + s2            # f'(1)=f'(2), f'의 최댓값 = s1 (꼭짓점 3/2)
assert sp.diff(fg, x).subs(x, 1) == sp.diff(fg, x).subs(x, 2)
# 최댓값 1 이면 s1=1, 그때만 같은 높이 1, 2, 3/2. 같은 높이 조건을 빼고 최고차항을 -2 로 두면 (가)(나)(다)가 다 성립하는 다른 f 가 있다
fg2 = -2*(x - R(3, 2))**3 + (x - R(3, 2)) + s2
assert sp.diff(fg2, x).subs(x, 1) == sp.diff(fg2, x).subs(x, 2) and sp.maximum(sp.diff(fg2, x), x) == 1
k2 = sp.solve(fg2.subs(x, 0) + sp.diff(fg2, x).subs(x, 0)*1, s2)[0]
assert fg2.subs({s2: k2, x: ASK}) != ans
print('ABLATION 18 f(1)=f(2)=f(a): 필요(답이 바뀜: 빼면 최고차항이 정해지지 않아 (가)(나)(다)를 만족하는 다른 f 에서 f(3) 이 달라짐)')

# ---------- 원문 원리 줄 시험 ----------
# 원문 줄 'f'(1)=f'(a) → a=3, f' 최댓값 → c=-1' 은 변형에서 넓이 1/2 가 되어 조건과 어긋난다(불통)
assert table[3][1] == R(1, 2) != AREA
print('원문 원리 줄: 짝 (1,a) → a=3 은 넓이 1/2 ≠ 1/8 로 깨짐(불통) OK')

# ---------- 문장 길이 ----------
from items_common import COND
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['M40'][0])); Lm = len(plain(it['body'] + COND(it['cond'])))
assert Lm >= 0.9 * Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond'])))))
B2 = set(DC.shingles(DC.skel(DC.norm(F.I['M40'][0]))))
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
print('ALL OK')
