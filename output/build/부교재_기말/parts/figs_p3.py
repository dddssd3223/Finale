exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
os.chdir('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb3/parts')

def seg(ax, xs, ys, lw=1.0): ax.plot(xs, ys, 'k', lw=lw)
def save(fig, name):
    fig.savefig(name + '.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

# ---- M7 ----  f(x)=x (0<=x<1), sqrt(2-x) (1<=x<=2); y=t, trapezoid POHQ shaded
fig, ax = plt.subplots(figsize=(2.5, 1.6))
axes(ax, (-0.35, 2.55), (-0.32, 1.42), dx=0.07, dy=0.06)
t = 0.62; xq = 2 - t * t
ax.fill([0, xq, xq, t], [0, 0, t, t], color='#e6e6e6', lw=0, zorder=0)
seg(ax, [0, 1], [0, 1], lw=1.1)
xs = np.linspace(1, 2, 200); seg(ax, xs, np.sqrt(2 - xs), lw=1.1)
seg(ax, [-0.22, 2.4], [t, t], lw=0.6)
seg(ax, [xq, xq], [0, t], lw=0.7)
dash(ax, [0, 1], [1, 1]); dash(ax, [1, 1], [0, 1])
s = 0.07; seg(ax, [xq - s, xq - s, xq], [0, s, s], lw=0.5)
ax.text(-0.06, 1, '1', ha='right', va='center')
ax.text(1, -0.06, '1', ha='center', va='top'); ax.text(xq, -0.06, 'H', ha='center', va='top')
ax.text(2.0, -0.06, '2', ha='center', va='top')
ax.text(t - 0.03, t + 0.04, 'P', ha='right', va='bottom')
ax.text(xq, t + 0.05, 'Q', ha='center', va='bottom')
ax.text(1.03, 1.04, 'y=f(x)', ha='left', va='bottom')
ax.text(2.43, t, 'y=t', ha='left', va='center')
save(fig, 'fig_M7')
