# -*- coding: utf-8 -*-
"""문학과 영상 〈고래를 위하여〉 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS
C = '①②③④⑤'
EX = {
 1: ("표현상 특징", "ㄱ. 1연(푸른 바다에 ~ / 마음속에 ~)과 3연(고래도 가끔 ~ / 나도 가끔 ~) 모두 유사한 구조가 반복된다. ㄴ. '없으면/않으면'(부정의 가정) + '아니지'(부정의 결론)로 고래(꿈)의 필요성을 강하게 드러낸다. "
     "ㄷ. 시선은 바다(고래) → 수평선 위 → 밤하늘 별로 상승한다. ㄹ. '고래도 가끔'과 '나도 가끔'이 대응한다."),
 2: ("시어의 의미", "'밤하늘'은 별이 빛나는 배경으로, 화자가 꿈을 위해 바라보는 공간이다. 꿈을 가로막는 절망적 현실로 볼 근거가 없다. ③ '수평선'은 고래가 치솟아 넘어서는 경계로 읽을 수 있다."),
 3: ("1연의 짜임", "1~2행은 '바다에 고래가 있어야 푸른 바다'라는 받아들이기 쉬운 사실이고, 3~5행은 이를 청년과 마음속 고래(꿈)의 관계로 옮긴 유추이다. ④ '-면 … 아니지'는 조건 하나를 두 번 대응시킨 것이지 여러 조건의 열거가 아니다."),
 4: ("㉠의 의미", "주체는 '바다', 위하는 대상은 '고래'이다. 바다가 고래를 위해 푸르듯 상대를 위해 자신을 내어 주는 것이 사랑이다. ④는 주체와 대상을 뒤집은 함정이고, ③ '아직'은 앞으로 알게 될 가능성을 남긴다."),
 5: ("3연 감상", "ㄷ. '별'과 '별들'의 차이를 '더 많은 이상을 이미 이루었다'로 읽을 근거가 없다. ㄱ·ㄴ·ㄹ은 적절하다(1연 '-지'의 당위 → 3연 '바라본다'의 실천)."),
 6: ("심상", "'푸른'은 시각적 심상이면서 '청(靑)년'과 이어져 청년의 가능성까지 환기한다. ② '밤하늘'은 별을 보는 배경일 뿐 좌절이 아니다. 청각·공감각 심상은 쓰이지 않았고, 세대 갈등도 드러나지 않는다."),
 7: ("[보기] 감상", "1연(꿈) → 2연(사랑) → 3연(꿈을 위한 실천)으로 '꿈과 사랑'이라는 주제 아래 통일되어 있다. 2연이 무관한 화제라 통일성을 약화한다는 감상은 부적절하다."),
 8: ("〈걷기왕〉과 비교", "ㄱ. 시의 '별'과 영화의 '비행기'는 모두 올려다보는 대상으로 지향·깨달음을 형상화한다. ㄴ. 상승(지향)과 멈춤(자기 속도)이라는 태도의 차이가 있다. "
     "ㄷ. 두 작품 모두 주제를 직접 진술하지 않고 형상화한다. 시에는 대사·지시문도 없다. ㄹ. 시와 영화의 형상화 요소가 서로 바뀌었다."),
}
SX = [
 ("시구 찾기", "(가) 수평선 위로 치솟아올라 (나) 내 마음속의 고래를 위하여. [각 5점, 시구를 그대로 써야 정답]"),
 ("서술형 채점 기준", "형식적 측면: 유사한 구조의 반복(대구)으로 운율·리듬감 형성 → 3점. "
  "내용적 측면(유추): 푸른 바다–고래의 관계를 청년–마음속 고래(꿈)로 옮겨 꿈의 필요성을 말함 → 4점. "
  "내용적 측면(부정): 부정의 가정+부정의 결론으로 꿈이 반드시 필요함을 강하게 강조 → 3점."),
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
    head = ('<h1>2학년 문학과 영상 〈고래를 위하여〉 모의고사 정답 및 해설</h1><div class="sub">선택형 8문항(각 10점) · 서답형 2문항(각 10점)</div>'
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
