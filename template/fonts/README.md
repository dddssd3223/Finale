# 글꼴

시험지 양식을 똑같이 재현하려면 아래 글꼴이 모두 이 폴더에 있어야 합니다.

## 저장소에 포함된 글꼴 (자유 라이선스)

| 파일 | 글꼴 | 용도 |
|---|---|---|
| `9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf`, `9Bty3DZF0dXLMZlywRbVRNhxy2pXV1A0.ttf` | 나눔명조 Regular / Bold (OFL) | 한글 대체 글꼴 (`MJ`) |
| `buE4poGnedXvwgX8.ttf` 외 `buE*.ttf` 3개 | Tinos Regular / Italic / Bold / BoldItalic (Apache 2.0) | 그림 라벨, 일부 수식 대체 (`TN`) |
| `pen.ttf` | Nanum Pen Script (OFL) | 채점용 빨간 손글씨 |

## 직접 넣어야 하는 글꼴 (상용, 저장소에 올리지 않음)

이 글꼴들은 재배포가 허용되지 않아 저장소에서 빠져 있습니다(`.gitignore`). 한글(한컴오피스)이나 Windows가 설치된 PC에서 복사해 아래 파일 이름으로 넣으세요.

| 넣을 파일 이름 | 원래 글꼴 | 어디서 | 용도 |
|---|---|---|---|
| `hbatang_web.ttf` | 한컴바탕 (Haansoft Batang) | 한컴오피스 설치 폴더의 `HANBatang.ttf` 등 | 본문 글꼴 (`HB`) |
| `hyhwpeq_web.ttf` | HyhwpEQ (한글 수식 글꼴) | 한컴오피스 설치 폴더의 `HYHWPEQ.TTF` | 수식의 영문·숫자 (한글 수식 편집기 모양) |
| `gulim_web.ttf` | 굴림 | Windows `C:\Windows\Fonts\gulim.ttc` → TTF로 추출 | 안내문·보기 번호 (`GL`) |
| `gulim.ttf` | 굴림 | 위와 같음 (같은 파일을 두 이름으로 넣어도 됨) | 시험지 머리글 다시 쓰기 (PyMuPDF) |

`.ttc`에서 굴림만 꺼내려면 다음을 실행합니다.

```python
from fontTools.ttLib import TTCollection
TTCollection('gulim.ttc').fonts[0].save('gulim.ttf')
```

글꼴이 빠지면 빌드는 되지만 모양이 원본 양식과 달라집니다. 특히 수식이 한글 수식 편집기 모양으로 나오지 않습니다.
