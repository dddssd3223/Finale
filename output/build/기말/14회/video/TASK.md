# 14회 해설 영상 대본 작성 (손필기 판서 + 목소리)

양정고 2학년 미적분Ⅰ 기말 모의고사 14회의 고난도 문항 해설 영상을 만든다. 너는 맡은 문항의 **판서 순서와 나레이션 대본**을 JSON으로 쓴다. 화면 그리기와 음성 합성은 본체가 한다.

## 읽을 것
- 문항: `cd /home/user/Finale/output/build/기말/14회 && python3 -c "import content3 as c, json; it=c.ITEMS[N]; print(json.dumps({k:it[k] for k in ('body','cond','bogi','choices','ans') if k in it}, ensure_ascii=False, indent=1))"` (서답형2는 `c.SITEMS['S2']`의 body·subs·ans)
- 이미 완성된 해설: `haeseol/items_*.json` 에서 `"n"`이 맡은 번호인 항목(think, flow, body, justify). 해설의 풀이 흐름과 답을 그대로 따른다. 새로운 풀이를 만들지 않는다.
- 그림이 있는 문항: 이번 영상 대상(14–18번·서답형2)에는 그림이 없다. figure는 쓰지 않는다.

## 결과 파일
`video/script_<번호>.json` (서답형2는 `script_S2.json`). 형식:

```json
{"n": "18", "title": "두 감소 구간이 이어지는 조건", "minutes": 4,
 "pages": [
  {"kind": "problem", "steps": [{"say": "18번입니다. ..."}]},
  {"kind": "board", "heading": "g′(x)의 부호", "steps": [
     {"board": "\\(m(t)=f(t)-|f(t)|\\) 로 두면", "say": "..."},
     {"board": "\\[g'(x)=k\\,m(kx)+m(x)\\le 0\\]", "say": "...", "mark": "key"}
  ]}
 ]}
```

- 첫 page는 `"kind": "problem"`: 문제 전체가 인쇄체로 한 번에 뜬다. steps는 1–2개, 무엇을 묻는지와 조건이 무슨 뜻인지 말로만 짚는다.
- 그다음 page들은 `"kind": "board"`: 판서 한 줄(`board`)이 손글씨로 왼쪽부터 써지면서 그 줄의 나레이션(`say`)이 나온다.
  - `board`는 짧게(한 줄, 한글 25자 안팎 또는 수식 한 줄). 수식은 `\( \)`·`\[ \]` KaTeX. 부등호는 그냥 `<` `>`를 써도 된다.
  - 한 page에 steps 4–6개. 넘치면 새 page(`heading`은 그 page의 단계 제목, STEP 흐름을 따른다).
  - 핵심 판단 줄에는 `"mark": "key"`(빨간 펜 + 밑줄). 함정·오답 경로는 `"mark": "trap"`. 정답 줄은 `"mark": "answer"`.
  - 그림을 띄울 page는 `"figure": "fig_15.svg"`.
- 마지막 page 끝 step은 정답과 함정 한 줄 정리.

## 나레이션(`say`) 규칙
- 선생님이 판서하며 설명하는 말투, 존댓말 '-습니다/-ㅂ니다'. 한 step에 1–3문장.
- 수식은 **읽는 말로** 쓴다. LaTeX·기호를 그대로 쓰지 않는다. 예: \(f'(x)\) → "에프 프라임 엑스", \(\int_0^x f(t)\,dt\) → "영부터 엑스까지 에프 티 디티의 정적분", \(x\ge 2\) → "엑스가 2 이상", \(\alpha\) → "알파", \(k^2\le 9\) → "케이 제곱이 9 이하".
- 판서 줄을 그대로 읽기만 하지 말고, 왜 그렇게 쓰는지 한마디를 붙인다.
- 문항당 나레이션 합계 600–1,000자(3–5분). 18번·서답형2는 1,200자까지.
- 교육과정 밖 도구(합성함수 미분 등)는 말하지 않는다. '이러한'은 쓰지 않는다.

## 끝나면
`python3 -c "import json; json.load(open('파일'))"`로 확인하고, 보고는 한 줄(파일 이름, page 수, 나레이션 글자 수). 커밋하지 않는다. 세션 생성 도구는 쓰지 않는다.
