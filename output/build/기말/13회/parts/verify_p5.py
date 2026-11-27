# -*- coding: utf-8 -*-
# 17번 후보 A17 3판 (M32: 두 영점이 a, a-18인 삼차함수, 방정식 f(x)-xf'(k)=0의 실근이 2개인 k의 개수) 검증 · author='claude'
import sympy as sp, os, sys, re
x, k, t, a, p, m = sp.symbols('x k t a p m', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def nk(f, line=x):
    """방정식 f(x)-line*f'(k)=0의 서로 다른 실근이 정확히 2개인 실수 k의 개수(정확 계산).
    실근 2개 ⇔ x에 대한 판별식이 0이고 세 근이 모두 같지는 않음(도함수의 판별식도 0이면 세 근이 같음)."""
    h = sp.expand(f - sp.diff(f, x).subs(x, k)*line)
    P = sp.Poly(sp.discriminant(h, x), k)
    T = sp.Poly(sp.discriminant(sp.diff(h, x), x), k)
    g = sp.gcd(P, T)
    roots = set(sp.real_roots(P, multiple=True))
    bad = set(sp.real_roots(g, multiple=True)) if g.degree() > 0 else set()
    return len(roots - bad)


def brute(f, kv):
    """직접 세기: k=kv일 때 서로 다른 실근의 개수."""
    h = sp.Poly(sp.expand(f - sp.diff(f, x).subs(x, kv)*x), x)
    return len(set(sp.real_roots(h, multiple=True)))


F = lambda av, gap=18: sp.expand((x - av)*(x - av + gap)**2)

# ---------- 1) (가), (나)에서 f(x) 결정
# (가): (x-a)f(x)≥0 ⇔ f의 부호가 x=a에서만 음→양 ⇔ f=(x-a)(x-p)^2 (p≠a이면 p에서 부호 불변, p=a이면 (x-a)^3). (나) f(a-18)=0 → p=a-18
fp = (x - a)*(x - p)**2
assert sp.solve(sp.Eq(fp.subs(x, a - 18), 0), p) == [a - 18]
fa = (x - a)*(x - a + 18)**2
assert sp.expand((x - a)*fa - (x - a)**2*(x - a + 18)**2) == 0                 # (가) 성립
mir = (x - a)**2*(x - a + 18)                                             # 거꾸로 둔 식은 (가)에 어긋남
assert ((x - a)*mir).subs({a: 0, x: -10}) < 0
print('f(x)=(x-a)(x-a+18)^2 (거꾸로 둔 (x-a)^2(x-a+18)은 (가)에 어긋남)')
assert sp.expand(sp.diff(fa, x) - 3*(x - a + 6)*(x - a + 18)) == 0

# ---------- 2) 접하는 점의 방정식과 판별식
G = sp.factor(sp.expand(fa.subs(x, t) - t*sp.diff(fa, x).subs(x, t)))
q = 2*t**2 - a*t - a*(a - 18)
assert sp.expand(G + (t - a + 18)*q) == 0
D = sp.factor(sp.discriminant(q, t)); assert sp.expand(D - 9*a*(a - 16)) == 0
assert sp.expand(q.subs(t, a - 18) + 36*(a - 18)) == 0                    # t=a-18이 ㉠의 근 ⇔ a=18
assert sp.expand(q.subs(t, a - 6)) == 72                                  # ㉠의 근에서 f'≠0
assert sp.expand(q.subs(t, a - 12) - (288 - 18*a)) == 0                   # 세 근이 같아지는 것은 a=16뿐
assert set(sp.solve(q.subs(a, 18), t)) == {0, 9}
f0, f16 = F(0), F(16)
assert sp.expand(f0 - 324*x - x**2*(x + 36)) == 0 and sp.diff(f0, x).subs(x, 0) == 324
assert sp.expand(f16 + 108*x - (x - 4)**3) == 0 and sp.diff(f16, x).subs(x, 4) == -108
print('접하는 점: (t-a+18){2t^2-at-a(a-18)}=0, D=9a(a-16) · a=0: x^2(x+36) · a=16: (x-4)^3')

# ---------- 3) 전수: k의 개수가 2 ⇔ 0<a≤16
ints = list(range(-60, 81))
grid = sorted(set(ints + [R(n, 8) for n in range(-24, 170)]))
tab = {av: nk(F(av)) for av in grid}
assert all((tab[av] == 2) == (0 < av <= 16) for av in grid)
assert tab[0] == 4 and tab[18] == 4 and tab[16] == 2 and tab[17] == 6 and tab[-1] == 6
assert set(tab.values()) == {2, 4, 6}
print('k의 개수: 0<a≤16 → 2, a=0·18 → 4, 그 밖 → 6 (정수 -60~80, 눈금 1/8로 -3~21)')
# 범위 밖(|a|가 큰 쪽)은 식으로: D>0이면 ㉠의 근 중 a-18이 아닌 t가 있고 f'(t)≠0, 세 근이 같지 않아 k가 3개 이상(위 2)의 세 항등식)
# 직접 세기로 다시 확인: 조건에 맞는 k는 a-18, a-6 (0<a≤16)
for av in [1, 5, R(7, 2), 12, 16]:
    assert brute(F(av), av - 18) == 2 and brute(F(av), av - 6) == 2
    assert all(brute(F(av), av - 18 + R(j, 4)) != 2 for j in range(-40, 120) if j not in (0, 48))
assert brute(F(16), 4) == 1 and brute(F(0), 0) == 2 and brute(F(18), 9) == 2 and brute(F(-2), 4) == 2 and brute(F(-2), -5) == 2
good = [av for av in ints if tab[av] == 2]
ANS = len(good)
assert good == list(range(1, 17)) and ANS == 16
print('조건을 만족시키는 정수 a: 1~16 →', ANS, '개')

# ---------- 4) 선지
ch = IT['choices']; vs = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ②, 선지 오름차순 등차', vs[1] - vs[0])

# ---------- 5) 오답
cnt = lambda c: len([n for n in ints if c(n)])
w15 = cnt(lambda n: D.subs(a, n) < 0)                       # 판별식 음수만(a=16 제외)
w17a = cnt(lambda n: D.subs(a, n) <= 0)                     # 판별식 0 이하 모두(a=0 포함)
w17b = cnt(lambda n: 0 < n < 18)                            # 어림: 원점이 두 영점 사이
w18 = cnt(lambda n: 0 < n <= 18)                            # 어림 + 원문 상황 a=18
w19 = cnt(lambda n: 0 <= n <= 18)
assert (w15, w17a, w17b, w18, w19) == (15, 17, 17, 18, 19)
assert set(IT['wrongs']) == {'15', '17', '18'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 15(D<0만), 17(D≤0 또는 0<a<18), 18(0<a≤18), 19(0≤a≤18)')
assert ANS not in {1, 18, 2} and ANS != 19
print('정답은 본문의 수·원문 답 19와 다름')

# ---------- 6) 원문 M32: 19
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['M32']; assert o[2] == '19'
fo = x**2*(x - 4)
ks = sorted(set(sp.solve(sp.diff(fo, x) - 0, x) + sp.solve(sp.diff(fo, x) + 4, x)))
assert all(brute(fo, kv) == 2 for kv in ks) and nk(fo) == 4
S = sum(ks); assert S == R(16, 3) and S.p + S.q == 19
print('원문 M32 OK: k=0, 2/3, 2, 8/3, 합 16/3, p+q=19')
# 원문 원리 줄 불통: 조건에 맞는 a에서는 f(0)≠0(x로 묶이지 않음), k는 네 개가 아니라 두 개
assert all(F(av).subs(x, 0) != 0 and tab[av] == 2 for av in good)
print('원문 줄 불통: 0<a≤16에서 f(0)≠0, k의 개수 2(원문 방식의 결론은 4)')

# ---------- 7) 문장 길이(원문의 90% 이상)
pl = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'] + ' ' + ' '.join('(%s) %s' % c for c in IT['cond']))); org_len = len(pl(o[0]))      # 원문 HTML처럼 상자 라벨 포함
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS

# (가)를 빼면 f가 정해지지 않는다: 예 f=(x-a+18)^3도 (나)를 만족시키고 이때 a≠18인 모든 a에서 k가 2개
assert all(nk(sp.expand((x - av + 18)**3)) == 2 for av in [-30, -5, 3, 17, 40])
ablation('(가)', 'f가 정해지지 않음: f=(x-a+18)^3이면 a≠18인 모든 정수 a가 조건에 맞아 개수가 정해지지 않음')
# (나)를 빼면 f=(x-a)(x-p)^2에서 p가 자유
c9 = len([n for n in ints if nk(F(n, 9)) == 2])
ablation('(나)', f'f가 정해지지 않음: 예 f(a-9)=0이면 {c9}개')
ablation('영점 사이의 거리 18(→9)', c9)
c27 = len([n for n in ints if nk(F(n, 27)) == 2])
ablation('영점 사이의 거리 18(→27)', c27)
# 방정식의 x를 (x-a)로: 직선이 부호가 바뀌는 영점을 지나 k는 늘 4개
cxa = len([n for n in range(-20, 41) if nk(F(n), x - n) == 2])
ablation("방정식의 x(→x-a)", cxa)
# k의 개수 2 → 4
c4 = len([n for n in ints if tab[n] == 4])
ablation('(다) k의 개수 2(→4)', c4)
c6 = len([n for n in range(1, 21) if tab[n] == 6])
ablation('(다) k의 개수 2(→6, 20 이하의 자연수)', c6)
# (다)를 빼면 a에 조건이 없음
ablation('(다) 전체', '정수 a에 조건이 없어 개수가 정해지지 않음')
# 최고차항의 계수 1 → 2: f=2(x-a)(x-a+18)^2, 접하는 직선의 구성은 같으나 식이 달라지는지 확인(개수는 같아 계수는 f를 정하는 데만 쓰임)
c2 = len([n for n in range(-30, 51) if nk(2*F(n)) == 2])
print('참고: 최고차항의 계수 1 → 2이면', c2, '개(f를 하나로 정하는 조건, 원문 단서 그대로)')
print('ALL OK')
