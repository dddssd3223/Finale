# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시
import pymupdf, math, random
random.seed(7)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
doc = pymupdf.open()
pg = doc.new_page(width=src[1].rect.width, height=src[1].rect.height)
pg.show_pdf_page(pg.rect, src, 1, rotate=-src[1].rotation)   # 스캔 페이지의 회전(/Rotate)을 반영해 보이는 그대로 배치
pg.insert_font(fontname='pen', fontfile='pen.ttf')

def stroke(pts, w=1.3):
    sh = pg.new_shape(); sh.draw_polyline(pts); sh.finish(color=RED, width=w, closePath=False, lineCap=1, lineJoin=1); sh.commit()

def oval(cx, cy, rx, ry, w=1.2):
    # 손으로 그린 듯한 타원(끝이 살짝 겹침)
    pts = []; a0 = random.uniform(-2.2, -1.6)
    for i in range(46):
        t = a0 + i / 40 * 2 * math.pi
        j = 1 + 0.04 * math.sin(3 * t + 1)
        pts.append((cx + rx * j * math.cos(t), cy + ry * j * math.sin(t)))
    stroke(pts, w)

def check(x, y, s=1.0, w=1.5):
    stroke([(x, y), (x + 4 * s, y + 6 * s), (x + 4.6 * s, y + 6.2 * s), (x + 14 * s, y - 9 * s)], w)

def write(x, y, t, size=16, rot=0):
    pg.insert_text((x, y), t, fontname='pen', fontsize=size, color=RED, morph=(pymupdf.Point(x, y), pymupdf.Matrix(rot)) if rot else None)

def score(cy, t, size=21):
    x = 497 - pymupdf.Font(fontfile='pen.ttf').text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)

CX = 497.6
def score(cy, t, size=21):
    x = CX - pymupdf.Font(fontfile='pen.ttf').text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
def slash(x0, y0, x1, y1): stroke([(x0, y0), ((x0+x1)/2+1, (y0+y1)/2), (x1, y1)], 1.6)
# 단답형 1: 오답 빗금
slash(98, 165, 128, 136); slash(95, 201, 124, 174); slash(160, 262, 196, 228)
for cy, t in [(150, '0'), (194, '0'), (246, '0'), (286.5, '0')]: score(cy, t)
# 서술형 1 (1)
check(294, 384); score(365, '2')
# 서술형 (2)
stroke([(252, 519), (262, 521), (272, 519), (282, 521), (292, 519), (302, 521), (312, 519), (322, 521), (332, 519)], 1.1)
write(47, 547, '근을 극점으로 쓴 서술 오류,', 11.5)
write(47, 560, '비율관계 근거 없음 -1', 11.5)
check(452, 540, 0.75)
score(485, '3')
# 서술형 (3)
check(276, 699); score(643, '4')
score(733.5, '9'); score(764.6, '9', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
