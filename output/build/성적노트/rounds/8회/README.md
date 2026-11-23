# 8회 성적 문자 발송 준비물
- `문자.txt`: LMS 본문
- `미적분1_기말8회_성적표.png`: MMS 이미지(send_solapi.py가 3장으로 나눔)
- `r8.json`: 성적표 원본 데이터(이름·학번 없음)
- 발송: `python3 output/build/성적노트/send_solapi.py output/build/성적노트/rounds/8회/미적분1_기말8회_성적표.png "$(cat output/build/성적노트/rounds/8회/문자.txt)"` (먼저 `--dry`로 확인, 키·번호는 환경 변수 SOLAPI_*)
