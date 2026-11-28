# -*- coding: utf-8 -*-
# A18 (14회 18번 후보, 원문 I41, db_ref 'I41 킬러 설계A') 검증
# 원문 풀이 · 연결 조건(경계 후보 전수) · 후보마다 계수 · 조각의 근과 범위로 f'의 부호(극값) 판정 · 정답 유일 · 선지 등차 · 오답 경로 재현
# · 조건 빼 보기 · 원문 설정 줄 시험 · 문장 길이 · 원문·N제 골격
import os, re, sys, html
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
import items_final as F
x, t, a = sp.symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p6.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['cand'] == 'A18' and it['key'] == 'I41' and it['ans'] == 3 and it['db_ref'] == 'I41 킬러 설계A'
assert it['core']['axis'] == '②' and set(it['core']) == {'axis', 'setting', 'principle', 'new'}
assert it['level'] == '최상' and it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
assert set(it['ops']) & {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}      # 분담표: 계수 ●
assert 'cond' not in it and 'bogi' not in it                           # 분담표: 상자 원문대로(원문에 상자 없음)
full = it['body']
for s_ in (r"두 상수 \(a\), \(t\)", "실수 전체의 집합에서 미분가능한 함수", r"3x^2+4ax & (x&lt;t)", r"ax^3+3x^2 & (x\ge t)",
           "극솟값을 갖지 않는다.", r"\(f(t+2)-f(t)=-4\)", r"\(f(2)=10\)", r"\(f(t-1)\)의 값은?"):
    assert s_ in full, s_
for w_ in ('오직', '이러한', '이와 같은', '최댓값', '최솟값', '<img', '가능한 모든', '합은', '넓이', '접선', '수직선', '개수', '양수', '정수'):
    assert w_ not in full, w_
for kk in ('sol', 'fast', 'wrong', 'note', 'var', 'body'):
    assert not re.search(r'\\\([^)]*?[<>]', it[kk]), kk
for kk in ('setting', 'principle', 'new'):
    assert not re.search(r'\\\([^)]*?[<>]', it['core'][kk]), kk
# core·머리 주석에 정답·풀이 요지가 없는지(정해지는 경계·계수·버려지는 갈래·정답)
head = open(os.path.join(HERE, 'p6.py')).read().split('ITEMS = {')[0]
for bad in ('t=0', 't=2', 't=-2', r'\pm2', 'a=-3', 'a=3', 'a=-1', '=7', r'\(7\)', r'\dfrac43', '범위 밖', '나누어 버', '세 갈래', '셋'):
    assert bad not in it['core']['new'] and bad not in head, bad
CH = [sp.Integer(v) for v in it['choices']]
VAL, C2 = -4, 10                                                        # 본문 수치: f(t+2)-f(t)=-4, f(2)=10

# ---------- 원문 I41 ----------
po, qo = x**2 - 4*x, -4*x**3 + x**2
assert all(po.subs(x, v) == qo.subs(x, v) for v in (-1, 1))            # 경계 ±1에서 이어짐
n1 = sp.integrate(qo, (x, -2, -1)) + sp.integrate(po, (x, -1, 0))
n2 = -(sp.integrate(po, (x, 0, 1)) + sp.integrate(qo, (x, 1, 2)))
assert (n1, n2) == (R(59, 3), R(43, 3)) and F.I['I41'][2] == '④' and F.I['I41'][1][3] == r'\dfrac{59}{43}'
print('원문 I41: f(0)-f(-2)=59/3, f(0)-f(2)=43/3, 비 59/43 (④) OK')

# ---------- 변형: f'(x)=3x^2+4ax (x<t), ax^3+3x^2 (x>=t) ----------
P = 3*x**2 + 4*a*x; Q = a*x**3 + 3*x**2
# 미분가능 ⇒ 두 조각이 x=t에서 이어짐
conn = sp.factor(P.subs(x, t) - Q.subs(x, t))
assert sp.expand(conn + a*t*(t - 2)*(t + 2)) == 0
# a=0: f'=3x^2, f(t+2)-f(t)=6(t+1)^2+2>0 → 조건 -4 불가
d0 = sp.expand(sp.integrate(Q.subs(a, 0), (x, t, t + 2)))
assert sp.expand(d0 - (6*(t + 1)**2 + 2)) == 0 and sp.solve(sp.Eq(d0, VAL), t) == []
TS = sorted(sp.solve(sp.Eq(conn / a, 0), t)); assert TS == [-2, 0, 2]
# 다른 t에서는 조각이 끊김(격자 확인)
for n in range(-24, 25):
    tv = R(n, 4)
    if tv not in TS:
        assert sp.simplify((P - Q).subs(x, tv) / a) != 0
print('연결 조건: at(t-2)(t+2)=0, a=0은 f(t+2)-f(t)=6(t+1)^2+2>0이라 불가 → t=-2, 0, 2 OK')

def piece_int(av, tv, lo, hi, left=None, right=None):
    """∫_lo^hi f'(x)dx (lo<=hi), 경계 tv에서 나눔"""
    L = (P if left is None else left).subs(a, av); Rr = (Q if right is None else right).subs(a, av)
    if hi <= tv: return sp.integrate(L, (x, lo, hi))
    if lo >= tv: return sp.integrate(Rr, (x, lo, hi))
    return sp.integrate(L, (x, lo, tv)) + sp.integrate(Rr, (x, tv, hi))
def diff_f(av, tv, lo, hi):
    return piece_int(av, tv, lo, hi) if lo <= hi else -piece_int(av, tv, hi, lo)
def extrema(av, tv):
    """f'의 부호가 바뀌는 점(조각의 근 가운데 그 조각의 범위 안에 있는 것과 경계)과 종류"""
    p, q = P.subs(a, av), Q.subs(a, av)
    pts = {sp.nsimplify(tv)} | {r for r in sp.real_roots(sp.Poly(p, x)) if r < tv} | {r for r in sp.real_roots(sp.Poly(q, x)) if r >= tv}
    pts = sorted(pts)
    xs = [pts[0] - 1] + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1]
    fp = lambda v: (p if v < tv else q).subs(x, v)
    s = [sp.sign(fp(v)) for v in xs]
    assert 0 not in s
    return [(pts[i], 'max' if s[i] > 0 else 'min') for i in range(len(pts)) if s[i]*s[i + 1] < 0]
def roots_in_range(av, tv):
    p, q = P.subs(a, av), Q.subs(a, av)
    return sorted({r for r in sp.real_roots(sp.Poly(p, x)) if r < tv} | {r for r in sp.real_roots(sp.Poly(q, x)) if r >= tv})

cands = {}
for tv in TS:
    sol = sp.solve(sp.Eq(sp.integrate(Q, (x, tv, tv + 2)), VAL), a)
    assert len(sol) == 1
    cands[tv] = sol[0]
assert cands == {-2: 3, 0: -3, 2: -1}
assert sp.expand(sp.integrate(Q, (x, -2, 0)) - (-4*a + 8)) == 0 and sp.expand(sp.integrate(Q, (x, 0, 2)) - (4*a + 8)) == 0 \
    and sp.expand(sp.integrate(Q, (x, 2, 4)) - (60*a + 56)) == 0
ex = {tv: extrema(av, tv) for tv, av in cands.items()}
assert ex[-2] == [(-4, 'max'), (-1, 'min')]
assert ex[0] == [(1, 'max')]
assert ex[2] == [(0, 'max'), (R(4, 3), 'min'), (3, 'max')]
ok = [tv for tv in TS if not any(k == 'min' for _, k in ex[tv])]
assert ok == [0]
T0, A0 = 0, cands[0]
# 해설의 인수분해
assert sp.expand(P.subs(a, 3) - 3*x*(x + 4)) == 0 and sp.expand(Q.subs(a, 3) - 3*x**2*(x + 1)) == 0
assert sp.expand(P.subs(a, -3) - 3*x*(x - 4)) == 0 and sp.expand(Q.subs(a, -3) - 3*x**2*(1 - x)) == 0
assert sp.expand(P.subs(a, -1) - x*(3*x - 4)) == 0 and sp.expand(Q.subs(a, -1) - x**2*(3 - x)) == 0
print('후보 (t, a) = (-2, 3), (0, -3), (2, -1) / 극값: t=-2 → 극대 -4·극소 -1, t=0 → 극대 1뿐, t=2 → 극대 0·극소 4/3·극대 3 → t=0, a=-3만 OK')
# 남은 함수가 실제로 미분가능한지(정의대로: 좌·우 미분계수)와 f(2)=10으로 정한 함숫값
h = sp.symbols('h', positive=True)
fL = sp.integrate(P.subs(a, A0), x); fR = sp.integrate(Q.subs(a, A0), x)
kR = C2 - fR.subs(x, 2); kL = fR.subs(x, T0) + kR - fL.subs(x, T0)           # x=t에서 연속, f(2)=10
fl = fL + kL; fr = fR + kR
dl = sp.limit((fl.subs(x, T0 - h) - fr.subs(x, T0)) / (-h), h, 0); dr = sp.limit((fr.subs(x, T0 + h) - fr.subs(x, T0)) / h, h, 0)
assert dl == dr == 0 and fr.subs(x, 2) == C2 and fr.subs(x, T0 + 2) - fr.subs(x, T0) == VAL
ans = fl.subs(x, T0 - 1)
assert ans == C2 - diff_f(A0, T0, T0 - 1, 2) == 7 and CH[it['ans'] - 1] == ans
assert fr.subs(x, 0) == 14 and sp.integrate(P.subs(a, A0), (x, -1, 0)) == 7
print(f't={T0}, a={A0}: f(0)=14, f(0)-f(-1)=7, f(t-1)=f(-1)={ans} OK')

# ---------- 선지 · 오답 ----------
assert len(set(CH)) == 5 and {CH[i + 1] - CH[i] for i in range(4)} == {2}        # 오름차순, 공차 2
fval = lambda av, tv: C2 - diff_f(av, tv, tv - 1, 2)
w1 = fval(cands[-2], -2)                                                # 5: t=-2 갈래
w2 = fval(cands[2], 2)                                                  # 9: t=2 갈래
assert sp.integrate(P.subs(a, 3), (x, -3, -2)) == -11 and sp.integrate(Q.subs(a, 3), (x, -2, 2)) == 16 and sp.integrate(P.subs(a, -1), (x, 1, 2)) == 1
# 11: f(t+2)-f(t)를 거꾸로 적분 → t=0에서 a=-1(극솟값 없음), f(0)=14, f(-1)=14-∫_{-1}^0(3x^2-4x)
ar = sp.solve(sp.Eq(sp.integrate(Q, (x, 2, 0)), VAL), a)[0]
assert ar == -1 and not any(k == 'min' for _, k in extrema(ar, 0))
w3 = (C2 - VAL) - sp.integrate(P.subs(a, ar), (x, -1, 0))
# 3: a=-3은 맞으나 f(2)→f(0)의 -4를 빼먹음
w4 = C2 - sp.integrate(P.subs(a, A0), (x, -1, 0))
assert [w1, w2, w3, w4] == [5, 9, 11, 3] == [int(v) for v in it['wrongs']]
for w in it['wrongs']: assert sp.Integer(w) in CH and sp.Integer(w) != ans
assert set(CH) == {ans, w1, w2, w3, w4}
# t로 나누면 t=±2뿐, 둘 다 극소가 있어 답 없음 / 범위를 보지 않고 근만 보면 세 갈래 모두 '극소'
assert all(any(k == 'min' for _, k in ex[tv]) for tv in (-2, 2))
def formal_min(av):                                                    # 범위를 무시: 이차 조각의 큰 근에서 음→양
    return max(sp.real_roots(sp.Poly(P.subs(a, av), x)))
assert formal_min(A0) == 4 and not (4 < T0)
nums = {int(n) for n in re.findall(r'-?\d+', re.sub(r'\\[a-zA-Z]+|&[a-z]+;|<[^>]+>|\^\d', ' ', full))}
assert nums == {3, 4, 2, -4, 10, -1}, nums
assert ans not in nums and -ans not in nums
print('정답이 본문의 수와 같지 않음 OK')
print('정답 = ③ 7, 선지 등차(공차 2, 오름차순), 오답 5(t=-2 갈래)·9(t=2 갈래)·11(차를 거꾸로 적분해 a=-1)·3(f(2)→f(0)의 -4 누락) 선지 안 OK')

# ---------- 조건 빼 보기 ----------
vals3 = sorted(fval(cands[tv], tv) for tv in TS)
assert vals3 == [5, 7, 9]
print("ABLATION 18 극솟값을 갖지 않는다: 필요(빼면 f(t-1)이 5, 7, 9의 셋)")
# f(t+2)-f(t)=-4: 빼면 t=0에서 음수 a가 모두 됨
free = [(av, C2 - piece_int(av, 0, -1, 2)) for av in (R(-1), R(-2), R(-5))]
assert all(not any(k == 'min' for _, k in extrema(av, 0)) for av, _ in free) and len({v for _, v in free}) == 3
print(f"ABLATION 18 f(t+2)-f(t)=-4: 필요(빼면 t=0, a={[str(v) for v, _ in free]}가 모두 되어 f(2)-f(-1)이 {[str(C2 - v) for _, v in free]})")
# 값 -4: 다른 값이면 답이 달라짐
alt = {}
for V2 in (-12, -8):
    got = []
    for tv in TS:
        av = sp.solve(sp.Eq(sp.integrate(Q, (x, tv, tv + 2)), V2), a)[0]
        if av != 0 and not any(k == 'min' for _, k in extrema(av, tv)): got.append(fval(av, tv))
    alt[V2] = got
assert all(v and v != [ans] for v in alt.values())
print(f"ABLATION 18 값 -4: 필요(바꾸면 {alt})")
# 미분가능(연결 조건): 빼면 예컨대 t=-1/2, a=-6도 극솟값이 없고 값이 다름
tv = R(-1, 2); av = sp.solve(sp.Eq(sp.integrate(Q, (x, tv, tv + 2)), VAL), a)[0]
assert av == -6 and not any(k == 'min' for _, k in extrema(av, tv)) and fval(av, tv) != ans
print(f"ABLATION 18 미분가능: 필요(연결 조건이 없으면 t=-1/2, a=-6도 조건에 맞고 값 {fval(av, tv)})")
print("ABLATION 18 f(2)=10: 필요(함숫값의 기준. 없으면 f(t-1)이 정해지지 않음)")
# 계수 a(조각의 계수): 원문처럼 수로 두면(a=-4 고정에 해당하는 꼴) 조건 -4와 맞는 경계가 없음
assert all(sp.integrate(Q.subs(a, av), (x, tv, tv + 2)) != VAL for tv in TS for av in (-4, 4))
print("ABLATION 18 계수 a: 필요(a를 수 ±4로 두면 세 경계 모두 f(t+2)-f(t)≠-4)")

# ---------- 같은 갈래를 고르는 다른 조건(겹침을 피해야 할 때의 대안): f'(x)=0의 서로 다른 실근의 개수 2 ----------
cnt = {tv: len(roots_in_range(cands[tv], tv)) for tv in TS}
assert cnt == {-2: 3, 0: 2, 2: 3}
print("대안 조건 'f'(x)=0의 서로 다른 실근의 개수가 2': t=-2 → 3개, t=0 → 2개, t=2 → 3개(같은 갈래만 남음)")

# ---------- 원문 설정 줄 시험(②형: 불통이어야 함) ----------
# 원문 줄: 경계와 조각이 수로 주어져 나누어 적분만 하면 된다. 변형은 경계 t와 계수 a가 문자라 적분할 구간이 정해지지 않고,
# 원문처럼 경계를 0이 아닌 대칭인 두 수(±2)로 보면 두 갈래 모두 극소가 있어 답에 닿지 못한다
assert sp.integrate(Q, (x, t, t + 2)).has(a) and sp.integrate(Q, (x, t, t + 2)).has(t)
assert [tv for tv in (-2, 2) if not any(k == 'min' for _, k in ex[tv])] == []
print('원문 설정 줄(주어진 경계에서 나누어 적분): 경계·계수가 문자라 적분 불가 · 경계를 ±2로만 보면 조건에 맞는 갈래 없음(불통) OK')

# ---------- 문장 길이 ----------
def plain(s): return html.unescape(re.sub(r'<[^>]+>', '', s))
Lo = len(plain(F.I['I41'][0])); Lm = len(plain(full))
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자')
assert Lm >= Lo, (Lo, Lm)

# ---------- 원문 · 인쇄 N제 골격 ----------
import dupcheck as DC
sk = lambda s_: set(DC.shingles(DC.skel(DC.norm(s_))))
A_ = sk(full); B2 = sk(F.I['I41'][0])
jd = len(A_ & B2) / len(A_ | B2)
print(f'원문 골격 유사도 {jd:.2f} (관문 0.60 미만)')
assert jd < 0.60
md = open('/home/user/Finale/output/N제/미적분1_기말_N제_06_부정적분과정적분.md').read()
sec = md.split('## I41 (부교재', 1)[1].split('\n## ', 1)[0]
nje = re.findall(r'\*\*(2\d\d)\.\*\*(.*?)(?=\n\n\*\*2\d\d\.\*\*|\Z)', sec, re.S)
assert [n for n, _ in nje] == ['281', '282', '283', '284', '285', '286'], [n for n, _ in nje]
for n, body in nje:
    C_ = sk(body); j2 = len(A_ & C_) / len(A_ | C_)
    print(f'  N제 {n}: 골격 {j2:.2f}')
    assert j2 < 0.60, (n, j2)
    assert 'x<t' not in body and '극솟값을 갖지' not in body and 'f(t' not in body
print('인쇄 N제 I41(281–286): 골격 0.60 미만, 한쪽 경계 x<t·극솟값을 갖지 않는 조건·f(t-1) 없음 OK')
print('ALL OK')
