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
from .Text import Text
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
import jieba


config = Config()
# Create your own config.ini file, and put your info in config.ini
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_Handler = config.LINE_Handler
line_bot_api = config.line_bot_api
handler = config.handler

# textStatus is for text searching function
textStatus = 'text_close'

jieba.load_userdict('./App/text.txt')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

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
    global textStatus
    try:
        textStatus = postback.getStatus()
    except:
        pass


@handler.add(MessageEvent, message=TextMessage)
def textmessage(event):
    global textStatus
    textmessage = Text(event, textStatus)
    textmessage.reply()
