# 3회 10번 그림: 곡선 y=f(x)=x^3+4x^2-24x-20 과 곡선 y=x^2+a (그림은 a=-30인 한 경우, 모양 확인용, 수치는 본문 식에서)
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
f = lambda x: x**3 + 4 * x**2 - 24 * x - 20
g = lambda x: x**2 - 30
fig, ax = K.new((-8.4, 6.6), (-62, 92), size=(2.3, 2.2), dx=0.12, dy=0.12, origin=False)
K.label(ax, 0.2, -2.5, 'O', 'left', 'top')
K.curve(ax, f, -7.25, 4.75, n=600)
K.curve(ax, g, -8.2, 6.2, n=400)
K.label(ax, -4.6, 82, 'y=f(x)', 'center', 'bottom', size=10)
K.label(ax, 6.4, 8, 'y=x^2+a'.replace('^2', '²'), 'right', 'top', size=10)
K.save(fig, out)
