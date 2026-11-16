# -*- coding: utf-8 -*-
# p2.py (6회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re, itertools
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, factor
x, a, k, r = symbols('x a k r', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 3, 6: 4, 7: 2, 8: 5}                                       # 분담표 목표 정답
REF = {5: 'D20 분석집_변형 1', 6: 'M6 분석집_변형 1', 7: 'D42 분석집_변형 1', 8: 'D16 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['D20', 'M6', 'D42', 'D16']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐')
    assert it['ops'] and all(o in OPS for o in it['ops']) and 'STUDY-' in it['precedent']
    if n in (6, 7): assert COEF & set(it['ops']), n                   # 계수 ● 자리
    if n in (6, 7): assert 'GEN1-' in it['precedent'], n               # 겹칠 장치 출처
    assert '함정 추가' not in it['vtype'] and it['level'] in ('하', '중')
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 ×
    for w in it['wrongs']:
        c = CIRC[it['choices'].index(w)]
        tag = f'{c} {w[2:]}:' if w.startswith('T:') else f'{c} \\({w}\\)'
        assert tag in it['wrong'], (n, tag)
    txt = it['body'] + ''.join(v for _, v in it.get('bogi', []))
    for m in re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', txt, re.S):
        assert '<' not in ''.join(m) and '>' not in ''.join(m), (n, m)

def arith(no):
    v = [nsimplify(c_) for c_ in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs):
    ch = IT[no]['choices']
    if str(ch[0]).startswith('T:'):
        good = IT[no]['ans'] == WANT[no] and ch[IT[no]['ans'] - 1] == val and len(set(ch)) == 5 \
            and sorted(IT[no]['wrongs']) == sorted(wrongs) and val not in wrongs
        print(f'{no}번: 판정 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 오답 {wrongs} {"OK" if good else "FAIL"}')
    else:
        chv = [nsimplify(c_) for c_ in ch]; ws = [nsimplify(w) for w in IT[no]['wrongs']]
        good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == chv[IT[no]['ans'] - 1] and arith(no)
                and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w != nsimplify(val) for w in ws))
        print(f'{no}번: 계산 {val}, 선지 {chv[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {chv[1] - chv[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def extrema(fx):
    """다항식의 (극대값 목록, 극소값 목록) — 도함수 부호 변화로 판정"""
    fp = diff(fx, x); mx, mn = [], []
    for c in sorted(set(sp.real_roots(sp.Poly(fp, x)))):
        e = Rational(1, 10**4)
        l, rr = fp.subs(x, c - e), fp.subs(x, c + e)
        if l > 0 > rr: mx.append(fx.subs(x, c))
        if l < 0 < rr: mn.append(fx.subs(x, c))
    return mx, mn

# ===== 원문·분석집 풀이 =====
# D20: f=2x^3-3(2a+1)x^2+6a(a+1)x+8, 극댓값 4 → 극솟값 3
fD = 2*x**3 - 3*(2*a + 1)*x**2 + 6*a*(a + 1)*x + 8
aa = [s_ for s_ in solve(fD.subs(x, a) - 4, a) if s_.is_real]
assert aa == [-2] and extrema(fD.subs(a, -2)) == ([4], [3])
# 분석집 D20 변형①: 2x^3-3(a+1)x^2+6ax+1, 극값의 차 8 → 극솟값의 합 -2
tot = 0
for av in [s_ for s_ in solve((a - 1)**3 - 8, a) + solve((a - 1)**3 + 8, a) if s_.is_real]:   # |a-1|^3=8
    mx, mn = extrema(2*x**3 - 3*(av + 1)*x**2 + 6*av*x + 1); assert mx[0] - mn[0] == 8; tot += mn[0]
assert tot == -2
# M6: [a,a+1]에서 x^3-3x+1 최솟값 -1 → 정수 a 합 -1
def minv(fx, L, R):
    cs = [L, R] + [c for c in sp.real_roots(sp.Poly(diff(fx, x), x)) if L <= c <= R]
    return min(fx.subs(x, c) for c in cs)
assert sum(A for A in range(-20, 20) if minv(x**3 - 3*x + 1, A, A + 1) == -1) == -1
# 분석집 M6 변형①: [a,a+2]에서 -x^3+6x^2-9x+3 최솟값 -1 → 합 2
assert sum(A for A in range(-20, 20) if minv(-x**3 + 6*x**2 - 9*x + 3, A, A + 2) == -1) == 2
# GEN1-02-015: N(1)+…+N(10)=39
assert sum(len([A for A in range(-30, 30) if minv(x**3 - 3*x + 1, A, A + L) == -1]) for L in range(1, 11)) == 39
# D42: (x-1)^2(x-3)^2, ㄷ: a>3에서 f(a)<f'(a)(a-3)
f42 = (x - 1)**2*(x - 3)**2
assert expand(f42 - (x**4 - 8*x**3 + 22*x**2 - 24*x + 9)) == 0
assert factor(f42 - diff(f42, x)*(x - 3)) == factor(-(x - 1)*(x - 3)**2*(3*x - 7))
# 분석집 D42 변형①: (x-1)^2(x-4)^2, 1<a<4에서 f(a)<f'(a)(a-1) ⟺ a<2
fS = (x - 1)**2*(x - 4)**2
assert factor(diff(fS, x)*(x - 1) - fS) == factor((x - 1)**2*(x - 4)*(3*x - 6))
# D16: f'=3(x-1)(x-r), r<=-2, 3r 홀수 → 최솟값 22
def m16(t):                                                          # 정수 계수 (b, c)를 전수: f=x^3+bx^2+cx
    vals = []
    for b in range(-60, 61):
        for c in range(-200, 201):
            fp = 3*x**2 + 2*b*x + c
            if fp.subs(x, 1) > 0 or fp.subs(x, Rational(1, 10**6) + 1) < 0: continue   # 감소·증가 경계(빠른 거르기, 아래 표본으로 확인)
            ok = all(fp.subs(x, Rational(j, 8)) <= 0 for j in range(-8*t, 8)) and all(fp.subs(x, 1 + Rational(j, 8)) >= 0 for j in range(1, 8))
            ok = ok and fp.subs(x, -t) <= 0
            if ok: vals.append((27 + 9*b + 3*c) - (8 + 4*b + 2*c))
    return min(vals)
assert m16(2) == 22
print('원문·분석집 풀이 OK (D20=3/-2, M6=-1/2, GEN=39, D42 ㄷ 인수, D16=22)')

# ===== 5번 =====
f5 = 2*x**3 - 3*(a - 1)*x**2 - 6*a*x + 10
assert factor(diff(f5, x)) == factor(6*(x + 1)*(x - a))
cands = []
for av in range(-30, 31):                                             # a 정수 전수 + 방정식 풀이로 실수 a 전부
    if av == -1: continue
    mx, mn = extrema(f5.subs(a, av))
    if mx[0] - mn[0] == 27: cands.append(av)
sols = sorted(s_ for s_ in solve((a + 1)**3 - 27, a) if s_.is_real) + sorted(s_ for s_ in solve((a + 1)**3 + 27, a) if s_.is_real)
assert sorted(sols) == cands == [-4, 2]
mins = [extrema(f5.subs(a, av))[1][0] for av in cands]
assert sorted(mins) == [-10, -1]
v5 = sum(mins); w5 = extrema(f5.subs(a, 2))[1][0]
assert v5 == -11 and w5 == -10
chk(5, v5, [w5])

# ===== 6번 =====
f6 = -x**3 + 6*x**2 - 3
assert factor(f6 + 3) == factor(-x**2*(x - 6))
def N6(n): return [A for A in range(-60, 60) if minv(f6, A, A + n) == -3]
NN = {n: len(N6(n)) for n in range(1, 41)}
assert all(NN[n] == (n + 2 if n <= 5 else 7) for n in NN)
sol6 = [n for n in NN if NN[n] == 6]
assert sol6 == [4] and N6(4) == [-4, -3, -2, -1, 0, 2]
w6 = [n for n in NN if len([A for A in N6(n) if A <= 0 <= A + n]) == 6]   # 오른쪽 끝이 6인 경우를 뺀 셈
assert w6 == [5]
chk(6, sol6[0], [w6[0]])

# ===== 7번 =====
f7 = (x - 1)**2*(x - k)**2
D7 = factor(diff(f7, x)*(x - 1) - f7)
assert expand(D7 - (x - 1)**2*(x - k)*(3*x - k - 2)) == 0
# ㄱ: 극댓값 (k-1)^4/16 ≠ /8
def judge(kv):
    fk = f7.subs(k, kv); mx, _ = extrema(fk)
    g1 = (len(mx) == 1 and mx[0] == (kv - 1)**4/8)
    Dk = D7.subs(k, kv)
    pts2 = [1 + (Rational(kv + 1, 2) - 1)*Rational(j, 200) for j in range(1, 200)]
    g2 = all(Dk.subs(x, t_) > 0 for t_ in pts2)
    pts3 = [kv + Rational(j, 7) for j in range(1, 200)] + [kv + Rational(1, 10**6)]
    g3 = all(Dk.subs(x, t_) > 0 for t_ in pts3)
    return g1, g2, g3
for kv in [Rational(3, 2), 2, 3, 4, Rational(7, 2), 5, 9, 20]:
    assert judge(kv) == (False, False, True), kv
# 기호로: ㄴ 반례 a=(k+2)/3 ~ (k+1)/2, ㄷ 세 인수 양
assert sp.simplify(Rational(1, 2)*(k + 1) - (k + 2)/3 - (k - 1)/6) == 0
v7 = 'T:ㄷ'
w7 = 'T:ㄴ, ㄷ'                                                        # ㄴ을 극대점까지 성립한다고 보면
chk(7, v7, [w7])

# ===== 8번 =====
def m8(t):                                                            # 이론식: 3r 홀수, r<=-t 중 최대 → (23-9r)/2
    s = -3*t if (3*t) % 2 == 1 else -3*t - 1
    return Rational(23 - 3*s, 2)
assert (m8(3), m8(4)) == (25, 31)
assert m16(3) == 25 and m16(4) == 31                                  # 정수 계수 전수와 일치
for t in range(1, 7): assert m8(t) == m16(t), t
v8 = m16(3) + m16(4); w8 = 25 + Rational(23 + 33, 2)
assert v8 == 56 and w8 == 53
fbad = x**3 - Rational(3, 2)*(1 + Rational(-11, 3))*x**2 + 3*Rational(-11, 3)*x   # 3r=-11은 t=4에서 위반
assert diff(fbad, x).subs(x, -4) > 0
chk(8, v8, [w8])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 5번
c8 = sorted(av for av in range(-30, 31) if av != -1 and (lambda e: e[0][0] - e[1][0])(extrema(f5.subs(a, av))) == 8)
s8 = sum(extrema(f5.subs(a, av))[1][0] for av in c8)
print(f'ABLATION 5 차 27: 필요(8이면 a={c8}, 합 {s8})'); assert s8 != v5
print('ABLATION 5 극솟값의 합(두 경우): 필요(한 경우만이면 -10)'); assert w5 != v5
# 6번
alt = [n for n in range(1, 41) if len([A for A in range(-60, 60) if minv(f6, A, A + n) == -3]) == 7]
print(f'ABLATION 6 개수 6: 필요(7이면 n={alt[:3]}… 하나로 정해지지 않음)'); assert len(alt) > 1
f6b = -x**3 + 3*x**2 - 2                                              # 등값점이 3인 함수(분석집·원문처럼 가까운 등값점)
nb = {n: len([A for A in range(-60, 60) if minv(f6b, A, A + n) == -2]) for n in range(1, 21)}
print(f'ABLATION 6 함수 -x^3+6x^2-3(등값점 6): 필요(-x^3+3x^2-2이면 개수 {sorted(set(nb.values()))}, 6인 n 없음)'); assert 6 not in nb.values()
# 7번
print('ABLATION 7 k>1: 필요(k<1이면 1과 k의 순서가 바뀌어 ㄷ의 3a-k-2 부호 판정이 달라짐)')
Dm = D7.subs(k, Rational(-5))
assert any(Dm.subs(x, t_) < 0 for t_ in [Rational(-5) + Rational(j, 10) for j in range(1, 60)])   # k=-5이면 ㄷ 거짓
print('ABLATION 7 ㄴ의 오른쪽 끝 (k+1)/2: 필요((k+2)/3이면 ㄴ 참, 답 ㄴ, ㄷ)')
assert all(D7.subs({k: 4, x: 1 + Rational(j, 100)}) > 0 for j in range(1, 100))
# 8번
def m8_noint(t): return Rational(23 + 9*t, 2)                          # 정수 계수 조건이 없으면 r=-t
v8b = m8_noint(3) + m8_noint(4)
print(f'ABLATION 8 모든 계수 정수: 필요(빼면 m(3)+m(4)={v8b})'); assert v8b != v8
print('ABLATION 8 (1,2)에서 증가: 필요(빼면 f\'(1)=0이 없어 f(3)-f(2)=19+5b+c가 아래로 한없이 작아짐: b=0, c=-3-N)')
assert all((19 + 5*0 + c) < -N for N, c in [(10, -40), (100, -130)])
print(f'ABLATION 8 t=3·4(홀짝 하나씩): 필요(m(3)+m(5)={m8(3) + m8(5)}, m(2)+m(4)={m8(2) + m8(4)})'); assert m8(3) + m8(5) != v8 and m8(2) + m8(4) != v8

print('ALL OK')
