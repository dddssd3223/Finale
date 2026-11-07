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
# 17번: f(x)=2-x (x<=1), x-2 (1<x<=3), 3x-8 (x>3)
fig,ax=plt.subplots(figsize=(2.5,2.4)); axes(ax,(-0.7,4.3),(-1.6,2.9),dx=0.1,dy=0.13)
ax.plot([-0.6,1],[2.6,1],'k',lw=1.0)
ax.plot([1,3],[-1,1],'k',lw=1.0)
ax.plot([3,3.6],[1,2.8],'k',lw=1.0)
ax.plot([1],[1],'ko',ms=3.2)
ax.plot([1],[-1],'o',ms=3.4,mfc='white',mec='k',mew=0.9)
ax.plot([1,1],[-1,1],'k--',lw=0.5); ax.plot([0,1],[1,1],'k--',lw=0.5); ax.plot([0,1],[-1,-1],'k--',lw=0.5)
ax.plot([3,3],[0,1],'k--',lw=0.5); ax.plot([1,3],[1,1],'k--',lw=0.5)
ax.text(1,0.12,'$1$',ha='center',va='bottom'); ax.text(3,-0.13,'$3$',ha='center',va='top')
ax.text(-0.1,1,'$1$',ha='right',va='center'); ax.text(-0.1,-1,'$-1$',ha='right',va='center')
ax.text(-0.1,2,'$2$',ha='right',va='center'); ax.text(2,-0.13,'$2$',ha='center',va='top')
ax.text(3.62,2.2,'y=f(x)',ha='left',va='center')
fig.savefig('fig17.svg',bbox_inches='tight',pad_inches=0.02)
