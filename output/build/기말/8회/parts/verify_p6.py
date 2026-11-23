# -*- coding: utf-8 -*-
# A18 (8회 18번 후보, 원문 M40, db_ref 'M40 킬러 설계A') 검증
# 원문 풀이(7, ④) · 변형: (가)의 짝 세 가지 전수(sympy solve) · (나)로 c 부호·크기 · 기울기 양수로 갈래 가림 · (다)로 상수 · 정답 유일
# · a 격자 전수(정의대로) · 선지 등차 · 오답(두 갈래 값) · 조건 빼 보기 · 원문 원리 줄 시험 · 넓이판이 버려진 이유 · 문장 길이 · 원문 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
from items_common import COND
x, a, c, k = sp.symbols('x a c k', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'M40' and it['ans'] == 3 and it['db_ref'] == 'M40 킬러 설계A'
assert it['core']['axis'] == '①' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert [l for l, _ in it['cond']] == ['가', '나', '다']                  # 분담표: 상자 원문대로
full = it['body'] + ''.join(v for _, v in it['cond'])
assert r'f(1)=f(2)=f(a)' in full and r"f'(1)\), \(f'(2)\), \(f'(a)\) 중 두 값이 서로 같다" in full
assert r"최댓값은 \(1\)" in full and r"\(f'(a)&gt;0\)일 때" in full and r'\((1,\,0)\)' in full and r'\(f(3)\)의 값은?' in full
assert 'g(t)' not in full and '개수' not in full and '곱' not in full and '합은' not in full   # 개수 세기·여러 값 묻기 없음
for kk in ('sol', 'fast', 'wrong', 'note', 'var'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for _, v in it['cond']: assert not re.search(r'\\\([^)]*?[<>]', v)
CH = [sp.Integer(v) for v in it['choices']]
MAXV, PASS, ASK = 1, (1, 0), 3

def fx_of(cv, av, kv): return cv*(x - 1)*(x - 2)*(x - av) + kv
def fprime_max(cv, av):
    """f'(x) 의 최댓값 (c>=0 이면 최댓값 없음 → None)"""
    if cv >= 0: return None
    gp = sp.diff(fx_of(cv, av, 0), x)
    return sp.simplify(gp.subs(x, sp.solve(sp.diff(gp, x), x)[0]))
def c_from_max(av):
    sols = [s for s in sp.solve(sp.Eq(fprime_max(-sp.Symbol('C', positive=True), av), MAXV), sp.Symbol('C', positive=True))]
    assert len(sols) == 1
    return -sols[0]
def k_from_tangent(cv, av, x0=0, P=PASS):
    f = fx_of(cv, av, k)
    return sp.solve(sp.Eq(f.subs(x, x0) + sp.diff(f, x).subs(x, x0)*(P[0] - x0), P[1]), k)[0]

# ---------- 원문 M40 ----------
g = (x - 1)*(x - 2)*(x - a); gp = sp.diff(g, x)
ao = [s for s in sp.solve(sp.Eq(gp.subs(x, 1), gp.subs(x, a)), a) if s not in (1, 2)]
assert ao == [3] and c_from_max(3) == -1
ko = k_from_tangent(-1, 3, 0, (-1, 0)); assert ko == -17
assert fx_of(-1, 3, ko).subs(x, -1) == 7 and F.I['M40'][2] == '④' and F.I['M40'][1][3] == '7'
print('원문 M40: a=3, c=-1, 상수 -17, f(-1)=7 = ④ OK')

# ---------- (가): 짝 세 가지 전수 ----------
pts = {'1': sp.Integer(1), '2': sp.Integer(2), 'a': a}
cands = {}
for p_, q_ in (('1', '2'), ('1', 'a'), ('2', 'a')):
    for s in sp.solve(sp.Eq(gp.subs(x, pts[p_]), gp.subs(x, pts[q_])), a):
        if s.is_real and s not in (1, 2): cands.setdefault(s, []).append((p_, q_))
assert cands == {R(3, 2): [('1', '2')], 3: [('1', 'a')], 0: [('2', 'a')]}, cands
for av in cands:
    vals = [gp.subs(x, pts[t]).subs(a, av) for t in ('1', '2', 'a')]
    assert len(set(vals)) == 2                                     # 두 값만 같다(셋 다 같은 a 없음)
    rs = sorted([1, 2, av]); assert rs[1] - rs[0] == rs[2] - rs[1]  # 등간격
print('(가): 짝 (1,2)·(1,a)·(2,a) → a = 3/2, 3, 0 세 갈래, 모두 등간격 OK')

# ---------- (나)·기울기·(다) ----------
table = {}
for av in cands:
    d = sorted([1, 2, av])[1] - sorted([1, 2, av])[0]
    cv = c_from_max(av); assert cv == -1/sp.nsimplify(d)**2 and cv < 0
    slope_a = sp.diff(fx_of(cv, av, 0), x).subs(x, av)
    kv = k_from_tangent(cv, av)
    table[av] = (cv, slope_a, kv, fx_of(cv, av, kv).subs(x, ASK))
assert table[R(3, 2)] == (-4, 1, 14, 2)
assert table[3] == (-1, -2, 5, 5) and table[0] == (-1, -2, 2, -4)
ok = [av for av, v in table.items() if v[1] > 0]
assert ok == [R(3, 2)]
ans = table[ok[0]][3]
# 구한 f 가 모든 조건을 정의대로 만족
fx = fx_of(-4, R(3, 2), 14); fp = sp.diff(fx, x)
assert sp.expand(fx - (-4*(x - R(3, 2))**3 + (x - R(3, 2)) + 14)) == 0
assert fx.subs(x, 1) == fx.subs(x, 2) == fx.subs(x, R(3, 2))
assert fp.subs(x, 1) == fp.subs(x, 2) != fp.subs(x, R(3, 2))
assert sp.maximum(fp, x) == 1 and fp.subs(x, R(3, 2)) > 0
assert fx.subs(x, 0) + fp.subs(x, 0)*(1 - 0) == 0
print('갈래별 (c, f\'(a), 상수, f(3)):', {str(kk): tuple(str(t) for t in v) for kk, v in table.items()})
print('기울기 양수는 a=3/2 하나뿐 → 정답 유일 OK')

# 격자 전수: a 를 -5..5 (1/40 간격, 1·2 제외)로 돌려 (가)·(나)·기울기를 정의대로 확인 — 남는 a 는 3/2 하나
hits = []
for i in range(-200, 201):
    av = R(i, 40)
    if av in (1, 2): continue
    fv = [gp.subs({a: av, x: t}) for t in (1, 2, av)]
    if len(set(fv)) == 3: continue                                 # (가) 아님
    cv = c_from_max(av)                                            # (나)
    if sp.diff(fx_of(cv, av, 0), x).subs(x, av) > 0: hits.append(av)
assert hits == [R(3, 2)]
print('전수: a=-5..5 (1/40 간격) 399개 중 (가)·(나)·기울기를 모두 만족하는 a 는 3/2 하나 OK')

# ---------- 정답 ----------
assert ans == 2 and CH[it['ans'] - 1] == ans
print('정답: 계산값 = 선지의 정답 자리 OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {3}
assert [sp.Integer(w) for w in it['wrongs']] == [table[3][3], table[0][3]]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert ans != 7
print('선지 등차(공차 3, 오름차순), 두 갈래 오답 5(a=3, 원문 짝)·-4(a=0) 가 선지 안, 정답은 원문 답 7 과 다름 OK')

# ---------- 조건 빼 보기 ----------
# (1) 기울기 양수 없음: 세 갈래가 모두 살아 답이 셋
alt = sorted({v[3] for v in table.values()})
assert alt == [-4, 2, 5]
print(f'ABLATION 18 기울기 양수: 필요(정해지지 않음: 빼면 a=3/2, 3, 0 세 갈래가 모두 남아 답이 {alt})')
# (2) (가) 없음: c<0 이면 기울기 양수인 같은 높이 점은 가운데 근 → 1<a<2 이면 모두 가능
alt2 = {}
for av in (R(5, 4), R(3, 2), R(7, 4)):
    cv = c_from_max(av); assert sp.diff(fx_of(cv, av, 0), x).subs(x, av) > 0
    alt2[str(av)] = fx_of(cv, av, k_from_tangent(cv, av)).subs(x, ASK)
assert len(set(alt2.values())) == 3
print(f'ABLATION 18 (가): 필요(정해지지 않음: 빼면 1<a<2 인 a 가 모두 남아 a=5/4, 3/2, 7/4 에서 답이 {sorted(set(alt2.values()))})')
# (3) (나) 없음: c 의 부호·크기 자유. c>0 이면 기울기 양수는 끝 근 → a=3, 0 도 살고, c<0 이어도 크기가 자유
alt3 = set()
for av in cands:
    for cv in (-4, -1, 1, 2):
        if sp.diff(fx_of(cv, av, 0), x).subs(x, av) > 0:
            alt3.add(fx_of(cv, av, k_from_tangent(cv, av)).subs(x, ASK))
assert len(alt3) >= 4 and ans in alt3
print(f'ABLATION 18 (나) 최댓값 1: 필요(정해지지 않음: 빼면 c 의 부호·크기가 남아 답이 {len(alt3)}가지 이상)')
# (4) (다) 없음: 상수 k 자유
assert fx_of(-4, R(3, 2), 0).subs(x, ASK) != fx_of(-4, R(3, 2), 1).subs(x, ASK)
print('ABLATION 18 (다): 필요(정해지지 않음: 빼면 상수가 남아 f(3)=-12+k)')
# (5) f(1)=f(2)=f(a) 없음: (가)의 a 가 아무 수나 될 수 있다. 예: a=3 으로 두고 f'(1)=f'(3) (변곡점 2),
#     f'(x)=1-3C(x-2)^2 꼴(최댓값 1), f'(3)=1-3C>0 인 C 를 잡으면 (가)(나)(다)·f'(a)>0 이 모두 성립하고 f(3) 은 C 에 따라 달라진다
Cs, s2 = sp.symbols('Cs s2', real=True)
alt5 = set()
for Cv in (R(1, 4), R(1, 5), R(1, 6)):
    fg = -Cv*(x - 2)**3 + (x - 2) + s2; fgp = sp.diff(fg, x)
    assert fgp.subs(x, 1) == fgp.subs(x, 3) != fgp.subs(x, 2) and sp.maximum(fgp, x) == 1 and fgp.subs(x, 3) > 0
    sv = sp.solve(fg.subs(x, 0) + fgp.subs(x, 0)*(1 - 0), s2)[0]
    alt5.add(fg.subs({s2: sv, x: ASK}))
assert len(alt5) == 3
print(f'ABLATION 18 f(1)=f(2)=f(a): 필요(정해지지 않음: 빼면 a=3, 최고차항 -1/4, -1/5, -1/6 등에서 (가)(나)(다)·f\'(a)>0 이 모두 성립, 답이 {len(alt5)}가지)')

# ---------- 원문 원리 줄 시험 ----------
assert table[3][1] < 0
print('원문 원리 줄: 짝 (1,a) → a=3, c=-1 은 f\'(3)=-2<0 이라 기울기 조건에서 깨짐(불통) OK')

# ---------- 넓이판이 버려진 이유 (설계A 넓이 조건 시험) ----------
# (나)로 정한 c 에서 곡선 y=f(x)와 직선 y=f(a)로 둘러싸인 넓이는 a=3/2 에서 최소(1/8)라, 넓이 1/8 을 두면 (가) 없이도 a 가 정해진다
def area_a(av):
    cv = c_from_max(av); rs = sorted({sp.Integer(1), sp.Integer(2), av})
    return sum(abs(sp.integrate(fx_of(cv, av, 0), (x, rs[i], rs[i + 1]))) for i in range(2))
assert area_a(R(3, 2)) == R(1, 8) and all(area_a(av) > R(1, 8) for av in (R(-1), 0, R(5, 4), R(7, 5), R(8, 5), R(7, 4), 3, 4))
print('넓이판: 넓이는 a=3/2 에서 최소 1/8 → (가)가 군더더기 → 쓰지 않음 (확인)')

# ---------- 문장 길이 ----------
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
