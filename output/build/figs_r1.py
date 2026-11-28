import numpy as np, matplotlib
matplotlib.use('svg')
from matplotlib import font_manager as fm
F='/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/fonts/'
for f in ['buE4poGnedXvwgX8.ttf','buE2poGnedXvwjX-fmE.ttf']: fm.fontManager.addfont(F+f)
import matplotlib.pyplot as plt
fm.fontManager.addfont(F+'hyhwpeq_web.ttf')
EQ=fm.FontProperties(fname=F+'hyhwpeq_web.ttf',size=11)
def pua(t, it=True):
    o=''
    for ch in t:
        if ch.islower() and it: o+=chr(0xE0E5+ord(ch)-97)
        elif ch.isupper(): o+=chr(0xE000+ord(ch)-65)
        elif ch.isdigit(): o+=chr(0xE03D if ch=='0' else 0xE034+int(ch)-1)
        else: o+={'-':chr(0xE046),'=':chr(0xE047),'(':chr(0xE044),')':chr(0xE045),' ':' '}.get(ch,ch)
    return o
_text=matplotlib.axes.Axes.text
def text(self,x,y,s,*a,**k):
    s=s.replace('$','').replace(r'\mathrm','')
    k.pop('family',None); k['fontproperties']=EQ
    return _text(self,x,y,pua(s),*a,**k)
matplotlib.axes.Axes.text=text
plt.rcParams.update({'font.family':'Tinos','mathtext.fontset':'custom','mathtext.it':'Tinos:italic','mathtext.rm':'Tinos','font.size':11,'svg.fonttype':'path'})
def axes(ax,xl,yl,asp='equal',dx=0.13,dy=0.12):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect(asp)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    kw=dict(arrowstyle='-|>',lw=0.8,color='k',mutation_scale=8)
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops=kw); ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops=kw)
    ax.text(xl[1]-0.02,-dy,'$x$',ha='right',va='top'); ax.text(dx,yl[1]-0.02,'$y$',ha='left',va='top')
    ax.text(-dx*0.6,-dy*0.8,'O',ha='right',va='top')

import numpy as np
# 15번: f(x)=2x^3-3x, A(-1,1), B(2,10), P_k
fig,ax=plt.subplots(figsize=(2.5,2.6)); axes(ax,(-1.9,2.7),(-3.0,12.5),asp=0.3,dx=0.1,dy=0.45)
X=np.linspace(-1.75,2.17,300); ax.plot(X,2*X**3-3*X,'k',lw=1.0)
T=np.linspace(-1.85,2.4,2); ax.plot(T,3*T+4,'k',lw=0.8)
k=0.55; P=(k,2*k**3-3*k)
ax.fill([-1,P[0],2],[1,P[1],10],facecolor='#c8c8c8',edgecolor='k',lw=0.7)
for (px,py) in [(-1,1),(2,10),P]: ax.plot([px],[py],'ko',ms=2.6)
ax.text(-1.08,1.25,'A',ha='right',va='bottom'); ax.text(1.93,10.2,'B',ha='right',va='bottom')
ax.text(P[0]+0.06,P[1]-0.35,'P',ha='left',va='top'); ax.text(P[0]+0.3,P[1]-1.05,'k',ha='left',va='top',fontsize=7)
ax.text(2.05,5.0,'y=f(x)',ha='left',va='center')
fig.savefig('fig15.svg',bbox_inches='tight',pad_inches=0.02)
# 17번: 곡선 y=f(x)와 직선 y=x/3, O, A(3,1), B(6,2), C(10/3,0)
f=lambda x: x/3+10/27*x*(x-3)*(x-6)
fig,ax=plt.subplots(figsize=(2.6,2.5)); axes(ax,(-0.9,7.4),(-3.0,6.8),asp=0.85,dx=0.15,dy=0.25)
X=np.linspace(-0.45,6.55,300); ax.plot(X,f(X),'k',lw=1.0)
L=np.linspace(-0.8,7.1,2); ax.plot(L,L/3,'k',lw=0.8)
T=np.linspace(1.75,3.85,2); ax.plot(T,-3*(T-3)+1,'k',lw=0.8)
ax.plot([10/3,6],[0,2],'k--',lw=0.5)
for (px,py) in [(0,0),(3,1),(6,2),(10/3,0)]: ax.plot([px],[py],'ko',ms=2.6)
ax.text(2.85,1.25,'A',ha='right',va='bottom'); ax.text(6.25,1.8,'B',ha='left',va='top')
ax.text(3.55,-0.25,'C',ha='left',va='top')
ax.text(6.0,5.9,'y=f(x)',ha='right',va='center')
fig.savefig('fig17.svg',bbox_inches='tight',pad_inches=0.02)
