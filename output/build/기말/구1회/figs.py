exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
import os
os.chdir('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/g1')
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


# ---- 1회 12번 : y=-x^3+x, y=x^3-x^2, y=ax(1-x) (a=1/2) ----
fig, ax = plt.subplots(figsize=(2.6, 1.8))
axes(ax, (-0.11, 1.19), (-0.3, 0.56), dx=0.02, dy=0.02)
set_O(ax, 0.015, -0.02, ha='left')
xs = np.linspace(-0.08, 1.07, 300); ax.plot(xs, -xs**3 + xs, 'k', lw=1.1)
xs = np.linspace(-0.08, 1.07, 300); ax.plot(xs, xs**3 - xs**2, 'k', lw=1.1)
xs = np.linspace(-0.06, 1.07, 300); ax.plot(xs, 0.5*xs*(1 - xs), 'k', lw=0.6)
ax.text(0.985, -0.025, '1', ha='right', va='top')
lab(ax, 0.66, 0.47, [('y=-x', 'eq'), ('3', 'sup'), ('+x', 'eq')])
lab(ax, 0.5, 0.2, [('y=ax(1-x)', 'eq')], ha='center', size=9.5)
lab(ax, 0.62, -0.245, [('y=x', 'eq'), ('3', 'sup'), ('-x', 'eq'), ('2', 'sup')])
save(fig, 'fig_g1_12')
