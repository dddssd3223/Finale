# -*- coding: utf-8 -*-
# 서답형1 (자체, D11 유형) · 서답형2 (I71 학교식, 보기 벗기기 단계화) 검증 · author='claude'
import sympy as sp, os, sys, re
x, t, a, c = sp.symbols('x t a c', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def increasing_everywhere(fx):
    """다항함수가 실수 전체에서 증가 ⇔ f'≥0 (f'≡0 아님, 다항식이라 0은 고립점)"""
    P = sp.Poly(sp.diff(fx, x), x)
    rts = sorted(set(P.real_roots()))
    pts = [rts[0] - 1] + [(rts[i] + rts[i + 1]) / 2 for i in range(len(rts) - 1)] + [rts[-1] + 1] if rts else [0]
    return all(P.eval(p) > 0 for p in pts)

# ================= S1 =================
# --- 원문 D11
fo = x**3 + a * x**2 + (2 * a + R(7, 3)) * x - 5
cnt = [av for av in range(-30, 31) if increasing_everywhere(fo.subs(a, av))]
assert cnt == list(range(-1, 8)) and len(cnt) == 9 and F.I['D11'][2] == '④' and F.I['D11'][1][3] == '9'
print('D11 원문 OK: 정수 a = -1..7, 9개 (원문 정답 ④)')

# --- S1
assert r"f(x)=x^3-3ax^2+3(a+2)x-3" in S1['body']
f1 = x**3 - 3 * a * x**2 + 3 * (a + 2) * x - 3
fp1 = sp.diff(f1, x)
D4 = sp.factor(sp.discriminant(sp.expand(fp1 / 3), x) / 4); assert sp.expand(D4 - (a + 1) * (a - 2)) == 0
# (1) a 격자(1/16 간격) 전수: 증가 ⇔ -1≤a≤2
grid = [R(i, 16) for i in range(-96, 97)]
good = [av for av in grid if increasing_everywhere(f1.subs(a, av))]
assert good == [av for av in grid if -1 <= av <= 2]
assert increasing_everywhere(f1.subs(a, -1)) and increasing_everywhere(f1.subs(a, 2))
# (2) 증가 + 수평 접선(f'(p)=0인 실수 p 존재)
lines = set()
for av in grid:
    g = f1.subs(a, av)
    if not increasing_everywhere(g): continue
    for p in sp.Poly(sp.diff(g, x), x).real_roots():
        lines.add(g.subs(x, p))
assert lines == {-4, 5}, lines
assert sp.factor(sp.diff(f1.subs(a, -1), x)) == 3 * (x + 1)**2 and f1.subs(a, -1).subs(x, -1) == -4
assert sp.factor(sp.diff(f1.subs(a, 2), x)) == 3 * (x - 2)**2 and f1.subs(a, 2).subs(x, 2) == 5
assert S1['ans'] == [r'(1) \(-1\le a\le2\)', r'(2) \(y=-4\), \(y=5\)']
# 오답 값
wr = sp.solve(a**2 - 3 * (a + 2), a); assert set(wr) == {R(3, 2) - sp.sqrt(33) / 2, R(3, 2) + sp.sqrt(33) / 2}
for w in (r'-1&lt;a&lt;2', r'\sqrt{33}', r'y=-1\), \(y=2', r'\(y=5\)(또는'): assert w in S1['wrong'], w
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D11)'
print('S1 OK: (1) -1≤a≤2 (2) y=-4, y=5 (a 격자 1/16 간격 [-6, 6] 전수)')

def abl1(cn, m): print(f'ABLATION S1 {cn}: {m}')
# (2)의 '실수 전체에서 증가' 삭제: 수평 접선이 무수히 많음
many = set()
for av in (-3, -2, 3, 4):
    g = f1.subs(a, av)
    for p in sp.Poly(sp.diff(g, x), x).real_roots(): many.add(g.subs(x, p))
assert len(many) >= 8
abl1("(2)의 '실수 전체에서 증가'", '필요(없으면 a<-1, a>2에서도 기울기 0인 접선이 생겨 접선이 무수히 많음)')
# (2)의 'x축과 평행' 삭제: 증가하는 모든 a의 모든 접선 → 정해지지 않음
abl1("(2)의 '기울기가 0인'", '필요(없으면 증가하는 모든 a의 모든 접선이 되어 직선이 정해지지 않음)')


# ================= S2 =================
def setup(r1, L):
    """f=x(x-r1)(x-c), g(t)=∫_t^{t+L} f - ∫_0^{r1}|f| 를 c의 구간별 식으로"""
    f = x * (x - r1) * (x - c)
    G = sp.integrate(f, (x, t, t + L))
    I = sp.integrate(f, (x, 0, r1))
    A = {'lo': -I, 'hi': I, 'mid': sp.integrate(f, (x, 0, c)) - sp.integrate(f, (x, c, r1))}
    return f, G, A

def absint_num(fc, lo, hi):
    """∫_lo^hi |fc| (c 대입된 다항식) 정확값"""
    rts = sorted(r for r in set(sp.Poly(fc, x).real_roots()) if lo < r < hi)
    cuts = [lo] + rts + [hi]
    return sum(abs(sp.integrate(fc, (x, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))

def gval(r1, L, cv, tv):
    fc = sp.expand(x * (x - r1) * (x - cv))
    return sp.integrate(fc, (x, tv, tv + L)) - absint_num(fc, 0, r1)

# --- 원문 I71: ㄱ·ㄴ·ㄷ 모두 참 → ⑤
cg = [R(i, 8) for i in range(-60, 41)]
for cv in cg:
    g0, gm1 = gval(1, 1, cv, 0), gval(1, 1, cv, -1)
    if g0 == 0: assert gm1 < 0                                    # ㄱ
    if gm1 > 0: assert cv < -1                                    # ㄴ (셋째 근 c<-1)
    if gm1 > 1: assert g0 < -1                                    # ㄷ
assert F.I['I71'][2] == '⑤' and F.I['I71'][1][4] == 'T:ㄱ, ㄴ, ㄷ'
print('I71 원문 OK: ㄱ·ㄴ·ㄷ 모두 참 (c 격자 1/8 간격 전수, 원문 정답 ⑤)')

# --- S2
assert r"f(0)=f(2)=0" in S2['body'] and r"\int_t^{t+2}f(x)\,dx-\int_0^2|f(x)|\,dx" in S2['body'] and 'cond' not in S2
f2, G2, A2 = setup(2, 2)
g2 = {k: sp.factor(G2 - v) for k, v in A2.items()}
assert sp.factor(g2['lo'].subs(t, -2)) == sp.factor(-16 * (c + 2) / 3)
assert sp.factor(g2['lo'].subs(t, -1)) == sp.factor(2 * (c - 4) / 3)
assert sp.factor(g2['hi'].subs(t, -1)) == -2 * c and sp.factor(g2['hi'].subs(t, 0)) == 0
# 식 점검: 구간별 식과 실제 |f| 적분 일치
for cv in (R(-7), R(-5), R(-2), R(-1, 3), R(0), R(1, 2), R(1), R(3, 2), R(2), R(3), R(5)):
    key = 'lo' if cv <= 0 else ('hi' if cv >= 2 else 'mid')
    for tv in (-2, -1, 0, 1):
        assert sp.simplify(g2[key].subs({c: cv, t: tv}) - gval(2, 2, cv, tv)) == 0
CG = [R(i, 8) for i in range(-120, 81)]           # c 격자 [-15, 10]
# (1) g(0)=0 ⇔ c≥2, f(-1) 최댓값 -9 (c=2)
z = [cv for cv in CG if gval(2, 2, cv, 0) == 0]; assert z == [cv for cv in CG if cv >= 2]
fm1 = [f2.subs({c: cv, x: -1}) for cv in z]; assert max(fm1) == -9 and f2.subs({c: 2, x: -1}) == -9
assert sp.expand(f2.subs(x, -1) + 3 * (c + 1)) == 0                          # f(-1)=-3(c+1) 감소 → c=2에서 최대
# (2) f(1)=-3 ⇒ c=-2 하나, g(0)=-8
c2 = sp.solve(sp.Eq(f2.subs(x, 1), -3), c); assert c2 == [-2]
assert gval(2, 2, -2, 0) == -8
# (3) g(-2)>0 이고 g(-1)=-6: 세 구간 식 모두에서 해를 구해 전수
cands = []
for key, cond in (('lo', lambda v: v <= 0), ('hi', lambda v: v >= 2), ('mid', lambda v: 0 < v < 2)):
    for s in sp.solve(sp.Eq(g2[key].subs(t, -1), -6), c):
        if s.is_real and cond(s): cands.append(s)
assert sorted(cands) == [-5, 3], cands                # g(-1)=-6 만으로는 후보 둘
assert gval(2, 2, -5, -2) == 16 and gval(2, 2, 3, -2) == -32
sel = [cv for cv in cands if gval(2, 2, cv, -2) > 0]; assert sel == [-5]
# mid 구간 (0,2)에서 g(-1)=-6의 실근 없음: 다항식 근 확인
mid_eq = sp.Poly(sp.expand(6 * (g2['mid'].subs(t, -1) + 6)), c)
assert not [r for r in mid_eq.real_roots() if 0 < r < 2]
# g(-2)>0 ⇔ c<-2 (격자) — c≥0이면 늘 음수
assert [cv for cv in CG if gval(2, 2, cv, -2) > 0] == [cv for cv in CG if cv < -2]
F4 = f2.subs({c: -5, x: 4}); assert F4 == 72
assert S2['ans'] == [r'(1) \(-9\)', r'(2) \(-8\)', r'(3) \(72\)']
print('S2 OK: (1) -9 (2) -8 (3) c=-5, f(4)=72 (c 세 구간 식 전수 + 격자 1/8 간격 확인)')
# 정답이 본문 수와 같지 않음
txt = S2['body'] + ''.join(q[0] for q in S2['subs'])
nums = set(re.findall(r'-?\d+', txt))
for v in ('-9', '-8', '72'): assert v not in nums, v
# 오답 값
assert f2.subs({c: 3, x: 4}) == 8 and f2.subs({c: 5, x: 4}) == -8           # (3) 절댓값 무시 c=3 · 부호 실수
assert sp.integrate(f2.subs(c, -2), (x, 0, 2)) == -4                           # (2) ∫f만
assert -3 * (-(2 + 1)) == 9                                                     # (1) 부호 실수
for w in (r'\(9\)', r'\(g(0)=0\)', r'=-4\)만', r'\(f(4)=8\)', r'\(f(4)=-8\)'): assert w in S2['wrong'], w
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['2점, 답만 적으시오.', '3점, 답만 적으시오.', '5점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S2['rubric'][:3]]
assert pts2 == [[2], [3], [5]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line_ for line_ in S2['rubric'][:3])
assert S2['db_ref'] == 'I71 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
for it in (S1, S2):
    tx = it['body'] + ''.join(q[0] for q in it['subs'])
    assert '이러한' not in tx and '이와 같은' not in tx
    assert not [m for m in re.findall(r'\\\(.*?\\\)', tx) if '<' in m or '>' in m]
print('S2 형식 OK')

def abl2(cn, m): print(f'ABLATION S2 {cn}: {m}')
# (a) (3)의 g(-2)>0 삭제 → c=-5, 3 두 후보, f(4)=72, 8
abl2('(3)의 g(-2)>0', f'필요(없으면 c=-5, 3이 모두 맞아 f(4)가 72, {f2.subs({c: 3, x: 4})}로 정해지지 않음)')
# (b) (3)의 g(-1)=-6 삭제 → c<-2 인 모든 c
abl2('(3)의 g(-1)=-6', '필요(없으면 c<-2인 모든 c가 되어 f(4)가 정해지지 않음)')
# (c) (1)의 g(0)=0 삭제 → f(-1)=-3(c+1) 위로 유계 아님
assert f2.subs({c: -100, x: -1}) == 297
abl2('(1)의 g(0)=0', '필요(없으면 c→-∞에서 f(-1)이 한없이 커져 최댓값이 없음)')
# (d) (2)의 f(1)=-3 삭제 → g(0)이 c마다 다름
assert gval(2, 2, -1, 0) != gval(2, 2, -2, 0)
abl2('(2)의 f(1)=-3', '필요(없으면 g(0)이 c에 따라 달라짐)')
# (e) 최고차항의 계수 1 삭제: f=px(x-2)(x-c), (3)에서 p=2이면 다른 c
p_ = sp.symbols('p', positive=True)
sol_p = sp.solve([sp.Eq(p_ * g2['lo'].subs(t, -1), -6)], c, dict=True)
assert sol_p and sp.simplify(sol_p[0][c].subs(p_, 2)) != -5
abl2('최고차항의 계수 1', f'필요(계수 p이면 (3)의 c={sp.simplify(sol_p[0][c])}로 p마다 달라짐)')
# (f) f(2)=0 → f(1)=0(원문): 정의식 구간과 근이 어긋나면 (1)의 c 범위가 바뀜
f_alt = x * (x - 1) * (x - c)
assert sp.integrate(f_alt.subs(c, R(3, 2)), (x, 0, 2)) != absint_num(sp.expand(f_alt.subs(c, R(3, 2))), 0, 2)
abl2('f(2)=0(근 2)', '필요(근이 1이면 [0, 2]에서 f가 부호를 바꿔 (1)의 g(0)=0 조건이 c≥2가 아니게 됨)')

print('ALL OK')
