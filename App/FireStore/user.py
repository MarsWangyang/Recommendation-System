
class User(object):

    # 直接用建構宣告一個user
    def __init__(self, user_id, user_name, status):
        self.user_id = user_id
        self.user_name = user_name
        self.status = status
    # 直接以class呼叫即可 將user dict 轉換成 user object

    @staticmethod
    def from_dict(source: dict):
        user = User(
            user_id=source.get("user_id"),
            user_name=source.get("user_name"),
            status=source.get("status"),
        )
        return user

    # 只能用user instance呼叫 將user object 轉成 dict
    def to_dict(self):
        user_dict = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "status": self.status,
        }
        return user_dict

    def __repr__(self):
        return (f'''User(
               user_id={self.user_id},
               user_name={self.user_name},
               status={self.status}
               )'''
                )
