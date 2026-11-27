# -*- coding: utf-8 -*-
# 서답형1 (자체, D15 방향) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a = sp.symbols('x a', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1 = ns['SITEMS']['S1']
assert set(ns['SITEMS']) == {'S1'}
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

def pieces(B, C):
    """f=x^3+Bx^2+C|x-a| 의 오른쪽(x>a)·왼쪽(x<a) 도함수"""
    return 3 * x**2 + 2 * B * x + C, 3 * x**2 + 2 * B * x - C

def inc_max_a(B, C):
    R, L = pieces(B, C)
    assert sp.discriminant(R, x) < 0                     # 오른쪽은 늘 양수
    rs = sorted(sp.solve(L, x)); return rs[0]            # 왼쪽: (-inf,a)에서 L>=0 ⇔ a <= 작은 근

def increasing(B, C, av):
    """수치 격자로 실수 전체 증가(f'>=0, 0은 고립점) 확인"""
    R, L = pieces(B, C)
    pts = [sp.Rational(i, 20) for i in range(-400, 400)]
    for p in pts:
        if p == av: continue
        v = (R if p > av else L).subs(x, p)
        if v < 0: return False
    return True

# --- 원문 D15: x^3+x^2+|x-a|+2 → 최댓값 -1 (②)
assert inc_max_a(1, 1) == -1 and F.I['D15'][2] == '②' and F.I['D15'][1][1] == '-1'
assert increasing(1, 1, -1) and not increasing(1, 1, sp.Rational(-9, 10))
print('D15 원문 OK: a의 최댓값 -1')

# --- S1 본문
assert r"f(x)=x^3-3x^2+24|x-a|" in S1['body'] and 'cond' not in S1
B, C = -3, 24
R, L = pieces(B, C)
assert sp.expand(R - (3 * (x - 1)**2 + 21)) == 0 and sp.expand(L - 3 * (x + 2) * (x - 4)) == 0

# (1) a=1: 감소 구간 전수(격자)
f1 = sp.Piecewise((x**3 - 3 * x**2 + 24 * (x - 1), x >= 1), (x**3 - 3 * x**2 - 24 * (x - 1), True))
fp1 = lambda p: (R if p > 1 else L).subs(x, p)
grid = [sp.Rational(i, 40) for i in range(-400, 400)]
neg = [p for p in grid if p != 1 and fp1(p) < 0]
assert min(neg) > -2 and max(neg) < 1 and min(neg) <= sp.Rational(-79, 40) and max(neg) >= sp.Rational(39, 40)
assert all(fp1(p) > 0 for p in grid if p < -2 or p > 1)
# 연속: x=1에서 좌우 극한 같음 → 닫힌구간 [-2,1]에서 감소
assert sp.limit(f1, x, 1, '-') == sp.limit(f1, x, 1, '+') == f1.subs(x, 1)
dec = (-2, 1)
print('S1 (1) OK: a=1일 때 감소 구간 [-2, 1]')

# (2) 최댓값
amax = inc_max_a(B, C); assert amax == -2
assert increasing(B, C, -2)
for av in (sp.Rational(-19, 10), sp.Rational(-1), 0, 1, 4, 5):
    assert not increasing(B, C, av), av
for av in (-3, sp.Rational(-41, 20), -10):
    assert increasing(B, C, av), av
print('S1 (2) OK: 역함수 존재 ⇔ a<=-2, 최댓값 -2 (a 격자 확인)')

assert S1['ans'] == [r'(1) \([-2,\ 1]\)', r'(2) \(-2\)']
# 정답이 본문 수와 같지 않음
txt = S1['body'] + ''.join(q[0] for q in S1['subs'])
nums = set(re.findall(r'-?\d+', txt))
assert '-2' not in nums, nums

# 오답 값
negall = [p for p in grid if L.subs(x, p) < 0]; assert min(negall) > -2 and max(negall) < 4     # [-2,4]
assert sp.discriminant(3 * x**2 - 6 * x + 24, x) < 0                                          # 부호 바꿈 → 감소 구간 없음
assert sorted(sp.solve(L, x))[1] == 4                                                         # 큰 근 4
for w in (r'\([-2,\ 4]\)', r'\(4\)', '감소 구간이 없다', '최댓값이 없다'): assert w in S1['wrong'], w

# 빼 보기
def abl(cn, m_): print(f'ABLATION S1 {cn}: {m_}')
# (1)의 a=1: a를 바꾸면 감소 구간이 바뀜 (a=0 → [-2,0], a=5 → [-2,4]), a가 정해지지 않으면 답이 없음
def dec_int(av):
    ng = [p for p in grid if p != av and (R if p > av else L).subs(x, p) < 0]
    return (sp.nsimplify(round(float(min(ng)) * 2) / 2), sp.nsimplify(round(float(max(ng)) * 2) / 2)) if ng else None
assert dec_int(1) == (-2, 1) and dec_int(0) == (-2, 0) and dec_int(5) == (-2, 4) and dec_int(-3) is None
abl('(1)의 a=1', '필요(a=0이면 [-2,0], a=5이면 [-2,4], a=-3이면 감소 구간 없음 — a 없이는 정해지지 않음)')
# 절댓값 계수 24: 바꾸면 답이 바뀜(원문 구조 보존 확인), 예 C=9(B=-3) → 작은 근 -1
assert inc_max_a(-3, 9) == -1 and inc_max_a(-3, 24) == -2
abl('절댓값 계수 24', '필요(9이면 최댓값 -1, 계수가 x<a 쪽 근을 정함)')
# x^2 계수 -3: 0이면 작은 근 -2√2
assert inc_max_a(0, 24) == -2 * sp.sqrt(2)
abl('x^2 계수 -3', '필요(0이면 최댓값 -2√2)')
# 상수항은 원문 +2를 뺌(군더더기 없음)
assert re.search(r'24\|x-a\|\\\]', S1['body'])   # 상수항 없음

# 배점·형식
assert len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts] == [5, 5], pts
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D15)' and S1['key'] == 'D15' and S1['bunseok'] is False
assert '이러한' not in txt and '이와 같은' not in txt
for fld in [S1['body']] + [q[0] for q in S1['subs']] + S1['rubric'] + S1['sol'] + [S1['fast'], S1['wrong'], S1['note'], S1['var']] + S1['ans']:
    for m in re.findall(r'\\\(.*?\\\)', fld, re.S): assert '<' not in m and '>' not in m, m
    for m in re.findall(r'\\\[.*?\\\]', fld, re.S): assert '<' not in m and '>' not in m, m
# 범위 밖 원문 미사용
for bad in ['D33', 'D34', 'D37', 'D39', 'D41', 'D49', 'D50', 'D51', 'D52', 'D57', 'D58', 'D60', 'D63', 'D65', 'D68', 'M65']:
    assert bad not in S1['note'] + S1['precedent'] + S1['key'], bad
print('ALL OK')
