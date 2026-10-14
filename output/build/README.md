# 재생성 (내부용)
- 바탕: `양정고 양식 복사본.pdf`의 벡터 페이지(머리글·틀·여백·꼬리말 원본 그대로). 결재란 행 제거, 학년/과목/문항수 문구를 굴림으로 교체.
- 본문: `content3.py` → Chromium 렌더링 후 원본 페이지 위에 겹침 (`python3 build3.py 시험지.pdf`).
- 해설: `python3 sol3.py 정답.pdf` / 정답 검증: `python3 verify.py`
- 글꼴: 본문 한컴바탕(HBATANG.TTF, 제공 egg 압축), 머리글 굴림(gulim.ttc), 수식 HyhwpEQ(제공 HYHWPEQ.TTF, PUA 인코딩 → eqfont.js에서 글자 치환). 글꼴 파일은 라이선스상 저장소에 포함하지 않음(EBDT·EBLC 제거 및 cmap 재작성 후 사용).
