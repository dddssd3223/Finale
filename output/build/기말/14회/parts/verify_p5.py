# -*- coding: utf-8 -*-
# 17번 후보 A17 1판 수정 (I46: g(x)=|∫_0^x f|의 극소·극대 자리 ∓3, ∫_{-3}^{9} f=48, g(3)) 검증 · author='claude'
import sympy as sp, os, sys, re, random
x, c, k, r, m = sp.symbols('x c k r m', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
V, P, LO, HI = 48, 3, -3, 9          # (나)의 값, 극대 자리, 구간 끝


def typ(F, x0):
    """|F|가 x=x0에서 극대('max')·극소('min')인지 정확한 유리수 계산으로 판정(두 가지 폭으로 확인)."""
    out = []
    for h in (R(1, 2000), R(1, 50000)):
        v0, vl, vr = abs(F.subs(x, x0)), abs(F.subs(x, x0 - h)), abs(F.subs(x, x0 + h))
        out.append('max' if (vl < v0 and vr < v0) else 'min' if (vl > v0 and vr > v0) else None)
    return out[0] if out[0] == out[1] else None


Fof = lambda f: sp.expand(sp.integrate(f, (x, 0, x)))

# ---------- 1) 갈래 (i): F(-3)≠0 → f(±3)=0 → F(-x)=-F(x), g는 y축 대칭
Fi = k*(x**3/3 - 9*x)
assert sp.expand(sp.diff(Fi, x) - k*(x + 3)*(x - 3)) == 0 and Fi.subs(x, 0) == 0
assert sp.expand(Fi.subs(x, -x) + Fi) == 0
assert Fi.subs(x, -3) == 18*k                                     # F(-3)≠0: '접한다' 갈래(F(-3)=0, f(-3)=0)도 불가능
for kv in (1, -1, R(5, 3)):
    assert typ(Fi.subs(k, kv), 3) == 'max' and typ(Fi.subs(k, kv), -3) == 'max'
print('(i) f(±3)=0이면 F(-x)=-F(x), g는 x=±3에서 모두 극대 → (가)에 어긋남')

# ---------- 2) 갈래 (ii): F(-3)=0, F(0)=0 → F=cx(x+3)(x-r), F'(3)=0 → r=5
Fg = c*x*(x + 3)*(x - r)
assert sp.solve(sp.Eq(sp.diff(Fg, x).subs(x, 3), 0), r) == [5]
FA = c*x*(x + 3)*(x - 5)
assert sp.expand(sp.diff(FA, x) - c*(x - 3)*(3*x + 5)) == 0
for cv in (1, -1, R(1, 9)):
    assert typ(FA.subs(c, cv), -3) == 'min' and typ(FA.subs(c, cv), 3) == 'max'
print('(ii) F(x)=cx(x+3)(x-5): x=-3에서 극소, x=3에서 극대')

# ---------- 3) 전수: f(x)=p(x^2+qx+s) 전체에서 (가)를 만족시키는 (q, s). g의 극값 종류는 p≠0과 무관하므로 p=1. 눈금 1/3, -12≤q, s≤12
def typq(qv, sv, x0):
    Fv = lambda t: abs(t**3/3 + qv*t**2/2 + sv*t)
    out = []
    for h in (R(1, 2000), R(1, 50000)):
        v0, vl, vr = Fv(x0), Fv(x0 - h), Fv(x0 + h)
        out.append('max' if (vl < v0 and vr < v0) else 'min' if (vl > v0 and vr > v0) else None)
    return out[0] if out[0] == out[1] else None
G3 = [R(j, 3) for j in range(-36, 37)]
hits = [(qv, sv) for qv in G3 for sv in G3 if typq(qv, sv, R(3)) == 'max' and typq(qv, sv, R(-3)) == 'min']
assert hits == [(R(-4, 3), R(-5))], hits
assert sp.expand(3*(x**2 - R(4, 3)*x - 5) - sp.diff(FA, x).subs(c, 1)) == 0
print('전수(눈금 1/3): (가)를 만족시키는 f는 f(x)=p(x-3)(3x+5) 꼴뿐')

# ---------- 4) (나)와 답
assert sp.expand(FA.subs(x, HI) - FA.subs(x, LO) - 432*c) == 0
assert sp.integrate(sp.diff(FA, x), (x, LO, HI)) == 432*c
cv = sp.solve(sp.Eq(432*c, V), c)[0]; assert cv == R(1, 9)
Fans = FA.subs(c, cv)
ANS = abs(Fans.subs(x, P)); assert ANS == 4
assert typ(Fans, -3) == 'min' and typ(Fans, 3) == 'max' and sp.integrate(sp.diff(Fans, x), (x, LO, HI)) == V
print('c = 1/9, g(3) =', ANS)

# ---------- 5) 선지
ch = IT['choices']; vs = [int(t) for t in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ①, 선지 오름차순 등차', vs[1] - vs[0])

# ---------- 6) 오답 경로
def path(F, sc):
    v = sp.solve(sp.Eq(F.subs(x, HI) - F.subs(x, LO), V), sc)[0]
    return abs(F.subs(sc, v).subs(x, P)), F.subs(sc, v)
w6, FB = path(Fi, k)                                   # 원문 읽기: f(±3)=0
w8, F8 = path(c*x*(x + 3)*(x - 6), c)                  # 세 번째 영점을 6으로(극대가 두 영점의 한가운데)
w12, F12 = path(c*(x + 3)**2*(x - 6), c)               # 접한다고 읽어 F=c(x+3)^2(x-6), F(0)=0 놓침
assert (w6, w8, w12) == (6, 8, 12)
assert typ(FB, -3) == 'max'
assert typ(F8, 3) is None and sp.diff(F8, x).subs(x, 3) != 0
assert F12.subs(x, 0) != 0
assert abs(FB.subs(x, 3) - FB.subs(x, -3)) == 12
assert set(IT['wrongs']) == {'6', '8', '12'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 6(원문 읽기), 8(세 번째 영점 6), 12(접한다고 읽기 / 두 극값의 차)')
assert ANS not in {0, 3, 9, 48}
print('정답은 본문의 수·원문 답 9와 다름')

# ---------- 7) 원문 I46: 9
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['I46']; assert o[2] == '④' and o[1][3] == '9'
fo = k*(4 - x**2)
kv = sp.solve(sp.Eq(sp.integrate(fo, (x, 0, 2)) - sp.integrate(fo, (x, 2, 3)), 23), k)[0]
assert kv == 3 and fo.subs({k: kv, x: 1}) == 9
print('원문 I46 OK: f(x)=3(4-x^2), f(1)=9')
assert sp.diff(FA, x).subs(x, -3) == 24*c
print('원문 줄 불통: 답 함수에서 f(-3)=24c≠0(극소 자리는 f의 영점이 아님)')

# ---------- 8) 문장 길이(원문의 90% 이상)
pl = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'] + ' ' + ' '.join('(%s) %s' % cc for cc in IT['cond']))); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS

Fo = k*(9*x - x**3/3)                                   # 원문 꼴: F가 -3에서 극소, 3에서 극대 → k>0
assert sp.expand(Fo.subs(x, HI) - Fo.subs(x, LO) + 144*k) == 0
ablation('(가)의 절댓값(원문 꼴로)', '정적분이 -144k<0이라 (나)를 만족시키는 함수가 없음')
vals = set()
for mv in (R(-5, 3), -6, 9):                            # f=(x-3)(x-m): 극대 조건만
    Fn = Fof((x - 3)*(x - mv)); I = Fn.subs(x, HI) - Fn.subs(x, LO)
    if I != 0 and typ(Fn, 3) == 'max':
        vals.add(abs(Fn.subs(x, 3)*V/I))
assert len(vals) >= 2
ablation('(가)의 극소 조건', f'값이 정해지지 않음: 예 {sorted(vals)}')
vals = set()
for rv in (5, 12, -9):                                  # F=x(x+3)(x-r): 극소 조건만
    Fn = x*(x + 3)*(x - rv); I = Fn.subs(x, HI) - Fn.subs(x, LO)
    if I != 0:
        vals.add(abs(Fn.subs(x, 3)*V/I))
assert len(vals) >= 2
ablation('(가)의 극대 조건', f'값이 정해지지 않음: 예 {sorted(vals)}')
ablation('(나)', '비례상수가 정해지지 않음: g(3)=36|c|')
ablation('(나)의 값 48(→24)', abs(FA.subs(x, 3)).subs(c, R(24, 432)))
c6 = sp.solve(sp.Eq(FA.subs(x, 6) - FA.subs(x, LO), V), c)[0]
ablation('(나)의 위끝 9(→6)', abs(FA.subs(c, c6).subs(x, 3)))
vals = set()
for rv in (5, 12, 21):                                  # 아래끝 -3: G=(x+3)(x-t)(x-rv), G'(3)=0이 되도록 t를 맞춘 예
    tv = sp.solve(sp.Eq(sp.diff((x + 3)*(x - m)*(x - rv), x).subs(x, 3), 0), m)[0]
    Gn = (x + 3)*(x - tv)*(x - rv)
    assert typ(Gn, 3) == 'max' and typ(Gn, -3) == 'min'
    vals.add(abs(Gn.subs(x, 3)*V/(Gn.subs(x, HI) - Gn.subs(x, LO))))
assert len(vals) >= 2
ablation('(가)의 아래끝 0(→ -3)', f'값이 정해지지 않음: 예 {sorted(vals)}')
ablation('이차함수(→ 일차함수)', 'F(0)=0, F′(3)=0이면 F=c(x^2-6x)이고 F(-3)≠0, f(-3)≠0이라 x=-3에서 극값이 없음')
assert FA.subs(x, 0) == 0
wB0 = abs(Fi.subs(x, 3)).subs(k, sp.solve(sp.Eq(Fi.subs(x, HI), V), k)[0])
print('참고: (나)의 아래끝 -3을 0으로 바꾸면 답 갈래의 값은 그대로 4, 원문 읽기의 값은', wB0, '(선지 밖)')
print('ALL OK')
