# 12회 14번 그림 (원문 J16 그림을 새로 그림): 포물선 y=f(x)=(x-4)^2, 직선 y=g(x)=-2x+k, y축과의 부분 S1, 두 그래프 사이 S2 (회색)
# 모양 확인용: 직선이 포물선과 y축 오른쪽 두 점에서 만나고 S1, S2가 생김. 판정용 수치(교점 좌표, k의 값)는 그림에 두지 않는다(본문 문장에 있음).
# 그리는 데 쓴 값은 k=10 (교점 x=3±√3)
# 출력: parts/fig_14.svg (+ 회차 폴더 fig_14.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_14.svg')
F = lambda x: (x - 4)**2
G = lambda x: -2 * x + 10
a, b = 3 - 3**0.5, 3 + 3**0.5
fig, ax = K.new((-1.0, 7.4), (-2.5, 19.0), size=(2.0, 2.0), dx=0.1, dy=0.1)
K.shade(ax, F, 0, a, G)
K.shade(ax, G, a, b, F)
K.curve(ax, F, -0.2, 7.0)
K.curve(ax, G, -0.7, 5.6)
K.sub(ax, 0.40, 10.4, 'S', '1', size=8)
K.sub(ax, 3.0, 2.6, 'S', '2', size=9)
K.label(ax, 6.75, 11.0, 'y=f(x)', 'center', 'bottom', size=9)
K.label(ax, -0.75, 11.6, 'y=g(x)', 'right', 'center', size=9)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_14.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
