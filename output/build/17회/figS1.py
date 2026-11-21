import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams['font.family']='DejaVu Serif'; plt.rcParams['mathtext.fontset']='cm'
t=1.25
fig,ax=plt.subplots(figsize=(2.6,2.3))
xs=np.linspace(-1.6,3.6,400); ax.plot(xs,xs**2,'k',lw=0.9)
xl=np.linspace(0.6,4.2,10); ax.plot(xl,2*t*xl-4,'k',lw=0.9)
P=(t,t*t); Q=(4/t,4)
xo=np.linspace(-0.3,4.0,10); ax.plot(xo,t*xo,'k',lw=0.6,ls=(0,(3,2)))
ax.annotate('',xy=(4.3,0),xytext=(-1.8,0),arrowprops=dict(arrowstyle='->',lw=0.7))
ax.annotate('',xy=(0,6.3),xytext=(0,-1.6),arrowprops=dict(arrowstyle='->',lw=0.7))
for (px,py),lab,off in [(P,'P',(-0.42,0.15)),(Q,'Q',(0.12,-0.35))]:
    ax.plot(px,py,'ko',ms=2.6); ax.text(px+off[0],py+off[1],r'$\mathrm{%s}$'%lab,fontsize=10)
ax.text(-0.35,-0.45,r'$\mathrm{O}$',fontsize=10)
ax.text(4.32,-0.18,r'$x$',fontsize=10); ax.text(0.1,6.15,r'$y$',fontsize=10)
ax.text(-1.75,3.2,r'$y=x^2$',fontsize=9)
ax.text(2.9,6.0,r'$y=2tx-4$',fontsize=9)
ax.set_xlim(-1.9,4.6); ax.set_ylim(-1.7,6.6); ax.axis('off')
plt.savefig('fig_S1.svg',bbox_inches='tight',pad_inches=0.02)
