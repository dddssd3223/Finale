# -*- coding: utf-8 -*-
# q18.py (견본5 18번 Claude 후보 B, claudeB18, 원본 D40) 검증
# 원문 풀이(50) · 전수 조사(유일성) · 정답 = ③ · 선지 등차 · 오답 값 · 조건 빼 보기 · 문장 길이 · 원문 설정 줄 불통
import os, re, sys
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '부교재_기말'))
from items_common import COND
import items_final as F
x = sp.symbols('x', real=True)
b, c, d, p, q, C = sp.symbols('b c d p q C', real=True)
ns = {}; exec(open(os.path.join(HERE, 'q18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claudeB18' and it['key'] == 'D40' and it['ans'] == 3
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나', '다']
CH = [sp.nsimplify(v) for v in it['choices']]

# ---------- 도구 ----------
def n_real(poly):
    """서로 다른 실근의 개수"""
    P = sp.Poly(sp.expand(poly), x)
    return len(set(sp.real_roots(P)))

def extrema(f):
    """(극댓값, 극솟값) 또는 None (최고차항 양수 삼차: 작은 임계점이 극대)"""
    r = sorted(set(sp.real_roots(sp.Poly(sp.diff(f, x), x))))
    if len(r) != 2:
        return None
    return sp.nsimplify(f.subs(x, r[0])), sp.nsimplify(f.subs(x, r[1]))

def ok(f, need=('본문', '가', '나', '다')):
    e = extrema(f); res = True
    if '본문' in need: res &= sp.diff(f, x).subs(x, 0) == 9
    if '가' in need: res &= n_real(f - 9*x) == 2
    if '나' in need: res &= e is not None and sp.simplify(e[0] - e[1] - 4) == 0
    if '다' in need: res &= e is not None and e[1] > 0
    return bool(res)

ASK = lambda f: sp.expand(f).subs(x, 2)

# ---------- 원문 D40 ----------
fo = x**3 + b*x**2 + c*x                      # 최고차항 1, f(0)=0
# (가) f-9x = x(x^2+bx+c-9) 의 서로 다른 실근 2개 ⇔ (판별식 0, c≠9) 또는 (c=9, b≠0)
cases_o = [dict(c=9)] + [dict(c=sp.solve(sp.Eq(b**2 - 4*(c - 9), 0), c)[0])]
sols_o = []
for cs in cases_o:
    fc = fo.subs(c, cs['c'])
    for bv in sp.solve(sp.Eq(sp.diff(fc, x).subs(x, 3), 0), b):        # (나) f'(3)=0
        fb = sp.expand(fc.subs(b, bv))
        if sp.diff(fb, x, 2).subs(x, 3) < 0 and n_real(fb - 9*x) == 2:   # x=3 극대
            sols_o.append(fb)
assert sols_o == [x**3 - 12*x**2 + 45*x]
fO = sols_o[0]
assert extrema(fO) == (54, 50) and F.I['D40'][2] == '50'
assert sp.factor(fO - 9*x) == x*(x - 6)**2
# 버려지는 꼴 x^2(x-p): c=9 → f'(3)=0 에서 b=-6, x=3은 극소
fx2 = x**3 - 6*x**2 + 9*x
assert sp.diff(fx2, x).subs(x, 3) == 0 and sp.diff(fx2, x, 2).subs(x, 3) > 0
print('원문 D40: f=x^3-12x^2+45x (f-9x=x(x-6)^2), 극솟값 f(5)=50 OK')

# ---------- 원문 설정 줄 불통: f(0)은 정해져 있지 않고, 답의 f는 f(0)≠0 ----------
fA = x**3 - 6*x**2 + 9*x + 32
assert fA.subs(x, 0) != 0 and sp.rem(sp.Poly(fA - 9*x, x), sp.Poly(x, x)).as_expr() != 0
assert ok(fO, ('가',)) and not ok(fO, ('본문',))                         # 원문의 f는 f'(0)=45
print('원문 설정 줄(f(0)=0 → f-9x=x·Q) 불통: 답의 f에서 f(0)=32, f-9x는 x로 나누어떨어지지 않음 OK')

# ---------- 전수 조사: f = x^3 + b x^2 + c x + d ----------
f = x**3 + b*x**2 + c*x + d
# 본문 f'(0)=9 → c=9
assert sp.diff(f, x).subs(x, 0) == c
f9 = f.subs(c, 9)
# (나) f'(x)=3x^2+2bx+9 = 3(x-α)(x-β), α<β:  f(α)-f(β) = (β-α)^3/2,  β-α = sqrt(4b^2-108)/3
al, be = sp.symbols('alpha beta', real=True)
assert sp.simplify(sp.integrate(-3*(x - al)*(x - be), (x, al, be)) - (be - al)**3/2) == 0
disc = sp.discriminant(sp.diff(f9, x), x)                        # 4b^2 - 108
gap = sp.sqrt(disc) / 3
bs = [bv for bv in sp.solve(sp.Eq(gap**3/2, 4), b) if bv.is_real]
assert sorted(bs) == [-6, 6]
# (가) g = f - 9x = x^3 + b x^2 + d 의 서로 다른 실근 2개 ⇔ 판별식 0 (b≠0 이라 삼중근 아님)
g = sp.expand(f9 - 9*x)
dg = sp.factor(sp.discriminant(g, x))
cands = []
for bv in bs:
    for dv in sp.solve(dg.subs(b, bv), d):
        fc = sp.expand(f9.subs({b: bv, d: dv}))
        assert ok(fc, ('본문', '가', '나'))
        cands.append(fc)
assert len(cands) == 4
# 4가지: (α,β)=(1,3)·(-3,-1) × 접점 x=0·x=α+β
tab = {}
for fc in cands:
    e = extrema(fc)
    tp = [r for r in set(sp.real_roots(sp.Poly(fc - 9*x, x))) if sp.diff(fc - 9*x, x).subs(x, r) == 0][0]
    tab[str(fc)] = dict(tangent=tp, ext=e, ask=ASK(fc), pass_=ok(fc))
    print(f'  후보 {fc}: 접점 x={tp}, (극대,극소)={e}, f(2)={ASK(fc)}, (다) {"만족" if e[1] > 0 else "불만족"}')
valid = [fc for fc in cands if ok(fc)]
assert valid == [fA] or (len(valid) == 1 and sp.expand(valid[0] - fA) == 0)
assert extrema(fA) == (36, 32) and sp.factor(fA - 9*x) == (x - 4)**2*(x + 2)
ans = ASK(fA)
assert ans == 34 and CH[it['ans'] - 1] == ans
print(f'유일한 f = {fA} (직선 y=9x는 x=4에서 접함), f(2) = {ans} = ③')

# 정수 계수 범위 무차별 대입으로 한 번 더 (c=9, b·d 정수)
hits = []
for bv in range(-15, 16):
    for dv in range(-120, 121):
        fc = x**3 + bv*x**2 + 9*x + dv
        e = extrema(fc)
        if e is None or e[0] - e[1] != 4 or e[1] <= 0:
            continue
        if n_real(fc - 9*x) == 2:
            hits.append((bv, dv))
assert hits == [(-6, 32)], hits
print('정수 계수 무차별 대입(b∈[-15,15], d∈[-120,120]): (b,d)=(-6,32) 하나 OK')

# ---------- 선지: 서로 다름, 등차 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and len(dif) == 1 and list(dif)[0] != 0
print('선지', [str(v) for v in CH], '공차', list(dif)[0])

# ---------- 오답 근거 값 ----------
f1 = x**3 - 6*x**2 + 9*x            # 원점에서 접함 (원문 풀이 그대로), 극솟값 0 (경계)
f2 = x**3 + 6*x**2 + 9*x - 32       # (α,β)=(-3,-1), x=-4에서 접함
f4 = x**3 + 6*x**2 + 9*x            # (α,β)=(-3,-1), 원점에서 접함
for fw in (f1, f2, f4):
    assert any(sp.expand(fw - fc) == 0 for fc in cands) and not ok(fw)
assert extrema(f1) == (4, 0) and extrema(f2) == (-32, -36) and extrema(f4) == (0, -4)
assert f1.subs(x, 0) == 0 and f4.subs(x, 0) == 0
wv = {1: ASK(f1), 2: ASK(f2), 4: ASK(f4)}
assert wv == {1: 2, 2: 18, 4: 50}
for i, v in wv.items():
    assert CH[i - 1] == v and v != ans
    lab = '①②③④⑤'[i - 1]
    assert lab in it['wrong'] and f'\\({v}\\)' in it['wrong']
assert wv[4] == int(F.I['D40'][2])   # ④ 50은 원문 답과 같은 수
print('오답 근거 값: ①2(원점 접함, 극솟값 0 경계) ②18((-3,-1), x=-4 접함) ④50((-3,-1), 원점 접함·원문 답과 같은 수) — 모두 선지에 있음')

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
# 본문 f'(0)=9 제거: f'(x)=3(x-p)^2-3 (극값 차 4), y=9x가 x=p+2에서 접함, 극솟값 9p+14>0
fp = lambda pv: sp.expand((x - pv)**3 - 3*(x - pv) + 9*pv + 16)
alt = {pv: fp(pv) for pv in (0, 1, 2, 3)}
assert all(ok(fv, ('가', '나', '다')) for fv in alt.values()) and alt[2] == fA
vals = {pv: ASK(fv) for pv, fv in alt.items()}
assert len(set(vals.values())) == 4
print(f"ABLATION 18 본문 f'(0)=9: 필요(정해지지 않음: (가)(나)(다)만이면 f'=3(x-p)^2-3, p=0→{vals[0]}, p=1→{vals[1]}, p=2→{vals[2]}, p=3→{vals[3]})")
# (가) 제거: 상수항 자유
fG = [fA - 32 + dv for dv in (5, 32, 40)]
assert all(ok(fv, ('본문', '나', '다')) for fv in fG) and len({ASK(fv) for fv in fG}) == 3
assert not ok(fG[0], ('가',))
print(f"ABLATION 18 (가): 필요(정해지지 않음: f=x^3-6x^2+9x+d, d>0이면 모두 만족, f(2)={[ASK(fv) for fv in fG]} 등)")
# (나) 제거: b 자유 (극값을 갖고 극솟값>0, y=9x 접함)
fN = []
for bv in (-6, -7, -8, -9):
    for dv in sp.solve(dg.subs(b, bv), d):
        fc = sp.expand(f9.subs({b: bv, d: dv}))
        if ok(fc, ('본문', '가', '다')):
            fN.append(fc)
assert len(fN) >= 3 and len({ASK(fv) for fv in fN}) == len(fN)
print(f"ABLATION 18 (나): 필요(정해지지 않음: b=-6,-7,-8,-9 등에서 (가)(다) 만족, f(2)={[sp.nsimplify(ASK(fv)) for fv in fN]})")
# (다) 제거: 4가지 후보
assert all(ok(fc, ('본문', '가', '나')) for fc in cands) and sorted(ASK(fc) for fc in cands) == [2, 18, 34, 50]
print('ABLATION 18 (다): 필요(정해지지 않음: 후보 4개, f(2)=2, 18, 34, 50)')

# ---------- 문장 길이 (태그·공백 제거, 조건 포함) ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['D40'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 142 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (상자 조건 {len(it["cond"])}개 + 본문 f\'(0)=9)')
print('ALL OK')
