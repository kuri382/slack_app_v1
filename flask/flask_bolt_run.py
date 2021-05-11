import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

load_dotenv() #環境変数読み込み

logging.basicConfig(level=logging.DEBUG)
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.message("hello")
def message_hello(message,say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "会議後アンケートの入力をお願いします！"
                },
                "accessory":{
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "回答を送信する"
                    },
                    "action_id": "button_click"
                }
            }
        ]
    )

@app.event("app_mention")
def event_test(body, say, logger):
    #logger.info(body)
    say("What's up?")


@app.event("message")
def handle_message():
    pass

@app.action("meeting_finished")
def send_interview(body,ack,say):
    ack()
    say("What's up?")
    


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


# FLASK_APP=app.py FLASK_ENV=development flask run -p 5000
if __name__ == "__main__":
    flask_app.run(debug=True, port=5000)