# -*- coding: utf-8 -*-
"""문학과 영상 〈고래를 위하여〉 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS
C = '①②③④⑤'
EX = {
 1: ("표현상 특징", "'-지'의 단정적 어조, '푸른'의 반복, 대구 구조로 청년들에게 꿈과 사랑을 따뜻하게 이야기한다. 반어나 냉소적 태도는 나타나지 않는다."),
 2: ("'고래'의 상징", "'푸른 바다에 고래가 없으면 푸른 바다가 아니지'처럼 고래는 바다를 가치 있게 만드는 존재이며, '마음속에 ~ 고래 한 마리 키우지 않으면 청년이 아니지'에서 청년이 품어야 할 꿈과 희망을 상징한다."),
 3: ("1연의 짜임", "1~2행(푸른 바다-고래)과 3~5행(청년-마음속 고래)이 같은 구조로 놓여, 바다에 고래가 필요하듯 청년에게 꿈이 필요하다는 생각을 유추의 방식으로 강조한다."),
 4: ("㉠의 의미", "바다가 고래를 위하여 푸르다는 것, 곧 상대를 위해 존재하고 그를 품어 주는 마음을 알아야 사랑을 안다는 뜻이다."),
 5: ("3연 감상", "고래가 별을 바라보듯 화자도 '내 마음속의 고래를 위하여' 별을 바라본다. 이는 꿈을 키우고 더 높은 이상을 지향하는 태도이지, 현실 안주가 아니다."),
 6: ("심상", "'푸른 바다', '수평선', '별' 등 시각적 심상이 중심이다. 소리·냄새·촉감의 심상은 쓰이지 않았고, 색채 이미지('푸른')가 두드러진다."),
 7: ("[보기] 감상", "화자는 청년을 다정하게 격려하며, '나도 가끔'처럼 자신도 꿈을 품은 사람으로서 공감한다. '청년이 아니지'를 비난이나 단절 선언으로 보는 것은 [보기]의 '따뜻한 시각', '격려'와 맞지 않는다."),
 8: ("형상화 방법 비교", "배경 음악과 효과음은 영상물인 〈걷기왕〉의 형상화 요소이다. 시는 시어의 상징, 반복·대구, 심상 등 언어로 형상화한다."),
}
SX = [
 ("시어 찾기", "(가) 1연 3행 '마음속에 푸른 바다의'에서 청년의 내면을 나타내는 시어는 '마음속'. (나) 3연에서 고래와 화자가 모두 바라보는 대상은 '별(별들)'. [각 5점]"),
 ("서술형 채점 기준", "형식적 측면: 유사한 구조의 반복(대구)으로 운율·리듬감 형성 → 5점. "
  "내용적 측면: 푸른 바다에 고래가 필요하듯 청년에게 꿈이 필요함을 유추로 강조 → 5점. 핵심어(운율/반복, 꿈의 필요성/유추) 없이 막연하면 각 2점."),
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
