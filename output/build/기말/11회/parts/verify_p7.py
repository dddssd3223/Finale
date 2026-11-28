# -*- coding: utf-8 -*-
# 서답형1 (자체, D53 방향) · 서답형2 (D71 후보_순위 2 학교식, 답만 3단계) 검증 · author='claude'
import sympy as sp, os, sys, re
x, t, a, b, C, k = sp.symbols('x t a b C k', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

# ================= S1 =================
# --- 원문 D53: f(1)=3, f'≥5 on (1,5) → f(5) 최솟값 23 (③)
assert F.I['D53'][2] == '③' and F.I['D53'][1][2] == '23' and 3 + 5 * 4 == 23
print('D53 원문 OK: f(5)의 최솟값 23 (원문 정답 ③)')

assert r"f(1)=-4" in S1['body'] and r"1&lt;x&lt;6" in S1['body'] and r"f'(x)\ge3" in S1['body'] and 'cond' not in S1
x0, f0, x1, m = 1, -4, 6, 3
# 조건을 만족시키는 함수 표본: f = 3x-7 + h, h는 [1,6]에서 증가(h'≥0), h(1)=0
lin = m * x + (f0 - m * x0); assert sp.expand(lin - (3 * x - 7)) == 0
fam = [sp.Integer(0), (x - 1)**3, (x - 1)**2 / 5, (x - 1) * R(1, 3), (x - 1)**3 * (x - 1) / 50,
       sp.integrate((s := sp.Symbol('s'))**2 * (s - 4)**2, (s, 1, x))]
vals6 = []
for h in fam:
    f = sp.expand(lin + h)
    assert f.subs(x, 1) == -4
    fp = sp.diff(f, x)
    # 1<x<6에서 f'≥3 확인 (다항식 최솟값 점검: 격자 + 임계점)
    crit = [r for r in sp.Poly(sp.diff(fp, x), x).real_roots() if 1 < r < 6] if sp.degree(fp, x) >= 2 else []
    assert all(fp.subs(x, v) >= 3 for v in [R(1) + R(i, 10) for i in range(1, 50)] + crit)
    vals6.append(f.subs(x, 6))
assert min(vals6) == 11 and lin.subs(x, 6) == 11
# 하한 증명: 평균값 정리 f(6) ≥ f(1) + 3·5
assert f0 + m * (x1 - x0) == 11
# (2) f(6)=11 이면 f(4)=5 : f(4) ≥ -4+9 , f(6)-f(4) ≥ 6
lo4 = f0 + m * (4 - x0); hi4 = 11 - m * (6 - 4)
assert lo4 == hi4 == 5
# 표본 중 f(6)=11인 것은 h≡0 뿐 → f(4)=5
assert [lin.subs(x, 4) + h.subs(x, 4) for h, v in zip(fam, vals6) if v == 11] == [5]
assert S1['ans'] == [r'(1) \(11\)', r'(2) \(5\)']
# 정답이 본문 수와 같지 않음
txt1 = S1['body'] + ''.join(q[0] for q in S1['subs'])
nums1 = set(re.findall(r'-?\d+', re.sub(r'\\\(\d\)', '', txt1)))
for v in ('11', '5'): assert v not in nums1, (v, nums1)
# 오답 값
assert f0 + m * 6 == 14 and 11 + m * 2 == 17
for w in (r'-4+18=14', r'f(4)\ge5\)라', r'f(4)\le5\)', r'=17\)'): assert w in S1['wrong'], w
# 배점·형식
assert len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D53)'
print('S1 OK: (1) 최솟값 11 (f=3x-7 + 증가 섭동 표본) (2) 양쪽 평균값 정리로 f(4)=5')

def abl1(cn, m_): print(f'ABLATION S1 {cn}: {m_}')
# f(1)=-4 삭제: f=3x+c 모두 가능 → f(6)=18+c, 하한 없음
assert (3 * x + 100).subs(x, 6) != (3 * x - 100).subs(x, 6)
abl1('f(1)=-4', '필요(없으면 f(x)=3x+c가 모두 되어 f(6)의 최솟값이 없음)')
# f'≥3 삭제: f = -4 - N(x-1) → f(6) 한없이 작음
abl1("1<x<6에서 f'(x)≥3", '필요(없으면 f(x)=-N(x-1)-4로 f(6)이 한없이 작아짐)')
# (2)의 'f(6)이 최솟값' 삭제: f=3x-7+(x-1)^3 이면 f(4)=32 ≠ 5
assert (lin + (x - 1)**3).subs(x, 4) == 32
abl1("(2)의 'f(6)이 최솟값과 같을 때'", '필요(없으면 f(x)=3x-7+(x-1)^3에서 f(4)=32처럼 f(4)가 정해지지 않음)')


# ================= S2 =================
def roots_count(fc, kv, tv, L):
    """g(x)=t 의 서로 다른 실근 수 (g=f+k |x|>L, -f |x|≤L)"""
    cnt = 0
    for r in set(sp.Poly(sp.expand(fc + kv - tv), x).real_roots()):
        if abs(r) > L: cnt += 1
    for r in set(sp.Poly(sp.expand(-fc - tv), x).real_roots()):
        if abs(r) <= L: cnt += 1
    return cnt

def solve_case(L, d0, M):
    """f'(0)=d0, 경계 L. (가)에서 f'(±L)=0 → f, 우연속 x=L → k=-2f(L), (나) 최댓값 M → C"""
    fp = d0 * (1 - x**2 / L**2)
    f = sp.integrate(fp, x) + C
    kv = -2 * f.subs(x, L)
    # 실근 2개인 t: (f(-L)+k, -f(-L)]
    Cv = sp.solve(sp.Eq(-f.subs(x, -L), M), C)[0]
    return sp.expand(f.subs(C, Cv)), sp.simplify(kv.subs(C, Cv))

# --- 원문 D71: L=1, f'(0)=6, M=13 → k+f(1/2) = 15/4 (①)
fo, ko = solve_case(1, 6, 13)
assert ko == 10 and sp.expand(fo - (-2 * x**3 + 6 * x - 9)) == 0 and ko + fo.subs(x, R(1, 2)) == R(15, 4)
assert F.I['D71'][2] == '①'
print('D71 원문 OK: f=-2x^3+6x-9, k=10, k+f(1/2)=15/4 (원문 정답 ①)')
# --- GEN1-01-169: L=2, f'(0)=3, M=10 → k=4, k+f(1)=3/4 (우리 문항과 수치 다름 확인)
fg, kg = solve_case(2, 3, 10)
assert kg == 4 and kg + fg.subs(x, 1) == R(3, 4)

# --- S2: (가) → f'(±2)=0 를 일반 삼차에서 확인
assert r"f'(0)=6" in S2['body'] and r"|x|&gt;2" in S2['body'] and r"|x|\le2" in S2['body']
assert r"최댓값은 \(11\)" in S2['cond'][1][1]
fp_gen = 3 * a * x**2 + 2 * b * x + 6
sol_ab = sp.solve([fp_gen.subs(x, 2), fp_gen.subs(x, -2)], [a, b], dict=True)
assert sol_ab == [{a: R(-1, 2), b: 0}]
# (가)를 만족시키는 삼차 f'(x)=3ax^2+2bx+6: |x|<2에서 ≥0, |x|>2에서 ≤0 → 격자 전수
ok = []
for av in [R(i, 8) for i in range(-24, 25) if i != 0]:
    for bv in [R(j, 8) for j in range(-24, 25)]:
        g_ = fp_gen.subs({a: av, b: bv})
        ins = all(g_.subs(x, v) >= 0 for v in [R(i, 10) for i in range(-20, 21)])   # 연속이므로 끝점 ±2 포함
        outs = all(g_.subs(x, v) <= 0 for v in [R(s * (20 + i), 10) for s in (1, -1) for i in range(0, 60)])
        if ins and outs: ok.append((av, bv))
assert ok == [(R(-1, 2), 0)], ok
f2, k2 = solve_case(2, 6, 11)
assert sp.expand(f2 - (-x**3 / 2 + 6 * x - 3)) == 0 and k2 == -10
# 우미분계수 확인: x=2 오른쪽 연속, x=-2 에서는 점프(왼쪽 극한 -21, 함숫값 11)
assert f2.subs(x, 2) + k2 == -f2.subs(x, 2)
assert f2.subs(x, -2) + k2 == -21 and -f2.subs(x, -2) == 11
# (나) 직접 확인: 실근 개수가 2인 t (반정수 격자 + 경계)
ts = [R(i, 2) for i in range(-80, 60)]
two = [tv for tv in ts if roots_count(f2, k2, tv, 2) == 2]
assert max(two) == 11 and min(two) == R(-41, 2) and roots_count(f2, k2, -21, 2) == 1
assert all(roots_count(f2, k2, tv, 2) == 2 for tv in ts if -21 < tv <= 11)
# C 유일성: C 격자에서 (나)의 최댓값이 11인 것은 C=-3 하나
for Cv in range(-10, 5):
    fc = sp.expand(-x**3 / 2 + 6 * x + Cv); kc = -2 * fc.subs(x, 2)
    mx = max(tv for tv in range(-60, 40) if roots_count(fc, kc, tv, 2) == 2)
    assert (mx == 11) == (Cv == -3), (Cv, mx)
A1 = f2.subs(x, 2) - f2.subs(x, -2); assert A1 == 16 == sp.integrate(sp.diff(f2, x), (x, -2, 2))
A3 = len([tv for tv in range(-60, 40) if roots_count(f2, k2, tv, 2) == 2]); assert A3 == 32
assert S2['ans'] == [r'(1) \(16\)', r'(2) \(-10\)', r'(3) \(32\)']
print('S2 OK: (1) 16 (2) k=-10 (3) 정수 t 32개 (일반 삼차 격자 전수 + C 격자 유일성 + 실근 개수 직접 셈)')
# 정답이 본문 수와 같지 않음
txt = S2['body'] + ''.join(v for _, v in S2['cond']) + ''.join(q[0] for q in S2['subs'])
nums = set(re.findall(r'-?\d+', txt))
for v in ('16', '-10', '32'): assert v not in nums, v
# 오답 값
assert sp.integrate(6 - 6 * x**2, (x, -2, 2)) == -8                           # (1) 원문 f'
assert -2 * f2.subs(x, -2) == 22                                                # (2) 연속점을 x=-2로
fw = -x**3 / 2 + 6 * x + C; Cw = sp.solve(sp.Eq(fw.subs(x, -2) - 2 * fw.subs(x, 2), 11), C)[0]
assert Cw == -35 and -2 * fw.subs({C: Cw, x: 2}) == 54                          # (2) 최댓값을 점프 아래값으로
assert A3 + 1 == 33 and A3 - 1 == 31                                            # (3) 끝 개폐
for w in (r'\(-8\)', r'=22\)', r'\(k=54\)', r'\(33\)', r'\(31\)'): assert w in S2['wrong'], w
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['2점, 답만 적으시오.', '5점, 답만 적으시오.', '3점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S2['rubric'][:3]]
assert pts2 == [[2], [5], [3]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line_ for line_ in S2['rubric'][:3])
assert S2['db_ref'] == 'D71 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
for it in (S1, S2):
    tx = it['body'] + ''.join(v for _, v in it.get('cond', [])) + ''.join(q[0] for q in it['subs'])
    assert '이러한' not in tx and '이와 같은' not in tx
    assert not [mm for mm in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', tx, re.S) if '<' in mm or '>' in mm]
print('S2 형식 OK')

def abl2(cn, m_): print(f'ABLATION S2 {cn}: {m_}')
# (나) 삭제 → C 정해지지 않음 → k 정해지지 않음
fa = sp.expand(-x**3 / 2 + 6 * x); assert -2 * (fa + 1).subs(x, 2) != -2 * (fa + 2).subs(x, 2)
abl2('(나) 최댓값 11', '필요(없으면 C가 정해지지 않아 (2)의 k가 정해지지 않음)')
# f'(0)=6 삭제 → f'=d(1-x^2/4), 최댓값 11 하나로 d·C 정해지지 않음
fd1, kd1 = solve_case(2, 3, 11); fd2, kd2 = solve_case(2, 9, 11)
assert kd1 != kd2 and fd1.subs(x, 2) - fd1.subs(x, -2) != fd2.subs(x, 2) - fd2.subs(x, -2)
abl2("f'(0)=6", f'필요(없으면 f\'(0)=3이면 k={kd1}, 9이면 k={kd2}처럼 (1)(2)(3)이 정해지지 않음)')
# (가) 삭제 → f'의 꼴이 정해지지 않음: 예) f'=6 상수 아님 등 → (1) 정해지지 않음
f_alt = sp.integrate(6 - x**2, x); assert f_alt.subs(x, 2) - f_alt.subs(x, -2) != 16
abl2('(가) 우미분계수', '필요(없으면 f\'(±2)=0이 나오지 않아 f\'(x)=6-x^2 등도 되어 (1)이 정해지지 않음)')
# (가)의 '0 이하' 삭제(존재만): 조각마다 증가도 허용 → f'의 부호 조건이 사라져 f 정해지지 않음
abl2("(가)의 '0 이하'", "필요(없으면 f'(±2)=0을 얻지 못해 f가 정해지지 않음)")
# 경계 |x|>2 → |x|>1(원문): 값이 달라짐
fo2, ko2 = solve_case(1, 6, 11); assert ko2 != -10
abl2('경계 2', f'필요(원문 경계 1이면 k={ko2})')

print('ALL OK')
