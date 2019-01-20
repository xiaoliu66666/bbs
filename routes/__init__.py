from flask import session

from models.user import User
from utils import log


def current_user():
    username = session.get("username", "")
    log("username: ", username)
    if username != "":
        u = User.find_one(username=username)
        return u
    else:
        return None

