# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Polygon, Circle
GL = fm.FontProperties(fname='../../fonts/hcrbatang.ttf')
plt.rcParams.update({'mathtext.fontset': 'stix', 'font.family': 'STIXGeneral', 'svg.fonttype': 'path'})
K = '#111'

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

def flow(name):
    W, H = 2.95, 3.9
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    cx = 1.25
    def rbox(y, txt, w=0.9, h=0.26, round_=False, doc=False):
        if doc:
            xs = [cx - w/2, cx + w/2, cx + w/2, cx - w/2]
            import numpy as np
            t = np.linspace(0, 1, 40)
            bx = list(cx + w/2 - t * w); by = list(y - h/2 + 0.05 * np.sin(t * 2 * np.pi))
            pts = [(cx - w/2, y + h/2), (cx + w/2, y + h/2)] + list(zip([cx + w/2] + bx, [y - h/2] + by))
            ax.add_patch(Polygon(pts, closed=True, facecolor='white', edgecolor=K, lw=0.8))
        else:
            ax.add_patch(FancyBboxPatch((cx - w/2, y - h/2), w, h, boxstyle=f'round,pad=0,rounding_size={h/2 if round_ else 0.0}',
                                        facecolor='white', edgecolor=K, lw=0.8))
        ax.text(cx, y, txt, ha='center', va='center', fontsize=8.6)
    def dia(y, txt, w=1.05, h=0.42):
        ax.add_patch(Polygon([(cx - w/2, y), (cx, y + h/2), (cx + w/2, y), (cx, y - h/2)], closed=True, facecolor='white', edgecolor=K, lw=0.8))
        ax.text(cx, y, txt, ha='center', va='center', fontsize=8.4)
    def arr(x0, y0, x1, y1):
        ax.annotate('', (x1, y1), (x0, y0), arrowprops=dict(arrowstyle='-|>,head_length=0.35,head_width=0.16', lw=0.8, color=K, shrinkA=0, shrinkB=0))
    def line(xs, ys): ax.plot(xs, ys, color=K, lw=0.8)
    lab = lambda x, y, t: ax.text(x, y, t, fontproperties=GL, fontsize=7.4, ha='center', va='center')
    Y = dict(s=3.7, i=3.28, d1=2.72, l=2.08, d2=1.48, p=0.9, e=0.38)
    rbox(Y['s'], '', round_=True); ax.text(cx, Y['s'], '시작', fontproperties=GL, fontsize=8.4, ha='center', va='center')
    ax.patches[-1].set_width(0.6); ax.patches[-1].set_x(cx - 0.3)
    rbox(Y['i'], r'$a\leftarrow2,\ n\leftarrow1$', w=1.1)
    dia(Y['d1'], ''); ax.text(cx, Y['d1'], r'$n$', fontsize=8.6, ha='right', va='center', x=cx - 0.2) if False else None
    ax.text(cx - 0.17, Y['d1'], r'$n$', fontsize=8.8, ha='center', va='center'); ax.text(cx + 0.1, Y['d1'], '은 짝수?', fontproperties=GL, fontsize=7.8, ha='center', va='center')
    # 양쪽 처리 상자
    for x, t in ((0.42, r'$a\leftarrow2a$'), (2.08, r'$a\leftarrow a+3$')):
        ax.add_patch(FancyBboxPatch((x - 0.36, Y['l'] - 0.13), 0.72, 0.26, boxstyle='round,pad=0,rounding_size=0', facecolor='white', edgecolor=K, lw=0.8))
        ax.text(x, Y['l'], t, ha='center', va='center', fontsize=8.6)
    dia(Y['d2'], ''); ax.text(cx, Y['d2'], r'$a>40\,?$', fontsize=8.8, ha='center', va='center')
    rbox(Y['p'], '', doc=True); ax.text(cx - 0.07, Y['p'] + 0.01, r'$a$', fontsize=8.8, ha='center', va='center'); ax.text(cx + 0.17, Y['p'] + 0.01, '를 인쇄', fontproperties=GL, fontsize=7.8, ha='center', va='center')
    rbox(Y['e'], '', round_=True); ax.text(cx, Y['e'], '끝', fontproperties=GL, fontsize=8.4, ha='center', va='center')
    ax.patches[-1].set_width(0.6); ax.patches[-1].set_x(cx - 0.3)
    arr(cx, Y['s'] - 0.13, cx, Y['i'] + 0.13)
    arr(cx, Y['i'] - 0.13, cx, Y['d1'] + 0.21)
    line([cx - 0.525, 0.42], [Y['d1'], Y['d1']]); arr(0.42, Y['d1'], 0.42, Y['l'] + 0.13); lab(0.62, Y['d1'] + 0.1, '아니요')
    line([cx + 0.525, 2.08], [Y['d1'], Y['d1']]); arr(2.08, Y['d1'], 2.08, Y['l'] + 0.13); lab(1.9, Y['d1'] + 0.1, '예')
    jy = Y['d2'] + 0.36
    line([0.42, 0.42], [Y['l'] - 0.13, jy]); line([2.08, 2.08], [Y['l'] - 0.13, jy]); line([0.42, 2.08], [jy, jy])
    arr(cx, jy, cx, Y['d2'] + 0.21)
    arr(cx, Y['d2'] - 0.21, cx, Y['p'] + 0.13); lab(cx + 0.14, Y['d2'] - 0.32, '예')
    # 아니요: n <- n+1 후 n 짝수 판단으로
    nx = 2.42
    line([cx + 0.525, nx], [Y['d2'], Y['d2']]); lab(1.97, Y['d2'] + 0.1, '아니요')
    ax.add_patch(FancyBboxPatch((nx - 0.3, Y['d2'] - 0.62 - 0.13), 0.6, 0.26, boxstyle='round,pad=0,rounding_size=0', facecolor='white', edgecolor=K, lw=0.8))
    ax.text(nx, Y['d2'] - 0.62, r'$n\leftarrow n+1$', ha='center', va='center', fontsize=8.4)
    arr(nx, Y['d2'], nx, Y['d2'] - 0.62 + 0.13)
    rx = 2.85
    line([nx + 0.3, rx], [Y['d2'] - 0.62, Y['d2'] - 0.62]); line([rx, rx], [Y['d2'] - 0.62, Y['i'] - 0.27])
    arr(rx, Y['i'] - 0.27, cx + 0.02, Y['i'] - 0.27)
    arr(cx, Y['p'] - 0.17, cx, Y['e'] + 0.13)
    fig.savefig(name + '.svg', transparent=True); fig.savefig(name + '_chk.png', dpi=200); plt.close(fig)

if __name__ == '__main__':
    net('fig_q9', dict(w11=3, w12=3, w21=1, w22=2, w31=4, w32=-1))
    net('fig_s3', dict(w11=2, w12=1, w21=1, w22=3, w31=3, w32=-2))
    flow('fig_q10')
