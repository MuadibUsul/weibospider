import requests
from requests.exceptions import ConnectionError
from SearchSpider.scrapy_redis.storage import RedisClient

TEST_URL_MAP = {
    'weibo': 'https://weibo.com/p/1003061192329374/info?mod=pedit_more"'
}


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    # 测试对应站点，返回200说明cookie有效
    # 不同站点可以以此为父类进行扩展，重写该方法，实现自己的测试逻辑
    def test(self, username, cookies):
        raise NotImplementedError

    # 迭代拿出所有的cookies，然后循环调用`test`方法测试是否可用
    # 如果cookie失效，就在redis删除对应的键值对
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.item():
            self.test(username, cookies)


# 微博站点的测试cookies逻辑
class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)

        try:
            headers = {
                "Cookies": "SUB="+cookies,
                # "User-Agent": UserAgent().random
                "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
            }
        except TypeError:
            print('Cookis不合法',  username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return

        try:
            test_url = TEST_URL_MAP[self.website]
            print(test_url)
            response = requests.get(test_url, headers=headers)
            if response.status_code == 200:
                print('cookies有效', username)
                print('部分测试结果', response.text[0:50])
            else:
                print(response.status_code, response.headers)
                print('cookies失效', username)
                self.cookies_db.delete(username)
                print('删除cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)

    def run_detector(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


# if __name__ == '__main__':
#     WeiboValidTester().run_detector()
