# https://github.com/line/line-bot-sdk-python
from flask import Flask, request, abort, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage
import config

app = Flask(__name__)

url_github = "https://github.com/dr666m1/project_morning_ai_bot"
line_bot_api = LineBotApi(config.token)
handler = WebhookHandler(config.secret)

@app.route("/")
def github():
    return redirect(url_github)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body) # output log to stdout
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

def send_message(event, msg):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    send_message(event, "メッセージありがとうございます\n明日のアイちゃんの動画もお楽しみに！")

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    send_message(event, "スタンプありがとうございます\n明日のアイちゃんの動画もお楽しみに！")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
