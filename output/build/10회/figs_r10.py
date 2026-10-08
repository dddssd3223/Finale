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
import numpy as np
def dash(ax,xs,ys): ax.plot(xs,ys,'k',ls=(0,(3,2)),lw=0.5)
def op(ax,x,y): ax.plot(x,y,'o',ms=3.2,mfc='white',mec='k',mew=0.8,zorder=5)
def cl(ax,x,y): ax.plot(x,y,'o',ms=3.2,color='k',zorder=5)
# 5번
fig,ax=plt.subplots(figsize=(2.5,2.1)); axes(ax,(-3.2,3.6),(-0.9,3.9))
x=np.linspace(-3.0,-1,10); ax.plot(x,x+3,'k',lw=0.9)
x=np.linspace(-1,1,60); ax.plot(x,x**2,'k',lw=0.9)
x=np.linspace(1,3.3,10); ax.plot(x,-x+4,'k',lw=0.9)
op(ax,-1,2); cl(ax,-1,1); op(ax,1,1); cl(ax,1,3)
dash(ax,[-1,-1],[0,2]); dash(ax,[-1,0],[2,2]); dash(ax,[1,1],[0,3]); dash(ax,[0,1],[3,3]); dash(ax,[-1,1],[1,1])
ax.text(-1,-0.12,'-1',ha='center',va='top'); ax.text(1.05,-0.12,'1',ha='left',va='top')
ax.text(-0.1,3,'3',ha='right',va='center'); ax.text(0.1,2.12,'2',ha='left',va='bottom'); ax.text(-0.1,1.12,'1',ha='right',va='bottom')
ax.text(2.0,2.7,'y=f(x)',ha='left',va='center')
fig.savefig('fig05.svg',bbox_inches='tight',pad_inches=0.02)
# 15번: f = x/2 + 5/32 x(x-4)(x-8), A(4,2), B(8,4), C(5,0)
f=lambda x:x/2+5/32*x*(x-4)*(x-8)
fig,ax=plt.subplots(figsize=(3.0,2.3)); axes(ax,(-1.2,13.2),(-2.4,8.6),asp='auto',dx=0.3,dy=0.3)
x=np.linspace(-0.25,9.0,300); ax.plot(x,f(x),'k',lw=0.9)
x=np.linspace(-0.8,12.4,10); ax.plot(x,x/2,'k',lw=0.7)
x=np.linspace(2.2,6.0,10); ax.plot(x,2-2*(x-4),'k',lw=0.7)
ax.plot([5,8],[0,4],'k',lw=0.7)
for P_ in [(4,2),(8,4),(5,0)]: ax.plot(*P_,'ko',ms=2)
ax.text(3.8,2.3,'A',ha='right',va='bottom'); ax.text(8.2,3.8,'B',ha='left',va='top'); ax.text(5.1,-0.35,'C',ha='left',va='top')
ax.text(9.4,8.2,'y=f(x)',ha='left',va='top')
X0,Y0=10.4,4.0
ax.text(X0,Y0,'y=',ha='left',va='center')
ax.text(X0+1.15,Y0+0.45,'1',ha='center',va='center',fontsize=8); ax.text(X0+1.15,Y0-0.45,'2',ha='center',va='center',fontsize=8)
ax.plot([X0+0.95,X0+1.35],[Y0,Y0],'k',lw=0.5); ax.text(X0+1.45,Y0,'x',ha='left',va='center')
fig.savefig('fig15.svg',bbox_inches='tight',pad_inches=0.02)
