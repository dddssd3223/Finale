# 서답형 답안지 스캔 위에 빨간 손글씨 채점 표시
import pymupdf, math, random
random.seed(7)
RED = (0.86, 0.08, 0.1)
src = pymupdf.open('scan.pdf')
doc = pymupdf.open(); doc.insert_pdf(src, from_page=1, to_page=1)
pg = doc[0]
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

# 단답형 1: 정답 동그라미
oval(98, 160, 11, 13); oval(93, 200, 12, 12); oval(165, 252, 20, 12)
for cy, t in [(158, '3'), (202, '3'), (254, '4'), (294.5, '10')]: score(cy, t)
# 서술형 1 (1)
check(364, 380); score(373, '2')
# 서술형 (2)
check(399, 428, 0.75)
stroke([(138, 522), (148, 524), (158, 522), (168, 524), (178, 522), (188, 524)], 1.1)   # A(0,3) 밑줄
write(128, 523, '*', 15)
write(389, 478, '* A가 x=0인 점인 근거', 11.5)
write(368, 494, '(OA<OB<OC) 없음  -1', 11.5)
check(463, 542, 0.7)
score(493, '3')
# 서술형 (3)
check(394, 702); score(651, '4')
# 소계·총점
score(739.5, '9'); score(768.7, '19', 20)
doc.save('graded.pdf', garbage=3, deflate=True)
