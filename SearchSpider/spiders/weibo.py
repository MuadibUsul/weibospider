# -*- coding: utf-8 -*-
import scrapy
from SearchSpider.weiboID import weiboID
import requests


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    HOST = ['http://weibo.com/']

    def get_first_url_page(self):
        for id in weiboID:
            fans_url = "https://weibo.com/" + id + "/fans"
            follows_url = "https://weibo.com/" + id + "/follow"


    def parse(self, response):
        for fans_url, follows_url in self.get_first_url():
            print(fans_url)
            print(follows_url)

    def parse_detail(self, response):
        pass


if __name__ == '__main__':

    WeiboSpider().parse()
