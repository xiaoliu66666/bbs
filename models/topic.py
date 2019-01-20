from models import Model


class Topic(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0)
    ]

    @classmethod
    def get(cls, id):
        m = cls.find(id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        rs = Reply.find_all(topic_id=self.id)
        return rs

    def board(self):
        from .board import Board
        b = Board.find(self.board_id)
        return b

    def user(self):
        from .user import User
        u = User.find(id=self.user_id)
        return u

