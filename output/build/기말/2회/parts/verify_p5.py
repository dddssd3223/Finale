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

# ---------- S2: f=x^3+4x^2-6x, 곡선 y=f(x)와 직선 y=ax 가 서로 다른 두 점에서 만남, f+|f-ax|=mx 가 세 실근인 m 존재
f = x**3 + 4 * x**2 - 6 * x
def meet(av):
    return len(set(sp.real_roots(sp.Poly(sp.expand(f - av * x), x))))
# --- '두 점에서 만남'의 기호 풀이: f-ax = x(x^2+4x-(a+6))
assert sp.expand(f - a * x - x * (x**2 + 4 * x - (a + 6))) == 0
qd = x**2 + 4 * x - (a + 6)
assert sp.solve(qd.subs(x, 0), a) == [-6] and sp.solve(sp.discriminant(qd, x), a) == [-10]
assert sp.factor(f + 6 * x) == x**2 * (x + 4) and sp.factor(f + 10 * x) == x * (x + 2)**2
# 판별식 4(a+10): a<-10 이면 한 점, a>-10·a≠-6 이면 세 점
assert sp.expand(sp.discriminant(qd, x) - 4 * (a + 10)) == 0
gridA = sorted(set([R(i, 4) for i in range(-80, 41)] + [R(-6), R(-10)]))
TWO = [av for av in gridA if meet(av) == 2]
assert TWO == [-10, -6], TWO
for av in gridA:
    assert meet(av) == (2 if av in (-10, -6) else (1 if av < -10 else 3))

def cntm(av, mv):
    """f+|f-ax| = mx 의 서로 다른 실근 개수 (무수히 많으면 inf)"""
    return cnt(f, av * x, 0, mv * x)

# --- 각 후보의 실근 개수 (임계값 + 촘촘한 격자)
gridM = sorted(set([R(i, 8) for i in range(-240, 161)] + [R(-14), R(-6), R(-10), R(-2)]), key=float)
# a=-10: x<0 에서 -10x, x≥0 에서 2x^3+8x^2-2x (원문 설정이 통하는 후보)
P10 = {mv: cntm(-10, mv) for mv in gridM}
assert P10[-10] == float('inf')
assert max(c for c in P10.values() if c != float('inf')) == 2
assert all(c != 3 for c in P10.values())
print('a=-10: 실근 개수 최대 2(m=-10 이면 무수히 많음) → 세 실근인 m 없음, 기각')

# a=-6: x<-4 에서 -6x, x≥-4 에서 2x^3+8x^2-6x
h6 = 2 * f + 6 * x
assert sp.expand(h6 - (2 * x**3 + 8 * x**2 - 6 * x)) == 0
assert all(sgn_at(f + 6 * x, sp.Integer(t)) < 0 for t in range(-20, -4)) and sgn_at(f + 6 * x, sp.Integer(0)) == 0
assert all(sgn_at(f + 6 * x, R(t, 4)) > 0 for t in range(-15, 41) if t != 0)   # x=0 의 좌우에서 부호 그대로
# 원점에서 그은 접선: h(t)=t h'(t) → t=0, -2, 기울기 -6, -14 / 끝점 (-4,24) 를 지나는 기울기 -6
tt = sp.solve(sp.expand(h6 - x * sp.diff(h6, x)), x)
assert sorted(tt) == [-2, 0] and {sp.diff(h6, x).subs(x, t_) for t_ in tt} == {-6, -14}
assert h6.subs(x, -4) == 24 and R(24, -4) == -6
ms = sp.Symbol('m')
assert sp.expand(h6 - ms * x - x * (2 * x**2 + 8 * x - 6 - ms)) == 0
P6 = {mv: cntm(-6, mv) for mv in gridM}
def expect6(mv):
    if mv < -14: return 1
    if mv == -14: return 2
    if mv < -6: return 3
    if mv == -6: return float('inf')
    return 2
for mv, c in P6.items(): assert c == expect6(mv), (mv, c)
for mv in [R(-14001, 1000), R(-13999, 1000), R(-6001, 1000), R(-5999, 1000)]: assert cntm(-6, mv) == expect6(mv)
assert all(0 in sols(f, -6 * x, 0, mv * x) for mv in gridM if mv != -6)       # 원점(접점)은 항상 근
print('a=-6: 개수 1(m<-14) 2(m=-14) 3(-14<m<-6) 무수히(m=-6) 2(m>-6)')

# (1) a 는 -6 하나
A1 = [av for av, P in ((-10, P10), (-6, P6)) if 3 in P.values()]
assert A1 == [-6]
# (2) 세 실근인 정수 m: -13..-7 → 7개
M3 = [mv for mv in range(-40, 41) if cntm(-6, mv) == 3]
assert M3 == list(range(-13, -6)) and len(M3) == 7
# (3) m=4: 0, 1 (x=-5 는 x≥-4 밖) → 합 1
assert sp.factor(h6 - 4 * x) == 2 * x * (x - 1) * (x + 5)
s4 = sols(f, -6 * x, 0, 4 * x)
assert s4 == {0, 1} and sum(s4) == 1
assert sgn_at(f + 6 * x, sp.Integer(-5)) < 0                                   # x=-5 에서는 g=-6x 조각 → 30 ≠ -20
assert S['ans'] == ['(1) \\(-6\\)', '(2) 7', '(3) 1']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'M56' and S.get('cand') == 'claudeS2'
assert S['core']['axis'] == '②' and '함정 추가' not in S['vtype'] and S['bunseok'] is False
assert S['body'].count(r'\[') == 1 and S['body'].rstrip().endswith('답하시오.')
print('S2 OK: (1) a=-6, (2) 정수 m -13..-7 → 7, (3) 0+1=1')

# ---------- 오답 근거
assert sp.factor(f + 10 * x) == x * (x + 2)**2                                  # (1) 원문식 부호=x 부호 후보 -10
assert len(M3) + 1 == 8 and P6[-6] == float('inf')                              # (2) m=-6 까지 넣으면 8
assert all(sp.discriminant(2 * x**2 + 8 * x - 6 - mv, x) > 0 for mv in range(-13, 40))  # (2) 판별식만 보면 m>-14 전부
assert sum(sp.roots(sp.Poly(h6 - 4 * x, x)).keys()) == -4                        # (3) x=-5 까지 넣으면 -4
print('오답 근거 OK: (1) -10 · {-6,-10}, (2) 8 · m>-14, (3) -4')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄 유지)
# 원문 설정 줄 '절댓값 안 부호 = x 의 부호 → x=0 에서 갈라 x<0 은 직선, x≥0 은 삼차' 를 a=-6 에 적용하면
def wrong_split(mv):
    if mv == -6: return float('inf')
    return len({r for r in sp.real_roots(sp.Poly(h6 - mv * x, x)) if r >= 0})
WS = {mv: wrong_split(mv) for mv in gridM}
assert max(c for c in WS.values() if c != float('inf')) == 2                    # 세 실근인 m 이 없다고 판정 → a 를 정할 수 없음
assert any(WS[mv] != P6[mv] for mv in gridM)
assert sp.discriminant(x**2 + 4 * x, x) > 0                                      # a=-6 의 이차인수 x^2+4x 는 항상 양수가 아님
assert max(c for c in P10.values() if c != float('inf')) == 2                   # 원문 설정이 맞는 a=-10 은 기각
# 원문 원리 줄 '직선 조각의 치역 + 극값 비교' : 직선 조각은 m≠-6 이면 근 0개, 경계 -14·-6 은 극값이 아닌 접선·끝점 기울기
assert all(not any(sgn_at(f + 6 * x, r) < 0 for r in sp.real_roots(sp.Poly((-6 - mv) * x, x))) for mv in gridM if mv != -6)
print('핵심 한 줄: 원문 설정 줄 불통 — a=-6 에 쓰면 세 실근 m 없음(틀린 판정), 그 설정이 맞는 a=-10 은 기각; 직선 조각은 근을 주지 않고 경계는 접선(-14)·끝점(-6) 기울기')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def has3(av):
    return any(cntm(av, mv) == 3 for mv in [R(i, 2) for i in range(-80, 41)])
def ablation(cname, res, why=''):
    base = (-6, 7, 1)
    msg = f'군더더기(답 그대로{"; " + why if why else ""})' if res == base else f'필요({res}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg
out = []
# 1) '곡선 y=f(x)와 직선 y=ax가 서로 다른 두 점에서 만난다' 제거
A_no2 = [av for av in [R(-12), R(-10), R(-9), R(-8), R(-7), R(-6), R(-5), R(-4), R(-2), R(0), R(2)] if has3(av)]
assert -6 in A_no2 and len(A_no2) >= 5, A_no2
out.append(ablation("'곡선 y=f(x)와 직선 y=ax가 서로 다른 두 점에서 만난다'", ('정해지지 않음: a ∈ ' + str(A_no2), '없음', '없음'), why='세 실근인 m 이 있는 a 가 a>-10 쪽에 여럿'))
# 2) '세 실근인 m 존재' 제거: a 후보 -6, -10 둘
assert sorted(TWO) == [-10, -6] and not has3(-10)
out.append(ablation("'서로 다른 세 실근을 갖도록 하는 실수 m이 존재'", ('정해지지 않음: a ∈ [-10, -6]', '없음', '없음'), why='a=-10 이면 (2)의 정수 m 0개, (3) m=4 의 실근 0, -2+√7 (합 -2+√7)'))
assert sols(f, -10 * x, 0, 4 * x) == {0, -2 + sp.sqrt(7)}
# 3) '두 점' → '세 점'
A3 = [av for av in [R(-9), R(-8), R(-5), R(-4), R(-2), R(2)] if meet(av) == 3 and has3(av)]
assert len(A3) >= 4
out.append(ablation("'두 점'(→ 세 점)", ('정해지지 않음: a ∈ ' + str(A3), '없음', '없음'), why='세 점에서 만나는 a 대부분에서 세 실근인 m 존재'))
assert all(r_.startswith('필요') for r_ in out), out
print('ALL OK')
