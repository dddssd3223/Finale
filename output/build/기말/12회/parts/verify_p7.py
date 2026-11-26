# -*- coding: utf-8 -*-
# 서답형1 (자체, D56 방향) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a, b, k = sp.symbols('x a b k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1 = ns['SITEMS']['S1']
assert set(ns['SITEMS']) == {'S1'}
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

# --- 원문 D56: x^3+ax^2-9x+b, x=1 극소, 극댓값 28 → a+b=4
fo = x**3 + a * x**2 - 9 * x + b
ao = sp.solve(sp.diff(fo, x).subs(x, 1), a)[0]
fo1 = fo.subs(a, ao); crit = sp.solve(sp.diff(fo1, x), x)
bo = sp.solve(fo1.subs(x, -3) - 28, b)[0]
assert ao == 3 and sorted(crit) == [-3, 1] and ao + bo == 4 and F.I['D56'][2] == '4'
print('D56 원문 OK: a=3, b=1, a+b=4')

# --- S1 본문
assert r"f(x)=x^3+ax^2-24x+b" in S1['body'] and r"\(x=4\)에서 극소" in S1['body'] and r"극솟값이 \(-75\)" in S1['body'] and 'cond' not in S1
f = x**3 + a * x**2 - 24 * x + b
# (1) a: f'(4)=0 의 해 하나, 그때 x=4가 실제로 극소
sa = sp.solve(sp.diff(f, x).subs(x, 4), a); assert sa == [-3]
f1 = f.subs(a, -3); fp = sp.diff(f1, x)
assert sp.expand(fp - 3 * (x - 4) * (x + 2)) == 0
assert fp.subs(x, sp.Rational(7, 2)) < 0 and fp.subs(x, sp.Rational(9, 2)) > 0   # 음 → 양: 극소
assert fp.subs(x, -3) > 0 and fp.subs(x, -1) < 0                                   # x=-2 극대
sb = sp.solve(f1.subs(x, 4) + 75, b); assert sb == [5]
fF = sp.expand(f1.subs(b, 5)); assert fF == x**3 - 3 * x**2 - 24 * x + 5
assert fF.subs(x, -2) == 33 and fF.subs(x, 4) == -75 and fF.subs(x, 0) == 5
A1 = (-3, 5)

# (2) 정수 k 전수: 서로 다른 실근이 양수 2개, 음수 1개
def sig(kv):
    rs = sorted(set(sp.Poly(fF - kv, x).real_roots()))
    return len(rs), sum(1 for r in rs if r > 0), sum(1 for r in rs if r < 0), rs
good = [kv for kv in range(-120, 80) if sig(kv)[:3] == (3, 2, 1)]
assert good == list(range(-74, 5)), (good[:3], good[-3:])
# 경계 확인: k=5 → 근 0 포함, k=-75 → 중근(서로 다른 실근 2개), k=33 → 2개
assert 0 in sig(5)[3] and sig(5)[:3] == (3, 1, 1)
assert sig(-75)[0] == 2 and sig(33)[0] == 2
# 실수 k 범위도 확인 (반정수 격자)
half = [sp.Rational(i, 2) for i in range(-200, 100)]
assert all((sig(kv)[:3] == (3, 2, 1)) == (-75 < kv < 5) for kv in half)
assert S1['ans'] == [r'(1) \(a=-3\), \(b=5\)', r'(2) \(-75&lt;k&lt;5\)']
print('S1 OK: (1) a=-3, b=5 (x=4 극소 확인) (2) -75<k<5 (정수·반정수 전수 + 경계 k=5, -75, 33)')

# 정답이 본문 수와 같지 않음
txt = S1['body'] + ''.join(q[0] for q in S1['subs'])
nums = set(re.findall(r'-?\d+', txt))
for v in ('-3', '5'): assert v not in nums, (v, nums)   # (2)의 아래끝 -75는 주어진 극솟값 그대로(범위 답이라 허용), 위끝 5는 본문에 없음

# 오답 값
assert sp.solve(48 - 8 * a - 24, a) == [3]                                   # 부호 실수
assert sp.solve(f1.subs(x, -2) + 75, b) == [-103]                             # 극솟값을 f(-2)로
three = [kv for kv in range(-120, 80) if sig(kv)[0] == 3]; assert three == list(range(-74, 33))   # 양수 조건 빠뜨림: -75<k<33
assert sig(5)[3][1] == 0                                                       # k=5 포함 오답: 근 0
for w in (r'\(a=3\)', r'\(b=-103\)', r'\(-75&lt;k&lt;33\)', r'\(-75&lt;k\le5\)', r'\(-75\le k&lt;5\)', r'\(-75&lt;k&lt;0\)'): assert w in S1['wrong'], w

# 빼 보기
def abl(cn, m_): print(f'ABLATION S1 {cn}: {m_}')
# x=4에서 극소 삭제: a 정해지지 않음 (a=0, a=-6 모두 극솟값 -75로 b 조정 가능한 함수 존재)
for av in (0, -6):
    g = x**3 + av * x**2 - 24 * x
    cps = sorted(sp.solve(sp.diff(g, x), x)); xm = max(cps)        # 최고차 양수 → 큰 임계점이 극소
    bv = -75 - g.subs(x, xm)
    gg = g + bv
    assert sp.simplify(gg.subs(x, xm)) == -75 and av != -3
abl('x=4에서 극소', '필요(없으면 a=0, -6처럼 극솟값이 -75인 함수가 여럿, (1)의 a가 정해지지 않음)')
# 극솟값 -75 삭제: b 정해지지 않고, (2)도 바뀜 (b=0이면 f(0)=0 → -80<k<0, 79개 아님)
fb0 = x**3 - 3 * x**2 - 24 * x
# b에 따라 (2)의 조건 집합이 옮겨짐을 직접 확인: b=0 → k 범위 (-80, 0)
good0 = [kv for kv in range(-150, 80) if (lambda rs: len(rs) == 3 and sum(1 for r in rs if r > 0) == 2 and sum(1 for r in rs if r < 0) == 1)(sorted(set(sp.Poly(fb0 - kv, x).real_roots())))]
assert good0 == list(range(-79, 0)) and good0 != good
abl('극솟값 -75', '필요(없으면 (1)의 b가 정해지지 않고, (2)의 범위 (b-80, b)가 b=0이면 (-80, 0)처럼 옮겨져 정해지지 않음)')
# (2)의 양수·음수 조건 삭제: 세 실근만이면 107
abl('(2)의 양의 실근 2개·음의 실근 1개', '필요(없으면 서로 다른 세 실근 조건만으로 -75<k<33, 위끝이 극댓값으로 바뀜)')

# 배점·형식
assert len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts] == [5, 5], pts
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D56)' and S1['key'] == 'D56' and S1['bunseok'] is False
assert '이러한' not in txt and '이와 같은' not in txt
# 수식 안 맨 부등호 없음
for fld in [S1['body']] + [q[0] for q in S1['subs']] + S1['rubric'] + S1['sol'] + [S1['fast'], S1['wrong'], S1['note'], S1['var']]:
    for m in re.findall(r'\\\(.*?\\\)', fld, re.S): assert '<' not in m and '>' not in m, m
print('ALL OK')
