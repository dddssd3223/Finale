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
def dash(ax,xs,ys): ax.plot(xs,ys,'k',ls='--',lw=0.5)
# 57
fig,ax=plt.subplots(figsize=(2.5,2.0)); axes(ax,(-0.45,4.8),(-0.45,3.7))
P=[(0,0),(0,1),(1,1),(2,2),(3,2),(3,3),(4,3),(4,0)]
ax.fill(*zip(*P),facecolor='#e2e2e2',edgecolor='k',lw=0.9)
for xv,yt in [(1,1),(2,2),(3,2)]: dash(ax,[xv,xv],[0,yt])
dash(ax,[0,2],[2,2]); dash(ax,[0,3],[3,3])
for v in [1,2,3,4]: ax.text(v,-0.13,f'{v}',ha='center',va='top')
for v in [1,2,3]: ax.text(-0.12,v,f'{v}',ha='right',va='center')
fig.savefig('fig57.svg',bbox_inches='tight',pad_inches=0.02)
# 65
fig,ax=plt.subplots(figsize=(2.8,2.1)); axes(ax,(-2.6,3.4),(-1.9,2.9))
x=np.linspace(-2.3,1,50); ax.plot(x,x+1,'k',lw=0.9)
x=np.linspace(1,2.85,50); ax.plot(x,-2*x+4,'k',lw=0.9)
ax.plot([1],[2],'ko',ms=2.5); ax.plot([-1],[-1],'ko',ms=2.5)
dash(ax,[0,1],[2,2]); dash(ax,[1,1],[0,2]); dash(ax,[-1,-1],[0,-1]); dash(ax,[-1,0],[-1,-1])
ax.text(1.08,2.08,'B',ha='left',va='bottom'); ax.text(-1.1,-1.05,'A',ha='right',va='top')
ax.text(-0.12,2,'2',ha='right',va='center'); ax.text(0.1,-1,'-1',ha='left',va='center')
ax.text(-1.05,0.08,'-1',ha='right',va='bottom'); ax.text(1,-0.13,'1',ha='center',va='top'); ax.text(2.08,-0.13,'2',ha='left',va='top')
ax.text(2.0,1.1,'y=f(x)',ha='left',va='center')
fig.savefig('fig65.svg',bbox_inches='tight',pad_inches=0.02)
# T5
f=lambda x:x**3-2*x
fig,ax=plt.subplots(figsize=(2.6,2.5)); axes(ax,(-2.0,3.6),(-2.0,5.2),dx=0.13,dy=0.15)
x=np.linspace(-1.75,2.3,200); ax.plot(x,f(x),'k',lw=0.9)
x=np.linspace(-2.0,2.9,10); ax.plot(x,x+2,'k',lw=0.7)
k=0.75; ax.fill([-1,k,2],[1,f(k),4],facecolor='#dddddd',edgecolor='k',lw=0.7)
for p in [(-1,1),(k,f(k)),(2,4)]: ax.plot(*p,'ko',ms=2)
ax.text(-1.12,1.12,'A',ha='right',va='bottom'); ax.text(2.08,3.9,'B',ha='left',va='top'); ax.text(k+0.05,f(k)-0.12,'P',ha='left',va='top')
ax.text(k+0.33,f(k)-0.35,'k',ha='left',va='top',fontsize=7)
ax.text(2.25,2.5,'y=f(x)',ha='left',va='center')
fig.savefig('figT5.svg',bbox_inches='tight',pad_inches=0.02)
# T7: f = x/2 + 5/8 x(x-2)(x-4)
f=lambda x:x/2+5/8*x*(x-2)*(x-4)
fig,ax=plt.subplots(figsize=(3.0,2.2)); axes(ax,(-0.7,6.9),(-1.1,4.2))
x=np.linspace(-0.12,4.6,300); ax.plot(x,f(x),'k',lw=0.9)
x=np.linspace(-0.4,5.6,10); ax.plot(x,x/2,'k',lw=0.7)
x=np.linspace(0.6,2.85,10); ax.plot(x,1-2*(x-2),'k',lw=0.7)
ax.plot([2.5,4],[0,2],'k',lw=0.7)
for p in [(2,1),(4,2),(2.5,0)]: ax.plot(*p,'ko',ms=2)
ax.text(1.9,1.15,'A',ha='right',va='bottom'); ax.text(4.08,1.9,'B',ha='left',va='top'); ax.text(2.45,-0.15,'C',ha='right',va='top')
X0,Y0=5.15,3.25
ax.text(X0,Y0,'y=',ha='left',va='center')
ax.text(X0+0.8,Y0+0.2,'1',ha='center',va='center',fontsize=8); ax.text(X0+0.8,Y0-0.2,'2',ha='center',va='center',fontsize=8)
ax.plot([X0+0.68,X0+0.92],[Y0,Y0],'k',lw=0.5); ax.text(X0+0.98,Y0,'x',ha='left',va='center')
ax.text(4.5,4.1,'y=f(x)',ha='left',va='top')
fig.savefig('figT7.svg',bbox_inches='tight',pad_inches=0.02)
