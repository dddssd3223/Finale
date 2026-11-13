# 4회 10번 그림 (원문 J17 그림을 변형에 맞게 다시 그림): 두 곡선 y=x^3+x^2, y=-2(x+k)^2+45 (k=3으로 그림, 모양 확인용)
# y축·직선 x=2, 넓이 A(y축 쪽, 포물선이 위)·B(직선 x=2 쪽, 삼차 곡선이 위) 회색 칠. 수치는 본문 식에만 둔다.
import os, sys
import numpy as np
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
k = 3.0
f = lambda x: x**3 + x**2
g = lambda x: -2 * (x + k)**2 + 45
# 교점의 x좌표 t: x^3+x^2+2(x+3)^2-45=0 (0<t<2)
t = [r.real for r in np.roots([1, 3, 12, -27]) if abs(r.imag) < 1e-9 and 0 < r.real < 2][0]
fig, ax = K.new((-1.85, 2.65), (-12, 40), size=(1.8, 2.15), dx=0.12, dy=0.12, origin=False)
K.label(ax, -0.1, -1.2, 'O', 'right', 'top')
K.shade(ax, g, 0, t, g=f)          # A
K.shade(ax, f, t, 2, g=g)          # B
K.curve(ax, f, -1.8, 2.84, n=600, clip_on=False)
K.curve(ax, g, -1.13, 2.2, n=400)
K.line(ax, [2, 2], [-10, 12], lw=0.7)
K.rich(ax, 0.62, 13, [('A', 0)], 'center', 'center', size=11)
K.rich(ax, 1.79, 3.4, [('B', 0)], 'center', 'center', size=9)
K.label(ax, 1.95, -10.8, 'x=2', 'center', 'top', size=10).set_clip_on(False)
K.rich(ax, 2.72, 37.2, [('y=x', 0), ('3', 1), ('+x', 0), ('2', 1)], 'right', 'center', size=10)
K.rich(ax, -0.8, 31.5, [('y=-2(x+k)', 0), ('2', 1), ('+45', 0)], 'right', 'center', size=10)
K.save(fig, out)
