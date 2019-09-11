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


class about(Item):
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
    URL = Field()  # 首页链接
    update_time = Field()


class blog(Item):
    """微博信息"""
    Public_Time = Field()  # 发布时间
    Blog_Content = Field()  # 博文正文
    Blog_tags = Field()  # 标签
    Image_Links = Field()  # 插图链接
    Fl_Frward = Field()  # 转发人数
    Fl_Comment = Field()  # 评论人数
    Fl_Like = Field()   # 点赞人数
