# -*- coding: utf-8 -*-
# 17번 후보 A17 (M26 킬러 설계A) 검증 · author='claude'
import sympy as sp, os, sys
t, s = sp.symbols('t s', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'A17.py')).read(), ns)
IT = ns['ITEMS'][17]


def roots_mult(p):
    """t>0 인 실근과 중복도 [(r, mult)] (정확한 값)"""
    P = sp.Poly(sp.expand(p), t)
    out = {}
    for r in sp.real_roots(P):
        out[r] = out.get(r, 0) + 1
    return [(r, k) for r, k in out.items() if r > 0]


def sign_changes(p):
    """t>0 에서 p 의 부호가 바뀌는 점의 개수 = 홀수 중복도 근의 개수"""
    return sum(1 for r, k in roots_mult(p) if k % 2 == 1)


def model(m, x0=0, start_too=False):
    """정수 m 에서 (a(m), b(m)). x0: 출발점, start_too: t=0 도 원점 통과로 셈"""
    v = 2 * t**3 - 6 * t + 7 - m
    x = x0 + sp.integrate(v.subs(t, s), (s, 0, t))
    a = sign_changes(v)
    rx = roots_mult(x)
    assert all(k % 2 == 1 for r, k in rx), (m, rx)            # 정수 m 에서 원점에 접하기만 하는 시각 없음
    b = len(rx) + (1 if start_too and x.subs(t, 0) == 0 else 0)
    return a, b


# ---------- 위치 함수
m = sp.symbols('m', integer=True)
v = 2 * t**3 - 6 * t + 7 - m
x = sp.integrate(v.subs(t, s), (s, 0, t))
assert sp.expand(x - (R(1, 2) * t**4 - 3 * t**2 + (7 - m) * t)) == 0
assert sp.expand(x - t * (R(1, 2) * t**3 - 3 * t + 7 - m)) == 0
h = 2 * t**3 - 6 * t + 7; g = R(1, 2) * t**3 - 3 * t + 7
assert sp.expand(sp.diff(h, t) - 6 * (t - 1) * (t + 1)) == 0 and h.subs(t, 0) == 7 and h.subs(t, 1) == 3
assert sp.solve(sp.diff(g, t), t) == [-sp.sqrt(2), sp.sqrt(2)] and sp.simplify(g.subs(t, sp.sqrt(2)) - (7 - 2 * sp.sqrt(2))) == 0
assert 4 < 7 - 2 * sp.sqrt(2) < 5                                   # 경계 판단: m=4 는 원점 재통과 없음
assert sp.expand(h - 3 - 2 * (t - 1)**2 * (t + 2)) == 0                # m=3: 접함(방향 안 바뀜)
assert sp.expand(h - 7 - 2 * t * (t**2 - 3)) == 0 and sp.expand(g - 7 - t * (t**2 - 6) / 2) == 0
print('위치 x(t)=t(t^3/2-3t+7-m), h 극소 3(t=1)·출발 7, g 극소 7-2√2(t=√2)·출발 7')

# ---------- 정수 m 전수: (a, b) 표와 식 대조 (|m|≤60, 그 밖은 아래 단조성으로)
def a_formula(mm):
    return 0 if mm <= 3 else 2 if mm < 7 else 1
def b_formula(mm):
    return 0 if mm <= 4 else 2 if mm < 7 else 1
TAB = {}
for mm in range(-60, 61):
    TAB[mm] = model(mm)
    assert TAB[mm] == (a_formula(mm), b_formula(mm)), (mm, TAB[mm])
# 범위 밖: m≤3 이면 h-m ≥ h-3 = 2(t-1)^2(t+2) ≥ 0 이고 g-m ≥ g(√2)-m > 0 → (0,0)
# m>7 이면 h-m, g-m 은 t=0 에서 음수, 극소 뒤 증가해 +∞ → t>0 근 하나씩 → (1,1)
for big in (10**3, 10**6, -10**3, -10**6):
    assert model(big) == (a_formula(big), b_formula(big))
print('정수 m 전수(-60..60, ±10^3, ±10^6): a=0(m≤3), 2(4≤m≤6), 1(m≥7); b=0(m≤4), 2(m=5,6), 1(m≥7)')
print('  m=1..9 (a,b):', [TAB[mm] for mm in range(1, 10)])

ANS = sum(TAB[mm][0] * TAB[mm][1] for mm in range(1, 10))
assert ANS == 11
ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2                   # 정답 ② = 11
assert len(set(ch)) == 5 and len({int(ch[i + 1]) - int(ch[i]) for i in range(4)}) == 1 and int(ch[1]) - int(ch[0]) == 1
print('정답 11 = 선지 ②, 선지 10..14 공차 1 오름차순')

# ---------- 유일성: 정답을 정하는 판정이 하나로 정해짐(경계 m=3, 4, 7 의 정확한 값)
assert TAB[3] == (0, 0) and TAB[4] == (2, 0) and TAB[7] == (1, 1)
assert sp.real_roots(sp.Poly(sp.expand(x.subs(m, 7)), t)).count(0) == 2   # m=7: t=0 이 위치의 이중근(출발점), 제외
print('경계: m=3 (0,0) 접함 · m=4 (2,0) 7-2√2>4 · m=7 (1,1) 출발 시각 근 제외')

# ---------- 원문 M26: 위치 x=t^4/2-3t^2+(7-m)t, 운동 방향이 두 번 바뀌는 정수 m 의 합 = 15 (⑤)
two = [mm for mm in range(-60, 61) if TAB[mm][0] == 2]
assert two == [4, 5, 6] and sum(two) == 15
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
o = F.I['M26']
assert o[1][4] == '15' and o[2] == '⑤'
print('원문 M26 OK: 3<m<7, 4+5+6=15 (원문 정답 ⑤ 15)')

# ---------- 오답 근거 (선지 안)
def total(fun):
    return sum(fun(mm) for mm in range(1, 10))
W10 = total(lambda mm: 0 if mm == 7 else TAB[mm][0] * TAB[mm][1])                    # m=7 을 경계로 제외
W12a = total(lambda mm: (2 * TAB[mm][1]) if mm == 7 else TAB[mm][0] * TAB[mm][1])     # a(7)=2 (t=0 근 셈)
W12b = total(lambda mm: (TAB[mm][0] * 2) if mm == 7 else TAB[mm][0] * TAB[mm][1])     # b(7)=2 (t=0 근 셈)
W14 = total(lambda mm: 4 if mm == 7 else TAB[mm][0] * TAB[mm][1])                     # 둘 다
W15 = total(lambda mm: (TAB[mm][0] * 2) if mm == 4 else TAB[mm][0] * TAB[mm][1])      # b(4)=2 (어림 실패)
assert sp.real_roots(sp.Poly(2 * t**3 - 6 * t, t)).count(0) == 1                    # v(t)=2t(t^2-3) 의 t=0 근
assert (W10, W12a, W12b, W14, W15) == (10, 12, 12, 14, 15)
assert all(w in ch for w in IT['wrongs']) and IT['wrongs'] == ['10', '12', '14'] and '15' not in ch
print('오답 근거 OK: 10(m=7 제외) · 12(a(7) 또는 b(7)에 t=0 셈) · 14(둘 다) · 선지 밖 15(m=4 어림 실패, 원문 답)')

# ---------- 원문 핵심 한 줄 테스트 (①형: 원리 줄 불통)
# 원리 줄 '3<m<7 이면 두 번(=2), 그 밖은 0' 으로 a 를 두고 b 없이 풀면
orig_line = total(lambda mm: 2 if 3 < mm < 7 else 0)
assert orig_line == 6 and orig_line != ANS
assert any(TAB[mm][0] * TAB[mm][1] != (4 if 3 < mm < 7 else 0) for mm in range(1, 10))   # m=4, m≥7 에서 어긋남
print('핵심 한 줄: 원문 원리 줄(3<m<7 고르기)로는 m=4 제거·m≥7 의 1×1 을 정할 수 없음 → 불통')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
out = []
def ablation(cname, res, why=''):
    msg = (f'군더더기(답 그대로{"; " + why if why else ""})' if res == ANS else f'필요({res}{"; " + why if why else ""})')
    print(f'ABLATION 17 {cname}: {msg}'); out.append(msg)
# 1) b(m) 빼기: Σ a(m)
ablation("'원점을 다시 지나는 횟수 b(m)'(곱에서 뺌, Σa(m))", sum(TAB[mm][0] for mm in range(1, 10)), 'm=4 가 남고 m≥7 은 1')
# 2) a(m) 빼기: Σ b(m)
ablation("'운동 방향을 바꾸는 횟수 a(m)'(곱에서 뺌, Σb(m))", sum(TAB[mm][1] for mm in range(1, 10)), '방향 전환 판정이 없어짐')
# 3) '원점을 출발하여' 빼기: 출발점 x0 미정 → 답이 정해지지 않음
alt = {x0: sum(model(mm, x0)[0] * model(mm, x0)[1] for mm in range(1, 10)) for x0 in (1, -1, -2)}
assert len(set(alt.values()) | {ANS}) > 1
ablation("'원점을 출발하여'(출발점 미정)", f'정해지지 않음 {alt}', '출발점에 따라 원점을 지나는 횟수가 달라짐')
# 4) '출발한 후 … 다시' 빼기: t=0 의 출발도 원점을 지나는 것으로 셈
ablation("'출발한 후 … 다시'(t=0 출발도 셈)", sum(model(mm, 0, True)[0] * model(mm, 0, True)[1] for mm in range(1, 10)), 'b(m)+1')
# 5) 곱 대신 합(조건 결합 방식): 두 횟수를 겹치지 않으면
ablation("곱 a(m)b(m)(→ 합 a(m)+b(m))", sum(TAB[mm][0] + TAB[mm][1] for mm in range(1, 10)), '곱이 m=4 를 지움')
assert all(r_.startswith('필요') for r_ in out), out

# ---------- 형식·기록
assert IT['key'] == 'M26' and IT['cand'] == 'A17' and IT['db_ref'] == 'M26 킬러 설계A'
assert IT['core']['axis'] == '①' and set(IT['core']) == {'axis', 'setting', 'principle', 'new'}
assert '함정 추가' not in IT['vtype'] and IT['bunseok'] is False and 'cond' not in IT
print('ALL OK')
