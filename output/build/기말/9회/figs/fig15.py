# 9회 15번 그림 (원문 I65에는 그림 없음, 새로 그림): 최고차항의 계수가 1이고 f'(1)=f'(5)=0인 삼차함수 y=f(x)의 그래프
# 모양 확인용(상수항은 풀이와 무관해 f(x)=x^3-9x^2+15x+9로 그림, 변곡점 (3, 0)). 극점의 x좌표 1, 5만 점선으로 표시하고 수치는 본문 식에만 둔다.
# 출력: parts/fig_15.svg (+ 회차 폴더 fig_15.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_15.svg')
F = lambda x: x**3 - 9 * x**2 + 15 * x + 9
fig, ax = K.new((-1.6, 7.6), (-21, 21), size=(2.4, 2.2), dx=0.1, dy=0.1)
K.curve(ax, F, -0.95, 6.95)
K.dash(ax, [1, 1], [0, F(1)])
K.dash(ax, [5, 5], [0, F(5)])
K.label(ax, 1, -1.2, '1', 'center', 'top', size=10)
K.label(ax, 5, 1.2, '5', 'center', 'bottom', size=10)
K.label(ax, 6.0, 17.5, 'y=f(x)', 'right', 'center', size=10)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_15.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
