# -*- coding: utf-8 -*-
# 17번 후보 A17 재설계판 (M26, 위치의 최솟값 판정) 검증 · author='claude'
import sympy as sp, os, sys
t, s, tau = sp.symbols('t s tau', real=True)
m = sp.symbols('m', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'A17.py')).read(), ns)
IT = ns['ITEMS'][17]

V = 2 * t**3 - 6 * t + 7 - m
X = sp.integrate(V.subs(t, s), (s, 0, t))
assert sp.expand(X - (R(1, 2) * t**4 - 3 * t**2 + (7 - m) * t)) == 0


def xmin(mv, x0=0):
    """t≥0 에서 x0+X 의 최솟값(정확한 값). 후보: t=0 과 v 의 양의 실근"""
    xx = sp.expand(X.subs(m, mv)) + x0
    cand = [sp.Integer(0)] + [r for r in sp.real_roots(sp.Poly(sp.expand(V.subs(m, mv)), t)) if r > 0]
    vals = [sp.nsimplify(sp.expand(xx.subs(t, r))) if r.is_rational else xx.subs(t, r) for r in cand]
    return min(vals, key=lambda e: sp.N(e, 60))


def cmp(e, c):
    """e 와 c 의 대소 (정확히 같으면 0)"""
    d = sp.simplify(e - c)
    if d == 0: return 0
    n = sp.N(d, 60); assert abs(n) > 1e-40
    return 1 if n > 0 else -1


def ok(mv, x0=0, strict_b=False):
    mn = xmin(mv, x0)
    ga = cmp(mn, 0) < 0                       # (가) x(k)<0 인 양수 k 존재 ⇔ 최솟값 < 0
    gb = cmp(mn, -12) > 0 if strict_b else cmp(mn, -12) >= 0   # (나) 모든 t>0 에서 x ≥ -12
    return ga, gb


# ---------- 핵심 줄: 극소 시각에서 m 소거
msol = sp.solve(V.subs(t, tau), m)[0]
phi = sp.factor(sp.expand(X.subs(t, tau).subs(m, msol)))
assert sp.expand(phi - R(3, 2) * tau**2 * (2 - tau**2)) == 0
assert sp.solve(sp.Eq(phi, -12), tau) == [-2, 2] or set(r for r in sp.solve(sp.Eq(phi, -12), tau) if r.is_real) == {-2, 2}
assert msol.subs(tau, 2) == 11
assert set(r for r in sp.solve(sp.Eq(phi, 0), tau) if r.is_real and r > 0) == {sp.sqrt(2)}
assert sp.simplify(msol.subs(tau, sp.sqrt(2)) - (7 - 2 * sp.sqrt(2))) == 0 and 4 < 7 - 2 * sp.sqrt(2) < 5
assert sp.expand(X.subs(m, 11) + 12 - R(1, 2) * (t - 2)**2 * (t**2 + 4 * t + 6)) == 0           # m=11: x+12 ≥ 0, 등호 t=2
assert sp.expand(X.subs(m, 7 - 2 * sp.sqrt(2)) - R(1, 2) * t * (t - sp.sqrt(2))**2 * (t + 2 * sp.sqrt(2))) == 0
assert sp.discriminant(t**2 + 4 * t + 6, t) < 0
assert sp.diff(X, m) == -t                                                                    # t>0 에서 m 에 대해 감소
print('핵심 줄: x(τ)=3/2·τ²(2-τ²); -12 ↔ τ=2, m=11 · 0 ↔ τ=√2, m=7-2√2 (4<7-2√2<5); ∂x/∂m=-t<0')

# ---------- 정수 m 전수 (|m|≤60, 그 밖은 단조성: m≤4 이면 x ≥ x(·;7-2√2) ≥ 0, m≥12 이면 x(2)=10-2m<-12)
TAB = {mv: ok(mv) for mm in [range(-60, 61)] for mv in mm}
SOLS = [mv for mv, (a, b) in TAB.items() if a and b]
assert SOLS == list(range(5, 12)), SOLS
for mv in range(-60, 61):
    assert TAB[mv][0] == (mv >= 5) and TAB[mv][1] == (mv <= 11), mv
assert xmin(11) == -12 and cmp(xmin(7), R(-9, 2)) == 0 and xmin(4) == 0 and cmp(xmin(5), 0) < 0
for mv in (10**3, -10**3, 10**6, -10**6): assert ok(mv) == (mv >= 5, mv <= 11)
assert all(sp.expand(X.subs(m, mv).subs(t, 2)) == 10 - 2 * mv for mv in range(12, 20))
ANS = max(SOLS) + min(SOLS)
assert ANS == 16
print('정수 m 전수(-60..60, ±10^3, ±10^6): (가) ⇔ m≥5, (나) ⇔ m≤11 → m=5..11, 최댓값+최솟값 = 16')
print('  최솟값: ' + ', '.join(f'm={mv}:{sp.N(xmin(mv), 5)}' for mv in range(3, 13)))

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(ch)) == 5 and len({int(ch[i + 1]) - int(ch[i]) for i in range(4)}) == 1 and int(ch[1]) - int(ch[0]) == 1
print('정답 16 = 선지 ②, 선지 15..19 공차 1 오름차순')

# ---------- 경우 분기 (풀이의 다섯 갈래)
def turns(mv):
    return sum(1 for r in sp.real_roots(sp.Poly(sp.expand(V.subs(m, mv)), t)) if r > 0 and
               sp.Poly(sp.expand(V.subs(m, mv)), t).as_expr().subs(t, r + R(1, 10**9)) * sp.Poly(sp.expand(V.subs(m, mv)), t).as_expr().subs(t, r - R(1, 10**9)) < 0)
assert [turns(mv) for mv in (2, 3)] == [0, 0] and turns(4) == 2 and xmin(4) == 0          # m≤3: 전환 없음 / m=4: 두 번, 음수 안 됨
assert turns(5) == turns(6) == 2 and cmp(xmin(6), 0) < 0                                  # m=5,6: 되돌아와 원점 지남
assert all(turns(mv) == 1 for mv in range(7, 13)) and cmp(xmin(12), -12) < 0              # m≥7: 한 번
print('경우: m≤3 전환 0 · m=4 전환 2, 최솟값 0 · m=5,6 음수 · 7≤m≤11 · m≥12 하한 위반')

# ---------- 원문 M26: 운동 방향이 두 번 바뀌는 정수 m 의 합 = 15 (⑤)
two = [mv for mv in range(-60, 61) if turns(mv) == 2]
assert two == [4, 5, 6] and sum(two) == 15
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
o = F.I['M26']
assert o[1][4] == '15' and o[2] == '⑤'
print('원문 M26 OK: 3<m<7, 4+5+6=15 (원문 정답 ⑤ 15)')

# ---------- 오답 근거
W15a = min(two) + 11                                     # (가)를 '두 번 바꾸면 되돌아와 음수'(원문 줄)로: 최솟값 4
W15b = 5 + max(mv for mv in range(-60, 61) if TAB[mv][0] and ok(mv, strict_b=True)[1])   # (나) 등호 뺌
W18 = min(mv for mv in range(-60, 61) if 7 - mv <= 0) + 11  # (가)를 v(0)≤0 으로: 최솟값 7
W19 = min(mv for mv in range(-60, 61) if 7 - mv < 0) + 11   # m=7 까지 뺌
assert (W15a, W15b, W18, W19) == (15, 15, 18, 19)
assert all(w in ch for w in IT['wrongs']) and IT['wrongs'] == ['15', '18']
print('오답 근거 OK: 15(원문 줄로 m=4 포함 / (나) 등호 뺌) · 18(m=5,6 놓침) · 19(m=7 도 뺌)')

# ---------- 원문 핵심 한 줄 테스트 (①형: 원리 줄 불통)
# 원리 줄(방향 두 번 ⇔ 3<m<7)로 (가)를 정하면 m=4 가 들어가 틀림, (나)는 전환 횟수와 무관(7..11 모두 한 번)
assert TAB[4][0] is False and 4 in two
assert len({turns(mv) for mv in range(7, 13)}) == 1 and TAB[11][1] and not TAB[12][1]
print('핵심 한 줄: 원문 원리 줄(전환 횟수, 3<m<7)은 (가)를 m=4 에서 틀리게 하고 (나)의 경계 11/12 를 가르지 못함 → 불통')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
out = []
def ablation(cname, res, why=''):
    msg = (f'군더더기(답 그대로{"; " + why if why else ""})' if res == ANS else f'필요({res}{"; " + why if why else ""})')
    print(f'ABLATION 17 {cname}: {msg}'); out.append(msg)
# 1) (가) 빼기: m≤11 전부 → 최솟값 없음
onlyb = [mv for mv in range(-60, 61) if TAB[mv][1]]
assert min(onlyb) == -60 and ok(-10**6)[1]
ablation('(가)', '정해지지 않음(m≤11, 최솟값 없음)', '아래로 끝없이')
# 2) (나) 빼기: m≥5 전부 → 최댓값 없음
assert ok(10**6)[0]
ablation('(나)', '정해지지 않음(m≥5, 최댓값 없음)', '위로 끝없이')
# 3) '정수' 빼기: 실수 m 이면 (가) ⇔ m>7-2√2 (열린 경계) → 최솟값 없음
m0 = 7 - 2 * sp.sqrt(2)
assert sp.expand(X.subs(m, m0) - R(1, 2) * t * (t - sp.sqrt(2))**2 * (t + 2 * sp.sqrt(2))) == 0   # m=m0: x ≥ 0, (가) 거짓
for eps in (R(1, 10**6), R(1, 10**3), R(1, 2)):                                                 # m0<m: x(√2)<0, (가) 참
    assert sp.simplify(X.subs({m: m0 + eps, t: sp.sqrt(2)}) + eps * sp.sqrt(2)) == 0
assert ok(R(9, 2)) == (True, True) and ok(R(42, 10)) == (True, True)                            # 4.2, 4.5 도 조건 만족(정수가 아니면 5보다 작은 값이 들어옴)
ablation("'정수 m'", '정해지지 않음(실수 m 이면 7-2√2&lt;m≤11, 최솟값 없음)', '(가)의 경계가 열려 있음')
# 4) '원점을 출발하여' 빼기: 출발점 x0 에 따라 답이 달라짐
alt = {}
for x0 in (1, 2, -1):
    S_ = [mv for mv in range(-60, 61) if all(ok(mv, x0))]
    alt[x0] = (max(S_) + min(S_)) if S_ and min(S_) > -60 and max(S_) < 60 else '없음'
assert set(alt.values()) != {ANS}
ablation("'원점을 출발하여'(출발점 미정)", f'정해지지 않음 {alt}', '출발점이 바뀌면 경계가 달라짐')
# 5) (나)의 등호: '-12 이상' → '-12 보다 크다'
S5 = [mv for mv in range(-60, 61) if TAB[mv][0] and ok(mv, strict_b=True)[1]]
ablation("(나)의 등호(≥ → >)", max(S5) + min(S5), 'm=11 에서 최솟값이 정확히 -12')
assert all(r_.startswith('필요') for r_ in out), out

# ---------- 형식·기록
assert IT['key'] == 'M26' and IT['cand'] == 'A17' and IT['db_ref'] == 'M26 킬러 설계A'
assert IT['core']['axis'] == '①' and set(IT['core']) == {'axis', 'setting', 'principle', 'new'}
assert '함정 추가' not in IT['vtype'] and IT['bunseok'] is False and [c[0] for c in IT['cond']] == ['가', '나']
assert '재설계' in IT['note']
print('ALL OK')
