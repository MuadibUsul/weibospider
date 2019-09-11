import scrapy
from SearchSpider.weiboID import weiboID


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    HOST = ['http://weibo.com/']

    def parse(self, response):
        pass
