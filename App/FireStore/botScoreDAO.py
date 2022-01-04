
from .botScore import BotScore
from google.cloud import firestore
# from google.auth.credentials import AnonymousCredentials


class BotScoreDAO:

    db = firestore.Client()
    botScores_ref = db.collection(u'botScores')

    # 新增資料時，若有重複資料，則採更新  傳入一個BotScore object
    @classmethod
    def save_botScore(cls, botScore: BotScore) -> None:

        cls.botScores_ref.add(document_data=botScore.to_dict())

        return botScore.to_dict()

    # 取用資料，開放以botScore_id的方式尋找 回傳BotScore object
    # @classmethod
    # def get_botScore(cls, botScore_id: str) -> BotScore:
    #     botScore_ref = cls.botScores_ref.document(botScore_id)
    #     botScore_doc = botScore_ref.get()
    #     if botScore_doc.exists:
    #         botScore = BotScore.from_dict(botScore_doc.to_dict())
    #     else:
    #         pass
    #     return botScore
