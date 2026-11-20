# 7회 15번 그림 (원문 J64 그림을 변형에 맞게 다시 그림): 두 곡선 y=f(x)=4x^2-17x+14, y=g(x)=-2x^2+9x-6, 직선 x=k(k=9/2, 그림에는 k로 표기)
# 두 곡선은 x=1, 10/3에서 만난다. A는 y축 쪽(f가 위), B는 두 교점 사이(g가 위), C는 x=k 쪽(f가 위). 수치는 본문 식에만 둔다.
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_15.svg')
F = lambda x: 4 * x**2 - 17 * x + 14
G = lambda x: -2 * x**2 + 9 * x - 6
k = 4.5
fig, ax = K.new((-0.9, 6.3), (-11.5, 24.5), size=(2.5, 2.7), dx=0.12, dy=0.1)
K.shade(ax, F, 0, k, g=G)
K.curve(ax, F, -0.42, 4.95)
K.curve(ax, G, -0.42, 5.0)
K.line(ax, [k, k], [-10.6, 22.5])
K.rich(ax, 0.3, 4.2, [('A', 0)], 'center', 'center', size=10)
K.rich(ax, 2.2, 2.1, [('B', 0)], 'center', 'center', size=10)
K.rich(ax, 4.12, 4.6, [('C', 0)], 'center', 'center', size=10)
K.label(ax, k + 0.12, -0.5, 'k', 'left', 'top', size=10)
K.label(ax, 4.62, 15.0, 'x=k', 'left', 'center', size=9)
K.label(ax, 4.2, 23.4, 'y=f(x)', 'right', 'center', size=9)
K.label(ax, 5.12, -9.2, 'y=g(x)', 'left', 'center', size=9)
K.save(fig, out)
