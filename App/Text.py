# -*- coding: UTF-8 -*-
from .Base import Base
from .Config import Config
import jieba
import jieba.analyse
import pandas as pd
import random
import json

config = Config()
handler = config.handler
line_bot_api = config.line_bot_api


class Text(Base):
    def __init__(self, event, status):
        self._event = event
        self._status = status
        self._text = self._event.message.text

    def _extractKeywords(self):
        self._tags = jieba.analyse.extract_tags(self._text, topK=5)
        for index, tag in enumerate(self._tags):
            if tag.isdigit():
                self._tags[index] = int(tag)

        for i in self._tags:
            print(type(i))
        return self._tags

    def _searchTable(self, tags: list):
        '''
            Search Keywords that user text to Bot, and retrieve from Bot_Info.xlsx
        '''
        bot_table_path = './Bot_Info.xlsx'
        bot_table = pd.read_excel(bot_table_path, engine='openpyxl')
        bot_label = bot_table['label']
        # print(f'tag: {tags}')
        # print(f'===bot_label==== \n{bot_label}')
        BotInfoList = []
        for i, eachBotLabel in enumerate(bot_label):
            # print(f'======eachBotLabel======\n{eachBotLabel}')
            for keyword in tags:
                print(f'keyword: {keyword}')
                if str(eachBotLabel).find(keyword) != -1:
                    BotInfoDict = {
                        "botName": bot_table.iloc[i].get('linebot_name'),
                        "intro": bot_table.iloc[i].get('Intro'),
                        "authorName": bot_table.iloc[i].get('student_name'),
                        "tags": bot_table.iloc[i].get('tags'),
                        "uri": bot_table.iloc[i].get('linebot_url'),
                        "postback": f"action=display_score_panel&botid={bot_table.iloc[i].get('email')}"
                    }
                    BotInfoList.append(BotInfoDict)

        # random.seed()
        # random.shuffle(self._result)
        # print('self._result:', len(self._result))
        # if len(self._result) == 0:
        #     self._result = QueryRedis().query(key='NoResult', dbNum=3)
        # elif len(self._result) > 12:
        #     self._result = self._result[0:12]
        # print(BotInfoList)
        return BotInfoList

    def reply(self):
        if self._status == 'text_open':
            if self._text != '????????????????????????????????????????????????????????????':
                self._keywords = self._extractKeywords()
                BotInfoList: list = self._searchTable(self._keywords)
                if len(BotInfoList) > 0:
                    reply_arr = self.displayBotTemplate(BotInfoList)
                else:
                    no_data_path = './Material/Fixed/no_data_path.json'
                    with open(no_data_path, newline='') as file:
                        reply_json = json.load(file)
                    reply_arr = self.processJson(reply_json)
                line_bot_api.reply_message(
                    self._event.reply_token,
                    reply_arr)
        else:
            pass
