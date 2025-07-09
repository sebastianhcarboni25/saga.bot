from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random
import requests

def get_restaurants(location, lang="en"):
    api_key = os.environ["GOOGLE_API_KEY"]
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"restaurants near {location}",
        "language": lang,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        return "Sorry, I couldn’t find any restaurants."

    # Pick top 3 results
    results = data["results"][:3]
    reply = ""
    for r in results:
        name = r["name"]
        address = r.get("formatted_address", "No address")
        rating = r.get("rating", "No rating")
        reply += f"🍽️ {name}\n⭐ {rating} | 📍 {address}\n\n"
    return reply.strip()

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

restaurants = {
    "english": [
        "🍜 Ramen Kura – Best pork ramen near Saga Station!",
        "🍣 Sushi Tama – Great sushi at a local price.",
        "🍛 Saga Curry Honpo – Tasty local beef curry.",
        "🍖 Yakiniku Ranmaru – Delicious grilled meat!",
        "☕ Café Morinokaze – Cute cafe with relaxing vibes."
    ],
    "japanese": [
        "🍜 佐賀駅近くのラーメン蔵がおすすめ！",
        "🍣 鮨たまは地元で人気の寿司屋です。",
        "🍛 佐賀カレーホンポでビーフカレーをどうぞ。",
        "🍖 焼肉らんまるでお肉を堪能してね！",
        "☕ カフェ森の風は落ち着ける素敵なカフェです。"
    ],
    "korean": [
        "🍜 사가역 근처 라멘 쿠라는 최고예요!",
        "🍣 스시 타마는 신선한 초밥이 맛있어요.",
        "🍛 사가 커리 혼포의 비프 커리를 추천합니다.",
        "🍖 야키니쿠 란마루에서 고기를 즐겨보세요!",
        "☕ 카페 모리노카제는 휴식하기 좋은 장소예요."
    ],
    "chinese": [
        "🍜 佐贺车站附近的拉面藏非常好吃！",
        "🍣 寿司玉是当地人推荐的寿司店。",
        "🍛 佐贺咖喱本铺的牛肉咖喱很好吃。",
        "🍖 烧肉兰丸的烤肉超级棒！",
        "☕ 森之风咖啡厅适合放松。"
    ]
}

history_facts = {
    "english": "🔸 Nabeshima Naomasa was a modernizing daimyo from Saga who supported the Meiji Restoration.",
    "japanese": "🔸 鍋島直正は佐賀の藩主で、明治維新を支えた近代化の先駆者です。",
    "korean": "🔸 나베시마 나오마사는 메이지 유신을 지지한 사가의 근대화된 영주였습니다.",
    "chinese": "🔸 锅岛直正是支持明治维新的佐贺藩主之一，是近代化的先锋。"
}

@app.route("/")
def home():
    return "Saga bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.lower()
    language = "english"
    for lang in ["japanese", "korean", "chinese", "english"]:
        if lang in user_msg:
            language = lang
            break
    
     if "nabeshima" in user_msg or "history" in user_msg:
        reply = history_facts[language]
    elif "restaurant" in user_msg or "eat" in user_msg or "food" in user_msg:
        reply = get_restaurants("Saga", lang=language[:2])

    else:
        reply = "Hi! 🌏 Type 'restaurant' or 'history', and add a language: english, japanese, korean, chinese."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
