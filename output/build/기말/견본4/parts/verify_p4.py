# -*- coding: utf-8 -*-
# 서답형2 (D65 구조 변경) 검증 · author='claude'
import sympy as sp, mpmath as mp, os
mp.mp.dps = 60
x, t, k = sp.symbols('x t k', real=True)
A, B, C, D, a, b = sp.symbols('A B C D a b', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py')).read(), ns)
S = ns['SITEMS']['S2']


# ---------- 도구 ----------
def nreal(expr):
    """다항식 expr(x)의 서로 다른 실근의 개수 (유리계수는 정확히, 아니면 고정밀 수치)"""
    P = sp.Poly(sp.expand(expr), x)
    if P.degree() <= 0:
        return 0 if P.as_expr() != 0 else sp.oo
    if P.domain.is_QQ or P.domain.is_ZZ:
        return sp.Poly(sp.sqf_part(P.as_expr()), x).count_roots()
    rs = mp.polyroots([mp.mpf(str(sp.N(c, 80))) for c in P.all_coeffs()], maxsteps=400, extraprec=400)
    re_ = sorted(float(mp.re(r)) for r in rs if abs(mp.im(r)) < 1e-15)
    out = []
    for r in re_:
        if not out or abs(r - out[-1]) > 1e-12: out.append(r)
    return len(out)

def real_crit(h):
    """h'(x)=0의 서로 다른 실근"""
    P = sp.Poly(sp.expand(sp.diff(h, x)), x)
    if P.domain.is_QQ or P.domain.is_ZZ:
        return sorted(set(sp.real_roots(P)), key=lambda r: float(r))
    return sorted({sp.nsimplify(s) for s in sp.solve(P.as_expr(), x) if s.is_real}, key=float)

def answers(f, K=1000):
    """(1) 기울기 2인 접선의 개수, (2) f(0), (3) f(x)=2x+k가 서로 다른 실근 4개인 정수 k의 최댓값"""
    h = sp.expand(f - 2 * x)
    lines = {sp.nsimplify(sp.N(h.subs(x, r), 40), rational=False) if not r.is_rational else h.subs(x, r) for r in real_crit(h)}
    lines = sorted({round(float(v), 9) for v in lines})
    n1 = len(lines)
    f0 = sp.nsimplify(f.subs(x, 0))
    ks = [kk for kk in range(-K, K + 1) if nreal(h - kk) == 4]
    k3 = max(ks) if ks else '없음'
    return (n1, f0, k3)

def cond_ga(f, d=4):
    """(가) f(-3), f(-1), f(1), f(3) 이 순서대로 공차 d인 등차수열"""
    v = [f.subs(x, s) for s in (-3, -1, 1, 3)]
    return all(sp.simplify(v[i + 1] - v[i] - d) == 0 for i in range(3))

def cond_na(f):
    """(나) 직선 y=2x가 곡선에 접하고(h=f-2x가 겹친 실근을 가짐) 교점의 개수가 2"""
    h = sp.expand(f - 2 * x)
    g = sp.gcd(sp.Poly(h, x), sp.Poly(sp.diff(h, x), x))
    tangent = g.degree() >= 1 and nreal(g.as_expr()) >= 1
    return tangent and nreal(h) == 2


# ---------- 원문 D65: f(-1),f(0),f(1),f(2) 등차, 양 끝 접선이 (k,0)에서 만남, f(2k)=20 → f(4k)=42
P4, Q4, R4, S4 = sp.symbols('P4 Q4 R4 S4', real=True)
fo = x**4 + P4 * x**3 + Q4 * x**2 + R4 * x + S4
vo = [fo.subs(x, s) for s in (-1, 0, 1, 2)]
so = sp.solve([vo[1] - vo[0] - (vo[2] - vo[1]), vo[2] - vo[1] - (vo[3] - vo[2])], [P4, Q4], dict=True)
assert len(so) == 1
fo = fo.subs(so[0])
assert sp.expand(fo - (x + 1) * x * (x - 1) * (x - 2) - (R4 - 2) * x - S4) == 0     # f = R + 일차식
T1 = sp.diff(fo, x).subs(x, -1) * (x + 1) + fo.subs(x, -1)
T2 = sp.diff(fo, x).subs(x, 2) * (x - 2) + fo.subs(x, 2)
sol_o = sp.solve([T1.subs(x, k), T2.subs(x, k), fo.subs(x, 2 * k) - 20], [R4, S4, k], dict=True)
vals_o = {sp.simplify(fo.subs(s_).subs(x, 4 * s_[k])) for s_ in sol_o}
assert vals_o == {42}, vals_o
print('D65 원문 OK: f(4k) = 42')

# ---------- S2 전수 풀이
f = x**4 + A * x**3 + B * x**2 + C * x + D
v = [f.subs(x, s) for s in (-3, -1, 1, 3)]
s1 = sp.solve([v[1] - v[0] - 4, v[2] - v[1] - 4, v[3] - v[2] - 4], [A, B, C], dict=True)
assert s1 == [{A: 0, B: -10, C: 2}]
f = f.subs(s1[0])                                              # x^4 - 10x^2 + 2x + D
h = sp.expand(f - 2 * x)
assert sp.expand(h - D - (x**2 - 1) * (x**2 - 9) + 9) == 0     # h(x)-h(1) = (x^2-1)(x^2-9)
# (1) 기울기 2인 접선: f'(t)=2 ⇔ 4t(t^2-5)=0, 접선 y=2x+h(t)
ts = sp.solve(sp.diff(f, x) - 2, x)
assert set(ts) == {0, sp.sqrt(5), -sp.sqrt(5)}
icpt = {sp.simplify(h.subs(x, r)) for r in ts}
assert icpt == {D, D - 25}                                      # 직선 두 개 (±√5 는 같은 직선)
for r in ts:                                                    # 접선식 확인
    T = sp.diff(f, x).subs(x, r) * (x - r) + f.subs(x, r)
    assert sp.expand(T - 2 * x - h.subs(x, r)) == 0
# (2) y=2x가 접함: f(t)=2t, f'(t)=2 를 (t, D)에 대해 전수 풀이
cand = sp.solve([f.subs(x, t) - 2 * t, sp.diff(f, x).subs(x, t) - 2], [t, D], dict=True)
Ds = sorted({c_[D] for c_ in cand})
assert Ds == [0, 25], Ds
cnt = {d_: nreal(h.subs(D, d_)) for d_ in Ds}
assert cnt == {0: 3, 25: 2}                                     # D=0 이면 교점 x=0, ±√10
keep = [d_ for d_ in Ds if cnt[d_] == 2]
assert keep == [25]
F = f.subs(D, 25)
assert sp.expand(F - (x**2 - 5)**2 - 2 * x) == 0
assert cond_ga(F) and cond_na(F)
assert [F.subs(x, s) for s in (-3, -1, 1, 3)] == [10, 14, 18, 22]
# (3) (x^2-5)^2 = k 가 서로 다른 실근 4개 ⇔ 0<k<25
for kk in range(-5, 31):
    n_ = nreal((x**2 - 5)**2 - kk)
    assert n_ == (4 if 0 < kk < 25 else 3 if kk == 25 else 2 if kk == 0 or kk > 25 else 0), (kk, n_)
ANS = answers(F)
assert ANS == (2, 25, 24), ANS
assert S['ans'] == ['(1) 2', '(2) 25', '(3) 24']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'D65'
# 오답 근거
assert len(ts) == 3                                             # (1) 근의 개수를 그대로 세면 3
F0 = f.subs(D, 0)
assert F0.subs(x, 0) == 0 and nreal(F0 - 2 * x) == 3            # (2) 원점에서 접하는 경우 0 (교점 3개라 제외)
assert nreal(F - 2 * x - 25) == 3                               # (3) k=25 이면 실근 3개 → 25 는 오답
assert answers(F0)[2] == -1                                     # (2)에서 D=0 을 택하면 (3) -1
print('S2 OK: (1) 2, (2) 25, (3) 24')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, vals, why=''):
    sv = list(dict.fromkeys(vals))
    if sv == [ANS]:
        msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    else:
        others = [s_ for s_ in sv if s_ != ANS]
        parts = []
        for i in range(3):
            col = list(dict.fromkeys(s_[i] for s_ in sv))
            parts.append(f'({i + 1}) ' + ('그대로 ' + str(ANS[i]) if col == [ANS[i]] else ' | '.join(map(str, col))))
        kind = '정해지지 않음' if len(sv) >= 2 else '답 바뀜'
        msg = f'필요({kind}: {", ".join(parts)}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg

res = []
# 1) 최고차항의 계수 1 제거: f = a(x^2-1)(x^2-9) + 2x + c, (나) 로 c 결정
va = []
for av in (1, 2, 3):
    fa = av * (x**2 - 1) * (x**2 - 9) + 2 * x + b
    ca = sp.solve([fa.subs(x, t) - 2 * t, sp.diff(fa, x).subs(x, t) - 2], [t, b], dict=True)
    for c_ in ca:
        Fa = fa.subs(b, c_[b])
        if cond_ga(Fa) and cond_na(Fa): va.append(answers(Fa))
res.append(ablation("'최고차항의 계수가 1'", va, why='f=a(x^2-5)^2+2x, a=1,2,3'))
# 2) '사차함수' 제거(차수 8): f-2x = (x^2-5)^2{(x^2-5)^2+c}, c>0 이면 (가)·(나) 성립
vd = [ANS]
for cv in (1, 2):
    F8 = (x**2 - 5)**2 * ((x**2 - 5)**2 + cv) + 2 * x
    assert cond_ga(F8) and cond_na(F8) and sp.Poly(F8, x).LC() == 1
    vd.append(answers(F8, K=1300))
res.append(ablation("'사차함수'(→ 최고차항의 계수가 1인 다항함수)", vd, why='예: f-2x=(x^2-5)^2{(x^2-5)^2+c}'))
# 3) 등차 조건 전체 제거: f=(x^2-s)^2+2x 도 (나) 성립
vg = []
for sv_ in (5, 1, 4):
    Fg = (x**2 - sv_)**2 + 2 * x
    assert cond_na(Fg)
    vg.append(answers(Fg))
res.append(ablation("'f(-3), f(-1), f(1), f(3)이 등차수열'", vg, why='예: f=(x^2-s)^2+2x'))
# 4) '공차가 4' 제거(등차수열만): f-2x = x^4-10x^2+mx+D. 겹친 근 t: m=20t-4t^3, D=3t^4-10t^2
fm = x**4 - 10 * x**2 + C * x + D
assert cond_ga(fm.subs(C, 2), 4)
vm = []
for tv in (sp.sqrt(5), -sp.sqrt(5), sp.sqrt(sp.Rational(5, 3)), -sp.sqrt(sp.Rational(5, 3))):
    mv = 20 * tv - 4 * tv**3; Dv = 3 * tv**4 - 10 * tv**2
    Fm = fm.subs({C: mv + 2, D: Dv})
    hm = sp.expand(Fm - 2 * x)
    assert sp.expand(hm.subs(x, tv)) == 0 and sp.expand(sp.diff(hm, x).subs(x, tv)) == 0
    assert nreal(hm) == 2, (tv, nreal(hm))
    if tv**2 == sp.Rational(5, 3):                                  # (x-t)^3(x+3t): 극값은 x=-2t 하나뿐 → 실근 4개 불가
        assert sp.expand(hm - (x - tv)**3 * (x + 3 * tv)) == 0
        crit = sp.solve(sp.diff(hm, x), x)
        assert {sp.radsimp(sp.simplify(r)) for r in crit} == {sp.radsimp(tv), sp.radsimp(-2 * tv)}, crit
        assert sp.simplify(sp.diff(hm, x, 2).subs(x, tv)) == 0
        lines = {sp.simplify(hm.subs(x, r)) for r in crit}
        vm.append((len(lines), sp.nsimplify(Fm.subs(x, 0)), '없음'))
    else:
        vm.append(answers(Fm))
# 나머지 t 는 교점 개수가 2가 아님을 확인 (q(x)=x^2+2tx+3t^2-10 의 판별식 10-2t^2)
for tv in [sp.Rational(i, 4) for i in range(-16, 17)]:
    mv = 20 * tv - 4 * tv**3; Dv = 3 * tv**4 - 10 * tv**2
    n_ = nreal(x**4 - 10 * x**2 + mv * x + Dv)
    assert n_ != 2 or tv**2 in (5, sp.Rational(5, 3)), tv
res.append(ablation("'공차가 4'(→ 등차수열만)", vm, why='y=2x가 x=t에서 세 번 겹쳐 접하는 경우 t^2=5/3 추가'))
# 5) 네 수 중 f(3) 제거(세 수 f(-3), f(-1), f(1)만 공차 4): h=f-2x 는 h(-3)=h(-1)=h(1) 만 남아 넷째 근 r 이 자유
#    h(x)-h(1)=(x+3)(x+1)(x-1)(x-r). r=3 은 본 문항, r=-5 이면 h=((x+2)^2-5)^2 도 (나) 성립
v3 = []
for Fr in (F, ((x + 2)**2 - 5)**2 + 2 * x):
    w3 = [Fr.subs(x, s) for s in (-3, -1, 1)]
    assert w3[1] - w3[0] == 4 and w3[2] - w3[1] == 4 and cond_na(Fr)
    v3.append(answers(Fr))
assert not cond_ga(((x + 2)**2 - 5)**2 + 2 * x)                # 넷째 수 f(3)=406 이라 공차 4가 깨짐
res.append(ablation("'네 수 중 f(3)'(→ 세 수 f(-3), f(-1), f(1))", v3, why='예: f=((x+2)^2-5)^2+2x (f(3)=406)'))
# 6) '직선 y=2x는 곡선에 접하고' 제거: 교점 2개만 → h=x^4-10x^2+D, D<0 또는 D=25
vt = []
for Dv in (25, -1, -11):
    Ft = f.subs(D, Dv)
    assert nreal(Ft - 2 * x) == 2
    vt.append(answers(Ft))
res.append(ablation("'직선 y=2x는 곡선 y=f(x)에 접하고'", vt, why='D<0 이면 교점 2개(접하지 않음)'))
# 7) '교점의 개수는 2' 제거: D=0, 25 둘 다 가능
vn = [answers(f.subs(D, Dv)) for Dv in Ds]
res.append(ablation("'만나는 점의 개수는 2'", vn, why='원점에서 접하는 D=0도 가능'))
# 8) (나) 전체 제거: D 자유
vall = [answers(f.subs(D, Dv)) for Dv in (25, 0, 7)]
res.append(ablation("'직선 y=2x에 대한 조건 전체'", vall, why='D 자유'))
assert all(r_.startswith('필요') for r_ in res), res
print('ALL OK')
