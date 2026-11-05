# -*- coding: utf-8 -*-
# 서답형2 (M56 구조 변경) 검증 · author='claude'
import sympy as sp, os
x, a, k = sp.symbols('x a k', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
S = ns['SITEMS']['S2']


# ---------- 도구: 방정식 F(x)+|F(x)-L(x)| = Rhs(x)+kv 의 서로 다른 실근 (정확한 값)
def sgn_at(p, r):
    """다항식 p 의 x=r 에서의 부호 (r 은 대수적 수). 0 이면 정확히 0"""
    v = sp.expand(p.subs(x, r)) if r.is_rational else None
    if v is not None: return sp.sign(v)
    P = sp.Poly(p, x)
    m = sp.Poly(sp.minimal_polynomial(r, x), x)
    if sp.gcd(P, m).degree() > 0 and sp.Poly(sp.rem(P, m), x).is_zero: return 0
    vv = sp.N(p.subs(x, r), 60)
    assert abs(vv) > 1e-40
    return 1 if vv > 0 else -1

def sols(F, L, kv, Rhs=0):
    """F(x)+|F(x)-L(x)| = Rhs + kv 의 실근 집합. F-L>=0 이면 2F-L, F-L<0 이면 L"""
    out = set()
    d = sp.expand(F - L)
    for r in sp.real_roots(sp.Poly(sp.expand(2 * F - L - Rhs - kv), x)):
        if sgn_at(d, r) >= 0: out.add(r)
    pl = sp.expand(L - Rhs - kv)
    if pl != 0:
        for r in sp.real_roots(sp.Poly(pl, x)) if sp.Poly(pl, x).degree() > 0 else []:
            if sgn_at(d, r) < 0: out.add(r)
    else:
        return None                                    # 무수히 많음
    return out

def cnt(F, L, kv, Rhs=0):
    s = sols(F, L, kv, Rhs)
    return float('inf') if s is None else len(s)


# ---------- 원문 M56: f=x^3/2-9x^2/2+10x, f+|f+x|=6x+k, 4근 정수 k 합 21
fo = x**3 / 2 - R(9, 2) * x**2 + 10 * x
assert sp.factor(fo + x) == x * (x**2 - 9 * x + 22) / 2 and sp.discriminant(x**2 - 9 * x + 22, x) < 0
go = x**3 - 9 * x**2 + 15 * x
assert sp.expand(2 * fo + x - 6 * x - go) == 0
assert sp.solve(sp.diff(go, x), x) == [1, 5] and go.subs(x, 1) == 7 and go.subs(x, 5) == -25
KO = [kv for kv in range(-40, 41) if cnt(fo, -x, kv, 6 * x) == 4]
assert KO == [1, 2, 3, 4, 5, 6] and sum(KO) == 21
for kv in [R(1, 2), R(13, 2)]: assert cnt(fo, -x, kv, 6 * x) == 4
for kv in [0, 7, -25, R(-1, 2), R(15, 2)]: assert cnt(fo, -x, kv, 6 * x) != 4
print('M56 원문 OK: 4근 정수 k = 1..6, 합 21 (원문 정답 21)')

# ---------- S2: f=x^3+4x^2-6x, 곡선 y=f(x)와 직선 y=ax 가 서로 다른 두 점에서 만남, 4근 k 존재
f = x**3 + 4 * x**2 - 6 * x
def meet(av):
    return len(set(sp.real_roots(sp.Poly(sp.expand(f - av * x), x))))
# --- '두 점에서 만남'의 기호 풀이: f-ax = x(x^2+4x-(a+6))
assert sp.expand(f - a * x - x * (x**2 + 4 * x - (a + 6))) == 0
qd = x**2 + 4 * x - (a + 6)
# (i) 이차식이 0 을 근으로 → a=-6 (다른 근 -4≠0) / (ii) 0 이 아닌 중근 → 판별식 0 → a=-10 (중근 -2)
assert sp.solve(qd.subs(x, 0), a) == [-6] and sp.solve(sp.discriminant(qd, x), a) == [-10]
assert sp.factor(f + 6 * x) == x**2 * (x + 4) and sp.factor(f + 10 * x) == x * (x + 2)**2
# 그 밖의 a: 판별식>0·a≠-6 이면 세 점, 판별식<0 이면 한 점
gridA = sorted(set([R(i, 4) for i in range(-80, 41)] + [R(-6), R(-10)]))
TWO = [av for av in gridA if meet(av) == 2]
assert TWO == [-10, -6], TWO
for av in gridA:
    assert meet(av) == (2 if av in (-10, -6) else (1 if av < -10 else 3))
# 기호: 판별식 4(a+10) — a<-10 이면 이차식 근 없음(한 점), a>-10·a≠-6 이면 0 이 아닌 서로 다른 두 근(세 점)
assert sp.expand(sp.discriminant(qd, x) - 4 * (a + 10)) == 0

# --- 각 후보의 실근 개수 함수 (정확한 임계값 + 촘촘한 격자)
def profile(av, crit):
    ks = sorted(set(crit + [c + d for c in crit for d in (R(-1, 100), R(1, 100))] + [R(i, 4) for i in range(-60, 241)]), key=float)
    return {kv: cnt(f, av * x, kv) for kv in ks}

# a=-10: x<0 에서 -10x, x≥0 에서 2x^3+8x^2-2x (원문 설정이 통하는 후보)
g10 = 2 * f + 10 * x
assert sp.expand(g10 - (2 * x**3 + 8 * x**2 - 2 * x)) == 0
c10 = [c for c in sp.solve(sp.diff(g10, x), x) if c >= 0]
assert len(c10) == 1 and sp.diff(g10, x).subs(x, 0) == -2                      # x≥0 에서 극값 하나(감소 → 증가)
assert not c10[0].is_rational                                                  # 극솟값은 무리수: 그 높이에서 x≥0 근 1개뿐
P10 = profile(-10, [R(0), R(20), sp.floor(g10.subs(x, c10[0]) * 1000) / 1000, sp.ceiling(g10.subs(x, c10[0]) * 1000) / 1000])
assert max(P10.values()) == 2, max(P10.values())
print('a=-10: 실근 개수 최대', max(P10.values()), '→ 4개인 k 없음, 기각')

# a=-6: x<-4 에서 -6x, x≥-4 에서 2x^3+8x^2-6x
g6 = 2 * f + 6 * x
assert sp.expand(g6 - (2 * x**3 + 8 * x**2 - 6 * x)) == 0
assert sp.expand(sp.diff(g6, x) - 2 * (x + 3) * (3 * x - 1)) == 0
assert g6.subs(x, -4) == 24 and g6.subs(x, -3) == 36 and g6.subs(x, R(1, 3)) == R(-28, 27)
assert all(sgn_at(f + 6 * x, sp.Integer(t)) < 0 for t in range(-20, -4)) and sgn_at(f + 6 * x, sp.Integer(0)) == 0
assert all(sgn_at(f + 6 * x, R(t, 4)) > 0 for t in range(-15, 41) if t != 0)   # x=0 의 좌우에서 부호 그대로
CR6 = [R(-28, 27), R(0), R(24), R(36)]
P6 = profile(-6, CR6)
def expect6(kv):
    if kv < R(-28, 27): return 0
    if kv == R(-28, 27): return 1
    if kv < 24: return 2
    if kv == 24: return 3
    if kv < 36: return 4
    if kv == 36: return 3
    return 2
for kv, c in P6.items(): assert c == expect6(kv), (kv, c)
for kv in [R(24001, 1000), R(35999, 1000), R(23999, 1000), R(-1037, 1000), R(-1036, 1000)]: assert cnt(f, -6 * x, kv) == expect6(kv)   # 경계 바로 옆
print('a=-6: 개수 0(k<-28/27) 1 2 3(k=24) 4(24<k<36) 3(k=36) 2')

# (1) a 는 -6 하나
A1 = [av for av, P in ((-10, P10), (-6, P6)) if max(P.values()) == 4]
assert A1 == [-6]
# (2) 실근 3개인 k: 24, 36 → 합 60
K3 = sorted(kv for kv, c in P6.items() if c == 3)
assert K3 == [24, 36] and sum(K3) == 60
assert sols(f, -6 * x, 24) == {-4, -sp.sqrt(3), sp.sqrt(3)}                    # 꺾인 점 x=-4 자신이 근
assert sols(f, -6 * x, 36) == {-6, -3, 2}
# (3) k=30: 네 실근의 합 -9
s30 = sols(f, -6 * x, 30)
assert len(s30) == 4 and -5 in s30 and sp.nsimplify(sp.N(sum(s30), 50)) == -9
cub = sp.Poly(x**3 + 4 * x**2 - 3 * x - 15, x)
assert sp.expand(g6 - 30 - 2 * cub.as_expr()) == 0 and len(sp.real_roots(cub)) == 3
assert all(r > -4 for r in sp.real_roots(cub))                                 # 세 근 모두 x≥-4 조각
assert -cub.all_coeffs()[1] / cub.all_coeffs()[0] == -4
ANS = (-6, 60, -9)
assert S['ans'] == ['(1) \\(-6\\)', '(2) 60', '(3) \\(-9\\)']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'M56' and S.get('cand') == 'claudeS2'
assert S['core']['axis'] == '②' and '함정 추가' not in S['vtype'] and S['bunseok'] is False
assert S['body'].count(r'\[') == 1 and S['body'].rstrip().endswith('답하시오.')
print('S2 OK: (1) a=-6, (2) 24+36=60, (3) -5+(-4)=-9')

# ---------- 오답 근거
assert sp.factor(f + 10 * x) == x * (x + 2)**2                                  # (1) 원문식 부호=x 부호 후보 -10
assert 36 + R(-28, 27) == R(944, 27)                                             # (2) 극값 경계로 944/27
assert K3[1] == 36                                                               # (2) 꺾인 점 놓치면 36
assert sum(sp.real_roots(cub)).equals(-4) or sp.nsimplify(sp.N(sum(sp.real_roots(cub)), 40)) == -4   # (3) 직선 조각 근 빠뜨려 -4
print('오답 근거 OK: (1) -10 · {-6,-10}, (2) 36 · 944/27, (3) -4')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄 유지)
# 원문 설정 줄 '절댓값 안 부호 = x 의 부호 → x=0 에서 갈라 x<0 은 직선, x≥0 은 삼차' 를 a=-6 에 적용하면
wrong_split = lambda kv: (set(r for r in sp.real_roots(sp.Poly(6 * x + kv, x)) if r < 0) |
                          set(r for r in sp.real_roots(sp.Poly(g6 - kv, x)) if r >= 0))
WS = {kv: len(wrong_split(kv)) for kv in P6}
assert max(WS.values()) == 2                                                     # 4근 k 가 없다고 판정 → a 를 정할 수 없음
assert any(WS[kv] != P6[kv] for kv in P6)
assert sp.discriminant(x**2 + 4 * x, x) > 0                                      # a=-6 의 이차인수 x^2+4x 는 항상 양수가 아님
# 원문 설정이 실제로 통하는 후보(a=-10, x(x+2)^2)는 4근이 없어 기각 → 설정 줄 불통
assert max(P10.values()) == 2
print('핵심 한 줄: 원문 설정 줄(부호=x 부호, x=0 에서 갈림) 불통 — a=-6 에 쓰면 4근 k 없음(틀린 판정), 그 설정이 맞는 a=-10 은 기각; 원리 줄(수평선 교점 개수) 유지')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def has4(av):
    """실근 4개인 k 가 있는지: 임계값(꺾인 점 높이·극값) 사이 대표점으로 조사"""
    av = sp.nsimplify(av)
    gg = 2 * f - av * x
    cand = [R(0)]
    for r in sp.real_roots(sp.Poly(sp.expand(f - av * x), x)):
        cand.append(sp.nsimplify(gg.subs(x, r)) if r.is_rational else sp.N(gg.subs(x, r), 30))
    for c in sp.real_roots(sp.Poly(sp.diff(gg, x), x)):
        cand.append(sp.nsimplify(gg.subs(x, c)) if c.is_rational else sp.N(gg.subs(x, c), 30))
    cand = sorted(set(float(c) for c in cand))
    probes = [sp.nsimplify(round((cand[i] + cand[i + 1]) / 2, 6)) for i in range(len(cand) - 1)] + [sp.nsimplify(round(c, 6)) for c in cand if abs(c - round(c)) < 1e-12]
    return any(cnt(f, av * x, kv) == 4 for kv in probes)

def ablation(cname, res, why=''):
    base = (-6, 60, -9)
    if res == base: msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    else: msg = f'필요({res}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg

out = []
# 1) '곡선과 직선이 서로 다른 두 점에서 만난다' 제거: 4근 k 가 있는 a 가 구간으로 여럿
A_no2 = [av for av in [R(-12), R(-10), R(-9), R(-8), R(-7), R(-6), R(-5), R(-4), R(-2), R(-1), R(0), R(1)] if has4(av)]
assert -6 in A_no2 and len(A_no2) >= 5, A_no2
out.append(ablation("'곡선 y=f(x)와 직선 y=ax가 서로 다른 두 점에서 만난다'", ('정해지지 않음: a ∈ ' + str(A_no2), '없음', '없음'), why='4근 k 가 있는 a 가 -10<a<0 쪽에 여럿'))
# 2) '4근 k 가 존재' 제거: a 후보 -6, -10 둘
out.append(ablation("'실근의 개수가 4가 되도록 하는 실수 k가 존재'", ('정해지지 않음: a ∈ [-10, -6]', '없음', '없음'), why='a=-10 이면 (2)의 3근 k 없음(개수 최대 2)'))
assert not any(c == 3 for c in P10.values())
# 3) '서로 다른' 제거(겹친 근 포함 두 점 → 의미 없음) 대신 '두 점' → '세 점': 4근 k 는 있으나 a 가 정해지지 않음
A3 = [av for av in [R(-9), R(-8), R(-5), R(-4), R(-2), R(-1)] if meet(av) == 3 and has4(av)]
assert len(A3) >= 4
out.append(ablation("'두 점'(→ 세 점)", ('정해지지 않음: a ∈ ' + str(A3), '없음', '없음'), why='세 점에서 만나는 a 대부분에서 4근 k 존재'))
assert all(r_.startswith('필요') for r_ in out), out
print('ALL OK')
