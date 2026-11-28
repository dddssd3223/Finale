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
# 17번: y=f(x)=x/2+5/32 x(x-4)(x-8), 직선 y=x/2, O, A(4,2), B(8,4), C(5,0)
f=lambda x: x/2+5/32*x*(x-4)*(x-8)
fig,ax=plt.subplots(figsize=(2.6,2.5)); axes(ax,(-1.2,9.9),(-1.6,6.8),asp=0.9,dx=0.2,dy=0.25)
X=np.linspace(-0.55,8.75,300); ax.plot(X,f(X),'k',lw=1.0)
L=np.linspace(-1.0,9.5,2); ax.plot(L,L/2,'k',lw=0.8)
T=np.linspace(2.6,5.6,2); ax.plot(T,-2*(T-4)+2,'k',lw=0.8)
ax.plot([5,8],[0,4],'k--',lw=0.5)
for (px,py) in [(0,0),(4,2),(8,4),(5,0)]: ax.plot([px],[py],'ko',ms=2.6)
ax.text(3.7,2.3,'A',ha='right',va='bottom'); ax.text(8.35,3.8,'B',ha='left',va='top')
ax.text(5.25,-0.3,'C',ha='left',va='top'); ax.text(8.3,6.3,'y=f(x)',ha='right',va='center')
fig.savefig('fig17.svg',bbox_inches='tight',pad_inches=0.02)
