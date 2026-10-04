# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시
import pymupdf, math, random
random.seed(7)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
doc = pymupdf.open()
SP = 0   # 이번 스캔은 1쪽이 서답형 답안지
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

CX = 484.3
def score(cy, t, size=21):
    x = CX - pymupdf.Font(fontfile='pen.ttf').text_length(t, fontsize=size) / 2
    write(x, cy + size * 0.32, t, size, rot=-4)
def slash(x0, y0, x1, y1): stroke([(x0, y0), ((x0+x1)/2+1, (y0+y1)/2), (x1, y1)], 1.6)
# 단답형 1: 정답 동그라미
oval(148, 165, 12, 13); oval(147, 205, 11, 13); oval(161, 250, 14, 19)
for cy, t in [(159.5, '3'), (204.2, '3'), (256.2, '4'), (296.6, '10')]: score(cy, t)
# 서술형 (1)
check(301, 384); score(374.3, '2')
# 서술형 (2): g(x)를 g(x)-f(x)로 적음
stroke([(232, 563), (250, 565), (270, 563), (290, 565), (310, 563), (330, 565), (350, 563), (370, 565), (390, 563), (412, 565)], 1.1)
write(46, 523, '이 식은 g(x)임 (g-f 아님),', 11.5)
write(46, 536, '단순근 배제 근거 없음  -3', 11.5)
score(494.3, '1')
# 서술형 (3): (2)의 오류가 이어진 값
slash(322, 690, 352, 668)
write(368, 708, '(2)의 오류로 값 틀림  -2', 11)
score(653.6, '2')
score(742.4, '5'); score(771.3, '15', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
