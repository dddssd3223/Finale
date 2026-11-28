import sys,numpy as np; sys.path.insert(0,'/home/user/Finale/output/build/기말/지침'); import figkit as K
r3=np.sqrt(3); k=2*r3
f=lambda x: np.abs(x**2-3)
fig,ax=K.new((-2.5,4.5),(-1.2,10.2),size=(2.3,2.3))
K.shade(ax,f,-r3,r3)
K.hatch(fig,ax,f,r3,k)
K.curve(ax,f,-2.4,k+0.12)
K.line(ax,[k,k],[-0.5,10.0])
K.label(ax,0.5,1.25,'A',size=10); K.label(ax,2.95,2.0,'B',size=10,bg=True)
K.label(ax,k-0.08,-0.3,'k','right','top',size=10)
K.tex(ax,r3,-0.35,r'$\sqrt{3}$','center','top',size=8); K.tex(ax,-r3,-0.35,r'$-\sqrt{3}$','center','top',size=8)
K.label(ax,-2.4,9.0,'y=f(x)','left','center',size=10)
K.save(fig,'/home/user/Finale/output/build/기말/견본3/parts/fig_b3_6.svg')
