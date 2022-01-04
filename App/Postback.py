import os
import json
import pandas as pd
from urllib.parse import parse_qs
from linebot.api import LineBotApi
from .Base import Base
from .Config import Config
from .FireStore.botScore import BotScore
from .FireStore.botScoreDAO import BotScoreDAO

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
        _postActionData: str = self._postData.get(key)[0]
        # try:
        adjoint_path = os.path.join(
            root_path, _postActionData + '.json')
        with open(adjoint_path, newline='') as file:
            reply_json = json.load(file)
        if _postActionData == 'choose_pick_type':
            reply_json['quickReply']['items'][0]['action']['data'] = "choose_type=list_all" + \
                "&" + "data=" + self._postData['store_label_data'][0]

            reply_json['quickReply']['items'][1]['action']['data'] = "choose_type=list_recommend" + \
                "&" + "data=" + self._postData['store_label_data'][0]

        if _postActionData == 'display_score_panel':
            for i in range(5):
                reply_json['quickReply']['items'][i]['action']['data'] = \
                    f"botid={self._postData['botid'][0]}&score={i+1}"

        line_bot_api.reply_message(
            self._event.reply_token,
            self.processJson(reply_json))

    # @_decoratorAction
    # def _Data(self):
    #     '''
    #         the format of this postback data should be data=list_XXX to generate bubble message.
    #     '''
    #     pass

    @_decoratorAction
    def _Choose_type(self):
        '''
            This method is for Bot carousel.
        '''
        _postDataData: str = self._postData.get('data')[0]
        _postChooseTypeData: str = self._postData.get('choose_type')[0]
        root_path = './Material/Template'
        bot_table_path = 'Bot_Info.xlsx'
        bot_table = pd.read_excel(bot_table_path, engine='openpyxl')
        tags = bot_table['tag_label']
        print('==========wwww===========\n', tags)
        BotInfoList = []
        if (_postDataData.startswith('list')):
            # pick random 3 bots to give a score
            label = _postDataData.split('list_')[1]
            print("=====label======\n", label)
            if _postChooseTypeData == 'list_all':
                # query bot in Bot_info.xlsx
                for i, eachBotTag in enumerate(tags):
                    eachTag = eval(eachBotTag)
                    print(f'=====Tag======\n{eachTag}')
                    for tag in eachTag:

                        if str(tag).find(label) != -1:
                            BotInfoDict = {
                                "botName": bot_table.iloc[i].get('linebot_name'),
                                "intro": bot_table.iloc[i].get('Intro'),
                                "authorName": bot_table.iloc[i].get('student_name'),
                                "tags": bot_table.iloc[i].get('tags'),
                                "uri": bot_table.iloc[i].get('linebot_url'),
                                "postback": f"action=display_score_panel&botid={bot_table.iloc[i].get('email')}"
                            }
                            BotInfoList.append(BotInfoDict)
                print(len(BotInfoList))
                if len(BotInfoList) > 0:
                    reply_arr = self.displayBotTemplate(BotInfoList)
                else:
                    no_data_path = './Material/Fixed/no_data_path.json'
                    with open(no_data_path, newline='') as file:
                        reply_json = json.load(file)
                    reply_arr = self.processJson(reply_json)
                print("=======reply_arr====\n", reply_arr)
                line_bot_api.reply_message(
                    self._event.reply_token,
                    reply_arr)
            elif _postChooseTypeData == 'list_recommend':
                pass

    @_decoratorAction
    def _Menu(self):
        '''
            This method is for switching Rich Menu.
        '''
        key = 'menu'
        _postMenuData = self._postData.get(key)[0]
        root_path = './Material/Fixed/rich_menu'
        rich_menu_id_path = os.path.join(
            root_path, _postMenuData) + '/rich_menu_id.txt'
        with open(rich_menu_id_path, 'r', encoding='utf8') as file:
            rich_menu_id = file.readline()
        line_bot_api.link_rich_menu_to_user(
            self._event.source.user_id, rich_menu_id)

    @_decoratorAction
    def _Status(self):
        self._key = 'status'
        try:
            self._textFlag = self._postData.get(self._key)[0]
            return self._textFlag
        except:
            self._textFlag = 'text_close'
            return self._textFlag

    @_decoratorAction
    def _Score(self):
        '''
            @Author: Isaac Huang
            This method is for FireStore API. Get Botid and score here.
        '''

        _postBotIDData = self._postData.get('botid')[0]
        _postScoreData = self._postData.get('score')[0]
        _whoScoreUserId = self._event.source.user_id

        botScore = BotScore(user_id=_whoScoreUserId,
                            bot_id=_postBotIDData, score=_postScoreData)
        BotScoreDAO.save_user(botScore)

    def getStatus(self):
        return self._textFlag

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
                exit = 0
            except:
                exit = 1
                print(
                    f'Method {self.methodCall} is not Implemented/Error.')
            if exit == 0:
                self.method()
