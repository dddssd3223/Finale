# -*- coding: utf-8 -*-
# p3.py (5회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, nsimplify, factor, sqrt, limit, Abs, oo

x, t, k, a, b = symbols('x t k a b', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 2, 10: 4, 11: 1, 12: 5}
DBREF = {9: 'D63 후보_순위 2', 10: 'D26 후보_순위 2', 11: 'D33 v3_추가 1', 12: 'D61 후보_순위 3'}
KEYS = {9: 'D63', 10: 'D26', 11: 'D33', 12: 'D61'}
LEVEL = {9: '중', 10: '중', 11: '중', 12: '중'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == LEVEL[n], f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')

def cv(c):
    return nsimplify(str(c))

def arith(n):
    v = [cv(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    return v

def chk(n, val):
    v = arith(n)
    ok(v[IT[n]['ans'] - 1] == val, f'{n}번 계산 정답 {val} = 선지 {IT[n]["ans"]}번')

# ---------- 9번 (D63) ----------
A_, B_, C_, D_ = symbols('A B C D')
def solve9(curve, P, Q, cubic=True):
    """f=A x^3+B x^2+C x+D, 곡선 y=f 위 원점 접선 = 곡선 y=curve(f) 위 점 (P,Q) 접선 → f 전체(유일성 확인)"""
    f = A_ * x**3 + B_ * x**2 + C_ * x + D_
    g = curve(f)
    m = diff(g, x).subs(x, P)
    eqs = [f.subs(x, 0), g.subs(x, P) - Q, diff(f, x).subs(x, 0) - m, Q - m * P]   # 같은 직선: 기울기·y절편(원점)
    s = solve(eqs, [A_, B_, C_, D_], dict=True)
    return [f.subs(z) for z in s]
# 원문: y=xf(x), (1,2) → f'(2)=-14
s0 = solve9(lambda f: x * f, 1, 2)
ok(len(s0) == 1 and diff(s0[0], x).subs(x, 2) == -14 and expand(s0[0] - (-2 * x**3 + 2 * x**2 + 2 * x)) == 0, '9번 원문 D63 정답 f\'(2)=-14 (선지 ⑤)')
# LIVE1-01-128: y=xf(x)+1 → f'(3)=17
sL = solve9(lambda f: x * f + 1, 1, 2)
ok(len(sL) == 1 and diff(sL[0], x).subs(x, 3) == 17, '9번 뼈대 LIVE1-01-128 정답 f\'(3)=17')
# 변형
s9 = solve9(lambda f: (x - 2) * f - 1, 1, -3)
ok(len(s9) == 1, '9번 연립의 해가 하나(미정계수 유일)')
f9 = s9[0]
ok(expand(f9 - (-2 * x**3 + 7 * x**2 - 3 * x)) == 0 and Poly(f9, x).degree() == 3, f'9번 f(x) = {f9} (삼차)')
g9 = (x - 2) * f9 - 1
ok(f9.subs(x, 1) == 2 and diff(f9, x).subs(x, 1) == 5 and g9.subs(x, 1) == -3 and diff(g9, x).subs(x, 1) == -3 and diff(f9, x).subs(x, 0) == -3, "9번 f(1)=2, f'(1)=5, g(1)=-3, g'(1)=f'(0)=-3")
ok(expand(diff(g9, x).subs(x, 1) * (x - 1) - 3 - diff(f9, x).subs(x, 0) * x) == 0, '9번 두 접선이 모두 y=-3x')
chk(9, f9.subs(x, -1))
# 오답: 상수 -1을 높이에서도 빠뜨림
w9 = solve9(lambda f: (x - 2) * f, 1, -3)
ok(len(w9) == 1 and w9[0].subs(x, -1) == 15 and '15' in IT[9]['wrongs'], f'9번 오답 15 = 상수 -1을 빠뜨린 값 (f={w9[0]})')
# 인수 부호 실수: f(1)-1=-3, f(1)+f'(1)=-3 → 최고차항 0
wsg = solve9(lambda f: x * f - 1 - 2 * 0, 1, -3)   # (x-2) 대신 x로 본 경우와 같은 연립: f(1)=-2, f(1)+f'(1)=-3
ok(len(wsg) == 1 and Poly(wsg[0], x).degree() < 3, f'9번 인수 x-2의 부호를 놓치면 최고차항 0 → 삼차함수가 아님 ({wsg[0]})')
# 빼 보기
print(f'ABLATION 9 상수 -1: 필요(없으면 f(-1)={w9[0].subs(x, -1)})')
E_ = symbols('E')
f4 = E_ * x**4 + A_ * x**3 + B_ * x**2 + C_ * x + D_
g4 = (x - 2) * f4 - 1
m4 = diff(g4, x).subs(x, 1)
s4 = solve([f4.subs(x, 0), g4.subs(x, 1) + 3, diff(f4, x).subs(x, 0) - m4, -3 - m4], [A_, B_, C_, D_], dict=True)
vals4 = {sp.simplify(f4.subs(s4[0]).subs(x, -1).subs(E_, e)) for e in (0, 1, 2)}
print(f'ABLATION 9 삼차함수: 필요(사차까지 허용하면 f(-1)이 {sorted(vals4)} 등으로 정해지지 않음)'); assert len(vals4) > 1

# ---------- 10번 (D26) ----------
def three_pts(fx, level):
    """그래프와 직선 y=level의 교점 x좌표(서로 다른 실근)"""
    return sorted(set(real_roots(Poly(fx - level, x))))
# 원문: 3x^4-4x^3-12x^2+k, x축, abc<0 → f(k/abc)=248
cand0 = []
for kv in range(-100, 101):
    r = three_pts(3 * x**4 - 4 * x**3 - 12 * x**2 + kv, 0)
    if len(r) == 3 and r[0] * r[1] * r[2] < 0: cand0.append((kv, r))
ok(len(cand0) == 1 and cand0[0][0] == 5, f'10번 원문: 조건을 만족시키는 정수 k는 {[c[0] for c in cand0]}')
k0 = 5; abc0 = sp.simplify(cand0[0][1][0] * cand0[0][1][1] * cand0[0][1][2])
fo = 3 * x**4 - 4 * x**3 - 12 * x**2 + k0
ok(abc0 == Rational(-5, 3) and fo.subs(x, k0 / abc0) == 248, '10번 원문 D26 정답 f(k/abc)=f(-3)=248 (선지 ④)')
# 변형: f=3x^4-8x^3-18x^2+k, 직선 y=7
F10 = 3 * x**4 - 8 * x**3 - 18 * x**2
ok(factor(diff(F10, x)) == 12 * x * (x - 3) * (x + 1), "10번 f'(x)=12x(x+1)(x-3)")
ok([F10.subs(x, v) for v in (-1, 0, 3)] == [-7, 0, -135], '10번 극값 k-7, k, k-135')
# 세 점에서만 만나는 k: 접해야 하므로 k ∈ {14, 7, 142}; 전수(극값 7이 아닌 k는 교점 0·2·4개, 접하지 않으면 세 점 불가)
hits3 = []
for kv in (14, 7, 142):
    r = three_pts(F10 + kv, 7)
    hits3.append((kv, len(r), r))
ok([h[1] for h in hits3] == [3, 3, 1], f'10번 k=14, 7은 세 점, k=142는 한 점')
ok(0 in hits3[1][2], '10번 k=7이면 x좌표 0이 있어 abc=0')
r14 = hits3[0][2]; abc = sp.simplify(r14[0] * r14[1] * r14[2])
ok(abc == Rational(-7, 3) and expand(F10 + 14 - 7 - (x + 1)**2 * (3 * x**2 - 14 * x + 7)) == 0, '10번 k=14: f-7=(x+1)²(3x²-14x+7), abc=-7/3')
# 일반 k의 교점 수: 극값 7이 아니면 세 점 불가 (정수·반정수 격자 전수)
grid = [Rational(j, 2) for j in range(-40, 400)]
g3 = [kv for kv in grid if len(three_pts(F10 + kv, 7)) == 3]
ok(g3 == [7, 14], f'10번 k=-20~199.5(간격 1/2) 전수: 세 점에서만 만나는 k는 {g3}')
chk(10, sp.simplify(14 / abc))
wv = 3 * (-1)   # 상수항을 k로 본 지름길
ok(wv == -3 and '-3' in IT[10]['wrongs'], '10번 오답 -3 = 상수항 k-7 대신 k로 쓴 지름길 3r')
# 빼 보기
print('ABLATION 10 abc<0: 필요(없으면 k=7도 세 점, k/abc 정해지지 않음)')
k_x = [kv for kv in range(-50, 200) if (lambda r: len(r) == 3 and r[0] * r[1] * r[2] < 0)(three_pts(F10 + kv, 0))]
ok(k_x == [7], f'x축 기준이면 k={k_x}')
print(f'ABLATION 10 직선 y=7: 필요(x축이면 k=7, k/abc={sp.simplify(7 / (Rational(-7, 3)))})'); assert sp.simplify(7 / Rational(-7, 3)) != -6

# ---------- 11번 (D33) ----------
def npts(c, m, kv):
    pts = set()
    for r in real_roots(Poly(x**2 + c * x - m * x - kv, x)):
        if r >= 0: pts.add(r)
    for r in real_roots(Poly(-x**2 - c * x - m * x - kv, x)):
        if r < 0: pts.add(r)
    return len(pts)
# 원문: |x|(x+1), 기울기 3 → 접선 y=3x-1, y=3x+4 → 거리 √10/2
xs = symbols('xs')
tp = solve(sp.Eq(2 * x + 1, 3), x)[0]; tm = solve(sp.Eq(-2 * x - 1, 3), x)[0]
c1 = (tp**2 + tp) - 3 * tp; c2 = (-tm**2 - tm) - 3 * tm
ok((tp, tm, c1, c2) == (1, -2, -1, 4) and sp.simplify(Abs(c2 - c1) / sqrt(10) - sqrt(10) / 2) == 0, '11번 원문 D33 정답 √10/2 (선지 ⑤)')
# 원문 v3_추가 1 스케치 검산: 0,1,2,3 → 4개
ok([kv for kv in range(-20, 21) if npts(1, 3, kv) == 3] == [0, 1, 2, 3], 'DB v3_추가 1 스케치(원문 수치) 4개 확인')
# 변형: |x|(x+2), y=4x+k
ks = [kv for kv in range(-60, 61) if npts(2, 4, kv) == 3]
ok(ks == list(range(0, 9)), f'11번 세 점에서 만나는 정수 k: {ks}')
ok(npts(2, 4, -1) == 2 and npts(2, 4, 9) == 2 and npts(2, 4, 0) == 3, '11번 경계 k=-1, 9는 두 점(접함), k=0은 세 점(꺾인 점 한 번)')
# 유리수 격자 전수: 세 점인 k는 (-1, 9) 전체
qs = [Rational(j, 4) for j in range(-12, 45)]
ok(all((npts(2, 4, q) == 3) == (-1 < q < 9) for q in qs), '11번 k=-3~11(간격 1/4) 전수: 세 점 ⇔ -1<k<9')
chk(11, len(ks))
ok(len(ks) + 1 == 10 and len(ks) + 2 == 11 and {'10', '11'} == set(IT[11]['wrongs']), '11번 오답 10(경계 하나 포함), 11(경계 둘 포함)')
# 빼 보기
print('ABLATION 11 절댓값: 필요(곡선 y=x(x+2)이면 직선과 많아야 두 점, 개수 0)')
assert all(len(set(real_roots(Poly(x**2 + 2 * x - 4 * x - kv, x)))) <= 2 for kv in range(-20, 21))
print('ABLATION 11 서로 다른: 필요(중복 근까지 세면 k=-1, 9도 세 점 → 11)')

# ---------- 12번 (D61) ----------
def tset(P):
    """조건(좌·우미분계수 곱 ≤ 0)을 만족시키는 t: 정의에 따라 각 후보에서 직접 한쪽 극한을 계산"""
    f = Abs(P)
    cand = set(real_roots(Poly(P, x))) | set(real_roots(Poly(diff(P, x), x)))
    good = set()
    for c in cand:
        hh = symbols('hh', positive=True)
        R = limit((f.subs(x, c + hh) - f.subs(x, c)) / hh, hh, 0)
        L = limit((f.subs(x, c - hh) - f.subs(x, c)) / (-hh), hh, 0)
        if sp.simplify(R * L) <= 0: good.add(c)
    return good, cand
# 후보 밖의 t: P≠0, P'≠0이면 곱 = P'^2 > 0 (미분가능) → 후보만 보면 충분
# 원문
Po = expand((x**4 - 4 * x**3 + 10 * x - 30) - (2 * x + 2))
go, _ = tset(Po)
ok(sp.simplify(sum(go)) == 5 and len(go) == 5, f'12번 원문 D61 정답 합 5 (선지 ④), t {len(go)}개')
# 변형
P12 = expand((x**4 - 5 * x**2 + 10 * x - 30) - (16 * x - 28))
ok(P12 == x**4 - 5 * x**2 - 6 * x - 2 and expand(P12 - (x + 1)**2 * (x**2 - 2 * x - 2)) == 0, '12번 P=t⁴-5t²-6t-2=(t+1)²(t²-2t-2)')
ok(expand(diff(P12, x) - 2 * (x + 1) * (2 * x**2 - 2 * x - 3)) == 0, "12번 P'=2(t+1)(2t²-2t-3)")
g12, c12 = tset(P12)
ok(g12 == c12 and len(c12) == 5, f'12번 후보 5개 모두 조건 만족: {sorted(c12, key=lambda z: float(z))}')
# 격자 점검: 후보 밖 t에서는 곱>0
f12 = Abs(P12)
for tv in [Rational(j, 7) for j in range(-21, 22)]:
    if tv in c12: continue
    ok_ = diff(P12, x).subs(x, tv)**2 > 0 and P12.subs(x, tv) != 0
    assert ok_
ok(True, '12번 t=-3~3(간격 1/7) 후보 밖에서는 곱 {P\'(t)}²>0')
chk(12, len(g12))
# 오답
roots_P = set(real_roots(Poly(P12, x))); roots_dP = set(real_roots(Poly(diff(P12, x), x)))
simple = {r for r in roots_P if diff(P12, x).subs(x, r) != 0}
ok(len(roots_dP) == 3 and '3' in IT[12]['wrongs'], "12번 오답 3 = P'=0인 t만 센 값")
ok(len(simple) == 2 and '2' in IT[12]['wrongs'], '12번 오답 2 = 꺾인 점(단순근)만 센 값')
ok(len(roots_P) + len(roots_dP) == 6, '12번 공통근 -1을 두 번 세면 6(선지 밖)')
# 빼 보기
lt = [c for c in c12 if sp.simplify(P12.subs(x, c)) == 0 and sp.simplify(diff(P12, x).subs(x, c)) != 0]
print(f'ABLATION 12 등호(≤ → <): 필요(<이면 {len(lt)}개)'); assert len(lt) != 5

print(f'{len(OK)}개 확인')
print('ALL OK')
