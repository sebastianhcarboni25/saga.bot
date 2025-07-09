from flask import Flask, request, abort
import os

from linebot.v3.messaging import Configuration, MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging.models import TextMessage, ReplyMessageRequest

app = Flask(__name__)

config = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
line_bot_api = MessagingApi(config)
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent)
def handle_message(event):
    if not isinstance(event.message, TextMessageContent):
        # Ignore non-text messages
        return

    user_text = event.message.text.lower()

    if any(word in user_text for word in ["nabeshima", "나베시마", "鍋島"]):
        reply_text = (
            "나베시마 나오마사:\n사가번 초기 다이묘이자 문화 후원자입니다.\n\n"
            "鍋島直正:\n佐賀藩の初代大名で、文化の支援者でした。\n\n"
            "Nabeshima Naomasa:\nFirst lord of Saga Domain and patron of culture."
        )
    elif any(word in user_text for word in ["okuma", "오쿠마", "大隈"]):
        reply_text = (
            "오쿠마 시게노부:\n일본 근대 정치의 선구자이자 와세다대 설립자입니다.\n\n"
            "大隈重信:\n日本近代政治の先駆者で、早稲田大学の創立者です。\n\n"
            "Okuma Shigenobu:\nPioneer of modern Japanese politics and founder of Waseda University."
        )
    elif any(word in user_text for word in ["saga castle", "사가성", "佐賀城"]):
        reply_text = (
            "사가성:\n에도 시대 사가 번의 중심 성곽입니다.\n\n"
            "佐賀城:\n江戸時代の佐賀藩の中心的な城です。\n\n"
            "Saga Castle:\nCentral castle of the Saga Domain from Edo period."
        )
    elif any(word in user_text for word in ["balloon museum", "벌룬 박물관", "バルーンミュージアム", "熱気球博物館"]):
        reply_text = (
            "사가 벌룬 박물관:\n열기구 축제 관련 전시와 체험이 있습니다.\n\n"
            "バルーンミュージアム:\n熱気球祭りに関する展示と体験があります。\n\n"
            "Saga Balloon Museum:\nMuseum featuring exhibits and experiences on the balloon festival."
        )
    elif "restaurant" in user_text or "식당" in user_text or "レストラン" in user_text or "餐厅" in user_text:
        reply_text = (
            "추천 식당:\n"
            "1. 사쿠라 스시\n2. 도쿄 라멘\n3. 카레 하우스\n\n"
            "推荐餐厅:\n"
            "1. 樱花寿司\n2. 东京拉面\n3. 咖喱屋\n\n"
            "おすすめレストラン:\n"
            "1. さくら寿司\n2. 東京ラーメン\n3. カレーハウス\n\n"
            "Recommended Restaurants:\n"
            "1. Sakura Sushi\n2. Tokyo Ramen\n3. Curry House"
        )
    else:
        reply_text = (
            "사가 역사나 식당에 대해 알고 싶으면 관련 단어를 보내주세요.\n"
            "佐賀の歴史やレストランについて知りたい場合は、関連するキーワードを送信してください。\n"
            "如果想了解佐贺历史或餐厅，请发送相关关键词。\n"
            "Send keywords about Saga history or restaurants for info."
        )

    reply_request = ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text=reply_text)]
    )
    line_bot_api.reply_message(reply_request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
