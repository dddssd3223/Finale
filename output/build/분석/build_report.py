# -*- coding: utf-8 -*-
import json, re, os, sys, glob, importlib, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); SCR=os.path.join(HERE,'..')
sys.path.insert(0,HERE)
from build3 import font_css, KATEX_CSS
sys.path.insert(0,os.path.join(SCR,'wb2/parts')); sys.path.insert(0,os.path.join(SCR,'wbfull'))
I={}
for f in sorted(glob.glob(os.path.join(SCR,'wb2/parts/items_p*.py'))):
    m=importlib.import_module(os.path.basename(f)[:-3]); I.update(m.I)
W=importlib.import_module('items'); I.update(W.I)
R=[1,2,3,4,5,7,8,9,12,13,15]
DATA={r:json.load(open(os.path.join(HERE,f'r{r}.json'))) for r in R}
L=json.load(open(os.path.join(HERE,'loss.json')))
CIRC='①②③④⑤'
def key_of(src):
    m=re.search(r'_removed\.pdf (0[12]) .*?— (\d+)번',src)
    if m: return ('L' if m.group(1)=='01' else 'C')+m.group(2)
    m=re.search(r'교재 (\d+)쪽.*? (\d+)번',src)
    if m:
        p,n=int(m.group(1)),int(m.group(2))
        if p>=78: return f'T{n}'
        return ('A' if n<=42 else 'B')+str(n)
    return None
def choices_html(ch, ans=None, mark=None):
    if not ch: return ''
    out=[]
    for i,c in enumerate(ch):
        t=c[2:] if c.startswith('T:') else f'\\({c}\\)'
        st=''
        if ans is not None and i+1==ans: st=' class="ok"'
        if mark is not None and i+1==mark and mark!=ans: st=' class="ng"'
        out.append(f'<span{st}>{CIRC[i]} {t}</span>')
    return '<div class="ch">'+''.join(out)+'</div>'
def scores(r):
    d=DATA[r]
    mc=sum(d['PTS'][str(n)] for n in range(1,19) if d['ANS'][str(n)]==d['MARK'][n-1])
    s1=sum(g for *_,g in d['SA'][0][1]); s2=sum(g for *_,g in d['SA'][1][1])
    nmc=sum(1 for n in range(1,19) if d['ANS'][str(n)]==d['MARK'][n-1])
    return mc,s1,s2,mc+s1+s2,nmc
CSS=r"""
@page{size:A4;margin:15mm 14mm 15mm 14mm}
body{font-family:'HB','MJ','GL',serif;font-size:9.6pt;line-height:1.65;margin:0;color:#000;background:#fff}
.katex{font-size:1.02em;font-family:'TN','KaTeX_Main'}
.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
.katex .text,.katex .text *{font-family:'HB','MJ','TN'!important;font-style:normal}
h1{font-family:'GL';font-size:17pt;font-weight:400;margin:0 0 1mm;-webkit-text-stroke:.3pt #000}
.sub{font-size:9.5pt;margin-bottom:4mm}
h2{font-family:'GL';font-size:12.5pt;font-weight:400;margin:6mm 0 2mm;border-bottom:1.3pt solid #000;padding-bottom:1mm;-webkit-text-stroke:.2pt #000;break-after:avoid}
h3{font-family:'GL';font-size:10.5pt;font-weight:400;margin:4mm 0 1.5mm;-webkit-text-stroke:.15pt #000;break-after:avoid}
table{border-collapse:collapse;width:100%;margin:1.5mm 0}
td,th{border:.6pt solid #000;padding:2pt 4pt;text-align:center;font-weight:400;font-size:9pt}
th{background:#eee;-webkit-print-color-adjust:exact;print-color-adjust:exact}
td.l{text-align:left}
.r{color:#c8141a}
.note{border:.7pt solid #000;padding:2.5mm 3.5mm;margin:2mm 0}
.key{border:1.3pt solid #c8141a;padding:2.5mm 3.5mm;margin:2mm 0}
.item{break-inside:avoid;margin:0 0 5mm}
.ihd{background:#222;color:#fff;padding:2pt 6pt;font-family:'GL';font-size:10pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pair{display:flex;gap:3mm;margin-top:1.5mm}
.box{flex:1;border:.7pt solid #000;padding:2mm 3mm;min-width:0}
.box .t{font-family:'GL';font-size:8.8pt;border-bottom:.5pt solid #999;margin-bottom:1mm;padding-bottom:.5mm}
.box.v{border-color:#c8141a}
.ch{display:flex;flex-wrap:wrap;gap:1mm 4mm;margin-top:1mm;font-size:9pt}
.ch .ok{font-weight:700;text-decoration:underline}
.ch .ng{color:#c8141a;text-decoration:line-through}
.kv{display:flex;border:.6pt solid #000;border-top:0}
.kv .k{flex:none;width:23mm;padding:1.5pt 4pt;font-family:'GL';font-size:8.6pt;background:#f2f2f2;border-right:.5pt solid #999;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.kv .v{flex:1;padding:1.5pt 5pt}
.cond{border:.6pt solid #000;padding:2pt 6pt;margin:2pt 0}
.ci{padding-left:2.2em;text-indent:-2.2em}.ck{display:inline-block;width:2.2em;text-indent:0}
.bogi{border:.6pt solid #000;padding:2pt 6pt;margin:3pt 0}.bogi legend{font-size:8.5pt}
.bi{display:flex;gap:4pt}
.fig{text-align:center;margin:3pt 0}
.bar{display:inline-block;height:8pt;background:#555;vertical-align:middle;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.bar.r{background:#c8141a}
"""
h=[]
h.append('<h1>미적분Ⅰ 중간고사 모의고사 결과 분석</h1><div class="sub">채점한 11회분(1·2·3·4·5·7·8·9·12·13·15회) 종합 분석과, 감점이 있었던 부교재 변형 문항의 원본 대조</div>')
# ---- 1. scores
h.append('<h2>1. 회차별 점수</h2>')
rows=''.join(f'<tr><td>{r}회</td><td>{s[4]}/18</td><td>{s[0]:.1f}</td><td>{s[1]}</td><td>{s[2]}</td><td><b>{s[3]:.1f}</b></td><td class="l"><span class="bar{" r" if s[3]<90 else ""}" style="width:{(s[3]-70)*3.2:.0f}pt"></span></td></tr>' for r in R for s in [scores(r)])
h.append(f'<table><tr><th>회차</th><th>선택형 정답</th><th>선택형(80)</th><th>단답형(10)</th><th>서술형(10)</th><th>총점</th><th style="width:40%">70점 기준 막대</th></tr>{rows}</table>')
avg=lambda rs: sum(scores(r)[3] for r in rs)/len(rs)
h.append(f'''<table><tr><th>구간</th><th>시험 구성</th><th>평균</th><th>특징</th></tr>
<tr><td>1–5회</td><td>부교재 중심, 기본 변형</td><td>{avg([1,2,3,4,5]):.1f}</td><td class="l">선택형은 거의 만점. 감점은 서답형(외부 단답, 서술 근거)에 집중</td></tr>
<tr><td>7–9회</td><td>부교재 고난도, 변형 강화</td><td>{avg([7,8,9]):.1f}</td><td class="l">8회 만점. 9회부터 변형 강도가 오르며 경우 누락이 드러남</td></tr>
<tr><td>12–15회</td><td>실전 구성(앞 쉬움, 뒤 4문항 고난도, 고3 외부)</td><td>{avg([12,13,15]):.1f}</td><td class="l">12회에서 78.1로 하락 후 13회 91.1, 15회 87.1로 회복·안정</td></tr></table>''')
# ---- 2. loss categories
from collections import defaultdict
cat=defaultdict(float); cnt=defaultdict(int); typ=defaultdict(float)
for r,i,l,t,c,s in L:
    c2={'계산(시간)':'계산','계산 이월':'계산 이월'}.get(c,c); cat[c2]+=l; cnt[c2]+=1; typ[t]+=l
tot=sum(cat.values())
h.append('<h2>2. 감점 원인 분석</h2>')
h.append(f'<div>11회 동안 감점 합계는 <b>{tot:.1f}점</b>(회당 평균 {tot/11:.1f}점)입니다. 부교재 변형에서 {typ["부교재"]:.1f}점, 외부 문항에서 {typ["외부"]:.1f}점이 빠졌습니다.</div>')
rows=''.join(f'<tr><td>{c}</td><td>{cnt[c]}</td><td>{v:.1f}</td><td>{v/tot*100:.0f}%</td><td class="l"><span class="bar{" r" if v/tot>0.15 else ""}" style="width:{v*4:.0f}pt"></span></td></tr>' for c,v in sorted(cat.items(),key=lambda x:-x[1]))
h.append(f'<table><tr><th>원인</th><th>건수</th><th>감점</th><th>비율</th><th style="width:42%">막대</th></tr>{rows}</table>')
h.append('''<div class="key"><b>핵심 진단</b>
<ol style="margin:1mm 0 0 0;padding-left:5mm">
<li><b>경우 누락이 1위</b>(약 3분의 1). 2·9·12·13·15회에 반복. 일반적인 경우를 풀면 끝났다고 판단하고, 중근·반대 방향 점프·제거 가능한 점·차수가 낮아지는 경우를 확인하지 않습니다.</li>
<li><b>계산과 계산 이월</b>이 합쳐 2위. 마지막 단계 계산 실수, 그리고 앞 소문항의 식·값을 그대로 다음 소문항에 가져가는 실수(3·4·15회 서술).</li>
<li><b>대상 착각</b>: 묻는 것이 \(g(a)\)인지 \(h(1)\)인지, \(f/g\)인지 \(g/f\)인지, "모든 값의 합"인지를 놓침(3·4·7·12회).</li>
<li>개념 자체가 틀린 경우는 우함수의 도함수 부호(1회), 곱의 미분가능성(12회) 정도로 적습니다.</li>
</ol></div>''')
h.append('<h3>전체 감점 목록</h3>')
rows=''.join(f'<tr><td>{r}회</td><td>{i}</td><td>{l:g}</td><td>{t}</td><td>{c}</td><td class="l">{s}</td></tr>' for r,i,l,t,c,s in L)
h.append(f'<table><tr><th>회차</th><th>문항</th><th>감점</th><th>출처</th><th>원인</th><th>내용</th></tr>{rows}</table>')
# ---- 3. strengths & issues
h.append('<h2>3. 강점과 변화</h2>')
h.append('''<ul>
<li><b>선택형 1–15번은 매우 안정적</b>: 11회 중 4회가 선택형 만점, 나머지도 대부분 1문항 오답.</li>
<li><b>킬러 대응</b>: 12·13·15회 17번(수능·평가원급 변형)을 모두 정답.</li>
<li><b>단답형</b>: 학교 기출 수준(15회)에서는 만점. 고3 22번급(12회)에서만 크게 흔들림.</li>
<li><b>개선된 습관</b>: 12회 이후 원본 기억 의존과 시간 압박으로 인한 쉬운 문항 실수가 사라짐.</li>
<li><b>남은 습관</b>: 경우 누락은 매 회 1건 정도로 줄었지만 사라지지 않았고, 서술형에서 앞 단계 식을 그대로 가져가는 실수가 15회에 다시 나옴.</li>
</ul>''')
h.append('''<div class="note"><b>제작상 문제 (알려 드려야 할 점)</b><br>
외부 문항 사용 기록 표(1–6회분)를 확인하지 않아, 같은 외부 원본이 다시 쓰였습니다.
11회 18번(5회 18번과 원본 같음), 13회 18번(1회 18번과 원본·변형 거의 동일), 13회 단답형(3회 18번 원본),
14회 18번(2회 18번 원본), 15회 18번(4회 18번 원본).
따라서 13·15회 18번 정답에는 익숙함이 일부 작용했을 수 있습니다(4회 18번은 틀렸고 15회 같은 원본은 맞혔으므로 학습 효과도 있음).
사용 기록은 이 내용으로 바로잡았습니다.</div>''')
h.append('<h2>4. 시험 당일 체크리스트</h2>')
h.append('''<div class="key"><ol style="margin:0;padding-left:5mm">
<li><b>경우 점검 3초</b>: 중근·근의 일치 / 등호·경계값 / 반대 방향(점프, 부호) / 제거 가능한 점 / 차수가 낮아지는 경우.</li>
<li><b>묻는 대상에 밑줄</b>: \(f\)·\(g\), 분자·분모, "모든 … 합/곱/개수".</li>
<li><b>단계형은 분모부터 다시 확인</b>: 앞 소문항 식을 그대로 쓰지 말 것. 답이 나오면 \(x=2.1\) 같은 값을 넣어 대략 맞는지 확인.</li>
<li><b>절댓값 극한</b>: 분자가 갇혀 있으면 중근만, 풀려 있으면 중근 + 기울기 합 \(0\)인 꺾인 점.</li>
<li><b>서술형</b>: 남긴 경우뿐 아니라 버린 경우와 그 이유를 한 줄씩.</li>
<li><b>시간</b>: 1–8번 빠르게(대입 확인 1회), 9–14번 2분 넘으면 표시 후 넘김, 남은 시간은 15번 이후.</li>
</ol></div>''')
# ---- Part 2
h.append('<h2 style="break-before:page">5. 변형 문항 원본 대조 (감점이 있었던 부교재 변형)</h2>')
h.append('<div>외부 문항은 제외했습니다. 각 문항에서 원본과 변형을 나란히 놓고, 무엇을 바꿨는지와 그 변화가 감점과 어떻게 연결되는지를 정리했습니다. 변형 쪽 선택지의 <u>밑줄</u>은 정답, <span class="r">취소선</span>은 내가 고른 답입니다.</div>')
REASON={(r,i):(c,s) for r,i,l,t,c,s in L}
def orig_box(key):
    q,ch,ans,srcs=I[key]
    a=ans if (isinstance(ans,str) and ans in CIRC) else ans
    return (f'<div class="box"><div class="t">원본 · 부교재 {key} · {srcs}</div>{q}'
            + choices_html(ch, CIRC.index(ans)+1 if ch and ans in CIRC else None)
            + (f'<div style="margin-top:1mm"><b>정답</b> {ans}</div>' if not ch else '') + '</div>')
mc_items=[(1,10),(2,17),(3,16),(9,11),(12,3),(12,15),(13,16),(15,16)]
k=0
for r,n in mc_items:
    d=DATA[r]; D=d['D'][str(n)]; key=key_of(D[1]); k+=1
    q,ch=d['Q'][str(n)]; q=q.replace('{PT}','').replace('fig17.svg','r2_fig17.svg' if r==2 else 'fig17.svg')
    ans=d['ANS'][str(n)]; mk=d['MARK'][n-1]
    c,s=REASON[(r,str(n))]
    h.append(f'<div class="item"><div class="ihd">[{k}] {r}회 {n}번 · {d["PTS"][str(n)]}점 · 원본 {key}</div>')
    h.append('<div class="pair">'+orig_box(key)+f'<div class="box v"><div class="t">변형 · {r}회 {n}번</div>{q}{choices_html(ch,ans,mk)}</div></div>')
    h.append(f'<div class="kv" style="border-top:.6pt solid #000;margin-top:1.5mm"><div class="k">변형 포인트</div><div class="v">{D[3]}</div></div>')
    h.append(f'<div class="kv"><div class="k">난도</div><div class="v">원본 {D[2]} → 변형 {D[4]}</div></div>')
    h.append(f'<div class="kv"><div class="k">변형 풀이</div><div class="v">{D[0]}</div></div>')
    h.append(f'<div class="kv"><div class="k">내 답 / 원인</div><div class="v"><span class="r">{CIRC[mk-1]} 표기 (정답 {CIRC[ans-1]})</span> · <b>{c}</b>: {s}</div></div></div>')
sa_items=[(1,['서술(2)']),(2,['서술(2)']),(3,['서술(2)','서술(3)']),(4,['서술(2)','서술(3)']),(5,['서술(2)']),(7,['서술(2)','서술(3)']),(9,['서술(2)','서술(3)']),(12,['서술(2)']),(15,['서술(2)(3)'])]
for r,its in sa_items:
    d=DATA[r]; S=d['S2']; key=key_of(S['d']['src']); k+=1
    lost=sum(l for rr,i,l,*_ in L if rr==r and i in its)
    subs=''.join(f'<div>({j+1}) {t} [{p}]</div>' for j,(t,p) in enumerate(S['sub']))
    got=' / '.join(f'{lab} {g}/{p}' for lab,p,g in d['SA'][1][1])
    h.append(f'<div class="item"><div class="ihd">[{k}] {r}회 서술형 1 · 원본 {key} · 감점 {lost:g}점</div>')
    h.append('<div class="pair">'+orig_box(key)+f'<div class="box v"><div class="t">변형 · {r}회 서술형 1 (2/4/4점 단계형)</div>{S["q"]}{subs}</div></div>')
    h.append(f'<div class="kv" style="border-top:.6pt solid #000;margin-top:1.5mm"><div class="k">변형 포인트</div><div class="v">{S["d"]["var"]}</div></div>')
    h.append(f'<div class="kv"><div class="k">정답</div><div class="v">{" / ".join(S["d"]["ans"])}</div></div>')
    h.append(f'<div class="kv"><div class="k">채점 기준</div><div class="v">{"<br>".join(S["d"]["sol"])}</div></div>')
    rs=' '.join(f'<b>{c}</b>: {s}' for rr,i,l,t,c,s in L if rr==r and i in its)
    h.append(f'<div class="kv"><div class="k">내 점수 / 원인</div><div class="v"><span class="r">{got}</span><br>{rs}</div></div></div>')
h.append('''<h2>6. 대조에서 보이는 패턴</h2><div class="key"><ul style="margin:0;padding-left:5mm">
<li><b>"특수 → 일반" 변형에서 주로 틀림</b>: 원본에서는 한 경우만 생기던 것이 변형에서 두 경우가 되거나(12회 15번, 13회 16번), 원본에 없던 예외(제거 가능한 점, 15회 16번)가 추가되면 원본 풀이 흐름대로 가다가 새로 생긴 경우를 놓칩니다.</li>
<li><b>원본 풀이를 기억하는 문항일수록 위험</b>: 3회 16번(원본은 \(h(1)\)을 묻는 구조와 비슷), 12회 단답(원본 중간값) 모두 원본의 결론이 변형에서 그대로 쓰이지 않습니다.</li>
<li><b>서술형은 원본보다 단계가 늘어난 곳에서 감점</b>: 변형에서 추가된 중간 단계(중근 경우, 다른 분모)에서 앞 단계 결과를 그대로 쓰거나 경우를 빠뜨립니다.</li>
<li><b>대처</b>: 익숙한 문제일수록 "원본과 무엇이 다른가"를 첫 줄에 적고 시작하세요. 바뀐 조건이 곧 새로 생긴 경우입니다.</li>
</ul></div>''')
html0=f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{"".join(h)}</body></html>'
html=re.sub(r'\\\\\[\d+pt\]', r'\\\\ ', html0)
_f=lambda m:m.group(0).replace('&lt;','<').replace('&gt;','>')
html=re.sub(r'\\\(.*?\\\)',_f,html,flags=re.S)
html=re.sub(r'\\\[.*?\\\]',_f,html,flags=re.S)
open(os.path.join(HERE,'rep_src.html'),'w').write(html)
subprocess.run(['node',os.path.join(HERE,'render3.js'),'rep_src.html','rep_tmp.pdf','bg'],cwd=HERE,check=True)
os.replace(os.path.join(HERE,'rep_tmp.pdf'),os.path.join(HERE,'analysis.pdf'))
