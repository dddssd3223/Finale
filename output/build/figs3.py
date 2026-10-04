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
def axes(ax,xl,yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal')
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    kw=dict(arrowstyle='-|>',lw=0.8,color='k',mutation_scale=8)
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops=kw); ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops=kw)
    ax.text(xl[1]-0.02,-0.13,'$x$',ha='right',va='top'); ax.text(0.12,yl[1]-0.02,'$y$',ha='left',va='top')
    ax.text(-0.08,-0.1,'O',ha='right',va='top')
fig,ax=plt.subplots(figsize=(2.6,2.25)); axes(ax,(-0.45,4.7),(-0.45,3.6))
ax.fill([0,0,1,1,2,3,3,4,4],[0,1,1,2,2,3,2,2,0],facecolor='#c8c8c8',edgecolor='k',lw=0.9)
for yv,xr in [(1,1),(2,1),(3,3)]: ax.plot([0,xr],[yv,yv],'k--',lw=0.5)
for xv,yt in [(1,1),(2,2),(3,2)]: ax.plot([xv,xv],[0,yt],'k--',lw=0.5)
for v in [1,2,3,4]: ax.text(v,-0.13,f'${v}$',ha='center',va='top')
for v in [1,2,3]: ax.text(-0.1,v,f'${v}$',ha='right',va='center')
fig.savefig('fig8.svg',bbox_inches='tight',pad_inches=0.02)
fig,ax=plt.subplots(figsize=(2.6,2.15)); axes(ax,(-2.0,4.9),(-1.3,3.9))
ax.plot([-1.9,0,2,4.4],[1.9,0,2,-0.4],'k',lw=1.0)
ax.plot([-1],[3],'ko',ms=3); ax.text(-1.1,3.05,'A',ha='right',va='bottom')
ax.plot([2],[0],'ko',ms=3); ax.text(2.05,-0.13,'B',ha='left',va='top')
ax.plot([-1,-1],[0,3],'k--',lw=0.5); ax.plot([-1,0],[3,3],'k--',lw=0.5)
ax.plot([2,2],[0,2],'k--',lw=0.5); ax.plot([0,2],[2,2],'k--',lw=0.5)
ax.text(-1,-0.13,'$-1$',ha='center',va='top'); ax.text(0.1,3,'$3$',ha='left',va='center')
ax.text(-0.1,2,'$2$',ha='right',va='center'); ax.text(4,-0.13,'$4$',ha='center',va='top')
ax.text(3.0,1.35,'y=f(x)',ha='left',va='bottom')
fig.savefig('fig17.svg',bbox_inches='tight',pad_inches=0.02)
