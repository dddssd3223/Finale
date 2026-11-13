# -*- coding: utf-8 -*-
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon, Circle
GL = fm.FontProperties(fname='../../fonts/hcrbatang.ttf')
plt.rcParams.update({'mathtext.fontset': 'stix', 'font.family': 'STIXGeneral', 'svg.fonttype': 'path'})
K = '#111'

class Flow:
    """간단한 순서도: 노드(종류, 중심, 폭, 높이, 글줄들), 화살표(꺾은선)"""
    def __init__(s, W, H):
        s.fig = plt.figure(figsize=(W, H)); s.ax = s.fig.add_axes([0, 0, 1, 1])
        s.ax.set_xlim(0, W); s.ax.set_ylim(0, H); s.ax.axis('off'); s.N = {}
    def txt(s, x, y, t, size=8.4):
        # '$..$'와 한글을 섞은 한 줄: 조각별로 글꼴을 달리해 이어 쓴다
        parts = [p for p in __import__('re').split(r'(\$[^$]+\$)', t) if p]
        widths = []
        for p in parts:
            o = s.ax.text(0, 0, p, fontsize=size, fontproperties=None if p.startswith('$') else GL)
            s.fig.canvas.draw(); bb = o.get_window_extent(); o.remove()
            widths.append(bb.width / s.fig.dpi)
        x0 = x - sum(widths) / 2
        for p, w in zip(parts, widths):
            s.ax.text(x0, y, p, fontsize=size, va='center', ha='left', fontproperties=None if p.startswith('$') else GL); x0 += w
    def node(s, name, kind, x, y, w, h, lines):
        a = s.ax
        if kind in ('box', 'term'):
            a.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=f'round,pad=0,rounding_size={h/2 if kind == "term" else 0}', facecolor='white', edgecolor=K, lw=0.8))
        elif kind == 'dia':
            a.add_patch(Polygon([(x - w/2, y), (x, y + h/2), (x + w/2, y), (x, y - h/2)], closed=True, facecolor='white', edgecolor=K, lw=0.8))
        elif kind == 'doc':
            t = np.linspace(0, 1, 40)
            pts = [(x - w/2, y + h/2), (x + w/2, y + h/2)] + list(zip([x + w/2] + list(x + w/2 - t*w), [y - h/2] + list(y - h/2 + 0.05*np.sin(t*2*np.pi))))
            a.add_patch(Polygon(pts, closed=True, facecolor='white', edgecolor=K, lw=0.8))
        n = len(lines)
        for i, l in enumerate(lines):
            s.txt(x, y + (n - 1) * 0.085 - i * 0.17, l)
        s.N[name] = (x, y, w, h)
    def P(s, name, side):
        x, y, w, h = s.N[name]
        return {'t': (x, y + h/2), 'b': (x, y - h/2), 'l': (x - w/2, y), 'r': (x + w/2, y)}[side]
    def arrow(s, pts, lab=None, lp=None):
        xs, ys = zip(*pts)
        s.ax.plot(xs[:-1], ys[:-1], color=K, lw=0.8) if len(pts) > 2 else None
        s.ax.annotate('', pts[-1], pts[-2], arrowprops=dict(arrowstyle='-|>,head_length=0.35,head_width=0.16', lw=0.8, color=K, shrinkA=0, shrinkB=0))
        if len(pts) > 2: s.ax.plot(xs[-2:], ys[-2:], color=K, lw=0.8, alpha=0)
        if lab: s.ax.text(lp[0], lp[1], lab, fontproperties=GL, fontsize=7.4, ha='center', va='center')
    def save(s, name):
        s.fig.savefig(name + '.svg', transparent=True); s.fig.savefig(name + '_chk.png', dpi=200); plt.close(s.fig)

def flow_m10():
    f = Flow(2.3, 3.75); c = 1.0
    f.node('s', 'term', c, 3.55, 0.6, 0.26, ['시작'])
    f.node('i', 'box', c, 3.05, 0.85, 0.42, [r'$a\leftarrow0$', r'$n\leftarrow0$'])
    f.node('n', 'box', c, 2.4, 0.85, 0.3, [r'$n\leftarrow n+1$'])
    f.node('a', 'box', c, 1.85, 0.85, 0.3, [r'$a\leftarrow a+n$'])
    f.node('d', 'dia', c, 1.25, 1.0, 0.44, [r'$n>2\,?$'])
    f.node('p', 'doc', c, 0.68, 0.9, 0.3, [r'$a$를 출력'])
    f.node('e', 'term', c, 0.2, 0.6, 0.26, ['끝'])
    f.arrow([f.P('s', 'b'), f.P('i', 't')]); f.arrow([f.P('i', 'b'), f.P('n', 't')]); f.arrow([f.P('n', 'b'), f.P('a', 't')])
    f.arrow([f.P('a', 'b'), f.P('d', 't')]); f.arrow([f.P('d', 'b'), f.P('p', 't')], '예', (c + 0.12, 0.96)); f.arrow([f.P('p', 'b'), (c, 0.33)])
    rx = 1.95; yy = 2.66
    f.arrow([f.P('d', 'r'), (rx, 1.25), (rx, yy), (c, yy)], '아니요', (1.75, 1.36))
    f.save('fig_q10')

def flow_s13():
    f = Flow(3.4, 4.0); c = 1.65
    f.node('s', 'term', c, 3.8, 0.6, 0.26, ['시작'])
    f.node('i', 'box', c, 3.3, 0.85, 0.42, [r'$a\leftarrow1$', r'$b\leftarrow1$'])
    f.node('d', 'dia', c, 2.62, 1.1, 0.46, [r'$a$가 홀수?'])
    f.node('L', 'box', 0.55, 1.95, 0.95, 0.4, [r'$b\leftarrow b+\frac{a-1}{2}$'])
    f.node('M', 'box', c, 1.95, 0.85, 0.4, [r'$b\leftarrow b+\frac{a}{2}$'])
    f.node('q', 'dia', c, 1.25, 1.0, 0.44, [r'$b=m\,?$'])
    f.node('R', 'box', 2.85, 1.95, 0.8, 0.3, [r'$a\leftarrow a+1$'])
    f.node('p', 'doc', c, 0.68, 0.9, 0.3, [r'$a$를 인쇄'])
    f.node('e', 'term', c, 0.2, 0.6, 0.26, ['끝'])
    f.arrow([f.P('s', 'b'), f.P('i', 't')]); f.arrow([f.P('i', 'b'), f.P('d', 't')])
    f.arrow([f.P('d', 'l'), (0.55, 2.62), f.P('L', 't')], '예', (0.8, 2.72))
    f.arrow([f.P('d', 'b'), f.P('M', 't')], '아니요', (c + 0.25, 2.3))
    jy = 1.6
    f.ax.plot([0.55, 0.55, c], [1.75, jy, jy], color=K, lw=0.8)
    f.arrow([f.P('M', 'b'), f.P('q', 't')])
    f.arrow([f.P('q', 'b'), f.P('p', 't')], '예', (c + 0.12, 0.96)); f.arrow([f.P('p', 'b'), (c, 0.33)])
    f.arrow([f.P('q', 'r'), (2.85, 1.25), f.P('R', 'b')], '아니요', (2.4, 1.36))
    yy = 2.98
    f.arrow([f.P('R', 't'), (2.85, yy), (c, yy)])
    f.save('fig_q11')

def flow_s5():
    f = Flow(2.9, 3.3); c = 1.0
    f.node('s', 'term', c, 3.1, 0.6, 0.26, ['시작'])
    f.node('i', 'box', c, 2.6, 0.85, 0.42, [r'$a\leftarrow0$', r'$b\leftarrow m$'])
    f.node('d', 'dia', c, 1.8, 1.0, 0.46, [r'$b\geq n\,?$'])
    f.node('R', 'box', 2.3, 1.8, 0.95, 0.42, [r'$a\leftarrow a+1$', r'$b\leftarrow b-n$'])
    f.node('p', 'doc', c, 1.05, 1.0, 0.3, [r'$(a,\,b)$를 인쇄'])
    f.node('e', 'term', c, 0.45, 0.6, 0.26, ['끝'])
    f.arrow([f.P('s', 'b'), f.P('i', 't')]); f.arrow([f.P('i', 'b'), f.P('d', 't')])
    f.arrow([f.P('d', 'r'), f.P('R', 'l')], '예', (1.66, 1.9))
    f.arrow([f.P('R', 't'), (2.3, 2.22), (c, 2.22)])
    f.arrow([f.P('d', 'b'), f.P('p', 't')], '아니요', (c + 0.22, 1.42)); f.arrow([f.P('p', 'b'), (c, 0.58)])
    f.save('fig_s3')

def net_xor():
    fig = plt.figure(figsize=(3.2, 1.6)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 3.2); ax.set_ylim(0, 1.6); ax.axis('off')
    P = {'x1': (0.3, 1.25), 'x2': (0.3, 0.32), 's1': (1.45, 1.25), 's2': (1.45, 0.32), 's3': (2.45, 0.78)}
    E = [('x1', 's1', '2', (0.85, 1.36)), ('x2', 's1', '2', (1.04, 1.12)), ('x1', 's2', r'$-1$', (1.04, 0.45)), ('x2', 's2', r'$-3$', (0.85, 0.2)),
         ('s1', 's3', '0.5', (2.02, 1.13)), ('s2', 's3', r'$w$', (2.02, 0.43))]
    for a, b, t, (lx, ly) in E:
        (x0, y0), (x1, y1) = P[a], P[b]; ax.plot([x0, x1], [y0, y1], color=K, lw=0.8)
        ax.text(lx, ly, t if t.startswith('$') else f'${t}$', fontsize=8.6, ha='center', va='center')
    lab = {'x1': r'$x_1$', 'x2': r'$x_2$', 's1': r'$s_1\,|\,f$', 's2': r'$s_2\,|\,g$', 's3': r'$s_3\,|\,h$'}
    for k, (x, y) in P.items():
        r = 0.17 if k.startswith('x') else 0.22
        ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor=K, lw=0.9, zorder=3))
        ax.text(x, y, lab[k], ha='center', va='center', fontsize=8.6 if k.startswith('x') else 7.6, zorder=4)
    ax.annotate('', (3.12, 0.78), (2.67, 0.78), arrowprops=dict(arrowstyle='-|>,head_length=0.35,head_width=0.16', lw=0.8, color=K))
    ax.text(2.9, 0.92, '출력값', fontproperties=GL, fontsize=7.4, ha='center')
    fig.savefig('fig_s5.svg', transparent=True); fig.savefig('fig_s5_chk.png', dpi=200); plt.close(fig)

if __name__ == '__main__':
    flow_m10(); flow_s13(); flow_s5(); net_xor()
