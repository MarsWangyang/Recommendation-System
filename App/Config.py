import configparser
from linebot import (LineBotApi, WebhookHandler)
config = configparser.ConfigParser()
config.read('config.ini')


class Config():
    def __init__(self):
        '''
            Create your own config.ini file, and put your info in config.ini
        '''
        self.LINE_CHANNEL_ACCESS_TOKEN = config["linebot"]["line_bot_api"]
        self.LINE_Handler = config["linebot"]["handler"]
        self.line_bot_api = LineBotApi(self.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(self.LINE_Handler)
