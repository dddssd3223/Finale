# -*- coding: utf-8 -*-
import sys, re, json, os, subprocess
sys.argv = ['build.py']
import build
from build import W, segs, tpl_paras, pack, escape, ITEMS, ANS, HERE
from eqconv import to_latex
from solcontent import S, S19, S20
from content import P

CIRC = '①②③④⑤'
def ans_text(n):
    k = ANS[n] - 1
    c = P[n]['blocks'][-1][1][k]
    return CIRC[k] + ' ' + (c[2:] if c.startswith('T:') else f'${c}$')

LINES = []   # (kind, text)
def L(kind, text): LINES.append((kind, text))

L('title', '정답 및 해설')
L('h', '[빠른 정답]')
L('p', '   '.join(f'{n}. {CIRC[ANS[n]-1]}' for n in range(1, 10)))
L('p', '   '.join(f'{n}. {CIRC[ANS[n]-1]}' for n in range(10, 19)))
L('p', f"19. (1) ${S19['ans'][0]}$  (2) ${S19['ans'][1]}$  (3) ${S19['ans'][2]}$")
L('p', "20. (1) 풀이 참조  (2) $a=-1$, $k= sqrt 2$  (3) $x=0$, 우미분계수 $-2$")
L('p', '정답 분포: ' + ', '.join(f'{CIRC[i]} {sum(1 for v in ANS.values() if v == i+1)}개' for i in range(5)))
L('p', '배점: 1~4번 4.2점, 5~8번 4.4점, 9~12번 4.6점, 13~15번 4.8점, 16~17번 5.0점, 18번 5.8점(선택형 83점) / 19번 7점, 20번 10점(서답형 17점)')
for n in range(1, 19):
    s = S[n]
    L('q', f'{n}번  [정답] {ans_text(n)}  [{P[n]["pt"]}점]')
    L('k', '[풀이]')
    for x in s['sol']: L('s', x)
    L('k', '[원본 출처] ' + s['src'])
    L('k', '[원본 난도] ' + s['d0'])
    L('k', '[변형 후 난도] ' + s['d1'])
    L('k', '[변형 포인트] ' + s['var'])
    L('k', '[오답 설계 근거]')
    for c, t in s['wrong']: L('s', f'{c} {t}')
    L('k', '[원본 대비 난도 점검] ' + s['chk'] + ' → 난도 하락 없음(통과)')
L('q', f"19번  [정답] (1) ${S19['ans'][0]}$ (2) ${S19['ans'][1]}$ (3) ${S19['ans'][2]}$  [7점: 2+2+3]")
L('k', '[단계별 풀이]')
for x in S19['sol']: L('s', x)
L('k', '[단계 사이의 연결] ' + S19['link'])
L('k', '[원본 출처] ' + S19['src'])
L('k', '[원본 난도] ' + S19['d0'])
L('k', '[변형 후 난도] ' + S19['d1'])
L('k', '[변형 포인트] ' + S19['var'])
L('k', '[원본 대비 난도 점검] 원본의 차수 결정·임계점 분석을 모두 유지하고 (3)에서 경우 분류가 추가됨 → 난도 하락 없음(통과)')
L('q', "20번  [모범답안] (2) $a=-1$, $k= sqrt 2$  (3) $x=0$, 우미분계수 $-2$  [10점: 3+3+4]")
L('k', '[모범답안 및 상세 풀이]')
for x in S20['sol']: L('s', x)
L('k', '[반드시 서술해야 하는 핵심 논리]')
for x in S20['core']: L('s', '• ' + x)
L('k', '[부분점수 기준]')
for part, tot, items in S20['rubric']:
    for t, p in items: L('s', f'{part}({tot}점) {t} … {p}점')
L('s', S20['note'])
L('k', '[원본 출처] ' + S20['src'])
L('k', '[원본 난도] ' + S20['d0'])
L('k', '[변형 후 난도] ' + S20['d1'])
L('k', '[변형 포인트] ' + S20['var'])
L('k', '[원본 대비 난도 점검] 예시문항의 핵심 추론(연속 조건 → 두 극값점의 같은 함숫값)을 유지하고 h의 미분가능성 분석을 추가 → 난도 하락 없음(통과)')
L('h', '[최종 검수]')
for t in ['1. 최종 파일 HWPX: 시험지·해설지 모두 HWPX (원본 HWPX를 직접 편집)',
          '2·3·4. 글꼴(한컴바탕 9pt 등)·글자 크기·수식 기준 크기(9pt)·여백: 원본 문단/글자 모양 ID를 그대로 사용',
          '5·6. 페이지당 문항 수: 원본과 동일(1쪽 1~5번, 2쪽 6~8번, 3~7쪽 1단 1문항, 8쪽 서답형)',
          '7·8. 문항 밀도·길이: 각 문항의 조건 수를 원본 이상으로 유지',
          '9·10·14. 원본 대비 난도: 문항별 [원본 대비 난도 점검] 참조, 후반부는 Level Up·평가원 4점·예시문항 사용',
          '11·12. 출처: 1~17번·20번은 미적분1 (2).pdf, 18번은 EBS 봉투 모의고사 3회 15번, 19번은 EBS 만점 마무리 시즌2 제3회 21번',
          '13. 그림: 원본이 그래프 해석형인 8번(←57번)·17번(←65번)은 새 조건에 맞게 그래프를 새로 작도',
          '15·16. 정답 유일성: 20문항 모두 직접 풀이 + 기호 계산(sympy)으로 재검증']:
    L('s', t)

# ---- 수식 크기 측정
eqs = []
for k, t in LINES:
    eqs += [v for kk, v in segs(t) if kk == 'e']
eqs = sorted(set(eqs))
json.dump([to_latex(e) for e in eqs], open('sol_lat.json', 'w'))
subprocess.run(['node', 'measure_eqs.js', 'sol_lat.json', 'sol_meas.json'], check=True)
meas = json.load(open('sol_meas.json'))
json.dump(eqs, open('eqs.json', 'w'), ensure_ascii=False)
w = W({'eq': meas, 'boxes': {}, 'items': []})

def lab_split(t):
    m = re.match(r'^(\[[^\]]+\])(.*)$', t)
    return (m.group(1), m.group(2)) if m else ('', t)

out = []
for k, t in LINES:
    if k == 'title':
        out.append(w.para(82, w.run(w.t(' ' + t), 56)))
    elif k == 'h':
        out.append(w.para(47, w.run(w.t(t), 56)))
    elif k == 'q':
        m = re.match(r'^(\d+번)(.*)$', t)
        out.append(w.para(88, w.run(w.t(' '), 102) + w.run(w.t(m.group(1)), 99) + w.run(w.inline(m.group(2)))))
    elif k == 'k':
        a, b = lab_split(t)
        out.append(w.para(21, w.run(w.t(a), 99) + w.run(w.inline(b))))
    elif k == 's':
        out.append(w.para(51, w.run(w.inline(t))))
    elif k == 'p':
        out.append(w.para(21, w.run(w.inline(t))))

head_open, tp = tpl_paras()
p0 = re.sub(r'<hp:rect .*?</hp:rect>', '', tp[0], flags=re.S)
head = p0 + tp[15]
xml = head_open + head + ''.join(out) + '</hs:sec>'
xml = xml.replace('<hp:t> 1</hp:t></hp:run><hp:run charPrIDRef="27"><hp:t>학년 </hp:t>', '<hp:t> 2</hp:t></hp:run><hp:run charPrIDRef="27"><hp:t>학년 </hp:t>')
xml = xml.replace('공통수학1', '미적분Ⅰ').replace('선택형: 17, 단답형: 3', '선택형: 18, 서답형: 2')
xml = xml.replace('<hp:t> 문제</hp:t>', '<hp:t> 정답 및 해설</hp:t>')
xml = xml.replace('&lt;8-', '&lt;해설 ')
xml = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', xml, flags=re.S)
from lxml import etree
etree.fromstring(xml.encode())
prv = '2026학년도 2학년 미적분Ⅰ 중간고사 정답 및 해설\n' + '\n'.join(re.sub(r'\$', '', t)[:70] for k, t in LINES[:12])
pack(xml, sys.argv_out if hasattr(sys, 'argv_out') else 'out_sol.hwpx', [], prv, title='2026 2학년 미적분Ⅰ 중간고사 정답 및 해설')
print('ok', len(xml), len(eqs))
