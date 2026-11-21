# -*- coding: utf-8 -*-
# 재활용: 6번(유력 EBS) ← 1차 부품 I4, 17번 ← 1차 부품 M55 (변형 정도가 2학기 중간 17번과 맞음; M33 합성함수형은 원본과 너무 멀어 제외)
import os as _o
def _load(f):
    ns = {}; exec(open(_o.path.join(_P, f)).read(), ns); return ns['ITEMS']
ITEMS = {6: _load('p2.py')[6], 17: _load('p5.py')[17]}
