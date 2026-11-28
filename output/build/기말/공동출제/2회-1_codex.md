MODEL: gpt-6-astra
EFFORT: medium

# Codex 작업 지시서 1/2: 2회(복습형) 17·18번 후보 + 서답형2

지침 전문(AGENTS.md · front.md · 2회 BRIEF.md)은 프롬프트 앞에 이미 있다. 이번 회차는 **복습형**이다(round.json). 분담표는 `output/build/기말/공동출제/2회_분담표.md`, 학교 선례는 `output/build/기말/지침/school_recipes.json`이다.
17·18은 Claude도 후보를 따로 낸다. 출제자 이름을 가린 독립 검토로 고른다.

| 번호 | 원문 | 축 | 정답 | 파일 |
|---|---|---|---|---|
| 17 후보 | M31 (Level Up, 난도 7) | ①형: 설정 유지·원리 교체. 최댓값·최솟값을 묻는다 | ⑤ | `output/build/기말/2회/후보/c17.py` + `verify_c17.py`, `cand='codex17'` |
| 18 후보 | D45 (Level Up, 난도 6) | ②형: 원리 유지·설정 교체. 값을 묻는다 | ② | `output/build/기말/2회/후보/c18.py` + `verify_c18.py`, `cand='codex18'` |
| 서답형2 | M56 (평가원, 난도 6) | 구조 변경 3단계 답만(4+4+2점), 체감 6/10 이하·약 4.5분. 세 단계 중 하나 이상은 최댓값·최솟값이 아닌 값 | — | `output/build/기말/2회/parts/c5.py` (`SITEMS={'S2': ...}`, `cand='codexS2'`) + `parts/verify_c5.py` |

## 규칙 요점
- **17·18·서답형2:** 0-4 설계 카드. 원문 핵심 한 줄(설정 줄·원리 줄)을 `core`에 적고, ①형은 원리 줄이, ②형은 설정 줄이 변형에서 통하지 않게 한다(d_step 0.75 이상). 흔한 패턴 금지. 문장 길이는 원문 이상, 조건은 모두 일하게(ABLATION). 원문 골격 유사도 0.25 이하. 17번은 **도함수가 판단에 실제로 들어가야** 한다(1회 Codex 17은 미분 없이 풀려 탈락).
- **선지:** 오름차순. 그럴듯한 오답(원문 방식대로 푼 값, 조건 하나를 놓친 값 등) **2개 이상을 선지 안에** 넣고 `wrongs=[...]`(선지 문자열 그대로)에 적는다. 공차는 1 기본, 오답을 넣기 위해 2·5·1/2 등으로 바꿀 수 있다(16·20처럼 키우지 않는다).
- **줄 바꾼 식·단서:** 원문에 없던 짧은 식은 문장 안에, 원문 단서는 원문 표현 그대로.
- **그림:** 만들지 않는다.
- **문항 dict 필드:** `author='codex'`, `vtype`, `effect`, `bunseok`(17·18·서답형2는 False), `precedent`, `wrongs`, `core=dict(axis, setting, principle, new)`, `cand`.
- **검사:** 각 verify는 마지막 줄이 `ALL OK`. `cd output/build/기말/2회 && python3 checkpart.py 후보/c17.py`(c18, parts/c5.py도)에서 중복 '금지'·말투·형식·흔한 패턴·학교 선례 '✗'가 0이어야 한다. '독립 검토 기록 없음'은 정상이다.
- `output/build/기말/2회/parts/p*.py`, `후보/p*.py`는 열지 않는다(독립성).
