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
CX = 497.0
def score(cy, t, size=21):
    x = CX - FONT.text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
# 단답형
oval(95, 157, 11, 14); oval(97, 200, 9, 15); oval(245, 261, 24, 15)
for cy, t in [(157, '3'), (202, '3'), (254, '4'), (294, '10')]: score(cy, t)
# 서술형
check(435, 400, 0.9); score(373, '2')
check(330, 562, 0.9); score(493, '4')
check(440, 700, 0.9); score(652, '4')
score(740.5, '10'); score(769, '20', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
