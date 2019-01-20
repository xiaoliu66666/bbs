import time
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient()

# 创建数据库 bbs
db = client["bbs"]


# def next_id(name):
#     """
#     实现 id 自增
#     :param name: 当前的类名
#     :return: 新的id
#     """
#     query = {
#         'name': name,
#     }
#     update = {
#         '$inc': {
#             'seq': 1
#         }
#     }
#     kwargs = {
#         'query': query,
#         'update': update,
#         'upsert': True,
#         'new': True,
#     }
#     # 存储数据的 id
#     new_id = db["data_id"].find_and_modify(**kwargs).get('seq')
#     return new_id


class Model:
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        new 是给外部使用的函数
        """
        name = cls.__name__
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}

        # form不为空
        for f in fields:
            # print(f)
            k, t, v = f
            # print(t)
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)

        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.save()
        return m

    def save(self):
        name = self.__class__.__name__
        db[name].insert_one(self.__dict__)

    @classmethod
    def delete(cls, id=None):
        """
        根据传入的 id， 实现软删除

        """
        name = cls.__name__
        query = {
            'id': id,
        }
        update = {
            'deleted': True
        }
        db[name].update_one(query, {"$set": update})

    @classmethod
    def _find(cls, *args, **kwargs):
        name = cls.__name__
        # pprint("name: " + name)
        # 过滤掉所有 deleted 字段为 True 的数据
        kwargs["deleted"] = False
        # result是一个 Cursor 对象
        result = db[name].find(kwargs)
        # pprint(result)
        ms = list(result)
        # pprint("查询结果：" + str(ms))
        # 返回一个列表
        return ms

    @classmethod
    def find_one(cls, **kwargs):
        name = cls.__name__
        result = db[name].find_one(kwargs)
        return result

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def all(cls):
        """
        返回所有的数据
        """
        return cls._find()

    @classmethod
    def update(cls, filter, update):
        """
        根据filter查到数据并更新
        :param filter:
        :param update: 要带上 $ 操作符
        :return:
        """
        name = cls.__name__
        db[name].update_one(filter, update)


    @classmethod
    def find(cls, id):
        return cls.find_one(_id=ObjectId(id))

    @property
    def id(self):
        return self._id