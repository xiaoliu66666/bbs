from models import Model
from .user import User


class Mail(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('read', bool, False),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
    ]

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()

    def sender(self):
        sender = User.find(self.sender_id)
        return sender.username

    def receiver(self):
        receiver = User.find(self.receiver_id)
        return receiver.username
