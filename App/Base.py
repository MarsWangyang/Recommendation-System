import abc
import linebot.models as md
import json


class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reply(self):
        return NotImplementedError

    @classmethod
    def processJson(cls, jsonFile: dict):
        '''
            Address json file that is load in by Redis
        '''
        cls._msgType = jsonFile.get('type')
        cls.returnArr = []

        if cls._msgType == 'text':
            cls.returnArr.append(
                md.TextSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'imagemap':
            cls.returnArr.append(
                md.ImagemapSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'template':
            cls.returnArr.append(
                md.TemplateSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'image':
            cls.returnArr.append(
                md.ImageSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'sticker':
            cls.returnArr.append(
                md.StickerSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'audio':
            cls.returnArr.append(
                md.AudioSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'location':
            cls.returnArr.append(
                md.LocationSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'flex':
            cls.returnArr.append(
                md.FlexSendMessage.new_from_json_dict(jsonFile))
        elif cls._msgType == 'video':
            cls.returnArr.append(
                md.VideoSendMessage.new_from_json_dict(jsonFile))
        print(cls.returnArr)
        return cls.returnArr

    @classmethod
    def displayBotTemplate(cls, botInfo: list) -> dict:
        bubble_template_path = './Material/Template/template_bubble.json'
        carousel_template_path = './Material/Template/template_carousel.json'
        flex_template_path = './Material/Template/template_flex_message.json'
        with open(bubble_template_path) as file:
            cls.bubble_template = json.load(file)
        with open(carousel_template_path) as file:
            cls.carousel_template = json.load(file)
        with open(flex_template_path) as file:
            cls.flex_template = json.load(file)

        botDisplayList = []

        for eachBotInfo in botInfo:
            # Bot Name/Title
            cls.bubble_template['body']['contents'][0]['text'] = eachBotInfo['botName']
            # Intro
            cls.bubble_template['body']['contents'][1]['contents'][0]['contents'][2]['text'] = eachBotInfo['intro']
            # Author name
            cls.bubble_template['body']['contents'][1]['contents'][1]['contents'][2]['text'] = eachBotInfo['authorName']
            # Tags
            cls.bubble_template['body']['contents'][1]['contents'][2]['contents'][2]['text'] = eachBotInfo['tags']
            # Link
            cls.bubble_template['footer']['contents'][0]['action']['uri'] = eachBotInfo['uri']
            # PostBack
            cls.bubble_template['footer']['contents'][1]['action']['data'] = eachBotInfo['postback']
            # Carousel Template
            botDisplayList.append(cls.bubble_template)

        cls.carousel_template['contents'] = botDisplayList
        cls.flex_template['contents'] = cls.carousel_template
        print("======cls.carousel_template======", cls.carousel_template)
        return cls.processJson(cls.flex_template)
