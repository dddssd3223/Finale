exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
import os
OUT = '/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb3/parts'
os.chdir(OUT)   # figs_head chdirs into wb2/parts; write our svgs into wb3/parts
def herm(px, py, ms, n=400):
    # piecewise cubic Hermite through (px,py) with slopes ms
    X=[]; Y=[]
    for i in range(len(px)-1):
        h=px[i+1]-px[i]; t=np.linspace(0,1,n//(len(px)-1))
        h00=2*t**3-3*t**2+1; h10=t**3-2*t**2+t; h01=-2*t**3+3*t**2; h11=t**3-t**2
        X+=list(px[i]+h*t); Y+=list(h00*py[i]+h10*h*ms[i]+h01*py[i+1]+h11*h*ms[i+1])
    return np.array(X), np.array(Y)
def dash(ax,xs,ys): ax.plot(xs,ys,'k',lw=0.5,dashes=(2.5,1.8))
PR = chr(0xE050)  # prime glyph in the equation font

# ---- D27: y=f'(x) (cubic-like: root O, min at a, root b, max at c, root d) ----
fig, ax = plt.subplots(figsize=(2.5, 1.75))
u = 1/30
P = [(-28, 77), (0, 0), (36, -44), (62, 0), (86, 47), (132, 0), (159, -47)]
px = np.array([p[0] for p in P])*u; py = np.array([p[1] for p in P])*u
axes(ax, (-1.5, 6.0), (-2.4, 3.2), dx=0.15, dy=0.15)
# remove default O (placed manually)
for t in ax.texts[:]:
    if t.get_text() == pua('O'): t.remove()
ms = [-2.6, -2.2, 0, 2.6, 0, -2.1, -2.0]
xs, ys = herm(px, py, ms); ax.plot(xs, ys, 'k', lw=0.9)
a, b, c, d = px[2], px[3], px[4], px[5]
dash(ax, [a, a], [0, py[2]]); dash(ax, [c, c], [0, py[4]])
ax.text(-0.12, -0.12, 'O', ha='right', va='top')
ax.text(a, 0.1, '$a$', ha='center', va='bottom')
ax.text(b+0.1, -0.12, '$b$', ha='left', va='top')
ax.text(c, -0.12, '$c$', ha='center', va='top')
ax.text(d+0.05, 0.1, '$d$', ha='left', va='bottom')
ax.text(c+0.4, py[4]+0.2, 'y=f' + PR + '(x)', ha='left', va='bottom')
fig.savefig('fig_D27.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

# ---- D28: y=f'(x): -x-1 (x<=-1), cos(pi x/2) (-1<=x<=2), x-3 (x>=2) ----
fig, ax = plt.subplots(figsize=(2.75, 1.5))
axes(ax, (-2.25, 4.3), (-1.25, 1.75), dx=0.15, dy=0.12)
for t in ax.texts[:]:
    if t.get_text() == pua('O'): t.remove()
xs = np.linspace(-2.05, -1, 20); ax.plot(xs, -xs-1, 'k', lw=0.9)
xs = np.linspace(-1, 2, 300); ax.plot(xs, np.cos(np.pi*xs/2), 'k', lw=0.9)
xs = np.linspace(2, 4.1, 20); ax.plot(xs, xs-3, 'k', lw=0.9)
dash(ax, [2, 2], [0, -1])
ax.text(-1, -0.12, '-1', ha='center', va='top')
ax.text(-0.1, -0.12, 'O', ha='right', va='top')
ax.text(1, -0.12, '1', ha='center', va='top')
ax.text(2, 0.1, '2', ha='center', va='bottom')
ax.text(3.05, -0.12, '3', ha='left', va='top')
ax.text(2.6, 1.75, 'y=f' + PR + '(x)', ha='left', va='top')
fig.savefig('fig_D28.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)
