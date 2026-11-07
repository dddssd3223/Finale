# 3회 10번 그림: y=h(x)=x^3+3x^2-24x-20 (극대 (-4, 60), 극소 (2, -48), y절편 -20)와 수평선 y=a (모양 확인용, 수치는 본문 식에서)
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
h = lambda x: x**3 + 3 * x**2 - 24 * x - 20
fig, ax = K.new((-8.2, 7.8), (-62, 82), size=(2.3, 2.2), dx=0.12, dy=0.12, origin=False)
K.label(ax, 0.2, -2.5, 'O', 'left', 'top')
K.curve(ax, h, -7.05, 5.45, n=600)
K.line(ax, [-8.0, 7.3], [25, 25])
K.label(ax, -4.0, 64, 'y=h(x)', 'center', 'bottom', size=10)
K.label(ax, 7.3, 28, 'y=a', 'right', 'bottom', size=10)
K.save(fig, out)
