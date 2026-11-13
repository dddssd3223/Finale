# -*- coding: utf-8 -*-
# 17번 후보 A17 (I44 킬러 설계A: 곡선 y=|f(x)-x-m|과 직선 y=t의 교점 개수 h(t), 불연속점 2개인 m의 합 → ∫_{-1}^1 f) 검증 · author='claude'
import sympy as sp, os, sys, re, html
x, C, m, t, a = sp.symbols('x C m t a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def nroots(poly):
    """실근 개수(서로 다른 것)"""
    return len(set(sp.real_roots(sp.Poly(sp.expand(poly), x))))


def count(F, mv, tv):
    """곡선 y=|F(x)-mv| 와 직선 y=tv 의 교점 개수"""
    if tv < 0: return 0
    if tv == 0: return nroots(F - mv)
    s1 = set(sp.real_roots(sp.Poly(sp.expand(F - mv - tv), x)))
    s2 = set(sp.real_roots(sp.Poly(sp.expand(F - mv + tv), x)))
    return len(s1 | s2)


def crit_vals(F):
    cps = sp.solve(sp.diff(F, x), x)
    return sorted({sp.nsimplify(F.subs(x, c)) for c in cps if c.is_real})


def discont(F, mv):
    """h(t) 가 불연속인 t 들. 후보는 0 과 |극값 - m| (그 밖에서는 h 가 국소 상수). 각 후보에서 좌우값과 함숫값 비교"""
    cand = sorted({sp.Integer(0)} | {sp.Abs(v - mv) for v in crit_vals(F)})
    cand = [c for c in cand if c >= 0]
    pts = sorted(set(cand))
    out = []
    for i, c in enumerate(pts):
        lo = (pts[i - 1] + c) / 2 if i > 0 else c - 1
        hi = (pts[i + 1] + c) / 2 if i + 1 < len(pts) else c + 1
        if not (count(F, mv, lo) == count(F, mv, c) == count(F, mv, hi)): out.append(c)
    return out


# ---------- 1) (가)에서 F = f - x
f = x**3 + sp.Symbol('p') * x**2 + sp.Symbol('q') * x + sp.Symbol('r')
p_, q_ = sp.Symbol('p'), sp.Symbol('q')
sol = sp.solve([sp.diff(f, x).subs(x, -1) - 1, sp.diff(f, x).subs(x, 3) - 1], [p_, q_], dict=True)
assert sol == [{p_: -3, q_: -8}], sol
Fsym = x**3 - 3 * x**2 - 9 * x + C
assert sp.expand(f.subs(sol[0]) - x - Fsym.subs(C, sp.Symbol('r'))) == 0
assert sp.expand(sp.diff(Fsym, x) - 3 * (x - 3) * (x + 1)) == 0
assert Fsym.subs(x, -1) - C == 5 and Fsym.subs(x, 3) - C == -27 and Fsym.subs(x, 1) - C == -11
assert sp.expand(Fsym.subs(x, 1 + a) + Fsym.subs(x, 1 - a) - 2 * Fsym.subs(x, 1)) == 0      # 점 (1, C-11) 대칭
print('(가): f = x^3-3x^2-8x+C, F=f-x = x^3-3x^2-9x+C, 극댓값 C+5, 극솟값 C-27, 중심 (1, C-11)')

# ---------- 2) m 전수: 불연속점 2개인 m 은 C-27, C-11, C+5 뿐 (C 에 대해 평행이동이므로 C=0 에서 m 을 조사하면 충분)
F0 = x**3 - 3 * x**2 - 9 * x
good = []
test_m = [R(k, 2) for k in range(-90, 41)] + [R(-11), R(-27), R(5), R(-11) + R(1, 1000), R(-11) - R(1, 1000), R(5) + R(1, 1000), R(-27) - R(1, 1000), 100, -100]
for mv in sorted(set(test_m)):
    d = discont(F0, mv)
    if len(d) == 2: good.append(mv)
    else: assert len(d) == 3, (mv, d)
assert good == [-27, -11, 5], good
assert discont(F0, -27) == [0, 32] and discont(F0, 5) == [0, 32] and discont(F0, -11) == [0, 16]
assert discont(F0, 0) == [0, 5, 27] and discont(F0, 20) == [0, 15, 47] and discont(F0, -40) == [0, 13, 45]
print('m 전수(C=0, 반정수 -45..20 + 경계 근방 + ±100): 불연속점 2개 ⇔ m ∈ {-27, -11, 5} ({0,32},{0,16},{0,32}), 나머지 3개')
# 해석적 확인: 두 높이 |5-m|, |m+27| 중 0 이 있거나 같을 때만 2개
mm = sp.symbols('mm', real=True)
assert set(sp.solve(sp.Eq((5 - mm)**2, (mm + 27)**2), mm)) == {-11}

# ---------- 3) (나): 합 3C-33 = 6 → C = 13, 답
Csol = sp.solve(sp.Eq(3 * C - 33, 6), C); assert Csol == [13]
fF = x**3 - 3 * x**2 - 8 * x + 13
assert sp.diff(fF, x).subs(x, -1) == 1 and sp.diff(fF, x).subs(x, 3) == 1
Fn = fF - x
gd = [mv for mv in [-14, 2, 18, 0, 1, 3, 10, -20, 30] if len(discont(Fn, mv)) == 2]
assert gd == [-14, 2, 18] and sum(gd) == 6
ANS = sp.integrate(fF, (x, -1, 1)); assert ANS == 24
assert sp.integrate(Fsym + x, (x, -1, 1)) == 2 * C - 2
print(f'(나): m = -14, 2, 18 의 합 6 → C=13, f=x^3-3x^2-8x+13, ∫_-1^1 f = {ANS}')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {2}
print('정답 24 = 선지 ①, 선지 24..32 공차 2 오름차순')

# ---------- 4) 오답 근거
w26a = 2 * sp.solve(sp.Eq(2 * C - 22, 6), C)[0] - 2          # 중심 m 놓침
w26b = 2 * 13                                                 # -2 빠뜨림
w32 = 2 * sp.solve(sp.Eq(C - 11, 6), C)[0] - 2               # 극값 m 놓침
w28 = 2 * 13 + 2                                              # 부호 실수
assert (w26a, w26b, w32, w28) == (26, 26, 32, 28)
assert all(v in ch for v in IT['wrongs']) and IT['wrongs'] == ['26', '32']
print('오답 근거 OK: 26(m=C-11 놓침 / -2 빠뜨림) · 32(m=C±… 극값 놓침) · 28(부호 실수)')

# ---------- 5) 원문 I44 직접 풀기: 52
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I44']
assert o[2] == '④' and o[1][3] == '52'
pp, qq, rr = sp.symbols('pp qq rr')
g = x**3 + pp * x**2 + qq * x + rr
eqs = sp.Poly(sp.expand(g.subs(x, -a) + g.subs(x, a + 2) - 2 * g.subs(x, 1)), a).coeffs()
s0 = sp.solve(list(eqs) + [sp.diff(g, x).subs(x, -1)], [pp, qq], dict=True)
assert s0 == [{pp: -3, qq: -9}], s0
g0 = g.subs(s0[0])
# g(t)=|g0-t| 미분불가능점 개수: 단순근(홀수 중복도) 개수. 극값이 0, p(>0) 에서만 불연속 → 극솟값 rr-27=0
def nondiff(G, tv):
    from collections import Counter
    rts = Counter(sp.real_roots(sp.Poly(sp.expand(G - tv), x)))
    return sum(1 for k in rts.values() if k % 2 == 1)
G27 = g0.subs(rr, 27)
assert [nondiff(G27, tv) for tv in (-1, 0, 1, 16, 32, 33)] == [1, 1, 3, 3, 1, 1]
assert sp.integrate(G27, (x, -1, 1)) == 52
# 다른 rr 이면 불연속점이 0 이 아니게 됨 (극값 rr+5, rr-27 둘 다 0 이 아니거나 p<0)
assert sp.solve(sp.Eq(rr - 27, 0), rr) == [27] and (rr + 5).subs(rr, 27) == 32
print('원문 I44 OK: f=x^3-3x^2-9x+27, 불연속점 0, 32, ∫_-1^1 f = 52 (원문 정답 ④ 52)')

# ---------- 6) 핵심 한 줄 (②형: 원문 설정 줄 불통)
body = IT['body'] + ''.join(c for _, c in IT['cond'])
assert 'int_1^{-a}' not in body and "f'(-1)=0" not in body and '미분가능' not in body
# 원문 설정 줄(f'(-1)=0 → f=x^3-3x^2-9x+C)을 f 에 그대로 쓰면 (가)와 모순
assert sp.diff(x**3 - 3 * x**2 - 9 * x, x).subs(x, -1) != 1
# 원문 원리 줄('극값이 0')만 쓰면 m 두 개(C-27, C+5)만 → 합 2C-22, 답 26 (오답)
print('핵심 한 줄: 설정 줄(적분 점대칭·f\'(-1)=0) 불통, 원리 줄(극값 높이)만으로는 중심 m 을 놓침')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
out = []
def ablation(cname, res, why=''):
    msg = (f'군더더기(답 그대로{"; " + why if why else ""})' if res == ANS else f'필요({res}{"; " + why if why else ""})')
    print(f'ABLATION 17 {cname}: {msg}'); out.append(msg)

# (가) 중 x=3 의 기울기 조건 빼기: f'(-1)=1 만 → F=x^3+bx^2+(2b-3)x+C 로 b 가 남음
b = sp.Symbol('b')
Fb = x**3 + b * x**2 + (2 * b - 3) * x + C
assert sp.diff(Fb, x).subs(x, -1) == 0
vals = set()
for bv in (-3, 0):
    Fv = Fb.subs({b: bv, C: 0})
    cv = crit_vals(Fv); assert len(cv) == 2
    s = sum(cv) + (cv[0] + cv[1]) / 2                              # 세 m 의 합(C=0) — 중심 높이는 두 극값의 평균
    cc = sp.solve(sp.Eq(3 * C + s, 6), C)[0]
    vals.add(sp.integrate((Fv + C + x).subs(C, cc), (x, -1, 1)))
assert len(vals) == 2
ablation("(가)의 점 (3, f(3)) 기울기", f'정해지지 않음({sorted(vals)})', 'b 가 남음')
# (가) 중 x=-1 빼기도 같은 이유
Fb3 = x**3 + b * x**2 + (-27 - 6 * b) * x + C                     # F'(3)=0 만
assert sp.diff(Fb3, x).subs(x, 3) == 0
vals3 = set()
for bv in (-3, 0):
    Fv = Fb3.subs({b: bv, C: 0}); cv = crit_vals(Fv); assert len(cv) == 2
    cc = sp.solve(sp.Eq(3 * C + sum(cv) + (cv[0] + cv[1]) / 2, 6), C)[0]
    vals3.add(sp.nsimplify(sp.integrate((Fv + C + x).subs(C, cc), (x, -1, 1))))
assert len(vals3) == 2
ablation("(가)의 점 (-1, f(-1)) 기울기", f'정해지지 않음({sorted(vals3)})', 'b 가 남음')
# (가)의 기울기 1 → 0 (원문처럼 기준선을 y=m 으로 본 경우): f'(-1)=f'(3)=0 → f=x^3-3x^2-9x+C, 기준선 y=x+m 이면 F=f-x 극점 무리수
F_alt = x**3 - 3 * x**2 - 10 * x
cps = sp.solve(sp.diff(F_alt, x), x); assert all(not c.is_rational for c in cps)
cv = crit_vals(F_alt); s = sum(cv) + (cv[0] + cv[1]) / 2
c_alt = sp.solve(sp.Eq(3 * C + s, 6), C)[0]
v_alt = sp.nsimplify(sp.integrate(F_alt + x + c_alt, (x, -1, 1)))
assert v_alt != ANS
ablation('(가)의 기울기 1(→ 0)', v_alt, '기준선 y=x+m 과 짝이 맞아야 F 의 극점이 -1, 3')
# (나) 합 6 빼기: C 가 정해지지 않음
ablation('(나)의 합 6', '정해지지 않음(C 자유)', '∫=2C-2')
# (나) '개수가 2' → '개수가 3': m 이 무수히 많아 합이 정의되지 않음
assert len(discont(F0, 0)) == 3 and len(discont(F0, 1)) == 3
ablation("(나)의 '개수가 2'(→ 3)", '정해지지 않음(m 무수히 많음)', '')
# 기준선의 -x 빼기: y=|f(x)-m| 이면 f 의 극점이 무리수, 답이 달라짐
F_nox = x**3 - 3 * x**2 - 8 * x
cv = crit_vals(F_nox); s = sum(cv) + (cv[0] + cv[1]) / 2
c_nox = sp.solve(sp.Eq(3 * C + s, 6), C)[0]
v_nox = sp.nsimplify(sp.integrate(F_nox + c_nox, (x, -1, 1)))
assert v_nox != ANS
ablation('기준선의 -x(→ y=|f(x)-m|)', v_nox, '')
# '최고차항의 계수가 1' 빼기: F=a(x^3-3x^2-9x)+C → ∫ 은 a 에 따라 달라짐
aa = sp.Symbol('aa', positive=True)
Fa = aa * (x**3 - 3 * x**2 - 9 * x) + C                           # 극댓값 5aa+C, 극솟값 -27aa+C, 중심 -11aa+C → 합 3C-33aa
ca = sp.solve(sp.Eq(3 * C - 33 * aa, 6), C)[0]
Ia = sp.simplify(sp.integrate(Fa.subs(C, ca) + x, (x, -1, 1)))
assert Ia.subs(aa, 1) == 24 and Ia.subs(aa, 2) != 24
ablation("'최고차항의 계수가 1'", f'정해지지 않음({Ia})', '')
assert all(r_.startswith('필요') for r_ in out), out

# ---------- 형식·기록
plain = lambda s_: re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html.unescape(s_)))
L, L0 = len(plain(body)), len(plain(o[0]))
assert L >= 0.9 * L0, (L, L0)
assert IT['key'] == 'I44' and IT['cand'] == 'A17' and IT['db_ref'] == 'I44 킬러 설계A' and IT['level'] == '상'
assert IT['core']['axis'] == '②' and set(IT['core']) == {'axis', 'setting', 'principle', 'new'}
assert '함정 추가' not in IT['vtype'] and IT['bunseok'] is False
assert {'OP12', 'OP11'} <= set(IT['ops']) and '\\[' not in IT['body'] and '?' in IT['body']
print(f'문장 길이 {L}자 (원문 {L0}자, 하한 90% {0.9 * L0:.0f}자) · 상자 (가)(나) · 줄 바꾼 식 없음')
print('ALL OK')
