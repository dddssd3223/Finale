# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시 (7회)
import pymupdf, math, random
random.seed(11)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('in/scan.pdf')
doc = pymupdf.open()
SP = 1   # 2쪽이 서답형 답안지
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
CX = 494.6
def score(cy, t, size=21):
    x = CX - FONT.text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
# 단답형
oval(118, 171, 14, 11); oval(128, 209, 20, 22)
slash(110, 262, 138, 238); write(150, 258, '정답 11', 13)
for cy, t in [(166.8, '3'), (210.3, '3'), (260.8, '0'), (299.5, '6')]: score(cy, t)
# 서술형 (1)
check(60, 400); score(375.5, '2')
# 서술형 (2): (1)의 조건과 합친 범위 없음
check(452, 524, 0.85)
write(68, 541, '(1)의 p의 범위와 합친', 10.5); write(68, 553, '최종 범위 없음  -1', 10.5)
score(492, '3')
# 서술형 (3): p=-5 배제 근거 없음
under(60, 152, 616)
write(70, 708, '밑줄 범위에 p=-5도 있음: (1)의 조건으로', 10.5); write(70, 720, '배제하는 근거 없음  -1', 10.5)
check(458, 700, 0.9)
score(647, '3')
score(734, '8'); score(762.5, '14', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
