# -*- coding: utf-8 -*-
# 서답형1 (자체, D21 유형) · 서답형2 (I69 학교식, LIVE2-03-279 단계화) 검증 · author='claude'
import sympy as sp, os, sys, re, random
x, t, a, b, k = sp.symbols('x t a b k', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def extrema(fx):
    """다항함수 fx의 극점: f'의 홀수 중복 근에서 부호 변화로 극대/극소"""
    P = sp.Poly(sp.diff(fx, x), x); cnt = {}
    for r in P.real_roots(): cnt[r] = cnt.get(r, 0) + 1
    out = []
    for r in sorted(cnt):
        if cnt[r] % 2:
            eps = R(1, 10**6)
            l = sp.sign(sp.N(P.eval(r - eps), 50)); rr = sp.sign(sp.N(P.eval(r + eps), 50))
            out.append((r, '극대' if l > 0 > rr else '극소'))
    return out

def solve_a_max_at(fa, p):
    """f'(p)=0인 a 가운데 x=p가 실제로 극대인 것"""
    sols = sp.solve(sp.diff(fa, x).subs(x, p), a)
    return [s for s in sols if (p, '극대') in extrema(fa.subs(a, s))]

# ================= S1 =================
# --- 원문 D21
fo = -x**4 / 4 + x**3 / 3 + 2 * x**2 + a * x
ao = solve_a_max_at(fo, 2); assert ao == [-4]
mo = [fo.subs(a, -4).subs(x, r) for r, s in extrema(fo.subs(a, -4)) if s == '극소']
assert mo == [R(-23, 12)] and F.I['D21'][2] == '③' and F.I['D21'][1][2] == r'-\dfrac{23}{12}'
print('D21 원문 OK: a=-4, 극솟값 -23/12 (원문 정답 ③)')

# --- S1
assert r"f(x)=-\dfrac14x^4+\dfrac43x^3-\dfrac12x^2+ax" in S1['body'] and r"\(x=3\)에서 극대" in S1['body']
f1a = -x**4 / 4 + R(4, 3) * x**3 - x**2 / 2 + a * x
A1 = solve_a_max_at(f1a, 3); assert A1 == [-6]          # a 유일
f1 = f1a.subs(a, -6)
assert sp.expand(sp.diff(f1, x) + (x + 1) * (x - 2) * (x - 3)) == 0
ex1 = extrema(f1); assert ex1 == [(-1, '극대'), (2, '극소'), (3, '극대')], ex1
mins = [f1.subs(x, r) for r, s in ex1 if s == '극소']; assert mins == [R(-22, 3)]
# (2) 열린구간 (k, k+1)에서 증가 ⇔ 그 구간에서 f' ≥ 0 (f'의 근이 유한 개)
fp1 = sp.diff(f1, x)
def incr_on(kv):
    """(kv, kv+1)에서 f'≥0 인지: 구간 안 f'의 근으로 나눈 조각마다 가운데 점 부호"""
    lo, hi = sp.nsimplify(kv), sp.nsimplify(kv) + 1
    cuts = [lo] + sorted(r for r in sp.Poly(fp1, x).real_roots() if lo < r < hi) + [hi]
    return all(fp1.subs(x, (cuts[i] + cuts[i + 1]) / 2) > 0 for i in range(len(cuts) - 1))
grid = [R(i, 20) for i in range(-200, 201)]
good = [kv for kv in grid if incr_on(kv)]
assert all(kv <= -2 or kv == 2 for kv in good) and 2 in good and -2 in good
assert all(incr_on(kv) for kv in grid if kv <= -2)
assert not any(incr_on(2 + R(1, 10**4) * s) for s in (-1, 1))      # k=2는 고립값
assert S1['ans'] == [r'(1) \(-\dfrac{22}{3}\)', r'(2) \(k\le-2\) 또는 \(k=2\)']
# 오답 값
assert f1.subs(x, 3) == R(-27, 4) and f1.subs(x, -1) == R(47, 12)
assert all(fp1.subs(x, v) < 0 for v in (0, R(1, 2), 1, 4))           # 감소 구간 확인(오답 근거)
for w in (r'-\dfrac{27}{4}', r'\dfrac{47}{12}', r'k\le-2\)', r'k\le-1', r'2\le k\le3'): assert w in S1['wrong'], w
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D21)'
print('S1 OK: (1) a=-6, 극솟값 -22/3 (2) k≤-2 또는 k=2 (k 격자 1/20 간격 [-10, 10] 전수)')

def abl1(c, m): print(f'ABLATION S1 {c}: {m}')
# 'x=3에서 극대' 삭제: a 가 정해지지 않음 (a=0, a=-6 이 다른 극솟값)
m0 = sorted(sp.N(f1a.subs(a, 0).subs(x, r), 6) for r, s in extrema(f1a.subs(a, 0)) if s == '극소')
assert m0 != [sp.N(R(-22, 3), 6)]
abl1('x=3에서 극대', f'필요(없으면 a가 정해지지 않음: a=0이면 극솟값 {m0})')
# '극대' → '극소': f'(3)=0 이면 a=-6 인데 x=3은 극대라 그런 a가 없음
sols = sp.solve(sp.diff(f1a, x).subs(x, 3), a)
assert sols == [-6] and (3, '극소') not in extrema(f1a.subs(a, -6))
abl1("'극대'(극소로 바꾸면)", '필요(극소로 바꾸면 조건을 만족시키는 a가 없음)')
# 구간 길이 1 → 2: 고립값 k=2가 사라짐
fp_save = fp1
def incr_len(kv, L):
    lo, hi = sp.nsimplify(kv), sp.nsimplify(kv) + L
    cuts = [lo] + sorted(r for r in sp.Poly(fp1, x).real_roots() if lo < r < hi) + [hi]
    return all(fp1.subs(x, (cuts[i] + cuts[i + 1]) / 2) > 0 for i in range(len(cuts) - 1))
g2 = [kv for kv in grid if incr_len(kv, 2)]
assert max(g2) == -3 and all(kv <= -3 for kv in g2)
abl1('구간 (k, k+1)의 길이 1', '필요(길이 2이면 k≤-3만 남아 k=2가 사라짐)')
# 2/3 대신 4/3 (x^3 계수): f' 근 구조가 달라짐
f9 = -x**4 / 4 + R(1, 1) * x**3 - x**2 / 2 + a * x
s9 = sp.solve(sp.diff(f9, x).subs(x, 3), a)
abl1('f의 계수 4/3, -1/2', f'필요(x^3 계수 1이면 a={s9}, 극소 위치·증가 구간이 바뀜)')


# ================= S2 =================
def h_of(fx, c):
    return sp.expand((x + c) * fx)

# --- 원문 I69: ㄱ 참, ㄴ ∫_0^1 g=-1 참, ㄷ 참(롤) → ⑤
fI = x**3 + x**2 + a * x + b
gI = fI + (x - 1) * sp.diff(fI, x)
assert sp.expand(sp.diff((x - 1) * fI, x) - gI) == 0                     # ㄱ
sab = sp.solve([sp.diff(fI, x).subs(x, -1), fI.subs(x, -1)], [a, b], dict=True); assert sab == [{a: -1, b: -1}]
assert sp.integrate(gI.subs(sab[0]), (x, 0, 1)) == -1                       # ㄴ
random.seed(1)
for _ in range(200):                                                       # ㄷ: f(0)=0 → (0,1)에 g의 근
    av = R(random.randint(-400, 400), random.randint(1, 20))
    gg = sp.Poly(gI.subs({a: av, b: 0}), x)
    assert any(0 < r < 1 for r in gg.real_roots())
assert F.I['I69'][2] == '⑤' and F.I['I69'][1][4] == 'T:ㄱ, ㄴ, ㄷ'
print('I69 원문 OK: ㄱ·ㄴ·ㄷ 모두 참 (원문 정답 ⑤)')

# --- S2
assert r"f(x)=x^3+x^2+ax+b" in S2['body'] and r"\(x=1\)에서 극값 \(0\)" in S2['body'] and r"g(x)=f(x)+(x+3)f'(x)" in S2['body'] and 'cond' not in S2
q1, q2, q3 = [q[0] for q in S2['subs']]
assert r'\int_0^2 g(x)' in q2 and r'\int_k^x g(t)' in q3 and '개수가 \\(3\\)' in q3 and '곱' in q3
# (1) a, b 유일 + x=1이 실제로 극점
sab2 = sp.solve([sp.diff(fI, x).subs(x, 1), fI.subs(x, 1)], [a, b], dict=True)
assert sab2 == [{a: -5, b: 3}]
f2 = fI.subs(sab2[0]); assert sp.factor(f2) == (x - 1)**2 * (x + 3)
assert any(r == 1 for r, _ in extrema(f2))
g2f = sp.expand(f2 + (x + 3) * sp.diff(f2, x))
h2 = h_of(f2, 3); assert sp.expand(sp.diff(h2, x) - g2f) == 0
assert sp.expand(h2 - (x**2 + 2 * x - 3)**2) == 0
# (2)
I2 = sp.integrate(g2f, (x, 0, 2)); assert I2 == 16 and h2.subs(x, 2) - h2.subs(x, 0) == 16
# (3) ∫_k^x g = h(x)-h(k); 서로 다른 실근 개수를 높이 c=h(k)에 대해 전수
def nroots(c):
    return len(set(sp.Poly(sp.expand(h2 - c), x).real_roots()))
ex2 = extrema(h2); assert ex2 == [(-3, '극소'), (-1, '극대'), (1, '극소')]
assert h2.subs(x, -1) == 16 and h2.subs(x, -3) == 0 == h2.subs(x, 1)
cs = [R(i, 4) for i in range(-8, 120)]
three = [c for c in cs if nroots(c) == 3]; assert three == [16]
assert all(nroots(c) == (0 if c < 0 else 2 if c == 0 else 4 if c < 16 else 3 if c == 16 else 2) for c in cs)
# 높이 h(k)는 0 이상만 나오므로 c=h(k)=16 ⇔ k의 값
ks = sorted(set(sp.solve(sp.Eq(h2.subs(x, k), 16), k)), key=lambda v: float(v))
assert ks == [-1 - 2 * sp.sqrt(2), -1, -1 + 2 * sp.sqrt(2)], ks
for kv in ks:   # 원래 방정식 ∫_k^x g(t)dt=0 그대로 확인
    eq = sp.integrate(g2f.subs(x, t), (t, kv, x))
    assert len(set(sp.Poly(sp.expand(eq), x).real_roots())) == 3
# k 격자(1/8 간격)에서 3개가 되는 k 없음(세 k는 격자 밖 무리수·-1) → -1 만 격자에 있음
kg = [R(i, 8) for i in range(-48, 33)]
assert [kv for kv in kg if nroots(h2.subs(x, kv)) == 3] == [-1]
P3 = sp.simplify(sp.prod(ks)); assert P3 == 7
assert S2['ans'] == [r'(1) \(a=-5\), \(b=3\)', r'(2) \(16\)', r'(3) \(7\)']
print('S2 OK: (1) a=-5, b=3 (2) 16 (3) k=-1, -1±2√2, 곱 7 (높이 c 전수 + k 확인)')

# 오답 값
assert f2.subs(x, 2) - f2.subs(x, 0) == 2                                # (x+3) 인수 뺌
assert h2.subs(x, 2) + h2.subs(x, 0) == 34                               # h(0) 부호
assert sp.expand((-1 - 2 * sp.sqrt(2)) * (-1 + 2 * sp.sqrt(2))) == -7      # 극대점 제외
assert P3 * (-3) * 1 == -21                                              # 극솟값 점 포함
for w in (r'b=-3', r'f(2)-f(0)=2', r'25+9=34', r'\(-1\) ·', r'\(-7\)', r'=-21'): assert w in S2['wrong'], w
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [q[1] for q in S2['subs']] == ['2점, 답만 적으시오.', '3점, 답만 적으시오.', '5점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S2['rubric'][:3]]
assert pts2 == [[2], [3], [5]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line_ for line_ in S2['rubric'][:3])
assert S2['db_ref'] == 'I69 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
for it in (S1, S2):
    tx = it['body'] + ''.join(q[0] for q in it['subs'])
    assert '이러한' not in tx and '이와 같은' not in tx
    assert not [m for m in re.findall(r'\\\(.*?\\\)', tx) if '<' in m or '>' in m]
print('S2 형식 OK')

def abl2(c, m): print(f'ABLATION S2 {c}: {m}')
# (a) 'x=1에서 극값 0' 삭제 → a, b 미정
abl2('x=1에서 극값 0', '필요(없으면 a, b가 정해지지 않아 (1)–(3) 모두 정해지지 않음)')
# (b) 극값 0 → 극값 4: h 가 완전제곱이 아니어서 (2)·(3)이 바뀜
sb = sp.solve([sp.diff(fI, x).subs(x, 1), fI.subs(x, 1) - 4], [a, b], dict=True)[0]
fb = fI.subs(sb); hb = h_of(fb, 3)
I2b = hb.subs(x, 2) - hb.subs(x, 0); assert I2b != 16
exb = extrema(hb); assert len(exb) == 3
abl2('극값 0의 0', f'필요(극값 4이면 (2)가 {I2b}, h가 완전제곱이 아니라 (3)의 높이 판단이 바뀜)')
# (c) 곱하는 일차식 x+3 → x-1(원문): h=(x-1)^3(x+3), W 모양이 아님
hc = h_of(f2, -1); exc = extrema(hc)
assert len(exc) == 1 and sp.integrate(sp.diff(hc, x), (x, 0, 2)) != 16
abl2('(x+3)f\'(x)의 x+3', f'필요(x-1이면 h=(x-1)^3(x+3)의 극값이 {len(exc)}개라 (3)에서 실근 3개인 k가 없고 (2)도 {hc.subs(x,2)-hc.subs(x,0)})')
# (d) (3)의 '3' → '2': 높이 0 또는 16 초과 → k 가 무수히 많아 곱이 정해지지 않음
assert nroots(0) == 2 and nroots(17) == 2
abl2('(3)의 개수 3', '필요(2로 바꾸면 h(k)=0 또는 h(k)>16인 k가 무수히 많아 곱이 정해지지 않음)')
# (e) (3)의 아래끝 k → 고정 0: 방정식 h(x)=9 → 실근 4개, 묻는 값이 사라짐
assert nroots(h2.subs(x, 0)) == 4
abl2('(3)의 아래끝 k', '필요(0으로 고정하면 h(x)=9의 실근이 4개로 정해져 k를 묻지 못함)')
# (f) (2)의 구간 [0, 2]
assert sp.integrate(g2f, (x, 0, 1)) == -9
abl2('(2)의 구간 끝 2', '필요(끝을 1로 두면 -9)')

print('ALL OK')
