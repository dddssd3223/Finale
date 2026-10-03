# -*- coding: utf-8 -*-
"""원본 HWPX 템플릿의 section0.xml 을 직접 편집해 새 시험지를 만든다.
1) preview 단계: 문항 블록을 HTML 로 조판해 수식 크기·문항 높이를 측정 (Chromium)
2) write 단계: 측정값으로 HWPX 문단/수식/상자/그림 XML 을 생성하여 템플릿에 삽입
"""
import re, json, os, sys, shutil, zipfile, subprocess, html
from xml.sax.saxutils import escape
from lxml import etree
from eqconv import to_latex

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..')
NS = {'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph'}
COLW = 25084          # 단 너비 (HWPUNIT)
LINE = 1352           # 9pt 150% 한 줄 높이
COLH = 61800          # 단 높이 근사

# ---------------------------------------------------------------- 공통 파서
def segs(text):
    """'..$eq$..' -> [('t',str)|('e',eq)]"""
    out = []
    parts = re.split(r'\$(.+?)\$', text)
    for i, s in enumerate(parts):
        if i % 2 == 0:
            if s: out.append(('t', s))
        else:
            out.append(('e', s))
    return out

def all_eqs(items):
    eqs = []
    for it in items:
        for b in it['blocks']:
            t = b[0]
            if t in ('p', 'sub', 'lbl'): eqs += [s for k, s in segs(b[1]) if k == 'e']
            elif t == 'd': eqs.append(b[1])
            elif t in ('box', 'bogi'):
                for l in b[1]: eqs += [s for k, s in segs(l) if k == 'e']
            elif t == 'ch': eqs += [c for c in b[1] if not c.startswith('T:')]
    return eqs

# ---------------------------------------------------------------- 미리보기 HTML
FONT = os.path.join(SCR, 'fonts')
KCSS = os.path.join(SCR, 'node_modules', 'katex', 'dist', 'katex.min.css')
PCSS = f"""
@font-face{{font-family:'B';src:url('file://{FONT}/9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf')}}
@font-face{{font-family:'B';src:url('file://{FONT}/9Bty3DZF0dXLMZlywRbVRNhxy2pXV1A0.ttf');font-weight:700}}
body{{margin:0;background:#fff;font-family:'B',serif;font-size:9pt;line-height:1.5;word-break:keep-all}}
.col{{width:{COLW/100}pt;position:relative;border:1px solid #ccc;display:inline-block;vertical-align:top;margin:4pt;height:{COLH/100}pt;overflow:visible}}
.item{{position:absolute;left:0;width:100%}}
.katex{{font-size:9pt}}
.p{{text-align:justify;margin:2pt 0}}
.p .no{{font-weight:700}}
.d{{text-align:center;margin:1pt 0}}
.box{{border:.53pt solid #000;padding:2.83pt;margin:2pt 0;width:{(COLW-1300)/100}pt;box-sizing:border-box}}
.box .l{{padding-left:7pt;text-indent:-7pt;text-align:justify}}
.box .c{{text-align:center}}
.ch{{display:flex;flex-wrap:wrap;margin:2pt 0 0 11.32pt}}
.ch span.o{{width:20%;white-space:nowrap}}
.ch.g span.o{{width:33%}}
.fig{{text-align:center;margin:2pt 0}}
.sub{{padding-left:7pt;text-indent:-7pt;margin:2pt 0;text-align:justify}}
.gap{{height:{LINE/100}pt}}
"""

def h_inline(text, eqmap):
    out = ''
    for k, s in segs(text):
        if k == 't': out += html.escape(s)
        else:
            lt = '\\(\\displaystyle ' + to_latex(s) + '\\)'
            out += f'<span class="eq" data-i="{eqmap[s]}">{lt}</span>'
    return out

def h_item(label, it, eqmap):
    o = []
    first = True
    for b in it['blocks']:
        t = b[0]
        if t == 'p':
            txt = b[1].replace('{PT}', f"[{it['pt']}점]")
            pre = f'<span class="no">{label}</span> ' if first and label else ''
            o.append(f'<div class="p">{pre}{h_inline(txt, eqmap)}</div>'); first = False
        elif t == 'd':
            o.append(f'<div class="d"><span class="eq" data-i="{eqmap[b[1]]}">\\(\\displaystyle {to_latex(b[1])}\\)</span></div>')
        elif t in ('box', 'bogi'):
            inner = ''.join(f'<div class="l">{h_inline(l, eqmap)}</div>' for l in b[1])
            if t == 'bogi': inner = '<div class="c">&lt;보 기&gt;</div>' + inner
            o.append(f'<div class="box">{inner}</div>')
        elif t == 'fig':
            o.append(f'<div class="fig"><img src="{b[1]}.png" style="width:{b[2]/100}pt"></div>')
        elif t == 'ch':
            g = all(c.startswith('T:') for c in b[1])
            cs = ''
            for i, c in enumerate(b[1]):
                inner = html.escape(c[2:]) if c.startswith('T:') else f'<span class="eq" data-i="{eqmap[c]}">\\(\\displaystyle {to_latex(c)}\\)</span>'
                cs += f'<span class="o">{"①②③④⑤"[i]}&nbsp;{inner}</span>'
            o.append(f'<div class="ch{" g" if g else ""}">{cs}</div>')
        elif t == 'sub':
            o.append(f'<div class="sub">{h_inline(b[1], eqmap)}</div>')
        elif t == 'gap':
            o.append('<div class="gap"></div>' * b[1])
        elif t == 'raw':
            o.append(b[1])
    return ''.join(o)

# ---------------------------------------------------------------- 배치 계획 (원본 HWPX 의 단별 문항 배치와 동일)
from content import P, Q19, Q20, ANS

SEC2 = dict(pt=0, blocks=[])     # 서답형 머리 블록(템플릿 문단 복사)
END = dict(pt=0, blocks=[])      # 수고하셨습니다 블록(템플릿 문단 복사)
ITEMS = {f'Q{n}': P[n] for n in P}
ITEMS['Q19'] = Q19; ITEMS['Q20'] = Q20
# (항목, 원본에서의 시작 위치 HWPUNIT)
COLS = [
    [('Q1', 19922), ('Q2', 40526)],
    [('Q3', 100), ('Q4', 19000), ('Q5', 38200)],
    [('Q6', 200), ('Q7', 29958)],
    [('Q8', 200)], [('Q9', 200)], [('Q10', 200)], [('Q11', 200)], [('Q12', 200)],
    [('Q13', 200)], [('Q14', 200)], [('Q15', 200)], [('Q16', 200)], [('Q17', 200)],
    [('Q18', 200)],
    [('SEC2', 400), ('Q19', 6590)],
    [('Q20', 300), ('END', 44298)],
]

def label(key):
    if key == 'Q19': return '단답형 19.'
    if key == 'Q20': return '서술형 20.'
    if key.startswith('Q'): return key[1:] + '.'
    return ''

def build_preview():
    items = [ITEMS[k] for c in COLS for k, _ in c if k in ITEMS]
    eqs = sorted(set(all_eqs(items)))
    eqmap = {e: i for i, e in enumerate(eqs)}
    body = []
    for ci, col in enumerate(COLS):
        parts = []
        for key, top in col:
            if key in ITEMS:
                inner = h_item(label(key), ITEMS[key], eqmap)
            elif key == 'SEC2':
                inner = '<div style="height:52pt"></div>'
            else:
                inner = '<div style="height:120pt"></div>'
            parts.append(f'<div class="item" data-k="{key}" style="top:{top/100}pt">{inner}</div>')
        body.append(f'<div class="col" data-c="{ci}">{"".join(parts)}</div>')
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KCSS}">'
           f'<style>{PCSS}</style></head><body>{"".join(body)}</body></html>')
    open(os.path.join(HERE, 'preview_src.html'), 'w').write(doc)
    json.dump(eqs, open(os.path.join(HERE, 'eqs.json'), 'w'), ensure_ascii=False)

if __name__ == '__main__' and sys.argv[1:] == ['preview']:
    build_preview()

# ---------------------------------------------------------------- HWPX 작성
class W:
    def __init__(self, measure):
        self.m = measure
        self.eqs = json.load(open(os.path.join(HERE, 'eqs.json')))
        self.eqidx = {e: i for i, e in enumerate(self.eqs)}
        self.nid = 1700000000
        self.z = 2000
        self.box_i = {}

    def _id(self):
        self.nid += 1; self.z += 1
        return self.nid, self.z

    def eq_size(self, s):
        # 원본 HWPX 수식 127개로 보정: 폭 = 0.87 x KaTeX(9pt) 폭, 높이는 일반 900/1050, 분수류 1.12배
        i = self.eqidx.get(s)
        if i is None or str(i) not in self.m['eq']:
            n = len(s); return int(300 + 230 * n), 900, 86
        e = self.m['eq'][str(i)]
        kw, kh, ka = e['w'] * 100, e['h'] * 100, e['asc'] * 100   # pt -> HWPUNIT
        w = int(0.87 * kw) + 40
        if kh <= 1260:
            h = 1050 if ('^' in s or '_' in s) else 900
            bl = 88 if h == 1050 else 86
        else:
            h = int(1.12 * kh)
            bl = max(45, min(90, round(100 * ka / kh)))
        return w, h, bl

    def eq(self, s):
        w, h, bl = self.eq_size(s)
        i, z = self._id()
        return (f'<hp:equation id="{i}" zOrder="{z}" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" '
                f'dropcapstyle="None" version="Equation Version 60" baseLine="{bl}" textColor="#000000" baseUnit="900" lineMode="CHAR" font="HYhwpEQ">'
                f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
                f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
                f'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="56" right="56" top="0" bottom="0"/>'
                f'<hp:script>{escape(s)}</hp:script></hp:equation>')

    def t(self, s):
        return f'<hp:t>{escape(s)}</hp:t>' if s else ''

    def inline(self, text):
        return ''.join(self.t(v) if k == 't' else self.eq(v) for k, v in segs(text))

    @staticmethod
    def para(pp, runs, style=0, cb=False, horz=COLW):
        return (f'<hp:p id="0" paraPrIDRef="{pp}" styleIDRef="{style}" pageBreak="0" columnBreak="{1 if cb else 0}" merged="0">{runs}'
                f'<hp:linesegarray><hp:lineseg textpos="0" vertpos="0" vertsize="900" textheight="900" baseline="765" spacing="452" '
                f'horzpos="0" horzsize="{horz}" flags="393216"/></hp:linesegarray></hp:p>')

    def run(self, inner, cp=52):
        return f'<hp:run charPrIDRef="{cp}">{inner}</hp:run>'

    def rect(self, inner_paras, h, w=23800):
        i, z = self._id()
        return (f'<hp:rect id="{i}" zOrder="{z}" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" '
                f'href="" groupLevel="0" instid="{i - 1000000}" ratio="0"><hp:offset x="0" y="0"/><hp:orgSz width="{w}" height="{h}"/>'
                f'<hp:curSz width="{w}" height="{h}"/><hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="{w//2}" centerY="{h//2}" rotateimage="1"/>'
                f'<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
                f'<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
                f'<hp:lineShape color="#000000" width="53" style="SOLID" endCap="FLAT" headStyle="NORMAL" tailStyle="NORMAL" headfill="1" tailfill="1" '
                f'headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" outlineStyle="NORMAL" alpha="0"/>'
                f'<hc:fillBrush><hc:winBrush faceColor="#FFFFFF" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
                f'<hp:shadow type="NONE" color="#B2B2B2" offsetX="0" offsetY="0" alpha="178"/>'
                f'<hp:drawText lastWidth="{w}" name="" editable="0"><hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" '
                f'linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">{inner_paras}</hp:subList>'
                f'<hp:textMargin left="283" right="283" top="283" bottom="283"/></hp:drawText>'
                f'<hc:pt0 x="0" y="0"/><hc:pt1 x="{w}" y="0"/><hc:pt2 x="{w}" y="{h}"/><hc:pt3 x="0" y="{h}"/>'
                f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
                f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
                f'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/>'
                f'<hp:shapeComment>사각형입니다.</hp:shapeComment></hp:rect>')

    def pic(self, binid, pxw, pxh, w):
        h = int(w * pxh / pxw)
        ow, oh = pxw * 75, pxh * 75
        i, z = self._id()
        sx, sy = w / ow, h / oh
        return (f'<hp:pic id="{i}" zOrder="{z}" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" '
                f'href="" groupLevel="0" instid="{i - 1000000}" reverse="0"><hp:offset x="0" y="0"/><hp:orgSz width="{ow}" height="{oh}"/>'
                f'<hp:curSz width="{w}" height="{h}"/><hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="{w//2}" centerY="{h//2}" rotateimage="1"/>'
                f'<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="{sx:.6f}" e2="0" e3="0" e4="0" e5="{sy:.6f}" e6="0"/>'
                f'<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
                f'<hc:img binaryItemIDRef="{binid}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>'
                f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{ow}" y="0"/><hc:pt2 x="{ow}" y="{oh}"/><hc:pt3 x="0" y="{oh}"/></hp:imgRect>'
                f'<hp:imgClip left="0" right="{ow}" top="0" bottom="{oh}"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
                f'<hp:imgDim dimwidth="{ow}" dimheight="{oh}"/><hp:effects/>'
                f'<hp:sz width="{w}" widthRelTo="ABSOLUTE" height="{h}" heightRelTo="ABSOLUTE" protect="0"/>'
                f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" '
                f'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/>'
                f'<hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')

    CIRC_IMG = ['image2', 'image3', 'image4', 'image5', 'image6']

    def circ(self, k):
        i, z = self._id()
        return (f'<hp:pic id="{i}" zOrder="{z}" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" '
                f'href="" groupLevel="0" instid="{i - 1000000}" reverse="0"><hp:offset x="0" y="0"/><hp:orgSz width="23580" height="23580"/>'
                f'<hp:curSz width="845" height="845"/><hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="423" centerY="423" rotateimage="1"/>'
                f'<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="0.035878" e2="0" e3="0" e4="0" e5="0.035878" e6="0"/>'
                f'<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
                f'<hc:img binaryItemIDRef="{self.CIRC_IMG[k]}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>'
                f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="23580" y="0"/><hc:pt2 x="23580" y="23580"/><hc:pt3 x="0" y="23580"/></hp:imgRect>'
                f'<hp:imgClip left="0" right="17640" top="0" bottom="17640"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
                f'<hp:imgDim dimwidth="17640" dimheight="17640"/><hp:effects/>'
                f'<hp:sz width="846" widthRelTo="ABSOLUTE" height="846" heightRelTo="ABSOLUTE" protect="0"/>'
                f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" '
                f'vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="0" right="0" top="0" bottom="0"/>'
                f'<hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')

    def item_width(self, c):
        if c.startswith('T:'):
            return 846 + 300 + int(len(c[2:]) * 820)
        return 846 + 300 + self.eq_size(c)[0]

    def choices(self, chs):
        grid = all(c.startswith('T:') for c in chs)
        rows = [chs[:3], chs[3:]] if grid else [chs]
        slot = (COLW - 1132) // (3 if grid else 5)
        out = []
        k = 0
        for row in rows:
            inner = ''
            for j, c in enumerate(row):
                inner += self.circ(k) + '<hp:t><hp:nbSpace/></hp:t>'
                inner += self.t(c[2:]) if c.startswith('T:') else self.eq(c)
                if j < len(row) - 1:
                    n = max(2, round((slot - self.item_width(c)) / 300))
                    inner += self.t(' ' * n)
                k += 1
            out.append(self.para(41, self.run(inner, 53), style=33, horz=COLW - 1132))
        return ''.join(out)

    def box(self, key, lines, bogi=False):
        idx = self.box_i.get(key, 0); self.box_i[key] = idx + 1
        hpt = self.m['boxes'][key][idx]
        h = int(hpt * 100 * 1.12) + 500
        ps = ''
        if bogi:
            ps += self.para(92, self.run(self.t('<보 기>'), 55), horz=23234)
        for l in lines:
            ps += self.para(81, self.run(self.inline(l), 55), style=39, horz=23234)
        return self.para(74, self.run(self.rect(ps, h)), style=36)

    def item(self, key, it, cb):
        out = []
        first = True
        for b in it['blocks']:
            t = b[0]
            brk = cb and not out
            if t == 'p':
                txt = b[1].replace('{PT}', f"[{it['pt']}점]")
                if first and key in ('Q19', 'Q20'):
                    lab = '단답형 19. ' if key == 'Q19' else '서술형 20. '
                    runs = self.run(self.t(' '), 102) + self.run(self.t(lab), 99) + self.run(self.inline(txt))
                    out.append(self.para(88, runs, cb=brk))
                elif first:
                    out.append(self.para(107, self.run(self.inline(txt)), style=36, cb=brk))
                else:
                    out.append(self.para(73, self.run(self.inline(txt)), style=36, cb=brk))
                first = False
            elif t == 'd':
                out.append(self.para(92, self.run(self.eq(b[1])), cb=brk))
            elif t == 'box':
                out.append(self.box(key, b[1]))
            elif t == 'bogi':
                out.append(self.box(key, b[1], bogi=True))
            elif t == 'ch':
                out.append(self.choices(b[1]))
            elif t == 'fig':
                binid, (pw, ph) = FIGS[b[1]]
                out.append(self.para(92, self.run(self.pic(binid, pw, ph, b[2])), cb=brk))
            elif t == 'sub':
                out.append(self.para(51, self.run(self.inline(b[1])), cb=brk))
            elif t == 'gap':
                out.extend(self.para(51, self.run('')) for _ in range(b[1]))
        return ''.join(out)

    def blank(self, n):
        return ''.join(self.para(41, self.run('', 53), style=33) for _ in range(max(0, n)))

FIGS = {}

def _nested_paras(body):
    # body 안의 중첩 문단(상자·머리말 등 subList 내부) 개수
    xml = ''.join(body)
    return len(re.findall(r'<hp:subList.*?</hp:subList>', xml, flags=re.S)) and sum(
        sl.count('<hp:p ') for sl in re.findall(r'<hp:subList.*?</hp:subList>', xml, flags=re.S))

def tpl_paras():
    s = open(os.path.join(HERE, 'clean_section.xml'), encoding='utf8').read()
    root = etree.fromstring(s.encode())
    ps = root.findall('hp:p', NS)
    ser = lambda p: re.sub(r' xmlns:\w+="[^"]+"', '', etree.tostring(p, encoding='unicode'))
    head_open = s[:s.index('<hp:p ')]
    return head_open, [ser(p) for p in ps]

def set_cb(px):
    return px.replace('columnBreak="0"', 'columnBreak="1"', 1)

def write_exam(out_name, fill=None, starts=None):
    m = json.load(open(os.path.join(HERE, 'measure.json')))
    w = W(m)
    head_open, tp = tpl_paras()
    pos = {(it['c'], it['k']): (it['top'] * 100, (it['top'] + it['h']) * 100) for it in m['items']}
    body = []
    # 1쪽 머리 부분(준수사항·선택형 안내·머리말/꼬리말) 그대로 사용
    head = ''.join(tp[0:16])
    head = head.replace('&lt;선택형 문제 – 82점&gt;', '&lt;선택형 문제 – 83점&gt;').replace('선택형 문제(1~17)번', '선택형 문제(1~18)번')
    body.append(head)
    for ci, col in enumerate(COLS):
        prev_end = None
        for j, (key, top) in enumerate(col):
            cb = (j == 0 and ci > 0)
            if prev_end is not None:
                gap = top - prev_end
                n = fill.get((ci, j), int(gap // LINE) - 2) if fill is not None else int(gap // LINE) - 2
                if fill is not None: fill[(ci, j)] = n
                body.append(w.blank(n))
            mark = 880000 + ci * 10 + j
            if key == 'SEC2':
                blk = [set_cb(tp[480]) if cb else tp[480]] + tp[481:485]
                blk = ''.join(blk)
                blk = blk.replace('&lt;단답형 문제 – 18점&gt;', '&lt;서답형 문제 – 17점&gt;')
                blk = blk.replace('단답형 문제(단답형 1번~단답형 3번)는 반드시', '서답형 문제(단답형 19번, 서술형 20번)는 반드시')
                blk = blk.replace('서답형 답안지의 해당란에 정답만 작성', '서답형 답안지의 해당란에 답을 작성')
                body.append(re.sub(r'<hp:p id="\d+"', f'<hp:p id="{mark}"', blk, count=1))
            elif key == 'END':
                blk = ''.join(tp[567:573])
                blk = blk.replace('선택형 17문제 = 82점', '선택형 18문제 = 83점').replace('서답형  3문제 = 18점', '서답형  2문제 = 17점')
                body.append(re.sub(r'<hp:p id="\d+"', f'<hp:p id="{mark}"', blk, count=1))
            else:
                body.append(re.sub(r'<hp:p id="\d+"', f'<hp:p id="{mark}"', w.item(key, ITEMS[key], cb), count=1))
            prev_end = pos[(ci, key)][1]
    xml = head_open + ''.join(body) + '</hs:sec>'
    # 머리말(제목) 수정
    xml = xml.replace('<hp:t> 1</hp:t></hp:run><hp:run charPrIDRef="27"><hp:t>학년 </hp:t>', '<hp:t> 2</hp:t></hp:run><hp:run charPrIDRef="27"><hp:t>학년 </hp:t>')
    xml = xml.replace('공통수학1', '미적분Ⅰ').replace('선택형: 17, 단답형: 3', '선택형: 18, 서답형: 2')
    # 남은 미주(zb) 표시 제거
    xml = re.sub(r'<hp:t>zb</hp:t><hp:ctrl><hp:endNote .*?</hp:endNote></hp:ctrl>', '', xml, flags=re.S)
    # 편집된 문단의 레이아웃 캐시 제거 → 한글이 열 때 다시 조판
    xml = re.sub(r'<hp:linesegarray>.*?</hp:linesegarray>', '', xml, flags=re.S)
    etree.fromstring(xml.encode())  # well-formed 검사
    return xml

def pack(section_xml, out_path, figs, prv_text, prv_png=None, title=None):
    src = os.path.join(HERE, 't')
    tmp = os.path.join(HERE, 'pkg')
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(src, tmp)
    open(os.path.join(tmp, 'Contents', 'section0.xml'), 'w', encoding='utf8').write(section_xml)
    hpf_p = os.path.join(tmp, 'Contents', 'content.hpf')
    hpf = open(hpf_p, encoding='utf8').read()
    # 새 그림 추가
    for binid, fn in figs:
        shutil.copy(os.path.join(HERE, fn), os.path.join(tmp, 'BinData', binid + '.png'))
        hpf = hpf.replace('<opf:item id="section0"', f'<opf:item id="{binid}" href="BinData/{binid}.png" media-type="image/png" isEmbeded="1"/><opf:item id="section0"')
    # 참조되지 않는 그림 제거(원본 문항 그림)
    refs = set(re.findall(r'binaryItemIDRef="(\w+)"', section_xml))
    for x in ['header.xml', 'masterpage0.xml']:
        refs |= set(re.findall(r'binaryItemIDRef="(\w+)"', open(os.path.join(tmp, 'Contents', x), encoding='utf8').read()))
    for m_ in re.finditer(r'<opf:item id="(image\d+)" href="([^"]+)"[^>]*/>', hpf):
        if m_.group(1) not in refs:
            os.remove(os.path.join(tmp, m_.group(2)))
            hpf = hpf.replace(m_.group(0), '')
    if title:
        hpf = re.sub(r'<opf:title>.*?</opf:title>', f'<opf:title>{escape(title)}</opf:title>', hpf)
    open(hpf_p, 'w', encoding='utf8').write(hpf)
    st = os.path.join(tmp, 'settings.xml')
    s = open(st, encoding='utf8').read()
    s = re.sub(r'paraIDRef="\d+" pos="\d+"', 'paraIDRef="0" pos="0"', s)
    open(st, 'w', encoding='utf8').write(s)
    open(os.path.join(tmp, 'Preview', 'PrvText.txt'), 'w', encoding='utf8').write(prv_text)
    if prv_png: shutil.copy(prv_png, os.path.join(tmp, 'Preview', 'PrvImage.png'))
    if os.path.exists(out_path): os.remove(out_path)
    with zipfile.ZipFile(out_path, 'w') as z:
        z.write(os.path.join(tmp, 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
        for root_, _, files in os.walk(tmp):
            for f in sorted(files):
                full = os.path.join(root_, f); rel = os.path.relpath(full, tmp)
                if rel == 'mimetype': continue
                z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)

def figs_info():
    from PIL import Image
    out = {}
    for name, binid in [('fig8', 'image21'), ('fig17', 'image22')]:
        im = Image.open(os.path.join(HERE, name + '.png'))
        out[name] = (binid, im.size)
    return out

if __name__ == '__main__' and sys.argv[1:2] == ['exam']:
    FIGS.update(figs_info())
    xml = write_exam('exam')
    prv = '2026학년도 2학년 미적분Ⅰ 중간고사 문제\n' + '\n'.join(
        f"{n}. " + re.sub(r'\$|\{PT\}', '', ITEMS[f'Q{n}']['blocks'][0][1])[:60] for n in range(1, 21))
    pack(xml, sys.argv[2], [('image21', 'fig8.png'), ('image22', 'fig17.png')], prv, title='2026 2학년 미적분Ⅰ 중간고사')
    print('written', sys.argv[2], len(xml))
