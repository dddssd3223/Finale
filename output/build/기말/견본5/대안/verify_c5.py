# -*- coding: utf-8 -*-
"""D62 변형: 두 절댓값 항의 미분계수 상쇄, 답과 조건의 필요성을 검사한다."""
from pathlib import Path
import html
import re
import runpy
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'부교재_기말'))
import items_final as original
it=runpy.run_path(str(HERE/'c5.py'))['SITEMS']['S2']
x,a,b,m,n=s.symbols('x a b m n',real=True)
R=s.Rational

def smooth(f,g):
    """절댓값의 모든 경계에서 실제 좌우 식의 함수값과 미분계수를 비교."""
    cuts=sorted(set(s.real_roots(f,x))|{s.S.Zero})
    for i,c in enumerate(cuts):
        left=(cuts[i-1]+c)/2 if i else c-1
        right=(c+cuts[i+1])/2 if i+1<len(cuts) else c+1
        lp=s.sign(f.subs(x,left))*f+g*s.sign(left)*x
        rp=s.sign(f.subs(x,right))*f+g*s.sign(right)*x
        hvalue=abs(f.subs(x,c))+g.subs(x,c)*abs(c)
        if s.simplify(lp.subs(x,c)-hvalue)!=0 or s.simplify(rp.subs(x,c)-hvalue)!=0:
            return False
        if s.simplify(s.diff(lp-rp,x).subs(x,c))!=0:
            return False
    return True

# f(0) != 0이면 |f|는 0에서 매끄럽다. g(0)=0이 필요하지만
# g(1)=0과 합치면 g는 영함수이므로 '일차함수'와 모순이다.
g=m*x+n
assert s.solve([g.subs(x,0),g.subs(x,1)],(m,n))=={m:0,n:0}
# 따라서 f(0)=0. 극솟값 0인 점 a가 0이면 f=x²(x-b).
# b!=0은 b에서 상쇄되지 않는 꺾임, b=0은 극값 없는 x³이므로 제외.
f0=x*x*(x-b)
assert s.diff(f0,x).subs(x,b)==b*b
assert s.diff(x**3,x)==3*x*x

# a!=0이므로 차수 비교로 f=x(x-a)². f″(a)=2a이므로 a>0.
f=x*(x-a)**2
assert s.diff(f,x,2).subs(x,a)==2*a
possible=s.solve(f.subs(x,1)-4,a)
assert set(possible)=={-1,3}
accepted=[]
for av in possible:
    fv=s.expand(f.subs(a,av))
    # h의 0에서 좌우 미분계수는 -(a²+n), +(a²+n).
    gv=s.expand((a*a*(x-1)).subs(a,av))
    assert gv.subs(x,1)==0 and smooth(fv,gv)
    if av>0:
        accepted.append((fv,gv))
    print(f'FAMILY a={av}: f″(a)={2*av}, g(0)={gv.subs(x,0)}, 극솟값0 조건={av>0}')
assert len(accepted)==1
fstar,gstar=accepted[0]
assert s.expand(fstar-x*(x-3)**2)==0 and gstar==9*x-9
crit=s.solve(s.diff(fstar,x),x); mins=[c for c in crit if s.diff(fstar,x,2).subs(x,c)>0]
answers=[mins[0],gstar.subs(x,0),abs(fstar.subs(x,2))+2*gstar.subs(x,2)]
assert answers==[3,-9,20]
assert it['ans']==['(1) 3','(2) -9','(3) 20']
assert [q[1] for q in it['subs']]==['4점, 답만 적으시오.','4점, 답만 적으시오.','2점, 답만 적으시오.']
# 모든 실수에서 h=x|x|(x+3). 특히 0의 좌우미분계수는 모두 0.
hp=x*x*(x+3)
hm=-hp
assert s.diff(hp,x).subs(x,0)==s.diff(hm,x).subs(x,0)==0
assert smooth(fstar,gstar)
assert s.diff(fstar,x).subs(x,0)==9  # 각 항은 따로 미분가능하지 않음
assert (-gstar.subs(x,0),gstar.subs(x,0))==(9,-9)
assert [fstar.subs(x,1),-gstar.subs(x,0),-1,fstar.subs(x,2),abs(fstar.subs(x,2))+2*gstar.subs(x,2)]==[4,9,-1,2,20]
print('ANSWERS (1) 0, (2) -9, (3) 11; 유일성·배점·오답 계산 OK')

def zero_minimum(p):
    """영점에서의 극소뿐 아니라 다른 극솟값의 유무도 확인한다."""
    cps=sorted(set(s.real_roots(s.diff(p,x),x)))
    mins=[]
    for i,c in enumerate(cps):
        left=(cps[i-1]+c)/2 if i else c-1
        right=(c+cps[i+1])/2 if i+1<len(cps) else c+1
        if s.diff(p,x).subs(x,left)<0<s.diff(p,x).subs(x,right):
            mins.append(s.simplify(p.subs(x,c)))
    return bool(mins) and all(v==0 for v in mins)

def ablation(label,fv,gv,omitted):
    checks={
        '삼차함수':s.degree(fv,x)==3,
        '최고차항':s.LC(s.Poly(fv,x))==1,
        '일차함수':s.degree(gv,x)==1,
        '미분가능':smooth(fv,gv),
        '극솟값0':zero_minimum(fv),
        'f(1)=4':fv.subs(x,1)==4,
        'g(1)=0':gv.subs(x,1)==0,
    }
    assert all(v for k,v in checks.items() if k!=omitted),(label,checks)
    assert not checks[omitted]
    cr=[c for c in s.solve(s.diff(fv,x),x) if c.is_real and s.diff(fv,x,2).subs(x,c)>0]
    vals=[sorted(cr) if len(cr)!=1 else cr[0],gv.subs(x,0),abs(fv.subs(x,2))+2*gv.subs(x,2)]
    assert vals!=answers
    print(f'ABLATION S2 {label}: 필요(f={s.factor(fv)}, g={s.factor(gv)}, 답={vals})')

ablation('h의 미분가능성',(x-2)**2*(x+3),x-1,'미분가능')
ablation('f의 극솟값 0',x*(x*x-5*x+8),8*(x-1),'극솟값0')
ablation('f(1)=4',x*(x-2)**2,4*(x-1),'f(1)=4')
ablation('g(1)=0',fstar,x-9,'g(1)=0')
ablation('최고차항 계수 1',4*x*(x-2)**2,16*(x-1),'최고차항')
ablation('삼차함수',x*(x-2)**2*((x-1)**2+4),20*(x-1),'삼차함수')
ablation('일차함수',fstar,(x-1)*(x+9),'일차함수')

# 원문: P=f-g=x²(x-c). 내부의 추가 단순근은 금지이므로 c>=1 또는 c=0.
c=s.symbols('c',real=True)
P=x*x*(x-c)
# c=0일 때 1 근방 P>0. 연결 조건에서 g(1)=g′(1)=0 → g=0, 일차함수에 모순.
assert s.solve([g.subs(x,1),s.diff(g,x).subs(x,1)],(m,n))=={m:0,n:0}
# c>=1에서는 1의 왼쪽에서 P<0. -P와 P+2g를 값·미분계수로 연결.
matched=s.solve([(2*P+2*g).subs(x,1),s.diff(2*P+2*g,x).subs(x,1)],(m,n))
assert matched=={m:2*c-3,n:2-c}
g_orig=g.subs(matched)
h_right=s.expand(P+2*g_orig)
cv=s.solve(h_right.subs(x,2)-5,c)
assert cv==[R(5,2)]
assert cv[0]>=1 and (2*c-3).subs(c,cv[0])!=0
assert h_right.subs({x:4,c:cv[0]})==39
assert original.I['D62'][2]=='39'
print('ORIGINAL D62 정답 39; 경계근 c=1 및 삼중 인수 c=0 분기 포함 OK')

def length(t):
    t=html.unescape(re.sub(r'<[^>]*>','',t))
    t=re.sub(r'\\[()\[\]]','',t)
    return len(re.sub(r'\s+',' ',t).strip())
text=it['body']+''.join(q[0] for q in it['subs'])
old_len,new_len=length(original.I['D62'][0]),length(text)
assert new_len>=old_len
assert it['author']=='codex' and it['key']=='D62'
print(f'LENGTH 동일 기준 원문 {old_len}자 → 변형(소문항 포함) {new_len}자')
print('ALL OK')
