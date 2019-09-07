import requests
import random
from SearchSpider.CookiePool.storage import RedisClient
from SearchSpider.CookiePool.configs import *
from SearchSpider.CookiePool.agents import agents


class Detector(object):
    """
    检测父类

    """
    def __int__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        pass

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups:
            self.test(username, cookies)


class WeiboCookiesDetector(Detector):
    def __init__(self, website='weibo'):
        Detector.__int__(self, website)
        print('开始测试Cookies')

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)

    def test(self, username, cookies):
        """
        传入用户名与Cookies,测试其是否能够使用
        :param username:
        :param cookies:
        :return:
        """
        headers = {
            'User-Agent': random.choice(agents),
            'Cookie': cookies
        }
        print('正在测试cookies', '用户名', username)
        try:
            test_url = TEST_URL_MAP[self.website]
            session = requests.Session()
            response = session.get(url=test_url, headers=headers, timeout=5)
            if response.status_code == 200:
                print('Cookies有效', username)
                # print('结果摘要', response.text[0, 100])
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.delete_cookie(username)
        except ConnectionError as e:
            print('发生异常', e.args)

    def delete_cookie(self, username):
        self.cookies_db.delete(username)
        print('删除Cookies成功', username)


# if __name__ == '__main__':
#     WeiboCookiesDetector().run()
#     # print(random.choice(agents))
