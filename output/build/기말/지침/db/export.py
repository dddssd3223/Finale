# 스크래치패드 DB(variation_db_full.json) → 저장소 db/variation_db.json (내부 기록 칸 제외)
import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src)); drop = {'전처리_복구', '검토', 'batch', '원문_복원_메모'}
json.dump({k: {f: v for f, v in e.items() if f not in drop} for k, e in d.items()}, open(dst, 'w'), ensure_ascii=False, indent=0)
