# -*- coding: utf-8 -*-
# p1.py (4회 1–4번) 검증: 원문 풀이 · 계산 정답 = 지정 선지(분담표 정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차(오름차순) · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re, random
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, nsimplify, Poly, real_roots, discriminant, oo, limit
x, t, a, k = symbols('x t a k', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 4, 2: 2, 3: 5, 4: 1}                                   # 분담표 정답 ④ ② ⑤ ①
KEY = {1: ('M42', 'M42 후보_순위 1'), 2: ('I54', 'I54 후보_순위 1'), 3: ('D53', 'D53 후보_순위 1'), 4: ('M11', '자체 (가장 가까운 M11)')}
assert sorted(IT) == [1, 2, 3, 4]
for n, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[n], n
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent']
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype'] and len(it['vtype']) <= 3 and it['level'] in ('하', '중', '중상', '상', '최상')
    assert 'cond' not in it and 'bogi' not in it and 'class="fig"' not in it['body'] and 'class="cond"' not in it['body']   # 1–4번: 상자·그림 없음
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(c):
    return nsimplify(str(c))

def arith(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0, list(d)[0]

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    ok_ar, dd = arith(no)
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and ok_ar and dd > 0
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def nroots(p):
    """다항식 p(x)=0의 서로 다른 실근의 개수"""
    return len(set(real_roots(Poly(p, x))))

def two_root_ks(h):
    """h(x)+k=0의 서로 다른 실근이 2개인 실수 k 전부: 판별식 = 0인 k(겹친 근이 있는 경우)를 모두 구해 개수를 직접 셈"""
    cand = solve(discriminant(h + k, x), k)
    return sorted(c for c in cand if nroots(h + c) == 2), cand

def min_on_ge0(h):
    """x≥0에서 다항식 h(x)(최고차항 계수 양수)의 최솟값과 그 값을 주는 x 전부: 끝점 0과 x>0인 정류점을 모두 비교"""
    assert limit(h, x, oo) == oo
    pts = [sp.Integer(0)] + [r for r in set(real_roots(Poly(diff(h, x), x))) if r > 0]
    m = min(h.subs(x, r) for r in pts)
    return m, sorted(r for r in pts if h.subs(x, r) == m)

# ===== 원문 풀이 =====
# M42: x^3-3x^2-9x+k=0, 서로 다른 실근 2개 → k=-5, 27, 합 22 (④)
ks0, _ = two_root_ks(x**3 - 3*x**2 - 9*x)
assert ks0 == [-5, 27] and sum(ks0) == 22
# I54: ∫_0^1(4x^3+a)dx=8 → a=7 (②)
assert solve(integrate(4*x**3 + a, (x, 0, 1)) - 8, a) == [7]
# D53: f(1)=3, 1<x<5에서 f'≥5 → f(5)≥3+5·4=23, f=5x-2에서 등호 (③)
assert 3 + 5*(5 - 1) == 23 and (5*x - 2).subs(x, 1) == 3 and (5*x - 2).subs(x, 5) == 23
# M11: x≥0에서 2x^3-6x^2+14>a → 최솟값 h(2)=6, 정수 a의 최댓값 5 (②)
o4 = 2*x**3 - 6*x**2 + 14
assert min_on_ge0(o4) == (6, [2]) and max(n for n in range(-20, 21) if n < 6) == 5
print('원문 풀이 OK (M42=22, I54=7, D53=23, M11=5)')

# ===== 1번 =====
h1 = 2*x**3 - 15*x**2 + 24*x
assert expand(diff(h1, x) - 6*(x - 1)*(x - 4)) == 0
assert (h1.subs(x, 1), h1.subs(x, 4)) == (11, -16)               # k=0일 때의 극댓값·극솟값 (부호가 다름: 원문 5, -27과 같은 배치)
ks1, cand1 = two_root_ks(h1)
assert sorted(cand1) == [-11, 16] and ks1 == [-11, 16]            # 겹친 근이 생기는 k는 둘뿐이고 둘 다 서로 다른 실근 2개
for kk in range(-60, 61):                                         # 전수: 정수 k를 훑어 실근 개수 확인 (-11<k<16에서 3개, 밖에서 1개)
    c = nroots(h1 + kk)
    assert c == (2 if kk in (-11, 16) else 3 if -11 < kk < 16 else 1), kk
v1 = sum(ks1)
assert v1 == 5
w1_sign = h1.subs(x, 1) + h1.subs(x, 4)                           # 오답: 극값 11, -16을 그대로 k로 봄
assert w1_sign == -5 == -v1
chk(1, v1, [w1_sign])

# ===== 2번 =====
I2 = integrate(6*x**2 + a, (x, 0, 1))
assert expand(I2 - (2 + a)) == 0
sol2 = solve(I2 - 8, a)
assert sol2 == [6]                                                # a에 대한 일차방정식 → 해 하나
v2 = sol2[0]
w2_div = solve((3*x**3 + a*x).subs(x, 1) - 8, a)[0]               # 오답: 6x^2의 부정적분을 3x^3으로
w2_org = solve(integrate(4*x**3 + a, (x, 0, 1)) - 8, a)[0]         # 오답: 원문 식의 값 1+a=8 (원문 답)
assert (w2_div, w2_org) == (5, 7)
chk(2, v2, [w2_div, w2_org])

# ===== 3번 =====
# 평균값 정리: f(6)-f(2)=4f'(c) (2<c<6), f'(c)≤4 → f(6)≤3+16
fc = symbols('fc', real=True)
assert sp.expand((3 + (6 - 2)*fc) - 19 - 4*(fc - 4)) == 0         # f(6)-19 = 4(f'(c)-4) ≤ 0 → f(6)≤19
eq3 = 4*x - 5                                                     # 등호를 주는 함수
assert eq3.subs(x, 2) == 3 and diff(eq3, x) == 4 and eq3.subs(x, 6) == 19
# 확인 1: 이차함수 족 f=p(x-2)^2+q(x-2)+3, f'=2p(x-2)+q ≤4 (2<x<6) ⇔ q≤4, 8p+q≤4. f(6)=16p+4q+3=2(8p+q)+2q+3 ≤ 8+8+3
p_, q_ = symbols('p_ q_', real=True)
fq = p_*(x - 2)**2 + q_*(x - 2) + 3
assert expand(fq.subs(x, 6) - (2*(8*p_ + q_) + 2*q_ + 3)) == 0
# 확인 2: f'=4-g(x)^2 꼴(g는 임의의 다항식)이면 f(6)=19-∫g^2 ≤ 19, 등호는 g=0뿐
random.seed(4)
for _ in range(300):
    g = sum(random.randint(-3, 3)*x**i for i in range(4))
    val = 3 + integrate(4 - g**2, (x, 2, 6))
    assert val <= 19 and (val == 19) == (g == 0)
v3 = eq3.subs(x, 6)                                               # 상한 19가 실제로 달성됨 → 최댓값
assert v3 == 19
w3_inc = 4*(6 - 2)                                                # 오답: 늘어나는 양만 구하고 f(2)=3을 더하지 않음
assert w3_inc == 16
chk(3, v3, [w3_inc])

# ===== 4번 (자체 기본형) =====
h4 = 2*x**3 - 3*x**2 + k - (12*x - 5)                             # 부등식 ⇔ h4 ≥ 0
assert expand(diff(h4, x) - 6*(x + 1)*(x - 2)) == 0
m4, at4 = min_on_ge0(h4.subs(k, 0))                               # k=0일 때 x≥0에서의 최솟값 -15 (x=2 하나)
assert (m4, at4) == (-15, [2]) and h4.subs({k: 0, x: 0}) == 5
v4 = solve(sp.Eq(m4 + k, 0), k)[0]                                # 최솟값 k-15 ≥ 0 ⇔ k ≥ 15 → 최솟값 15 (등호 포함이라 달성)
assert v4 == 15
for kk in [Rational(i, 4) for i in range(0, 161)]:                # 전수: k를 1/4 간격으로 훑어 '항상 성립 ⇔ k≥15' 확인
    assert (min_on_ge0(h4.subs(k, kk))[0] >= 0) == (kk >= 15), kk
w4_noc = -min_on_ge0(2*x**3 - 3*x**2 - 12*x)[0]                   # 오답: 우변의 상수 -5를 넣지 않음
w4_sign = -min_on_ge0(2*x**3 - 3*x**2 - 12*x - 5)[0]              # 오답: -5를 옮길 때 부호를 바꾸지 않음
assert (w4_noc, w4_sign) == (20, 25)
ch4 = [cv(c) for c in IT[4]['choices']]
assert -h4.subs({k: 0, x: 0}) not in ch4 and -h4.subs({k: 0, x: -1}) not in ch4   # 끝값 x=0(-5)·범위 밖 x=-1(-12)로 답하는 값은 선지에 없음
assert arith(4)[1] == 5                                           # 공차 5 (공차 1 아님)
chk(4, v4, [w4_noc, w4_sign])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 1번
three = [kk for kk in range(-60, 61) if nroots(h1 + kk) == 3]
print(f'ABLATION 1 실근의 개수 2: 필요(3으로 바꾸면 -11<k<16인 모든 실수라 합이 정해지지 않음, 정수만 {len(three)}개)'); assert len(three) == 26
ks1b, _ = two_root_ks(2*x**3 - 15*x**2 + 36*x)
print(f'ABLATION 1 일차항 24x: 필요(36x이면 k={ks1b}, 합 {sum(ks1b)} ≠ {v1})'); assert sum(ks1b) != v1
ks1c, _ = two_root_ks(x**3 - 3*x**2 - 9*x)
print(f'ABLATION 1 삼차식 전체: 필요(원문 식이면 합 {sum(ks1c)} ≠ {v1})')
# 2번
s2b = solve(integrate(6*x**2 + a, (x, 0, 2)) - 8, a)
print(f'ABLATION 2 적분 구간 [0, 1]: 필요([0, 2]이면 a={s2b} ≠ [{v2}])'); assert s2b != [v2]
s2c = solve(I2 - 7, a)
print(f'ABLATION 2 우변 8: 필요(7이면 a={s2c} ≠ [{v2}])'); assert s2c != [v2]
print(f'ABLATION 2 6x^2: 필요(원문 4x^3이면 a={w2_org} ≠ {v2})'); assert w2_org != v2
# 3번
vals = sorted({(4*x + c).subs(x, 6) for c in (-5, 0, 7)})
print(f"ABLATION 3 f(2)=3: 필요(빼면 f=4x+c가 모두 조건을 만족시켜 f(6)={vals}로 최댓값 없음)"); assert len(vals) == 3
m_ = symbols('m_', positive=True)
up = (3 + (4 + m_)*(x - 2)).subs(x, 6)
print(f"ABLATION 3 f'(x)≤4의 방향: 필요(≥4이면 f=3+(4+m)(x-2)에서 f(6)={up}로 최댓값 없음)"); assert limit(up, m_, oo) == oo
# 구간을 2<x<5로 줄이면: [2,5]에서 기울기 4, (5,6)에서 기울기가 자유 → f(6)이 얼마든지 커짐 (매끄러운 예: f'=4+m(x-5)^2·[x>5] 꼴, 여기서는 f(6)-f(5)=m/3)
tail = integrate(m_*(x - 5)**2, (x, 5, 6))
print(f"ABLATION 3 구간 2<x<6: 필요(2<x<5이면 x>5에서 f'=4+m(x-5)^2으로 두어 f(6)=15+4+{tail}로 최댓값 없음)"); assert limit(tail, m_, oo) == oo
print(f"ABLATION 3 상한 4: 필요(원문 5이면 3+5·4={3 + 5*4} ≠ {v3})")
# 4번
print(f'ABLATION 4 x≥0: 필요(빼면 삼차식이라 x→-∞에서 -∞, 어떤 k로도 항상 성립하지 않음)'); assert limit(h4, x, -oo) == -oo
mb = min_on_ge0((2*x**3 - 3*x**2 - 12*x))[0]
print(f'ABLATION 4 우변의 -5: 필요(빼면 최솟값 {mb}, k의 최솟값 {-mb} ≠ {v4})'); assert -mb != v4
mc = min_on_ge0(2*x**3 - 3*x**2 - 36*x + 5)[0]
print(f'ABLATION 4 우변의 12x: 필요(36x이면 k의 최솟값 {-mc} ≠ {v4})'); assert -mc != v4
print(f'ABLATION 4 최솟값: 필요(최댓값으로 바꾸면 k≥{v4}인 모든 실수라 정해지지 않음)')

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
