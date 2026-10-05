# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시
import pymupdf, math, random
random.seed(7)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
doc = pymupdf.open()
SP = 0   # 1쪽이 서답형 답안지
pg = doc.new_page(width=src[SP].rect.width, height=src[SP].rect.height)
pg.show_pdf_page(pg.rect, src, SP, rotate=-src[SP].rotation)   # 스캔 페이지의 회전(/Rotate)을 반영해 보이는 그대로 배치
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

CX = 496.2
def score(cy, t, size=21):
    x = CX - pymupdf.Font(fontfile='pen.ttf').text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
# 단답형
oval(94, 155, 12, 17); oval(94, 201, 13, 12); oval(155, 246, 15, 12)
for cy, t in [(160, '3'), (205, '3'), (257, '4'), (296.8, '10')]: score(cy, t)
# 서술형 (1)
check(386, 388); score(375.2, '2')
# 서술형 (2): 인수분해와 배정 근거 생략
check(376, 528, 0.85)
write(384, 549, '인수분해, 배정 근거', 10.5)
write(384, 561, '생략  -1', 10.5)
score(495, '3')
# 서술형 (3)
check(452, 706); score(654.7, '4')
score(744, '9'); score(772.7, '19', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
