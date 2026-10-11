# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시 (16회)
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
oval(113, 160, 12, 14); oval(118, 252, 17, 14)
slash(100, 214, 128, 192); write(140, 210, '3', 16)
for cy, t in [(160, '3'), (203, '0'), (252, '4'), (297, '7')]: score(cy, t)
# 서술형 (1)
check(452, 372, 0.9); score(361, '2')
# 서술형 (2)
check(452, 524, 0.8)
write(72, 559, '좌우극한 g(3)/(-2)=g(3)/(3a-9) 로 쓰면 더 안전', 9.5)
score(486, '4')
# 서술형 (3)
check(450, 661, 0.65)
write(75, 714, '뒷면 계속 풀이 확인: h(1)+h(2) = -53/6  O', 11)
score(649, '4')
score(733, '10'); score(767, '17', 20)
# 뒷면 (서술형 (3) 계속)
bk = pymupdf.open('in/back.pdf')
pg = doc.new_page(width=bk[0].rect.width, height=bk[0].rect.height)
pg.show_pdf_page(pg.rect, bk, 0)
pg.insert_font(fontname='pen', fontfile='pen.ttf')
oval(483, 284, 22, 20)
check(520, 270, 1.0)
write(225, 380, '서술형 1 (3) 계속 풀이 인정: h(1)+h(2) = -53/6', 12)
write(225, 398, '(3) 4/4 -> 서술형 10/10', 12)
doc.save('graded.pdf', garbage=3, deflate=True)
