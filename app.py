import os
import json
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()

# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# 'hello' を含むメッセージをリッスンします
@app.message("hello")
def message_hello(message, say):
    """
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(f"Hey there <@{message['user']}>!")
    """
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "会議後アンケートの入力をお願いします！"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "チェックボックスから選択"
                },
                "accessory": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "mrkdwn",
                                "text": "*自分の意見が採用されました😁*"
                            },
                            "description": {
                                "type": "mrkdwn",
                                "text": "*達成度81~100%*"
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "mrkdwn",
                                "text": "*議論に参加できました🙂*"
                            },
                            "description": {
                                "type": "mrkdwn",
                                "text": "*達成度51~80%*"
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "mrkdwn",
                                "text": "*あまり発言できませんでした😔*"
                            },
                            "description": {
                                "type": "mrkdwn",
                                "text": "*達成度0~50%*"
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "checkboxes-action"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "回答ありがとうございます！"
                },
                "accessory": {
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

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> さん！回答ありがとうございます！")

# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))