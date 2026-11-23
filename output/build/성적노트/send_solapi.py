# -*- coding: utf-8 -*-
"""회차 성적표 이미지를 솔라피(SOLAPI) MMS로 보냄.

사용:  python3 send_solapi.py <성적표.png> "<문자 본문>" [--text2 "<둘째 문자>"] [--single] [--to 01012345678] [--from 01012345678] [--dry]
- API 키: 환경 변수 SOLAPI_API_KEY, SOLAPI_API_SECRET (환경 설정의 Network secrets/환경 변수)
- 번호: --to/--from 또는 환경 변수 SOLAPI_TO, SOLAPI_FROM (발신번호는 솔라피 콘솔에 사전 등록 필수)
- 이미지: MMS 제한(JPG 200KB 이하)에 맞춰 폭 640px로 줄이고, 세로로 길면 여러 장으로 나눠 각각 MMS로 보냄
- --single: 나누지 않고 한 장으로 보냄(두 단으로 나란히 붙여 1500x1440px·200KB 안에 맞춤)
- --text2: 첫 MMS 뒤에 이미지 없는 LMS를 하나 더 보냄(개인 코멘트용)
- 본문은 LMS·MMS 한도 2,000바이트(EUC-KR 기준) 안이어야 함
- --dry: 이미지 변환·서명만 하고 실제 발송은 하지 않음
"""
import os, sys, io, json, hmac, hashlib, base64, uuid, datetime, argparse, urllib.request
from PIL import Image

API = 'https://api.solapi.com'
MAX_BYTES = 200 * 1024
WIDTH, MAX_H = 640, 1300

def auth_header():
    key, secret = os.environ['SOLAPI_API_KEY'], os.environ['SOLAPI_API_SECRET']
    date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    salt = uuid.uuid4().hex
    sig = hmac.new(secret.encode(), (date + salt).encode(), hashlib.sha256).hexdigest()
    return f'HMAC-SHA256 apiKey={key}, date={date}, salt={salt}, signature={sig}'

def call(path, body):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method='POST',
                                 headers={'Authorization': auth_header(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f'솔라피 오류 {e.code}: {e.read().decode(errors="replace")}')

def to_jpgs(png):
    im = Image.open(png).convert('RGB')
    im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
    n = -(-im.height // MAX_H)
    # 카드 사이 빈 줄(배경색만 있는 가로줄)에서 자름: 나눌 지점 근처에서 가장 가까운 빈 줄
    g = im.convert('L'); px = g.load(); bg = px[2, 2]
    blank = [all(abs(px[x, y] - bg) < 6 for x in range(0, WIDTH, 4)) for y in range(im.height)]
    cuts, start = [0], 0
    for i in range(1, n):
        ideal = round(im.height * i / n)
        cand = [y for y in range(max(start + 200, ideal - 250), min(im.height - 1, start + MAX_H)) if blank[y]]
        y = min(cand, key=lambda y: abs(y - ideal)) if cand else min(start + MAX_H, ideal)
        cuts.append(y); start = y
    cuts.append(im.height)
    parts = []
    for i in range(len(cuts) - 1):
        piece = im.crop((0, cuts[i], WIDTH, cuts[i + 1]))
        for q in range(88, 40, -6):
            buf = io.BytesIO(); piece.save(buf, 'JPEG', quality=q, optimize=True, progressive=False)
            if buf.tell() <= MAX_BYTES: break
        parts.append(buf.getvalue())
    return parts

MAX_W, MAX_HH = 1500, 1440  # 솔라피 MMS 해상도 한도

def to_one_jpg(png):
    """나누지 않은 한 장. 세로가 1440px을 넘으면 카드 사이 빈 줄에서 반으로 잘라 두 단으로 나란히 붙임."""
    im0 = Image.open(png).convert('RGB')
    g = im0.convert('L'); px = g.load(); bg = px[2, 2]
    W0, H0 = im0.size
    blank = [all(abs(px[x, y] - bg) < 6 for x in range(0, W0, 8)) for y in range(H0)]
    cand = [y for y in range(H0 // 2 - H0 // 6, H0 // 2 + H0 // 6) if blank[y]]
    cut = min(cand, key=lambda y: abs(y - H0 // 2)) if cand else H0 // 2
    cols = [im0.crop((0, 0, W0, cut)), im0.crop((0, cut, W0, H0))]
    gap = W0 // 30
    sheet = Image.new('RGB', (2 * W0 + gap, max(cut, H0 - cut)), im0.getpixel((2, 2)))
    sheet.paste(cols[0], (0, 0)); sheet.paste(cols[1], (W0 + gap, 0))
    k = min(MAX_W / sheet.width, MAX_HH / sheet.height, 1)
    for f in (1, 0.92, 0.85, 0.78):
        w, h = round(sheet.width * k * f), round(sheet.height * k * f)
        im = sheet.resize((w, h), Image.LANCZOS)
        for q in range(88, 50, -4):
            buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True, progressive=False)
            if buf.tell() <= MAX_BYTES:
                print(f'한 장(두 단): {w}x{h}px, 화질 {q}')
                return [buf.getvalue()]
    raise SystemExit('한 장으로 200KB 안에 맞출 수 없어요. --single 없이 나눠 보내세요.')

def nbytes(t):
    return len(t.encode('cp949', errors='replace'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('png'); ap.add_argument('text')
    ap.add_argument('--to', default=os.environ.get('SOLAPI_TO'))
    ap.add_argument('--from', dest='frm', default=os.environ.get('SOLAPI_FROM'))
    ap.add_argument('--subject', default='성적표')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--single', action='store_true')
    ap.add_argument('--text2')
    ap.add_argument('--subject2', default='코멘트')
    a = ap.parse_args()
    for name, t in (('본문', a.text), ('둘째 문자', a.text2)):
        if t is not None:
            n = nbytes(t)
            print(f'{name} {n}바이트')
            if n > 2000:
                raise SystemExit(f'{name}이 2,000바이트를 넘어요({n}).')
    parts = to_one_jpg(a.png) if a.single else to_jpgs(a.png)
    print(f'이미지 {len(parts)}장: ' + ', '.join(f'{len(p) // 1024}KB' for p in parts))
    if a.dry:
        for i, p in enumerate(parts, 1):
            open(f'{os.path.splitext(a.png)[0]}_mms{i}.jpg', 'wb').write(p)
        print('dry run: 발송하지 않음'); return
    if not (a.to and a.frm):
        raise SystemExit('받는 번호(--to/SOLAPI_TO)와 보내는 번호(--from/SOLAPI_FROM)가 필요해요.')
    for i, p in enumerate(parts, 1):
        fid = call('/storage/v1/files', {'file': base64.b64encode(p).decode(), 'type': 'MMS'})['fileId']
        text = a.text if i == 1 else f'({i}/{len(parts)})'
        msg = {'to': a.to.replace('-', ''), 'from': a.frm.replace('-', ''), 'text': text,
               'subject': a.subject if len(parts) == 1 else f'{a.subject} {i}/{len(parts)}', 'imageId': fid}
        r = call('/messages/v4/send', {'message': msg})
        print(f'{i}/{len(parts)} 발송: {r.get("statusCode")} {r.get("statusMessage")}')
    if a.text2:
        msg = {'to': a.to.replace('-', ''), 'from': a.frm.replace('-', ''), 'text': a.text2, 'subject': a.subject2}
        r = call('/messages/v4/send', {'message': msg})
        print(f'둘째 문자 발송: {r.get("statusCode")} {r.get("statusMessage")}')

if __name__ == '__main__':
    main()
