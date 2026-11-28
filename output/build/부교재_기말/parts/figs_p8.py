exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
import os
os.chdir('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb3/parts')
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy
from matplotlib.patches import FancyArrowPatch

EQF = F + 'hyhwpeq_web.ttf'
EXTRA = {'+': chr(0xE048), ',': chr(0xE052), '|': chr(0xE04D), "'": chr(0xE050)}
def P(s, it=True):
    return ''.join(EXTRA.get(c, None) or pua(c, it) for c in s)
def fp(size): return FontProperties(fname=EQF, size=size)
TIT = FontProperties(family='Tinos', style='italic', size=11)

def lab(ax, x, y, pieces, ha='left', size=11):
    """Label built from pieces drawn left to right, vertically centred on (x, y).
    kinds: 'eq' equation font, 'rm' roman eq font (no italics), 'sup', 'sub', 'it' (Tinos italic), 'frac' ((num, den))."""
    fig = ax.figure; r = fig._get_renderer(); k72 = 72 / fig.dpi
    items = []
    for s, kd in pieces:
        if kd == 'frac':
            a = _text(ax, 0, 0, P(s[0]), fontproperties=fp(size * 0.8), ha='center', va='center')
            b = _text(ax, 0, 0, P(s[1]), fontproperties=fp(size * 0.8), ha='center', va='center')
            w = max(a.get_window_extent(r).width, b.get_window_extent(r).width) * k72 + 1.6
            items.append((kd, (a, b), w))
        else:
            if kd == 'it': t = _text(ax, 0, 0, s, fontproperties=FontProperties(family='Tinos', style='italic', size=size), ha='left', va='center')
            elif kd in ('sup', 'sub'): t = _text(ax, 0, 0, P(s), fontproperties=fp(size * 0.64), ha='left', va='center')
            elif kd == 'rm': t = _text(ax, 0, 0, P(s, False), fontproperties=fp(size), ha='left', va='center')
            else: t = _text(ax, 0, 0, P(s), fontproperties=fp(size), ha='left', va='center')
            items.append((kd, t, t.get_window_extent(r).width * k72 + (0.3 if kd in ('sup', 'sub') else 0)))
    tot = sum(w for _, _, w in items)
    off = {'left': 0, 'center': -tot / 2, 'right': -tot}[ha]
    for kd, t, w in items:
        if kd == 'frac':
            a, b = t; cx = off + w / 2
            a.set_transform(offset_copy(ax.transData, fig=fig, x=cx, y=size * 0.47, units='points')); a.set_position((x, y))
            b.set_transform(offset_copy(ax.transData, fig=fig, x=cx, y=-size * 0.5, units='points')); b.set_position((x, y))
            base = ax.transData.transform((x, y)); inv = ax.transData.inverted()
            p0 = inv.transform((base[0] + (off + 0.5) / k72, base[1] + 0.3 / k72)); p1 = inv.transform((base[0] + (off + w - 0.5) / k72, base[1] + 0.3 / k72))
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k', lw=0.5, solid_capstyle='butt')
        else:
            dy = {'sup': size * 0.38, 'sub': -size * 0.3}.get(kd, 0)
            t.set_transform(offset_copy(ax.transData, fig=fig, x=off, y=dy, units='points')); t.set_position((x, y))
        off += w

def arrow(ax, p_from, p_to, rad=0.3):
    ax.add_patch(FancyArrowPatch(p_from, p_to, arrowstyle='-|>', mutation_scale=5, lw=0.5, color='k',
                                 connectionstyle='arc3,rad=%g' % rad, shrinkA=0, shrinkB=0))
def shade(ax, xs, y1, y2): ax.fill_between(xs, y1, y2, facecolor='#e6e6e6', edgecolor='none', zorder=0)
def save(fig, name):
    fig.savefig(name + '.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)
def set_O(ax, x, y, ha='right', va='top'):
    t = ax.texts[-1]; t.set_position((x, y)); t.set_ha(ha); t.set_va(va)
LW = 1.0
def dash(ax, xs, ys): ax.plot(xs, ys, 'k', lw=0.5, dashes=(2.5, 1.8))

# ---- J46 : y=f'(x)=3x^2+8x+4 (k=-2/3) ----
fig, ax = plt.subplots(figsize=(2.0, 2.3))
axes(ax, (-4.0, 3.4), (-2.3, 6.4), dx=0.2, dy=0.2)
ax.texts[-3].set_visible(False); ax.texts[-2].set_visible(False)   # custom x, y labels
set_O(ax, 0.22, -0.2, ha='left')
xs = np.linspace(-2.97, 0.52, 300); ax.plot(xs, 3*xs**2 + 8*xs + 4, 'k', lw=LW)
ax.text(3.3, -0.25, 'x', ha='right', va='top'); ax.text(-0.15, 6.3, 'y', ha='right', va='top')
lab(ax, 0.3, 6.0, [("y=f'(x)", 'eq')])
ax.text(-2.12, -0.2, 'P', ha='right', va='top')
ax.text(-0.72, 0.18, 'Q', ha='right', va='bottom')
lab(ax, -1.75, -0.5, [('S', 'it'), ('1', 'sub')], size=10)
lab(ax, 0.95, 1.15, [('S', 'it'), ('2', 'sub')], size=10)
ax.plot([0.85, 0.08], [1.15, 1.0], 'k', lw=0.5)
arrow(ax, (0.3, 1.05), (0.05, 1.0), rad=0)
save(fig, 'fig_J46')

# ---- J48 : f=(x-1)(x-5)(x-a), a=6+3sqrt2, vertically scaled ----
a = 6 + 3*np.sqrt(2); s = 0.125
fJ48 = lambda x: s*(x-1)*(x-5)*(x-a)
fig, ax = plt.subplots(figsize=(2.6, 2.2))
axes(ax, (-2.7, 16.0), (-9.3, 7.9), asp='equal', dx=0.5, dy=0.4)
ax.texts[-2].set_visible(False); ax.text(-0.3, 7.8, 'y', ha='right', va='top')
xs = np.linspace(-0.12, 11.05, 400); ax.plot(xs, fJ48(xs), 'k', lw=LW)
for lo, hi in [(0, 1), (1, 5), (5, a)]:
    xx = np.linspace(lo, hi, 100); shade(ax, xx, fJ48(xx), 0)
ax.text(1.25, -0.35, 'P', ha='left', va='top'); ax.text(4.85, -0.35, 'Q', ha='right', va='top')
ax.text(a + 0.2, -0.35, 'R', ha='left', va='top')
lab(ax, 11.3, 6.3, [('y=f(x)', 'eq')])
lab(ax, 2.1, 1.6, [('S', 'it'), ('2', 'sub')], size=10)
lab(ax, 7.3, -2.6, [('S', 'it'), ('3', 'sub')], size=10)
lab(ax, 1.3, -4.3, [('S', 'it'), ('1', 'sub')], size=10)
arrow(ax, (1.7, -3.5), (0.5, -1.7), rad=0.35)
save(fig, 'fig_J48')

# ---- J50 : y=x^2+3, y=-x^2/5+3, x=2 ----
fig, ax = plt.subplots(figsize=(2.4, 2.35))
axes(ax, (-5.8, 5.9), (-1.0, 10.0), dx=0.3, dy=0.3)
set_O(ax, -0.15, -0.25)
xs = np.linspace(-2.65, 2.65, 300); ax.plot(xs, xs**2 + 3, 'k', lw=LW)
xs = np.linspace(-4.3, 4.3, 300); ax.plot(xs, -xs**2/5 + 3, 'k', lw=LW)
ax.plot([2, 2], [-1.0, 10.0], 'k', lw=0.8)
xx = np.linspace(0, 2, 100); shade(ax, xx, xx**2 + 3, -xx**2/5 + 3)
lab(ax, -2.75, 9.4, [('y=x', 'eq'), ('2', 'sup'), ('+3', 'eq')], ha='right')
lab(ax, -2.75, 2.75, [('y=-', 'eq'), (('1', '5'), 'frac'), ('x', 'eq'), ('2', 'sup'), ('+3', 'eq')], ha='right')
ax.text(2, -1.25, 'x=2', ha='center', va='top')
save(fig, 'fig_J50')

# ---- J57 : y=-x^4+x, y=x^4-x^3, y=(3/4)x(1-x) ----
fig, ax = plt.subplots(figsize=(2.6, 1.8))
axes(ax, (-0.11, 1.19), (-0.25, 0.6), dx=0.02, dy=0.02)
set_O(ax, 0.015, -0.02, ha='left')
xs = np.linspace(-0.08, 1.07, 300); ax.plot(xs, -xs**4 + xs, 'k', lw=1.1)
xs = np.linspace(-0.08, 1.07, 300); ax.plot(xs, xs**4 - xs**3, 'k', lw=1.1)
xs = np.linspace(-0.06, 1.07, 300); ax.plot(xs, 0.75*xs*(1 - xs), 'k', lw=0.6)
ax.text(0.985, -0.025, '1', ha='right', va='top')
lab(ax, 0.42, 0.535, [('y=-x', 'eq'), ('4', 'sup'), ('+x', 'eq')])
lab(ax, 0.36, 0.245, [('y=ax(1-x)', 'eq')])
lab(ax, 0.58, -0.185, [('y=x', 'eq'), ('4', 'sup'), ('-x', 'eq'), ('3', 'sup')])
save(fig, 'fig_J57')

# ---- J58 : f=x^3-7x+6, segment OP (y=4x) ----
fJ58 = lambda x: x**3 - 7*x + 6
q = (-3 + np.sqrt(17)) / 2
fig, ax = plt.subplots(figsize=(1.45, 3.2))
axes(ax, (-2.5, 4.5), (-1.7, 14.6), dx=0.3, dy=0.3)
set_O(ax, -0.15, -0.3)
xs = np.linspace(-2.05, 3.17, 400); ax.plot(xs, fJ58(xs), 'k', lw=LW)
ax.plot([0, 3], [0, 12], 'k', lw=LW)
dash(ax, [0, 3], [12, 12]); dash(ax, [3, 3], [12, 0])
xx = np.linspace(0, q, 60); shade(ax, xx, fJ58(xx), 4*xx)
xx = np.linspace(q, 3, 200); shade(ax, xx, 4*xx, fJ58(xx))
ax.text(3, -0.3, '3', ha='center', va='top')
ax.text(3.15, 12.1, 'P', ha='left', va='center')
lab(ax, 0.68, 4.05, [('Q', 'rm')], ha='center', size=10)
lab(ax, 1.55, 3.5, [('B', 'it')], ha='center', size=10)
lab(ax, -0.55, 1.0, [('A', 'it')], ha='center', size=10)
arrow(ax, (-0.3, 1.1), (0.2, 1.75), rad=0.4)
lab(ax, 3.4, 13.8, [('y=f(x)', 'eq')])
save(fig, 'fig_J58')

# ---- J61 : f=(4/3)x(x-2)(x-3) ----
fJ61 = lambda x: 4/3*x*(x-2)*(x-3)
fig, ax = plt.subplots(figsize=(2.4, 2.1))
axes(ax, (-0.75, 3.85), (-1.0, 3.1), dx=0.06, dy=0.06)
set_O(ax, -0.04, -0.06)
xs = np.linspace(-0.1, 3.43, 400); ax.plot(xs, fJ61(xs), 'k', lw=LW)
xx = np.linspace(0, 3, 300); shade(ax, xx, fJ61(xx), 0)
ax.text(1.96, -0.06, 'P', ha='right', va='top'); ax.text(3.04, -0.06, 'Q', ha='left', va='top')
lab(ax, 0.92, 1.1, [('A', 'it')], ha='center')
lab(ax, 2.55, -0.36, [('B', 'it')], ha='center')
lab(ax, 3.5, 2.9, [('y=f(x)', 'eq')])
save(fig, 'fig_J61')

# ---- J62 : y=x^3/4+x/2, y=-4x/3+2, x=2 ----
g = lambda x: x**3/4 + x/2; L = lambda x: -4*x/3 + 2
x0 = [r.real for r in np.roots([0.25, 0, 0.5 + 4/3, -2]) if abs(r.imag) < 1e-9][0]
fig, ax = plt.subplots(figsize=(2.45, 2.2))
axes(ax, (-2.25, 4.0), (-1.35, 4.25), dx=0.1, dy=0.1)
set_O(ax, 0.05, -0.1, ha='left')
xs = np.linspace(-1.25, 2.27, 300); ax.plot(xs, g(xs), 'k', lw=LW)
ax.plot([-1.53, 2.33], [L(-1.53), L(2.33)], 'k', lw=LW)
ax.plot([2, 2], [-1.35, 4.1], 'k', lw=0.8)
xx = np.linspace(0, x0, 100); shade(ax, xx, L(xx), g(xx))
xx = np.linspace(x0, 2, 100); shade(ax, xx, g(xx), L(xx))
lab(ax, 0.47, 0.8, [('A', 'it')], ha='center'); lab(ax, 1.62, 0.8, [('B', 'it')], ha='center')
lab(ax, -0.72, 2.75, [('y=mx+2', 'eq')], ha='right')
lab(ax, 2.3, 3.7, [('y=', 'eq'), (('1', '4'), 'frac'), ('x', 'eq'), ('3', 'sup'), ('+', 'eq'), (('1', '2'), 'frac'), ('x', 'eq')])
ax.text(2, -1.45, 'x=2', ha='center', va='top')
save(fig, 'fig_J62')

# ---- J64 : f=3x^2-7x+2, y=(x-2)/3, x=k=8/3 ----
fJ64 = lambda x: 3*x**2 - 7*x + 2; Lk = lambda x: (x - 2)/3; k = 8/3
fig, ax = plt.subplots(figsize=(2.4, 2.7))
axes(ax, (-2.3, 5.5), (-2.4, 6.6), dx=0.15, dy=0.15)
set_O(ax, -0.1, -0.12)
xs = np.linspace(-0.515, 2.85, 300); ax.plot(xs, fJ64(xs), 'k', lw=LW)
ax.plot([-2.25, 5.4], [Lk(-2.25), Lk(5.4)], 'k', lw=LW)
ax.plot([k, k], [-2.3, 6.5], 'k', lw=0.8)
xx = np.linspace(0, 4/9, 60); shade(ax, xx, fJ64(xx), Lk(xx))
xx = np.linspace(4/9, 2, 200); shade(ax, xx, Lk(xx), fJ64(xx))
xx = np.linspace(2, k, 100); shade(ax, xx, fJ64(xx), Lk(xx))
lab(ax, -0.62, 4.95, [('y=f(x)', 'eq')], ha='right')
lab(ax, 3.4, 1.65, [('y=', 'eq'), (('1', '3'), 'frac'), ('x-', 'eq'), (('2', '3'), 'frac')])
lab(ax, -0.5, 0.75, [('A', 'it')], ha='center', size=10)
arrow(ax, (-0.3, 0.75), (0.1, 0.4), rad=-0.3)
lab(ax, 1.15, -1.15, [('B', 'it')], ha='center', size=10)
lab(ax, 2.38, 0.95, [('C', 'it')], ha='center', size=10)
ax.text(k, -2.45, 'x=k', ha='center', va='top')
save(fig, 'fig_J64')

# render to PNG for inspection
import pymupdf
os.makedirs('crop8', exist_ok=True)
for n in ['J46', 'J48', 'J50', 'J57', 'J58', 'J61', 'J62', 'J64']:
    d = pymupdf.open('fig_%s.svg' % n); pdf = pymupdf.open('pdf', d.convert_to_pdf())
    pdf[0].get_pixmap(dpi=200).save('crop8/fig_%s.png' % n)
