# -*- coding: utf-8 -*-
"""회차 고정본(3회부터). 회차 폴더의 저장소 파일 + 출력 PDF + 빌드에 쓰는 저장소 밖 파일(글꼴·양식·node 모듈)의 지문을 남기고, 나중에 바뀌었는지 본다.
사용: python3 freeze.py make <회차 폴더>     # <회차>/manifest.json 쓰기
      python3 freeze.py check <회차 폴더>    # 지금 파일과 비교 (바뀐 것·없는 것 출력, 다 같으면 OK)"""
import sys, os, json, hashlib, subprocess, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
BASE = os.path.join(ROOT, 'output', 'build', '기말')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def tracked(rd):
    out = subprocess.run(['git', 'ls-files', rd], cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
    return sorted(os.path.relpath(os.path.join(ROOT, f), ROOT) for f in out if f and not f.endswith('manifest.json'))
def collect(rd):
    name = os.path.basename(os.path.abspath(rd).rstrip('/'))
    files = {f: sha(os.path.join(ROOT, f)) for f in tracked(os.path.relpath(os.path.abspath(rd), ROOT))}
    for mdir in sorted(glob.glob(os.path.join(BASE, '공동출제', '풀이', f'측정_{name}*'))):
        for f in tracked(os.path.relpath(mdir, ROOT)): files[f] = sha(os.path.join(ROOT, f))
    for p in sorted(glob.glob(os.path.join(ROOT, 'output', f'미적분1_기말고사_{name}_*.pdf'))):
        files[os.path.relpath(p, ROOT)] = sha(p)
    ext = {}
    for d in ('fonts', 'src'):
        for p in sorted(glob.glob(os.path.join(BASE, d, '*'))): ext[f'{d}/{os.path.basename(p)}'] = sha(p)
    for m in ('katex', 'playwright-core'):
        try: ext[f'node_modules/{m}'] = json.load(open(os.path.join(BASE, 'node_modules', m, 'package.json')))['version']
        except Exception: ext[f'node_modules/{m}'] = None
    return {'round': name, 'files': files, 'external': ext}
if __name__ == '__main__':
    cmd, rd = sys.argv[1], sys.argv[2]; mf = os.path.join(rd, 'manifest.json')
    if cmd == 'make':
        json.dump(collect(rd), open(mf, 'w'), ensure_ascii=False, indent=1); print(mf, len(json.load(open(mf))['files']), 'files')
    else:
        old, now = json.load(open(mf)), collect(rd); bad = 0
        for sec in ('files', 'external'):
            for k, v in old[sec].items():
                if now[sec].get(k) != v: bad += 1; print(f'{sec}: {"없음" if k not in now[sec] else "바뀜"} {k}')
            for k in now[sec].keys() - old[sec].keys(): bad += 1; print(f'{sec}: 새로 생김 {k}')
        print('OK (고정본과 같음)' if not bad else f'다른 곳 {bad}개')
