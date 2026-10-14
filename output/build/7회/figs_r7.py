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
# 4번
fig,ax=plt.subplots(figsize=(2.4,2.1)); axes(ax,(-2.2,3.6),(-1.7,3.1))
x=np.linspace(-2.0,0,10); ax.plot(x,-x+1,'k',lw=0.9)
x=np.linspace(0,1,10); ax.plot(x,x-1,'k',lw=0.9)
x=np.linspace(1,3.4,10); ax.plot(x,-x+3,'k',lw=0.9)
op(ax,0,1); cl(ax,0,-1); op(ax,1,0); cl(ax,1,2)
dash(ax,[0,1],[2,2]); dash(ax,[1,1],[0,2]); dash(ax,[-1,-1],[0,2]); dash(ax,[-1,0],[2,2])
ax.text(-0.1,2,'2',ha='right',va='center'); ax.text(0.1,1.05,'1',ha='left',va='bottom'); ax.text(0.1,-1,'-1',ha='left',va='center')
ax.text(-1,-0.12,'-1',ha='center',va='top'); ax.text(1.08,-0.12,'1',ha='left',va='top'); ax.text(3,-0.12,'3',ha='center',va='top')
ax.text(2.3,1.25,'y=f(x)',ha='left',va='center')
fig.savefig('fig04.svg',bbox_inches='tight',pad_inches=0.02)
# 13번
fig,ax=plt.subplots(figsize=(2.4,2.0)); axes(ax,(-0.9,5.3),(-0.8,6.0))
x=np.linspace(-0.55,4.55,300); ax.plot(x,np.abs(x**2-4*x),'k',lw=0.9)
dash(ax,[-0.9,5.0],[2.6,2.6]); dash(ax,[2,2],[0,4]); dash(ax,[0,2],[4,4])
ax.text(-0.1,4,'4',ha='right',va='center'); ax.text(2,-0.15,'2',ha='center',va='top'); ax.text(4,-0.15,'4',ha='center',va='top')
ax.text(4.95,2.75,'y=t',ha='right',va='bottom')
def seq(ax,x,y,parts):
    fig=ax.figure; fig.canvas.draw(); inv=ax.transData.inverted()
    for p_,kind in parts:
        if kind=='bar': t_=ax.annotate('|',(x+0.02,y),ha='left',va='bottom',fontsize=11,family='Tinos')
        elif kind=='sup': t_=ax.text(x+0.01,y+0.3,p_,ha='left',va='bottom',fontsize=7)
        else: t_=ax.text(x,y,p_,ha='left',va='bottom')
        fig.canvas.draw(); x=t_.get_window_extent().transformed(inv).x1+(0.02 if kind=='bar' else 0)
seq(ax,2.1,5.25,[('y=',''),('','bar'),('x',''),('2','sup'),('-4x',''),('','bar')])
fig.savefig('fig13.svg',bbox_inches='tight',pad_inches=0.02)
