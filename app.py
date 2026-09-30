import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# github path
BASE = "https://raw.githubusercontent.com/msk0923/dooray-godori/main/images/"

# 키워드 ↔ 파일 이름 목록은 emojis.json에서 관리
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "emojis.json"), encoding="utf-8") as f:
    EMOJIS = json.load(f)


@app.get("/")
def health():
    # 서버가 켜져 있는지 브라우저로 확인하는 용도
    return f"dooray-godori OK (이모티콘 {len(EMOJIS)}개)"


@app.post("/dooray/emo")
def emo():
    data = request.get_json(silent=True) or request.form
    key = (data.get("text") or "").strip()
    file = EMOJIS.get(key)

    # 디버깅용 로그 (토큰 값은 찍지 않고 입력 키워드만 기록)
    print(f"[godori] 요청 받음: text='{key}' -> {'찾음' if file else '없음'}", flush=True)

    if not file:
        # 키워드가 없거나 틀리면 입력한 본인에게만 안내
        return jsonify({
            "responseType": "ephemeral",
            "text": "사용 가능한 키워드: " + ", ".join(EMOJIS),
        })

    return jsonify({
        "responseType": "inChannel",
        "text": key,                                 # 두레이는 text가 있어야 메시지를 띄움
        "attachments": [{"imageUrl": BASE + file}],  # 큰 이미지 한 장만
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
