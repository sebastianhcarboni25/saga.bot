{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, abort\
from linebot import LineBotApi, WebhookHandler\
from linebot.exceptions import InvalidSignatureError\
from linebot.models import MessageEvent, TextMessage, TextSendMessage\
import os\
import random\
\
app = Flask(__name__)\
\
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])\
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])\
\
restaurants = [\
    "
\f1 \uc0\u55356 \u57180 
\f0  Ramen Kura \'96 Best pork ramen near Saga Station!",\
    "
\f1 \uc0\u55356 \u57187 
\f0  Sushi Tama \'96 Great sushi at a local price.",\
    "
\f1 \uc0\u55356 \u57179 
\f0  Saga Curry Honpo \'96 Tasty local beef curry.",\
    "
\f1 \uc0\u55356 \u57174 
\f0  Yakiniku Ranmaru \'96 Delicious grilled meat!",\
    "
\f1 \uc0\u9749 
\f0  Caf\'e9 Morinokaze \'96 Cute cafe with relaxing vibes."\
]\
\
historical_figures = \{\
    "nabeshima": "
\f1 \uc0\u55357 \u56632 
\f0  Nabeshima Naomasa: A powerful daimyo who modernized Saga during the Bakumatsu period.",\
    "naomasa": "
\f1 \uc0\u55357 \u56632 
\f0  Nabeshima Naomasa modernized Saga\'92s army and supported the Meiji Restoration.",\
    "history": "
\f1 \uc0\u55357 \u56540 
\f0  Saga was home to leaders who helped modernize Japan, including Nabeshima Naomasa and others."\
\}\
\
@app.route("/")\
def home():\
    return "Saga bot is running!"\
\
@app.route("/callback", methods=['POST'])\
def callback():\
    signature = request.headers['X-Line-Signature']\
    body = request.get_data(as_text=True)\
\
    try:\
        handler.handle(body, signature)\
    except InvalidSignatureError:\
        abort(400)\
\
    return 'OK'\
\
@handler.add(MessageEvent, message=TextMessage)\
def handle_message(event):\
    user_msg = event.message.text.lower()\
    if any(word in user_msg for word in ["eat", "restaurant", "food", "hungry"]):\
        reply = random.choice(restaurants)\
    elif any(name in user_msg for name in historical_figures):\
        for name in historical_figures:\
            if name in user_msg:\
                reply = historical_figures[name]\
                break\
    else:\
        reply = "Hi! I can recommend restaurants in Saga 
\f1 \uc0\u55356 \u57180 
\f0  or tell you about famous people 
\f1 \uc0\u55358 \u56785 \u8205 \u55356 \u57235 
\f0 . Try typing 'restaurant' or 'Nabeshima'."\
\
    line_bot_api.reply_message(\
        event.reply_token,\
        TextSendMessage(text=reply)\
    )\
\
if __name__ == "__main__":\
    app.run(host="0.0.0.0", port=10000)\
}