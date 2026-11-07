# -*- coding: utf-8 -*-
# 2회 p2 (Claude 10·12·14·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os
import sympy as sp

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {10: 5, 12: 4, 14: 5, 16: 1}
x, t, s, u = sp.symbols('x t s u', real=True)
a, b, k, p = sp.symbols('a b k p')
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def ch(no):
    return [sp.Rational(c) for c in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1 and list(d)[0] > 0, f'선지 {v} 서로 다르고 오름차순 등차(공차 {d})')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    check(no, IT[no].get('author') == 'claude', "author='claude'")
    for f_ in ('vtype', 'effect', 'bunseok', 'precedent', 'wrongs'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [sp.Rational(z) for z in IT[no]['wrongs']]
    check(no, all(sp.nsimplify(z) in v and sp.nsimplify(z) != v[IT[no]['ans'] - 1] for z in vals) and sorted(w) == sorted(set(sp.nsimplify(z) for z in vals)),
          f'오답 {vals} 선지에 있음, wrongs {IT[no]["wrongs"]}와 같음 ({why})')


def ablation(no, cname, vals, ans, why='', undef=None):
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = '필요(남은 조건을 만족시키는 경우가 없음)'
    else:
        sv = sorted(set(vals), key=lambda v: float(v))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:4]))}{" 등" if len(sv) > 4 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')


def sign_changes(P, var):
    P = sp.Poly(sp.expand(P), var)
    rs = P.real_roots()
    return [r for r in sorted(set(rs), key=lambda z: float(z)) if rs.count(r) % 2 == 1]


def gen_poly(deg, name='c'):
    cs = sp.symbols(f'{name}0:{deg + 1}')
    return sum(cs[i] * x**i for i in range(deg + 1)), cs


def ident_solve(expr, cs):
    eqs = sp.Poly(sp.expand(expr), x).all_coeffs()
    return sp.solve(eqs, cs, dict=True)


# ================= 원문 직접 풀이 =================
# I60: (가) ∫_1^x f = (x-1)/2 {f(x)+f(1)}, (나) ∫_0^2 f = 5∫_{-1}^1 x f, f(0)=1 → f(4)=7
P, cs = gen_poly(6)
S = ident_solve(sp.integrate(P.subs(x, t), (t, 1, x)) - (x - 1) / 2 * (P + P.subs(x, 1)), cs)
P1 = P.subs(S[0])
fr = [c for c in cs if P1.has(c)]
S2 = sp.solve([sp.integrate(P1, (x, 0, 2)) - 5 * sp.integrate(x * P1, (x, -1, 1)), P1.subs(x, 0) - 1], fr, dict=True)
check('I60', len(S) == 1 and sp.Poly(P1, x).degree() == 1 and len(S2) == 1 and P1.subs(S2[0]).subs(x, 4) == 7, f'I60 원문: f={sp.expand(P1.subs(S2[0]))}, f(4)=7')

# M35: f=x^3/7-x^2, [t,t+3], 0<=t<=5, g 최댓값+최솟값 = 4 (④)
def gfun(f, tv, L):
    cands = [tv, tv + L] + [r for r in sp.solve(sp.diff(f, x), x) if r.is_real and tv < r < tv + L]
    return max(f.subs(x, c) for c in cands)
fM = x**3 / 7 - x**2
gs = [gfun(fM, sp.Rational(i, 20), 3) for i in range(0, 101)]
check('M35', max(gs) + min(gs) == 4 and min(gs) == gfun(fM, 3, 3), f'M35 원문: g 최솟값 {min(gs)} (t=3), 최댓값 {max(gs)}, 합 {max(gs) + min(gs)}')

# I24: f' = q(x-1)(x-2) (q>0), ∫_0^3|f'| = f(3)-f(0)+4 → f(2)-f(1) = -2 (①)
q = sp.symbols('q', positive=True)
fp24 = q * (x - 1) * (x - 2)
absI = sp.integrate(fp24, (x, 0, 1)) - sp.integrate(fp24, (x, 1, 2)) + sp.integrate(fp24, (x, 2, 3))
qs = sp.solve(sp.Eq(absI, sp.integrate(fp24, (x, 0, 3)) + 4), q)
check('I24', len(qs) == 1 and sp.integrate(fp24.subs(q, qs[0]), (x, 1, 2)) == -2, f'I24 원문: 계수 {qs}, f(2)-f(1)=-2')

# I61: f=(x+1)(x-1)(x-a), a>1, g'=2xF, 극값 하나 ⇔ F(a)>=0 ⇔ a<=√6
F61 = sp.integrate(((t + 1) * (t - 1) * (t - a)), (t, 0, x))
Fa = sp.factor(F61.subs(x, a))
amax = [r for r in sp.solve(Fa, a) if r.is_real and r > 1]
cnt = lambda av: len(sign_changes(2 * x * F61.subs(a, av), x))
check('I61', amax == [sp.sqrt(6)] and cnt(sp.Rational(24, 10)) == 1 and cnt(sp.Rational(25, 10)) == 3 and sp.simplify(F61.subs(a, sp.sqrt(6)).subs(x, sp.sqrt(6))) == 0,
      f'I61 원문: F(a)={Fa}, 경계 a={amax}(F(√6)=f(√6)=0 이중근, 등호 포함), a=2.4 극값 1개, a=2.5 극값 3개')

def bmap(no):
    it = IT[no]; bm = it.get('bunseok_map') or {}
    full = all(bm.get(f_) for f_ in ('tip', 'direction', 'traps', 'calc')) and bm['direction'].startswith('방향 ')
    marks = ['①②③④⑤'[it['choices'].index(w)] for w in it['wrongs']]
    check(no, it['bunseok'] is True and full and all(any(m in tr for tr in bm['traps']) for m in marks),
          f'bunseok_map 4요소(tip·direction·traps·calc), 함정이 선지 {marks}로 잡힘')


# ================= 10번 =================
P, cs = gen_poly(6)
S = ident_solve(sp.integrate(P.subs(x, t), (t, 1, x)) - (x - 1) / 4 * (P + 3 * P.subs(x, 1)), cs)
P10 = sp.expand(P.subs(S[0]))
fr = [c for c in cs if P10.has(c)]
A_, B_ = sp.symbols('A_ B_')
form = sp.solve(sp.Poly(sp.expand(P10 - (A_ * (x - 1)**3 + B_)), x).all_coeffs(), fr + [A_], dict=True)
check(10, len(S) == 1 and len(fr) == 2 and sp.Poly(P10, x).degree() == 3 and form != [],
      f'(가)를 6차 이하 일반 다항식으로 풀면 f={sp.factor(P10)} 꼴 = a(x-1)^3+b (자유 계수 2개)')
# 최고차항 비교(미분 없이): a x^n → 좌변 a/(n+1), 우변 a/4 → n=3
check(10, [n_ for n_ in range(1, 10) if sp.Rational(1, n_ + 1) == sp.Rational(1, 4)] == [3], '최고차항 비교 a/(n+1)=a/4 → n=3')
S10 = sp.solve([sp.integrate(P10, (x, 0, 2)) - 5 * sp.integrate(x * P10, (x, -1, 1)), P10.subs(x, -1) + 1], fr, dict=True)
f10 = sp.expand(P10.subs(S10[0]))
check(10, len(S10) == 1 and sp.expand(f10 - ((x - 1)**3 / 2 + 3)) == 0, f'(나)·f(-1)=-1 → f={f10} = (x-1)^3/2+3 (유일)')
check(10, sp.simplify(sp.integrate(f10.subs(x, t), (t, 1, x)) - (x - 1) / 4 * (f10 + 3 * f10.subs(x, 1))) == 0, '(가) 항등식 성립 확인')
# 계산 정리: ∫_0^2 f = 2f(1)=2b (점대칭), ∫_{-1}^1 xf = a∫(x^4+3x^2) (홀수차 소거), f(3)+f(-1)=2b
fg = A_ * (x - 1)**3 + B_
check(10, sp.simplify(sp.integrate(fg, (x, 0, 2)) - 2 * B_) == 0 and sp.simplify(sp.integrate(x * fg, (x, -1, 1)) - A_ * sp.integrate(x**4 + 3 * x**2, (x, -1, 1))) == 0
      and sp.integrate(x**4 + 3 * x**2, (x, -1, 1)) == sp.Rational(12, 5) and sp.simplify(fg.subs(x, 3) + fg.subs(x, -1) - 2 * B_) == 0,
      '계산 정리: ∫_0^2 f=2b, ∫_{-1}^1 xf=a·12/5, f(3)+f(-1)=2b')
ans10 = f10.subs(x, 3)
ans_ok(10, ans10)
# 오답 ①: 이차로 착각 f=A(x-1)^2+B → 직선 x=1 대칭으로 f(3)=f(-1)
Aq, Bq = sp.symbols('Aq Bq')
fq = Aq * (x - 1)**2 + Bq
sq = sp.solve([sp.integrate(fq, (x, 0, 2)) - 5 * sp.integrate(x * fq, (x, -1, 1)), fq.subs(x, -1) + 1], [Aq, Bq], dict=True)
w10a = fq.subs(sq[0]).subs(x, 3)
# 오답 ②: 점 (1,b) 대칭을 원점 대칭처럼 써서 ∫_{-1}^1 xf = 0 → 2b=0
sz = sp.solve([sp.integrate(fg, (x, 0, 2)) - 0, fg.subs(x, -1) + 1], [A_, B_], dict=True)
w10b = fg.subs(sz[0]).subs(x, 3)
# 선지 밖 오답(참고): 대칭구간 2배 누락 ∫_0^1 a(x^4+3x^2)
s2 = sp.solve([sp.integrate(fg, (x, 0, 2)) - 5 * A_ * sp.integrate(x**4 + 3 * x**2, (x, 0, 1)), fg.subs(x, -1) + 1], [A_, B_], dict=True)
check(10, w10a == -1 and w10b == 1 and fg.subs(s2[0]).subs(x, 3) not in ch(10), f'이차 착각 {w10a}, ∫xf=0 소거 {w10b}, (2배 누락 {fg.subs(s2[0]).subs(x, 3)}는 선지 밖)')
wrong_in(10, [w10a, w10b], '이차 착각 / 홀수항 소거 범위')
bmap(10)
print('--- 10번 조건 빼 보기 ---')
P, cs = gen_poly(4)
Sn = sp.solve([sp.integrate(P, (x, 0, 2)) - 5 * sp.integrate(x * P, (x, -1, 1)), P.subs(x, -1) + 1], cs[:2], dict=True)
vals = [sp.expand(P.subs(Sn[0])).subs(x, 3).subs({cs[2]: c2, cs[3]: c3, cs[4]: 0}) for c2, c3 in [(0, 0), (1, 0), (0, 1)]]
ablation(10, '(가)', vals, 7)
vals = [fg.subs(x, 3).subs({A_: av, B_: 8 * av - 1}) for av in [0, 1, 2]]
ablation(10, '(나)', vals, 7)
vals = [fg.subs(x, 3).subs({A_: av, B_: 6 * av}) for av in [1, 2, 3]]
ablation(10, 'f(-1)=-1', vals, 7)

# ================= 12번 =================
f12 = x**3 - 5 * x**2 - 8 * x
check(12, sp.factor(f12 + 12) == sp.factor((x + 2) * (x - 1) * (x - 6)) and f12.subs(x, 1) == -12, f'f(x)+12 = {sp.factor(f12 + 12)} (정수 x=1 대입)')
check(12, sp.factor(sp.diff(f12, x)) == sp.factor((3 * x + 2) * (x - 4)), "f'=(3x+2)(x-4): 극대 -2/3(음수), 극소 4 → x≥0에서 감소 후 증가")
check(12, sp.expand(f12.subs(x, t + 5) - f12.subs(x, t) - 5 * (t - 1) * (3 * t + 8)) == 0, "a=5: f(t+5)-f(t)=5(t-1)(3t+8) → t=1에서 교차")
g12 = [gfun(f12, sp.Rational(i, 40), 5) for i in range(0, 81)]
check(12, min(g12) == -12 and gfun(f12, 1, 5) == -12, f'a=5: g 최솟값 {min(g12)} (t=1)')
# 유일성: a 격자 전수 (교차점 t 포함)
hit = []
for av in [sp.Rational(i, 8) for i in range(1, 81)]:
    ts = [sp.Rational(i, 10) for i in range(0, 21)] + [r for r in sp.solve(f12.subs(x, t + av) - f12.subs(x, t), t) if r.is_real and 0 <= r <= 2]
    gm = min((gfun(f12, tv, av) for tv in ts), key=lambda z: float(z))
    if abs(float(gm) + 12) < 1e-9:
        hit.append(av)
check(12, hit == [5], f'a∈(0,10] (1/8 간격) 전수: g 최솟값이 -12인 a = {hit}')
ans12 = sp.Integer(6 - 1)
ans_ok(12, ans12)
# 오답 ②: 극대점 -2/3을 사이에 둔 -2, 1을 끝점으로 (실제 a=3이면 g 최솟값은 -12가 아님)
# 오답 ③: 극소점 4를 구간의 가운데로 보아 2(6-4)
check(12, min(gfun(f12, sp.Rational(i, 40), 3) for i in range(0, 81)) != -12 and min(gfun(f12, sp.Rational(i, 40), 4) for i in range(0, 81)) != -12,
      'a=3, a=4이면 g 최솟값이 -12가 아님(오답 확인)')
wrong_in(12, [1 - (-2), 2 * (6 - 4)], '-2, 1을 끝점 / 극소점을 구간의 가운데로')
bmap(12)
print('--- 12번 조건 빼 보기 ---')
vals = []
for m in [-28, -20, -12]:   # 최솟값을 바꾸면 a가 바뀜
    rs = sorted([r for r in sp.solve(f12 - m, x) if r.is_real and r >= 0], key=float)
    vals.append(sp.nsimplify(rs[-1] - rs[0]) if len(rs) >= 2 else None)
ablation(12, "'g(t)의 최솟값이 -12'", [v_ for v_ in vals if v_ is not None], 5)
ablation(12, "'0<=t<=2'", [], 5, undef='t의 범위가 없으면 g(t)는 아래로 무한히 작아져 최솟값이 없음')

# ================= 14번 =================
pp = sp.symbols('pp', positive=True); kk = sp.symbols('kk', positive=True)
fp14 = pp * x * (x - 2)
F14 = sp.integrate(fp14, x)
A14 = -sp.integrate(fp14, (x, 0, 2))
B14 = sp.integrate(fp14, (x, 2, kk))
C14 = sp.integrate(fp14, (x, -1, 0))
absI = C14 + A14 + B14           # kk>2
signed = F14.subs(x, kk) - F14.subs(x, -1)
sol14 = sp.solve([sp.Eq(A14, B14), sp.Eq(A14, 4)], [pp, kk], dict=True)
sol14 = [d for d in sol14 if d[kk] > 2]
check(14, len(sol14) == 1 and sol14[0] == {pp: 3, kk: 3}, f'A=B=4 → {sol14} (유일)')
fpn = fp14.subs(sol14[0])
ans14 = sp.integrate(sp.Abs(fpn), (x, -1, 3))
check(14, ans14 == 12 and sp.integrate(fpn, (x, -1, 3)) + 8 == 12, f'∫_{{-1}}^3 |3x(x-2)| dx = {ans14}')
check(14, A14.subs(pp, 3) == 4 and B14.subs({pp: 3, kk: 3}) == 4, '그림 수치: A=4, B=4 (본문에 0, 2, k>2만 있으면 풀림)')
ans_ok(14, ans14)
wrong_in(14, [sp.integrate(fpn, (x, -1, 3)), sp.integrate(sp.Abs(fpn), (x, 0, 3))], '절댓값 무시 / x<0 부분 빼먹음')
print('--- 14번 조건 빼 보기 ---')
vals = []
for kv in [sp.Rational(5, 2), 3, 4]:
    pv = sp.solve(sp.Eq(absI.subs(kk, kv), signed.subs(kk, kv) + 8), pp)[0]
    vals.append(sp.integrate(sp.Abs(fp14.subs(pp, pv)), (x, -1, kv)))
ablation(14, 'A=B', vals, 12)
vals = [sp.integrate(sp.Abs(fp14.subs(pp, pv)), (x, -1, 3)) for pv in [1, 2, 3]]
ablation(14, 'A=4', vals, 12)

# ================= 16번 =================
F16 = sp.integrate((t + a) * (t - a) * (t - 6), (t, 0, x))
def nextr(av):
    return len(sign_changes(2 * x * F16.subs(a, av), x))
check(16, sp.simplify(sp.diff(x**2 * F16 - sp.integrate(t**2 * (t + a) * (t - a) * (t - 6), (t, 0, x)), x) - 2 * x * F16) == 0, "g'(x)=2xF(x)")
cnts = {av: nextr(av) for av in range(1, 41)}
good = [av for av, c in cnts.items() if c == 1]
check(16, good == list(range(3, 17)), f'a=1..40 전수: 극값 1개인 a = {good}')
check(16, all(c in (1, 3) for c in cnts.values()) and all(nextr(av) == 3 for av in range(17, 61)), 'a>16이면 모두 극값 3개 (a≤60까지 확인; F(a)=a^3(16-a)/4<0)')
check(16, sp.factor(F16.subs(x, 6)) == sp.factor(18 * a**2 - 108) and sp.factor(F16.subs(x, a) - a**3 * (16 - a) / 4) == 0,
      f'F(6)={sp.expand(F16.subs(x, 6))}, F(a)={sp.factor(F16.subs(x, a))}')
check(16, nextr(16) == 1 and nextr(6) == 1 and nextr(2) == 3, '경계 a=16(이중근)·a=6(f 중근)은 극값 1개, a=2는 3개')
ans16 = len(good)
ans_ok(16, ans16)
# 오답: a<6에서 원문처럼 x=a에서 판정 (F(a)>0이라 모두 됨) → a=1..16
Fa16 = F16.subs(x, a)
w16a = len([av for av in range(1, 17) if (av < 6 and Fa16.subs(a, av) > 0) or av == 6 or (av > 6 and Fa16.subs(a, av) >= 0)])
# 오답: a^2>=6에서 √6≈2.4를 내려 a=2부터
w16b = len([av for av in range(int(sp.floor(sp.sqrt(6))), 17)])
check(16, w16a == 16 and w16b == 15, f'원문 방식 판정 {w16a}개, √6 내림 {w16b}개')
wrong_in(16, [w16b, w16a], '√6 내림 / 안쪽에서도 움직이는 근에서 판정')
print('--- 16번 조건 빼 보기 ---')
ablation(16, "'자연수 a'", [], 14, undef='실수 a이면 √6≤a≤16 무수히 많음')
ablation(16, "'오직 하나의 극값'", [], 14, undef='조건이 없으면 모든 자연수 a, 개수가 정해지지 않음')

print('ALL OK' if ok else 'SOME FAIL')
