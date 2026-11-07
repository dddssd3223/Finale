# -*- coding: utf-8 -*-
# 2회 선택본: 17·18 후보 경쟁(Claude·Codex 각 1). 원본은 ../후보/에 두고, 독립 검토로 고른 것만 가져온다(근거: ../review/).
import runpy as _rp
_D = '/home/user/Finale/output/build/기말/2회/'
def _g(f, k='ITEMS'):
    return _rp.run_path(_D + f)[k]
ITEMS = {
    17: _g('후보/c17.py')[17],    # review/codex17.json 통과(검토 반영: f=4x³−12x+2) · claude17 미통과(원문 설정·풀이 전반 재사용, d_step 0.55)
    18: _g('후보/p18.py')[18],    # review/claude18_v*.json (두 후보 모두 1차 미통과 → 더 나은 claude18을 검토 지적대로 수정) · codex18 미통과(설정 줄 변형 통)
}
SITEMS = {}
