from flask import Flask, request, abort
import os
import requests

from linebot.v3.messaging import Configuration, MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LocationMessageContent
from linebot.v3.messaging.models import TextMessage

app = Flask(__name__)

config = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
line_bot_api = MessagingApi(config)
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def get_nearby_restaurants(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,
        "type": "restaurant",
        "key": GOOGLE_API_KEY,
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return "Error fetching restaurants."

    results = response.json().get("results", [])
    if not results:
        return "No restaurants found nearby."

    message = ""
    for place in results[:5]:
        name = place.get("name", "Unknown")
        rating = place.get("rating", "N/A")
        address = place.get("vicinity", "No address")
        message += f"🍽 {name}\n⭐ {rating} | 📍 {address}\n\n"

    return message.strip()

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
        if "restaurant" in message.text.lower():
            reply = "📍 Please send your location to get nearby restaurant recommendations!"
        else:
            reply = "Hi! Send the word 'restaurant' and then share your location 📍 to get suggestions!"
        line_bot_api.reply_message(
            event.reply_token,
            [TextMessage(text=reply)]
        )

    elif isinstance(message, LocationMessageContent):
        lat = message.latitude
        lng = message.longitude
        results = get_nearby_restaurants(lat, lng)
        line_bot_api.reply_message(
            event.reply_token,
            [TextMessage(text=results)]
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
