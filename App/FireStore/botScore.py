
class BotScore(object):

    # 直接用建構宣告一個botScore
    def __init__(self, user_id, bot_id, score):
        self.user_id = user_id
        self.bot_id = bot_id
        self.score = score
    # 直接以class呼叫即可 將botScore dict 轉換成 botScore object

    @staticmethod
    def from_dict(source: dict):
        botScore = BotScore(
            user_id=source.get("user_id"),
            bot_id=source.get("bot_id"),
            score=source.get("score"),
        )
        return botScore

    # 只能用botScore instance呼叫 將botScore object 轉成 dict
    def to_dict(self):
        botScore_dict = {
            "user_id": self.user_id,
            "bot_id": self.bot_id,
            "score": self.score,
        }
        return botScore_dict

    def __repr__(self):
        return (f'''BotScore(
               user_id={self.user_id},
               bot_id={self.bot_id},
               score={self.score}
               )'''
                )
