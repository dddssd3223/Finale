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

# ---------- S2: f=x^3+6x^2-6x, 원점에서의 접선 y=ax, f+|f-ax|=-24x+k
f = x**3 + 6 * x**2 - 6 * x
RHS = -24 * x
def cntk(av, kv):
    return cnt(f, av * x, kv, RHS)
A_ = sp.diff(f, x).subs(x, 0)
assert A_ == -6 and sp.expand(f.subs(x, 0)) == 0                                 # 원점에서의 접선 y=-6x
assert sp.factor(f + 6 * x) == x**2 * (x + 6)
# (1) f(x) < ax 의 해: x<-6 (x=0 에서는 부호 그대로)
SOL1 = sp.solve_univariate_inequality(f - A_ * x < 0, x, relational=False)
assert SOL1 == sp.Interval.open(-sp.oo, -6), SOL1
gridK = sorted(set([R(i, 4) for i in range(-600, 161)] + [R(-108), R(-8), R(0)]), key=float)
# --- a=-6: x<-6 에서 G=18x, x≥-6 에서 G=2x(x+3)^2
assert all(sgn_at(f + 6 * x, sp.Integer(t)) < 0 for t in range(-30, -6)) and sgn_at(f + 6 * x, sp.Integer(0)) == 0
assert all(sgn_at(f + 6 * x, R(t, 4)) > 0 for t in range(-23, 41) if t != 0)   # x=0 의 좌우에서 부호 그대로
G6_l = sp.expand(-6 * x + 24 * x); G6_r = sp.expand(2 * f + 6 * x + 24 * x)
assert G6_l == 18 * x and sp.factor(G6_r) == 2 * x * (x + 3)**2
assert sp.expand(G6_r - 2 * (f + 15 * x)) == 0                                  # 기각된 후보의 접점 x=-3 이 극대점
assert sp.expand(sp.diff(G6_r, x) - 6 * (x + 3) * (x + 1)) == 0
assert G6_r.subs(x, -6) == -108 == G6_l.subs(x, -6) and G6_r.subs(x, -3) == 0 and G6_r.subs(x, -1) == -8
assert sp.diff(G6_l, x) > 0 and sp.diff(G6_r, x).subs(x, -6) > 0                # 갈리는 점 좌우 모두 증가 → 극점 아님
P6 = {kv: cntk(-6, kv) for kv in gridK}
def expect6(kv):
    if kv < -8 or kv > 0: return 1
    if kv in (-8, 0): return 2
    return 3
for kv, c in P6.items(): assert c == expect6(kv), (kv, c)
for kv in [R(-8001, 1000), R(-7999, 1000), R(-1, 1000), R(1, 1000), R(-108), R(-10801, 100), R(-10799, 100)]:
    assert cntk(-6, kv) == expect6(kv), kv
assert max(P6.values()) == 3                                                    # 4개는 없음
print('a=-6: 개수 1(k<-8) 2(k=-8) 3(-8<k<0) 2(k=0) 1(k>0); x=-6(높이 -108)은 경계 아님')

# (2) 두 실근인 k: -8, 0 → 합 -8
K2 = sorted(kv for kv, c in P6.items() if c == 2)
assert K2 == [-8, 0] and sum(K2) == -8
assert sols(f, -6 * x, 0, RHS) == {-3, 0} and sols(f, -6 * x, -8, RHS) == {-4, -1}
# (3) 세 실근의 합: -8<k<0 의 모든 k 에서 -6 (세 근 모두 x≥-6 의 삼차 조각)
for kv in [R(-799, 100), R(-5), R(-4), R(-1), R(-1, 100), R(-13, 3)]:
    s3 = sols(f, -6 * x, kv, RHS)
    assert len(s3) == 3 and all(sgn_at(f + 6 * x, r) >= 0 for r in s3)
    assert sp.nsimplify(sp.N(sum(s3), 50)) == -6
assert sp.Poly(G6_r - k, x).all_coeffs()[:2] == [2, 12]
assert S['ans'] == ['(1) \\(x&lt;-6\\)', '(2) \\(-8\\)', '(3) \\(-6\\)']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'M56' and S.get('cand') == 'claudeS2'
assert S['core']['axis'] == '②' and '함정 추가' not in S['vtype'] and S['bunseok'] is False
assert S['body'].count(r'\[') == 1 and S['body'].rstrip().endswith('답하시오.') and '(단' not in S['body']
print('S2 OK: (1) x<-6, (2) -8+0=-8, (3) -6')

# ---------- 오답 근거
assert sp.solve_univariate_inequality(x < 0, x, relational=False) != SOL1          # (1) 원문식 부호=x 부호: x<0
assert G6_r.subs(x, -6) + 0 == -108 and G6_r.subs(x, -6) - 8 + 0 == -116        # (2) 갈리는 점 높이를 경계로 넣은 값
print('오답 근거 OK: (1) x<0 · x≤-6, (2) -108 · -116')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄 유지)
def wrong_split(kv):
    out = {r for r in sp.real_roots(sp.Poly(G6_l - kv, x)) if r < 0} | {r for r in sp.real_roots(sp.Poly(G6_r - kv, x)) if r >= 0}
    return len(out)
WS = {kv: wrong_split(kv) for kv in gridK}
assert max(WS.values()) == 1                                                     # x=0 에서 가르면 증가함수로 보여 세 실근 없음(틀린 판정)
assert any(WS[kv] != P6[kv] for kv in gridK)
assert sp.discriminant(x**2 + 6 * x, x) > 0                                      # 이차인수 x^2+6x 는 항상 양수가 아님
assert P6[R(-108)] == P6[R(-108) + R(1, 4)] == P6[R(-108) - R(1, 4)] == 1        # 갈리는 점 높이 -108 은 개수 경계 아님
print('핵심 한 줄: 원문 설정 줄(부호=x 부호, x=0 에서 갈림) 불통 — x=0 에서 가르면 증가함수로 보여 세 실근 없음; 원리(수평선 교점 개수·도함수 극값) 유지, 갈리는 점은 경계 아님')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def answers(av):
    """a 에 대한 ((1) f<ax 해, (2) 두 실근 k 합, (3) 세 근의 합 또는 '없음')"""
    s1 = sp.solve_univariate_inequality(f - av * x < 0, x, relational=False)
    Pk = {kv: cntk(av, kv) for kv in [R(i, 2) for i in range(-300, 121)]}
    k2 = [kv for kv, c in Pk.items() if c == 2]
    k3 = [kv for kv, c in Pk.items() if c == 3]
    s3 = '없음' if not k3 else sp.nsimplify(sp.N(sum(sols(f, av * x, k3[len(k3) // 2], RHS)), 40))
    return (s1, sum(k2) if k2 and len(k2) < 6 else ('없음' if not k2 else '구간'), s3)
def ablation(cname, res, why=''):
    base = (SOL1, -8, -6)
    msg = f'군더더기(답 그대로{"; " + why if why else ""})' if res == base else f'필요({res}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg
out = []
assert answers(-6) == (SOL1, -8, -6)
# 1) '원점에서의 접선' 제거(→ 원점을 지나는 직선 y=ax, a 미정): a 마다 답이 다름
alt = {av: answers(av) for av in [R(-15), R(-10), R(-4)]}
assert all(v != answers(-6) for v in alt.values())
out.append(ablation("'곡선 위의 원점에서의 접선'(→ 원점을 지나는 직선)", ('정해지지 않음: a 마다 다름 ' + str({str(k_): str(v[0]) for k_, v in alt.items()}), '없음', '없음'), why='a=-15 이면 x<0 에서 갈리고 세 실근 없음'))
# 2) 우변의 -24x 를 원문처럼 수평선만(k)으로
P6k = {kv: cnt(f, -6 * x, kv) for kv in [R(i, 2) for i in range(-40, 300)]}
assert max(P6k.values()) == 4 and sorted(kv for kv, c in P6k.items() if c == 2) != [-8, 0]
out.append(ablation("우변 '-24x'(→ 우변 k)", ('(1) 그대로', '바뀜(실근 4개가 생기고 두 실근 k 가 달라짐)', '바뀜'), why='왼쪽 조각이 감소 직선 -6x 가 되어 갈리는 점이 극소'))
assert all(r_.startswith('필요') for r_ in out), out
print('ALL OK')
