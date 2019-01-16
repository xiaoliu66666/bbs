import time
from models import Model
from .user import User


class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.title = form.get('title', '')

        self.ct = int(time.time())
        self.read = False

        self.sender_id = -1
        self.receiver_id = int(form.get("to", -1))

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
