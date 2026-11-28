# 8회 10번 그림 (원문 M7 그림을 변형에 맞게 다시 그림): 곡선 y=f(x)=-x^2+6x+40, 두 직선 x=t, x=2t 사이 회색 칠
# 그림은 t=2.4인 한 경우(모양 확인용). 수치는 본문 식에만 둔다. 정의역 [0, 10]: (0, 40)에서 시작해 x=10에서 x축과 만난다.
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
F = lambda x: -x**2 + 6 * x + 40
t = 2.4
fig, ax = K.new((-1.6, 12.0), (-7, 56), size=(2.4, 2.2), dx=0.1, dy=0.1)
K.shade(ax, F, t, 2 * t)
K.curve(ax, F, 0, 10)
K.line(ax, [t, t], [0, F(t)])
K.line(ax, [2 * t, 2 * t], [0, F(2 * t)])
K.label(ax, t, -1.5, 't', 'center', 'top', size=10)
K.label(ax, 2 * t, -1.5, '2t', 'center', 'top', size=10)
K.label(ax, 8.9, 32, 'y=f(x)', 'left', 'center', size=10)
K.save(fig, out)
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
