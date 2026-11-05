# -*- coding: utf-8 -*-
"""M31 후보(검토 반영): 임계 높이 전수 분류, 합성 극한, 최솟값 유일성(기호+격자), 원문 원리 불통, 오답·빼 보기."""
from fractions import Fraction as F
from pathlib import Path
import runpy
import numpy as np
import sympy as s

x, t, u, m, c = s.symbols('x t u m c', real=True)
R = s.Rational
it = runpy.run_path(str(Path(__file__).with_name('c17.py')))['ITEMS'][17]
assert it['key'] == 'M31' and it['author'] == 'codex' and it['cand'] == 'codex17'
assert '(검토 반영: Claude 수정)' in it['var']
assert '않는다 .' not in it['cond'][0][1] and it['cond'][0][1].endswith('<u>않는</u>다.')


def distinct_real(poly):
    return set(s.Poly(poly, x).real_roots(radicals=False))


def count_abs(poly, height):
    """|poly(x)|=height 의 서로 다른 실근 개수."""
    if height < 0:
        return 0
    if height == 0:
        return len(distinct_real(poly))
    return len(distinct_real(poly-height)) + len(distinct_real(poly+height))


def count_plain(poly, height):
    """절댓값을 뺀 poly(x)=height 의 서로 다른 실근 개수(오답 경로)."""
    return len(distinct_real(poly-height))


eps = R(1, 100)

# ---------- 원문: 답 36 ----------
original = x**3-3*x**2-9*x+10
critical = s.solve(s.diff(original, x), x)
assert critical == [-1, 3]
assert [original.subs(x, v) for v in critical] == [15, -17]
levels_original = [0, 15, 17]
original_h = lambda z: count_abs(original, z)-count_abs(original, z-2)
candidates = sorted(set(levels_original + [v+2 for v in levels_original]))
discontinuous = [z for z in candidates
                 if len({original_h(z-eps), original_h(z), original_h(z+eps)}) > 1]
assert discontinuous == [0, 2, 15, 19]
assert sum(discontinuous) == 36
assert [original_h(17-eps), original_h(17), original_h(17+eps)] == [-2]*3
print('원문 M31: 불연속점 [0, 2, 15, 19], 합 36 OK')

# ---------- 후보: f=4x^3-12x+2 ----------
f = 4*x**3-12*x+2
assert s.expand(s.diff(f, x)-12*(x-1)*(x+1)) == 0
assert [f.subs(x, z) for z in [-1, 1]] == [10, -6]          # 극솟값 음수 → 절댓값이 일한다
levels = sorted({0} | {abs(f.subs(x, z)) for z in [-1, 1]})
assert levels == [0, 6, 10]
heights = [-1, 0, 1, 6, 7, 10, 11]
assert [count_abs(f, z) for z in heights] == [0, 3, 6, 5, 4, 3, 2]
# 점프 높이 전수: 임계 높이 사이 표본과 임계 높이에서 g 값을 비교한다.
side_counts = {z: (count_abs(f, z-eps), count_abs(f, z+eps)) for z in levels}
assert side_counts == {0: (0, 6), 6: (6, 4), 10: (4, 2)}
assert all(a != b for a, b in side_counts.values())


def bad_points(q, lv=levels, sc=side_counts):
    """각 점의 국소 전개: 홀수 차수로 높이를 통과할 때만 양쪽 극한이 다르다."""
    result = set()
    for height in lv:
        for root, mult in s.roots(s.Poly(q-height, x)).items():
            if root.is_real and mult % 2 and sc[height][0] != sc[height][1]:
                result.add(root)
    return result


# m 전체 분류: 판별식이 양수면 두 단순근(통과), 0이면 접촉점(꼭짓점, 극한 존재).
q = (x-u)**2+m
assert s.discriminant(q-c, x) == 4*(c-m)
assert s.expand(q.subs(m, c)-c) == s.expand((x-u)**2)
cells = [(-1, 6), (0, 4), (3, 4), (6, 2), (8, 2), (10, 0), (11, 0)]
for height, expected in cells:
    assert len(bad_points(q.subs({u: 2, m: height}))) == expected
# 꼭짓점 x=2에서 높이 6에 닿음: g(6)=5이지만 양쪽 극한은 모두 g(6+)=4 → 극한 존재
assert count_abs(f, 6) == 5 and side_counts[6][1] == 4
assert s.reduce_inequalities([m >= 6, m < 10], m).as_set() == s.Interval.Ropen(6, 10)
# (가): m in [6,10), α,β 는 q=10 의 두 근. 근의 곱은 u²+m-10.
assert s.Poly(q-10, x).TC() == u**2+m-10
m_value = s.solve(u**2+m-10, m)[0]
assert m_value == 10-u**2
domain = s.reduce_inequalities([m_value >= 6, m_value < 10], u)
assert domain.as_set() == s.Union(s.Interval.Ropen(-2, 0), s.Interval.Lopen(0, 2))
target = s.expand(q.subs({x: 1, m: m_value}))
assert target == 11-2*u and s.diff(target, u) == -2         # 감소 → u=2 에서만 최소
answer = target.subs(u, 2)
assert answer == 7
assert s.solve(s.Eq(target, answer), u) == [2]              # 기호적 유일성
attainer = s.expand(q.subs({u: 2, m: 6}))
assert attainer == x**2-4*x+10
assert bad_points(attainer) == {s.Integer(0), s.Integer(4)}
print('17: g표 0,3,6,5,4,3,2 / 부재점 6/4/2/0, 허용 u=[-2,0)∪(0,2], 최솟값 7 (u=2,m=6 유일) OK')

# ---------- 격자 확인: g를 수치 근으로 따로 계산, 극한은 좌우 표본 비교 ----------
fc = [4.0, 0.0, -12.0, 2.0]


def g_num(tv):
    if tv < 0:
        return 0
    found = []
    for sign in ([1] if tv == 0 else [1, -1]):
        rts = np.roots([fc[0], fc[1], fc[2], fc[3]-sign*tv])
        found += [r.real for r in rts if abs(r.imag) < 1e-7]
    found.sort()
    return len([r for i, r in enumerate(found) if i == 0 or abs(r-found[i-1]) > 1e-6])


def grid_bad(uu, mm):
    """후보점(q=c 의 근, 꼭짓점)에서 좌우 표본의 g(q(x))를 비교한다. c는 t 격자로 찾은 점프 높이."""
    qf = lambda z: (z-uu)**2+mm
    pts = {uu}
    for cc in jump_levels:
        if cc > mm:
            d = (cc-mm)**0.5
            pts |= {uu-d, uu+d}
    h = 1e-5
    return sorted(p for p in pts if g_num(qf(p-h)) != g_num(qf(p+h)))


tgrid = [k/8 for k in range(-16, 113)]
jump_levels = [tg+1/16 for tg, tn in zip(tgrid, tgrid[1:]) if g_num(tg+1/32) != g_num(tn+1/32)]
jump_levels = sorted({round(v*16)/16 for v in jump_levels})
# 격자 간격 1/8 안에서 점프가 일어나는 칸: 0, 6, 10 을 각각 포함
assert len(jump_levels) == 3 and all(any(abs(j-L) < 1/8 for j in jump_levels) for L in [0, 6, 10])
jump_levels = [0.0, 6.0, 10.0]
valid = []
for i in range(-24, 25):          # u in [-6,6], 간격 1/4
    for j in range(-48, 57):      # m in [-12,14], 간격 1/4
        uu, mm = i/4, j/4
        bp = grid_bad(uu, mm)
        if len(bp) == 2 and abs(bp[0]*bp[1]) < 1e-9:
            valid.append((F(i, 4), F(j, 4), (1-uu)**2+mm))
best = min(v[2] for v in valid)
assert abs(best-7) < 1e-9
assert [(a, b) for a, b, v in valid if abs(v-best) < 1e-9] == [(2, 6)]
assert all(b == 10-a*a and 6 <= b < 10 for a, b, _ in valid)
print(f'격자 {49*105}점: 조건 만족 {len(valid)}개, 모두 m=10-u², 6≤m<10, 최솟값 7은 (u,m)=(2,6)에서만 OK')

# ---------- 원문 원리 줄 불통 ----------
# 원문 원리: '점프가 상쇄되는 점은 제외(연속)'. 새 문항에서는 상쇄가 없는데도 극한이 존재하는 점(꼭짓점)이 답을 정한다.
new_h = lambda z: count_abs(f, z)-count_abs(f, z-2)
new_cands = sorted(set(levels + [v+2 for v in levels]))
new_disc = [z for z in new_cands if len({new_h(z-eps), new_h(z), new_h(z+eps)}) > 1]
assert new_disc == [0, 2, 6, 8, 10, 12] and sum(new_disc) == 38 and sum(new_disc) != answer
assert sum(new_disc) not in map(s.sympify, it['choices'])
# 상쇄 기준으로 판정하면 m=6 꼭짓점(점프 4→... 상쇄 없음)을 부재점으로 셈 → 경계 m=6 배제, 최솟값 없음
assert side_counts[6][0] != side_counts[6][1]               # 높이 6의 점프는 상쇄되지 않는다
assert s.Integer(2) not in bad_points(attainer)              # 그런데 꼭짓점 x=2에서 극한은 존재
cancel_rule_bad = bad_points(attainer) | {s.Integer(2)}
assert len(cancel_rule_bad) == 3                             # 원문 기준이면 (가) 불만족 → 답 7을 못 얻음
print('원문 원리 줄 불통: 이동·상쇄로는 38(선지 밖), 상쇄 기준은 꼭짓점 판정을 틀려 답 7을 못 얻음 OK')

# ---------- 선지·오답 ----------
choices = list(map(s.sympify, it['choices']))
assert len(choices) == len(set(choices)) == 5
assert {choices[i+1]-choices[i] for i in range(4)} == {1}
assert it['ans'] == 5 and choices[it['ans']-1] == answer
# 오답 1: 절댓값을 뺌 → f(x)=t 의 점프 높이 -6, 10
plain_levels = [-6, 10]
plain_sides = {z: (count_plain(f, z-eps), count_plain(f, z+eps)) for z in plain_levels}
assert plain_sides == {-6: (1, 3), 10: (3, 1)}
wq = (x-4)**2-6
assert bad_points(wq, plain_levels, plain_sides) == {s.Integer(0), s.Integer(8)}
assert (s.reduce_inequalities([m_value >= -6, m_value < 10], u).as_set()
        == s.Union(s.Interval.Ropen(-4, 0), s.Interval.Lopen(0, 4)))
wrong_abs = (11-2*u).subs(u, 4)
assert wrong_abs == wq.subs(x, 1) == 3
assert len(bad_points(wq)) == 6                              # 실제 g로는 부재점 6개 → 오답
# 오답 2: (나) 무시 → 6≤m<10 에서 (1-u)²+m 최소
wn = s.expand((x-1)**2+6)
assert bad_points(wn) == {-1, 3} and (-1)*3 != 0
wrong_nonb = wn.subs(x, 1)
# 오답 2': 경계 함수에서 이차항 빠뜨림
wrong_drop_term = (attainer-x**2).subs(x, 1)
assert [wrong_abs, wrong_nonb, wrong_drop_term] == [3, 6, 6]
assert it['wrongs'] == [str(wrong_abs), str(wrong_nonb)]
assert all(s.sympify(v) in choices and s.sympify(v) != answer for v in it['wrongs'])
print('오답: 절댓값 무시 3(①), (나) 무시·이차항 누락 6(④) — 선지 안 OK')

# ---------- 빼 보기(조건 삭제 반례) ----------
without_ga = (x-4)**2-6                                       # 0 이 부재점이지만 부재점 6개
assert s.Integer(0) in bad_points(without_ga) and len(bad_points(without_ga)) == 6
assert without_ga.subs(x, 1) == 3 < answer
print('ABLATION 17 (가) 두 점뿐: 필요(q=(x-4)^2-6, 부재점 여섯 개, q(1)=3)')
without_na = (x-1)**2+6
assert bad_points(without_na) == {-1, 3}
assert without_na.subs(x, 1) == 6 < answer
print('ABLATION 17 (나) 두 점의 곱 0: 필요(q=(x-1)^2+6, 부재점 -1·3, q(1)=6)')
without_monic = 4*(x-1)**2+6
assert bad_points(without_monic) == {0, 2}
assert without_monic.subs(x, 1) == 6 < answer
print('ABLATION 17 최고차항 계수 1: 필요(q=4(x-1)^2+6, 부재점 0·2, q(1)=6)')
without_abs_answer = wrong_abs
assert without_abs_answer != answer
print('ABLATION 17 절댓값: 필요(빼면 3)')
print('선지·정답 위치 ⑤·오답 3,6 OK')
print('ALL OK')
