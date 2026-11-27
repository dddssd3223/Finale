# 13회 9번 그림 (원문 J50 그림을 새로 그림): 포물선 y=x^2+3 과 y=-x^2/2+ax+3, y축과 직선 x=4 사이의 두 부분(회색)
# 모양 확인용: 두 곡선이 y축 위의 점과 그 오른쪽 한 점에서 만나 위아래가 바뀜. a의 값·교점 좌표는 그림에 두지 않는다(본문 문장에 있음).
# 그리는 데 쓴 값은 a=3 (교점 x=0, 2).
# 출력: parts/fig_9.svg (+ 회차 폴더 fig_9.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_9.svg')
F = lambda x: x**2 + 3
G = lambda x: -0.5 * x**2 + 3 * x + 3
fig, ax = K.new((-1.2, 5.4), (-2.0, 23.0), size=(2.4, 2.3), dx=0.12, dy=0.1)
K.shade(ax, F, 0, 2, G)
K.shade(ax, F, 2, 4, G)
K.curve(ax, F, -1.0, 4.45)
K.curve(ax, G, -0.9, 5.2)
K.line(ax, [4, 4], [-0.0, 21.5])
K.label(ax, 4.0, -0.6, '4', 'center', 'top', size=10)
K.rich(ax, 4.15, 2.6, [('x=4', 0)], 'left', 'center', size=9)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_9.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
