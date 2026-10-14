# -*- coding: utf-8 -*-
"""0회 그림 3개를 실제 시험지(스캔) 실측 좌표대로 다시 그림 (벡터 SVG).
좌표는 모두 쪽 위의 pt 단위: 원점 위치 (ox, oy), 한 칸 u(pt)."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'mathtext.fontset': 'stix', 'font.family': 'STIXGeneral', 'svg.fonttype': 'path'})
LW, AW, DW, R = 1.25, 0.75, 0.6, 2.1     # 그래프·축·점선 굵기(pt), 점 반지름(pt)
GRAY = '#222222'

def canvas(x0, y0, x1, y1, ox, oy, u):
    W, H = x1 - x0, y1 - y0
    fig = plt.figure(figsize=(W / 72, H / 72))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.set_xlim((x0 - ox) / u, (x1 - ox) / u); ax.set_ylim((oy - y1) / u, (oy - y0) / u)
    ax.set_aspect('equal')
    return fig, ax

def axes(ax, xa, xb, ya, yb, u):
    k = dict(arrowstyle='-|>,head_length=0.55,head_width=0.22', lw=AW, color=GRAY, shrinkA=0, shrinkB=0)
    ax.annotate('', (xb, 0), (xa, 0), arrowprops=k); ax.annotate('', (0, yb), (0, ya), arrowprops=k)

def dot(ax, x, y, filled, u):
    ax.add_patch(plt.Circle((x, y), R / u, facecolor=GRAY if filled else 'white', edgecolor=GRAY, lw=0.8, zorder=5))

def lab(ax, x, y, s, size=10, **k):
    ax.text(x, y, s, fontsize=size, ha='center', va='center', color='#111', **k)

def save(fig, name):
    fig.savefig(name + '.svg', transparent=True); plt.close(fig)

# 1번 ------------------------------------------------------------------
def fig0():
    ox, oy, u = 159.0, 403.6, 22.2
    fig, ax = canvas(86, 352, 240, 462, ox, oy, u)
    axes(ax, -3.15, 3.47, -2.5, 2.14, u)
    d = dict(color=GRAY, lw=DW, ls=(0, (3, 2)))
    ax.plot([-1, 0], [1, 1], **d); ax.plot([-1, -1], [1, -2], **d); ax.plot([1, 1], [1, -1], **d)
    ax.plot([0, 1], [-1, -1], **d); ax.plot([-1, 0], [-2, -2], **d)
    g = dict(color=GRAY, lw=LW, solid_capstyle='butt')
    ax.plot([-2.88, -1], [1.76, -2], **g)          # y=-2x-4
    ax.plot([0, 1], [1, 1], **g)
    ax.plot([-1, 0], [0, -1], **g)
    ax.plot([1, 3.5], [-1, 1.5], **g)              # y=x-2
    for x, y, f in [(-1, 1, 1), (0, 1, 0), (1, 1, 1), (-1, 0, 0), (0, -1, 1), (1, -1, 0), (-1, -2, 0)]:
        dot(ax, x, y, f, u)
    P = lambda X, Y: ((X - ox) / u, (oy - Y) / u)
    lab(ax, *P(153.6, 381.5), r'$1$'); lab(ax, *P(126.5, 397.5), r'$-1$'); lab(ax, *P(153.6, 411), r'$\mathrm{O}$')
    lab(ax, *P(177.5, 411.5), r'$1$'); lab(ax, *P(147.5, 429), r'$-1$'); lab(ax, *P(171.5, 448), r'$-2$')
    lab(ax, *P(214.5, 365), r'$y\!=\!f(x)$', 11); lab(ax, *P(233.5, 410.5), r'$x$', 11); lab(ax, *P(153.5, 359), r'$y$', 11)
    save(fig, 'fig0')

# 15번 -----------------------------------------------------------------
def fig1():
    ox, oy, u = 123.75, 303.75, 24.2
    fig, ax = canvas(72, 250, 248, 416, ox, oy, u)
    axes(ax, -2.05, 4.96, -4.55, 2.12, u)
    f = lambda x: x**3 - 2 * x**2 - 2 * x
    xs = np.linspace(-1.5, 3.2, 600); ys = f(xs); m = (ys >= -4.55) & (ys <= 2.12)
    g = dict(color=GRAY, lw=LW)
    ax.plot(xs[m], ys[m], **g)
    ax.plot([-1.03, 2.27], [2.06, -4.54], **g)       # O에서의 접선 y=-2x
    ax.plot([1.70, 5.01], [-4.6, 2.02], **g)         # A에서의 접선 y=2x-8
    for x, y in [(0, 0), (2, -4), (4, 0)]:
        ax.add_patch(plt.Circle((x, y), 1.6 / u, color=GRAY, zorder=5))
    P = lambda X, Y: ((X - ox) / u, (oy - Y) / u)
    lab(ax, *P(130.5, 299), r'$\mathrm{O}$', 11); lab(ax, *P(223.5, 312.5), r'$\mathrm{B}$', 11)
    lab(ax, *P(181, 401), r'$\mathrm{A}$', 11); lab(ax, *P(167.5, 270.5), r'$y=f(x)$', 11.5)
    lab(ax, *P(241.5, 310), r'$x$', 11.5); lab(ax, *P(129.5, 258.5), r'$y$', 11.5)
    save(fig, 'fig1')

# 17번 -----------------------------------------------------------------
def fig2():
    ox, oy, u = 160.0, 239.0, 24.4
    fig, ax = canvas(60, 167, 262, 276, ox, oy, u)
    axes(ax, -3.95, 3.99, -1.37, 2.83, u)
    g = dict(color=GRAY, lw=LW)
    xs = np.linspace(-3.82, 0, 200); ax.plot(xs, xs**2 / 9 - 1, **g)
    xs = np.linspace(0, 1, 100); ax.plot(xs, 1 - xs**2, **g)
    ax.plot([1, 3.82], [2, -0.82], **g)
    d = dict(color=GRAY, lw=DW, ls=(0, (3, 2)))
    ax.plot([1, 1], [0, 2], **d); ax.plot([0, 1], [2, 2], **d)
    for x, y, fl in [(0, -1, 0), (0, 1, 1), (1, 0, 0), (1, 2, 1)]:
        dot(ax, x, y, fl, u)
    P = lambda X, Y: ((X - ox) / u, (oy - Y) / u)
    lab(ax, *P(154.5, 190), r'$2$'); lab(ax, *P(154.5, 216.5), r'$1$'); lab(ax, *P(171, 263.5), r'$-1$')
    lab(ax, *P(153, 245.5), r'$\mathrm{O}$'); lab(ax, *P(184.5, 247), r'$1$'); lab(ax, *P(236.5, 246.5), r'$3$')
    lab(ax, *P(83, 246.5), r'$-3$'); lab(ax, *P(218, 195), r'$y\!=\!f(x)$', 11)
    lab(ax, *P(255.5, 243.5), r'$x$', 11); lab(ax, *P(157.5, 175), r'$y$', 11)
    save(fig, 'fig2')

if __name__ == '__main__':
    fig0(); fig1(); fig2()
