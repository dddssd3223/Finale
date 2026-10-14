exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
from matplotlib.font_manager import FontProperties
TIN = FontProperties(family='Tinos', size=11)
def dash(ax,xs,ys): ax.plot(xs,ys,'k',lw=0.5,dashes=(2.5,1.8))

def seq(ax, x, y, pieces, ha='left'):
    """Draw a label made of pieces left-to-right starting at data point (x,y) (baseline-ish center).
    piece: (str, kind) kind in 'eq' (equation font), 'sup' (small raised eq), 'lt' ('<' in Tinos), 'sqrt' (radical over eq text)."""
    fig = ax.figure; ax.apply_aspect(); r = fig._get_renderer()
    widths = []
    arts = []
    for s, k in pieces:
        if k == 'lt':
            t = _text(ax, 0, 0, '<', fontproperties=FontProperties(family='Tinos', size=12), va='center', ha='left')
        elif k == 'sup':
            t = _text(ax, 0, 0, pua(s), fontproperties=FontProperties(fname=F+'hyhwpeq_web.ttf', size=7), va='center', ha='left')
        else:
            t = _text(ax, 0, 0, pua(s), fontproperties=EQ, va='center', ha='left')
        bb = t.get_window_extent(r); widths.append(bb.width * 72 / fig.dpi); arts.append(t)
    tot = sum(widths) + sum(4 for s, k in pieces if k == 'sqrt')
    off = -tot if ha == 'right' else (-tot / 2 if ha == 'center' else 0)
    from matplotlib.transforms import offset_copy
    for (s, k), t, w in zip(pieces, arts, widths):
        if k == 'sqrt':
            off += 4
        tr = offset_copy(ax.transData, fig=fig, x=off, y=(4 if k == 'sup' else (-0.8 if k == 'lt' else 0)), units='points')
        t.set_transform(tr); t.set_position((x, y))
        if k == 'sqrt':
            # radical sign drawn in points relative to (x,y)
            xs = [-4.2, -3.3, -1.9, -0.6, w + 0.3]
            ys = [-0.6, -1.2, -5.0, 6.2, 6.2]
            base = ax.transData.transform((x, y))
            pts = [(base[0] + (off + a) * fig.dpi / 72, base[1] + b * fig.dpi / 72) for a, b in zip(xs, ys)]
            inv = ax.transData.inverted()
            dpts = inv.transform(pts)
            ax.plot(dpts[:, 0], dpts[:, 1], 'k', lw=0.6, solid_capstyle='butt')
        off += w

def save(fig, name):
    fig.savefig(name + '.svg', bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)

# ---------- L40 ----------
tt = 0.53
fig, ax = plt.subplots(figsize=(2.6, 1.8)); axes(ax, (-1.85, 2.75), (-1.35, 1.75))
xs = np.linspace(-1.78, 1.75, 300); ax.plot(xs, tt * xs**2, 'k', lw=1.0)
px, py = 1 / (2 * tt), 1 / (4 * tt)
xs = np.linspace(-1.5, 2.6, 10); ax.plot(xs, 0.5 * xs, 'k', lw=0.6)
xs = np.linspace(-0.3, 2.45, 10); ax.plot(xs, xs - 1, 'k', lw=0.6)
qx = (px + py + 1) / 2; qy = qx - 1
ax.fill([px, qx, 2], [py, qy, 1], facecolor='#dddddd', edgecolor='k', lw=0.6)
ax.plot([px, qx], [py, qy], 'k', lw=0.6)
s = 0.09; u = np.array([1, 1]) / np.sqrt(2); v = np.array([-1, 1]) / np.sqrt(2)
c = np.array([qx, qy]); ax.plot(*zip(c + s * u, c + s * u + s * v, c + s * v), color='k', lw=0.5)
ax.text(px - 0.04, py + 0.06, 'P', ha='right', va='bottom')
ax.text(qx + 0.1, qy - 0.08, 'Q', ha='left', va='top')
ax.text(2.08, 1.0, 'R', ha='left', va='top')
seq(ax, 0.42, 1.62, [('y=tx', 'eq'), ('2', 'sup')])
ax.text(1.85, 1.62, 'y=x-1', ha='left', va='center')
save(fig, 'fig_L40')

# ---------- L42 ----------
cub = lambda x: (x - 1) * (x + 0.5) * (x - 2)
fig, ax = plt.subplots(figsize=(3.0, 1.75)); axes(ax, (-4.4, 4.4), (-1.5, 2.6), asp='auto', dx=0.2, dy=0.12)
xs = np.linspace(-4.3, 0, 200); ax.plot(xs, (xs + 3) * (xs - 3) / 9, 'k', lw=1.0)
xs = np.linspace(0, 1, 100); ax.plot(xs, cub(xs), 'k', lw=1.0)
xs = np.linspace(1, 4.0, 10); ax.plot(xs, -xs + 3, 'k', lw=1.0)
dash(ax, [0, 1], [2, 2]); dash(ax, [1, 1], [0, 2])
ax.plot([0], [1], 'ko', ms=3); ax.plot([1], [2], 'ko', ms=3)
ax.plot([0], [-1], 'o', ms=3, mfc='white', mec='k', mew=0.8); ax.plot([1], [0], 'o', ms=3, mfc='white', mec='k', mew=0.8)
ax.text(-3, -0.12, '-3', ha='center', va='top'); ax.text(1, -0.12, '1', ha='center', va='top'); ax.text(3, -0.12, '3', ha='center', va='top')
ax.text(-0.15, 2, '2', ha='right', va='center'); ax.text(-0.15, 1, '1', ha='right', va='center')
ax.text(0.15, -1, '-1', ha='left', va='center')
ax.text(1.75, 1.95, 'y=f(x)', ha='left', va='center')
save(fig, 'fig_L42')

# ---------- L44 ----------
t = 2.0
yP = (-t + np.sqrt(t * t + 4 * t)) / 2; xP = yP**2
xQ = (t - np.sqrt(t * t + 4 * t)) / 2; yQ = xQ**2
fig, ax = plt.subplots(figsize=(2.6, 1.75)); axes(ax, (-1.95, 2.95), (-0.35, 2.75), dx=0.13, dy=0.12)
ax.fill([0, t, xP], [0, 0, yP], facecolor='#e2e2e2', edgecolor='none')
ax.fill([0, -1, xQ], [0, 0, yQ], facecolor='#e2e2e2', edgecolor='none')
xs = np.linspace(-1.55, 0, 200); ax.plot(xs, xs**2, 'k', lw=1.0)
xs = np.linspace(0, 2.45, 300); ax.plot(xs, np.sqrt(xs), 'k', lw=1.0)
ax.plot([0, t], [1, 0], 'k', lw=0.8); ax.plot([-1, 0], [0, t], 'k', lw=0.8)
ax.plot([0, xP], [0, yP], 'k', lw=0.6); ax.plot([0, xQ], [0, yQ], 'k', lw=0.6)
ax.text(0.1, t, 'C', ha='left', va='center'); ax.text(-0.08, 1.0, 'B', ha='right', va='bottom')
ax.text(xP + 0.02, yP + 0.08, 'P', ha='left', va='bottom'); ax.text(xQ - 0.12, yQ + 0.0, 'Q', ha='right', va='center')
ax.text(-1, -0.12, 'D', ha='center', va='top'); ax.text(t, -0.12, 'A', ha='center', va='top')
seq(ax, -0.25, 2.6, [('y=x', 'eq'), ('2', 'sup'), ('(x', 'eq'), ('<', 'lt'), ('0)', 'eq')], ha='right')
seq(ax, 1.75, 1.95, [('y=', 'eq'), ('x', 'sqrt')])
save(fig, 'fig_L44')

# ---------- L46 ----------
tt = 1.0
fig, ax = plt.subplots(figsize=(1.75, 1.85)); axes(ax, (-1.6, 3.2), (-1.7, 3.8))
xs = np.linspace(-1.2, 2.95, 300); ax.plot(xs, xs**2 - 2 * xs, 'k', lw=1.0)
xs = np.linspace(-1.3, 1.45, 10); ax.plot(xs, -2 * (xs - tt) + tt**2 - 2 * tt, 'k', lw=0.6)
ax.plot([0, -tt], [0, tt * tt + 2 * tt], 'k', lw=0.6)
ax.text(-tt - 0.1, 3.0, 'Q', ha='right', va='center')
ax.text(tt - 0.05, -1.15, 'P', ha='right', va='top')
seq(ax, 0.8, 3.55, [('y=x', 'eq'), ('2', 'sup'), ('-2x', 'eq')])
save(fig, 'fig_L46')

# ---------- L48 ----------
tt = 0.4
fig, ax = plt.subplots(figsize=(1.55, 1.55))
ax.set_xlim(-0.12, 1.15); ax.set_ylim(-0.1, 1.12); ax.set_aspect('equal'); ax.axis('off')
ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k', lw=1.0)
ry = tt / (1 + tt * tt / 2); rx = ry / tt
ax.fill([1, 1, rx], [0, tt, ry], facecolor='#dddddd', edgecolor='none')
ax.plot([0, 1], [0, tt], 'k', lw=0.7); ax.plot([1, 1 - tt / 2], [0, 1], 'k', lw=0.7)
ax.text(-0.03, 1.0, 'A', ha='right', va='center'); ax.text(-0.03, 0, 'B', ha='right', va='center')
ax.text(1.03, 0, 'C', ha='left', va='center'); ax.text(1.03, 1.0, 'D', ha='left', va='center')
ax.text(1.04, tt + 0.02, 'P', ha='left', va='center'); ax.text(1 - tt / 2, 1.03, 'Q', ha='center', va='bottom')
ax.text(rx - 0.03, ry + 0.03, 'R', ha='right', va='bottom')
save(fig, 'fig_L48')

# ---------- L49 ----------
fig, ax = plt.subplots(figsize=(2.9, 2.3)); axes(ax, (-2.85, 2.85), (-1.75, 2.85), dx=0.15, dy=0.12)
xs = np.linspace(-2.75, -1, 10); ax.plot(xs, -(xs + 2), 'k', lw=1.0)
xs = np.linspace(-1, 1, 200); ax.plot(xs, 1 - xs**3, 'k', lw=1.0)
xs = np.linspace(1, 2.7, 10); ax.plot(xs, -(xs - 2), 'k', lw=1.0)
dash(ax, [-1, -1], [-1, 2]); dash(ax, [-1, 0], [2, 2]); dash(ax, [-1, 1], [1, 1]); dash(ax, [1, 1], [0, 1]); dash(ax, [-1, 0], [-1, -1])
for p in [(-1, 2), (-1, -1), (1, 1)]: ax.plot(*p, 'o', ms=3, mfc='white', mec='k', mew=0.8)
for p in [(-1, 1), (1, 0)]: ax.plot(*p, 'ko', ms=3)
for v, s in [(-2, '-2'), (-1, '-1'), (1, '1'), (2, '2')]:
    ax.text(v - (0.25 if v == -1 else (0.12 if v < 0 else 0)), -0.12, s, ha='center', va='top')
ax.text(0.08, 2, '2', ha='left', va='center'); ax.text(0.08, 1.07, '1', ha='left', va='bottom')
ax.text(-0.08, -1.12, '-1', ha='right', va='top')
ax.text(1.0, 1.8, 'y=f(x)', ha='left', va='center')
save(fig, 'fig_L49')
