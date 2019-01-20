
from models import Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    """
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
    ]

    def from_form(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.user_image = 'default.png'

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.from_form(form)
        # pprint("u: " + str(u))
        user = User.find_one(username=u.username)
        # pprint("user: " + str(user))
        if user is not None and user.get("password", "") == u.salted_password(u.password):
            return user
        else:
            return None


# 测试能否根据用户名找到对应用户，结果可行
# def case(username=None):
#     from pymongo import MongoClient
#
#     client = MongoClient()
#
#     # 创建数据库 bbs
#     db = client["bbs"]
#
#     u = User.find_one(username=username)
#     return u
#
#
# u = case(username="qwe")
# print(u)