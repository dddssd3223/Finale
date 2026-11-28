# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시 (8회)
import pymupdf, math, random
random.seed(13)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('in/scan.pdf')
doc = pymupdf.open()
SP = 0   # 1쪽이 서답형 답안지
pg = doc.new_page(width=src[SP].rect.width, height=src[SP].rect.height)
pg.show_pdf_page(pg.rect, src, SP, rotate=-src[SP].rotation)
pg.insert_font(fontname='pen', fontfile='pen.ttf')
FONT = pymupdf.Font(fontfile='pen.ttf')
def stroke(pts, w=1.3):
    sh = pg.new_shape(); sh.draw_polyline(pts); sh.finish(color=RED, width=w, closePath=False, lineCap=1, lineJoin=1); sh.commit()
def oval(cx, cy, rx, ry, w=1.2):
    pts = []; a0 = random.uniform(-2.2, -1.6)
    for i in range(46):
        t = a0 + i / 40 * 2 * math.pi
        j = 1 + 0.04 * math.sin(3 * t + 1)
        pts.append((cx + rx * j * math.cos(t), cy + ry * j * math.sin(t)))
    stroke(pts, w)
def check(x, y, s=1.0, w=1.5):
    stroke([(x, y), (x + 4 * s, y + 6 * s), (x + 4.6 * s, y + 6.2 * s), (x + 14 * s, y - 9 * s)], w)
def slash(x0, y0, x1, y1, w=1.6):
    stroke([(x0, y0), ((x0 + x1) / 2 + 1, (y0 + y1) / 2 - 1), (x1, y1)], w)
def under(x0, x1, y, w=1.1):
    stroke([(x0, y), ((x0 + x1) / 2, y + 1.2), (x1, y - 0.5)], w)
def write(x, y, t, size=16, rot=0):
    pg.insert_text((x, y), t, fontname='pen', fontsize=size, color=RED, morph=(pymupdf.Point(x, y), pymupdf.Matrix(rot)) if rot else None)
CX = 503.0
def score(cy, t, size=21):
    x = CX - FONT.text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
def under(x0, x1, y, w=1.1):
    stroke([(x0, y), ((x0 + x1) / 2, y + 1.2), (x1, y - 0.5)], w)
def slash(x0, y0, x1, y1, w=1.6):
    stroke([(x0, y0), ((x0 + x1) / 2 + 1, (y0 + y1) / 2 - 1), (x1, y1)], w)
# 단답형
oval(113, 156, 10, 14); oval(137, 195, 14, 18); oval(145, 246, 12, 15)
for cy, t in [(153, '3'), (198, '3'), (250, '4'), (291, '10')]: score(cy, t)
# 서술형 (1)
check(400, 395, 0.9); score(371, '2')
# 서술형 (2): r=1(중근) 경우 누락
under(330, 478, 488)
write(150, 520, 'r=1(중근)이면 x^2=1의 근이 ±1뿐이라', 10.5); write(150, 532, '불연속점이 b, c 두 개: 이 경우 누락  -1', 10.5)
score(491, '3')
# 서술형 (3): r 계산 오류
oval(247, 654, 22, 12)
write(300, 637, '분자 (x-4)(x-3-r)가 x=-1에서 0: -4-r=0, r=-4 (착안 1점)', 9.5)
slash(460, 736, 482, 714); write(430, 700, '정답 18', 12)
score(653, '1')
score(743, '6'); score(773, '16', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
