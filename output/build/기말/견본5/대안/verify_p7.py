# -*- coding: utf-8 -*-
# 견본5 서답형2 (D62 구조 변경) 검증 · author='claude' (B팀)
import sympy as sp, os, itertools
x, c, p, q, m, n, r = sp.symbols('x c p q m n r', real=True)
A3, A2, A1, A0 = sp.symbols('A3 A2 A1 A0', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S = ns['SITEMS']['S2']
R = sp.Rational


# ---------- 도구 ----------
def real_roots_mult(P):
    """다항식 P(x)의 실근과 중복도 {근: 중복도} (계수 유리수)"""
    out = {}
    for rt in sp.real_roots(sp.Poly(sp.expand(P), x)):
        out[rt] = out.get(rt, 0) + 1
    return out

def is_h_ok(f, g, a=1):
    """h=|f-g| (x<a), f+g (x>=a)가 실수 전체에서 미분가능한가 (f, g 유리계수 다항식)
    x<a: |F|는 F의 실근 ρ에서 F'(ρ)=0일 때만 미분가능(단순근이면 좌·우 미분계수 부호가 반대)
    x=a: 왼쪽 근방의 부호 s로 h=sF, 오른쪽 f+g와 함숫값·미분계수가 같아야 함"""
    F = sp.expand(f - g); G = sp.expand(f + g)
    if F == 0: return False
    for rt, k in real_roots_mult(F).items():
        if rt < a and k < 2: return False
    # x=a 왼쪽 근방의 부호: F를 (x-a)^k로 나눈 몫의 a에서의 값과 (-1)^k
    k = 0; Q = F
    while sp.expand(Q).subs(x, a) == 0:
        Q = sp.quo(sp.Poly(Q, x), sp.Poly(x - a, x)).as_expr(); k += 1
    s = sp.sign(Q.subs(x, a)) * (-1) ** k
    L = s * F
    return sp.simplify(L.subs(x, a) - G.subs(x, a)) == 0 and sp.simplify(sp.diff(L, x).subs(x, a) - sp.diff(G, x).subs(x, a)) == 0

def hfun(f, g, a=1):
    return sp.Piecewise((sp.Abs(f - g), x < a), (f + g, True))

def onesided(f, g, pt, a=1):
    """h의 x=pt에서의 (좌극한, 우극한, 함숫값, 좌미분계수, 우미분계수) — 조각을 직접 골라 계산"""
    L = sp.Abs(f - g) if pt <= a else f + g          # 왼쪽 조각
    Rr = sp.Abs(f - g) if pt < a else f + g          # 오른쪽 조각
    v = (f + g).subs(x, pt) if pt >= a else sp.Abs(f - g).subs(x, pt)
    return (sp.limit(L, x, pt, '-'), sp.limit(Rr, x, pt, '+'), v,
            sp.limit((L - v) / (x - pt), x, pt, '-'), sp.limit((Rr - v) / (x - pt), x, pt, '+'))

def hprime_roots(f, g, a=1):
    """방정식 h'(x)=0의 서로 다른 실근 (h가 미분가능하다고 할 때). x<a는 |F|의 도함수, x>=a는 (f+g)'"""
    F = sp.expand(f - g); G = sp.expand(f + g)
    out = set()
    # x<a: F의 실근(미분가능이면 F'=0)에서 h'=0, 그 밖에서는 h'=±F' → F'=0
    for rt in sp.real_roots(sp.Poly(sp.diff(F, x), x)):
        if rt < a: out.add(rt)
    for rt in sp.real_roots(sp.Poly(F, x)):
        if rt < a: out.add(rt)
    for rt in sp.real_roots(sp.Poly(sp.diff(G, x), x)):
        if rt >= a: out.add(rt)
    return sorted(out, key=float)

def fam(cv):
    """F=x^3(x-c), g = -(F의 x=1에서의 접선), f = F + g"""
    F = x**3 * (x - cv)
    g = sp.expand(-F.subs(x, 1) - sp.diff(F, x).subs(x, 1) * (x - 1))
    return sp.expand(F + g), g

def answers(f, g):
    G = sp.expand(f + g)
    return (G.subs(x, 2), sp.diff(G, x).subs(x, 1), G.subs(x, 4))


# ---------- 원문 D62: 삼차 f, 일차 g, h 미분가능, h(0)=0, h(2)=5 → h(4)=39
F0 = x**2 * (x - c)                                   # h(0)=0, |F|가 x=0에서 미분가능 ⇒ F(0)=F'(0)=0
fo = x**3 + A2 * x**2 + A1 * x + A0
# 경계 x=1: 왼쪽이 +F이면 2g 가 x=1에서 함숫값·미분계수 0 → g≡0
gm = m * x + n
sp_plus = sp.solve([(fo - gm - (fo + gm)).subs(x, 1), sp.diff(fo - gm - (fo + gm), x).subs(x, 1)], [m, n], dict=True)
assert sp_plus == [{m: 0, n: 0}]
# 왼쪽이 -F: f(1)=f'(1)=0, f = F + g
so = sp.solve([sp.expand(F0 + gm - fo).coeff(x, k) for k in range(4)] + [fo.subs(x, 1), sp.diff(fo, x).subs(x, 1)], [A2, A1, A0, m, n], dict=True)
assert len(so) == 1
fo1 = fo.subs(so[0]); go1 = gm.subs(so[0])
Ho = sp.expand(fo1 + go1)
cs = sp.solve(Ho.subs(x, 2) - 5, c)
assert cs == [R(5, 2)]
fo2, go2 = fo1.subs(c, R(5, 2)), go1.subs(c, R(5, 2))
assert is_h_ok(fo2, go2) and sp.expand(fo2 - go2).subs(x, 0) == 0
assert sp.expand(fo2 + go2).subs(x, 4) == 39
print('D62 원문 OK: f-g=x^2(x-5/2), h(4) = 39')


# ---------- S2 전수 풀이
f = x**4 + A3 * x**3 + A2 * x**2 + A1 * x + A0
g = m * x + n
F = f - g
# [1] 경계 x=1 (원리 유지): 왼쪽 근방에서 h=+F 이면 g(1)=g'(1)=0 → g≡0 (모순)
plus = sp.solve([(F - (f + g)).subs(x, 1), sp.diff(F - (f + g), x).subs(x, 1)], [m, n], dict=True)
assert plus == [{m: 0, n: 0}]
#     h=-F 이면 f(1)=0, f'(1)=0
minus = sp.solve([(-F - (f + g)).subs(x, 1), sp.diff(-F - (f + g), x).subs(x, 1)], [A0, A1], dict=True)
assert len(minus) == 1
fm = f.subs(minus[0])
assert sp.expand(fm.subs(x, 1)) == 0 and sp.expand(sp.diff(fm, x).subs(x, 1)) == 0
#     따라서 g(1) = -F(1), g'(1) = -F'(1): g 는 -(F의 x=1에서의 접선)
# [2] h(0)=0: F(0)=0, |F|가 x=0에서 미분가능 ⇒ F'(0)=0 ⇒ F = x^2(x^2+px+q)
#     [3] F(x)→+∞ (x→-∞), x=1 왼쪽에서 F<0 ⇒ x<1에서 부호가 바뀌는 실근 α, |F| 미분가능 ⇒ (x-α)^3 | F
#     x^2(x^2+px+q) 에서 그런 α는 0뿐 (q=0) ⇒ F = x^3(x-c), c>=1 (c<1, c≠0 이면 단순근, c=0 이면 F=x^4>=0)
#     전수: p, q 를 격자에서 훑어 조건을 모두 만족하는 것은 q=0, -p>=1 (p≠-4/3) 뿐임을 확인
found = []
grid = [R(k, 3) for k in range(-27, 28)]
for pv, qv in itertools.product(grid, grid):
    Fv = x**2 * (x**2 + pv * x + qv)
    gv = sp.expand(-Fv.subs(x, 1) - sp.diff(Fv, x).subs(x, 1) * (x - 1))
    if sp.Poly(gv, x).degree() != 1: continue                    # g 는 일차함수
    fv = sp.expand(Fv + gv)
    if is_h_ok(fv, gv): found.append((pv, qv))
assert found and all(qv == 0 and -pv >= 1 for pv, qv in found), [t for t in found if not (t[1] == 0 and -t[0] >= 1)][:5]
assert {-pv for pv, qv in found} == {v for v in (-t for t in grid) if v >= 1 and v != R(4, 3)}
print(f'격자 {len(grid)**2}개 (p, q) 중 미분가능한 것: q=0, c=-p>=1, c≠4/3 ({len(found)}개)')
#     F(1)=0 인 경우(c=1)도 미분가능: 왼쪽 근방에서 F<0, g(1)=0, g'(1)=-1
f1, g1 = fam(1)
assert is_h_ok(f1, g1) and g1 == 1 - x
# [4] 족: f - g = x^3(x-c), g = (3c-4)(x-1) + c - 1, c>=1, c≠4/3 (c=4/3 이면 g=1/3 상수)
fc, gc = fam(c)
assert sp.expand(gc - ((3 * c - 4) * (x - 1) + c - 1)) == 0
assert sp.expand(fc - (x - 1)**2 * (x**2 + (2 - c) * x + 3 - 2 * c)) == 0
assert gc.subs(c, R(4, 3)) == R(1, 3)
Hc = sp.expand(fc + gc)
# (1) h(2) = 6 (c와 무관)
assert sp.simplify(Hc.subs(x, 2)) == 6
assert sp.expand(sp.diff(Hc, c)).subs(x, 2) == 0
# (2) 방정식 h'(x)=0 의 서로 다른 실근의 개수
#   x<1: h' = F' 또는 -F', F' = x^2(4x-3c) → 0, (c<4/3 이면) 3c/4
#   x>=1: k(x) = 4x^3 - 3cx^2 + 6c - 8, k(1) = 3c-4, k' = 6x(2x-c), k(c/2) = -(c-4)(c^2+4c-8)/4
kx = sp.diff(Hc, x)
assert sp.expand(kx - (4 * x**3 - 3 * c * x**2 + 6 * c - 8)) == 0
assert sp.expand(kx.subs(x, 1) - (3 * c - 4)) == 0
assert sp.factor(sp.diff(kx, x)) == 6 * x * (2 * x - c)
assert sp.expand(kx.subs(x, c / 2) + (c - 4) * (c**2 + 4 * c - 8) / 4) == 0
def count(cv):
    fv, gv = fam(cv)
    return len(hprime_roots(fv, gv))
cnt = {}
for cv in sorted(set([R(k, 12) for k in range(12, 121)] + [R(4), R(3, 2), R(2), R(5, 4)])):
    if cv == R(4, 3): continue
    fv, gv = fam(cv)
    assert is_h_ok(fv, gv)
    cnt[cv] = count(cv)
two = [cv for cv, k in cnt.items() if k == 2]
assert two == [4], two
assert all(cnt[cv] >= 3 for cv in cnt if cv < R(4, 3))
assert all(cnt[cv] == 1 for cv in cnt if R(4, 3) < cv < 4)
assert all(cnt[cv] == 3 for cv in cnt if cv > 4)
#   c^2+4c-8=0 의 근 c=-2+2√3 은 접점 x=c/2 가 1보다 작아 x>=1 에서 k>0 (근 없음)
c2 = -2 + 2 * sp.sqrt(3)
assert c2 / 2 < 1 and kx.subs(c, c2).subs(x, 1) > 0
assert c2 < 2   # x>=1 에서 k'(x)=6x(2x-c)>0 이고 k(1)>0 이므로 근 없음
#   c=4/3 은 h'=0 의 근이 {0, 1} 두 개이지만 g 가 상수함수라 제외
f43, g43 = fam(R(4, 3))
assert is_h_ok(f43, g43) and hprime_roots(f43, g43) == [0, 1] and sp.Poly(g43, x).degree() == 0
# 답
F4, G4 = fam(4)
assert G4 == 8 * x - 5 and sp.factor(F4) == (x - 1)**2 * (x**2 - 2 * x - 5)
assert is_h_ok(F4, G4) and sp.expand(F4 - G4).subs(x, 0) == 0 and hprime_roots(F4, G4) == [0, 2]
assert sp.factor(sp.diff(F4 + G4, x)) == 4 * (x - 2)**2 * (x + 1)
# 미분가능 재확인 (좌·우 미분계수)
for pt in (0, 1):
    a_, b_, v_, hl, hr = onesided(F4, G4, pt)
    assert a_ == b_ == v_ and hl == hr, (pt, a_, b_, v_, hl, hr)
ANS = answers(F4, G4)
assert ANS == (6, 8, 54), ANS
assert S['ans'] == ['(1) 6', '(2) 8', '(3) 54']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'D62' and S['core']['axis'] == '②'
# 단계별 유일성: (1)은 족 전체에서 6, (2)·(3)은 c=4 하나
assert {answers(*fam(cv))[0] for cv in cnt} == {6}
print('S2 OK: (1) 6, (2) 8, (3) 54  (f=(x-1)^2(x^2-2x-5), g=8x-5, f-g=x^3(x-4))')
# 오답 근거
assert answers(f43, g43)[1:] == (0, R(514, 3))                   # c=4/3 (g 상수) 을 택하면
assert sp.nsimplify(sp.expand(sp.diff(fam(c2)[0] + fam(c2)[1], x).subs(x, 1))) == 6 * sp.sqrt(3) - 10   # 접점 확인 생략
assert sp.expand(F4 - G4).subs(x, 2) == -16 and sp.expand(F4 - G4).subs(x, 4) == 0     # 조각 착각 f-g
# 원문 설정 줄을 그대로 쓰면(f-g=x^2(x^2+px+q), q≠0) 미분가능한 h가 없음 → 격자 결과에 q≠0 없음 (위 assert)

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, vals, why=''):
    sv = list(dict.fromkeys(vals))
    if sv == [ANS]:
        msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    elif not sv:
        msg = f'필요(조건을 만족시키는 h 없음{"; " + why if why else ""})'
    else:
        parts = []
        for i in range(3):
            col = list(dict.fromkeys(s_[i] for s_ in sv))
            parts.append(f'({i + 1}) ' + ('그대로 ' + str(ANS[i]) if col == [ANS[i]] else ' | '.join(map(str, col))))
        kind = '정해지지 않음' if len(sv) >= 2 else '답 바뀜'
        msg = f'필요({kind}: {", ".join(parts)}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg

res = []
# 1) '최고차항의 계수가 1' 제거: f-g = a x^3(x-4) 도 모든 조건 만족 (h 가 a배)
va = [ANS]
for av in (2, 3):
    Fa = av * x**3 * (x - 4)
    ga = sp.expand(-Fa.subs(x, 1) - sp.diff(Fa, x).subs(x, 1) * (x - 1)); fa = sp.expand(Fa + ga)
    assert is_h_ok(fa, ga) and len(hprime_roots(fa, ga)) == 2 and sp.Poly(ga, x).degree() == 1
    va.append(answers(fa, ga))
res.append(ablation("'최고차항의 계수가 1'", va, why='f-g=ax^3(x-4), a=2,3'))
# 2) '사차함수' → '삼차함수': f-g = x^2(x-c), c>=1 (원문 설정), h'=0 의 근이 2개 ⇔ c=6+3√2
F3 = x**2 * (x - c)
g3 = sp.expand(-F3.subs(x, 1) - sp.diff(F3, x).subs(x, 1) * (x - 1)); f3 = sp.expand(F3 + g3)
k3 = sp.expand(sp.diff(f3 + g3, x))
assert sp.expand(k3 - (3 * x**2 - 2 * c * x + 4 * c - 6)) == 0
c3 = 6 + 3 * sp.sqrt(2)
assert sp.simplify(k3.subs(c, c3).subs(x, c3 / 3)) == 0 and c3 / 3 > 1
for cv in [R(k, 4) for k in range(4, 60)]:                       # 다른 c 에서는 근의 개수가 2가 아님
    fv, gv = f3.subs(c, cv), g3.subs(c, cv)
    if sp.Poly(gv, x).degree() != 1: continue
    assert is_h_ok(fv, gv) and len(hprime_roots(fv, gv)) != 2, cv
G3 = sp.expand(f3 + g3).subs(c, c3)
v3 = [(sp.nsimplify(sp.expand(G3.subs(x, 2))), sp.nsimplify(sp.expand(sp.diff(G3, x).subs(x, 1))), sp.nsimplify(sp.expand(G3.subs(x, 4))))]
res.append(ablation("'사차함수'(→ 삼차함수, 원문 설정)", v3, why='f-g=x^2(x-c), c=6+3√2'))
# 3) '일차함수' → 상수함수 허용: c=4/3 (g=1/3) 도 h'=0 의 근이 {0, 1}
res.append(ablation("'일차함수'(→ 상수함수 허용)", [ANS, answers(f43, g43)], why='c=4/3, g=1/3'))
# 4) '실수 전체의 집합에서 미분가능' → 연속, x≠1 에서 미분가능: f-g=x^3(x-2), g=2-x
F5 = x**3 * (x - 2); g5 = 2 - x; f5 = sp.expand(F5 + g5)
a5, b5, v5, dl, dr = onesided(f5, g5, 1)
assert a5 == b5 == v5                                                           # 연속
assert (dl, dr) == (2, -4)                                                      # x=1 에서 미분불가능
assert sp.Abs(f5 - g5).subs(x, 0) == 0
z5 = [z for z in sp.real_roots(sp.Poly(sp.diff(F5, x), x)) if z < 1]
z5 = sorted(set(z5) | {z for z in sp.real_roots(sp.Poly(sp.diff(f5 + g5, x), x)) if z > 1}, key=float)
assert len(z5) == 2                                                             # h'(x)=0 의 근 0 과 x>1 의 하나
res.append(ablation("'미분가능'(→ 연속, x=1 제외 미분가능)", [(sp.expand(f5 + g5).subs(x, 2), '없음', sp.expand(f5 + g5).subs(x, 4))], why='f-g=x^3(x-2), g=2-x, x=1에서 좌미분 2·우미분 -4'))
# 5) 'h(0)=0' 제거: f-g=(x-r)^3(x-c) (r<1<=c). r=-1 에서 h'=0 의 근이 2개인 c 를 찾음
Fr = (x + 1)**3 * (x - c)
gr = sp.expand(-Fr.subs(x, 1) - sp.diff(Fr, x).subs(x, 1) * (x - 1)); fr = sp.expand(Fr + gr)
kr = sp.expand(sp.diff(fr + gr, x))
# x>=1 에서 kr 이 x축에 접하는 점 t>=1: kr(t)=kr'(t)=0
tc = sp.solve([kr.subs(x, sp.Symbol('t')), sp.diff(kr, x).subs(x, sp.Symbol('t'))], [sp.Symbol('t'), c], dict=True)
vr = []
for s_ in tc:
    tv, cv = s_[sp.Symbol('t')], s_[c]
    if not (tv.is_real and cv.is_real) or tv < 1 or cv < 1: continue
    fv, gv = fr.subs(c, cv), gr.subs(c, cv)
    if not cv.is_rational: continue
    if is_h_ok(fv, gv) and len(hprime_roots(fv, gv)) == 2:
        vr.append(answers(fv, gv))
assert vr, tc
res.append(ablation("'곡선 y=h(x)는 원점을 지난다'(h(0)=0)", [ANS] + vr, why='f-g=(x+1)^3(x-c)'))
# 6) '방정식 h'(x)=0 의 서로 다른 실근의 개수 2' 제거: c 자유 (c>=1, c≠4/3)
res.append(ablation("'h'(x)=0의 서로 다른 실근의 개수가 2'", [answers(*fam(cv)) for cv in (4, 2, 3)], why='c=4,2,3'))
# 7) 'h'(x)=0 의 실근 개수' 를 1 로 바꾸면 c 가 구간 (4/3, 4) → 정해지지 않음 (개수 2가 일함을 확인)
assert all(cnt[cv] == 1 for cv in (R(3, 2), R(2), R(3)))
# 8) 절댓값 제거 (x<1 에서 h=f-g): 왼쪽이 +F 이므로 g≡0 → 조건을 만족시키는 h 없음
assert plus == [{m: 0, n: 0}]
res.append(ablation("'|f(x)-g(x)|의 절댓값'(→ f(x)-g(x))", [], why='x=1에서 2g의 함숫값·미분계수가 0 → g≡0'))
assert all(r_.startswith('필요') for r_ in res), res
print('ALL OK')
