# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시
import pymupdf, math, random
random.seed(7)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
doc = pymupdf.open()
SP = 1   # 2쪽이 서답형 답안지
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

CX = 485.3
def score(cy, t, size=21):
    x = CX - pymupdf.Font(fontfile='pen.ttf').text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
def slash(x0, y0, x1, y1): stroke([(x0, y0), ((x0+x1)/2+1, (y0+y1)/2), (x1, y1)], 1.6)
# 단답형
oval(120, 163, 14, 13); oval(119, 204, 11, 13)
slash(160, 264, 184, 238)
for cy, t in [(158.9, '3'), (203.5, '3'), (255.5, '0'), (296, '6')]: score(cy, t)
# 서술형 (1)
check(392, 396); score(373.8, '2')
# 서술형 (2): a, b 부호 오류, D(k) 식 없음
stroke([(300, 563), (310, 565), (320, 563), (330, 565), (340, 563), (350, 565), (358, 563)], 1.1)
write(372, 479, 'a, b 부호 오류,', 10.5)
write(372, 491, 'D(k) 식, 검증 없음 -2', 10.5)
score(493.8, '2')
# 서술형 (3)
slash(283, 645, 309, 616)
write(330, 664, '(2)의 오류로 값 틀림  -2', 11)
score(653, '2')
score(741.9, '6'); score(771.2, '12', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
