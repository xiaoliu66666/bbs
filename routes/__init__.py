from flask import session

from models.user import User
from utils import log


def current_user():
    uid = session.get('user_id', '')
    u = User.find(uid)
    return u


