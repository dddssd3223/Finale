# -*- coding: utf-8 -*-
"""1~5회 회차별 문항·정답·해설·채점 결과 로더"""
import os, sys, re, glob, shutil, importlib.util
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
HERE = os.path.dirname(os.path.abspath(__file__))
REP = '/home/user/Finale/output/build'
MODS = ('content3', 'sold', 'sol3', 'build3')

def load_round(n):
    d = os.path.join(SCR, f'r{n}')
    for m in MODS: sys.modules.pop(m, None)
    sys.path.insert(0, d)
    try:
        import content3, sol3
        D = sol3.D
        out = dict(c=content3, D=D, S1=sol3.S1, S2=sol3.S2)
    finally:
        sys.path.remove(d)
        for m in MODS: sys.modules.pop(m, None)
    rp = os.path.join(REP, 'report.py' if n == 1 else f'{n}회/report.py')
    t = open(rp).read()
    out['mark'] = eval(re.search(r'MARK = (\[.*?\])', t).group(1))
    out['sa'] = eval(re.search(r'SA = (\[.*?\])\n', t, re.S).group(1))
    note = re.search(r'<div class="note">\n(.*?)</div>', t, re.S).group(1)
    note = note.replace('{{', '{').replace('}}', '}').replace('\\\\', '\\')
    out['notes'] = [x.strip() for x in note.split('<br>') if x.strip()]
    # 그림: 회차 접두어로 복사
    for f in glob.glob(os.path.join(d, 'fig*.svg')):
        shutil.copy(f, os.path.join(HERE, f'r{n}_' + os.path.basename(f)))
    return out

def fixfig(s, n):
    return re.sub(r'src="(fig[^"]+\.svg)"', lambda m: f'src="r{n}_{m.group(1)}"', s)
