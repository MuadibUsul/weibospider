# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
import pymysql


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, FollowsItem):
            followsItems = dict(item)
            follows = followsItems.pop("follows")
            for i in range(len(follows)):
                followsItems[str(i + 1)] = follows[i]
            try:
                self.Follows.insert(followsItems)
            except Exception:
                pass
        elif isinstance(item, FansItem):
            fansItems = dict(item)
            fans = fansItems.pop("fans")
            for i in range(len(fans)):
                fansItems[str(i + 1)] = fans[i]
            try:
                self.Fans.insert(fansItems)
            except Exception:
                pass
        return item

#
# class MysqlPipline(object):
#     def __init__(self):
#         db = pymysql.connect('localhost', 'root', 'suchen', 'sina')
#         cursor = db.cursor()
#         cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#         sql = """"""
#         cursor.execute(sql)
#         # 关闭数据库连接
#         db.close()
#
#     def process_item(self, item, spider):
