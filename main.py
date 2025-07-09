from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

# Restaurant list (generic suggestions)
restaurants = {
    "en": [
        "🍜 Fukunoie Ramen, Honjo - Saga's students favourite Ramen",
        "🍣 Hamazushi – Great sushi at a local price.",
        "🍛 Yellow Spice Curry Tojinmachi – Tasty local curry.",
        "🍖 Ju ju Karubi – Delicious grilled meat!",
        "☕ Nowhere coffee – Modern cafe with relaxing vibes."
    ],
    "jp": [
        "🍜 本庄のふくの家ラーメン – 学生に人気！",
        "🍣 はま寿司 – 手頃な価格で美味しい寿司。",
        "🍛 イエロースパイスカレー唐人町 – 地元の人気カレー！",
        "🍖 じゅじゅカルビ – 美味しい焼肉のお店！",
        "☕ Nowhere Coffee – モダンで落ち着けるカフェ。"
    ],
    "cn": [
        "🍜 本庄福之家拉面 – 佐贺学生最爱！",
        "🍣 Hama寿司 – 价格实惠的美味寿司。",
        "🍛 Yellow Spice咖喱 – 地道风味咖喱。",
        "🍖 Juju Karubi – 烤肉非常棒！",
        "☕ Nowhere coffee – 现代风格、适合放松的咖啡馆。"
    ],
    "kr": [
        "🍜 후쿠노이에 라멘 – 사가 대학생들에게 인기!",
        "🍣 하마스시 – 저렴하고 맛있는 스시.",
        "🍛 옐로우 스파이스 카레 – 현지인이 추천하는 카레.",
        "🍖 주주 카루비 – 맛있는 불고기 집!",
        "☕ 노웨어 커피 – 모던하고 편안한 분위기의 카페."
    ],
    "vi": [
        "🍜 Fukunoie Ramen – Mì ramen được sinh viên ở Saga yêu thích!",
        "🍣 Hamazushi – Sushi ngon và giá rẻ.",
        "🍛 Yellow Spice Curry – Cà ri địa phương ngon tuyệt.",
        "🍖 Ju ju Karubi – Thịt nướng ngon không thể cưỡng!",
        "☕ Nowhere coffee – Quán cafe hiện đại và yên tĩnh."
    ]
}

# Named best-of spots
best_places = {
    "best curry": {
        "en": "🍛 Try Stool Coffee – top-rated for beef curry!",
        "jp": "🍛 Stool Coffeeのビーフカレーは絶品！",
        "cn": "🍛 推荐Stool Coffee的牛肉咖喱！",
        "kr": "🍛 스툴 커피 – 소고기 카레가 유명해요!",
        "vi": "🍛 Hãy thử cà ri bò tại Stool Coffee!"
    },
    "best coffee": {
        "en": "☕ Check out 03 Coffee – perfect for relaxing.",
        "jp": "☕ 03 Coffeeでリラックスしましょう！",
        "cn": "☕ 试试03 Coffee，放松好去处。",
        "kr": "☕ 03 커피 – 휴식에 딱 좋은 곳이에요.",
        "vi": "☕ Hãy ghé 03 Coffee để thư giãn nhé!"
    },
    "best sushi": {
        "en": "🍣 Visit Kura Sushi for fresh sushi!",
        "jp": "🍣 くら寿司へ行ってみて！",
        "cn": "🍣 去Kura寿司品尝新鲜美味！",
        "kr": "🍣 쿠라 스시 – 신선한 초밥!",
        "vi": "🍣 Thử sushi tươi tại Kura Sushi nhé!"
    },
    "best ramen": {
        "en": "🍜 RaRaRamen is a local favourite!",
        "jp": "🍜 ラララーメンは地元で人気！",
        "cn": "🍜 RaRa拉面是当地最爱！",
        "kr": "🍜 라라라멘은 지역 주민이 추천해요!",
        "vi": "🍜 RaRaRamen là món mì được yêu thích ở đây!"
    },
    "best yakiniku": {
        "en": "🔥 Yakiniku King is the go-to for grilled meat!",
        "jp": "🔥 焼肉キングがおすすめ！",
        "cn": "🔥 烤肉推荐Yakiniku King！",
        "kr": "🔥 야키니쿠 킹 – 고기 맛집이에요!",
        "vi": "🔥 Thử món nướng tại Yakiniku King nhé!"
    }
}

# Historical content
historical_figures = {
    "nabeshima": {
        "en": "🔸 Nabeshima Naomasa: Modernized Saga during the Bakumatsu.",
        "jp": "🔸 鍋島直正：幕末に佐賀を近代化した大名。",
        "cn": "🔸 锅岛直正：在幕末时期推进佐贺现代化。",
        "kr": "🔸 나베시마 나오마사 – 사가의 근대화를 이끈 영주.",
        "vi": "🔸 Nabeshima Naomasa: Người hiện đại hóa Saga thời Bakumatsu."
    }
}

seven_wise_men = {
    "okuma": {
        "en": "🏛️ Okuma Shigenobu: Founder of Waseda University and PM of Japan.",
        "jp": "🏛️ 大隈重信：早稲田大学の創設者、元総理大臣。",
        "cn": "🏛️ 大隈重信：早稻田大学创始人，日本前首相。",
        "kr": "🏛️ 오쿠마 시게노부 – 와세다 대학 설립자, 일본 총리.",
        "vi": "🏛️ Okuma Shigenobu: Người sáng lập ĐH Waseda và Thủ tướng Nhật."
    }
}

saga_castle_info = {
    "en": "🏯 Saga Castle: Originally built in 1602, now a history museum.",
    "jp": "🏯 佐賀城：1602年に築城。現在は歴史博物館です。",
    "cn": "🏯 佐贺城：建于1602年，现在是历史博物馆。",
    "kr": "🏯 사가 성 – 1602년에 지어진 역사적 성입니다.",
    "vi": "🏯 Lâu đài Saga: Xây dựng năm 1602, nay là bảo tàng."
}

def detect_language(text):
    if "jp" in text:
        return "jp"
    elif "kr" in text:
        return "kr"
    elif "cn" in text:
        return "cn"
    elif "vi" in text:
        return "vi"
    else:
        return "en"

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
    lang = detect_language(user_msg)

    for keyword in best_places:
        if keyword in user_msg:
            reply = best_places[keyword][lang]
            break
    else:
        if any(word in user_msg for word in ["eat", "restaurant", "food", "hungry"]):
            reply = random.choice(restaurants[lang])
        elif any(name in user_msg for name in historical_figures):
            for name in historical_figures:
                if name in user_msg:
                    reply = historical_figures[name][lang]
                    break
        elif any(name in user_msg for name in seven_wise_men):
            for name in seven_wise_men:
                if name in user_msg:
                    reply = seven_wise_men[name][lang]
                    break
        elif "castle" in user_msg or "saga castle" in user_msg:
            reply = saga_castle_info[lang]
        else:
            reply = {
                "en": "Hi! Try asking for 'best ramen' or 'Saga Castle'. Add 'jp', 'cn', 'kr' or 'vi' for language!",
                "jp": "こんにちは！「best ramen」や「佐賀城」と聞いてみてください。「jp」「cn」など言語も指定できます。",
                "cn": "你好！试试输入“best ramen”或“Saga Castle”。可加“cn”“jp”等选择语言。",
                "kr": "안녕하세요! ‘best ramen’ 또는 ‘사가 성’을 입력해보세요. 언어는 ‘kr’ 같이 지정할 수 있어요.",
                "vi": "Xin chào! Hãy thử 'best ramen' hoặc 'Lâu đài Saga'. Có thể thêm 'vi', 'jp' để chọn ngôn ngữ."
            }[lang]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
