# -*- coding: utf-8 -*-
# p3.py (9회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, Poly, expand, solve, integrate, diff, Abs

x, t, al = symbols('x t alpha', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 4, 10: 3, 11: 2, 12: 5}          # 분담표 9⑤·12④를 맞바꿈(회차 분포 그대로)
DBREF = {9: 'I72 후보_순위 2', 10: 'I31 후보_순위 2', 11: 'I47 예상밖 1', 12: 'I58 후보_순위 2'}
KEYS = {9: 'I72', 10: 'I31', 11: 'I47', 12: 'I58'}
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
    ok('이러한' not in it['body'] and '이와 같은' not in it['body'], f'{n}번 금지 어구 없음')
    ok(not any(('<' in m or '>' in m) for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'], re.S)), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if 'OP49' in IT[n]['ops']) == 0, '결합(OP49) 없음 — 장치는 같은 원문 DB에서')

def chk(n, v0):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    return v

# ---------- 9번 (I72) ----------
A = symbols('a', real=True)
def f9(a, c):
    """x<0 조각 계수 c: g(x) = -c∫_0^x f (x<0), ∫_0^x f (x≥0), g = x²(x−a) → f = -g'/c (x<0), g' (x≥0)"""
    gp = x * (3 * x - 2 * a)
    return (-gp / c, gp)
# g가 삼차이고 f 연속 → f(0)=0, g'(0)=0 을 일반 삼차로 확인
p0, p1, p2 = symbols('p0 p1 p2', real=True)
gg = x**3 + p2 * x**2 + p1 * x + p0
sol0 = solve([gg.subs(x, 0), -diff(gg, x).subs(x, 0) / 2 - diff(gg, x).subs(x, 0)], [p0, p1], dict=True)
ok(sol0 == [{p0: 0, p1: 0}], '9번 g(0)=0, −g′(0)/2=g′(0) → g=x³+p₂x² = x²(x−a)')
def roots_abs(a, c, k=3):
    L, R = f9(a, c)
    rs = set()
    for r in solve(sp.Eq(L, k * x), x) + solve(sp.Eq(L, -k * x), x):
        if r.is_real and r < 0: rs.add(r)
    for r in solve(sp.Eq(R, k * x), x) + solve(sp.Eq(R, -k * x), x):
        if r.is_real and r >= 0: rs.add(r)
    return sorted(rs)
a9 = solve(f9(A, 2)[1].subs(x, 1) + 1, A)
ok(a9 == [2], '9번 f(1)=3−2a=−1 → a=2 (유일)')
R9 = roots_abs(2, 2)
ok(R9 == [Rational(-2, 3), 0, Rational(1, 3), Rational(7, 3)], f'9번 |f(x)|=|3x|의 서로 다른 실근 {R9}')
# 수치로도 전수(부호 변화 + 0): |f|−|3x|의 근을 촘촘한 격자에서 확인
Lf, Rf = f9(2, 2)
Fn = sp.lambdify(x, sp.Piecewise((Abs(Lf) - Abs(3 * x), x < 0), (Abs(Rf) - Abs(3 * x), True)))
grid = [i / 3000 for i in range(-30000, 30001)]
sgn = 0; cross = 0
for u in grid:
    v_ = Fn(u)
    if abs(v_) < 1e-12: continue
    s = 1 if v_ > 0 else -1
    if sgn and s != sgn: cross += 1
    sgn = s
ok(cross == 4, f'9번 수치 확인: |f|−|3x|의 부호 변화 {cross}개(−2/3, 0, 1/3, 7/3, 모두 부호가 바뀌는 근) (−10..10)')
v9 = chk(9, len(R9))
W1 = roots_abs(2, 1)
ok(len(W1) == 3 and val('3') in [val(w) for w in IT[9]['wrongs']], f'9번 오답 3: 계수 2를 놓치면(원문 꼴) 근 {W1}')
ok(Rational(10, 3) > 0 and len(R9) + 1 == 5, '9번 오답 5: x<0 조각의 x=10/3을 범위 확인 없이 더함')
# 원문 I72: ㄱ 참, ㄴ 거짓(a=0 반례), ㄷ 참 → ④(ㄱ, ㄷ)
L0, R0 = f9(0, 1)
crit0 = [r for r in solve(diff(L0, x), x) if r < 0] + [r for r in solve(diff(R0, x), x) if r > 0]
ok(crit0 == [] and all(sp.diff(R0, x).subs(x, u) >= 0 for u in (Rational(1, 10), 1)) and all(sp.diff(L0, x).subs(x, u) >= 0 for u in (Rational(-1, 10), -1)), '9번 원문 ㄴ: a=0이면 f=3x|x| 증가, 극댓값 없음(거짓)')
cnt = set()
for aa in [Rational(i, 20) for i in range(-9, 10)]:     # 2<f(1)<4 ⇔ −1/2<a<1/2
    Lo, Ro = f9(aa, 1)
    rs = {r for r in solve(Lo - x, x) if r.is_real and r < 0} | {r for r in solve(Ro - x, x) if r.is_real and r >= 0}
    cnt.add(len(rs))
ok(cnt == {3}, '9번 원문 ㄷ: −1/2<a<1/2 격자에서 f(x)=x의 실근 항상 3개(참) → 원문 정답 ④(ㄱ, ㄷ)')
# 빼 보기
for fv in (1, 3):
    aa = solve(f9(A, 2)[1].subs(x, 1) - fv, A)[0]
    print(f'ABLATION 9 f(1)=−1: 필요(f(1)={fv}이면 a={aa}, 근 {len(roots_abs(aa, 2))}개)'); assert len(roots_abs(aa, 2)) != 4
print(f'ABLATION 9 x<0 조각의 계수 −2: 필요(−1이면 근 {len(W1)}개)')
print(f'ABLATION 9 |3x|의 계수 3: 필요(|f(x)|=|x|이면 근 {len(roots_abs(2, 2, 1))}개)'); assert len(roots_abs(2, 2, 1)) != 4

# ---------- 10번 (I31) ----------
b, p, d, q = symbols('b p d q', real=True)
f10 = x**4 + b * x**3 + p * x**2 + d * x + q
cond = expand(integrate(diff(f10, x), (x, -2 * al, -al)) + integrate(diff(f10, x), (x, al, 2 * al)))
co = Poly(cond, al).coeffs()
s10 = solve(co, [b, d], dict=True)
ok(s10 == [{b: 0, d: 0}], f'10번 등식 ⇔ {cond}=0 (모든 α) ⇔ b=d=0 (우함수)')
fe = f10.subs({b: 0, d: 0})
s10b = solve([diff(fe, x).subs(x, 1), fe.subs(x, 1) - 2], [p, q], dict=True)
ok(s10b == [{p: -2, q: 3}], '10번 f′(1)=0, f(1)=2 → p=−2, q=3 (유일)')
F10 = fe.subs(s10b[0])
ok(F10.subs(x, 1) == 2 and diff(F10, x).subs(x, 1) == 0 and diff(F10, x, 2).subs(x, 1) != 0, '10번 x=1에서 극값 2(극소, f″(1)=8)')
v10 = chk(10, F10.subs(x, 2))
ok((x**2 - 1)**2 == (x**2 - 1)**2 and ((x**2 - 1)**2).subs(x, 2) == 9, '10번 오답 9: 원문 극값 0의 f=(x²−1)²에서 f(2)=9')
ok((x**4 - 2 * x**2 + 2).subs(x, 2) == 10, '10번 오답 10: q=2(f(0)=2로 착각)에서 f(2)=10')
# 반대 순서(∫_α^{2α} = ∫_{−2α}^{−α})로 쓰면 사차함수가 없음을 확인(쓰지 않은 꼴)
bad = expand(integrate(diff(f10, x), (x, al, 2 * al)) - integrate(diff(f10, x), (x, -2 * al, -al)))
ok(solve(Poly(bad, al).coeffs(), [b, p, d], dict=True) == [], '10번 (확인) 합 대신 같다로 쓰면 짝수차가 상수여야 해 사차함수 없음 → 합=0 꼴 채택')
# 원문 I31: 30∫_{−1}^{1} f = 32
fo = (x**2 - 1)**2
ok(30 * integrate(fo, (x, -1, 1)) == 32, '10번 원문 I31 정답 32')
ok(15 * integrate(F10, (x, -1, 1)) == 76, '10번 (note) 학교식_예상 1의 묻는 값 15∫ = 76')
# 빼 보기
fr = f10.subs({})
free = solve([diff(f10, x).subs(x, 1), f10.subs(x, 1) - 2], [p, q], dict=True)[0]
vals = {expand(f10.subs(free).subs(x, 2).subs({b: bb, d: dd})) for bb, dd in [(0, 0), (1, 0), (0, 1), (1, 1)]}
print(f'ABLATION 10 적분 등식: 필요(없으면 b, d가 남아 f(2) 값이 {sorted(vals)} 등으로 정해지지 않음)'); assert len(vals) > 1
print(f'ABLATION 10 x=1에서 극값 2: 필요(없으면 p, q가 남음)')
print(f'ABLATION 10 극값 2(값): 필요(극값 0이면 f(2)=9)')

# ---------- 11번 (I47) ----------
c4, c3, c2, c1, c0 = symbols('c4 c3 c2 c1 c0', real=True)
def solve11(f0, wrong=False):
    """f = 4x³+βx²+γx+f0(삼차, g 사차 최고차 1) 일반 꼴. 등식과 ∫_{−a}^{a}xg=0 전부를 계수로 풀기"""
    be, ga, f3 = symbols('be ga f3', real=True)
    sols = []
    for deg in (3,):
        f = f3 * x**3 + be * x**2 + ga * x + f0
        if wrong:
            g = f + integrate(f.subs(x, t), (t, 0, x))            # ∫(x−t)f′ 을 ∫f 로 바꾼 오답
        else:
            g = expand(f + integrate((x - t) * diff(f, x).subs(x, t), (t, 0, x)))
        aa = symbols('aa', real=True)
        I = expand(integrate(x * g, (x, -aa, aa)))
        eqs = Poly(I, aa).coeffs() + [Poly(g, x).coeff_monomial(x**4) - 1]
        for s in solve(eqs, [f3, be, ga], dict=True):
            sols.append((expand(f.subs(s)), expand(g.subs(s))))
    return sols
S11 = solve11(2)
ok(len(S11) == 1 and S11[0] == (4 * x**3 - 12 * x**2 + 2, x**4 - 12 * x**2 + 2), f'11번 f(0)=2: (f, g) = {S11} (유일)')
# 차수: f의 최고차항 k·xⁿ이면 g의 최고차항은 k·xⁿ⁺¹/(n+1) → g가 최고차 1인 사차이면 n=3, k=4
for n_ in range(1, 7):
    kk = symbols('kk', nonzero=True)
    lead = expand(integrate((x - t) * diff(kk * x**n_, x).subs(x, t), (t, 0, x)))
    ok(lead == kk * x**(n_ + 1) / (n_ + 1), f'11번 f가 {n_}차이면 g는 {n_ + 1}차')
fS, gS = S11[0]
ok(expand(diff(gS, x) - (diff(fS, x) + fS - 2)) == 0, "11번 g′ = f′ + f − f(0)")
v11 = chk(11, fS.subs(x, -1) + gS.subs(x, -1))
SW = solve11(2, wrong=True)
ok(len(SW) == 1 and SW[0][0].subs(x, -1) + SW[0][1].subs(x, -1) == -22, f'11번 오답 −22: ∫(x−t)f′=∫f로 바꾸면 {SW}')
S0 = solve11(0)
ok(S0[0][0].subs(x, 1) + S0[0][1].subs(x, 1) == -19, '11번 원문 I47 정답 −19 (f(0)=0, f(1)+g(1))')
ok(S0[0][0].subs(x, -1) + S0[0][1].subs(x, -1) == -27 and -27 not in [val(c) for c in IT[11]['choices']], '11번 (note) f(0)=0이면 −27(선지 밖)')
ok(fS.subs(x, 1) + gS.subs(x, 1) == -15, '11번 (note) f(1)+g(1)=−15')
# 빼 보기
print(f'ABLATION 11 f(0)=2: 필요(f(0)=0이면 −27, f(0)=1이면 {solve11(1)[0][0].subs(x, -1) + solve11(1)[0][1].subs(x, -1)})')
assert solve11(1)[0][0].subs(x, -1) + solve11(1)[0][1].subs(x, -1) != -23
be, ga, f3 = symbols('be ga f3', real=True)
fN = 4 * x**3 + be * x**2 + ga * x + 2
gN = expand(fN + integrate((x - t) * diff(fN, x).subs(x, t), (t, 0, x)))
vN = {expand(fN.subs(x, -1) + gN.subs(x, -1)).subs({be: bb, ga: cc}) for bb, cc in [(-12, 0), (0, 0), (1, 2)]}
print(f'ABLATION 11 ∫xg=0: 필요(없으면 β, γ가 남아 값이 {sorted(vN)} 등)'); assert len(vN) > 1

# ---------- 12번 (I58) ----------
C = symbols('C', real=True)
H = -2 * x + C                      # G − 3F (G′ − 3F′ = 3f − 2 − 3f = −2)
c12 = solve(integrate(H.subs(x, 2 * x + 1), (x, 0, 1)), C)
ok(c12 == [4], '12번 ∫_0^1 H(2x+1)dx = C−4 = 0 → C=4 (유일)')
# 구체 f 여러 개로 G, F를 직접 만들어 확인
for fx in (x**2, 3 * x**3 - x + 5, sp.Integer(7)):
    F = integrate(fx, x) + 11
    G0 = integrate(3 * fx - 2, x)
    k = symbols('k')
    G = G0 + k
    ks = solve(integrate(G.subs(x, 2 * x + 1), (x, 0, 1)) - 3 * integrate(F.subs(x, 2 * x + 1), (x, 0, 1)), k)
    ok(len(ks) == 1 and expand((G - 3 * F).subs(k, ks[0]).subs(x, 4)) == -4, f'12번 f={fx}로 직접: G(4)−3F(4)=−4')
v12 = chk(12, H.subs(C, 4).subs(x, 4))
cw = solve(integrate(H, (x, 0, 1)), C)[0]
ok(H.subs(C, cw).subs(x, 4) == -7, '12번 오답 −7: 인자 2x+1을 무시(∫_0^1 H=0 → C=1)')
ok(H.subs(C, solve(H.subs(x, 1), C)[0]).subs(x, 4) == -6, '12번 오답 −6: G(1)=3F(1)로 봄(C=2, 학교식_예상 1의 답)')
# 원문 I58: G(5)−2F(5)=2
Ho = x + C
ok(Ho.subs(C, solve(Ho.subs(x, 3), C)[0]).subs(x, 5) == 2, '12번 원문 I58 정답 2(②)')
# 빼 보기
print(f'ABLATION 12 정적분 조건: 필요(없으면 C가 정해지지 않음)')
print(f'ABLATION 12 인자 2x+1: 필요(x이면 C=1, 답 −7)')
H2 = -x + C   # 3F 대신 같은 계수가 아니면 f가 남는지: G가 3f−2의 부정적분, 2F와 비교하면 f가 소거되지 않음
print("ABLATION 12 3f와 3F의 계수 일치: 필요(3F 대신 2F이면 G−2F의 도함수가 f−2로 f가 남아 값이 정해지지 않음)")
fx1, fx2 = x, x**2
vals12 = set()
for fx in (fx1, fx2):
    F = integrate(fx, x); k = symbols('k'); G = integrate(3 * fx - 2, x) + k
    ks = solve(integrate(G.subs(x, 2 * x + 1), (x, 0, 1)) - 2 * integrate(F.subs(x, 2 * x + 1), (x, 0, 1)), k)
    vals12.add(expand((G - 2 * F).subs(k, ks[0]).subs(x, 4)))
assert len(vals12) > 1

print(f'{len(OK)} checks')
print('ALL OK')
