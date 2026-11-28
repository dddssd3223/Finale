# 12회 18번 그림 (원문 J48 그림을 새로 그림): 삼차곡선 y=f(x)가 x축의 양의 부분과 세 점에서 만나는 모양, 넓이 S1·S2·S3의 자리(회색)
# 모양 확인용: S1은 곡선과 x축, y축 사이, S2·S3은 곡선과 x축 사이의 왼쪽·오른쪽 부분.
# 판정용 수치(x절편의 값, 점 이름)는 그림에 두지 않는다(본문 문장에 있음). 그리는 데 쓴 x절편은 본문의 값과 무관하게 고른 1.3, 3.7, 5.6이다.
# 출력: parts/fig_18.svg (+ 회차 폴더 fig_18.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_18.svg')
r1, r2, r3 = 1.3, 3.7, 5.6
F = lambda x: 0.55 * (x - r1) * (x - r2) * (x - r3)
fig, ax = K.new((-0.9, 6.9), (-15.5, 6.2), size=(2.3, 2.1), dx=0.1, dy=0.1, origin=False)
K.label(ax, -0.12, -0.5, 'O', 'right', 'top')
K.shade(ax, F, 0, r1)
K.shade(ax, F, r1, r2)
K.shade(ax, F, r2, r3)
K.curve(ax, F, -0.07, 6.33)
K.sub(ax, 0.42, -2.6, 'S', '1', 'center', 'center', size=9)
K.sub(ax, 2.45, 1.25, 'S', '2', 'center', 'center', size=9)
K.sub(ax, 4.72, -0.62, 'S', '3', 'center', 'center', size=8)
K.label(ax, 6.05, 3.9, 'y=f(x)', 'right', 'bottom', size=10)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_18.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
