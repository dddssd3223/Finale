exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
os.chdir('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb3/parts')
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy
plt.rcParams['hatch.linewidth'] = 0.45
PLUS = chr(0xE048)
SM = FontProperties(fname=F + 'hyhwpeq_web.ttf', size=7)
FR = FontProperties(fname=F + 'hyhwpeq_web.ttf', size=8.5)
GRAY = '0.88'
ITF = FontProperties(fname=F + 'buE2poGnedXvwjX-fmE.ttf', size=11)

def IT(ax, x, y, s, **kw):
    # italic capital (area/name labels such as A, B, C, S)
    kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    return _text(ax, x, y, s, fontproperties=ITF, **kw)

def hatch(ax, xs, ylo, yhi, lw=0.45, gap=2.2):
    # 45-degree hatching (in display space) restricted to ylo<=y<=yhi over xs, clipped geometrically
    fig = ax.figure; ax.apply_aspect()
    T = ax.transData; inv = T.inverted()
    lo = T.transform(np.column_stack([xs, ylo])); hi = T.transform(np.column_stack([xs, yhi]))
    X = lo[:, 0]; L = lo[:, 1]; H = hi[:, 1]
    Y0, Y1 = L.min(), H.max(); step = gap * fig.dpi / 72
    c = X.min() - (Y1 - Y0)
    while c < X.max():
        u = np.linspace(0, Y1 - Y0, 600); px = c + u; py = Y0 + u
        ok = (px >= X.min()) & (px <= X.max())
        lo_i = np.interp(px, X, L); hi_i = np.interp(px, X, H)
        ok &= (py >= lo_i) & (py <= hi_i)
        idx = np.where(ok)[0]
        if len(idx):
            runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
            for r_ in runs:
                d = inv.transform([(px[r_[0]], py[r_[0]]), (px[r_[-1]], py[r_[-1]])])
                ax.plot(d[:, 0], d[:, 1], 'k', lw=lw, solid_capstyle='butt')
        c += step

def save(fig, name):
    fig.savefig(name + '.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

def P(s):
    return pua(s).replace('+', PLUS)

def seq(ax, x, y, pieces, ha='left'):
    """Label from pieces placed left to right at data point (x, y) (vertical centre).
    kinds: 'eq' normal, 'sup' raised small, 'sub' lowered small, 'frac' (num, den) small stacked fraction."""
    fig = ax.figure; ax.apply_aspect(); r = fig._get_renderer()
    items = []
    for s, k in pieces:
        if k == 'it':
            t = _text(ax, 0, 0, s, fontproperties=ITF, va='center', ha='left')
            items.append((k, t, t.get_window_extent(r).width * 72 / fig.dpi)); continue
        if k == 'frac':
            tn = _text(ax, 0, 0, P(s[0]), fontproperties=FR, va='bottom', ha='center')
            td = _text(ax, 0, 0, P(s[1]), fontproperties=FR, va='top', ha='center')
            w = max(tn.get_window_extent(r).width, td.get_window_extent(r).width) * 72 / fig.dpi + 1.5
            items.append((k, (tn, td), w))
        else:
            t = _text(ax, 0, 0, P(s), fontproperties=(SM if k in ('sup', 'sub') else EQ), va='center', ha='left')
            items.append((k, t, t.get_window_extent(r).width * 72 / fig.dpi))
    tot = sum(w for _, _, w in items)
    off = -tot if ha == 'right' else (-tot / 2 if ha == 'center' else 0)
    for k, t, w in items:
        if k == 'frac':
            tn, td = t
            tn.set_transform(offset_copy(ax.transData, fig=fig, x=off + w / 2, y=0.6, units='points')); tn.set_position((x, y))
            td.set_transform(offset_copy(ax.transData, fig=fig, x=off + w / 2, y=-0.4, units='points')); td.set_position((x, y))
            base = ax.transData.transform((x, y))
            pts = [(base[0] + (off + 0.4) * fig.dpi / 72, base[1] + 0.3 * fig.dpi / 72),
                   (base[0] + (off + w - 0.4) * fig.dpi / 72, base[1] + 0.3 * fig.dpi / 72)]
            d = ax.transData.inverted().transform(pts)
            ax.plot(d[:, 0], d[:, 1], 'k', lw=0.5, solid_capstyle='butt')
        else:
            dy = 3.6 if k == 'sup' else (-2.6 if k == 'sub' else 0)
            t.set_transform(offset_copy(ax.transData, fig=fig, x=off, y=dy, units='points')); t.set_position((x, y))
        off += w

def lab(ax, x, y, s, ha='left'):
    """Shorthand: '^' and '_' introduce one-char sup/sub, e.g. 'y=x^3+4x^2-3', 'S_1'."""
    pieces = []; buf = ''; i = 0
    while i < len(s):
        ch = s[i]
        if ch in '^_' and i + 1 < len(s):
            if buf: pieces.append((buf, 'eq')); buf = ''
            pieces.append((s[i + 1], 'sup' if ch == '^' else 'sub')); i += 2; continue
        buf += ch; i += 1
    if buf: pieces.append((buf, 'eq'))
    seq(ax, x, y, pieces, ha)

def curve(ax, f, x0, x1, lw=1.0, n=400):
    xs = np.linspace(x0, x1, n); ax.plot(xs, f(xs), 'k', lw=lw)

def drop_O(ax):
    for t in list(ax.texts):
        if t.get_text() == pua('O'): t.remove()

# ---- J2: y=|x^2-1|, A (gray) on [-1,1], B (hatched) on [1,k] ----
fig, ax = plt.subplots(figsize=(1.85, 1.75))
axes(ax, (-1.75, 2.15), (-0.55, 2.75), asp='auto', dx=0.09, dy=0.09)
drop_O(ax)
kk = np.sqrt(3)
f = lambda x: np.abs(x**2 - 1)
xs = np.linspace(-1, 1, 200); ax.fill_between(xs, 0, f(xs), color=GRAY, lw=0)
xs = np.linspace(1, kk, 200); hatch(ax, xs, 0 * xs, f(xs))
curve(ax, f, -1.62, 1.82)
ax.plot([kk, kk], [-0.5, 2.7], 'k', lw=0.7)
ax.text(-1.0, -0.08, '-1', ha='center', va='top'); ax.text(-0.25, -0.08, 'O', ha='center', va='top')
ax.text(1.0, -0.08, '1', ha='center', va='top'); ax.text(kk - 0.13, -0.08, 'k', ha='center', va='top')
IT(ax, -0.18, 0.38, 'A'); IT(ax, 1.52, 0.45, 'B', bbox=dict(fc='white', ec='none', pad=0.3))
ax.text(-1.15, 2.7, 'y=f(x)', ha='center', va='center')
save(fig, 'fig_J2')

# ---- J6: cubic through a,0,b; areas A, B, C; vertical line x=c ----
fig, ax = plt.subplots(figsize=(1.9, 1.6))
axes(ax, (-1.45, 2.05), (-1.2, 2.25), asp='auto', dx=0.07, dy=0.1)
drop_O(ax)
a_, b_, c_ = -1.0, 1.1, 1.55
f = lambda x: x * (x - a_) * (x - b_)
xs = np.linspace(a_, c_, 300); ax.fill_between(xs, 0, f(xs), color=GRAY, lw=0)
curve(ax, f, -1.3, c_)
ax.plot([c_, c_], [0, f(c_)], 'k', lw=0.7)
ax.text(a_ - 0.08, 0.04, 'a', ha='right', va='bottom'); IT(ax, -0.55, 0.17, 'A')
ax.text(-0.04, -0.08, 'O', ha='right', va='top'); IT(ax, 0.55, -0.2, 'B')
ax.text(b_ + 0.04, -0.08, 'b', ha='left', va='top'); ax.text(c_ + 0.02, -0.08, 'c', ha='center', va='top')
IT(ax, 1.37, 0.3, 'C')
ax.text(c_ - 0.05, 2.05, 'y=f(x)', ha='center', va='center')
save(fig, 'fig_J6')

# ---- J10: y=x^3+4x^2-3 and y=x^2+x, region between (x from -3 to 1) shaded ----
fig, ax = plt.subplots(figsize=(1.95, 1.75))
axes(ax, (-4.6, 2.8), (-4.8, 7.6), asp='auto', dx=0.13, dy=0.3)
drop_O(ax)
f = lambda x: x**3 + 4 * x**2 - 3
g = lambda x: x**2 + x
xs = np.linspace(-3, 1, 300); ax.fill_between(xs, f(xs), g(xs), color=GRAY, lw=0)
curve(ax, f, -4.07, 1.23); curve(ax, g, -3.22, 2.25)
ax.set_xlim(-4.6, 2.8); ax.set_ylim(-4.8, 7.6)
ax.text(-0.15, 0.25, 'O', ha='right', va='bottom')
lab(ax, 2.3, 7.0, 'y=x^2+x'); lab(ax, 0.15, -3.75, 'y=x^3+4x^2-3')
save(fig, 'fig_J10')

# ---- J14: y=-x^4+2x^3 and y=k(x-2), k=-3/10; A gray (between y-axis and first intersection), B hatched ----
fig, ax = plt.subplots(figsize=(2.25, 1.5))
axes(ax, (-0.6, 3.45), (-0.95, 2.25), asp='auto', dx=0.06, dy=0.09)
drop_O(ax)
K = -0.3
f = lambda x: -x**4 + 2 * x**3
l = lambda x: K * (x - 2)
xs = np.linspace(0, 2, 2001); d = f(xs) - l(xs)
x1 = xs[np.argmax(d > 0)]
xa = np.linspace(0, x1, 100); ax.fill_between(xa, f(xa), l(xa), color=GRAY, lw=0)
xb = np.linspace(x1, 2, 200); hatch(ax, xb, l(xb), f(xb))
curve(ax, f, -0.5, 2.12)
curve(ax, l, -0.5, 2.95)
ax.text(0.04, -0.07, 'O', ha='left', va='top'); ax.text(1.95, -0.07, '2', ha='right', va='top')
IT(ax, 0.13, 0.33, 'A'); IT(ax, 1.12, 0.92, 'B', bbox=dict(fc='white', ec='none', pad=0.3))
lab(ax, 0.62, 2.02, 'y=-x^4+2x^3')
ax.text(2.2, -0.72, 'y=k(x-2)', ha='left', va='center')
save(fig, 'fig_J14')

# ---- J15: square OABC side 3, line y=ax, parabola y=x^2/a (a=3.5); S1 white, S3 dark gray, S2 light gray ----
fig, ax = plt.subplots(figsize=(2.0, 1.7))
axes(ax, (-0.55, 4.4), (-0.6, 3.75), asp='equal', dx=0.1, dy=0.09)
drop_O(ax)
A_ = 3.5
xs = np.linspace(0, 3, 300)
upper = np.minimum(A_ * xs, 3); lower = xs**2 / A_
ax.fill_between(xs, lower, upper, color='0.68', lw=0)
ax.fill_between(xs, 0, lower, color=GRAY, lw=0)
ax.plot([0, 3, 3], [3, 3, 0], 'k', lw=0.7)
curve(ax, lambda x: A_ * x, -0.13, 0.98)
curve(ax, lambda x: x**2 / A_, -0.5, 3.5)
ax.text(0.04, -0.07, 'O', ha='left', va='top'); ax.text(3.0, -0.07, 'A', ha='center', va='top')
ax.text(-0.07, 3.0, 'C', ha='right', va='center'); ax.text(2.95, 3.06, 'B', ha='right', va='bottom')
seq(ax, 0.1, 2.5, [('S','it'),('1','sub')]); seq(ax, 1.05, 1.95, [('S','it'),('3','sub')]); seq(ax, 2.15, 0.6, [('S','it'),('2','sub')])
ax.text(1.0, 3.55, 'y=ax', ha='left', va='center')
seq(ax, 3.3, 3.12, [('y=', 'eq'), (('1', 'a'), 'frac'), ('x', 'eq'), ('2', 'sup')])
save(fig, 'fig_J15')

# ---- J16: f(x)=(x-4)^2, g(x)=-2x+10; S1 (between y-axis and first intersection), S2 lens ----
fig, ax = plt.subplots(figsize=(2.0, 1.85))
axes(ax, (-0.9, 10.2), (-4.6, 17.5), asp='auto', dx=0.2, dy=0.5)
drop_O(ax)
f = lambda x: (x - 4)**2
g = lambda x: -2 * x + 10
r1, r2 = 3 - np.sqrt(3), 3 + np.sqrt(3)
xs = np.linspace(0, r1, 100); ax.fill_between(xs, g(xs), f(xs), color=GRAY, lw=0)
xs = np.linspace(r1, r2, 100); ax.fill_between(xs, f(xs), g(xs), color=GRAY, lw=0)
curve(ax, f, -0.05, 7.95)
curve(ax, g, -1.5, 6.8, lw=0.8)
ax.set_xlim(-0.9, 10.2); ax.set_ylim(-4.6, 17.5)
ax.text(-0.15, -0.4, 'O', ha='right', va='top'); ax.text(4.0, -0.4, '4', ha='center', va='top')
seq(ax, 2.25, 10.7, [('S','it'),('1','sub')]); seq(ax, 3.35, 7.2, [('S','it'),('2','sub')])
ax.annotate('', xy=(0.55, 10.5), xytext=(2.1, 10.9), arrowprops=dict(arrowstyle='-|>', lw=0.5, color='k', mutation_scale=5, connectionstyle='arc3,rad=0.3'))
ax.annotate('', xy=(3.4, 2.4), xytext=(3.75, 6.1), arrowprops=dict(arrowstyle='-|>', lw=0.5, color='k', mutation_scale=5, connectionstyle='arc3,rad=-0.3'))
ax.text(8.1, 16.2, 'y=f(x)', ha='left', va='center')
ax.text(6.95, -3.9, 'y=g(x)', ha='left', va='center')
save(fig, 'fig_J16')

# ---- J17: y=x^3+x^2, y=-x^2+k (k=14/3), x=2; A between y-axis and intersection, B up to x=2 ----
fig, ax = plt.subplots(figsize=(1.75, 2.45))
axes(ax, (-2.7, 3.0), (-2.6, 13.8), asp='auto', dx=0.1, dy=0.35)
drop_O(ax)
K = 14 / 3
f = lambda x: x**3 + x**2
g = lambda x: -x**2 + K
xs = np.linspace(0, 2, 400)
ax.fill_between(xs, np.minimum(f(xs), g(xs)), np.maximum(f(xs), g(xs)), color=GRAY, lw=0)
curve(ax, f, -1.33, 2.12)
curve(ax, g, -2.6, 2.55)
ax.set_xlim(-2.7, 3.0); ax.set_ylim(-2.6, 13.8)
ax.plot([2, 2], [-2.5, 13.7], 'k', lw=0.7)
ax.text(-0.05, -0.3, 'O', ha='right', va='top')
IT(ax, 0.55, 2.75, 'A'); IT(ax, 1.62, 4.3, 'B')
lab(ax, 2.18, 12.6, 'y=x^3+x^2')
lab(ax, -1.75, 3.3, 'y=-x^2+k', ha='right')
ax.text(2.0, -2.75, 'x=2', ha='center', va='top')
save(fig, 'fig_J17')

# ---- J19: f=x^3/4 and its inverse; both lens regions shaded ----
fig, ax = plt.subplots(figsize=(1.75, 1.6))
axes(ax, (-3.2, 4.0), (-3.2, 3.75), asp='equal', dx=0.15, dy=0.15)
drop_O(ax)
f = lambda x: x**3 / 4
g = lambda x: np.cbrt(4 * x)
xs = np.linspace(-2, 2, 400)
ax.fill_between(xs, f(xs), g(xs), color=GRAY, lw=0)
curve(ax, f, -2.3, 2.3)
curve(ax, g, -3.1, 3.1)
ax.text(0.15, -0.12, 'O', ha='left', va='top')
ax.text(0.62, 3.45, 'y=f(x)', ha='left', va='center')
ax.text(2.25, 1.65, 'y=g(x)', ha='left', va='center')
save(fig, 'fig_J19')

# ---- J21: y=2x^2-8 and y=-x^2+6x+1; lens between x=-1 and 3 shaded; line x=k (figure not to scale in the source) ----
fig, ax = plt.subplots(figsize=(2.15, 1.8))
axes(ax, (-3.2, 9.0), (-11.0, 13.6), asp='auto', dx=0.25, dy=0.6)
drop_O(ax)
f = lambda x: 2 * x**2 - 8
g = lambda x: -x**2 + 6 * x + 1
xs = np.linspace(-1, 3, 300); ax.fill_between(xs, f(xs), g(xs), color=GRAY, lw=0)
curve(ax, f, -2.95, 3.12); curve(ax, g, -1.85, 7.2)
ax.set_xlim(-3.2, 9.0); ax.set_ylim(-11.0, 13.6)
ax.plot([1, 1], [-10.8, 13.4], 'k', lw=0.7)
ax.text(-2.05, -0.5, '-2', ha='right', va='top'); ax.text(2.05, -0.5, '2', ha='left', va='top')
ax.text(-0.75, 4.0, 'O', ha='center', va='center')
ax.annotate('', xy=(-0.05, 0.15), xytext=(-0.7, 3.2), arrowprops=dict(arrowstyle='-|>', lw=0.5, color='k', mutation_scale=5, connectionstyle='arc3,rad=0.3'))
ax.text(-2.3, -7.9, '-8', ha='right', va='center')
ax.annotate('', xy=(-0.1, -8.0), xytext=(-2.2, -7.9), arrowprops=dict(arrowstyle='-|>', lw=0.5, color='k', mutation_scale=5, connectionstyle='arc3,rad=0.3'))
lab(ax, 1.25, 12.7, 'y=2x^2-8')
ax.text(1.15, -10.6, 'x=k', ha='left', va='center')
lab(ax, 3.6, -10.6, 'y=-x^2+6x+1')
save(fig, 'fig_J21')

# ---- J22: f=x^3+2x^2+2x-4, inverse g, line y=-x-6 (no shading) ----
fig, ax = plt.subplots(figsize=(2.2, 1.75))
axes(ax, (-9.3, 3.6), (-8.9, 4.7), asp='equal', dx=0.3, dy=0.3)
drop_O(ax)
f = lambda x: x**3 + 2 * x**2 + 2 * x - 4
ts = np.linspace(-1.75, 1.3, 400)
ax.plot(ts, f(ts), 'k', lw=1.0)                  # y=f(x)
tg = np.linspace(-1.9, 1.6, 400)
ax.plot(f(tg), tg, 'k', lw=1.0)                  # y=g(x) (mirror of f in y=x)
curve(ax, lambda x: -x - 6, -8.0, 2.1)
ax.set_xlim(-9.3, 3.6); ax.set_ylim(-8.9, 4.7)
ax.text(-0.25, -0.3, 'O', ha='right', va='top')
ax.text(-6.95, -0.2, '-6', ha='center', va='top')
ax.text(0.25, -6.0, '-6', ha='left', va='center')
ax.text(-6.0, 3.0, 'y=-x-6', ha='center', va='center')
ax.text(1.5, 4.1, 'y=f(x)', ha='left', va='center')
for t in ax.texts:
    if t.get_text() == pua('y'): t.set_position((-0.25, 4.65)); t.set_ha('right')
ax.text(1.5, 2.6, 'y=g(x)', ha='left', va='center')
save(fig, 'fig_J22')
