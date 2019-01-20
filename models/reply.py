from models import Model


class Reply(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('receiver_id', int, -1),
        ('user_id', int, -1)
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

