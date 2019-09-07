from flask import Flask, g
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
