# -*- coding: utf-8 -*-
"""이미지 없는 문자(LMS) 한 통: python3 send_text.py <본문.txt> [--subject 제목] [--dry]
키·번호는 send_solapi.py와 같은 환경 변수 SOLAPI_*. 본문은 2,000바이트(EUC-KR) 이하."""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import send_solapi as S

ap = argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--subject', default='모의고사'); ap.add_argument('--dry', action='store_true')
a = ap.parse_args()
t = open(a.file, encoding='utf-8').read().strip()
n = S.nbytes(t); print(f'본문 {n}바이트')
if n > 2000: raise SystemExit('2,000바이트를 넘어요.')
if a.dry: print('dry run: 발송하지 않음'); raise SystemExit
msg = {'to': os.environ['SOLAPI_TO'].replace('-', ''), 'from': os.environ['SOLAPI_FROM'].replace('-', ''), 'text': t, 'subject': a.subject}
r = S.call('/messages/v4/send', {'message': msg})
print(f'발송: {r.get("statusCode")} {r.get("statusMessage")}')
