# 12회 10번 그림 (원문 J10 그림을 새로 그림): 삼차곡선 y=2x^3+ax^2-9x-5 와 포물선 y=x^2+5x+7, 둘러싸인 두 부분(회색)
# 모양 확인용: 두 곡선이 세 점에서 만나고 둘러싸인 부분이 두 개 생김. 판정용 수치(a의 값, 교점 좌표)는 그림에 두지 않는다(본문 문장에 있음).
# 그리는 데 쓴 값은 a=1 (교점 x=-2, -1, 3). 왼쪽 부분이 좁아 그림에서는 y축 눈금을 좁혀 두 부분이 보이게 했다.
# 출력: parts/fig_10.svg (+ 회차 폴더 fig_10.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_10.svg')
F = lambda x: 2 * x**3 + x**2 - 9 * x - 5
G = lambda x: x**2 + 5 * x + 7
fig, ax = K.new((-3.0, 6.2), (-14.0, 44.0), size=(2.6, 2.2), dx=0.1, dy=0.1, origin=False)
K.label(ax, 0.12, -1.2, 'O', 'left', 'top')
K.shade(ax, F, -2, -1, G)
K.shade(ax, F, -1, 3, G)
K.curve(ax, F, -2.62, 3.25)
K.curve(ax, G, -2.95, 3.75)
K.rich(ax, 2.75, 9.0, [('y=2x', 0), ('3', 1), ('+ax', 0), ('2', 1), ('-9x-5', 0)], 'left', 'center', size=9)
K.rich(ax, 3.9, 40.5, [('y=x', 0), ('2', 1), ('+5x+7', 0)], 'left', 'center', size=9)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_10.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
