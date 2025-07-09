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
    message = event.message
    if isinstance(message, TextMessageContent):
        text = message.text.lower()

        if "nabeshima" in text or "나베시마" in text or "鍋島" in text:
            reply = (
                "나베시마 나오마사:\n"
                "사가번의 초기 다이묘로, 영리한 군주이자 문화 후원자였습니다.\n\n"
                "鍋島直正:\n"
                "佐賀藩の初代大名であり、聡明な統治者かつ文化の支援者でした。\n\n"
                "Nabeshima Naomasa:\n"
                "The first lord of Saga Domain, known as a wise ruler and patron of culture.\n\n"
                "鍋島直正：\n"
                "佐賀藩の初代藩主であり、文化の後援者としても知られています。"
            )

        elif "okuma" in text or "오쿠마" in text or "大隈" in text:
            reply = (
                "오쿠마 시게노부:\n"
                "일본 근대 정치의 선구자이자 와세다 대학 설립자입니다.\n\n"
                "大隈重信:\n"
                "日本近代政治の先駆者であり、早稲田大学の創立者です。\n\n"
                "Okuma Shigenobu:\n"
                "A pioneer of modern Japanese politics and founder of Waseda University.\n\n"
                "大隈重信：\n"
                "日本の近代政治の先駆者であり、早稲田大学の創設者です。"
            )

        elif "saga castle" in text or "사가성" in text or "佐賀城" in text:
            reply = (
                "사가성:\n"
                "에도 시대에 세워진 사가 번의 중심 성곽입니다.\n\n"
                "佐賀城:\n"
                "江戸時代に建てられた佐賀藩の中心的な城郭です。\n\n"
                "Saga Castle:\n"
                "The central castle of the Saga Domain built during the Edo period.\n\n"
                "佐賀城：\n"
                "江戸時代に建てられた佐賀藩の中心的な城です。"
            )

        elif "balloon museum" in text or "벌룬 박물관" in text or "バルーンミュージアム" in text or "熱気球博物館" in text:
            reply = (
                "사가 벌룬 박물관:\n"
                "열기구 축제와 관련된 전시와 체험을 제공하는 박물관입니다.\n\n"
                "バルーンミュージアム:\n"
                "熱気球祭りに関する展示や体験を提供する博物館です。\n\n"
                "Saga Balloon Museum:\n"
                "A museum offering exhibits and experiences related to the hot air balloon festival.\n\n"
                "熱気球博物館：\n"
                "熱気球祭りに関連した展示と体験ができます。"
            )

        elif "restaurant" in text:
            reply = (
                "여기 추천 식당 목록입니다:\n"
                "1. 사쿠라 스시\n"
                "2. 도쿄 라멘\n"
                "3. 카레 하우스\n"
                "4. 도시락 익스프레스\n"
                "5. 우동 코너\n\n"
                "这里是推荐的餐厅列表:\n"
                "1. 樱花寿司\n"
                "2. 东京拉面\n"
                "3. 咖喱屋\n"
                "4. 便当快递\n"
                "5. 乌冬角落\n\n"
                "おすすめのレストランリストです:\n"
                "1. さくら寿司\n"
                "2. 東京ラーメン\n"
                "3. カレーハウス\n"
                "4. 弁当エクスプレス\n"
                "5. うどんコーナー\n\n"
                "Here is the list of recommended restaurants:\n"
                "1. Sakura Sushi\n"
                "2. Tokyo Ramen\n"
                "3. Curry House\n"
                "4. Bento Express\n"
                "5. Udon Corner\n"
            )

        else:
            reply = (
                "식당이나 사가 역사에 대해 알고 싶으면 관련 단어를 보내주세요.\n"
                "如果您想了解餐厅或佐贺历史，请发送相关词汇。\n"
                "レストランや佐賀の歴史について知りたい場合は、関連するキーワードを送ってください。\n"
                "Send keywords about restaurants or Saga history to get info.\n"
            )

        reply_request = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply)]
        )

        line_bot_api.reply_message(reply_request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
