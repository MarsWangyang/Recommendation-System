from flask import Flask, request, abort

import pandas as pd
import os
import json
import random
import hashlib
import string
import openpyxl
from urllib import parse

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    PostbackAction, ImagemapSendMessage, ImageSendMessage, StickerSendMessage, AudioSendMessage, LocationSendMessage,
    FlexSendMessage, VideoSendMessage,
)
from linebot.models.events import JoinEvent, PostbackEvent, MemberJoinedEvent, MemberLeftEvent, FollowEvent
import logging
import configparser

app = Flask(__name__)

config = configparser.ConfigParser().read('config.ini')
# Create your own config.ini file, and put your info in config.ini
LINE_CHANNEL_ACCESS_TOKEN = config["linebot"]["line_bot_api"]
LINE_Handler = config["linebot"]["handler"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_Handler)


def getMessageObject(jsonObject):
    message_type = jsonObject.get('type')
    if message_type == 'text':
        return TextSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'imagemap':
        return ImagemapSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'template':
        return TemplateSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'image':
        return ImageSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'sticker':
        return StickerSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'audio':
        return AudioSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'location':
        return LocationSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'flex':
        return FlexSendMessage.new_from_json_dict(jsonObject)
    elif message_type == 'video':
        return VideoSendMessage.new_from_json_dict(jsonObject)


def get_reply_messages(data):
    querystring_dict = dict(parse.parse_qsl(data))
    section = querystring_dict['section']
    action = querystring_dict['action']
    try:
        data = querystring_dict['data']
    except:
        data = "None"
    reply_table = pd.read_excel(
        'reply_messages_police.xlsx', engine='openpyxl')
    section_row = reply_table[reply_table.section == section]
    action_row = section_row[section_row.action == action]
    print("action_row: ", action_row)
    if data == "None":
        data_row = action_row
    else:
        data_row = action_row[action_row.data == data]
    print("Row: ", data_row)
    return_array = []
    for i in range(5):
        if not pd.isna(data_row['message' + str(i + 1)].values[0]):
            print("massage json string: ",
                  data_row['message' + str(i + 1)].values[0])
            print(type(data_row['message' + str(i + 1)].values[0]))
            jsonObject = json.loads(
                data_row['message' + str(i + 1)].values[0])  # string to dict
            messageObject = getMessageObject(jsonObject)
            return_array.append(messageObject)

    print("generate reply messages:", return_array)
    return return_array


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # print("post")
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msgtxt = event.message.text

    if msgtxt == "test":
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="testing"))
    if msgtxt == "#replay":
        line_bot_api.reply_message(
            event.reply_token, get_reply_messages("section=jbwstudio&action=initial"))


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, get_reply_messages("section=jbwstudio&action=initial"))


@handler.add(PostbackEvent)
def handle_postback(event):

    data = event.postback.data
    print("received data:", data)

    line_bot_api.reply_message(event.reply_token, get_reply_messages(data))


if __name__ == "__main__":
    app.debug = True
    loghandler = logging.FileHandler('flask.log')
    app.logger.addHandler(loghandler)
    app.run(port=5000)
