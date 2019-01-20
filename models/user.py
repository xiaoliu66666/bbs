from werkzeug.security import generate_password_hash, check_password_hash

from models import Model
from utils import log


class User(Model):
    """
    User 是一个保存用户数据的 model
    """
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
    ]

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        raw_pwd = form.get('password', '')
        pwd = generate_password_hash(raw_pwd)
        if len(name) > 2 and User.find_one(username=name) is None:
            u = User.new(form, password=pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User.new(form)
        # log("form: ", form)
        # user 是根据用户名查询到的用户，u 是根据表单生成的用户
        user = User.find_one(username=u.username)
        if user is not None and check_password_hash(user.password, u.password):
            # log("u: ", user)
            return user
        else:
            return None


# 测试User能否调用Model的各种方法，结果可行
# 所以问题应该出在session部分，发现session里面并没有保存任何东西
# def case(id):
#     from pymongo import MongoClient
#     from bson import ObjectId
#
#     client = MongoClient()
#     # 创建数据库 bbs
#     db = client["bbs"]
#
#     User.delete(id)
#
#
# case("5c429e5b9252f92740742e11")






