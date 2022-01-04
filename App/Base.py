import abc
import linebot.models as md
import json
import copy


class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reply(self):
        return NotImplementedError

    @classmethod
    def processJson(cls, jsonFile):
        '''
            Address complete .json and send to line-bot
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
        # print(cls.returnArr)
        return cls.returnArr

    @classmethod
    def displayBotTemplate(cls, botInfo: list) -> list:
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
            cls._copyTemplate = copy.deepcopy(cls.bubble_template)
            # print(cls._copyTemplate)
            botDisplayList.append(cls._copyTemplate)

        flexDisplayList = []
        last_message = len(botDisplayList) % 12
        if last_message != 0:
            message_number = len(botDisplayList) // 12 + 1
        else:
            message_number = len(botDisplayList) // 12
        for i in range(message_number):
            if i == message_number:
                botDisplayListTemp = botDisplayList[12*i:12*i+last_message]
            else:
                botDisplayListTemp = botDisplayList[12*i:12*(i+1)]
            cls.carousel_template['contents'] = botDisplayListTemp
            cls.flex_template['contents'] = cls.carousel_template
            cls._copyFlexTemplate = copy.deepcopy(cls.flex_template)

            flexDisplayList.append(cls.processJson(cls._copyFlexTemplate)[0])

        return flexDisplayList
