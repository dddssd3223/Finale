# -*- coding: utf-8 -*-
"""문학과 영상 〈걷기왕〉 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS
C = '①②③④⑤'
EX = {
 1: ("시나리오의 형식", "시나리오는 장면 번호, 대사, 지시문으로 이루어지며 서술자가 개입하지 않는다. 인물의 심리는 대사·행동·영상 기법으로 드러난다. ⑤ 'A.', 'B.'는 몽타주 장면 구분이다."),
 2: ("내용 이해", "S#53에서 수지는 '저 골대까지 잠깐이라도 나보다 앞서면 받아 줄게.'라고 조건을 건다. ① 만복은 담임의 권유를 거절한다. ③ 지현은 무리하지 말라고 한다. ④ 수지는 병원에 가라고 한다. ⑤ 만복은 경기를 그만둔다."),
 3: ("S#50 대화", "만복의 '노력해도 안 되는 것도 있잖아요. 그게 다 제 탓은 아니잖아요.'는 모든 결과를 노력 부족(개인의 탓)으로 돌리는 담임(사회)의 시각에 의문을 제기한다. ⑤ ㉠은 오히려 끝없는 노력을 요구한다."),
 4: ("만복의 심리", "㉡ '이거라도 안 하면 왠지…… 무서워서요', ㉢ '그냥 그렇게 믿고 싶은 거겠지'에서 만복이 좋아서라기보다 뒤처질 것 같은 불안 때문에 경보에 매달리고 있음을 알 수 있다. [A]의 '불안한 마음이 들 때마다 더욱 훈련에 열중했다'와도 연결된다."),
 5: ("[A] 몽타주", "[A]는 짧은 장면들을 이어 붙인 몽타주이다. 하나의 장면을 길게 찍는 롱 테이크가 아니며, 훈련이 여유롭게 진행되는 것도 아니다(지옥 훈련, 붕대·파스)."),
 6: ("[B] 꿈 장면", "결승선을 통과하면 다시 출발 소리가 울리는 반복은 끝없이 더 많은 성취를 요구받는 압박감을 상징한다. 멈추자 쏟아지는 비난은 실패에 대한 두려움을 보여 준다."),
 7: ("㉣과 '정신력' 대사", "수지가 하던 '노력', '정신력' 이야기를 그대로 되돌려주며, 자신의 무리는 '미련함'이라 부르는 수지의 이중적인 기준을 지적한다."),
 8: ("[C] 감상", "드러누운 만복의 '표정이 편하다'는 지시문과 ㉤에서 알 수 있듯, 만복의 선택은 좌절이 아니라 자기만의 속도를 받아들이는 깨달음이다."),
}
SX = [
 ("촬영 기법", "(가) 인물의 어깨 너머로 상대를 촬영하는 오버 더 숄더 숏. (나) 피사체의 일부를 화면에 꽉 차게 찍는 익스트림 클로즈업 숏. [각 5점]"),
 ("서술형 채점 기준", "① '오버 페이스'(자기 능력 이상으로 무리함)를 활용해 급수조차 하지 않은 이유를 쓰면 4점. "
  "② 만복이 경기를 그만두고 편안해한 선택(㉤ 활용)과의 대비를 쓰면 3점. "
  "③ '자기만의 삶의 속도', '경쟁 사회 비판' 등 주제와 연결하면 3점."),
]
CSS = r"""@page{size:A4;margin:14mm 13mm}
body{font-family:'HB','GL';font-size:9.6pt;color:#111;line-height:1.6}
h1{font-family:'GL';font-size:15pt;text-align:center;margin:0 0 3pt;-webkit-text-stroke:.3pt #000}
.sub{text-align:center;color:#555;font-family:'GL';font-size:9pt;margin-bottom:10pt}
table{border-collapse:collapse;width:100%;margin-bottom:10pt}
th,td{border:.6pt solid #888;padding:3pt 4pt;text-align:center;font-size:9.4pt}
th{background:#eee;font-family:'GL';font-weight:400;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.it{margin:0 0 7pt;break-inside:avoid}.it b.n{font-family:'GL'}
.it .t{color:#555;font-family:'GL';font-size:8.8pt;margin-left:4pt}
h2{font-family:'GL';font-size:11pt;margin:10pt 0 5pt;border-bottom:1pt solid #333;padding-bottom:2pt}"""
def build(out):
    head = ('<h1>2학년 문학과 영상 〈걷기왕〉 모의고사 정답 및 해설</h1><div class="sub">선택형 8문항(각 10점) · 서답형 2문항(각 10점)</div>'
            '<table><tr><th>번호</th>' + ''.join(f'<th>{n}</th>' for n in range(1, 9)) + '</tr><tr><th>정답</th>'
            + ''.join(f'<td>{C[ANS[n]-1]}</td>' for n in range(1, 9)) + '</tr></table>'
            '<table><tr><th style="width:14%">서답형</th><th>정답</th></tr>'
            + ''.join(f'<tr><td>{i+1}</td><td style="text-align:left">{a}</td></tr>' for i, a in enumerate(SA_ANS)) + '</table>')
    body = '<h2>선택형 해설</h2>' + ''.join(f'<div class="it"><b class="n">{n}. {C[ANS[n]-1]}</b><span class="t">{EX[n][0]}</span><br>{EX[n][1]}</div>' for n in range(1, 9))
    body += '<h2>서답형 해설</h2>' + ''.join(f'<div class="it"><b class="n">서답형 {i+1}. {SA_ANS[i]}</b><span class="t">{t}</span><br>{x}</div>' for i, (t, x) in enumerate(SX))
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{body}</body></html>')
    open(os.path.join(HERE, 'sol_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'sol_src.html', 'sol_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'sol_tmp.pdf'), out)
if __name__ == '__main__':
    build(sys.argv[1])
