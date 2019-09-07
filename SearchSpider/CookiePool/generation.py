from SearchSpider.CookiePool.account import weibo_accounts
from SearchSpider.CookiePool.storage import RedisClient
from SearchSpider.CookiePool.login import get_cookies


class WeiboCookiesGenerator(object):
    def __init__(self):
        """
        初始化redis
        """
        self.accounts_db = RedisClient('accounts', 'weibo')
        self.cookies_db = RedisClient('cookies', 'weibo')
        self.extraction_account()

    def extraction_account(self):
        redis_account_usernames = self.accounts_db.username()
        for weibo_account in weibo_accounts.keys():
            if weibo_account not in redis_account_usernames:
                weibo_account_password = weibo_accounts[weibo_account]
                print(weibo_account + " " + weibo_account_password)
                self.accounts_db.set(weibo_account, weibo_account_password)

    def find_empty_cookie(self):
        """
        找到未生成cookie的账号并生成cookie
        :return:
        """
        account_usernames = self.accounts_db.username()
        cookie_usernames = self.cookies_db.username()
        for account_username in account_usernames:
            if account_username not in cookie_usernames:
                account_password = self.accounts_db.get(account_username)
                self.generate_cookie(account_username, account_password)

    def generate_cookie(self, username, password):
        """
        传入账号密码,生成cookie并存储到redis数据库中
        :param username:
        :param password:
        :return:
        """
        count = 0
        while True:
            cookie = get_cookies(username, password)
            print('生成Cookies成功')
            cookie = cookie[0] + '=' + cookie[1]
            print(type(cookie))
            if cookie:
                self.cookies_db.set(username, cookie)
                break
            elif count == 3:
                print('生成cookie失败')
                break
            count += 1


# if __name__ == '__main__':
    # Generation().generate_cookie('0014015610110', 'gjm83438')
    # Generation().find_empty_cookie()
