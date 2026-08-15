from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# ---------------------------------------------------------
# 코스 정보. 여기 값만 바꾸면 카드/상세 페이지 내용이 통째로 바뀝니다.
# image_file: static/images/ 폴더에 넣을 지도 캡처 이미지 파일명.
#             카카오맵/네이버지도에서 경로 그려서 캡처한 스크린샷을 그대로 저장하면 됩니다.
# ---------------------------------------------------------

COURSES = {
    "danghyeoncheon": {
        "name": "당현천",
        "start": "상계역",
        "distance_km": 8.15,
        "summary": "상계역 출발, 당현천 따라 쭉 내려가서 노원구청 찍고 복귀",
        "steps": ["상계역 출발", "당현천을 따라 남하", "중랑천 합류부에서 노원구청 방면으로 우회전", "노원구청 찍고 유턴", "상계역으로 복귀"],
        "image_file": "danghyeoncheon.png",
    },
    "seoulforest": {
        "name": "서울숲",
        "start": "자양역 (CU 편의점 앞)",
        "distance_km": 8.15,  # 실측 데이터 못 찾아서 우선 예시값. GPX 앱으로 실측하면 여기 숫자만 바꾸면 됨
        "summary": "자양역 CU 앞 출발, 서울숲까지 달려서 한 바퀴 돌고 복귀",
        "steps": ["자양역 CU 편의점 출발", "서울숲 방면으로 진입", "서울숲 둘레 한 바퀴", "왔던 길로 자양역 복귀"],
        "image_file": "seoulforest.png",
    },
    "cheonho": {
        "name": "천호대교",
        "start": "광나루역",
        "distance_km": 8.0,
        "summary": "광나루역 출발, 천호대교 찍고 왕복",
        "steps": ["광나루역 출발", "한강변 따라 천호대교 방면 진행", "천호대교 아래에서 턴", "광나루역으로 복귀"],
        "image_file": "cheonho.png",
    },
}


def get_weather():
    """
    wttr.in에서 서울 현재 날씨를 가져옵니다. 키 발급 없이 바로 쓸 수 있어요.
    강수확률은 시간대별 예보 데이터 중 하나를 골라 어림잡은 값이라 100% 정확하진 않아요.
    """
    try:
        res = requests.get("https://wttr.in/Seoul?format=j1", timeout=5)
        res.raise_for_status()
        data = res.json()
        current = data["current_condition"][0]
        # 시간대별 예보(3시간 간격 8개) 중 중간쯤을 강수확률 참고용으로 사용
        hourly = data["weather"][0]["hourly"]
        chance_of_rain = hourly[len(hourly) // 2]["chanceofrain"]
        return {
            "desc": current["weatherDesc"][0]["value"],
            "temp_c": current["temp_C"],
            "chance_of_rain": chance_of_rain,
        }
    except Exception:
        return None


@app.route("/")
def index():
    weather = get_weather()
    return render_template("index.html", weather=weather, courses=COURSES)


@app.route("/course/<course_key>")
def course_detail(course_key):
    if course_key not in COURSES:
        return render_template("index.html", weather=get_weather(), courses=COURSES)
    course = COURSES[course_key]

    # static/images/ 폴더에 해당 파일이 실제로 있는지 확인
    image_path = os.path.join(app.static_folder, "images", course["image_file"])
    image_exists = os.path.isfile(image_path)

    return render_template("course.html", key=course_key, course=course, image_exists=image_exists)


if __name__ == "__main__":
    app.run(debug=True)
