from SearchSpider.scrapy_redis.storage import RedisClient
from SearchSpider.scrapy_redis.account import account_data
from SearchSpider.scrapy_redis.LoginWeibo import get_cookies

account_conn = RedisClient('accounts', 'weibo')
cookies_conn = RedisClient('cookies', 'weibo')


# 将account文件中的所有账户密码信息存至redis数据库中
def set_account_info():
    for account_info in account_data:
        username = account_info["account_username"]
        password = account_info["password"]
        result = account_conn.set(username, password)
        print('账号', username, '密码', password)
        print('录入成功' if result else '录入失败')


# 将redis数据库中的所有账户信息请求到cookies并存入redis数据库
def set_cookies_info():
    for account in account_conn.username():
        password = account_conn.get(account)
        cookies = get_cookies(username=account, password=password)
        if cookies:
            result = cookies_conn.set(username=account, value=cookies)
            print('账号', account, 'Cookies', password)
            print('录入成功' if result else '录入失败')
        else:
            print("Cookies为空")
            continue


if __name__ == '__main__':

    set_account_info()
    set_cookies_info()