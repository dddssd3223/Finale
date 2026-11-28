MODEL: gpt-6-astra
EFFORT: medium

# Codex 작업 지시서 1/2: 1회(학교형) 17·18번 후보 + 서답형1

먼저 다음 셋을 읽는다.
- `AGENTS.md`
- `output/build/기말/1회/BRIEF.md`: 이번 회차는 **학교형**이다. round.json에 적혀 있다.
- `output/build/기말/지침/front.md`: **0-8 학교 선례(가장 우선)**, 0-4 설계 카드, 0-1(익스텐션은 그대로 금지, 독특한 변형만 참고)

분담표는 `output/build/기말/공동출제/1회_분담표.md`다. 학교 선례 기록은 `output/build/기말/지침/school_recipes.json`이다.
17·18은 Claude도 후보를 따로 낸다. 출제자 이름을 가린 독립 검토로 고른다.

| 번호 | 원문 | 축 | 정답 | 파일 |
|---|---|---|---|---|
| 17 후보 | M32 (Level Up, 난도 6) | ①형: 설정 유지·원리 교체. 최댓값·최솟값을 묻는다 | ③ | `output/build/기말/1회/후보/c17.py` + `verify_c17.py`, `cand='codex17'` |
| 18 후보 | J33 (Level Up, 난도 5) | ②형: 원리 유지·설정 교체. 값을 묻는다 | ④ | `output/build/기말/1회/후보/c18.py` + `verify_c18.py`, `cand='codex18'` |
| 서답형1 | 자체 출제(가장 가까운 유형 D15, `key='D15'`, `src='학교 자체 출제'`) | 기본 서술 4+6점, 풀이 과정. 무겁지 않게(체감 3.0) | — | `output/build/기말/1회/parts/c4.py` (`SITEMS={'S1': ...}`) + `parts/verify_c4.py` |

## 규칙 요점
- **17·18:** 0-4 설계 카드를 따른다.
  - 원문 핵심 한 줄(설정 줄·원리 줄)을 적는다. 흔한 패턴은 금지다.
  - 문장 길이는 원문 이상, 조건은 모두 일하게(ABLATION) 한다.
  - 원문 골격 유사도는 0.25 이하로 한다(학교 17·18 실측 0.06–0.15).
  - 경계 판단은 바뀐 원리에서 자연히 생기는 것 하나만 둔다. 함정을 덧붙이지 않는다.
- **선지 (0-8):** 오름차순, 공차 1 위주(2·5·1/2·1/5 가능). 오답 근거를 넣으려고 공차를 키우지 않는다.
- **구하는 값:** 자연스러운 함숫값이나 정적분으로 한다. 끼워 맞춘 값은 쓰지 않는다.
- **문항 dict 필드:** `author='codex'`, `vtype`, `effect`, `bunseok=False`, `precedent`(따른 학교 선례 또는 참고한 익스텐션 id)를 넣는다. 17·18에는 `core=dict(axis, setting, principle, new)`와 `cand`도 넣는다.
- **검사:** 각 verify는 마지막 줄이 `ALL OK`여야 한다. `cd output/build/기말/1회 && python3 checkpart.py 후보/c17.py`(c18, parts/c4.py도)에서 다음이 0이어야 한다. '독립 검토 기록 없음'은 정상이다.
  - 중복 '금지'
  - 말투·형식 표시
  - 흔한 패턴 표시
  - 학교 선례 '✗' 표시
- **보고서:** `output/build/기말/1회/후보/CODEX_REPORT_1.md`에 쓴다.
- `output/build/기말/1회/parts/p*.py`, `후보/p*.py`는 열지 않는다(독립성).
