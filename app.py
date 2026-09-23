from flask import Flask, request, jsonify

app = Flask(__name__)

BASE = "https://raw.githubusercontent.com/msk0923/dooray-godori/main/"

EMOJIS = {
    "확인":   BASE + "01_confirm.png",
    "좋아요": BASE + "02_good.png",
    "작업중": BASE + "03_work.png",
    "확인중": BASE + "04_cheking.png",
    "회의중": BASE + "05_meeting.png",
    "부탁":   BASE + "06_please.png",
    "죄송":   BASE + "07_sorry.png",
    "완료":   BASE + "08_done.png",
}


@app.get("/")
def health():
    # 서버가 켜져 있는지 브라우저로 확인하는 용도
    return "dooray-godori OK"


@app.post("/dooray/emo")
def emo():
    data = request.get_json(silent=True) or request.form
    key = (data.get("text") or "").strip()
    url = EMOJIS.get(key)

    # 디버깅용 로그 (토큰 값은 찍지 않고 입력 키워드만 기록)
    print(f"[godori] 요청 받음: text='{key}' -> {'찾음' if url else '없음'}", flush=True)

    if not url:
        # 키워드가 없거나 틀리면 입력한 본인에게만 안내
        return jsonify({
            "responseType": "ephemeral",
            "text": "사용 가능한 키워드: " + ", ".join(EMOJIS),
        })

    return jsonify({
        "responseType": "inChannel",
       "text": f"[{key}]({url})",
        "attachments": [{"imageUrl": url, "thumbUrl": url}],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
