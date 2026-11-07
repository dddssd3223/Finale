# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시 (15회)
import pymupdf, math, random
random.seed(13)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
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
CX = 503.0
def score(cy, t, size=21):
    x = CX - FONT.text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
def under(x0, x1, y, w=1.1):
    stroke([(x0, y), ((x0 + x1) / 2, y + 1.2), (x1, y - 0.5)], w)
def slash(x0, y0, x1, y1, w=1.6):
    stroke([(x0, y0), ((x0 + x1) / 2 + 1, (y0 + y1) / 2 - 1), (x1, y1)], w)
# 단답형
oval(116, 166, 10, 15); oval(116, 211, 10, 14); oval(120, 262, 16, 14)
for cy, t in [(166, '3'), (210, '3'), (260, '4'), (297, '10', )]: score(cy, t)
# 서술형 (1)
check(455, 385, 0.9); score(371, '2')
# 서술형 (2): x^2으로 나눈 식과 혼동
slash(90, 470, 290, 445)
write(95, 505, 'f(x)f(-x)/(x-2) = x^2|x^2-4|/(x-2) = x^2(x+2)  (x>2)', 12)
write(95, 522, '-> 16.  (1)처럼 x^2으로 나눈 식으로 계산함', 12)
score(494, '0')
# 서술형 (3)
under(378, 470, 670)
write(95, 700, '좌극한: x<2이면 |x^2-4| = -(x^2-4) 이므로 -16, 우극한 16', 12)
write(95, 717, '좌우 다름 -> 극한은 존재하지 않음', 12)
score(650, '0')
score(733, '2'); score(767, '12', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
