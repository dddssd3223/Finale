# -*- coding: utf-8 -*-
"""양정고 2026 정기고사 3회(1학기 중간·기말 대수, 2학기 중간 미적분Ⅰ) 부교재 변형 분석"""
import os, sys, json, subprocess, html
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
CON = os.path.join(HERE, '..', 'aim', 'concept')
sys.path.insert(0, CON)
from build import font_css, KATEX_CSS

EX = [('1중', '1학기 중간', '대수 · 지수~삼각함수의 그래프', 's1_mid.json'),
      ('1기', '1학기 기말', '대수 · 삼각함수의 활용~수학적 귀납법', 's1_final.json'),
      ('2중', '2학기 중간', '미적분Ⅰ · 함수의 극한~미분', 's2_mid.json')]
D = {k: json.load(open(os.path.join(HERE, f))) for k, _, _, f in EX}
E = lambda s: html.escape(str(s))

def kind(k):
    if '평가원' in k or '대표' in k: return 'P'
    if 'Level' in k: return 'L'
    if '자체' in k or '외부' in k: return 'S'
    return 'E'
KN = {'P': ('평가원', '#d0312d'), 'E': ('EBS 유형', '#7a7a7a'), 'L': ('Level Up', '#1f4fd6'), 'S': ('자체·외부', '#7b3fb0')}
def ct(c): return c.split('(')[0].strip()
def lab(x): return str(x.get('label') or x['no']).replace('서답형', '서')
def diff(x):
    t = x['diff_effect']
    return 'up' if '어려워' in t.split(':')[0].split('—')[0] else ('down' if '쉬워' in t.split(':')[0].split('—')[0] else 'eq')
def band(x, ex):
    l = lab(x)
    if l.startswith('서') or (ex == '2중' and l in ('19', '20')): return '서답'
    n = int(l)
    return '1–4' if n <= 4 else '5–8' if n <= 8 else '9–12' if n <= 12 else '13–16' if n <= 16 else '17–18'
BANDS = ['1–4', '5–8', '9–12', '13–16', '17–18', '서답']
def dot(k): return f'<span class="dot" style="background:{KN[k][1]}"></span>'
def det(x):
    d = x['change_detail']
    return d if isinstance(d, list) else [s.strip() for s in str(d).replace('; ', '\n').split('\n') if s.strip()]

ALL = [(e, x) for e, *_ in EX for x in D[e]]
N = len(ALL)
c_kind = Counter(kind(x['src_kind']) for _, x in ALL)
c_ct = Counter(ct(c) for _, x in ALL for c in x['change_type'])
only_num = [(e, x) for e, x in ALL if set(ct(c) for c in x['change_type']) <= {'숫자 변경', '형식 변경'}]
c_diff = Counter(diff(x) for _, x in ALL)

CSS = r"""
@page{size:A4;margin:13mm 12mm 12mm}
html,body{margin:0;background:#fff}
body{font-family:'HB','GL';font-size:8.8pt;color:#111;line-height:1.45}
h1{font-family:'GY','GL';font-size:16.5pt;text-align:center;margin:0 0 2pt;font-weight:400}
.sub{text-align:center;color:#555;font-family:'GL';font-size:9pt;margin-bottom:7pt}
.tag{display:inline-block;background:#111;color:#fff;padding:2pt 8pt;font-family:'GL';font-size:8.5pt;letter-spacing:1pt}
h2{font-family:'GY','GL';font-weight:400;font-size:12pt;margin:10pt 0 5pt;border-bottom:1.2pt solid #222;padding-bottom:2pt}
h3{font-family:'GY','GL';font-weight:400;font-size:10pt;margin:7pt 0 3pt;color:#1f4e9a}
table{border-collapse:collapse;width:100%}
th,td{border:.6pt solid #aaa;padding:2pt 4pt;vertical-align:middle;text-align:center;font-size:8pt;line-height:1.35}
th{background:#eef0f3;font-family:'GL';font-weight:400}
td.l{text-align:left}
.sm{font-size:7.3pt;color:#555}
.dot{display:inline-block;width:6.5pt;height:6.5pt;border-radius:50%;margin-right:2pt;vertical-align:-.3pt}
.cards{display:flex;gap:6pt;margin:4pt 0 6pt}
.cards>div{flex:1;border:.8pt solid #bbb;border-radius:3pt;padding:4pt 6pt;text-align:center}
.cards b{display:block;font-family:'GY','GL';font-weight:400;font-size:14pt;color:#1f4e9a}
.cards span{font-size:7.8pt;color:#444}
.key{background:#f5f7fb;border-left:3pt solid #1f4e9a;padding:5pt 9pt;margin:4pt 0}
.key li{margin:1.5pt 0}
.ct{display:inline-block;border-radius:6pt;padding:0 4pt;margin:.5pt 1pt;font-family:'GL';font-size:6.9pt;background:#eef0f3;color:#333;white-space:nowrap}
.up{color:#d0312d}.down{color:#1f8a4c}.eq{color:#777}
.pb{break-before:page}
tr{break-inside:avoid}
.case{border:.8pt solid #999;border-radius:3pt;margin:0 0 8pt;break-inside:avoid}
.case .hd{display:flex;gap:6pt;align-items:center;background:#f2f2f2;border-bottom:.6pt solid #ccc;padding:3pt 8pt;font-family:'GY','GL';font-size:9pt}
.case .hd .r{margin-left:auto;font-family:'GL';font-size:7.8pt;color:#666}
.pair{display:flex}
.pair>div{flex:1;padding:4pt;text-align:center}.pair>div:first-child{border-right:.6pt dashed #bbb}
.pair img{max-width:100%;max-height:205pt}
.cap{font-family:'GL';font-size:7.4pt;color:#888;margin-bottom:2pt;text-align:left}
.cd{border-top:.6pt dashed #ccc;padding:3pt 9pt 4pt;font-size:8.1pt;background:#fffaf2}
.cd li{margin:.5pt 0}
.hm td{vertical-align:top;text-align:left;font-size:7.6pt}
"""

def overview():
    rows = []
    def r(name, f): rows.append(f'<tr><td class="l">{name}</td>' + ''.join(f'<td class="l">{f(e)}</td>' for e, *_ in EX) + '</tr>')
    def src(e):
        c = Counter(kind(x['src_kind']) for x in D[e])
        return ' '.join(f'{dot(k)}{KN[k][0]} {c[k]}' for k in 'PELS' if c[k])
    r('출처 구성', src)
    r('가장 많이 쓴 변형', lambda e: ', '.join(f'{k} {v}' for k, v in Counter(ct(c) for x in D[e] for c in x['change_type']).most_common(3)))
    r('숫자만 바꾼 문항', lambda e: ', '.join(lab(x) for f, x in only_num if f == e) + '번')
    r('원문 대비 난도', lambda e: (lambda c: f'<span class="eq">같음 {c["eq"]}</span> · <span class="up">어려워짐 {c["up"]}</span> · <span class="down">쉬워짐 {c["down"]}</span>')(Counter(diff(x) for x in D[e])))
    r('고배점 킬러 출처', lambda e: {'1중': '15·17·18번 평가원 22·21·18번급(2026 6월 22번 등), 16번 대표기출→보기형',
                                   '1기': '9번 2010 수능 30번, 15번 2025 9월 22번, 16번 2026 9월 20번, 17번 Level Up, 18번 자체',
                                   '2중': '9번 2025 9월 21번, 12번 2014 수능 28번, 16번 2024 9월 15번, 17·18번 Level Up 심화, 20번 2025 수능 21번'}[e])
    r('서답형 구성', lambda e: {'1중': '서1 평가원 4점(2021 6월 14번) 서술화 · 서2 부교재 밖 고난도',
                              '1기': '서1 평가원 4점(2022 9월 12번) 3단계 서술 · 서2 교과서형 귀납법 증명',
                              '2중': '19번 자체 기본 논증(미분가능성) · 20번 평가원 킬러(2025 수능 21번) 3단계'}[e])
    head = '<tr><th style="width:15%">항목</th>' + ''.join(f'<th>{n}<div class="sm">{s}</div></th>' for _, n, s, _ in EX) + '</tr>'
    return f'<table>{head}{"".join(rows)}</table>'

def heatmap():
    head = '<tr><th style="width:9%">번호대</th>' + ''.join(f'<th>{n}</th>' for _, n, _, _ in EX) + '<th style="width:30%">공통 패턴</th></tr>'
    pat = {'1–4': '유형 EBS 기본 + 최신 평가원 3점. 숫자·계수만 교체가 대부분',
           '5–8': '유형 EBS. 숫자·조건 변경. 2학기엔 Level Up이 6·7번까지 내려옴',
           '9–12': '평가원 4점(21번급 포함) + Level Up/대표기출. 함수 교체·단답→선지',
           '13–16': 'Level Up·유형 후반·평가원. 구조 변경·조건 추가로 난도 상승 구간',
           '17–18': '평가원 킬러 또는 Level Up 심화, 1기 18번은 자체. 소재 두 개 결합',
           '서답': '하나는 평가원 4점~킬러를 단계형으로, 하나는 기본 논증·교과서형'}
    rows = ''
    for b in BANDS:
        rows += f'<tr><td><b>{b}</b></td>'
        for e, *_ in EX:
            its = [x for x in D[e] if band(x, e) == b]
            rows += '<td>' + '<br>'.join(f'{dot(kind(x["src_kind"]))}{lab(x)}번 <span class="sm">{"·".join(ct(c).replace(" 변경","").replace(" 교체","교체") for c in x["change_type"][:2])}</span> <span class="{diff(x)}">{"▲" if diff(x)=="up" else "▼" if diff(x)=="down" else "="}</span>' for x in its) + '</td>'
        rows += f'<td class="l">{pat[b]}</td></tr>'
    return f'<table class="hm">{head}{rows}</table><div class="sm" style="margin-top:2pt">{" ".join(dot(k)+KN[k][0] for k in "PELS")} · 원문 대비 <span class="up">▲어려워짐</span> <span class="eq">=같음</span> <span class="down">▼쉬워짐</span></div>'

TECH = [
 ('숫자·계수만 교체', '1중 1·3·9, 1기 3·5·6, 2중 3·7', '구조와 풀이 순서가 그대로. 앞번호에 집중. 첨자를 한 칸 밀거나(1기 3·10) 계수를 바꿔 답만 달라짐'),
 ('단답형 → 5지선다', '2중 8·9·10·12·13·15·17, 1기 9·10·15', '부교재 단답형을 선지형으로 바꾸면서 숫자도 같이 바꿈. 원문 답을 외워도 소용없음'),
 ('식·함수 교체 (풀이 도구 유지)', '1중 15·17(지수↔로그), 1기 9·12(등차↔등비), 1중 서1(sin→cos), 2중 18(이차→사차), 2중 20', '같은 핵심 도구(진수 비교, 등비중항, 고정점·판별식)를 다른 함수에 적용'),
 ('절댓값 위치 이동', '1중 10·12·14, 2중 16', '|f+f|→|cos|, −|tan3x|→−tan|3x|, 따로 정한 값 −|x−2| 등. 대칭·접기 해석이 바뀜'),
 ('구간·경우 늘리기', '2중 12, 1중 13', '구간 2개→3개로 특수한 a(점프 상쇄)를 따로 확인하게 함. 난도 상승의 주 수단'),
 ('같은 그림, 다른 질문', '2중 1·17', '그래프는 그대로 두고 묻는 극한을 바꿈. 17번은 g/f → 합성 f∘g로 심화'),
 ('주어진 것 ↔ 구하는 것', '1기 11, 1중 4·11', '사인법칙 등을 역방향으로 적용'),
 ('보기형 변환·ㄷ 함정', '1중 16·18', '원문 질문을 ㄷ으로 넣고 숫자를 살짝 틀리게(1083→1075), 참이던 ㄴ을 거짓으로'),
 ('풀이 안내 제거', '1기 16', '평가원 빈칸 채우기(가)(나)(다)의 안내를 지우고 결과만 물음 → 혼자 풀이 구성'),
 ('단계형 서술화', '1중 서1, 1기 서1, 2중 20', '평가원 4점·킬러를 (1)(2)(3)으로 쪼개 앞 단계 답이 다음 단계 입력이 됨'),
 ('출처 두 개 결합', '1중 17·18, 2중 14·15, 1기 18', '한 문항의 구조 + 다른 문항의 함수·조건. 자체 문항도 부교재 소재 조합'),
 ('도형 조건 추가', '1기 8·14', '삼각형 문제에 원·지름 조건을 씌워 한 단계 추가'),
]
def tech():
    return '<table><tr><th style="width:21%">변형 기법</th><th style="width:27%">사례 문항</th><th>내용</th></tr>' + ''.join(
        f'<tr><td class="l"><b>{a}</b></td><td class="l sm">{b}</td><td class="l">{c}</td></tr>' for a, b, c in TECH) + '</table>'

def itemtable(e):
    rows = ''
    for x in D[e]:
        k = kind(x['src_kind'])
        sp = f'p.{x["src_page"]} #{x["src_no"]}' if x.get('src_page') and x.get('src_no') else '—'
        org = E(str(x.get('src_origin') or '').split(' (')[0].split(' —')[0])[:46]
        cts = ''.join(f'<span class="ct">{ct(c)}</span>' for c in x['change_type'])
        dd = '<br>'.join('· ' + E(s)[:120] for s in det(x)[:3])
        d = diff(x)
        rows += (f'<tr><td>{lab(x)}</td><td>{float(x["pts"]):.1f}</td><td class="l">{dot(k)}{sp}<div class="sm">{E(x["src_kind"])}<br>{org}</div></td>'
                 f'<td class="l">{cts}</td><td class="l" style="font-size:7.4pt">{dd}</td>'
                 f'<td class="{d}">{"어려워짐" if d=="up" else "쉬워짐" if d=="down" else "같음"}</td></tr>')
    return ('<table><tr><th style="width:5%">번호</th><th style="width:5%">배점</th><th style="width:20%">부교재 출처</th><th style="width:17%">변형 유형</th><th>무엇이 바뀌었나</th><th style="width:7%">난도</th></tr>'
            + rows + '</table>')

CASES = [
 ('2중', '3', '숫자만 교체', '3번 자리 — 원문 그대로 구조, 숫자만'),
 ('1중', '15', '지수 → 로그 + 조건 교체', '평가원 22번급을 15번 자리로 · 쉬워짐'),
 ('1중', '16', '대표기출 → 보기형', 'ㄷ에 원문 질문을 넣고 숫자로 함정'),
 ('1기', '16', '풀이 안내 제거 + 수치 변경', '빈칸 채우기 → 5지선다 · 어려워짐'),
 ('2중', '12', '구간 2개 → 3개', '특수한 a 확인 단계 추가 · 어려워짐'),
 ('2중', '17', '같은 그래프 · 합성함수 심화', 'Level Up 심화 변형 · 1등급 변별'),
 ('2중', '20', '평가원 킬러 → 3단계 서답', '2025 수능 21번 · 고정점 이동'),
 ('1기', '서답형1', '평가원 4점 → 3단계 서술', '5지선다 → (1)(2)(3) 서술'),
]
def cases():
    out = ''
    for e, l, t, r in CASES:
        x = next(v for v in D[e] if lab(v) == lab({'no': l}) or str(v.get('label')) == l or str(v['no']) == l)
        name = dict((a, b) for a, b, _, _ in EX)[e]
        sp = f'부교재 p.{x["src_page"]} #{x["src_no"]} · {E(str(x["src_origin"]).split(" (")[0])}'
        out += (f'<div class="case"><div class="hd"><span style="color:#d0312d">{name} {lab(x)}번</span><span>{t}</span><span class="r">{r}</span></div>'
                f'<div class="pair"><div><div class="cap">부교재 원문 · {sp}</div><img src="file://{x["src_img"]}"></div>'
                f'<div><div class="cap">실제 시험</div><img src="file://{x["exam_img"]}"></div></div>'
                f'<div class="cd"><ul style="margin:0;padding-left:11pt">' + ''.join(f'<li>{E(s)}</li>' for s in det(x)[:4])
                + f'<li style="list-style:none;margin-left:-11pt;color:#1f4e9a">유지된 핵심: {E(x["core_kept"])}</li></ul></div></div>')
    return out

def build(out):
    up = c_diff['up']; dn = c_diff['down']; eq = c_diff['eq']
    head = (f'<div style="text-align:right"><span class="tag">FINAL PAGE · 출제 습관 분석</span></div>'
            f'<h1>양정고 2026 정기고사 3회 · 부교재 변형 분석</h1>'
            f'<div class="sub">1학기 중간·기말(대수) + 2학기 중간(미적분Ⅰ) · 같은 출제진 · 60문항 전부 부교재 원문과 1:1 대조</div>'
            f'<div class="cards"><div><b>0 / {N}</b><span>원문 그대로 낸 문항</span></div>'
            f'<div><b>{N - c_kind["S"]} / {N}</b><span>부교재에서 출제 ({(N - c_kind["S"]) / N * 100:.0f}%)</span></div>'
            f'<div><b>{c_kind["P"]}문항</b><span>평가원 기출·대표기출 출처</span></div>'
            f'<div><b>{len(only_num)}문항</b><span>숫자만 바꿈 (대부분 1–9번)</span></div>'
            f'<div><b>{eq} · {up} · {dn}</b><span>원문 대비 같음·어려워짐·쉬워짐</span></div></div>'
            '<h2>1. 세 시험 비교</h2>' + overview() +
            '<div class="key"><b style="font-family:GY,GL;font-weight:400">핵심 결론</b><ol style="margin:2pt 0 0;padding-left:13pt">'
            '<li><b>원문 그대로는 0문항, 풀이 핵심은 거의 100% 유지.</b> 숫자·함수·조건·질문은 바꾸지만 "무엇으로 푸는가"는 원문과 같다. → 원문 답이 아니라 <b>풀이 도구</b>를 익혀야 한다.</li>'
            f'<li><b>평가원 기출이 뼈대</b>({c_kind["P"]}/{N}). 책에 실린 최신 평가원(2026학년도 6·9월·수능, 2025 수능 21번 등)은 거의 다 나왔고, 고배점·서답형은 대부분 평가원 출처.</li>'
            '<li><b>번호대 역할이 고정</b>: 1–8 유형 EBS·평가원 3점 소폭 변형 → 9–12 평가원 4점 → 13–18 Level Up·평가원 킬러 구조 변형 → 서답형 1개는 평가원을 단계형으로.</li>'
            '<li><b>2학기에 바뀐 점</b>: Level Up이 2→4→6문항으로 늘고 6·7번까지 내려옴(앞부분이 어려워진 이유). 부교재 단답형을 5지선다로 바꾼 문항이 7개로 급증.</li>'
            '<li><b>난도 조절 수단</b>: 어려워진 문항은 대부분 13–18번(구간·경우 늘리기, 소재 결합, 안내 제거), 쉬워진 문항은 킬러를 친절하게 만든 경우(1중 15, 2중 15·20)도 있다.</li>'
            '<li><b>자체·외부 문항은 시험당 1~2개</b>, 위치는 14·18·서답형. 자체 문항도 부교재 소재(거리식·도형 구조)를 조합한다.</li></ol></div>')
    p2 = ('<h2 class="pb">2. 번호대별 출제 지도</h2>' + heatmap() +
          '<h2>3. 변형 기법 사전</h2>' + tech() +
          '<div class="sm" style="margin-top:3pt">집계(중복 포함): ' + ', '.join(f'{k} {v}' for k, v in c_ct.most_common()) + '</div>')
    p3 = ''.join(f'<h2 class="pb">{4 + i}. {n} 문항별 대조 <span class="sm">({s})</span></h2>' + itemtable(e) for i, (e, n, s, _) in enumerate(EX))
    p4 = '<h2 class="pb">7. 원문 ↔ 실제 대표 사례</h2>' + cases()
    p5 = ('<h2 class="pb">8. 미적분Ⅰ 기말 출제 예측과 모의고사 제작 규칙</h2>'
          '<table><tr><th style="width:12%">번호대</th><th style="width:30%">예상 출처</th><th>예상 변형 · 모의고사 제작 규칙</th></tr>'
          '<tr><td>1–4</td><td class="l">04단원·적분 유형 EBS 기본, 책의 최신 평가원 3점</td><td class="l">숫자·계수만 교체. 원문 구조 유지. 정적분 계산·증감 기본은 여기</td></tr>'
          '<tr><td>5–8</td><td class="l">유형 EBS + <b>Level Up 1~2개</b></td><td class="l">2학기 중간처럼 앞부분에 Level Up을 숫자만 바꿔 배치 → 앞부분 시간 압박 재현</td></tr>'
          '<tr><td>9–12</td><td class="l">평가원 4점(21번급 1개 포함), 대표기출</td><td class="l">부교재 단답형 → 5지선다, 숫자 동시 변경. 9번 자리에 평가원 21번급을 둘 수 있음</td></tr>'
          '<tr><td>13–16</td><td class="l">Level Up·평가원 4점, 자체 1개 가능</td><td class="l">구간·경우 늘리기, 절댓값 위치 이동, 함수 교체(삼차→사차), 같은 그래프 다른 질문</td></tr>'
          '<tr><td>17–18</td><td class="l">책의 최신 평가원 킬러, Level Up 심화</td><td class="l">함수 교체 + 조건 추가, 소재 두 개 결합. 풀이 도구는 원문 그대로</td></tr>'
          '<tr><td>서답형</td><td class="l">평가원 킬러 1 + 기본 논증 1</td><td class="l">킬러를 (1)(2)(3) 연쇄 단계형으로(앞 답이 뒤 입력). 다른 하나는 증감표·극값 판정·정적분 성질 같은 교과서형 논증</td></tr></table>'
          '<div class="key"><b style="font-family:GY,GL;font-weight:400">기말 모의고사에 그대로 적용할 규칙</b><ol style="margin:2pt 0 0;padding-left:13pt">'
          '<li>부교재 문항을 원문 그대로 내지 않는다. 대신 위 <b>변형 기법 사전</b>에서 번호대에 맞는 기법을 골라 적용한다.</li>'
          '<li>출처 비율 목표: 평가원 35–40% · 유형 EBS 30% · Level Up 25% · 자체 1–2문항(14·18·서답 자리).</li>'
          '<li>책에 실린 <b>가장 최근 평가원 문항은 전부</b> 최소 1회, 고난도는 2회 이상 다른 변형으로 낸다.</li>'
          '<li>부교재 단답형 문항은 5지선다로 바꾸는 연습판을 따로 만든다(2학기 중간 7문항 사례).</li>'
          '<li>킬러는 원문 풀이 도구를 유지한 채 함수·조건만 바꿔 2–3가지 판으로 반복한다(2025 수능 21번이 3번 연습으로 적중한 방식).</li>'
          '<li>서답형 킬러 채점에 "앞 단계 답 대입 검산" 항목을 넣어 연쇄 감점을 훈련한다.</li></ol></div>'
          '<div class="sm">한계: 1중 5·6번은 출처표상 "유형 대표 문항"이라 가장 가까운 부교재 문항으로, 1기 1·2번은 유사 후보로 대응시켰다(신뢰도 낮음). 1기 부교재 스캔에 p.107이 빠져 있다. '
          '1학기는 대수, 2학기는 미적분Ⅰ이라 내용이 아니라 출제 습관을 비교한 것이다.</div>')
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{p2}{p3}{p4}{p5}</body></html>')
    open(os.path.join(HERE, 'rep_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(CON, 'render3.js'), os.path.join(HERE, 'rep_src.html'), os.path.join(HERE, 'rep_tmp.pdf'), 'bg'], cwd=CON, check=True)
    os.replace(os.path.join(HERE, 'rep_tmp.pdf'), out)
    print(N, c_kind, c_ct, len(only_num), c_diff)

if __name__ == '__main__':
    build(sys.argv[1])
