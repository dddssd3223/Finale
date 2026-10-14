exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy
def dash(ax,xs,ys): ax.plot(xs,ys,'k',lw=0.5,dashes=(2.5,1.8))
PLUS = chr(0xE048)
def lab_sq(ax, x, y, base='y=x', **kw):
    # base text (left-aligned, top-aligned at (x,y)) followed by a small raised '2'
    fig = ax.figure; r = fig._get_renderer()
    t = ax.text(x, y, base, ha='left', va='top')
    w = t.get_window_extent(r).width * 72 / fig.dpi
    tr = offset_copy(ax.transData, fig=fig, x=w + 0.3, y=1.0, units='points')
    _text(ax, x, y, pua('2'), fontproperties=FontProperties(fname=F+'hyhwpeq_web.ttf', size=7), ha='left', va='top', transform=tr)

# ---- L61 ----
fig, ax = plt.subplots(figsize=(2.6, 2.15))
t = 10/9; s = np.sqrt(1+4*t); a = (1+s)/2; b = (1-s)/2; yA = a*a
axes(ax, (-2.5, 2.6), (-0.45, 3.75), dx=0.1, dy=0.1)
xs = np.linspace(-1.9, 1.86, 300); ax.plot(xs, xs**2, 'k', lw=0.9)
xs = np.linspace(-1.6, 2.2, 10); ax.plot(xs, xs+t, 'k', lw=0.9)
ax.plot([-2.45, 2.3], [yA, yA], 'k', lw=0.9)
ax.plot([b, b], [b*b, yA], 'k', lw=0.8)
q = 0.1; ax.plot([b-q, b-q, b], [yA, yA-q, yA-q], 'k', lw=0.5)
ax.text(b+0.02, yA+0.1, 'H', ha='center', va='bottom')
ax.text(-a-0.02, yA-0.1, 'C', ha='right', va='top')
ax.text(a+0.03, yA-0.1, 'A', ha='left', va='top')
ax.text(b-0.08, b*b, 'B', ha='right', va='center')
lab_sq(ax, 0.75, 3.8)
ax.text(2.08, 3.78, 'y=x'+PLUS+'t', ha='left', va='top')
fig.savefig('fig_L61.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

# ---- L62 ----
fig, ax = plt.subplots(figsize=(2.6, 2.2))
t = 0.65
axes(ax, (-2.4, 4.4), (-1.5, 4.3), dx=0.15, dy=0.15)
xs = np.linspace(-2.05, 2.06, 300); ax.plot(xs, xs**2, 'k', lw=0.9)
x0, x1 = (-1.5+1)/(2*t), (4.25+1)/(2*t); ax.plot([x0, x1], [2*t*x0-1, 2*t*x1-1], 'k', lw=0.9)
ax.plot([-2.0, 4.3], [-2.0*t, 4.3*t], 'k', lw=0.9)
ax.text(t-0.12, t*t+0.08, 'P', ha='right', va='bottom')
ax.text(1/t+0.15, 1-0.05, 'Q', ha='left', va='top')
lab_sq(ax, 2.05, 4.3)
ax.text(x1+0.08, 4.25, 'y=2tx-1', ha='left', va='top')
fig.savefig('fig_L62.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

# ---- C2 ----
fig, ax = plt.subplots(figsize=(2.4, 1.85))
axes(ax, (-2.2, 6.6), (-3.0, 3.7), dx=0.15, dy=0.15)
xs = np.linspace(-1.9, 1, 200); ax.plot(xs, xs**2, 'k', lw=0.9)
ax.plot([1, 3], [1, -1], 'k', lw=0.9)
xs = np.linspace(3, 5.95, 200); ax.plot(xs, -(xs-3)*(xs-5), 'k', lw=0.9)
dash(ax, [0, 1], [1, 1]); dash(ax, [1, 1], [0, 1]); dash(ax, [0, 3], [-1, -1]); dash(ax, [3, 3], [-1, 0])
ax.plot([1, 3], [0, 0], 'ko', ms=3)
ax.plot([1, 3], [1, -1], 'o', ms=3, mfc='white', mec='k', mew=0.8)
ax.text(1, -0.2, '1', ha='center', va='top'); ax.text(2, -0.2, '2', ha='center', va='top')
ax.text(3.08, -0.2, '3', ha='left', va='top'); ax.text(4.9, -0.2, '5', ha='right', va='top')
ax.text(-0.1, 1, '1', ha='right', va='center'); ax.text(-0.1, -1, '-1', ha='right', va='center')
ax.text(4.4, 1.25, 'y=f(x)', ha='left', va='bottom')
fig.savefig('fig_C2.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)
