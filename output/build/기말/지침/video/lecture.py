# 해설 영상(손필기 판서 + 목소리): python3 lecture.py <회차 폴더> <출력.mp4> <script_*.json …>
# 대본 형식: <회차>/video/TASK.md. 판서 줄이 왼쪽부터 써지는 동안 그 줄의 나레이션이 나온다.
import sys, os, json, re, subprocess, concurrent.futures as cf
B = '/home/user/Finale/output/build/기말'
sys.path.insert(0, B + '/지침'); import haeseol2 as H
RD = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); SCRIPTS = sys.argv[3:]
sys.path.insert(0, RD); import content3 as c
RN = os.path.basename(RD)
W = os.path.join(os.path.dirname(OUT), '_lec_' + os.path.splitext(os.path.basename(OUT))[0]); os.makedirs(W, exist_ok=True)
F = H.FONTS; NAN = '/usr/share/fonts/truetype/nanum/'
VOICE = os.environ.get('LEC_VOICE', 'ko-KR-InJoonNeural')
CS = '①②③④⑤'

def figs_of(n):
    it = c.SITEMS[n] if not str(n).isdigit() else c.ITEMS[int(n)]
    return re.findall(r'src="(fig_[^"]+)"', it['body'] + str(it.get('after') or ''))

def problem_html(n):
    if n == 'S2' or n == 'S1':
        it = c.SITEMS[n]
        subs = ''.join(f'<div class="sub"><b>({i+1})</b> {t} <span class="pt">[{p.split(",")[0]}]</span></div>' for i, (t, p) in enumerate(it['subs']))
        return f'<div class="pb"><div class="qn">서답형 {n[1]}</div><div class="qt">{it["body"]}{subs}</div></div>'
    it = c.ITEMS[int(n)]
    cond = ''
    if it.get('cond'):
        cond = '<div class="cond">' + ''.join(f'<div class="cr"><span class="cl">{"㈎㈏㈐㈑"["가나다라".index(a)]}</span><span>{t}</span></div>' for a, t in it['cond']) + '</div>'
    after = it.get('after') or ''
    bogi = ''
    if it.get('bogi'):
        bogi = '<div class="cond"><div class="bh">&lt;보 기&gt;</div>' + ''.join(f'<div class="cr"><span class="cl">{k}.</span><span>{t}</span></div>' for k, t in it['bogi']) + '</div>'
    ch = it.get('choices') or []
    chs = '<div class="chs">' + ''.join(f'<span>{CS[i]} {x[2:] if str(x).startswith("T:") else chr(92)+"("+str(x)+chr(92)+")"}</span>' for i, x in enumerate(ch)) + '</div>'
    body = re.sub(r'<(?:div|span)[^>]*>\s*<img[^>]*>\s*</(?:div|span)>|<img[^>]*>', '', it['body'])
    return f'<div class="pb"><div class="qn">{n}.</div><div class="qt">{body}{cond}{after}{bogi}{chs}</div></div>'

CSS = f"""
@font-face{{font-family:'PEN';src:url('file://{NAN}NanumPen.ttf')}}
@font-face{{font-family:'BPEN';src:url('file://{NAN}NanumBarunpenB.ttf')}}
@font-face{{font-family:'SJ';src:url('file://{F}/shinjung.ttf')}}
@font-face{{font-family:'BD';src:url('file://{F}/busan_M.ttf')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1920px;height:1080px;overflow:hidden;background:#fbfaf4}}
.pg{{position:absolute;inset:0;display:none;background:#fbfaf4;
  background-image:linear-gradient(#e6ecf3 1px,transparent 1px);background-size:100% 54px;background-position:0 150px}}
.pg.on{{display:block}}
.pg:before{{content:'';position:absolute;left:150px;top:0;bottom:0;border-left:3px solid #f1b8b8}}
.hd{{position:absolute;left:190px;top:34px;right:80px;display:flex;align-items:baseline;gap:26px;font-family:'BPEN';color:#20304f}}
.hd .no{{font-size:54px}} .hd .tt{{font-size:40px;color:#3b5a8c}}
.bd{{position:absolute;left:800px;right:70px;top:150px;bottom:40px;font-family:'PEN';font-size:58px;line-height:1.5;color:#1d2a46}}
.ln{{opacity:0;margin:4px 0}} .ln.v{{opacity:1}}
.ln .katex{{font-size:.72em;color:#1d2a46}} .ln .katex-display{{margin:.15em 0 .15em 40px;text-align:left}} .ln .katex-display>.katex{{text-align:left}}
.ln.key{{color:#c0392b}} .ln.key .katex{{color:#c0392b}} span.u{{display:inline-block;max-width:100%}} .ln.key>span.u{{border-bottom:4px solid #e57373;padding-bottom:2px}}
.ln.trap{{color:#d9822b}} .ln.trap .katex{{color:#d9822b}}
.ln.answer{{color:#1f7a3f}} .ln.answer .katex{{color:#1f7a3f}} .ln.answer>span.u{{border:4px solid #4caf73;border-radius:40px;padding:0 26px}}
.fig{{position:absolute;right:110px;top:190px;width:640px;background:#fff;border:2px solid #d8dee8;border-radius:12px;padding:10px}}
.fig img{{width:100%}}
.side{{position:absolute;left:30px;top:24px;width:730px;bottom:24px;display:flex;flex-direction:column;gap:14px}}
.side .pb{{position:static;font-size:21px;line-height:1.75;padding:18px 22px;border-radius:12px;gap:10px}}
.side .fig{{position:static;width:100%;max-height:430px;display:flex;justify-content:center}} .side .fig img{{height:380px;width:auto;max-width:100%}} .side .chs{{gap:22px;flex-wrap:wrap}} .chs span{{white-space:nowrap}}
.pg.board:before{{left:780px}} .pg.board .hd{{left:800px}}
.pfig{{position:absolute;right:70px;top:170px;width:560px;background:#fff;border:2px solid #d8dee8;border-radius:12px;padding:10px}} .pfig img{{width:100%}}
.pg.wpf .pb{{right:660px}}
.pb{{position:absolute;left:190px;right:110px;top:160px;display:flex;gap:22px;font-family:'SJ';font-size:40px;line-height:1.9;color:#111;background:#fff;border:2px solid #d8dee8;border-radius:16px;padding:40px 48px}}
.pb .qn{{font-family:'BD';color:#1f3c74}} .pb .katex{{font-size:1.02em}}
.cond{{border:2px solid #333;padding:12px 24px;margin:12px 0}} .cr{{display:flex;gap:16px}} .cl{{font-family:'BD'}} .bh{{text-align:center;font-family:'BD'}}
.chs{{display:flex;gap:60px;margin-top:10px}} .sub{{margin-top:10px}} .pt{{color:#777;font-size:.8em}}
.pb img{{max-height:330px;display:block;margin:8px 0}}
.title{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;font-family:'BPEN';color:#20304f}}
.title .a{{font-size:44px;color:#6b7a94}} .title .b{{font-size:120px}} .title .c{{font-size:52px;color:#3b5a8c}}
"""

def esc_say(s): return s

states = []   # (page_id, upto, say|None, kind)
pages_html = []
items = []
for sp in SCRIPTS:
    d = json.load(open(sp)); items.append(d)
for d in items:
    n = str(d['n']); lab = f'{n}번' if n.isdigit() else ('서답형 ' + n[1])
    pid = f'p{len(pages_html)}'
    pages_html.append(f'<section class="pg" id="{pid}"><div class="title"><div class="a">미적분Ⅰ 기말 모의고사 {RN}</div><div class="b">{lab}</div><div class="c">{d.get("title","")}</div></div></section>')
    states.append((pid, -1, None, 'title'))
    for pg in d['pages']:
        pid = f'p{len(pages_html)}'
        if pg.get('kind') == 'problem':
            fg = figs_of(n); pf = ''.join(f'<div class="pfig"><img src="file://{RD}/{f}"></div>' for f in fg[:1])
            pages_html.append(f'<section class="pg{" wpf" if fg else ""}" id="{pid}"><div class="hd"><span class="no">{lab}</span><span class="tt">문제 읽기</span></div>{problem_html(n)}{pf}</section>')
            for st in pg['steps']: states.append((pid, -1, st['say'], 'problem'))
            continue
        fg = figs_of(n) or ([pg['figure']] if pg.get('figure') else [])
        figh = f'<div class="side">{problem_html(n)}' + ''.join(f'<div class="fig"><img src="file://{RD}/{f}"></div>' for f in fg[:1]) + '</div>'
        lines = ''.join(f'<div class="ln {st.get("mark","")}" data-i="{i}"><span class="u">{H.DFR(st["board"])}</span></div>' for i, st in enumerate(pg['steps']))
        pages_html.append(f'<section class="pg board" id="{pid}"><div class="hd"><span class="no">{lab}</span><span class="tt">{pg.get("heading","")}</span></div>{figh}<div class="bd">{lines}</div></section>')
        states.append((pid, -1, None, 'blank'))
        for i, st in enumerate(pg['steps']): states.append((pid, i, st['say'], 'line'))

html = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{H.KATEX_CSS}"><style>{CSS}</style></head><body>{"".join(pages_html)}</body></html>'
open(os.path.join(W, 'page_src.html'), 'w').write(H.fx(html))
json.dump([[a, b] for a, b, _, _ in states], open(os.path.join(W, 'states.json'), 'w'))
subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lecture_shoot.js'), W], check=True)

# 음성
def tts(i_say):
    i, say = i_say
    mp = os.path.join(W, f'a{i:04d}.mp3')
    if os.path.exists(mp) and os.path.getsize(mp) > 0: return
    env = dict(os.environ, SSL_CERT_FILE='/root/.ccr/ca-bundle.crt')
    for _ in range(4):
        r = subprocess.run(['edge-tts', '--proxy', os.environ.get('HTTPS_PROXY', ''), '--voice', VOICE, '--rate', '+4%', '--text', say, '--write-media', mp], env=env, capture_output=True)
        if r.returncode == 0 and os.path.getsize(mp) > 0: return
    raise RuntimeError(f'tts 실패 {i}: {r.stderr[-300:]}')
with cf.ThreadPoolExecutor(6) as ex: list(ex.map(tts, [(i, s[2]) for i, s in enumerate(states) if s[2]]))
dur = lambda f: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())

# 조각: 앞 화면 → 이번 화면을 왼쪽부터 닦아 내며(쓰는 느낌) 나레이션
segs = []
def seg(i, prev, cur, a, kind):
    out = os.path.join(W, f's{i:04d}.mp4')
    if kind in ('title', 'blank'):
        T = 2.2 if kind == 'title' else 0.6
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', str(T), '-i', cur, '-f', 'lavfi', '-t', str(T), '-i', 'anullsrc=r=24000:cl=mono',
               '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-shortest', out]
    else:
        D = dur(a) + 0.45
        wipe = 0.25 if kind == 'problem' else min(2.6, max(0.8, 0.5 * D))
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', str(D), '-i', prev, '-loop', '1', '-t', str(D), '-i', cur, '-i', a,
               '-filter_complex', f'[0:v]fps=30,format=yuv420p[a];[1:v]fps=30,format=yuv420p[b];[a][b]xfade=transition=wiperight:duration={wipe:.2f}:offset=0.05,trim=duration={D:.2f}[v];[2:a]apad,atrim=duration={D:.2f}[au]',
               '-map', '[v]', '-map', '[au]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-ar', '24000', '-ac', '1', out]
    subprocess.run(cmd, check=True); return out
jobs = []
for i, (pid, upto, say, kind) in enumerate(states):
    cur = os.path.join(W, f'f{i:04d}.png'); prev = os.path.join(W, f'f{max(i-1,0):04d}.png')
    jobs.append((i, prev, cur, os.path.join(W, f'a{i:04d}.mp3') if say else None, kind))
with cf.ThreadPoolExecutor(4) as ex: segs = list(ex.map(lambda j: seg(*j), jobs))
lst = os.path.join(W, 'list.txt'); open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', OUT], check=True)
print(OUT, round(dur(OUT) / 60, 1), '분', len(states), '장면')
