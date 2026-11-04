# -*- coding: utf-8 -*-
"""c2: 경우 전수 검사, 원문 재계산, 15번 조건별 반례 검증."""
from pathlib import Path
import importlib.util
import itertools
import re
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('codex_c2', HERE / 'c2.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
IT = module.ITEMS
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as source

x, t, a, b, c, m, n, C = s.symbols('x t a b c m n C', real=True)
WANT = {9: ('M48',3), 11: ('D38',5), 13: ('I45',4), 15: ('I59',5)}


def value(text):
    match = re.fullmatch(r'\\[dt]?frac\{?(-?\d+)\}?\{?(\d+)\}?',text)
    return s.Rational(match[1],match[2]) if match else s.sympify(text)


def check(no, got, wrong):
    item = IT[no]
    choices = list(map(value,item['choices']))
    assert (item['key'],item['ans']) == WANT[no]
    assert item['author']=='codex'
    assert len(choices)==len(set(choices))==5
    assert len({choices[j+1]-choices[j] for j in range(4)})==1
    assert s.simplify(got-choices[item['ans']-1])==0
    assert sum(s.simplify(got-v)==0 for v in choices)==1
    listed = re.findall(r'[①②③④⑤] \\\((.*?)\\\)', item['wrong'])
    assert list(map(value,listed))==wrong
    assert all(w in choices and w!=got for w in wrong)
    print(f'{no}: 정답 {got}, 위치 {item["ans"]}, 유일성·등차·오답 {wrong} OK')


def original(key, got):
    _,choices,ans,_ = source.I[key]
    expected = value(choices['①②③④⑤'.index(ans)]) if choices else value(ans)
    assert s.simplify(got-expected)==0, (key,got,expected)
    print(f'ORIGINAL {key}: {got} OK')


assert set(IT)==set(WANT)

# 9: 속력 일치의 모든 실근을 제곱식으로 독립 확인하고 중복 시각을 제거한다.
X1=t**3-6*t**2+9*t
X2=-3*t
v1,v2=s.diff(X1,t),s.diff(X2,t)
same=s.solve(v1-v2,t)
opposite=s.solve(v1+v2,t)
times=sorted(set(same+opposite))
all_roots=s.solve(v1**2-v2**2,t)
assert times==sorted(all_roots)==[2-s.sqrt(2),s.Integer(2),2+s.sqrt(2)]
assert all(r>=0 and s.simplify(s.Abs(v1.subs(t,r))-s.Abs(v2.subs(t,r)))==0 for r in times)
delta=s.factor(X1-X2)
assert s.expand(delta-t*((t-3)**2+3))==0
distances=[s.simplify(s.Abs(delta.subs(t,r))) for r in times]
assert all(d>0 for d in distances)
wrong_same=sum(s.Abs(delta.subs(t,r)) for r in same)
wrong_opposite=s.simplify(sum(s.Abs(delta.subs(t,r)) for r in opposite))
check(9,s.simplify(sum(distances)),[wrong_same,wrong_opposite,wrong_same*2+wrong_opposite])
orig_delta=(t**3-2*t**2+3*t)-(t**2+12*t)
orig_times=[r for r in s.solve(s.diff(orig_delta,t),t) if r>=0]
assert orig_times==[3]
original('M48',s.Abs(orig_delta.subs(t,orig_times[0])))

# 11: 순서쌍 16개를 전수 검사한다. 삼차함수의 도함수가 부호를 바꾸는 점을 찾는다.
def local_maxima(poly):
    return [(r,s.simplify(poly.subs(x,r)))
            for r in s.solve(s.diff(poly,x),x)
            if r.is_real and s.diff(poly,x,2).subs(x,r)<0]


valid=[]
stationary_zero=[]
for aa,bb in itertools.product(range(4),repeat=2):
    poly=(x-aa)*(x-bb)*(x-3)
    extrema=local_maxima(poly)
    if any(v==0 for _,v in extrema): valid.append((aa,bb))
    if any(poly.subs(x,r)==0 for r in s.solve(s.diff(poly,x),x)):
        stationary_zero.append((aa,bb))
assert valid==[(0,0),(1,1),(2,2)]
# f'=0, f=0만으로 극대임을 보장할 수 없으므로 삼중 인수인 경우를 제외한다.
diag=[(i,i) for i in range(4)]
assert all(pair in stationary_zero for pair in diag)
assert local_maxima((x-3)**3)==[]
check(11,s.Integer(len(valid)),[s.Integer(len(diag))])
orig_max=[]
for aa,bb in itertools.product(range(3),repeat=2):
    orig_max += [v for _,v in local_maxima((x-aa)*(x-bb)*(x-2))]
largest=max(orig_max)
assert largest==s.Rational(32,27)
p,q=s.fraction(largest)
original('D38',p+q)

# 13: 극한의 존재로 n=0. g의 자유로운 상수항 c가 답에 영향을 주지 않음을 확인한다.
f=m*x+n
limexpr=s.expand(s.integrate(f,(x,0,x))/x**2)
assert limexpr==m/2+n/x
f=5*x
g=x**3+a*x**2+b*x+c
eq1=s.integrate(f*g,(x,-1,1))
eq2=s.integrate(f*s.diff(g,x),(x,-1,1))-20
sol=s.solve([eq1,eq2],(a,b),dict=True)
assert sol==[{a:3,b:-s.Rational(3,5)}]
target=s.simplify(f.subs(x,s.diff(g,x).subs(x,1)).subs(sol[0]))
assert target==42 and c not in target.free_symbols
bad_m=s.Rational(5,2)
badsol=s.solve([s.integrate(bad_m*x*g,(x,-1,1)),
                s.integrate(bad_m*x*s.diff(g,x),(x,-1,1))-20],(a,b),dict=True)
assert len(badsol)==1
bad_target=s.simplify(bad_m*s.diff(g,x).subs(x,1).subs(badsol[0]))
bad_drop_high=s.Integer(5)*(3+2*sol[0][a])
check(13,target,[bad_target,bad_drop_high])
fo=m*x; go=x**2+b*x+c
so=s.solve([s.integrate(fo*go,(x,-1,1)),s.integrate(fo*s.diff(go,x),(x,-1,1))-8],(m,b),dict=True)
assert so==[{b:0,m:6}]
original('I45',(m*s.diff(go,x).subs(x,1)).subs(so[0]))

# 15: 차수를 미리 가정하지 않고 곱의 차수로 모든 후보를 좁힌다.
P=5*x**4+4*x**3+3*x**2+12*x
# (가) ⇒ f의 짝수차 부분=3x², F의 홀수차 부분=x³, deg F>=3.
# (나) ⇒ deg(FG)=5. F(0)≠0과 f(0)=0에서 g(0)=0.
# g=0이면 P=0으로 모순이므로 deg G>=2. 가능한 차수 쌍은 (3,2)뿐이다.
degree_pairs=[(df,dg) for df in range(3,6) for dg in range(2,6) if df+dg==5]
assert degree_pairs==[(3,2)]
F=x**3+a*x**2+C
G=b*x**2+c
equations=s.Poly(s.diff(F*G,x)-P,x).all_coeffs()
sol=s.solve(equations,(a,b,c,C),dict=True)
assert sol==[{C:5,a:1,b:1,c:1}]
F0,G0=s.expand(F.subs(sol[0])),s.expand(G.subs(sol[0]))


def conditions(ff,gg):
    # ff,gg는 부정적분 F,G. 미분과 정적분을 실제로 계산한다.
    return [s.expand(s.integrate(s.diff(ff,x),(x,-x,x))-2*x**3)==0,
            s.expand(s.diff(ff*gg,x)-P)==0,
            ff.subs(x,0)!=0]


def target15(ff,gg):
    return s.simplify(ff.subs(x,1)+gg.subs(x,1))


assert conditions(F0,G0)==[True,True,True]
target=target15(F0,G0)
# (다)를 지운 이차·삼차 후보의 모든 실수해도 인수분해로 확인한다.
h=s.symbols('h',real=True)
candidate_b=1-h
candidate_c=h**2-h+1
candidate_C=6-h*candidate_c
last=s.factor(candidate_C*candidate_b)
assert s.expand(last-(h-1)*(h-2)*(h**2+h+3))==0
assert s.discriminant(h**2+h+3,h)<0
alternatives=[]
for hv in [1,2]:
    ff=(x**3+h*x**2+candidate_C).subs(h,hv)
    gg=(x**2+candidate_b*x+candidate_c).subs(h,hv)
    assert conditions(ff,gg)[:2]==[True,True]
    alternatives.append((ff,gg))
assert [target15(ff,gg) for ff,gg in alternatives]==[9,6]
check(15,target,[target15(*alternatives[1]),F0.subs(x,1),F0.subs(x,1)+1])

# 조건을 하나씩 지우고 나머지를 만족시키는 구체적 반례로 답이 달라짐을 보인다.
counterexamples=[(2*F0,G0/2), (x**3+5,s.Integer(1)), alternatives[1]]
for removed,(ff,gg) in enumerate(counterexamples):
    checks=conditions(ff,gg)
    assert not checks[removed]
    assert all(ok for j,ok in enumerate(checks) if j!=removed)
    changed=target15(ff,gg)
    assert changed!=target
    print(f'ABLATION 15 {"가나다"[removed]}: 필요(F={ff}, G={gg}, 답 {changed} ≠ {target})')

# I59 원문: 하한 대입+미분으로 f, 다항식 계수 비교로 F,G를 유일 결정.
fo=4*x-1
assert s.expand(s.integrate(fo,(x,1,x))-(x*fo-2*x**2-1))==0
Fo=2*x**2-x+C
Go=a*x**2+b*x+c
so=s.solve(s.Poly(s.diff(Fo*Go,x)-(8*x**3+3*x**2+1),x).all_coeffs(),(a,b,c,C),dict=True)
assert so==[{C:1,a:1,b:1,c:0}]
Go=Go.subs(so[0])
original('I59',Go.subs(x,3)-Go.subs(x,1))

print('ALL OK')
