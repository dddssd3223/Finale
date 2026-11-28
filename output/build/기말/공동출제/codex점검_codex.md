# Codex 작업 지시서: codex점검 (파이프라인 점검용 1문항)

| 번호 | 원문 키 | 출처 구분 | 목표 난도 | 정답 번호 | 파일 |
|---|---|---|---|---|---|
| 1 | I49 | 평가원 | 하 | ③ | parts/c1.py, parts/verify_c1.py |

- 번호대 1–4 기준(front.md '1–4번' 절): 숫자·조건 변경 위주의 쉬운 문항, 배점 4.0.
- 형식은 output/build/기말/견본3/parts/p1.py와 같다(ITEMS = {1: dict(...)}), dict에 author='codex'.
- 검증: verify_c1.py ALL OK, `cd output/build/기말/견본3 && python3 checkpart.py ../codex점검/parts/c1.py` 통과.
- 재실행: 시크릿 이름 API_KEY
- 재실행 2: 한글 경로 처리 수정
- 재실행 3: codex 0.166 옵션(-s workspace-write)
- 재실행 4: codex login
