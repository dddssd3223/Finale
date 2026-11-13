MODEL: gpt-6-astra
EFFORT: medium

# Codex 작업 지시서 2/2: 2회(복습형) 홀수 1–15번

지침 전문(AGENTS.md · front.md · 2회 BRIEF.md)은 프롬프트 앞에 이미 있다. 이번 회차는 **복습형**이다(round.json). 분담표는 `output/build/기말/공동출제/2회_분담표.md`, 학교 선례는 `output/build/기말/지침/school_recipes.json`이다.

| 번호 | 원문 | 분석집 방향(`bunseok`) | 그림 | 목표 체감 · 시간 | 정답 | 파일 |
|---|---|---|---|---|---|---|
| 1 | D17 (EBS, 난도 3) | — (False) | | 1.3 · 0.7분 | ② | `parts/c1.py` |
| 3 | I29 (EBS, 3) | **○ (True)** | | 1.3 · 0.8분 | ① | `parts/c1.py` |
| 5 | J20 (EBS, 4) | **○ (True)** | | 3.3 · 1.4분 | ⑤ | `parts/c1.py` |
| 7 | J45 (Level Up, 5) | — (False) | | 4.7 · 2.0분 | ④ | `parts/c1.py` |
| 9 | J58 (평가원, 5) | — (False) | **그림 문항** | 5.7 · 3.0분 | ③ | `parts/c2.py` |
| 11 | I43 (Level Up, 5) | **○ (True)** | | 3.7 · 1.7분 | ① | `parts/c2.py` |
| 13 | I45 (Level Up, 4) | — (False) | | 4.7 · 2.4분 | ② | `parts/c2.py` |
| 15 | M66 (평가원, 6) | **○ (True)** | | 5.7 · 3.0분 | ③ | `parts/c2.py` |

파일은 모두 `output/build/기말/2회/parts/` 아래(`c1.py`+`verify_c1.py`, `c2.py`+`verify_c2.py`, `ITEMS={번호: dict(...)}`).

## 규칙 요점
- **복습형:** `bunseok=True` 문항(3·5·11·15)만 analysis.json의 `study`(분석집 판정·TIP·변형 방향)를 쓰고, 분석집 TIP에서 나온 함정을 쓸 수 있다(`vtype`에 '함정 추가'). 나머지는 학교형처럼 함정 없이 낸다. 분석집과 같은 문항은 금지.
- **무게:** 1–12번은 같음·쉬워짐(어려워짐은 회 전체 1개까지 — 이번에는 Claude 쪽 짝수에서 쓰지 않으면 9번에 1개 허용), 13–16번은 어려워짐 1–2개(13·15 중 하나). 목표 체감·시간을 지킨다(1회 측정에서 3번이 무거웠다: 1–4번은 한두 단계로 끝나게).
- **선지:** 오름차순. 그럴듯한 오답을 선지 안에(`wrongs=[...]`, 13·15번은 2개 이상, 1–11번은 1개 이상). 공차는 1 기본, 몇 문항은 2·5·1/2 등(회 전체 공차 1은 10–13개).
- **9번 그림:** 그림 파일은 만들지 않는다. 본문에 `<div class="fig"><img src="fig_9.svg" style="width:150pt"></div>` 자리만 두고, note에 그릴 내용(함수식, 라벨, 칠할 영역 이름 A·B)을 적는다. Claude가 그린다. 풀이에 쓰는 값은 본문에 쓴다.
- **줄 바꾼 식·단서:** 원문에 없던 짧은 식은 문장 안에, 원문 단서는 원문 표현 그대로.
- **문항 dict 필드:** `author='codex'`, `vtype`, `effect`, `bunseok`, `precedent`, `wrongs`.
- **검사:** 각 verify는 마지막 줄이 `ALL OK`. `cd output/build/기말/2회 && python3 checkpart.py parts/c1.py`(c2도)에서 중복 '금지'·말투·형식·학교 선례 '✗'가 0이어야 한다.
- `output/build/기말/2회/parts/p*.py`는 열지 않는다(독립성).
