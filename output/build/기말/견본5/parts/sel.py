# -*- coding: utf-8 -*-
# 견본5 선택본: 같은 번호를 두 출제자(Claude B팀·Codex)가 냈거나 17·18·서답형2 후보 경쟁을 한 문항.
# 원본은 ../대안/, ../후보/에 그대로 두고, 독립 검토자가 고른 것만 여기서 가져온다(근거: ../review/).
import runpy as _rp
_D = '/home/user/Finale/output/build/기말/견본5/'
def _g(f, k='ITEMS'):
    return _rp.run_path(_D + f)[k]
_B1, _B2 = _g('대안/p5.py'), _g('대안/p6.py')     # Claude B팀 (1·3·5·7 / 9·11·13·15)
_C1, _C2 = _g('대안/c1.py'), _g('대안/c2.py')     # Codex (1·3·5·7 / 9·11·13·15)
ITEMS = {
    1: _B1[1], 3: _B1[3], 5: _C1[5], 7: _B1[7],          # review/compare1_7.json
    9: _C2[9], 11: _C2[11], 13: _B2[13], 15: _C2[15],    # review/compare9_15.json
    18: _g('후보/p18.py')[18],                            # review/claude18.json (관문 3 통과)
}
SITEMS = {'S2': _g('대안/c5.py', 'SITEMS')['S2']}       # review/codexS2.json (관문 3 통과, 검토 수정 반영)
