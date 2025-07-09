from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

restaurants = [
    "🍜 Ramen Kura – Best pork ramen near Saga Station!",
    "🍣 Sushi Tama – Great sushi at a local price.",
    "🍛 Saga Curry Honpo – Tasty local beef curry.",
    "🍖 Yakiniku Ranmaru – Delicious grilled meat!",
    "☕ Café Morinokaze – Cute cafe with relaxing vibes."
]

historical_figures = {
    "nabeshima": "🔸 Nabeshima Naomasa: A powerful daimyo who modernized Saga during the Bakumatsu period.",
    "naomasa": "🔸 Nabeshima Naomasa modernized Saga’s army and supported the Meiji Restoration.",
    "history": "📜 Saga was home to leaders who helped modernize Japan, including Nabeshima Naomasa and others."
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
    if any(word in user_msg for word in ["eat", "restaurant", "food", "hungry"]):
        reply = random.choice(restaurants)
    elif any(name in user_msg for name in historical_figures):
        for name in historical_figures:
            if name in user_msg:
                reply = historical_figures[name]
                break
    else:
        reply = "Hi! I can recommend restaurants in Saga 🍜 or tell you about famous people 🧑‍🎓. Try typing 'restaurant' or 'Nabeshima'."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
