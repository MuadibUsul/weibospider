# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class SearchspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    NickName = Field()  # 昵称
    Gender = Field()  # 性别
    Province = Field()  # 所在省
    City = Field()  # 所在城市
    Signature = Field()  # 个性签名
    Birthday = Field()  # 生日
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    Sex_Orientation = Field()  # 性取向
    Marriage = Field()  # 婚姻状况
    URL = Field()  # 首页链接

