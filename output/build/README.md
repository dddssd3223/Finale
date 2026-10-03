# 재생성 방법 (내부용)

원본 `양정고 양식 복사본.hwpx`의 section0.xml을 직접 편집해 시험지를 만든다.

1. `content.py` / `solcontent.py` — 문항·해설 데이터(수식은 한글 수식 문법)
2. `python3 build.py preview && node measure.js` — 수식 크기 측정(원본 수식 127개로 보정)
3. `python3 tune.py` — python-hwpx 페이지 추정기로 문항 시작 위치를 원본과 맞춤(`fill.json`)
4. `python3 final.py 시험지.hwpx x` / `python3 solbuild.py` — HWPX 생성
5. `python3 -m hwpx.tools.validator 파일.hwpx` — OWPML 스키마 검증
6. `verify.py` — 20문항 정답 sympy 재검증
