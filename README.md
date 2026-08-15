# 오늘은 러닝 하는 날

## 실행 방법 (로컬)

```bash
pip install -r requirements.txt
python app.py
```

http://127.0.0.1:5000 접속

## 파일 구조

```
running-app/
  app.py               날씨 fetch + 코스 데이터 + 라우팅
  Procfile             Render 배포용
  requirements.txt
  templates/
    base.html
    index.html          날씨 + 코스 3개 카드
    course.html          경로 일러스트(SVG) + 거리 + 스텝 안내
  static/
    style.css
```

## 코스 수정하기

`app.py`의 `COURSES` 딕셔너리만 고치면 카드/상세 페이지 텍스트가 다 반영됩니다.
- `distance_km`, `summary`, `steps` 자유롭게 수정 가능
- 경로 그림(SVG)은 `templates/course.html` 안에 코스별로 따로 그려져 있어서, 코스를 새로 추가하면 `course.html`에 `{% elif key == "새코스키" %}` 블록도 추가해야 그림이 나와요 (텍스트 정보는 자동 반영되지만 그림만 예외)

## 배포 (기존 프로젝트들과 동일한 방식)

디스코드 알림이 없어서 환경변수 설정이 필요 없습니다 — 코드 그대로 배포하면 돼요.

1. 깃허브에 새 저장소 만들고 push
2. Render → New Web Service → 저장소 연결
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. Environment Variables 설정 안 해도 됩니다 (필요한 비밀값이 없음)
