# -*- coding: utf-8 -*-
# 1회 선택본: 17·18 후보 경쟁(Claude·Codex 각 1). 원본은 ../후보/에 두고, 독립 검토자가 고른 것만 가져온다(근거: ../review/).
import runpy as _rp
_D = '/home/user/Finale/output/build/기말/1회/'
def _g(f, k='ITEMS'):
    return _rp.run_path(_D + f)[k]
ITEMS = {
    17: _g('후보/p17.py')[17],    # review/claude17.json 통과 (codex17 미통과: 미분 없이 풀림, 원문 원리 줄 통)
    18: _g('후보/p18.py')[18],    # review/claude18.json 통과 (codex18 미통과: 원문 설정 줄 통, d_step 0.60)
}
SITEMS = {}
