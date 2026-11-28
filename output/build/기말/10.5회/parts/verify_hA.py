# -*- coding: utf-8 -*-
# hA.py (10.5회 새 1–5번) 검증: 원래 문항 풀이 재확인 · 새 수치 계산 정답 = 목표 선지 · 유일성 · 선지 5개 서로 다름·등차
# · wrongs가 선지에 있고 실제 실수 경로로 나옴 · 조건 빼 보기 · 정답이 원래 답·원래/새 본문 수와 다름 · 형식
import os, re
import sympy as sp
from sympy import symbols, Rational, integrate, solve, expand, nsimplify, Abs, Piecewise, oo
x, t, k, a, b, c = symbols('x t k a b c', real=True)
ns = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hA.py'), encoding='utf-8') as fh:
    exec(fh.read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 5, 3: 1, 4: 4, 5: 2}
KEYS = {1: 'I55', 2: 'I3', 3: 'I8', 4: 'I38', 5: 'I57'}
ORIG_ANS = {1: 12, 2: -3, 3: 15, 4: 6, 5: -8}
ORIG_BODY = {
    1: r"\(\displaystyle\int_{-1}^{3}(2x+|x-1|)\,dx\)의 값은?",
    2: r"함수 \(f(x)=6x^2-4x-4\)의 한 부정적분 \(F(x)\)에 대하여 \(F(0)=1\)일 때, \(F(1)\)의 값은?",
    3: r"x^3-9x (|x|>1) 2x+2 (|x|<1) 점 \((0,\ k)\) 최솟값이 \(-2\)",
    4: r"\(f(1)+f(-1)=\dfrac43\) \(\displaystyle0\le\int_0^1 f(x)\,dx\le2\) 계수가 \(1\) f(2x)",
    5: r"\(f(x)=x^2+6x+a\) \int_0^x \([k,\,k+1]\) 최솟값이 \(-7\)",
}
REQ = ('body', 'choices', 'ans', 'sol', 'fast', 'wrong', 'wrongs', 'level', 'key', 'src', 'note')
assert sorted(IT) == [1, 2, 3, 4, 5]

def nums(s):
    out = set()
    for m in re.finditer(r'(-?)\\dfrac\{?(\d+)\}?\{?(\d+)\}?|(-?)(?<![\w^])(\d+)', s):
        if m.group(2):
            out.add(Rational(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1))
        else:
            n = int(m.group(5)); out |= {nsimplify(n), nsimplify(-n)}
    return out

for no, it in IT.items():
    assert all(f in it for f in REQ), no
    assert it['key'] == KEYS[no]
    assert '이러한' not in it['body'] + it['sol'] + it['note']
    for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'] + it['sol'] + it['fast'] + it['wrong'] + it['note'], re.S):
        assert '<' not in m and '>' not in m, m
    assert len(it['choices']) == 5 and all(w in it['choices'] for w in it['wrongs'])
    assert it['choices'][it['ans'] - 1] not in it['wrongs']

def chk(no, val, wrongs):
    it = IT[no]
    ch = [nsimplify(s) for s in it['choices']]
    d = {ch[i + 1] - ch[i] for i in range(4)}
    ws = sorted(nsimplify(w) for w in it['wrongs'])
    val = nsimplify(val)
    good = (it['ans'] == WANT[no] and ch[it['ans'] - 1] == val and len(set(ch)) == 5 and len(d) == 1
            and ws == sorted(nsimplify(w) for w in wrongs) and val not in ws
            and val != ORIG_ANS[no] and val not in nums(ORIG_BODY[no]) and val not in nums(it['body']))
    print(f'{no}번: 계산 {val}, 선지 위치 {it["ans"]} (목표 {WANT[no]}), 공차 {list(d)}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

# ===== 원래 문항 다시 풀기 =====
assert integrate(2*x + Abs(x - 1), (x, -1, 3)) == 12
assert (2*x**3 - 2*x**2 - 4*x + 1).subs(x, 1) == -3
print('원래 문항 1·2 OK')

# ===== 1번 =====
v1 = integrate(3*x + Abs(x - 2), (x, 0, 4))
assert v1 == integrate(2*x + 2, (x, 0, 2)) + integrate(4*x - 2, (x, 2, 4)) == 28
w1a = integrate(3*x + (x - 2), (x, 0, 4))                      # 나누지 않고 |x-2|=x-2
w1b = integrate(3*x, (x, 0, 4)) + integrate(2 - x, (x, 0, 2))   # 삼각형 하나만
assert (w1a, w1b) == (24, 26)
assert integrate(2*x, (x, -1, 3)) + integrate(1 - x, (x, -1, 1)) == 10   # 10회에서 고른 ③ 10도 같은 경로
assert integrate(3*x - (x - 2), (x, 0, 4)) == 24                # 반대 부호로 통째 벗겨도 ① (다른 선지 안 만듦)
chk(1, v1, [w1a, w1b])

# ===== 2번 =====
C = symbols('C')
F = integrate(6*x**2 - 2*x + 3, x) + C
Cv = solve(F.subs(x, 0) - 1, C); assert Cv == [1]
v2 = F.subs(C, 1).subs(x, 1)
w2 = (F - C).subs(x, 1)                                          # 적분상수 빠뜨림
f1 = (6*x**2 - 2*x + 3).subs(x, 1)                               # f(1)을 답으로: 선지 밖
assert f1 == 7 and str(f1) not in IT[2]['choices']
assert v2 - w2 == 1                                              # 빼 보기: F(0) 조건 없이는 F(1)=4+C 결정 안 됨
chk(2, v2, [w2])

# ===== 3번 =====
def solve3(mid, outer, m):
    fm = integrate(mid, (x, 0, x)) + k                           # -1<x<1
    f1_, fm1 = fm.subs(x, 1), fm.subs(x, -1)
    fR = f1_ + integrate(outer, (x, 1, x))                        # x>1
    fL = fm1 - integrate(outer, (x, x, -1))                       # x<-1
    crit = solve(outer, x)
    mins = [fR.subs(x, r) for r in crit if r > 1] + [fL.subs(x, r) for r in crit if r < -1]
    return fm, fR, fL, mins
fm, fR, fL, mins = solve3(4*x + 4, x**3 - 9*x, -2)
assert sorted(expand(m - k) for m in mins) == [-18, -10]
fpw = Piecewise((fL, x < -1), (fm, x <= 1), (fR, True))
# 부호표·극값: -1은 극값 아님, 1은 극대, ±3 극소
fp = Piecewise((x**3 - 9*x, Abs(x) > 1), (4*x + 4, True))
sgn = [sp.sign(fp.subs(x, s)) for s in (-4, -2, -0.5, 0.5, 2, 4)]
assert sgn == [-1, 1, 1, 1, -1, 1]
kk = solve(fL.subs(x, -3) + 2, k); assert kk == [16]
v3 = kk[0]
# 유일성: 최솟값을 수치로 확인
import numpy as np
g = sp.lambdify(x, fpw.subs(k, v3), 'numpy')
xs = np.linspace(-8, 8, 160001)
assert abs(min(g(xx) for xx in xs[::40]) + 2) < 1e-6 and abs(g(-3.0) + 2) < 1e-12
w3 = solve(fR.subs(x, 3) + 2, k)[0]                               # 오른쪽 극솟값을 최솟값으로
assert w3 == 8
# 원래 수치 다시 풀기(15)
_, _, fL0, _ = solve3(2*x + 2, x**3 - 9*x, -2)
assert solve(fL0.subs(x, -3) + 2, k) == [15]
# 빼 보기: 연속 조건 빼면(바깥 조각 상수 따로) k 결정 안 됨 → 생략 불가 확인
assert fR.subs(x, 3) != fL.subs(x, -3)
chk(3, v3, [w3])

# ===== 4번 =====
f = x**2 + b*x + c
cs = solve(f.subs(x, 1) + f.subs(x, -1) + Rational(2, 3), c); assert cs == [Rational(-4, 3)]
I0 = expand(integrate(f, (x, 0, 1)).subs(c, cs[0]))
assert I0 == b/2 - 1
blo, bhi = solve(I0 - 1, b)[0], solve(I0 - 3, b)[0]; assert (blo, bhi) == (4, 8)
J = expand(integrate(f.subs(x, 2*x), (x, 0, 1)).subs(c, cs[0])); assert J == b
v4 = J.subs(b, blo) + J.subs(b, bhi)
w4a = 1 + 3                                                       # ∫f(2x)=∫f
w4b = 2*1 + 2*3                                                   # ∫f(2x)=2∫f
K = expand(integrate(f, (x, -1, 2)).subs(c, cs[0]))               # 원문 묻는 값
w4c = K.subs(b, blo) + K.subs(b, bhi)
assert (w4a, w4b, w4c) == (4, 8, 16)
# 빼 보기: (가)를 빼면 ∫f(2x) = 2∫f - c + 2/3 이라 c에 따라 합이 바뀜
Jc = expand(integrate(f.subs(x, 2*x), (x, 0, 1)))
assert expand(Jc - (2*integrate(f, (x, 0, 1)) - c + Rational(2, 3))) == 0 and sp.diff(Jc, c) != 0
# 원래 수치(6)
cs0 = solve(f.subs(x, 1) + f.subs(x, -1) - Rational(4, 3), c)[0]
J0 = expand(integrate(f.subs(x, 2*x), (x, 0, 1)).subs(c, cs0)); I00 = expand(integrate(f, (x, 0, 1)).subs(c, cs0))
assert J0.subs(b, solve(I00, b)[0]) + J0.subs(b, solve(I00 - 2, b)[0]) == 6
chk(4, v4, [w4a, w4b, w4c])

# ===== 5번 =====
def amin(p, kv):                                                  # [k,k+1]에서 f>=0 이 되는 a의 최솟값
    q = -(x**2 + 2*p*x)
    pts = [kv, kv + 1] + ([-p] if kv <= -p <= kv + 1 else [])
    return max(q.subs(x, s) for s in pts)
def ks(p, m):
    cand = set()
    for r in solve(k**2 + 2*p*k + m, k):
        cand |= {r, r - 1}
    return sorted(kv for kv in cand if amin(p, kv) == m)
K5 = ks(2, -12); assert K5 == [-7, 2]
v5 = K5[0] * K5[1]
# 유일성: k 격자 전수 확인(amin(k) = -12 인 k 는 위 두 개뿐), 축 품으면 4
grid = [Rational(i, 100) for i in range(-1200, 1201)]
assert [kv for kv in grid if amin(2, kv) == -12] == [-7, 2]
assert all(amin(2, kv) == 4 for kv in grid if -3 <= kv <= -2)
w5 = sp.prod(solve(k**2 + 4*k - 12, k))                            # 한 끝점만 보고 두 근 곱
assert w5 == -12 and amin(2, -6) == -5
assert ks(3, -7) == [-8, 1]                                       # 원래 수치(-8)
chk(5, v5, [w5])

print('ALL OK')
