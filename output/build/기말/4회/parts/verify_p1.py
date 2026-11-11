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
KEY = {1: ('M42', 'M42 후보_순위 1'), 2: ('I54', 'I54 후보_순위 1'), 3: ('D53', 'D53 후보_순위 1'), 4: ('M23', '자체 (가장 가까운 M23)')}
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

def meet_times(p1, p2, strict=True):
    """두 위치 p1(t), p2(t)가 같아지는 시각 (strict: t>0, 아니면 t≥0), 오름차순"""
    rs = sorted(set(real_roots(Poly(p1 - p2, t))))
    return [r for r in rs if (r > 0 if strict else r >= 0)]

# ===== 원문 풀이 =====
# M42: x^3-3x^2-9x+k=0, 서로 다른 실근 2개 → k=-5, 27, 합 22 (④)
ks0, _ = two_root_ks(x**3 - 3*x**2 - 9*x)
assert ks0 == [-5, 27] and sum(ks0) == 22
# I54: ∫_0^1(4x^3+a)dx=8 → a=7 (②)
assert solve(integrate(4*x**3 + a, (x, 0, 1)) - 8, a) == [7]
# D53: f(1)=3, 1<x<5에서 f'≥5 → f(5)≥3+5·4=23, f=5x-2에서 등호 (③)
assert 3 + 5*(5 - 1) == 23 and (5*x - 2).subs(x, 1) == 3 and (5*x - 2).subs(x, 5) == 23
# M23: x1=t^3-5t^2, x2=-2t^2+10t → t=5, p-q=35 (단답)
o1, o2 = t**3 - 5*t**2, -2*t**2 + 10*t
assert meet_times(o1, o2) == [5] and (diff(o1, t) - diff(o2, t)).subs(t, 5) == 35
print('원문 풀이 OK (M42=22, I54=7, D53=23, M23=35)')

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
x1, x2 = -t**3 + 7*t**2, 2*t**2 + 6*t
assert expand((x1 - x2) + t*(t - 2)*(t - 3)) == 0
mt = meet_times(x1, x2)                                           # t>0에서 만나는 시각 전수
assert mt == [2, 3]
assert [x1.subs(t, s) for s in mt] == [x2.subs(t, s) for s in mt] == [20, 36]
vP, vQ = diff(x1, t), diff(x2, t)
assert expand(vP - (-3*t**2 + 14*t)) == 0 and expand(vQ - (4*t + 6)) == 0
assert all(vP.subs(t, s) != 0 and vQ.subs(t, s) != 0 and vP.subs(t, s) != vQ.subs(t, s) for s in mt)   # 만나는 순간 정지·같은 속도 아님
v4 = vP.subs(t, mt[1])
assert v4 == 15
w4_first = vP.subs(t, mt[0])                                      # 오답: 처음 만나는 순간의 P의 속도
w4_Q = vQ.subs(t, mt[1])                                          # 오답: 두 번째 만나는 순간의 Q의 속도
assert (w4_first, w4_Q) == (16, 18)
assert vQ.subs(t, mt[0]) == 14 and vQ.subs(t, mt[0]) not in [cv(c) for c in IT[4]['choices']]         # 두 실수가 겹쳐 정답이 되는 경로 없음
chk(4, v4, [w4_first, w4_Q])

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
both = sorted({vP.subs(t, s) for s in mt})
print(f'ABLATION 4 두 번째로: 필요(빼면 만나는 순간이 t={mt} 둘이라 속도 {both}로 정해지지 않음)'); assert len(both) == 2
mt0 = meet_times(x1, x2, strict=False)
print(f'ABLATION 4 t>0: 필요(t≥0이면 만나는 시각 {mt0}, 두 번째는 t={mt0[1]}, 속도 {vP.subs(t, mt0[1])} ≠ {v4})'); assert mt0 == [0, 2, 3] and vP.subs(t, mt0[1]) != v4
x2b = 2*t**2 + 4*t
mtb = meet_times(x1, x2b)
print(f'ABLATION 4 x2의 6t: 필요(4t이면 만나는 시각 {mtb}, 두 번째 속도 {vP.subs(t, mtb[1])} ≠ {v4})'); assert vP.subs(t, mtb[1]) != v4

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
