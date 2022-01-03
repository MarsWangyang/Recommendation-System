
from .user import User
from google.cloud import firestore
# from google.auth.credentials import AnonymousCredentials


class UserDAO:
    # 上線後要改
    # db = firestore.Client(project=os.environ.get('GCP_PROJECT'))
    # users_ref=db.collection(u'users')

    #db = firestore.Client(project='ccs', credentials=AnonymousCredentials())

    db = firestore.Client()
    users_ref = db.collection(u'users')

    # 新增資料時，若有重複資料，則採更新  傳入一個User object
    @classmethod
    def save_user(cls, user: User) -> None:
        user_ref = cls.users_ref.document(user.user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            print(f"update {user.user_id} info")
            user_ref.set(document_data=user.to_dict(), merge=True)
        else:
            print(f"create new doc for{user.user_id}")
            cls.users_ref.add(document_data=user.to_dict(),
                              document_id=user.user_id)

        return user.to_dict()

    # 取用資料，開放以user_id的方式尋找 回傳User object
    @classmethod
    def get_user(cls, user_id: str) -> User:
        user_ref = cls.users_ref.document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user = User.from_dict(user_doc.to_dict())
        else:
            pass
        return user
