# -*- coding: utf-8 -*-
# 서답형2 (J66 구조 변경) 검증 · author='claude'
import sympy as sp, os
t, a, u = sp.symbols('t a u', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4.py')).read(), ns)
S = ns['SITEMS']['S2']
R = sp.Rational


# ---------- 도구 ----------
def changes(p, lo=0, whole=False):
    """다항식 p(t)의 부호가 바뀌는 점(홀수 번 겹친 실근) 목록. whole=False면 t>lo 만, True면 모든 실수 t"""
    p = sp.expand(p)
    if p == 0: return None
    out = []
    for fac, m in sp.sqf_list(sp.Poly(p, t))[1]:
        if m % 2 == 0: continue
        for r in sp.real_roots(fac):
            if whole or r > lo: out.append(r)
    return sorted(set(out), key=lambda r: float(r))

def distance(p, A=0, B=2):
    """시각 A에서 B까지 움직인 거리 ∫|p| (정확한 값)"""
    cut = sorted({r for r in sp.real_roots(sp.Poly(sp.expand(p), t)) if A < r < B}, key=float)
    pts = [A] + cut + [B]
    return sp.nsimplify(sum(abs(sp.integrate(p, (t, pts[i], pts[i + 1]))) for i in range(len(pts) - 1)))

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

# ---------- S2 전수 풀이: v=(1-t)q(t), q=t^2-2at+a+2
q = t**2 - 2 * a * t + a + 2
v = sp.expand((1 - t) * q)
assert sp.expand(sp.discriminant(q, t) / 4 - (a + 1) * (a - 2)) == 0      # D/4=(a+1)(a-2)
assert sp.expand(q.subs(t, 1) - (3 - a)) == 0 and q.subs(t, 0) == a + 2
# q의 근 배치가 바뀌는 a: 판별식 0(a=-1,2), 근이 t=0을 지남(a=-2), 근이 t=1을 지남(a=3)
CR = [R(-2), R(-1), R(2), R(3)]
assert sorted(set(sp.solve(sp.discriminant(q, t), a)) | {sp.solve(q.subs(t, 0), a)[0], sp.solve(q.subs(t, 1), a)[0]}) == CR
# 각 임계값과 그 사이(및 바깥) 구간의 대표점 + 촘촘한 격자로 전수 조사
reps = CR + [R(-3), R(-3, 2), R(0), R(5, 2), R(4)]
grid = sorted(set(reps + [R(i, 16) for i in range(-160, 161)]))
cnt = {av: len(changes(v.subs(a, av))) for av in grid}
OK = [av for av in grid if cnt[av] == 1]
assert all((-2 <= av <= 2 or av == 3) == (cnt[av] == 1) for av in grid)
assert all(cnt[av] == 2 for av in grid if av < -2)                          # 양의 근 하나 + t=1
assert all(cnt[av] == 3 for av in grid if 2 < av and av != 3)                # 두 양의 근 + t=1
assert changes(v.subs(a, 3)) == [5] and changes(v.subs(a, 2)) == [1] and changes(v.subs(a, -2)) == [1]
assert sp.factor(v.subs(a, 3)) == sp.factor(-(t - 1)**2 * (t - 5))
assert sp.factor(q.subs(a, 2)) == (t - 2)**2 and sp.factor(q.subs(a, -2)) == t * (t + 4)
# 구간 [-2,2] 전체에서 t>0 이면 q(t)≥0 (기호 증명): -1≤a≤2 는 판별식≤0, -2≤a<-1 은 큰 근 a+√(a²-a-2) ≤ 0
assert sp.solve_univariate_inequality((a + 1) * (a - 2) <= 0, a, relational=False) == sp.Interval(-1, 2)
big = a + sp.sqrt(a**2 - a - 2)
assert sp.solve_univariate_inequality(sp.sqrt(a**2 - a - 2) <= -a, a, relational=False).intersect(sp.Interval(-sp.oo, -1)) == sp.Interval(-2, -1)
for av in [R(-2), R(-7, 4), R(-3, 2), R(-5, 4), R(-1)]:
    assert sp.simplify(big.subs(a, av)) <= 0
# (1) a의 최댓값, (2) a의 최솟값
A1, A2 = max(OK), min(OK)
assert (A1, A2) == (3, -2)
# (3) 시각 0에서 2까지 움직인 거리의 최솟값: -2≤a≤2 이면 ∫₀¹v-∫₁²v = 7/2-a, a=3 이면 8/3
I01, I12 = sp.integrate(v, (t, 0, 1)), sp.integrate(v, (t, 1, 2))
assert sp.expand(I01 - (R(13, 12) + a / 6)) == 0 and sp.expand(I12 - (R(-29, 12) + 7 * a / 6)) == 0
Dlin = sp.expand(I01 - I12)
assert Dlin == R(7, 2) - a
for av in [R(i, 8) for i in range(-16, 17)]:                                # 직접 계산과 일치
    assert distance(v.subs(a, av)) == Dlin.subs(a, av), av
assert distance(v.subs(a, 3)) == R(8, 3) and disp(v.subs(a, 3)) == R(8, 3)  # a=3: [0,2]에서 v≥0
# 빠른 풀이 t=u+1: v=-u{u^2+(2-2a)u+3-a}
assert sp.expand(v.subs(t, u + 1) + u * (u**2 + (2 - 2 * a) * u + 3 - a)) == 0
assert sp.integrate(2 * (u**3 + (3 - a) * u), (u, 0, 1)) == Dlin
Dset = {av: distance(v.subs(a, av)) for av in OK}
A3 = min(Dset.values())
assert A3 == R(3, 2) and [av for av in OK if Dset[av] == A3] == [2]          # 최솟값은 a=2 에서만
assert all(Dset[av] > A3 for av in OK if av != 2)
ANS = (A1, A2, A3)
assert S['ans'] == ['(1) 3', '(2) -2', r'(3) \(\dfrac32\)']
assert [s_[1][:2] for s_ in S['subs']] == ['4점', '4점', '2점'] and all('답만' in s_[1] for s_ in S['subs'])
assert S.get('author') == 'claude' and S['key'] == 'J66' and S.get('cand') == 'claudeS2'
assert S['core']['axis'] == '②' and '함정 추가' not in S['vtype'] and S['bunseok'] is False
print('S2 OK: (1) 3, (2) -2, (3) 3/2')

# ---------- 오답 근거
assert max(av for av in grid if (av + 1) * (av - 2) <= 0) == 2                 # (1) 판별식만: 2
assert min(av for av in grid if (av + 1) * (av - 2) <= 0) == -1                # (2) 판별식만: -1
assert all(Dset[av] > R(3, 2) for av in OK if av < 2) and Dset[3] == R(8, 3)  # (3) a=2 를 빼면 -2≤a<2 에서 최솟값 없음 → a=3 의 8/3
assert sp.expand(disp(v) - (4 * a - 4) / 3) == 0 and min(disp(v.subs(a, av)) for av in OK) == -4   # 변화량으로: -4
assert max(Dset.values()) == R(11, 2) and Dset[-2] == R(11, 2)                # 최댓값: 11/2
print('오답 근거 OK: (1) 2, (2) -1, (3) 8/3 · -4 · 11/2')

# ---------- 원문 핵심 한 줄 테스트 (②형: 설정 줄 불통, 원리 줄 유지)
# 원문 설정 줄 '드러난 근이 겹치거나 0으로 모이는 a만 본다'를 그대로 쓰면 후보는 근 배치가 바뀌는 유한 개 a뿐
cand_setting = [av for av in CR if cnt[av] == 1]
assert cand_setting == [-2, -1, 2, 3]
assert any(cnt[av] == 1 and av not in CR for av in grid)                     # 실제 답 집합에는 구간 [-2,2] 가 있음 → 불통
assert len([av for av in OK if av not in CR]) == 62   # -2<a<2 의 격자점 (a=-1 제외)
print('핵심 한 줄: 원문 설정 줄(유한 개 a 대입) 불통 — 답 집합에 구간 -2≤a≤2 포함; 원리 줄(부호 바뀜) 유지')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def answers(okset):
    """조건을 만족시키는 a 집합(격자) → (최댓값, 최솟값, 거리 최솟값). 격자 끝에 닿으면 '없음'(유계 아님)"""
    if not okset: return ('없음', '없음', '없음')
    mx = '없음' if max(okset) == max(grid) else max(okset)
    mn = '없음' if min(okset) == min(grid) else min(okset)
    ds = [Dset.get(av) if av in Dset else distance(v.subs(a, av)) for av in okset]
    lo = min(ds)
    dm = '없음' if any(okset[i] in (min(grid), max(grid)) for i, d_ in enumerate(ds) if d_ == lo) else lo
    return (mx, mn, dm)

def ablation(cname, res, why=''):
    if res == ANS:
        msg = f'군더더기(답 그대로{"; " + why if why else ""})'
    else:
        parts = [f'({i + 1}) ' + ('그대로 ' + str(ANS[i]) if res[i] == ANS[i] else str(res[i])) for i in range(3)]
        kind = '정해지지 않음' if '없음' in res else '답 바뀜'
        msg = f'필요({kind}: {", ".join(parts)}{"; " + why if why else ""})'
    print(f'ABLATION S2 {cname}: {msg}')
    return msg

out = []
assert answers(OK) == ANS
# 1) 방향 조건 전체 제거: 모든 실수 a
out.append(ablation("'운동 방향을 한 번만 바꿀 때' 전체", answers(grid), why='a 제한 없음'))
# 2) '한 번만' 제거(운동 방향을 바꿀 때): 모든 a에서 적어도 한 번 바뀜
assert all(cnt[av] >= 1 for av in grid)
out.append(ablation("'한 번만'(→ 운동 방향을 바꿀 때)", answers([av for av in grid if cnt[av] >= 1]), why='모든 a에서 t=1 또는 t=5에서 바뀜'))
# 3) 't≥0'·'시각 t=0일 때 출발한' 제거: 모든 실수 t에서 부호가 한 번만 바뀜 → -1≤a≤2 또는 a=3
cw = {av: len(changes(v.subs(a, av), whole=True)) for av in grid}
OKw = [av for av in grid if cw[av] == 1]
assert all((-1 <= av <= 2 or av == 3) == (av in OKw) for av in grid)
out.append(ablation("'t≥0, 시각 t=0일 때 출발한'(→ 모든 실수 t)", answers(OKw), why='음의 근도 세어 -2≤a<-1 이 빠짐'))
# 4) '한 번만' → '바꾸지 않을 때'(0번): 해 없음
out.append(ablation("'한 번만'(→ 운동 방향을 바꾸지 않을 때)", answers([av for av in grid if cnt[av] == 0]), why='t=1 또는 t=5에서 반드시 바뀜'))
assert all(r_.startswith('필요') for r_ in out), out
print('ALL OK')
