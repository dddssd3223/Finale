# 3회 18번 그림 (후보 A18 재설계, 원문 J46): y=f'(x)=3(x+p)(x-k), k=-p/3 (S1=S2일 때 PQ:QO=2:1, 모양 확인용, p=3으로 그림)
# 수치(A(-2, f(-2)), 넓이 64/3)는 본문에만 둔다. 그림은 P·Q·O와 S1·S2의 자리만 보여 준다.
# 점 P(-p, 0), Q(k, 0), 원점 O · S1(P~Q, x축 아래), S2(Q~O, x축 위) 회색 칠
import os, sys
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '후보', 'fig_18.svg')
p = 3.0; k = -p / 3
fp = lambda x: 3 * (x + p) * (x - k)
fig, ax = K.new((-4.3, 1.5), (-4.4, 12.2), size=(2.1, 2.3), dx=0.12, dy=0.12)
K.shade(ax, fp, -p, k)
K.shade(ax, fp, k, 0)
K.curve(ax, fp, -3.72, 0.17, n=600)
K.label(ax, -p - 0.1, -0.5, 'P', 'right', 'top', size=10)
K.label(ax, k - 0.1, 0.5, 'Q', 'right', 'bottom', size=10)
K.tex(ax, -2.0, -1.25, r'$S_1$', 'center', 'center', size=10)
K.tex(ax, -0.36, 1.75, r'$S_2$', 'center', 'center', size=9)
K.label(ax, 0.32, 8.6, "y=f'(x)", 'left', 'center', size=10)
K.save(fig, out)
if len(sys.argv) > 2:   # 확인용 PNG
    fig.savefig(sys.argv[2], dpi=200)
