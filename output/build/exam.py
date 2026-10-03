from common import *

NPAGES = 6
CSS = FONT_CSS + r"""
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#000}
body{font-family:'NM',serif;font-size:9.4pt;line-height:1.72;word-break:keep-all}
.katex{font-size:1.07em}
.katex-display{margin:.45em 0}
.page{width:210mm;height:297mm;padding:9mm 12.5mm 7mm 13mm;display:flex;flex-direction:column;page-break-after:always;overflow:hidden;position:relative}
.page:last-child{page-break-after:auto}
.hd{font-family:'NG',sans-serif}
.r1{display:flex;justify-content:space-between;align-items:flex-start}
.r1 .t{font-size:11.2pt;margin-top:2.2mm;letter-spacing:.2pt}
.sign{border-collapse:collapse;font-family:'NM';font-size:7.4pt}
.sign td{border:.7pt solid #000;width:12mm;text-align:center;padding:0;letter-spacing:2.2pt}
.sign tr:first-child td{height:4.4mm;font-weight:700}
.sign tr:last-child td{height:12mm}
.r2{display:flex;gap:16mm;font-size:9.6pt;margin-top:-6.5mm;align-items:baseline}
.r2 b{font-weight:400;font-size:11pt}
.r2 small{font-size:7.6pt}
.r3{display:flex;align-items:flex-end;justify-content:space-between;margin-top:6.5mm}
.logo{display:inline-flex;width:9.4mm;height:9.4mm;border:1.4pt solid #000;border-radius:50%;align-items:center;justify-content:center;font-family:'NM';font-weight:800;font-size:15pt;margin-right:3mm;line-height:1}
.ttl{display:flex;align-items:baseline}
.ttl .g{font-size:19pt;font-weight:400}
.ttl .s{font-size:14pt}
.ttl .m{font-size:20pt;font-weight:700;letter-spacing:-.3pt}
.ttl .e{font-size:16.5pt}
.r3 .dt{font-size:7pt;padding-bottom:1mm}
.bar{border-top:2.6pt solid #000;margin-top:1.2mm}
.r4{font-size:7.6pt;display:flex;justify-content:space-around;border-bottom:.8pt solid #000;padding:.4mm 6mm .3mm}
.body{flex:1;display:flex;border-left:.8pt solid #000;border-right:.8pt solid #000;min-height:0}
.col{flex:1;display:flex;flex-direction:column;padding:2.6mm 3.6mm 1mm;min-height:0;overflow:hidden}
.col+.col{border-left:.8pt solid #000}
.slot{min-height:0;overflow:hidden}
.ft{display:flex;justify-content:space-between;align-items:center;font-family:'NG';font-size:7.8pt;border-top:.8pt solid #000;padding-top:2mm}
.ft .c{display:flex;align-items:center;gap:2mm}
.ft .c i{font-style:normal;display:inline-flex;width:6mm;height:6mm;border:1pt solid #000;border-radius:50%;align-items:center;justify-content:center;font-weight:800;font-size:9.5pt}
.notice{border:.8pt solid #000;padding:1.4mm 2.4mm 1.6mm;font-family:'NG';font-size:8pt;line-height:1.5;margin-bottom:2.4mm}
.notice h4{text-align:center;margin:0 0 .8mm;font-weight:400;font-size:8pt}
.notice p{margin:0 0 .3mm;padding-left:3.2mm;text-indent:-3.2mm}
.sec{font-family:'NG';margin:0 0 3mm}
.sec .h{font-size:11.2pt}
.sec .d{font-size:8.6pt;line-height:1.45}
.sec u{text-underline-offset:2px}
.q{position:relative;padding-left:6.2mm;text-align:justify}
.q .n{position:absolute;left:0;top:0;font-weight:800;font-size:10.2pt}
.q .pt{white-space:nowrap}
.ch{display:flex;justify-content:space-between;margin:3.2mm 2mm 0 1mm}
.ch>span{min-width:12mm}
.chg{display:grid;grid-template-columns:repeat(3,1fr);row-gap:1.2mm;margin:3mm 0 0 1mm}
.cond{border:.7pt solid #000;padding:1.6mm 2.6mm;margin:2.2mm 0}
.ci{display:flex;gap:1.2mm}
.ci .ck{flex:none}
.bogi{border:.7pt solid #000;margin:2.6mm 0 0;padding:.6mm 3mm 1.8mm}
.bogi legend{margin:0 auto;padding:0 2mm;font-size:9pt}
.bi{display:flex;gap:1.6mm;margin:.6mm 0}
.bi .bk{flex:none}
.fig{text-align:center;margin:1.6mm 0 .8mm}
.fig svg{width:var(--fw,44mm);height:auto}
.sub{margin-top:2.6mm;padding-left:6mm;text-indent:-6mm}
.ansl{height:var(--h);}
.end{text-align:center;font-family:'NG';margin-top:auto;margin-bottom:12mm}
.end .a{font-size:20pt}
.end .b{font-size:15pt;margin:1mm 0 6mm}
.end .c{font-size:13pt;line-height:1.7}
.memo{border:.6pt dashed #777;flex:1;margin-top:3mm;position:relative}
.memo span{position:absolute;top:1mm;left:2mm;font-family:'NG';font-size:7.5pt;color:#555}
"""

def header(pg):
    return f"""
<div class="hd r1"><div class="t">2026학년도&nbsp;&nbsp;&nbsp; 제( 2 )학기 &nbsp;&nbsp;( 중간고사 ) 출제</div>
<table class="sign"><tr><td>교무</td><td>교감</td><td>교장</td></tr><tr><td></td><td></td><td></td></tr></table></div>
<div class="hd r2"><span>고사 일자&nbsp; 2026년 10월 (&nbsp;&nbsp;&nbsp;)일</span><span><b>출제교사 (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <small>(인)</small> )</b></span></div>
<div class="hd r3"><div class="ttl"><span class="logo">高</span><span class="g">2</span><span class="s">학년&nbsp;</span><span class="m">미적분Ⅰ</span><span class="s">과&nbsp;</span><span class="e">중간고사</span><span class="s">&nbsp;문제</span></div>
<div class="dt">시행일 2026년 10월 (&nbsp;&nbsp;&nbsp;)일 - (&nbsp;&nbsp;)교시</div></div>
<div class="bar"></div>
<div class="hd r4"><span>과 정 : ( 2022 개정 교육과정 )</span><span>과목코드 : (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)</span><span>이수학점 : ( 4 )</span><span>문항수 ( 선택형: 18, 서답형: 2 )</span></div>"""

def footer(pg):
    return f"""<div class="ft"><span>이 시험문제의 저작권은 양정고등학교에 있습니다.</span><span class="c"><i>고</i>양 정 고 등 학 교 &lt;{NPAGES}-{pg}&gt;</span><span>무단 복제 및 전재, 상업적 이용을 금지합니다.</span></div>"""

def mcq(n):
    pt, body, ch = Q[n]
    grid = all('\\(' not in c for c in ch)  # ㄱㄴㄷ형 선지는 3+2 배치
    chs = ''.join(f'<span>{CIRC[i]} {c}</span>' for i, c in enumerate(ch))
    ptx = f' <span class="pt">[{pt:.1f}점]</span>'
    body = body.replace('{PT}', ptx) if '{PT}' in body else body + ptx
    return (f'<div class="q" data-id="q{n}"><span class="n">{n}.</span>{body}'
            f'<div class="{"chg" if grid else "ch"}">{chs}</div></div>')

NOTICE = """<div class="notice"><h4>&lt;정기고사 준수사항&gt;</h4>
<p>■ 아래의 내용을 반드시 읽고 시험에 임하시기 바랍니다!</p>
<p>■ 휴대폰 등 전자기기는 전원을 꺼 가방 속에 넣어야 합니다.</p>
<p>■ 선택형 답안지에는 반드시 컴퓨터용 사인펜으로 표기해야 합니다. 답안을 수정할 경우 답안지를 교체하거나 수정테이프를 사용하기 바랍니다.</p>
<p>■ 시험지 아래쪽에 적힌 총 쪽수를 참조하여 받은 시험지의 매수를 확인하기 바랍니다.</p>
<p>■ 정해진 시험 종료 시각을 확인하여 답안지를 미리 작성하기 바랍니다.</p></div>
<div class="sec"><div class="h">&lt;선택형 문제 – 80점&gt;</div><div class="d">선택형 문제(1~18)번의 정답은 반드시<br><u>OMR카드에 컴퓨터용 사인펜으로 명확히 표기</u>하시오.</div></div>"""

SEC2 = """<div class="sec"><div class="h">&lt;서답형 문제 – 20점&gt;</div><div class="d">서답형 문제(19~20)번은 답안지의 해당 칸에 답을 쓰시오.<br>단답형은 답만, <u>서술형은 풀이 과정을 반드시 서술</u>하시오.</div></div>"""

def q19():
    subs = ''.join(f'<div class="sub">({i+1}) {t} <span class="pt">[{p}점]</span></div><div class="ansl" style="--h:{h}mm"></div>'
                   for i, ((t, p), h) in enumerate(zip(Q19S, [14, 22, 0])))
    return f'<div class="q" data-id="q19"><span class="n" style="position:static;margin-left:-6.2mm">단답형 19.</span> {Q19}{subs}</div>'

def q20():
    subs = ''.join(f'<div class="sub">({i+1}) {t} <span class="pt">[{p}점]</span></div>' for i, (t, p) in enumerate(Q20S))
    return f'<div class="q" data-id="q20"><span class="n" style="position:static;margin-left:-6.2mm">서술형 20.</span> {Q20}{subs}</div>'

def slot(html, w=1, fixed=False):
    st = f'flex:{w} 1 0' if not fixed else 'flex:none'
    return f'<div class="slot" style="{st}">{html}</div>'

PAGES = [
    ([slot(NOTICE, fixed=True), slot(mcq(1)), slot(mcq(2), 1.25)], [slot(mcq(3)), slot(mcq(4)), slot(mcq(5), 1.25)]),
    ([slot(mcq(6)), slot(mcq(7))], [slot(mcq(8), 1.45), slot(mcq(9))]),
    ([slot(mcq(10)), slot(mcq(11))], [slot(mcq(12)), slot(mcq(13))]),
    ([slot(mcq(14), 1.25), slot(mcq(15))], [slot(mcq(16)), slot(mcq(17))]),
    ([slot(mcq(18))], [slot(SEC2, fixed=True), slot(q19())]),
    ([slot(q20(), fixed=True), '<div class="memo"><span>풀이 공간</span></div>'],
     ['<div class="memo" style="margin-top:0"><span>풀이 공간</span></div>',
      '<div class="end"><div class="a">수고하셨습니다</div><div class="b">(˘･ᴗ･˘)</div><div class="c">선택형 18문제 = 80점<br>서답형&nbsp; 2문제 = 20점</div></div>']),
]

def build():
    out = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>미적분Ⅰ 중간고사 시험지</title>'
           f'<link rel="stylesheet" href="file://{KATEX}"><style>{CSS}</style></head><body>']
    for i, (L, R) in enumerate(PAGES, 1):
        out.append(f'<div class="page">{header(i)}<div class="body"><div class="col">{"".join(L)}</div>'
                   f'<div class="col">{"".join(R)}</div></div>{footer(i)}</div>')
    out.append('</body></html>')
    open(os.path.join(HERE, 'exam_src.html'), 'w', encoding='utf8').write(''.join(out))

if __name__ == '__main__':
    build()
