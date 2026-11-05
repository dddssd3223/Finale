# 2회 9번 그림: f(x)=(x-1)(x-2)(x+4), 선분 OP (P(3,14)), Q는 OP와 곡선의 다른 교점. A(0~xQ, 곡선과 y축·OQ), B(xQ~3, 곡선과 PQ)
import sys, numpy as np
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
f = lambda x: (x-1)*(x-2)*(x+4)
line = lambda x: 14*x/3
xq = -2 + np.sqrt(20/3)
fig, ax = K.new((-0.75, 3.75), (-4.5, 25.5), size=(1.75, 2.6), dx=0.2, dy=0.12)
K.shade(ax, f, 0, xq, g=line); K.shade(ax, line, xq, 3, g=f)
K.curve(ax, f, -0.42, 3.32)
K.line(ax, [0, 3], [0, 14], lw=K.LW)
K.dash(ax, [3, 3], [14, 0])
K.label(ax, 3.0, -0.9, '3', 'center', 'top', size=10)
K.label(ax, 3.1, 14.0, 'P', 'left', 'top', size=10)
K.label(ax, xq + 0.06, line(xq) + 0.9, 'Q', 'left', 'bottom', size=10)
K.tex(ax, 0.17, 4.0, r'$A$', 'center', 'center', size=8)
K.tex(ax, 1.95, 5.0, r'$B$', 'center', 'center', size=10)
K.label(ax, 3.05, 21.0, 'y=f(x)', 'right', 'center', size=10)
K.save(fig, sys.argv[1])
