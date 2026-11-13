# -*- coding: utf-8 -*-
"""새 회차 폴더 만들기: python3 new_round.py r10 [기존회차폴더]
engine/의 빌드 스크립트를 복사하고, 기존 회차(기본 rounds/example_r8)의 문항 파일을 출발점으로 복사한다."""
import os, sys, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1]
base = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'rounds', 'example_r8')
dst = os.path.join(ROOT, 'rounds', name)
os.makedirs(dst, exist_ok=False)
for f in ['build3.py', 'render3.js', 'eqfont.js', 'ans3.py', 'report.py', 'mark.py', 'photocopy.py', 'figs_head.py']:
    shutil.copy(os.path.join(ROOT, 'engine', f), dst)
for f in ['content3.py', 'sold.py', 'sol3.py']:
    shutil.copy(os.path.join(base, f), dst)
print('만들었습니다:', dst)
print('다음: content3.py(문항) · sold.py(해설) · sol3.py(서답형 채점기준) 수정 후')
print('  cd', dst, '&& python3 build3.py exam.pdf && python3 sol3.py sol.pdf && python3 ans3.py ans.pdf')
