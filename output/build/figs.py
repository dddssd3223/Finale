import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'cm','font.size':11})
def axes(ax,xl,yl,xo=0.12,yo=0.12):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal')
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    kw=dict(arrowstyle='-|>',lw=0.9,color='k',mutation_scale=9)
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops=kw)
    ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops=kw)
    ax.text(xl[1]-0.02,-0.15,'$x$',ha='right',va='top'); ax.text(0.12,yl[1]-0.02,'$y$',ha='left',va='top')
    ax.text(-0.1,-0.12,'O',ha='right',va='top',family='DejaVu Serif',fontsize=10)
# ---- fig8: region 1 on [0,1], 2 on [1,2], y=x on [2,3], 2 on [3,4]
fig,ax=plt.subplots(figsize=(2.6,2.25))
axes(ax,(-0.45,4.7),(-0.45,3.6))
X=[0,0,1,1,2,2,3,3,4,4]; Y=[0,1,1,2,2,2,3,2,2,0]
ax.fill(X,Y,facecolor='#bdbdbd',edgecolor='k',lw=1.0)
for xv,yv in [(1,1),(2,2),(3,3),(3,2),(1,2)]:
    pass
ax.plot([0,1],[1,1],'k',lw=1.0)
for yv,xr in [(1,1),(2,1),(3,3)]:
    ax.plot([0,xr],[yv,yv],'k--',lw=0.6)
ax.plot([3,3],[0,2],'k--',lw=0.6); ax.plot([1,1],[0,1],'k--',lw=0.6); ax.plot([2,2],[0,2],'k--',lw=0.6)
for v in [1,2,3,4]: ax.text(v,-0.12,f'${v}$',ha='center',va='top')
for v in [1,2,3]: ax.text(-0.1,v,f'${v}$',ha='right',va='center')
fig.savefig('fig8.png',dpi=300,bbox_inches='tight',pad_inches=0.03,facecolor='white')
# ---- fig17: f zigzag, A(-1,3), B(2,0)
fig,ax=plt.subplots(figsize=(2.6,2.15))
axes(ax,(-2.0,4.9),(-1.3,3.9))
xs=np.array([-1.9,0,2,4.4]); ys=np.array([1.9,0,2,-0.4])
ax.plot(xs,ys,'k',lw=1.1)
ax.plot([-1],[3],'ko',ms=3.2); ax.text(-1.1,3.05,r'$\mathrm{A}$',ha='right',va='bottom')
ax.plot([2],[0],'ko',ms=3.2); ax.text(2.05,-0.12,r'$\mathrm{B}$',ha='left',va='top')
ax.plot([-1,-1],[0,3],'k--',lw=0.6); ax.plot([-1,0],[3,3],'k--',lw=0.6)
ax.plot([2,2],[0,2],'k--',lw=0.6); ax.plot([0,2],[2,2],'k--',lw=0.6)
ax.text(-1,-0.12,'$-1$',ha='center',va='top'); ax.text(0.1,3,'$3$',ha='left',va='center')
ax.text(-0.1,2,'$2$',ha='right',va='center'); ax.text(4,-0.12,'$4$',ha='center',va='top')
ax.text(3.0,1.35,'$y=f(x)$',ha='left',va='bottom',fontsize=10)
fig.savefig('fig17.png',dpi=300,bbox_inches='tight',pad_inches=0.03,facecolor='white')
from PIL import Image
for f in ['fig8.png','fig17.png']:
    im=Image.open(f); print(f,im.size)
