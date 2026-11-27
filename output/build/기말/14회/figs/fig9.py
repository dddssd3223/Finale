# 14회 9번 그림 (원문 J52에 그림 없음 → 새로 그림): 곡선 y=x^2-5x, 직선 y=3x, 점 A를 지나는 직선, 곡선과 그 직선으로 둘러싸인 부분(회색)
# 모양 확인용: 곡선과 직선 y=3x가 원점 O와 점 A에서 만나고, A를 지나는 다른 직선이 곡선과 한 점에서 더 만남.
# 기울기·교점 좌표·넓이는 그림에 두지 않는다(수치는 본문 문장에 있음).
# 그리는 데 쓴 값은 A(8, 24), A를 지나는 직선 y=7x-32(곡선과 x=4에서 만남).
# 출력: parts/fig_9.svg (+ 회차 폴더 fig_9.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_9.svg')
F = lambda x: x**2 - 5 * x
L1 = lambda x: 3 * x
L2 = lambda x: 7 * x - 32
fig, ax = K.new((-1.6, 10.2), (-9.0, 33.0), size=(2.5, 2.4), dx=0.1, dy=0.1)
K.shade(ax, F, 4, 8, L2)
K.curve(ax, F, -1.0, 8.75)
K.curve(ax, L1, -1.2, 9.6)
K.curve(ax, L2, 3.3, 9.0)
K.dot(ax, 8, 24)
K.label(ax, 7.55, 25.6, 'A', roman=True, size=10)
K.label(ax, -0.55, -1.7, 'O', roman=True, size=10)
K.rich(ax, 8.85, 13.8, [('y=x', 0), ('2', 1), ('-5x', 0)], 'left', 'center', size=8)
K.rich(ax, 9.7, 29.2, [('y=3x', 0)], 'left', 'center', size=8)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_9.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
