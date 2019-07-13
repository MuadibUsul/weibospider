# 存储模块

import random
import redis
from SearchSpider.scrapy_redis.setting import *


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化ｒｅｄｉｓ连接
        :param type:
        :param website:
        :param host:地址
        :param port:端口
        :param password:密码
        """

        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取hash的名称
        :return: hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """

        :param username: 用户名
        :param value: 密码或者cookie
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """

        :param username: 用户名
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值对
        :param username:
        :return:
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取数目
        :return:
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机获取键值，用于随机cookie的获取
        :return:
        """
        return random.choice(self.db.hvals(self.name()))

    def username(self):
        """
        获取所有账户信息
        :return:
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return:
        """
        return self.db.hgetall(self.name())

# if __name__ == '__main__':
#     print(RedisClient("cookies", "weibo").random())
