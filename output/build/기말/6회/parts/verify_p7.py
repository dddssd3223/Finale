# -*- coding: utf-8 -*-
# 서답형1 (자체, D24 유형) · 서답형2 (I67 학교식) 검증 · author='claude'
import sympy as sp, os, sys, re
x, t, a, k, C = sp.symbols('x t a k C', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7.py')).read(), ns)
S1, S2 = ns['SITEMS']['S1'], ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def extrema_abs(fl, fr):
    """x<0 조각 fl, x>=0 조각 fr (f(0)=fl(0)=fr(0)) 인 연속함수의 극값 [(x, 값, 종류)] — 미분불가 점 x=0 포함, 부호 변화로 판정"""
    out = []
    pts = []
    for c in sp.Poly(sp.diff(fl, x), x).real_roots():
        if c < 0: pts.append((c, sp.diff(fl, x)))
    for c in sp.Poly(sp.diff(fr, x), x).real_roots():
        if c > 0: pts.append((c, sp.diff(fr, x)))
    for c, d in pts:
        e = R(1, 10**4)
        l, r_ = d.subs(x, c - e), d.subs(x, c + e)
        if l > 0 > r_: out.append((c, (fl if c < 0 else fr).subs(x, c), 'max'))
        elif l < 0 < r_: out.append((c, (fl if c < 0 else fr).subs(x, c), 'min'))
    dl, dr = sp.diff(fl, x).subs(x, 0), sp.diff(fr, x).subs(x, 0)   # 왼쪽·오른쪽 미분계수
    e = R(1, 10**4)
    sl, sr = sp.diff(fl, x).subs(x, -e), sp.diff(fr, x).subs(x, e)
    if sl < 0 < sr: out.append((0, fr.subs(x, 0), 'min'))
    elif sl > 0 > sr: out.append((0, fr.subs(x, 0), 'max'))
    return sorted(out, key=lambda u: u[0])

def pieces(expr_abs):
    """expr_abs 는 Abs(x)를 포함한 식 → (x<0 조각, x>=0 조각)"""
    return sp.expand(expr_abs.subs(sp.Abs(x), -x)), sp.expand(expr_abs.subs(sp.Abs(x), x))

# ================= S1 =================
# --- 원문 D24: x^3+x^2/2+a|x|+2, 좌·우미분계수 곱 -4, a>0 → 모든 극값의 합 11/2
fo = x**3 + R(1, 2) * x**2 + a * sp.Abs(x) + 2
flo, fro = pieces(fo)
asol = [v for v in sp.solve(sp.diff(flo, x).subs(x, 0) * sp.diff(fro, x).subs(x, 0) + 4, a) if v > 0]
assert asol == [2]
ex_o = extrema_abs(flo.subs(a, 2), fro.subs(a, 2))
assert ex_o == [(-1, R(7, 2), 'max'), (0, 2, 'min')] and sum(v for _, v, _ in ex_o) == R(11, 2)
assert F.I['D24'][2] == '②' and F.I['D24'][1][1] == r'\dfrac{11}2'
print('D24 원문 OK: a=2, 극대 7/2 + 꺾인 극소 2 = 11/2 (원문 정답 ② 11/2)')

# --- S1: 2x^3+3x^2+a|x|+1, x=-2 에서 극값
assert r"f(x)=2x^3+3x^2+a|x|+1" in S1['body'] and r"\(x=-2\)에서 극값을 갖는다" in S1['body']
f1 = 2 * x**3 + 3 * x**2 + a * sp.Abs(x) + 1
fl1, fr1 = pieces(f1)
# x=-2 는 x<0 조각 안이고 미분가능 → f'(-2)=0 이 필요; 모든 실수 a 에서 극값 여부를 직접 판정
sol_a = sp.solve(sp.diff(fl1, x).subs(x, -2), a)
assert sol_a == [12]
ok_a = [av for av in sol_a if any(c == -2 for c, _, _ in extrema_abs(fl1.subs(a, av), fr1.subs(a, av)))]
assert ok_a == [12]
# a 를 넓게 훑어도 x=-2 에서 극값인 a 는 12 뿐 (f'(-2)≠0 이면 극값 아님)
assert [av for av in range(-30, 31) if any(c == -2 for c, _, _ in extrema_abs(fl1.subs(a, av), fr1.subs(a, av)))] == [12]
A1 = 12
assert S1['ans'][0] == r'(1) \(12\)'
fl, fr = fl1.subs(a, A1), fr1.subs(a, A1)
assert sp.expand(sp.diff(fl, x) - 6 * (x - 1) * (x + 2)) == 0
assert sp.Poly(sp.diff(fr, x), x).real_roots() == []                  # x>0 에서 근 없음
ex1 = extrema_abs(fl, fr)
assert ex1 == [(-2, 21, 'max'), (0, 1, 'min')], ex1
ANS_S1 = sum(v for _, v, _ in ex1)
assert ANS_S1 == 22 and S1['ans'][1] == r'(2) \(22\)'
# 수치 확인: x=0 근처 좌우 값이 f(0)=1 보다 큼(극소)
fn = sp.lambdify(x, f1.subs(a, A1))
assert fn(-0.01) > 1 and fn(0.01) > 1 and fn(-2.01) < 21 and fn(-1.99) < 21
# 오답 값
assert sp.solve(sp.diff(fr1, x).subs(x, -2), a) == [-12]                # |x|=x 로 두면 a=-12
assert ANS_S1 - 1 == 21                                                 # x=0 빼면 21
assert fl.subs(x, 1) == -6 and 21 + fl.subs(x, 1) == 15 and 21 + 1 + fl.subs(x, 1) == 16
exw = extrema_abs(fl1.subs(a, -12), fr1.subs(a, -12))                   # a=-12 이면 극점 구조가 바뀜
assert (0, 1, 'max') in exw and any(c == 1 and kd == 'min' for c, _, kd in exw)
# 배점·형식
assert 'cond' not in S1 and len(S1['subs']) == 2 and len(S1['ans']) == 2 and len(S1['sol']) == 2
assert [q[1] for q in S1['subs']] == ['5점, 풀이 과정을 쓰시오.', '5점, 풀이 과정을 쓰시오.']
pts1 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S1['rubric'][:2]]
assert [sum(u) for u in pts1] == [5, 5], pts1
assert not re.findall(r'\[(\d)점\]', ''.join(S1['rubric'][2:]))
assert S1['level'] == '중' and S1['db_ref'] == '자체 (가장 가까운 D24)'
print('S1 OK: (1) a=12 하나, (2) 극대 f(-2)=21 + 꺾인 극소 f(0)=1 = 22')

def abl1(cname, msg): print(f'ABLATION S1 {cname}: {msg}')
# (a) x=-2 에서 극값 삭제: a 가 정해지지 않고 극값의 합도 바뀜
outs = []
for av in (6, 12, 24):
    e_ = extrema_abs(fl1.subs(a, av), fr1.subs(a, av)); outs.append((av, sp.nsimplify(sp.simplify(sum(v for _, v, _ in e_)))))
assert len({o[1] for o in outs}) == 3 and outs[1][1] == 22
abl1('x=-2에서 극값', '필요(없으면 a가 정해지지 않아 (2)가 ' + ', '.join(f'a={u}이면 {sp.N(v, 6) if u != 12 else v}' for u, v in outs) + ')')
# (b) 위치 -2 를 다른 값으로: 답이 바뀜(위치 수치가 a 를 정함)
for xp in (-1, -3):
    av = sp.solve(sp.diff(fl1, x).subs(x, xp), a)[0]
    assert av != 12
abl1('극값 위치 -2', '필요(x=-1이면 a=0, x=-3이면 a=36으로 바뀜)')
# (c) |x| 항: a|x| 를 ax 로 바꾸면 x=0 꺾인 점이 사라져 (2)의 판단이 없어짐
fs = 2 * x**3 + 3 * x**2 + a * x + 1
as_ = sp.solve(sp.diff(fs, x).subs(x, -2), a)[0]
crs = sp.Poly(sp.diff(fs.subs(a, as_), x), x).real_roots()
abl1('a|x|의 절댓값', f'필요(ax로 바꾸면 a={as_}, 극점 {crs}로 바뀌어 x=0의 극소 판단이 없어짐)')


# ================= S2 =================
def solve_i67(rhs, lo_f=1, lo_g=-1, kk=None):
    """∫_{lo_f}^x t f + ∫_{lo_g}^x t g = rhs, f = x g' (f, g 다항식) 의 해 (g, f, k값) — 일반 이차 g 로 전수"""
    p0, p1, p2, p3 = sp.symbols('p0:4')
    g = p3 * x**3 + p2 * x**2 + p1 * x + p0          # 삼차까지 열어 둠(차수도 결정되는지 확인)
    f = x * sp.diff(g, x)
    lhs = sp.integrate((t * f.subs(x, t)), (t, lo_f, x)) + sp.integrate((t * g.subs(x, t)), (t, lo_g, x))
    eqs = sp.Poly(sp.expand(lhs - rhs), x).all_coeffs()
    unk = [p0, p1, p2, p3] + ([kk] if kk is not None else [])
    sols = sp.solve(eqs, unk, dict=True)
    return [(sp.expand(g.subs(s)), sp.expand(f.subs(s)), s.get(kk) if kk is not None else None) for s in sols]

# --- 원문 I67: 3x^4+8x^3-3x^2 → g=4x^2+12x-6, ∫_0^3 g = 72
so = solve_i67(3 * x**4 + 8 * x**3 - 3 * x**2)
assert len(so) == 1 and so[0][0] == 4 * x**2 + 12 * x - 6
assert sp.integrate(so[0][0], (x, 0, 3)) == 72 and F.I['I67'][2] == '①' and F.I['I67'][1][0] == '72'
print('I67 원문 OK: g=4x^2+12x-6, ∫_0^3 g=72 (원문 정답 ① 72)')
# LIVE2-03-271: 6x^4-4x^3-6x^2 → 9 (S2 와 수치가 다름)
sl = solve_i67(6 * x**4 - 4 * x**3 - 6 * x**2)
assert len(sl) == 1 and sp.integrate(sl[0][0], (x, 0, 3)) == 9

# --- S2
assert r"3x^4-4x^3+x^2+k" in S2['cond'][0][1] and r"\int_1^x tf(t)" in S2['cond'][0][1] and r"\int_{-1}^x tg(t)" in S2['cond'][0][1]
assert S2['cond'][1][1] == r"\(f(x)=xg'(x)\)" and '상수 \\(k\\)' in S2['body']
s2 = solve_i67(3 * x**4 - 4 * x**3 + x**2 + k, kk=k)
assert len(s2) == 1, s2                                                   # g, f, k 하나로 정해짐
G2, F2, K2 = s2[0]
assert G2 == 4 * x**2 - 6 * x + 2 and F2 == 8 * x**2 - 6 * x and K2 == -4
ANS1 = sp.expand(F2 + G2); ANS2 = sp.integrate(G2, (x, 0, 3)); ANS3 = K2
assert ANS1 == 12 * x**2 - 12 * x + 2 and ANS2 == 15 and ANS3 == -4
assert S2['ans'] == [r'(1) \(f(x)+g(x)=12x^2-12x+2\)', r'(2) \(15\)', r'(3) \(-4\)']
# 항등식 직접 확인 + x=1, x=-1 두 대입 모두 k=-4
lhs = sp.integrate(t * F2.subs(x, t), (t, 1, x)) + sp.integrate(t * G2.subs(x, t), (t, -1, x))
assert sp.expand(lhs - (3 * x**4 - 4 * x**3 + x**2 - 4)) == 0
assert sp.integrate(t * G2.subs(x, t), (t, -1, 1)) == -4 and sp.integrate(t * F2.subs(x, t), (t, 1, -1)) == 4
# 숨은 관계: 원문·LIVE271 은 g 상수항 = -3/2 × x^2 계수 라 k=0, S2 는 이를 깨서 k≠0
assert so[0][0].coeff(x, 0) == R(-3, 2) * so[0][0].coeff(x, 2) and G2.coeff(x, 0) != R(-3, 2) * G2.coeff(x, 2)
# 오답 값
xg_int = sp.integrate(ANS1, x)                                            # 4x^3-6x^2+2x 를 g 로
assert sp.integrate(xg_int, (x, 0, 3)) == 36
assert sp.expand(x * ANS1) == 12 * x**3 - 12 * x**2 + 2 * x              # (1) x 로 안 나눔
assert sp.solve(-sp.integrate(t * F2.subs(x, t), (t, 1, -1)) - (8 + k), k) == [-12]   # x=-1 대입 부호 실수
assert sp.integrate(G2.subs(x, t), (t, -1, 1)) == R(20, 3)                     # t 빠뜨림 → k=20/3
# 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3 and [c[0] for c in S2['cond']] == ['가', '나']
assert [q[1] for q in S2['subs']] == ['3점, 답만 적으시오.', '4점, 답만 적으시오.', '3점, 답만 적으시오.']
pts2 = [[int(v) for v in re.findall(r'\[(\d)점\]', line)] for line in S2['rubric'][:3]]
assert pts2 == [[3], [4], [3]] and sum(map(sum, pts2)) == 10, pts2
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:]))
assert all('채점자 참고용' in line for line in S2['rubric'][:3])
assert S2['db_ref'] == 'I67 후보_순위 2' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
print('S2 OK: g=4x^2-6x+2, f=8x^2-6x, k=-4 하나 → (1) 12x^2-12x+2 (2) 15 (3) -4')

def abl2(cname, msg): print(f'ABLATION S2 {cname}: {msg}')
# (a) (나) 삭제: f+g 만 정해지고 g 는 자유 → (2)·(3) 이 정해지지 않음
outs = []
for c0 in (0, 1, 3):                                   # g 에 c0*x 를 더하고 f 에서 뺌
    g_ = G2 + c0 * x; f_ = ANS1 - g_
    l_ = sp.integrate(t * f_.subs(x, t), (t, 1, x)) + sp.integrate(t * g_.subs(x, t), (t, -1, x))
    kk = sp.expand(l_ - (3 * x**4 - 4 * x**3 + x**2))
    assert kk.free_symbols == set()                    # (가)는 k=kk 로 성립
    outs.append((sp.integrate(g_, (x, 0, 3)), kk))
assert len({o[0] for o in outs}) == 3 and len({o[1] for o in outs}) == 3
abl2('(나) f(x)=xg\'(x)', '필요(없으면 (2), (3)이 ' + ', '.join(f'({u}, {v})' for u, v in outs) + ' 등으로 정해지지 않음)')
# (b) (가) 삭제: f, g 에 대한 식이 (나)뿐 → 아무것도 정해지지 않음
gs = [x**2, x**2 + 1]
assert len({sp.integrate(g_, (x, 0, 3)) for g_ in gs}) == 2
abl2('(가) 적분 등식', '필요(없으면 g(x)=x^2, x^2+1 등 아무 다항함수나 되어 (1)–(3)이 정해지지 않음)')
# (c) (가)의 아래끝: 둘 다 같은 1 로 두면 k 가 바뀜 → 아래끝 -1 이 (3)을 정함
s_c = solve_i67(3 * x**4 - 4 * x**3 + x**2 + k, lo_f=1, lo_g=1, kk=k)
assert len(s_c) == 1 and s_c[0][0] == G2 and s_c[0][2] != -4
abl2('(가)의 아래끝 -1', f'필요(1로 바꾸면 (1), (2)는 그대로지만 k={s_c[0][2]}로 바뀜)')
# (d) 우변 계수 교체가 일함: 원문 우변 + k 이면 k=0, g 원문
s_d = solve_i67(3 * x**4 + 8 * x**3 - 3 * x**2 + k, kk=k)
assert s_d[0][2] == 0 and sp.integrate(s_d[0][0], (x, 0, 3)) == 72
abl2('우변 3x^4-4x^3+x^2', '필요(원문 우변이면 k=0, (2)=72로 원문 그대로)')

print('ALL OK')
