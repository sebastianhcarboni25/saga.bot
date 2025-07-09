from flask import Flask, request, abort
import os
import requests

# LINE SDK v3
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationMessage
)

# Setup Flask app
app = Flask(__name__)

# LINE API configuration
config = Configuration(access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
line_bot_api = MessagingApi(configuration=config)
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# Get restaurants nearby using Google Places API
def get_nearby_restaurants(lat, lng):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,
        "type": "restaurant",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return "No restaurants found nearby."

    message = ""
    for place in data["results"][:5]:  # Top 5 restaurants
        name = place.get("name", "Unknown")
        rating = place.get("rating", "N/A")
        address = place.get("vicinity", "No address")
        message += f"🍽 {name}\n⭐ {rating} | 📍 {address}\n\n"

    return message.strip()

# LINE webhook endpoint
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# Message handling
@handler.add(MessageEvent)
def handle_message(event):
    msg_type = event.message.type

    if msg_type == "text":
        user_message = event.message.text.lower()
        if "restaurant" in user_message:
            reply = "📍 Please send your location to get nearby restaurant recommendations!"
        else:
            reply = "Hi! Send the word 'restaurant' and then share your location 📍 to get suggestions!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    elif msg_type == "location":
        lat = event.message.latitude
        lng = event.message.longitude
        restaurant_list = get_nearby_restaurants(lat, lng)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=restaurant_list)
        )

# Render-friendly port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # default for local
    app.run(host="0.0.0.0", port=port)
