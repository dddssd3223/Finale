# 13회 10번 그림 (원문 J21 그림을 새로 그림): 두 삼차곡선 y=x^3-4x^2-5x-8, y=x^3-7x^2+7x+7 로 둘러싸인 부분(회색)과 이 부분을 이등분하는 직선 x=k(점선)
# 모양 확인용: 두 곡선이 두 점에서 만나 한 부분을 둘러쌈. 교점 좌표·k의 값은 그림에 두지 않는다(본문 문장에 있음).
# 그리는 데 쓴 값은 교점 x=-1, 5, k=2.
# 출력: parts/fig_10.svg (+ 회차 폴더 fig_10.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
F = lambda x: x**3 - 4 * x**2 - 5 * x - 8
G = lambda x: x**3 - 7 * x**2 + 7 * x + 7
fig, ax = K.new((-2.2, 6.8), (-46.0, 40.0), size=(2.6, 2.3), dx=0.1, dy=0.1)
K.shade(ax, F, -1, 5, G)
K.curve(ax, F, -1.75, 6.25)
K.curve(ax, G, -1.45, 6.55)
K.dash(ax, [2, 2], [-44.0, 34.0])
K.rich(ax, 2.12, -40.0, [('x=k', 0)], 'left', 'center', size=9)
K.rich(ax, 6.0, 40.0, [('y=x', 0), ('3', 1), ('-4x', 0), ('2', 1), ('-5x-8', 0)], 'right', 'bottom', size=8)
K.rich(ax, 6.7, 24.0, [('y=x', 0), ('3', 1), ('-7x', 0), ('2', 1), ('+7x+7', 0)], 'left', 'center', size=8)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_10.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
