import json
import os
import pandas as pd


class Template():
    def __init__(self):
        bubble_template_path = './Material/Template/template_bubble.json'
        with open(bubble_template_path) as file:
            self.bubble_template = json.loads(file)

    def _queryBotInfo(self):
        botInfoTable = pd.read_excel(
            'reply_messages_police.xlsx', engine='openpyxl')

    def addressDisplay(self):
        self.carouselContent = []
