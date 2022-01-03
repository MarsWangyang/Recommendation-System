import os
import json
import pandas as pd
from urllib.parse import parse_qs
from linebot.api import LineBotApi
from .Base import Base
from .Config import Config

config = Config()
# Create your own config.ini file, and put your info in config.ini
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_Handler = config.LINE_Handler
line_bot_api = config.line_bot_api
handler = config.handler


class PostBack(Base):
    def __init__(self, event):
        self._event = event
        self._postData = parse_qs(self._event.postback.data)

    def _decoratorAction(func):
        def wrapper(self, *args, **kargs):
            for key in self._postData.keys():
                funcName = func.__name__.lower().lstrip('_')
                if key.lower() == funcName:
                    func(self, *args, **kargs)
        return wrapper

    @_decoratorAction
    def _Action(self):
        '''
            This method is to switch Quick Reply Message. (Load json file in ./Material/Fixed/)
        '''
        key = 'action'
        root_path = './Material/Fixed'
        _postActionData = self._postData.get(key)[0] + '.json'
        adjoint_path = os.path.join(root_path, _postActionData)
        try:
            with open(adjoint_path, newline='') as file:
                reply_json = json.load(file)
                if (_postActionData == 'choose_pick_type.json'):
                    for i in range(2):
                        reply_json['quickReply']['items'][i]['action']['data'] = "data=" + \
                            self._postData['store_label_data'][0]

                if (_postActionData == 'display_score_panel.json'):
                    for i in range(5):
                        reply_json['quickReply']['items'][i]['action']['data'] = \
                            f"botid={self._postData['botid'][0]}&score={i+1}"
            line_bot_api.reply_message(
                self._event.reply_token,
                super().processJson(reply_json))
        except:
            error_path = './Material/Fixed/action_error.json'
            with open(error_path, newline='') as file:
                reply_json = json.load(file)
            line_bot_api.reply_message(
                self._event.reply_token,
                super().processJson(reply_json))

    def _Data(self):
        '''
            This method is for Bot carousel, and the format of this postback data should be data=list_XXX to generate bubble message.
        '''
        key = 'data'
        _postDataData: str = self._postData.get(key)[0]
        root_path = './Material/Template'
        bot_table_path = './Bot_Info.xlsx'
        bot_table = pd.read_excel(bot_table_path, engine='openpyxl')
        tags = bot_table['tags']
        BotInfoList = []
        if (_postDataData.startswith('list')):
            # pick random 3 bots to give a score
            label = _postDataData.split('list_')[1]
            # query bot in Bot_info.xlsx
            for i, eachBotTag in enumerate(tags):
                if str(eachBotTag).find(label) != -1:
                    BotInfoDict = {
                        "botName": bot_table.iloc[i].get('linebot_name'),
                        "intro": bot_table.iloc[i].get('Intro'),
                        "authorName": bot_table.iloc[i].get('student_name'),
                        "tags": bot_table.iloc[i].get('tags'),
                        "uri": bot_table.iloc[i].get('linebot_url'),
                        "postback": f"action=display_score_panel&botid={bot_table.iloc[i].get('email')}"
                    }
                    BotInfoList.append(BotInfoDict)
            print("=====BotInfoList=====", BotInfoList)

        line_bot_api.reply_message(
            self._event.reply_token,
            super().displayBotTemplate(BotInfoList))

    def getPostData(self):
        return self._postData

    def reply(self):
        '''
            According to postback data, find corresponding function to call.
        '''
        for pbKey in self._postData.keys():
            self.methodCall = '_' + pbKey.capitalize()
            try:
                self.method = getattr(self, self.methodCall)

            except:
                print(
                    f'Method {self.methodCall} is not Implemented/Error.')
            self.method()
