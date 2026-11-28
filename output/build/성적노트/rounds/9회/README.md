# 9회 성적 문자 발송 준비물
- `문자1.txt`: 첫째 MMS 본문(객관 성적만) — 정사각 성적표 한 장과 함께
- `문자2.txt`: 둘째 LMS(개인 코멘트)
- `문자3.txt`: 셋째 LMS(이번 주 할 일·한마디)
- `미적분1_기말9회_성적표_정사각.png`: 1440×1440 정사각 성적표(`shot_square.js`, 내 위치 370명 환산 포함)
- `r9.json`: 성적표 원본 데이터(이름·학번 없음)
- 발송(성적노트 폴더에서, 먼저 `--dry`):
  `python3 send_solapi.py rounds/9회/미적분1_기말9회_성적표_정사각.png "$(cat rounds/9회/문자1.txt)" --text2 "$(cat rounds/9회/문자2.txt)" --text2 "$(cat rounds/9회/문자3.txt)" --single --subject "미적분Ⅰ 9회 성적" --subject2 "9회 코멘트" --subject2 "이번 주 할 일"`
- 키·번호는 환경 변수 SOLAPI_*
