# 11회 14번 그림 (원문 J19 그림을 새로 그림): 곡선 y=f(x)=x^3-3x^2+3x+3 과 원점을 지나는 직선 y=mx, 둘러싸인 두 부분(회색)
# 모양 확인용: 직선이 곡선과 세 점에서 만나고 두 부분이 생김. 판정용 수치(교점 좌표, m의 값)는 그림에 두지 않는다(본문 문장에 있음).
# 그리는 데 쓴 값은 m=4 (교점 x=-1, 1, 3)
# 출력: parts/fig_14.svg (+ 회차 폴더 fig_14.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_14.svg')
F = lambda x: (x - 1)**3 + 4
L = lambda x: 4 * x
fig, ax = K.new((-2.0, 4.0), (-11.0, 19.0), size=(2.3, 2.3), dx=0.1, dy=0.1, origin=False)
K.label(ax, 0.12, -0.9, 'O', 'left', 'top')
K.shade(ax, F, -1, 1, L)
K.shade(ax, F, 1, 3, L)
K.curve(ax, F, -1.35, 3.33)
K.curve(ax, L, -1.9, 3.95)
K.label(ax, 3.25, 17.2, 'y=f(x)', 'right', 'center', size=10)
K.label(ax, 3.55, 11.6, 'y=mx', 'left', 'top', size=10)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_14.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
