from urllib import parse
import openpyxl
import string
import hashlib
import random
import json
import os
import pandas as pd
from App import app
from flask import request, abort
from .Base import Base
from .Postback import PostBack
from .Config import Config
from .FireStore.user import User
from .FireStore.userDAO import UserDAO
import configparser
import logging
from linebot.models.events import JoinEvent, PostbackEvent, MemberJoinedEvent, MemberLeftEvent, FollowEvent
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
from linebot.exceptions import (InvalidSignatureError)
from linebot import (LineBotApi, WebhookHandler)

from flask import Flask

# config = configparser.ConfigParser()
# config.read('config.ini')
config = Config()
# Create your own config.ini file, and put your info in config.ini
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_Handler = config.LINE_Handler
line_bot_api = config.line_bot_api
handler = config.handler


# def get_reply_messages(data):
#     querystring_dict = dict(parse.parse_qsl(data))
#     section = querystring_dict['section']
#     action = querystring_dict['action']
#     try:
#         data = querystring_dict['data']
#     except:
#         data = "None"

#     reply_table = pd.read_excel(
#         'reply_messages_police.xlsx', engine='openpyxl')
#     section_row = reply_table[reply_table.section == section]
#     action_row = section_row[section_row.action == action]
#     print("action_row: ", action_row)
#     if data == "None":
#         data_row = action_row
#     else:
#         data_row = action_row[action_row.data == data]
#     print("Row: ", data_row)
#     return_array = []
#     for i in range(5):
#         if not pd.isna(data_row['message' + str(i + 1)].values[0]):
#             print("massage json string: ",
#                   data_row['message' + str(i + 1)].values[0])
#             print(type(data_row['message' + str(i + 1)].values[0]))
#             jsonObject = json.loads(
#                 data_row['message' + str(i + 1)].values[0])  # string to dict
#             # messageObject = getMessageObject(jsonObject)
#             # return_array.append(messageObject)

#     print("generate reply messages:", return_array)
#     return return_array


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

    # if msgtxt == "test":
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text="testing"))
    # if msgtxt == "#replay":
    #     line_bot_api.reply_message(
    #         event.reply_token, get_reply_messages("action=initial"))


@handler.add(FollowEvent)
def handle_follow(event):
    path = './Material/Fixed/follow.json'
    with open(path, newline='') as file:
        follow_json = json.load(file)
    reply_follow = Base.processJson(follow_json)
    line_bot_api.reply_message(event.reply_token, reply_follow)

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    print(profile.display_name)
    print(profile.user_id)
    user = User(user_id=user_id, user_name=profile.display_name,
                status=profile.status_message)
    UserDAO.save_user(user)


@handler.add(PostbackEvent)
def handle_postback(event):
    postback = PostBack(event)
    postback.reply()
    # data = event.postback.data
    # print("received data:", data)

    # line_bot_api.reply_message(event.reply_token, get_reply_messages(data))
