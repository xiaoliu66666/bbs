from models import Model


class Reply(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('topic_id', str, ''),
        ('receiver_id', str, ''),
        ('user_id', str, '')
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

