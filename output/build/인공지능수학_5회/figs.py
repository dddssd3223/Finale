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

def net(name, w, ws=(1.0, 1.0)):
    """2-2-1 다층 퍼셉트론. w = dict(w11,w12,w21,w22,w31,w32) 글자"""
    fig = plt.figure(figsize=(2.9, 1.55)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.9); ax.set_ylim(0, 1.55); ax.axis('off')
    P = {'x1': (0.3, 1.25), 'x2': (0.3, 0.3), 'z1': (1.45, 1.25), 'z2': (1.45, 0.3), 'y': (2.55, 0.78)}
    E = [('x1', 'z1', 'w11', 'top'), ('x2', 'z1', 'w12', 'up'), ('x1', 'z2', 'w21', 'down'), ('x2', 'z2', 'w22', 'bot'),
         ('z1', 'y', 'w31', 'top'), ('z2', 'y', 'w32', 'bot')]
    for a, b, k, pos in E:
        (x0, y0), (x1, y1) = P[a], P[b]
        ax.plot([x0, x1], [y0, y1], color=K, lw=0.8, zorder=1)
        sub = k[1:]
        if pos in ('up', 'down'):      # 교차하는 두 선: 출발 노드 가까이에 붙임
            t = 0.3; mx, my = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            mx += 0.2; dy = 0.07 if pos == 'down' else -0.07
        else:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            dy = {'top': 0.1, 'bot': -0.12}[pos]
            if a.startswith('z'): dy = 0.11 if pos == 'top' else -0.13
        ax.text(mx, my + dy, rf'$w_{{{sub}}}={w[k]}$', ha='center', va='center', fontsize=8.2)
    for k, (x, y) in P.items():
        ax.add_patch(Circle((x, y), 0.17, facecolor='white', edgecolor=K, lw=0.9, zorder=3))
        s = {'x1': r'$x_1$', 'x2': r'$x_2$', 'z1': r'$z_1$', 'z2': r'$z_2$', 'y': r'$y$'}[k]
        ax.text(x, y, s, ha='center', va='center', fontsize=10, zorder=4)
    fig.savefig(name + '.svg', transparent=True); fig.savefig(name + '_chk.png', dpi=200); plt.close(fig)


def flow_quad():
    f = Flow(3.6, 3.4)
    f.node('s', 'term', 1.5, 3.22, 0.6, 0.24, ['시작'])
    f.node('i', 'box', 1.5, 2.8, 1.1, 0.28, [r'$a,\,b,\,c$ 값 입력'])
    f.node('d1', 'dia', 1.5, 2.3, 0.85, 0.36, [r'$a=0\,?$'])
    f.node('d2', 'dia', 1.5, 1.78, 0.85, 0.36, ['(가)'])
    f.node('d3', 'dia', 1.5, 1.26, 0.85, 0.36, ['(나)'])
    f.node('o1', 'doc', 0.38, 0.62, 0.62, 0.3, ['(다)'])
    f.node('o2', 'doc', 1.5, 0.62, 0.62, 0.3, ['(라)'])
    f.node('o3', 'doc', 2.35, 0.62, 0.62, 0.3, ['(마)'])
    f.node('o4', 'doc', 3.18, 0.62, 0.62, 0.3, [r'$x=-\frac{c}{b}$'])
    f.node('e', 'term', 1.5, 0.15, 0.6, 0.24, ['끝'])
    f.arrow([f.P('s', 'b'), f.P('i', 't')]); f.arrow([f.P('i', 'b'), f.P('d1', 't')])
    f.arrow([f.P('d1', 'b'), f.P('d2', 't')], '예', (1.62, 2.06)); f.arrow([f.P('d2', 'b'), f.P('d3', 't')], '예', (1.62, 1.54))
    f.arrow([f.P('d3', 'b'), f.P('o2', 't')], '예', (1.62, 0.95))
    f.arrow([f.P('d1', 'l'), (0.38, 2.3), f.P('o1', 't')], '아니요', (0.75, 2.4))
    f.arrow([f.P('d3', 'r'), (2.35, 1.26), f.P('o3', 't')], '아니요', (2.15, 1.36))
    f.arrow([f.P('d2', 'r'), (3.18, 1.78), f.P('o4', 't')], '아니요', (2.6, 1.88))
    for k in ('o1', 'o3', 'o4'):
        x = f.N[k][0]; f.ax.plot([x, x], [0.45, 0.33], color=K, lw=0.8)
    f.ax.plot([0.38, 3.18], [0.33, 0.33], color=K, lw=0.8)
    f.arrow([f.P('o2', 'b'), f.P('e', 't')])
    f.save('fig_q4')

if __name__ == '__main__':
    net('fig_q8', dict(w11=5, w12=4, w21=1, w22=2, w31=4, w32=-4))
    flow_quad()
