import sys; sys.path.insert(0,'/home/user/Finale/output/build/기말/지침'); import figkit as K
fig,ax=K.new((-0.6,5.6),(-0.6,2.9),size=(2.4,1.45),dx=0.18,dy=0.18)
K.line(ax,[0,4,4,0],[0,0,2,2],lw=0.9)
for x,y in [(4,0),(4,2),(0,2)]: K.dot(ax,x,y,ms=2.4)
K.label(ax,3.95,-0.12,'A(4,0)','right','top',size=9)
K.label(ax,4.05,2.08,'B(4,2)','left','bottom',size=9)
K.label(ax,-0.1,2.08,'C(0,2)','right','bottom',size=9)
K.save(fig,'/home/user/Finale/output/build/기말/견본4/parts/fig_c_14.svg')
