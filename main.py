from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationMessage
)
import os
import requests

app = Flask(__name__)

# Use your environment variables
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# Get nearby restaurants using Google Places API
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
    for place in data["results"][:5]:  # Limit to 5 results
        name = place.get("name", "Unknown")
        rating = place.get("rating", "N/A")
        address = place.get("vicinity", "Address not found")
        message += f"🍽 {name}\n⭐ {rating} | 📍 {address}\n\n"

    return message.strip()

# Webhook route
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# Text and location message handler
@handler.add(MessageEvent)
def handle_message(event):
    msg_type = event.message.type

    if msg_type == "text":
        user_message = event.message.text.lower()
        if "restaurant" in user_message:
            reply = "📍 Please send your location so I can find restaurants nearby!"
        else:
            reply = "Hi! Type 'restaurant' and send your 📍 location to get recommendations!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    elif msg_type == "location":
        lat = event.message.latitude
        lng = event.message.longitude
        restaurant_list = get_nearby_restaurants(lat, lng)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=restaurant_list))

# Run app (for local dev only)
if __name__ == "__main__":
    app.run(debug=True)
