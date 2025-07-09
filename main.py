from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import random

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

# General restaurant pool
restaurants = [
    "🍜 Fukunoie Ramen, Honjo - Saga's students favourite Ramen",
    "🍣 Hamazushi – Great sushi at a local price.",
    "🍛 Yellow Spice Curry Tojinmachi – Tasty local curry.",
    "🍖 Ju ju Karubi – Delicious grilled meat!",
    "☕ Nowhere coffee – Modern cafe with relaxing vibes."
]

# Named best-of spots
best_places = {
    "best curry": "🍛 Try Stool coffee – top-rated for beef curry!",
    "best coffee": "☕ Check out 03 Coffee – perfect for relaxing with coffee.",
    "best sushi": "🍣 Visit Kura sushi for authentic and fresh sushi!",
    "best ramen": "🍜 RaRaRamen is a local favourite for tonkotsu ramen!",
    "best yakiniku": "🔥 Yakiniku King is the go-to place for grilled meat in Saga."
}

# Historical figures
historical_figures = {
    "nabeshima": "🔸 Nabeshima Naomasa: A powerful daimyo who modernized Saga during the Bakumatsu period.",
    "naomasa": "🔸 Nabeshima Naomasa modernized Saga’s army and supported the Meiji Restoration.",
    "history": "📜 Saga was home to leaders who helped modernize Japan, including Nabeshima Naomasa and others.",
}

# 7 Wise Men of Saga
seven_wise_men = {
    "soejima": "🧠 Soejima Taneomi: A diplomat and politician who helped shape Meiji foreign policy.",
    "eto": "⚖️ Eto Shimpei: A legal reformer and advocate for parliamentary government.",
    "okuma": "🏛️ Okuma Shigenobu: Founded Waseda University and served as Prime Minister.",
    "oe": "📚 Oe Taku: Contributed to education and modernization in Saga.",
    "shimada": "💡 Shimada Saburo: Worked on infrastructure and helped develop Saga’s industry.",
    "nakamura": "🔬 Nakamura Keiu: Prominent in medical reforms and modernization.",
    "shigenobu": "🏛️ Okuma Shigenobu (again): Famous for liberal politics and education. His house is located in the East of Saga, Please visit his museum!"
}

# Saga Castle Info
saga_castle_info = "🏯 Saga Castle: Originally built in 1602, it played a key role in the Edo period. The reconstructed main keep is now a museum showcasing Saga’s history."

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

    # Priority: Exact keyword matches for "best ..." phrases
    for keyword in best_places:
        if keyword in user_msg:
            reply = best_places[keyword]
            break
    else:
        # General restaurant-related message
        if any(word in user_msg for word in ["eat", "restaurant", "food", "hungry"]):
            reply = random.choice(restaurants)
        # Historical figure lookup
        elif any(name in user_msg for name in historical_figures):
            for name in historical_figures:
                if name in user_msg:
                    reply = historical_figures[name]
                    break
        # 7 Wise Men lookup
        e
