# 1회 10번 그림: f(x)=3x(x-3)(x-4), 영역 A(0~3, 곡선과 선분 OP), B(3~4, 곡선과 선분 PQ)
import sys, numpy as np
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
f = lambda x: 3*x*(x-3)*(x-4)
fig, ax = K.new((-0.75, 4.75), (-5.2, 21.5), size=(2.0, 2.3), dx=0.16, dy=0.12)
K.shade(ax, f, 0, 3); K.shade(ax, f, 3, 4)
K.curve(ax, f, -0.12, 4.33)
K.label(ax, 3.04, 0.7, 'P', 'left', 'bottom', size=10)
K.label(ax, 3.97, 0.7, 'Q', 'right', 'bottom', size=10)
K.tex(ax, 1.25, 8.5, r'$A$', 'center', 'center', size=10)
K.tex(ax, 3.52, -1.05, r'$B$', 'center', 'center', size=7)
K.label(ax, 4.1, 6.3, 'y=f(x)', 'center', 'bottom', size=10)
K.save(fig, sys.argv[1])
