# 10회 15번 그림 (원문 M60에는 그림 없음, 새로 그림): 삼차함수 f(x)=x^3+ax^2+bx+1의 도함수 y=f'(x)의 그래프
# 모양 확인용: 아래로 볼록, x축과 만나는 두 점의 x좌표가 모두 음수(본문 문장에 같은 내용이 있음). 수치는 그림에 두지 않는다.
# 그리는 데 쓴 값은 a=9/2, b=4 (f'(x)=3x^2+9x+4, 두 근 약 -2.46, -0.54) — 본문 조건(만나는 점의 x좌표가 모두 음수, ∫_{-1}^{1}f'(x)dx>8)을 만족시킨다.
# 출력: parts/fig_15.svg (+ 회차 폴더 fig_15.svg는 같은 파일을 복사)
import os, sys, shutil
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'parts', 'fig_15.svg')
F = lambda x: 3 * x**2 + 9 * x + 4
fig, ax = K.new((-3.6, 1.4), (-4.2, 9.0), size=(2.4, 2.2), dx=0.1, dy=0.1)
K.curve(ax, F, -3.25, 0.42)
K.label(ax, 0.5, 7.6, "y=f'(x)", 'left', 'center', size=10)
K.save(fig, out)
if len(sys.argv) <= 1:
    shutil.copyfile(out, os.path.join(HERE, '..', 'fig_15.svg'))
if len(sys.argv) > 2: fig.savefig(sys.argv[2], dpi=200)
