# -*- coding: utf-8 -*-
# 서답형2 (J66 구조 변경) 검증 · author='claude'
import sympy as sp, os
t, a, s = sp.symbols('t a s', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py')).read(), ns)
S = ns['SITEMS']['S2']
R = sp.Rational


# ---------- 도구 ----------
def changes(p, lo=0, whole=False):
    """다항식 p(t)의 부호가 바뀌는 점(홀수 번 겹친 실근) 목록. whole=False면 t>lo 만, True면 모든 실수 t"""
    p = sp.expand(p)
    if p == 0: return None
    out = []
    if not all(c.is_rational for c in sp.Poly(p, t).all_coeffs()):          # 무리수 계수: 근과 겹친 횟수를 직접
        for r, m in sp.roots(sp.Poly(p, t)).items():
            if m % 2 and r.is_real and (whole or r > lo): out.append(sp.nsimplify(r) if r.is_rational else r)
        return sorted(set(out), key=lambda r: float(r))
    for fac, m in sp.sqf_list(sp.Poly(p, t))[1]:
        if m % 2 == 0: continue
        for r in sp.real_roots(fac):
            if whole or r > lo: out.append(r)
    return sorted(set(out), key=lambda r: float(r))

def distance(p, A, B):
    """시각 A에서 B까지 움직인 거리 ∫|p| (정확한 값)"""
    cut = sorted({r for r in sp.roots(sp.Poly(sp.expand(p), t)) if r.is_real and A < r < B}, key=float)
    pts = [A] + cut + [B]
    return sp.nsimplify(sp.simplify(sum(abs(sp.integrate(p, (t, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))))

def disp(p, A=0, B=2):
    return sp.integrate(p, (t, A, B))


# ---------- 원문 J66: v=-t(t-1)(t-a)(t-2a) (a≥0), 방향 한 번 ⇔ a∈{0,1/2,1}, ∫₀²v 최댓값 4/15
vo = -t * (t - 1) * (t - a) * (t - 2 * a)
crit_o = [R(0), R(1, 2), R(1)]                                   # 근이 겹치는 a (a=0, 2a=1, a=1)
grid_o = sorted(set(crit_o + [R(1, 4), R(3, 4), R(3, 2), R(2), R(5)] + [R(i, 16) for i in range(0, 64)]))
ok_o = [av for av in grid_o if len(changes(vo.subs(a, av))) == 1]
assert ok_o == crit_o, ok_o                                      # 열린구간 (0,1/2),(1/2,1),(1,∞) 에서는 세 번
vals_o = {av: disp(vo.subs(a, av)) for av in ok_o}
assert vals_o == {0: R(-12, 5), R(1, 2): R(-11, 15), 1: R(4, 15)}, vals_o
assert max(vals_o.values()) == R(4, 15)
assert sp.expand(disp(vo) - (R(-12, 5) + 4 * a - R(4, 3) * a**2)) == 0
print('J66 원문 OK: a ∈ {0, 1/2, 1}, 위치의 변화량의 최댓값 4/15')

# ---------- S2: v=(a-t)q(t), q=t^2-at+4
q = t**2 - a * t + 4
v = sp.expand((a - t) * q)
assert sp.expand(v - (-t**3 + 2 * a * t**2 - (a**2 + 4) * t + 4 * a)) == 0
assert sp.expand(q.subs(t, a)) == 4                                          # t=a 는 q의 근이 아님(겹침 없음)
assert sp.expand(sp.discriminant(q, t) - (a**2 - 16)) == 0                   # D=a^2-16
# --- 기호 증명(경우 셋)
# (i) a≤0: t>0 에서 q(t)=t^2+(-a)t+4>0, a-t<0 → v<0, 바뀜 0번
# (ii) 0<a≤4: D≤0 → q≥0(모든 t), t=a 는 v의 단순근(q(a)=4) → 바뀜은 t=a 한 번
# (iii) a>4: D>0, 두 근의 합 a>0·곱 4>0 → 서로 다른 두 양의 근, 둘 다 a 아님 → 세 번
assert sp.solve_univariate_inequality(a**2 - 16 <= 0, a, relational=False) == sp.Interval(-4, 4)
r1, r2 = (a - sp.sqrt(a**2 - 16)) / 2, (a + sp.sqrt(a**2 - 16)) / 2
assert sp.simplify(sp.expand(q - (t - r1) * (t - r2))) == 0
assert sp.simplify(r1 * r2) == 4 and sp.simplify(r1 + r2) == a
assert sp.solve(sp.Eq(q.subs(t, a), 0), a) == []                             # 어떤 a에서도 t=a 와 q의 근이 겹치지 않음
assert sp.factor(q.subs(a, 4)) == (t - 2)**2 and changes(v.subs(a, 4)) == [4]
assert changes(v.subs(a, 0)) == []                                           # a=0: t=0 은 출발 시각
# --- 전수 조사: 임계값(-4, 0, 4)과 그 사이·바깥 대표점 + 촘촘한 격자 + 무리수 표본
CR = [R(-4), R(0), R(4)]
grid = sorted(set(CR + [R(i, 8) for i in range(-80, 81)]), key=float)
extra = [2 * sp.sqrt(3), sp.sqrt(17), sp.sqrt(2), -sp.sqrt(20)]
cnt = {av: len(changes(v.subs(a, av))) for av in grid + extra}
for av, c in cnt.items():
    exp_c = 0 if av <= 0 else (1 if av <= 4 else 3)
    assert c == exp_c, (av, c)
OK = [av for av in grid if cnt[av] == 1]
assert all((0 < av <= 4) == (av in OK) for av in grid)
for av in OK + [2 * sp.sqrt(3)]:
    assert changes(v.subs(a, av)) == [av]                                    # 운동 방향을 바꾸는 시각은 t=a
# (1) a의 값의 범위: 0<a≤4
A1 = sp.Interval.Lopen(0, 4)
assert all((av in A1) == (av in OK) for av in grid)
# (2) 시각 0에서 운동 방향을 바꾸는 시각 t=a 까지 움직인 거리: 0<t<a 에서 v≥0 이므로 ∫₀^a v
X = sp.expand(sp.integrate(v, (t, 0, a)))
assert X == 2 * a**2 - a**4 / 12
for av in OK + [2 * sp.sqrt(3)]:
    assert all(sp.N(v.subs({a: av, t: av * R(k, 20)})) >= 0 for k in range(1, 20))
    assert sp.simplify(distance(v.subs(a, av), 0, av) - X.subs(a, av)) == 0, av
# 빠른 풀이: q(a-t)=q(t) → 2X = a∫₀^a q
assert sp.expand(q.subs(t, a - t) - q) == 0
assert sp.expand(2 * X - a * sp.integrate(q, (t, 0, a))) == 0
# (3) X(a)의 최댓값 (0<a≤4): f'(a)=a(12-a^2)/3, 안쪽 a=2√3 에서 최대 12
fX = sp.Lambda(a, X)
crit = [c for c in sp.solve(sp.diff(X, a), a) if c in A1]
assert crit == [2 * sp.sqrt(3)]
assert sp.expand(X - (12 - (a**2 - 12)**2 / 12)) == 0
assert fX(2 * sp.sqrt(3)) == 12 and fX(4) == R(32, 3) and sp.limit(X, a, 0, '+') == 0
assert sp.maximum(X, a, A1) == 12
assert all(X.subs(a, av) < 12 for av in OK)                                  # 격자(유리수) 어디서도 12에 닿지 않음 → 최대는 a=2√3 하나
ANS = (A1, X, sp.Integer(12))
assert S['ans'] == [r'(1) \(0&lt;a\le4\)', r'(2) \(2a^2-\dfrac{a^4}{12}\)', '(3) 12']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'J66' and S.get('cand') == 'claudeS2'
assert S['core']['axis'] == '②' and '함정 추가' not in S['vtype'] and S['bunseok'] is False
assert S['body'].rstrip().endswith('답하시오.') and '\n\n' not in S['body'] and not S.get('after')
print('S2 OK: (1) 0<a≤4, (2) 2a^2-a^4/12, (3) 12 (a=2√3)')

# ---------- 오답 근거
assert sp.solve_univariate_inequality(a**2 - 16 <= 0, a, relational=False) == sp.Interval(-4, 4)   # (1) 판별식만: -4≤a≤4
assert changes(v.subs(a, 4)) == [4] and sp.factor(q.subs(a, 4)) == (t - 2)**2                  # (1) a=4 에서 t=2 를 세면 0<a<4
assert sp.real_roots(sp.Poly(v.subs(a, 0), t)) == [0]                                          # (1) t=0 을 세면 0≤a≤4
assert sp.expand(-a**4 / 4 + 2 * a**4 / 3 - a**2 * a**2 / 2 + 4 * a**2) == 4 * a**2 - a**4 / 12  # (2) 4 빠뜨림
assert fX(4) == R(32, 3)                                                                       # (3) 구간 끝만: 32/3
print('오답 근거 OK: (1) -4≤a≤4 · 0<a<4 · 0≤a≤4, (2) 4a^2-a^4/12, (3) 32/3 · 2√3')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄 유지)
# 원문 설정 줄 '드러난 근이 겹치거나 0으로 모이는 a만 대입'을 쓰면: 겹침 a 없음(q(a)=4), a=0 은 바뀜 0번 → 후보 없음
cand_setting = [av for av in [R(0)] + sp.solve(q.subs(t, a), a) if cnt.get(av, len(changes(v.subs(a, av)))) == 1]
assert cand_setting == []
assert len(OK) > 30                                                          # 실제 답 집합은 구간 → 설정 줄 불통
print('핵심 한 줄: 원문 설정 줄(겹침·0으로 모임 값 대입) 불통 — 후보 0개, 답 집합은 구간 0<a≤4; 원리 줄(부호 바뀜) 유지')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
LO, HI = min(grid), max(grid)
def answers(okset, whole=False):
    """조건을 만족시키는 a 집합(격자) → ((1) 집합, (2) 거리식, (3) 최댓값). 바꾸는 시각이 없거나 여럿이거나 0 이하이면 (2)(3) '없음'"""
    if not okset: return ('없음', '없음', '없음')
    r1_ = tuple(okset)
    times = [changes(v.subs(a, av), whole=whole) for av in okset]
    if any(len(tt) != 1 or tt[0] <= 0 for tt in times): return (r1_, '없음', '없음')
    if any(tt[0] != av for tt, av in zip(times, okset)): return (r1_, '없음', '없음')
    return (r1_, X, '없음' if (LO in okset or HI in okset) else sp.maximum(X, a, sp.Interval(min(okset), max(okset))))

def ablation(cname, res, why=''):
    base = (tuple(OK), X, sp.Integer(12))
    def rng(x):
        lo_ = '−∞' if min(x) == LO else f'{min(x)}'
        hi_ = '∞' if max(x) == HI else f'{max(x)}'
        return f'a 범위 [{lo_}, {hi_}] 쪽 (격자 {len(x)}점)'
    show = lambda i, x: ('그대로' if x == base[i] else ('없음' if x == '없음' else (rng(x) if i == 0 else str(x))))
    if res == base:
        msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    else:
        parts = [f'({i + 1}) ' + show(i, res[i]) for i in range(3)]
        kind = '정해지지 않음' if '없음' in res else '답 바뀜'
        msg = f'필요({kind}: {", ".join(parts)}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg

out = []
assert answers(OK) == (tuple(OK), X, 12)
# 1) 방향 조건 전체 제거: 모든 실수 a
out.append(ablation("'운동 방향을 한 번만 바꿀 때' 전체", answers(grid), why='a≤0 이면 바꾸는 시각 없음, a>4 이면 세 개'))
# 2) '한 번만' 제거(운동 방향을 바꿀 때): a>0 전체
out.append(ablation("'한 번만'(→ 운동 방향을 바꿀 때)", answers([av for av in grid if cnt[av] >= 1]), why='a>4 이면 바꾸는 시각이 세 개'))
# 3) 't≥0'·'시각 t=0일 때 출발한' 제거: 모든 실수 t에서 부호가 한 번만 바뀜 → -4≤a≤4
cw = {av: len(changes(v.subs(a, av), whole=True)) for av in grid}
OKw = [av for av in grid if cw[av] == 1]
assert all((-4 <= av <= 4) == (av in OKw) for av in grid)
out.append(ablation("'t≥0, 시각 t=0일 때 출발한'(→ 모든 실수 t)", answers(OKw, whole=True), why='음수 a 도 들어와 -4≤a≤4, 바꾸는 시각 t=a 가 음수일 수 있음'))
# 4) '한 번만' → '바꾸지 않을 때'(0번): a≤0
out.append(ablation("'한 번만'(→ 운동 방향을 바꾸지 않을 때)", answers([av for av in grid if cnt[av] == 0]), why='a≤0, 바꾸는 시각 없음'))
assert all(r_.startswith('필요') for r_ in out), out
print('ALL OK')
