from models import Model


class Topic(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('title', str, ''),
        ('user_id', str, ''),
        ('board_id', str, ''),
        ('views', int, 0)
    ]

    @classmethod
    def get(cls, id):
        m = cls.find(id)
        new = m.views + 1
        m.update(views=new)
        return m

    def replies(self):
        from .reply import Reply
        rs = Reply.find_all(topic_id=self._id)
        return rs

    def board(self):
        from .board import Board
        b = Board.find(self.board_id)
        return b

    def user(self):
        from .user import User
        u = User.find(id=self.user_id)
        return u


from pymongo import MongoClient
from bson import ObjectId
import time
client = MongoClient()
# 创建数据库 bbs
db = client["bbs"]
t = Topic.find('5c445b499252f94720da9933')
# print(type(t))
# for i in t:
t.update(views=10)
print(t._id)
# t.update(views=10)
t = Topic.find('5c445b499252f94720da9933')

print(t.__dict__)
# t.update(views=10)
