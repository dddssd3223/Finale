# 2회 14번 그림: y=f'(x)=3x(x-2), 부분 A(0<=x<=2, x축 아래), 부분 B(2<=x<=k, k=3, x축 위), 직선 x=k 점선
import os, sys, numpy as np
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_14.svg')
fp = lambda x: 3 * x * (x - 2)
fig, ax = K.new((-1.3, 3.9), (-4.6, 11.5), size=(2.2, 2.2), dx=0.12, dy=0.12)
K.shade(ax, fp, 0, 2)
K.shade(ax, fp, 2, 3)
K.curve(ax, fp, -0.95, 3.18, n=600)
K.dash(ax, [3, 3], [0, 9])
K.label(ax, 2.02, -0.55, '2', 'center', 'top', size=10)
K.label(ax, 3.0, -0.55, 'k', 'center', 'top', size=10)
K.label(ax, 1.0, -1.45, 'A', 'center', 'center', size=10, roman=True)
K.label(ax, 2.72, 1.55, 'B', 'center', 'center', size=10, roman=True)
K.label(ax, 3.25, 10.4, "y=f'(x)", 'left', 'center', size=10)
K.save(fig, out)
