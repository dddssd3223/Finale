# -*- coding: utf-8 -*-
"""실제 중간고사 응시 시험지(스캔)에 문항별 주석을 달아 평가하는 PDF"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(SCR, 'r20')); from build3 import font_css, KATEX_CSS
sys.path.insert(0, os.path.join(SCR, 'myexam')); from regoff import S, off

PW, PH, SW = 1028, 1031, 728          # 쪽 크기(pt), 스캔 폭
OK, NG, TIP, GOOD = '#1a7f37', '#cf222e', '#1f5fd1', '#8250df'
PT = {n: p for n, p in zip(range(1, 19), [4.0]*4 + [4.2]*4 + [4.4]*2 + [4.5]*2 + [4.7]*3 + [4.9] + [5.2]*2)}

def crop(pg, side, px, py):
    """예전에 본 1.5배 단 이미지(lb/p{n}{L,R}.png)의 픽셀 → 스캔 pt"""
    x0 = (36 if side == 'L' else 299) * 1.2352 + 4.2
    return (x0 + px / 1.5, 146 * 1.2352 - 4.4 + py / 1.5)

B = json.load(open(os.path.join(SCR, 'r0', 'blocks.json')))
def qpos(key):
    b = next(x for x in B if x['k'] == key); pg = int(b['top'] // 842); t = b['top'] - pg * 842
    OX, OY = off('a.pdf' if pg < 4 else 'b.pdf', pg % 4)
    col = 42.2 if key in ('Q1', 'Q2', 'Q5', 'Q6', 'Q9', 'Q11', 'Q13', 'Q15', 'Q17', 'SEC1') else 301.5
    return (col * S + OX, (t + 6) * S + OY)

# 문항 카드: (쪽, 키, 제목, 판정 'O'/'X'/'P', 점수 문자열, 본문, [표시점 (쪽단, px, py)])
C = [
 (1, 'Q1', '1번 · 그래프 좌·우극한', 'O', '4.0 / 4.0',
  r"그래프 옆에 \(-2\), \(1\)을 먼저 적고 더함. 값 읽기를 시각적으로 남긴 좋은 습관.", [('L', 85, 590)]),
 (1, 'Q2', '2번 · 연속과 미정계수', 'O', '4.0 / 4.0',
  r"분자가 \(x-1\)을 인수로 가져야 함 → \((x+2)(x-1)\)로 \(a=1\), \(b=3\). 군더더기 없음.", [('L', 420, 830)]),
 (1, 'Q3', '3번 · 평균값 정리', 'O', '4.0 / 4.0',
  r"풀이 없이 암산. 평균변화율 \(=7=2c\). 모의고사에 없던 단원인데도 바로 해결.", []),
 (1, 'Q4', '4번 · 도함수 범위 → \(f(3)\) 최대·최소', 'O', '4.0 / 4.0',
  r"극단 함수 \(x+2\), \(2x+2\)를 넣어 \(5\), \(8\)을 바로 얻음. 가장 빠른 길.<br><span class=tip>보완</span> 서술형이면 근거 한 줄 필요: \(1\le\dfrac{f(3)-f(0)}{3}\le2\) (평균값 정리).", [('R', 300, 830)]),
 (2, 'Q5', '5번 · 극한의 대소 관계', 'O', '4.2 / 4.2',
  r"\(\dfrac fg\to3\) (끼우기)로 정하고, 분자·분모를 \(g^2\)으로 나눠 \(\dfrac75\). 정석.", [('L', 300, 330)]),
 (2, 'Q6', '6번 · 사잇값 정리', 'O', '4.2 / 4.2',
  r"\(h(x)=f(x)+f(x+1)+x\)를 만들어 정수점 부호(음 → 양)로 \((0,\,1)\) 선택. 정석.<br><span class=tip>체크</span> ④에 밑줄 친 흔적 → 마지막에 흔들렸던 듯. 부호표를 믿고 넘어가기.", [('L', 230, 880), ('L', 60, 772)]),
 (2, 'Q7', '7번 · 집합 조건 삼차함수', 'O', '4.2 / 4.2',
  r"\(f(x)-2=(x^2-a^2)(x+2a)\)로 놓고 미분 → \((a-5)(a+1)=0\), \(f(0)>0\)으로 \(a=-1\). 모의 10회 13번 원본 효과.", [('R', 420, 400)]),
 (2, 'Q8', '8번 · 곱의 미분 + 관계식', 'O', '4.2 / 4.2',
  r"\(x=2\) 대입 → \(g(2)=-1\), \(f(2)=-3\) → \(h'(2)\)식에 넣어 \(g'(2)=1\). 순서 완벽.", [('R', 250, 840)]),
 (3, 'Q9', '9번 · 정수 조건 부등식', 'O', '4.4 / 4.4',
  r"양 끝 식이 같아지는 \(k=2,\,3\)을 바로 찾아 \(f\)를 결정. 16회 15번에서 익힌 핵심.", [('L', 330, 510)]),
 (3, 'Q10', '10번 · \(\infty\)꼴 극한과 다항함수', 'O', '4.4 / 4.4',
  r"\(t=\dfrac1x\) 치환으로 최고차 \(5x^3\), \(f(2)=0\), \(f'(2)=70\) → 연립. 계산이 길었지만 실수 없음.", [('R', 330, 740)]),
 (4, 'Q11', '11번 · 좌·우극한과 곱', 'O', '4.5 / 4.5',
  r"풀이 없이 암산 처리. 좌·우극한 비교만으로 충분한 문항이라 시간 절약 잘함.", []),
 (4, 'Q12', '12번 · 함수의 곱의 연속', 'O', '4.5 / 4.5',
  r"\(f(a)=0\)인 \(a=-1,\,5\)에 더해, 양쪽 점프가 상쇄되는 \(a=2\)를 표로 따로 확인.<br><span class=good>최고</span> 이번 시험에서 '경우 누락' 약점을 이겨낸 장면.", [('R', 190, 465), ('R', 330, 420)]),
 (5, 'Q13', '13번 · 대칭축과 미분계수의 합', 'O', '4.7 / 4.7',
  r"극한을 \(3f'(2k-3)\)으로 바꾸고 대칭축 \(x=5\) → \(f=(x-5)^2+k\). 시그마 계산을 한 번 지웠지만 바로 바로잡음.", [('L', 280, 330), ('L', 100, 540)]),
 (5, 'Q14', '14번 · 도형과 극한', 'O', '4.7 / 4.7',
  r"두 원 사이 거리를 식으로 세우고 유리화 → \(\dfrac{t+1}{\sqrt{5t^2+12t+8}+2t+3}\to\dfrac2{10}\). 정석.", [('R', 330, 890)]),
 (6, 'Q15', '15번 · 접선과 도형', 'O', '4.7 / 4.7',
  r"정삼각형으로 가정하던 시도를 지우고, 접선 기울기 조건 두 개로 돌아와 \(a=-2\) 결정. 판단 전환이 좋았음.", [('L', 180, 770), ('L', 190, 855)]),
 (6, 'Q16', '16번 · 함숫값을 따로 정의한 함수', 'O', '4.9 / 4.9',
  r"\(f(x)-1=(x-2)(x-4)(x-k)\)로 놓고 극한 조건에서 \(k=3\), 마지막 \(10g(7)=61\).<br><span class=tip>필기</span> 숫자 3을 'ㄱ'처럼 써서 7과 헷갈릴 수 있음. 3·7 구분해서 쓰기.", [('R', 280, 520), ('R', 300, 930)]),
 (7, 'Q17', '17번 · 합성함수 극한', 'O', '5.2 / 5.2',
  r"\(g(t)=0,\,1\)이 되는 위치로 경우를 나눠 그래프를 직접 그림.<br><span class=good>베스트</span> 처음 보는 유형을 그림으로 해결한 이번 시험 최고의 풀이.<br><span class=tip>흔적</span> ④ 7(\(k=1\))에 동그라미 → 최종 ① 4로 고침. \(k\) 범위의 끝값을 다시 따진 것으로 보임(추정). 끝값 포함 여부를 한 줄로 적어 두면 더 안전.", [('L', 280, 690), ('L', 220, 830), ('L', 300, 416)]),
 (7, 'Q18', '18번 · \(f(x)/f(x^2)\)의 불연속', 'X', '0 / 5.2',
  r"풀이 흔적 없음. 앞 17문항 답 개수를 세어(가장 적은 ①) 찍음 → 정답 ④. 같은 개수 메모가 6쪽 위에도 있음.<br><span class=bad>원인</span> 시간 부족. 학교 시험은 정답 개수가 고르지 않아 개수 찍기는 근거가 약함.<br><span class=tip>최소 1줄</span> (다)에서 \(f(-3)=0\)부터 쓰면 조건 (가)(나)로 이어짐.", [('R', 130, 880)]),
]
SA = [
 (8, 'SEC1', '서답형 1 · 연속·미분가능성', 'O', '10 / 10',
  r"답안지에 근거를 갖춰 만점. 좌·우미분계수 비교까지 완성.<br>여백의 V자 그림은 절댓값 꺾인 점 확인용으로 좋은 습관.", [('L', 120, 640)]),
 (8, 'SEC1b', '서답형 2 계산을 1번 여백에서 반복', 'X', '',
  r"\(-\tfrac12\)로 조립제법을 시도함. <b>\(-\tfrac12\)은 \(f\)의 근이 아님.</b><br>\(4x+4=2x+3\)의 해 \(x=-\tfrac12\)은 두 일차식이 같아지는 점이고, 그때 값 \(4x+4=2\)가 \(f\)의 근.", [('L', 180, 1020), ('L', 330, 770)]),
 (8, 'S2', '서답형 2 · 고정점과 판별식', 'P', '4 / 10',
  r"(1) \(f(2)=0\) → \(b=-6\) 정답.<br><span class=bad>(2)(3)</span> \((2x+1)\)을 인수로 가정한 것이 출발 오류. 마지막에 쓴 4는 시간에 쫓긴 값.<br><span class=tip>올바른 흐름</span>"
  r"\[f(x)=(x-2)\{x^2+(a+2)x+3\}\]"
  r"이차식이 실근이 없어야 함(판별식 \(<0\)) → \(a\ge-5\) → 최솟값 \(-5\)."
  r"\[f(1)=-(a+6)\le-1\]", [('R', 410, 320), ('R', 220, 520)]),
]

def head_tag(v):
    return {'O': (OK, '정답'), 'X': (NG, '오답'), 'P': ('#9a6700', '부분 점수')}[v]

CSS = f"""
@page{{size:{PW}pt {PH}pt;margin:0}}
html,body{{margin:0;background:#fff}}
body{{font-family:'GL';color:#111}}
.pg{{position:relative;width:{PW}pt;height:{PH}pt;page-break-after:always;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.scan{{position:absolute;left:0;top:0;width:{SW}pt;height:{PH}pt}}
.panel{{position:absolute;left:{SW}pt;top:0;width:{PW-SW}pt;height:{PH}pt;background:#f6f7f9;border-left:1pt solid #d0d7de;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.ph{{margin:16pt 14pt 6pt;font-size:10.5pt;-webkit-text-stroke:.25pt #000}}
.ph span{{color:#57606a;font-size:8.5pt;-webkit-text-stroke:0}}
.box{{position:absolute;left:12pt;width:{PW-SW-24}pt;background:#fff;border:.8pt solid #d0d7de;border-left:3pt solid var(--c);border-radius:3pt;padding:5pt 7pt 6pt;box-sizing:border-box;font-size:8.6pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.box .t{{display:flex;justify-content:space-between;align-items:center;margin-bottom:2pt;font-size:9.2pt;-webkit-text-stroke:.2pt #000}}
.box .v{{color:#fff;background:var(--c);border-radius:8pt;padding:0 6pt;font-size:8pt;-webkit-text-stroke:0;white-space:nowrap}}
.box .s{{color:#57606a;font-size:8pt;-webkit-text-stroke:0;margin-left:4pt}}
.box .katex-display{{margin:3pt 0}}
.n{{display:inline-block;width:13pt;height:13pt;line-height:13pt;border-radius:50%;background:var(--c);color:#fff;text-align:center;font-size:7.6pt;margin-right:3pt;-webkit-text-stroke:0;vertical-align:1pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.mk{{position:absolute;width:15pt;height:15pt;margin:-7.5pt 0 0 -7.5pt;border-radius:50%;background:var(--c);color:#fff;font-size:8.4pt;line-height:15pt;text-align:center;border:1.2pt solid #fff;box-shadow:0 0 0 .6pt var(--c);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.qm{{position:absolute;height:13pt;margin-top:-13pt;padding:0 5pt;border-radius:7pt;background:var(--c);color:#fff;font-size:8pt;line-height:13pt;white-space:nowrap;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.tip,.bad,.good{{display:inline-block;border-radius:2pt;padding:0 4pt;margin-right:3pt;font-size:7.6pt;color:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.tip{{background:{TIP}}}.bad{{background:{NG}}}.good{{background:{GOOD}}}
.sum{{position:absolute;left:12pt;right:12pt;bottom:14pt;font-size:8.2pt;line-height:1.5;color:#24292f}}
table{{border-collapse:collapse;width:100%;font-size:8.2pt}}
td,th{{border:.6pt solid #d0d7de;padding:2pt 4pt;text-align:center}}
th{{background:#eaeef2;font-weight:400;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

LAYOUT_JS = r"""
<script>
function lay(){for(const p of document.querySelectorAll('.panel')){let y=parseFloat(p.dataset.start);
 const bx=[...p.querySelectorAll('.box')];const lim=p.getBoundingClientRect().height-(p.querySelector('.sum')?p.querySelector('.sum').getBoundingClientRect().height+26:14);
 for(const b of bx){const a=parseFloat(b.dataset.a);let t=Math.max(a,y);b.style.top=t+'px';y=t+b.getBoundingClientRect().height+8}
 if(y>lim){let over=y-lim;for(let i=bx.length-1;i>=0&&over>0;i--){const b=bx[i];const t=parseFloat(b.style.top);const nt=Math.max(i?parseFloat(bx[i-1].style.top)+bx[i-1].getBoundingClientRect().height+8:p.dataset.start*1,t-over);over-=t-nt;b.style.top=nt+'px'}}}}
document.fonts.ready.then(lay);
</script>"""

def page_html(pg, cards, extra_head='', summary=''):
    f = 'a.pdf' if pg <= 4 else 'b.pdf'
    h = [f'<div class="pg"><img class="scan" src="scan{pg}.jpg">']
    boxes = []; num = 0
    def anc(key):
        if key == 'SEC1b': return crop(pg, 'L', 180, 1020)
        ax, ay = qpos(key)
        return (ax, ay + 37 * S) if key == 'SEC1' else (ax, ay)
    cards = sorted(cards, key=lambda c: anc(c[1])[1])
    for (p, key, title, v, score, body, spots) in cards:
        c, lab = head_tag(v)
        ax, ay = anc(key)
        if key != 'SEC1b':
            h.append(f'<div class="qm" style="--c:{c};left:{ax+18:.1f}pt;top:{ay-2:.1f}pt">{"✓" if v=="O" else ("✗" if v=="X" else "△")} {score}</div>')
        nums = []
        for side, px, py in spots:
            num += 1; x, y = crop(pg, side, px, py); x -= 13; y -= 7
            h.append(f'<div class="mk" style="--c:{c};left:{x:.1f}pt;top:{y:.1f}pt">{num}</div>'); nums.append(num)
        nn = ''.join(f'<span class="n" style="--c:{c}">{k}</span>' for k in nums)
        boxes.append((ay, f'<div class="box" data-a="{ay*4/3:.1f}" style="--c:{c}"><div class="t"><span>{nn}{title}</span>'
                          f'<span>{"<span class=v>"+lab+"</span>" if v else ""}<span class="s">{score}</span></span></div>{body}</div>'))
    boxes.sort(key=lambda t: t[0])
    h.append(f'<div class="panel" data-start="{44*4/3}"><div class="ph">{extra_head}</div>{"".join(b for _, b in boxes)}{summary}</div></div>')
    return ''.join(h)

def build(out):
    pages = []
    for pg in range(1, 9):
        cards = [c for c in C + SA if c[0] == pg]
        head = f'주석 · {pg}쪽 <span>8쪽 중</span>'
        summ = ''
        if pg == 1:
            summ = ('<div class="sum"><b>총점 88.8 / 100</b><br>'
                    '<table><tr><th>구분</th><th>득점</th><th>내용</th></tr>'
                    '<tr><td>선택형 1–17번</td><td>75.6 / 75.6</td><td>전부 정답</td></tr>'
                    '<tr><td>선택형 18번</td><td>0 / 5.2</td><td>시간 부족 · 찍음</td></tr>'
                    '<tr><td>서답형 1</td><td>10 / 10</td><td>만점</td></tr>'
                    '<tr><td>서답형 2</td><td>4 / 10</td><td>(1)만 정답</td></tr></table>'
                    '<span style="color:#57606a">표시: 문항 번호 옆 띠 = 판정·점수, 숫자 원 = 오른쪽 주석과 연결된 풀이 위치</span></div>')
        pages.append(page_html(pg, cards, head, summ))
    total = f"""<div class="pg" style="padding:60pt 70pt;box-sizing:border-box;font-size:13pt">
<div style="font-size:24pt;-webkit-text-stroke:.45pt #000;margin-bottom:6pt">실제 중간고사 응시 시험지 평가 · 총평</div>
<div style="color:#57606a;font-size:13pt;margin-bottom:22pt">미적분Ⅰ · 2026년 10월 13일(화) 1교시 · 88.8점</div>
<table style="font-size:13pt;line-height:1.9"><tr><th style="width:18%">구분</th><th style="text-align:left">평가</th></tr>
<tr><td style="color:{OK}">잘한 점</td><td style="text-align:left">
· 선택형 1–17번 전부 정답. 처음 보는 3·4·17번도 극단값 대입과 그래프로 해결했음.<br>
· 12번에서 특수한 \\(a=2\\)를 따로 확인 → 모의고사 내내 남았던 '경우 누락' 약점을 실전에서 이겨냄.<br>
· 15번에서 막힌 가정(정삼각형)을 버리고 조건식으로 돌아온 판단이 빨랐음.<br>
· 서답형 1 만점: 서술형 근거 쓰기는 완성 단계.</td></tr>
<tr><td style="color:{NG}">놓친 점 (11.2점)</td><td style="text-align:left">
· 18번 5.2점: 풀이 없이 답 개수로 찍음 → 시간 배분 문제.<br>
· 서답형 2 (2)(3) 6점: 두 일차식이 같아지는 \\(x=-\\tfrac12\\)를 \\(f\\)의 근으로 착각 → 조립제법 방향 오류. 같은 시도를 여백 두 곳에서 반복함.</td></tr>
<tr><td style="color:{TIP}">시간 흐름 (추정)</td><td style="text-align:left">
· 앞부분(1–8번)이 모의고사보다 어려워 예상보다 시간을 더 썼고, 17번에도 그래프를 그리며 공을 들임.<br>
· 그 결과 18번은 빈칸, 20번은 첫 방향을 의심할 시간이 없었던 흐름으로 보임.</td></tr>
<tr><td style="color:{GOOD}">기말 처방</td><td style="text-align:left">
1. <b>고정점 문항 순서:</b> 두 식이 같아지는 \\(x\\) → 그때의 값이 \\(f\\)의 근 → 인수분해 → 나머지 이차식 판별식.<br>
2. <b>막히면 1분 규칙:</b> 첫 방향이 1분 안에 진전 없으면 조건을 처음부터 다시 읽기.<br>
3. <b>마지막 두 문항 배분:</b> 고난도가 둘 남으면 첫 조건 한 줄씩 쓰고 더 풀릴 쪽에 집중.<br>
4. <b>필기:</b> 3과 7을 구분해서 쓰기(16번 'ㄱ'처럼 보이는 3).</td></tr></table></div>"""
    pages.append(total)
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{"".join(pages)}{LAYOUT_JS}</body></html>')
    open(os.path.join(HERE, 'ann_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'ann_src.html', 'ann_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'ann_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
