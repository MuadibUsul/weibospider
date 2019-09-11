from flask import Flask
from SearchSpider.CookiePool.storage import RedisClient

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to Cookies Pool System</h1>'


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookies，访问地址如/weibo/random
    :param website:
    :return:
    """
    cookies = RedisClient('cookies', website).random()
    return cookies


@app.route('/<website>/view')
def view(website):
    # 返回目前账号数量以及cookie数量
    table_x = ''
    # account_list = RedisClient('accounts', website).all()
    cookie_list = RedisClient('cookies', website).all()
    for account, cookie in cookie_list.items():
        table_account_x = "<td>" + account + "</td>"
        table_cookie_x = "<td>" + cookie + "</td>"
        table_x = table_x + "<tr>" + table_account_x + "\n" + table_cookie_x + "</tr>"
    return "<table>" + table_x + "</table>"
