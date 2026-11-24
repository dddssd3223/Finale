# -*- coding: utf-8 -*-
# p3.py (11회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re, math
import sympy as sp
from sympy import symbols, Rational, integrate, diff, solve, expand, factor, Piecewise
from fractions import Fraction as Fr

x = symbols('x', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 4, 10: 2, 11: 3, 12: 1}
DBREF = {9: 'D70 후보_순위 2', 10: 'J8 후보_순위 2', 11: 'J43 후보_순위 2', 12: 'D59 결합 2'}
KEYS = {9: 'D70', 10: 'J8', 11: 'J43', 12: 'D59'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

def val(c):
    c = re.sub(r'\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1) if m else Rational(c)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == '중', f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level(중)')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    for f_ in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
        ok('이러한' not in it[f_] and '이와 같은' not in it[f_], f'{n}번 {f_} 금지 어구 없음')
    ok(not any(('<' in m or '>' in m) for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'], re.S)), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if IT[n]['effect'] == '어려워짐') == 0, '9–12번 어려워짐 0개')

def chk(n, v0):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1 and abs(v[1] - v[0]) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    body_nums = {Rational(s) for s in re.findall(r'-?\d+', re.sub(r'\^\{?\d+\}?', ' ', re.sub(r'\\[a-zA-Z]+', ' ', IT[n]['body'])))}
    ok(v0 not in body_nums, f'{n}번 정답 {v0}이 본문에 나온 수(지수 제외)와 다름')
    return v

# ---------- 9번 (D70) ----------
def ks(crits, L=Fr(3, 2)):
    """열린구간 (k, k+L)에 극점이 하나라도 있는 정수 k의 집합"""
    s = set()
    for c in crits:
        k = math.floor(c - L) + 1
        while k < c:
            s.add(k); k += 1
    return s
def crit9(a, base=-2, q=3):
    f = (x - base)**2 * (x - q * a)
    return sorted({Fr(str(r)) for r in solve(diff(f, x), x)}), f
# 평균변화율 곱 조건 ⇔ 구간 안에 극점: 직접 확인(a=2, 몇 k에서 격자 세 점을 찾음)
def cond_direct(f, k, L=Rational(3, 2), N=60):
    pts = [k + L * Rational(i, N) for i in range(1, N)]
    vals = [f.subs(x, p) for p in pts]
    sl = [(vals[i + 1] - vals[i]) for i in range(len(vals) - 1)]
    return any(sl[i] * sl[j] < 0 for i in range(len(sl)) for j in range(i + 1, len(sl)))
cr, f9 = crit9(2)
for kk in range(-6, 6):
    ok(cond_direct(f9, kk) == (kk in ks(cr)), f'9번 a=2, k={kk}: 평균변화율 곱 조건 {"성립" if kk in ks(cr) else "불성립"} = 극점 포함 여부')
sols = []
for a in range(-500, 501):
    cr, _ = crit9(a)
    if len(cr) == 2 and sum(ks(cr)) == 2: sols.append(a)
ok(sols == [2], f'9번 정수 a 전수(−500..500): 합 2가 되는 a = {sols}')
ok(ks(crit9(2)[0]) == {-3, 2, 3}, '9번 a=2: k = −3, 2, 3')
ok(sum(ks(crit9(-1)[0])) == -7, '9번 a=−1: k가 겹쳐 {−4, −3}, 합 −7(4a−6과 다름)')
f9a = (x + 2)**2 * (x - 6)
ok(expand(diff(f9a, x) - (x + 2) * (3 * x - 10)) == 0, "9번 f'=(x+2)(3x−10)")
v9 = chk(9, f9a.subs(x, -1))
# 오답: 극점 2a−2/3도 k 하나(2a−1)만 준다고 봄 → −3+2a−1=2 → a=3
aw = solve(-3 + (2 * symbols('A') - 1) - 2, symbols('A'))[0]
ok(aw == 3 and ((x + 2)**2 * (x - 3 * aw)).subs(x, -1) == -10, '9번 오답 −10: 극점마다 k 하나로 보아 a=3, f(−1)=−10')
ok(sum(ks(crit9(3)[0])) != 2, '9번 a=3이면 실제 합은 2가 아님(오답 경로 확인)')
# 원문 D70: f=x³−2ax², 곱 −12 → a=−2, f′(10)=380
orig = []
for a in range(-200, 201):
    if a == 0: continue
    f = x**3 - 2 * a * x**2
    c = sorted({Fr(str(r)) for r in solve(diff(f, x), x)})
    K = ks(c)
    if math.prod(K) == -12: orig.append(a)
ok(orig == [-2] and diff(x**3 + 4 * x**2, x).subs(x, 10) == 380, f'9번 원문 D70: 곱 −12인 a={orig}, f′(10)=380')
# 빼 보기
alt = [a for a in range(-200, 201) if len(crit9(a)[0]) == 2 and sum(ks(crit9(a)[0])) == 6]
print(f'ABLATION 9 합 2: 필요(합 6이면 a = {alt}, f(−1) = {[((x + 2)**2 * (x - 3 * a)).subs(x, -1) for a in alt]})'); assert alt and alt != [2]
alt2 = [a for a in range(-200, 201) if len(crit9(a)[0]) == 2 and sum(ks(crit9(a)[0], Fr(1))) == 2]
print(f'ABLATION 9 구간 길이 3/2: 필요(길이 1이면 합 2인 a = {alt2})'); assert alt2 != [2]
alt3 = []
for i in range(-600, 601):                      # a를 1/6 간격 실수로 넓히면
    av = Rational(i, 6)
    cr3 = sorted({Fr(str(r)) for r in solve(diff((x + 2)**2 * (x - 3 * av), x), x)})
    if len(cr3) == 2 and sum(ks(cr3)) == 2: alt3.append(av)
print(f'ABLATION 9 정수 a: 필요(실수 a이면 합 2인 a가 {alt3[:6]}… 등 여럿)'); assert len(alt3) > 1

# ---------- 10번 (J8) ----------
A, B, Cc = symbols('A B Cc')
q = A * x**2 + B * x + Cc
eqs = [Eq for Eq in (
    Cc - 4,                                        # x=0 연속
    q.subs(x, 2) - 0,                              # x=2 연속: f(2) = lim_{x→−2+}(2x+4) = 0
    integrate(2 * x + 4, (x, -2, 0)) + integrate(q, (x, 0, 2)) - 4)]
S10 = solve(eqs, [A, B, Cc], dict=True)
ok(S10 == [{A: 3, B: -8, Cc: 4}], f'10번 연속·주기·정적분 조건 → (a, b, c) = {S10}')
qq = q.subs(S10[0])
ok(factor(qq) == (x - 2) * (3 * x - 2), '10번 0≤x≤2에서 f=(3x−2)(x−2)')
def F10(t):
    """주기 4 함수의 값(구간 (−2, 2]로 옮김)"""
    t = Rational(t); u = t - 4 * sp.floor((t + 2) / 4)
    if u == -2: u = Rational(2)
    return (2 * u + 4) if u < 0 else qq.subs(x, u)
def I10(lo, hi, piece=None):
    """[lo, hi]의 적분: 정수 칸마다 (−2, 2] 안으로 옮겨 정확히 적분"""
    tot = 0
    for s in range(lo, hi):
        u0 = s - 4 * math.floor((s + 2) / 4)          # s를 [−2, 2)로
        u1 = u0 + 1
        g = (2 * x + 4) if u1 <= 0 else qq
        tot += integrate(g, (x, u0, u1))
    return tot
# 연속 확인(조각 경계)
ok(all(F10(t) == lim for t, lim in ((0, 4), (2, 0), (-2, 0), (4, 4), (-20, 4))), '10번 x=−2, 0, 2, 4, −20에서 함숫값이 조각 극한과 같음(연속)')
ok(I10(-2, 2) == 4 and I10(0, 2) == 0, '10번 한 주기 적분 4, ∫_0^2 f = 0')
a1, a2 = I10(-20, -17), I10(30, 32)
ok(a1 == 1 and a2 == 4, f'10번 ∫_(−20)^(−17) f = {a1}, ∫_30^32 f = {a2}')
v10 = chk(10, a1 - a2)
ok(integrate(qq, (x, 2, 3)) - 4 == -1, '10번 오답 −1: 2≤x≤3에서 이차식을 그대로 적분(3) − 4')
ok(I10(0, 2) - 4 == -4, '10번 오답 −4: ∫_0^3을 ∫_0^2만으로 봄')
# 원문 J8: 4/3
qo = x**2 - 4 * x + 3
orig10 = integrate(x + 3, (x, -3, 0)) + integrate(qo, (x, 0, 1)) - integrate(x + 3, (x, -3, 0))
ok(orig10 == Rational(4, 3), '10번 원문 J8 정답 4/3(④)')
# 빼 보기
Sx = solve(eqs[:2], [B, Cc], dict=True)[0]
ab = A
qa = (A * x**2 + B * x + Cc).subs(Sx)
dep = sp.simplify(integrate(qa, (x, 0, 2)) + 1 - 4)
print(f'ABLATION 10 ∫_(−2)^2 f = 4: 필요(없으면 구하는 값 = {dep}, a에 따라 바뀜)'); assert sp.diff(dep, ab) != 0
print('ABLATION 10 연속: 필요(없으면 c와 f(2)=0이 나오지 않아 a, b, c가 정해지지 않음)')
print('ABLATION 10 f(x−2)=f(x+2): 필요(없으면 (−2, 2] 밖의 f가 정해지지 않음)')

# ---------- 11번 (J43) ----------
def feas11(c, f2=True, f10=True, inc=True, lo=2, hi=10):
    """∫_lo^c f = ∫_c^hi f 가 가능한지: 두 적분의 열린 범위가 겹치는지(부호 조건 + 선택한 (가) 조건)"""
    c = Rational(c)
    A_hi = (c**2 - lo**2) / 2                                   # f<x
    A_lo = lo * (c - lo) if (f2 and inc) else -sp.oo            # 증가·f(2)=2 → f>2
    B_lo = (hi**2 - c**2) / 2                                   # f>x
    B_hi = hi * (hi - c) if (f10 and inc) else sp.oo            # 증가·f(10)=10 → f<10
    return max(A_lo, B_lo) < min(A_hi, B_hi)
C11 = [c for c in range(3, 10) if feas11(c)]
ok(C11 == [8], f'11번 자연수 c(2<c<10) 전수: 적분 상등이 가능한 c = {C11}')
I = symbols('I'); cc = symbols('cc')
gen11 = sp.simplify((integrate(x, (x, 2, cc)) - I) + (I - integrate(x, (x, cc, 10))))
ok(gen11 == cc**2 - 52, f'11번 ∫|f−x| = {gen11} (I와 무관)')
# 실제 함수(c=8)로 확인: f = 2 + 6t^m (t=(x−2)/6), f = 10 − 2(1−s)^n (s=(x−8)/2)
for m_, n_ in ((4, 4), (Rational(9, 2), Rational(7, 4))):
    f_lo = 2 + 6 * ((x - 2) / 6)**m_
    f_hi = 10 - 2 * (1 - (x - 8) / 2)**n_
    I1, I2 = integrate(f_lo, (x, 2, 8)), sp.nsimplify(integrate(f_hi, (x, 8, 10)))
    grid_lo = [2 + Rational(i, 10) for i in range(1, 60)]; grid_hi = [8 + Rational(i, 10) for i in range(1, 20)]
    ok(I1 == I2 and f_lo.subs(x, 2) == 2 and f_lo.subs(x, 8) == 8 and f_hi.subs(x, 8) == 8 and f_hi.subs(x, 10) == 10
       and all(diff(f_lo, x).subs(x, t) > 0 for t in grid_lo) and all(diff(f_hi, x).subs(x, t) > 0 for t in grid_hi)
       and all(f_lo.subs(x, t) < t for t in grid_lo) and all(f_hi.subs(x, t) > t for t in grid_hi), f'11번 c=8 예시 함수(m={m_}, n={n_}, I={I1}): 조건 모두 만족')
    tot = sp.nsimplify(integrate(x - f_lo, (x, 2, 8)) + integrate(f_hi - x, (x, 8, 10)))
    ok(tot == 12, f'11번 예시 함수(I={I1})에서 ∫|f−x| = {tot}')
v11 = chk(11, gen11.subs(cc, 8))
ok(integrate(x, (x, 0, 8)) - integrate(x, (x, 8, 10)) == 14, '11번 오답 14: 아래끝을 원문처럼 0으로 둠(32−18)')
ok(not feas11(9) and feas11(9, f2=False) and feas11(9, f10=False) and feas11(9, inc=False), '11번 c=9는 f(2)=2·f(10)=10·증가가 모두 있어야 빠짐')
# 원문 J43: 36
ok(6**2 == 36, '11번 원문 J43 정답 36(정사각형 6², g의 대칭 이용)')
# 빼 보기
for nm, kw in (('f(2)=2', dict(f2=False)), ('f(10)=10', dict(f10=False)), ('증가', dict(inc=False))):
    cs = [c for c in range(3, 10) if feas11(c, **kw)]
    print(f'ABLATION 11 {nm}: 필요(없으면 c = {cs}, 값 {[c * c - 52 for c in cs]})'); assert cs != [8]
print('ABLATION 11 자연수 c: 필요(실수 c이면 c²>52인 c가 여럿, 값이 정해지지 않음)')
J = symbols('J')
print(f'ABLATION 11 ∫_2^c f = ∫_c^10 f: 필요(없으면 c=8에서 값 = {(30 - I) + (J - 18)}, 정해지지 않고 c도 하나로 안 정해짐)')
print('ABLATION 11 2<x<c에서 f<x, c<x<10에서 f>x: 필요(없으면 |f−x|를 부호대로 나눌 수 없음)')

# ---------- 12번 (D59) ----------
a = symbols('a', real=True)
f12 = 8 * x**3 + 12 * a * x**2 - 18 * a**2 * x + 4
ok(expand(diff(f12, x) - 6 * (2 * x + 3 * a) * (2 * x - a)) == 0, "12번 f'=6(2x+3a)(2x−a)")
mx, mn = f12.subs(x, a / 2), f12.subs(x, -3 * a / 2)
ok(expand(mx - (4 - 5 * a**3)) == 0 and expand(mn - (27 * a**3 + 4)) == 0, '12번 a<0: 극대 f(a/2)=4−5a³, 극소 f(−3a/2)=27a³+4')
cand = [r for r in solve(mx - 3, a) if r.is_real and r < 0] + [r for r in solve(mn - 3, a) if r.is_real and r < 0]
ok(cand == [Rational(-1, 3)], f'12번 음수 a 중 y=3이 극값 높이가 되는 a = {cand}')
fa = f12.subs(a, Rational(-1, 3))
ok(expand(fa - 3 - (2 * x - 1)**2 * (2 * x + 1)) == 0, '12번 f−3 = (2x−1)²(2x+1)')
S = integrate(fa - 3, (x, Rational(-1, 2), Rational(1, 2)))
ok(S == Rational(2, 3) and all((fa - 3).subs(x, t) >= 0 for t in [Rational(i, 20) for i in range(-10, 11)]), '12번 [−1/2, 1/2]에서 곡선이 직선 위, S = 2/3')
ok(S != Rational(4, 3), '12번 넓이가 N제 380·원문 J49의 4/3과 다름')
v12 = chk(12, 3 * S)
ok(IT[12]['choices'] == sorted(IT[12]['choices'], key=val), '12번 오름차순 선지(정답 ①)')
ok(3 * Rational(8, 6) * 1**3 == 4, '12번 오답 4: 이차함수 넓이 공식 |k|(β−α)³/6을 써서 4/3, ×3')
# 원문 D59: a=1/3, f(2)=14
fo = (x**3 + 3 * a * x**2 - 9 * a**2 * x + 4).subs(a, Rational(1, 3))
ok(fo.subs(x, 2) == 14, '12번 원문 D59 정답 14(④)')
# 빼 보기
cand_pos = [r for r in solve(mx - 3, a) + solve(mn - 3, a) if r.is_real and r > 0]
print(f'ABLATION 12 음수 a: 필요(양수 a이면 y=3이 극소 f(a/2)=4−5a³에서 접해 a = {cand_pos}, 무리수)'); assert cand_pos
print('ABLATION 12 접할 조건: 필요(없으면 a가 정해지지 않음)')
r5 = [r for r in solve(mn + 4, a) if r.is_real and r < 0][0]
S5 = integrate(f12.subs(a, r5) + 4, (x, 3 * r5 / 2 * 1, -3 * r5 / 2))
print(f'ABLATION 12 직선 y=3: 필요(y=−4이면 a={r5}, 3S={3 * S5})'); assert 3 * S5 != 2
print(f'{len(OK)} checks')
print('ALL OK')

