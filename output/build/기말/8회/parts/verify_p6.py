# -*- coding: utf-8 -*-
# A18 2판 (8회 18번 후보, 원문 M40, db_ref 'M40 킬러 설계A') 검증
# 원문 풀이(7, ④) · (가)의 짝 세 가지 전수(sympy solve) · 갈래마다 정적분·(다) 연립으로 (c, k) · (나) c<0 으로 갈래 가림 · 정답 유일
# · a 격자 전수(정의대로) · 선지 등차 · 오답(두 갈래 값) · 조건 빼 보기 · 원문 원리 줄 시험 · 문장 길이 · 원문 골격
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
assert it['cand'] == 'A18' and it['key'] == 'M40' and it['ans'] == 1 and it['db_ref'] == 'M40 킬러 설계A'
assert it['core']['axis'] == '①' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert [l for l, _ in it['cond']] == ['가', '나', '다']                  # 분담표: 상자 원문대로
full = it['body'] + ''.join(v for _, v in it['cond'])
assert r'f(1)=f(2)=f(a)' in full and r"f'(1)\), \(f'(2)\), \(f'(a)\) 중 두 값이 서로 같다" in full
assert '최댓값을 갖는다' in full and r'\int_{-1}^{1}f(x)\,dx=-24' in full and r'\((3,\,f(3))\)' in full and r'\((2,\,0)\)' in full
assert r'\(f(0)\)의 값은?' in full and "f'(a)&gt;0" not in full
assert 'g(t)' not in full and '개수' not in full and '곱' not in full and '합은' not in full and '오직' not in full
for kk in ('sol', 'fast', 'wrong', 'note', 'var'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for _, v in it['cond']: assert not re.search(r'\\\([^)]*?[<>]', v)
CH = [sp.Integer(v) for v in it['choices']]
INT, X0, P, ASK = (-1, 1, -24), 3, (2, 0), 0

def fx_of(cv, av, kv): return cv*(x - 1)*(x - 2)*(x - av) + kv
def has_max(cv, av):          # f'(x) 가 최댓값을 가짐 ⇔ 이차함수 f' 의 최고차항 계수 < 0
    lc = sp.Poly(sp.diff(fx_of(cv, av, 0), x), x).LC(); return lc < 0
def ck(av, use_int=True, use_tan=True):
    f = fx_of(c, av, k); eqs = []
    if use_int: eqs.append(sp.Eq(sp.integrate(f, (x, INT[0], INT[1])), INT[2]))
    if use_tan: eqs.append(sp.Eq(f.subs(x, X0) + sp.diff(f, x).subs(x, X0)*(P[0] - X0), P[1]))
    return sp.solve(eqs, [c, k], dict=True)

# ---------- 원문 M40 ----------
g = (x - 1)*(x - 2)*(x - a); gp = sp.diff(g, x)
ao = [s for s in sp.solve(sp.Eq(gp.subs(x, 1), gp.subs(x, a)), a) if s not in (1, 2)]
assert ao == [3]
gp3 = sp.diff(-1*(x - 1)*(x - 2)*(x - 3), x); assert sp.maximum(gp3, x) == 1
fo = fx_of(-1, 3, k); ko = sp.solve(fo.subs(x, 0) + sp.diff(fo, x).subs(x, 0)*(-1 - 0), k)[0]
assert ko == -17 and fx_of(-1, 3, ko).subs(x, -1) == 7 and F.I['M40'][2] == '④' and F.I['M40'][1][3] == '7'
print('원문 M40: a=3, c=-1, 상수 -17, f(-1)=7 = ④ OK')

# ---------- (가): 짝 세 가지 전수 ----------
pts = {'1': sp.Integer(1), '2': sp.Integer(2), 'a': a}
cands = {}
for p_, q_ in (('1', '2'), ('1', 'a'), ('2', 'a')):
    for s in sp.solve(sp.Eq(gp.subs(x, pts[p_]), gp.subs(x, pts[q_])), a):
        if s.is_real and s not in (1, 2): cands.setdefault(s, []).append((p_, q_))
assert cands == {R(3, 2): [('1', '2')], 3: [('1', 'a')], 0: [('2', 'a')]}, cands
for av in cands:
    assert len({gp.subs(x, pts[t]).subs(a, av) for t in ('1', '2', 'a')}) == 2
    rs = sorted([1, 2, av]); assert rs[1] - rs[0] == rs[2] - rs[1]
print('(가): 짝 (1,2)·(1,a)·(2,a) → a = 3/2, 3, 0 세 갈래, 모두 등간격 OK')

for av in cands: assert sp.integrate((x-1)*(x-2)*(x-av), (x, -1, 1)) == -R(2, 3)*(3 + av) - 4*av
# ---------- 갈래마다 정적분·(다) 연립 → (c, k), (나)로 가림 ----------
table = {}
for av in cands:
    S = ck(av); assert len(S) == 1
    cv, kv = S[0][c], S[0][k]
    table[av] = (cv, kv, fx_of(cv, av, kv).subs(x, ASK), has_max(cv, av))
assert table[R(3, 2)][:3] == (12, 42, 6) and table[3][:3] == (2, 4, -8) and table[0][:3] == (-3, -15, -15)
print('갈래별 (c, k, f(0), f\'최댓값 있음):', {str(kk): tuple(str(t) for t in v) for kk, v in table.items()})
ok = [av for av, v in table.items() if v[3]]
assert ok == [0]                        # 세 갈래가 c·k까지 살아 있다가 (나)에서 하나만 남음
ans = table[0][2]
fx = fx_of(-3, 0, -15); fp = sp.diff(fx, x)
assert fx.subs(x, 1) == fx.subs(x, 2) == fx.subs(x, 0)
assert fp.subs(x, 2) == fp.subs(x, 0) != fp.subs(x, 1)
assert sp.maximum(fp, x) == 3
assert sp.integrate(fx, (x, -1, 1)) == -24 and fx.subs(x, 3) + fp.subs(x, 3)*(2 - 3) == 0
print('정답 유일: (나)를 만족하는 갈래는 a=0 하나 OK')

# 격자 전수: a=-5..5 (1/40 간격, 1·2 제외), 정의대로 (가) → 연립 → (나)
hits = []
for i in range(-200, 201):
    av = R(i, 40)
    if av in (1, 2): continue
    if len({gp.subs({a: av, x: t}) for t in (1, 2, av)}) == 3: continue
    S = ck(av)
    if len(S) == 1 and has_max(S[0][c], av): hits.append((av, fx_of(S[0][c], av, S[0][k]).subs(x, ASK)))
assert hits == [(0, -15)]
print('전수: a=-5..5 (1/40 간격) 399개 중 모든 조건을 만족하는 경우는 a=0 하나 OK')

# ---------- 정답 · 선지 · 오답 ----------
assert ans == -15 and CH[it['ans'] - 1] == ans
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {7}
assert [sp.Integer(w) for w in it['wrongs']] == [table[3][2], table[R(3, 2)][2]]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert ans != 7
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+', ' ', full))}
assert ans not in nums and -ans not in nums, nums
print('정답이 본문의 어떤 수(부호 포함)와도 같지 않음 OK')
print('정답 = ①, 선지 등차(공차 7, 오름차순), 오답 -8(a=3, 원문 짝)·6(a=3/2, 가운데 근) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
alt = sorted({v[2] for v in table.values()})
assert alt == [-15, -8, 6]
print(f'ABLATION 18 (나) 최댓값을 갖는다: 필요(정해지지 않음: 빼면 세 갈래가 모두 남아 답이 {alt})')
for nm, kw in (('정적분 -24', dict(use_int=False)), ('(다)', dict(use_tan=False))):
    S = ck(0, **kw); assert len(S) == 1 and len(S[0]) == 1      # c, k 중 하나가 남음
    vals = set()
    for cv in (-1, -2, -3):
        sub = {c: cv} if c not in S[0] else {}
        kv = S[0][k].subs(sub) if k in S[0] else sp.solve(sp.Eq(S[0][c], cv), k)[0]
        vals.add(fx_of(cv, 0, kv).subs(x, ASK))
    assert len(vals) == 3
    print(f'ABLATION 18 {nm}: 필요(정해지지 않음: 빼면 c, k 가 한 식으로만 묶여 c=-1, -2, -3 에서 답이 {sorted(vals)})')
# (가) 없음: a 자유
alt3 = {}
for av in (R(-1, 2), R(-1, 4), R(1, 4)):
    S = ck(av); cv = S[0][c]
    if has_max(cv, av): alt3[str(av)] = fx_of(cv, av, S[0][k]).subs(x, ASK)
assert len(set(alt3.values())) >= 2, alt3
print(f'ABLATION 18 (가): 필요(정해지지 않음: 빼면 a={list(alt3)} 에서도 나머지 조건이 성립, 답이 {len(set(alt3.values()))}가지)')
# f(1)=f(2)=f(a) 없음: f'(2)=f'(0) (변곡점 1) 꼴 f=C(x-1)^3+L(x-1)+M 에서 C<0, 정적분·(다) 두 식으로는 세 미지수가 남음
C_, L_, M_ = sp.symbols('C_ L_ M_')
fg = C_*(x - 1)**3 + L_*(x - 1) + M_
eqs = [sp.Eq(sp.integrate(fg, (x, -1, 1)), -24), sp.Eq(fg.subs(x, 3) + sp.diff(fg, x).subs(x, 3)*(2 - 3), 0)]
vals = set()
for Cv in (-3, -6):
    S = sp.solve([e.subs(C_, Cv) for e in eqs], [L_, M_], dict=True)
    if S: vals.add(fg.subs({C_: Cv, **S[0]}).subs(x, ASK))
assert len(vals) == 2
print(f'ABLATION 18 f(1)=f(2)=f(a): 필요(답이 바뀜: 빼면 같은 높이가 없어 최고차항 계수가 남고 답이 {sorted(vals)} 등)')

# ---------- 원문 원리 줄 시험 ----------
# 원문 줄: 짝 (1,a) → a=3, 최댓값 1 → c=-1. 변형엔 최댓값 수치가 없어 c 를 정할 수 없고, 연립으로 구한 a=3 의 c=2>0 이라 (나)에서 깨짐
assert table[3][0] > 0 and not table[3][3]
print('원문 원리 줄: a=3 은 c=2>0 이라 (나)에서 깨지고, 최댓값으로 c 를 정하는 줄은 쓸 수 없음(불통) OK')

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
