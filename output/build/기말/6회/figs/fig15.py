# 6회 15번 그림 (원문 J62 그림을 변형에 맞게 다시 그림): 곡선 y=4x^3-6x^2+x+4, 곡선에 접하는 직선 y=mx+2(m=1, 그림에는 y=mx+2로 표기), 직선 x=2
# 직선은 x=1에서 곡선에 접하고 0<x<2에서 곡선이 접선보다 위에 있다. A는 y축 쪽, B는 x=2 쪽. 수치는 본문 식에만 둔다.
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_15.svg')
F = lambda x: 4 * x**3 - 6 * x**2 + x + 4
T = lambda x: x + 2
fig, ax = K.new((-0.45, 2.95), (-1.2, 16.0), size=(2.2, 2.6), dx=0.12, dy=0.1)
K.shade(ax, F, 0, 2, g=T)
K.curve(ax, F, -0.3, 2.1)
K.curve(ax, T, -0.4, 2.6)
K.line(ax, [2, 2], [-0.6, 15.2])
K.rich(ax, 0.24, 3.15, [('A', 0)], 'center', 'center', size=10)
K.rich(ax, 1.72, 6.4, [('B', 0)], 'center', 'center', size=10)
K.label(ax, 2.0, -0.3, '2', 'center', 'top', size=10)
K.label(ax, 2.1, 10.0, 'x=2', 'left', 'center', size=9)
K.label(ax, 2.1, 3.4, 'y=mx+2', 'left', 'top', size=9)
K.rich(ax, 0.92, 14.6, [('y=4x', 0), ('3', 1), ('-6x', 0), ('2', 1), ('+x+4', 0)], 'center', 'center', size=9)
K.save(fig, out)
