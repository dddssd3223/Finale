# -*- coding: utf-8 -*-
# 17번 후보 A17 1판 (I46: g(x)=|∫_0^x f|의 극소·극대 자리 ∓a, ∫_{-a}^{3a} f=48, g(a)) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a, c, k, r, m, q, s = sp.symbols('x a c k r m q s', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
V = 48


def typ(F, x0):
    """|F|가 x=x0에서 극대('max')·극소('min')인지 정확한 유리수 계산으로 판정(두 가지 폭으로 확인)."""
    out = []
    for h in (R(1, 2000), R(1, 50000)):
        v0, vl, vr = abs(F.subs(x, x0)), abs(F.subs(x, x0 - h)), abs(F.subs(x, x0 + h))
        out.append('max' if (vl < v0 and vr < v0) else 'min' if (vl > v0 and vr > v0) else None)
    return out[0] if out[0] == out[1] else None


def Fof(f):
    return sp.expand(sp.integrate(f, (x, 0, x)))


# ---------- 1) 갈래 (i): F(-a)≠0 → f(±a)=0 → F는 홀함수 꼴, |F|는 y축 대칭 → x=±a가 같은 종류
Fi = k*(x**3/3 - a**2*x)
assert sp.expand(sp.diff(Fi, x) - k*(x + a)*(x - a)) == 0 and Fi.subs(x, 0) == 0
assert sp.expand(Fi.subs(x, -x) + Fi) == 0
assert sp.simplify(Fi.subs(x, -a) - R(2, 3)*k*a**3) == 0          # F(-a)≠0: '접한다' 갈래(F(-a)=0, f(-a)=0)도 불가능
for av in (1, 2, R(3, 2)):
    for kv in (1, -1, R(5, 3)):
        Fn = Fi.subs({a: av, k: kv})
        assert typ(Fn, av) == 'max' and typ(Fn, -av) == 'max'
print('(i) f(±a)=0이면 F(-x)=-F(x), |F|는 x=±a에서 모두 극대 → (가)에 어긋남')

# ---------- 2) 갈래 (ii): F(-a)=0, F(0)=0 → F=cx(x+a)(x-r), F'(a)=0 → r=5a/3
Fg = c*x*(x + a)*(x - r)
sol_r = sp.solve(sp.Eq(sp.diff(Fg, x).subs(x, a), 0), r)
assert sol_r == [R(5, 3)*a]
FA = c*x*(x + a)*(x - R(5, 3)*a)
assert sp.expand(sp.diff(FA, x) - c/3*(x - a)*(9*x + 5*a)) == 0
for av in (1, 2, R(3, 2), 3):
    for cv in (1, -1, R(3, 8)):
        Fn = FA.subs({a: av, c: cv})
        assert typ(Fn, -av) == 'min' and typ(Fn, av) == 'max'
print('(ii) F(x)=cx(x+a)(x-5a/3): x=-a에서 극소, x=a에서 극대')

# ---------- 3) 전수: a=1로 놓고(가로 방향 확대·축소로 일반성을 잃지 않음) f(x)=p(x^2+qx+s) 전체에서 (가)를 만족시키는 (q, s)
#            |F|의 극값 종류는 p≠0과 무관하므로 p=1. 눈금 1/9, -6≤q, s≤6
hits = []
G9 = [R(j, 9) for j in range(-54, 55)]
def typq(qv, sv, x0):
    """F=x^3/3+qx^2/2+sx에 대한 typ(빠른 계산)."""
    Fv = lambda t: abs(t**3/3 + qv*t**2/2 + sv*t)
    out = []
    for h in (R(1, 2000), R(1, 50000)):
        v0, vl, vr = Fv(x0), Fv(x0 - h), Fv(x0 + h)
        out.append('max' if (vl < v0 and vr < v0) else 'min' if (vl > v0 and vr > v0) else None)
    return out[0] if out[0] == out[1] else None
for qv in G9:
    for sv in G9:
        if typq(qv, sv, R(1)) == 'max' and typq(qv, sv, R(-1)) == 'min':
            hits.append((qv, sv))
assert hits == [(R(-4, 9), R(-5, 9))], hits
assert sp.expand(3*(x**2 - R(4, 9)*x - R(5, 9)) - sp.diff(FA, x).subs({a: 1, c: 1})) == 0
print('전수(a=1, 눈금 1/9): (가)를 만족시키는 f는 f(x)=p(x-1)(9x+5)/9 꼴뿐')

# ---------- 4) (나)와 답
I_na = sp.expand(FA.subs(x, 3*a) - FA.subs(x, -a))
assert sp.simplify(I_na - 16*c*a**3) == 0
assert sp.simplify(sp.integrate(sp.diff(FA, x), (x, -a, 3*a)) - 16*c*a**3) == 0
ca3 = sp.solve(sp.Eq(16*m, V), m)[0]                                # m=ca^3
assert ca3 == 3
val = sp.simplify(sp.Abs(FA.subs(x, a))/sp.Abs(c*a**3))             # |F(a)|/|ca^3|
ANS = sp.nsimplify(R(4, 3)*ca3)
assert sp.simplify(FA.subs(x, a) + R(4, 3)*c*a**3) == 0 and ANS == 4
for av in (1, 2, 3, R(1, 2), 7):                                    # a의 값과 무관
    cv = R(3)/av**3
    Fn = FA.subs({a: av, c: cv})
    assert sp.integrate(sp.diff(Fn, x), (x, -av, 3*av)) == V and abs(Fn.subs(x, av)) == 4
    assert typ(Fn, -av) == 'min' and typ(Fn, av) == 'max'
print('ca^3 = 3, g(a) =', ANS, '(a의 값과 무관)')

# ---------- 5) 선지
ch = IT['choices']; vs = [int(t) for t in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ①, 선지 오름차순 등차', vs[1] - vs[0])

# ---------- 6) 오답 경로
def path(F, scale):
    """F는 scale(=비례상수×a^3)에 대한 식. (나)에서 scale을 정해 |F(a)|를 돌려준다."""
    I = sp.simplify((F.subs(x, 3*a) - F.subs(x, -a)).subs(a, 1))
    sc = sp.solve(sp.Eq(I, V), scale)[0]
    return abs(F.subs({a: 1, scale: sc}).subs(x, 1)), F.subs({a: 1, scale: sc})
w6, FB = path(Fi, k)                                               # 원문 읽기: f(±a)=0
w8, F8 = path(c*x*(x + a)*(x - 2*a), c)                            # 세 번째 영점을 2a로(극대가 두 영점의 한가운데)
w12, F12 = path(c*(x + a)**2*(x - 2*a), c)                         # 접한다고 읽어 F=c(x+a)^2(x-2a), F(0)=0 놓침
assert (w6, w8, w12) == (6, 8, 12)
assert typ(FB, -1) == 'max'                                        # 원문 읽기는 (가)에 어긋남
assert typ(F8, 1) is None and sp.diff(F8, x).subs(x, 1) != 0       # r=2a이면 x=a가 극값의 자리가 아님
assert F12.subs(x, 0) != 0                                         # 아래끝 조건 F(0)=0에 어긋남
assert abs(FB.subs(x, 1) - FB.subs(x, -1)) == 12                   # 원문 읽기에서 두 극값의 차
assert set(IT['wrongs']) == {'6', '8', '12'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 6(원문 읽기), 8(세 번째 영점 2a), 12(접한다고 읽기 / 두 극값의 차)')
assert ANS not in {0, 3, 48} and ANS != 9
print('정답은 본문의 수·원문 답 9와 다름')

# ---------- 7) 원문 I46: 9
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I46']; assert o[2] == '④' and o[1][3] == '9'
fo = k*(4 - x**2)
kv = sp.solve(sp.Eq(sp.integrate(fo, (x, 0, 2)) - sp.integrate(fo, (x, 2, 3)), 23), k)[0]
assert kv == 3 and fo.subs({k: kv, x: 1}) == 9
print('원문 I46 OK: f(x)=3(4-x^2), f(1)=9')
# 원문 원리 줄 불통: 답 함수에서 f(-a)≠0, 정적분 값 조건에 절댓값이 없음
assert sp.simplify(sp.diff(FA, x).subs(x, -a) - R(8, 3)*c*a**2) == 0
print('원문 줄 불통: 답 함수에서 f(-a)=8ca^2/3≠0(극소 자리는 f의 영점이 아님)')

# ---------- 8) 문장 길이(원문의 90% 이상)
pl = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'] + ' ' + ' '.join('(%s) %s' % cc for cc in IT['cond']))); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS

# (가)의 절댓값을 빼면(원문 꼴: F가 -a에서 극소, a에서 극대) f=k(a^2-x^2), k>0 → ∫_{-a}^{3a} f<0
Fo = k*(a**2*x - x**3/3)
Io = sp.simplify(Fo.subs(x, 3*a) - Fo.subs(x, -a))
assert sp.simplify(Io + R(16, 3)*k*a**3) == 0
ablation('(가)의 절댓값(원문 꼴로)', '정적분이 -16ka^3/3<0이라 (나)를 만족시키는 함수가 없음')
# (가)의 극소 조건을 빼면 f(a)=0, F(a)≠0만 남아 값이 정해지지 않음
vals = set()
for mv in (R(-5, 9), -2, 3):
    Fn = Fof((x - 1)*(x - mv)); I = Fn.subs(x, 3) - Fn.subs(x, -1)
    if I != 0 and typ(Fn, 1) == 'max':
        vals.add(abs(Fn.subs(x, 1)*V/I))
assert len(vals) >= 2
ablation('(가)의 극소 조건', f'값이 정해지지 않음: 예 {sorted(vals)}')
# (가)의 극대 조건을 빼면
vals = set()
for rv in (R(5, 3), 4, -3):
    Fn = x*(x + 1)*(x - rv); I = Fn.subs(x, 3) - Fn.subs(x, -1)
    if I != 0:
        vals.add(abs(Fn.subs(x, 1)*V/I))
assert len(vals) >= 2
ablation('(가)의 극대 조건', f'값이 정해지지 않음: 예 {sorted(vals)}')
ablation('(나)', '비례상수가 정해지지 않음: |F(a)|=4|c|a^3/3')
ablation('(나)의 값 48(→24)', R(4, 3)*sp.solve(sp.Eq(16*m, 24), m)[0])
I2 = sp.simplify(FA.subs(x, 2*a) - FA.subs(x, -a))
ablation('(나)의 위끝 3a(→2a)', R(4, 3)*sp.solve(sp.Eq(sp.simplify(I2/(c*a**3))*m, V), m)[0])
# 아래끝 0을 -a로: G(x)=∫_{-a}^x f → G(-a)=0이 저절로 성립, 극소 조건이 일하지 않음
vals = set()
for rv in (R(5, 3), 4, 7):                                          # G=(x+1)(x-t)(x-rv)에서 G'(1)=0이 되도록 t를 맞춘 예
    tv = sp.solve(sp.Eq(sp.diff((x + 1)*(x - m)*(x - rv), x).subs(x, 1), 0), m)[0]
    Gn = (x + 1)*(x - tv)*(x - rv)
    assert typ(Gn, 1) == 'max' and typ(Gn, -1) == 'min'
    I = Gn.subs(x, 3) - Gn.subs(x, -1)
    vals.add(abs(Gn.subs(x, 1)*V/I))
assert len(vals) >= 2
ablation('(가)의 아래끝 0(→ -a)', f'값이 정해지지 않음: 예 {sorted(vals)}')
ablation('이차함수(→ 일차함수)', 'F가 이차함수라 |F|의 극대·극소가 x=±a에 함께 놓일 수 없음(F(0)=0, F′(a)=0이면 F=c(x^2-2ax), F(-a)≠0)')
# 참고(단서·구간 아래끝)
Fneg = FA.subs({a: -2, c: R(3)/(-2)**3})
assert sp.integrate(sp.diff(Fneg, x), (x, 2, -6)) == V and abs(Fneg.subs(x, -2)) == 4 and typ(Fneg, 2) == 'min' and typ(Fneg, -2) == 'max'
print('참고: 단서 양수를 음수로 바꿔도 값은 4(a≠0을 보장하는 단서)')
assert sp.simplify(FA.subs(x, 3*a) - FA.subs(x, 0) - 16*c*a**3) == 0
wB0 = abs(R(2, 3)*sp.solve(sp.Eq(6*m, V), m)[0])
print('참고: (나)의 아래끝 -a를 0으로 바꾸면 답 갈래의 값은 그대로 4, 원문 읽기의 값은', wB0, '(선지 밖)')
print('ALL OK')
