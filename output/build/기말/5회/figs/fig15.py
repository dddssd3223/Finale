# 5회 15번 그림 (원문 J57 그림을 변형에 맞게 다시 그림): 두 곡선 y=x^4-x^3, y=-2x^4+2x와 곡선 y=ax(1-x) (a=1로 그림, 모양 확인용)
# 두 곡선은 x=0, 1에서만 만나고, 곡선 y=ax(1-x)가 둘러싸인 도형을 위·아래 두 부분으로 나눈다. 수치는 본문 식에만 둔다.
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_15.svg')
a = 1.0
L = lambda x: x**4 - x**3
U = lambda x: -2 * x**4 + 2 * x
H = lambda x: a * x * (1 - x)
fig, ax = K.new((-0.42, 1.62), (-0.5, 1.45), size=(2.3, 1.75), dx=0.12, dy=0.12)
K.shade(ax, U, 0, 1, g=L)
K.curve(ax, U, -0.2, 1.13)
K.curve(ax, L, -0.38, 1.3)
K.curve(ax, H, -0.12, 1.12)
K.label(ax, 1.0, -0.06, '1', 'center', 'top', size=10)
K.rich(ax, 1.33, 0.72, [('y=x', 0), ('4', 1), ('-x', 0), ('3', 1)], 'left', 'center', size=9)
K.rich(ax, 0.86, 1.08, [('y=-2x', 0), ('4', 1), ('+2x', 0)], 'left', 'center', size=9)
K.label(ax, 1.12, -0.36, 'y=ax(1-x)', 'left', 'center', size=9)
K.save(fig, out)
