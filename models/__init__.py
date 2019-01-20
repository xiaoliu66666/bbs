import time
from bson import ObjectId
from pymongo import MongoClient

from utils import log

client = MongoClient()

# 创建数据库 bbs
db = client["bbs"]


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
        m.id = ""
        return m

    def save(self):
        name = self.__class__.__name__
        insert = db[name].insert_one(self.__dict__)
        self.id = str(insert.inserted_id)
        db[name].update_one({"id": ""}, {"$set": {"id": self.id}})
        # log("self.id", self.id)

    @classmethod
    def delete(cls, id=None):
        """
        根据传入的 id， 实现软删除
        """
        name = cls.__name__
        query = {
            '_id': ObjectId(id),
        }
        update = {
            'deleted': True
        }
        db[name].update_one(query, {"$set": update})

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def _find(cls, *args, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(kwargs, deleted=False)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def all(cls):
        """
        返回所有的数据
        """
        return cls._find()

    def update(self, *args, **kwargs):
        """
        根据filter查到数据并更新
        :param filter:
        :param update: 是一个字典
        :return:
        """
        _filter = {"_id": self._id}
        name = self.__class__.__name__
        # kwargs.update({"updated_time": int(time.time())})
        db[name].update_one(_filter, {"$set": kwargs})

    @classmethod
    def find(cls, id):
        return cls.find_one(_id=ObjectId(id))

