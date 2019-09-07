# -*- coding: utf-8 -*-

import re
import json
import random
from urllib import parse
import requests
import base64
import rsa
from hashlib import md5
import binascii
import time
import logging
from SearchSpider.CookiePool.agents import agents


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


class WeiboLogin(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.session = requests.Session()
        logging.debug('initial completed!')

    def get_su(self):
        username_quote = parse.quote_plus(self._username)
        su = base64.b64encode(username_quote.encode("utf-8")).decode('utf-8')
        # logging.debug("su is: %s", su)
        return su

    def get_prelogin_args(self, su):
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.19)",
            "su": su,
            "_": int(time.time() * 1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            prelogin_args = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except Exception as excep:
            prelogin_args = {}
            logging.error("Get prelogin args error:%s" % excep)
        # logging.debug("Prelogin args are: %s", prelogin_args)
        return prelogin_args

    def get_sp(self, servertime, nonce, pubkey):
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self._password)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        sp = binascii.b2a_hex(password).decode()
        # logging.debug("sp is: %s", sp)
        return sp

    def get_postdata(self, su, sp, prelogin_args):
        postdata = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "qrcode_flag": 'false',
            "useticket": "1",
            "pagerefer": "",
            "vsnf": "1",
            "su": su,
            "service": "miniblog",
            "servertime": prelogin_args['servertime'],
            "nonce": prelogin_args['nonce'],
            "pwencode": "rsa2",
            "rsakv": prelogin_args['rsakv'],
            "sp": sp,
            "sr": "1366*768",
            "encoding": "UTF-8",
            "prelt": "1085",
            "url": "https://www.weibo.com/ajaxlogin.php?framelogin=1&callback=parent."
                   "sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }
        # 如果需要输入验证码
        if 'showpin' in prelogin_args.keys():
            if prelogin_args['showpin'] == 1:
                pin_url = 'https://login.sina.com.cn/cgi/pin.php?r=%s&s=0&p=%s' % (
                    int(time.time() * 1000), prelogin_args["pcid"])
                try:
                    # 拿到验证码
                    pic = self.session.get(pin_url).content
                except Exception as excep:
                    pic = b''
                    logging.error("Get pin error:%s" % excep)
                # 将验证码保存到本地文件
                with open("pin.png", "wb") as file_out:
                    file_out.write(pic)
                # 交互请输入验证码上的文字
                code = get_code()
                # print(code)
                postdata["pcid"] = prelogin_args["pcid"]
                # 将输入的验证码传递给postdata["door"]
                postdata["door"] = code
            else:
                pass
        else:
            pass
        # logging.debug("postdata is: %s",postdata)
        # 返回postdata
        return postdata

    def Login(self):
        # 构造请求头
        agent = random.choice(agents)
        self.session.headers.update({
            'User-Agent': agent})
        # 调用get_su()拿到加密后的用户名
        self.su = self.get_su()
        # 调用get_prelogin_args()，拿到返回值prelogin_args
        self.prelogin_args = self.get_prelogin_args(self.su)
        # 如果没拿到返回值，则输出log信息
        if not self.prelogin_args:
            logging.debug('Weibo Prelogin Fail!')
        else:
            # 调用get_sp()拿到sp密钥
            self.sp = self.get_sp(self.prelogin_args["servertime"], self.prelogin_args["nonce"],
                                  self.prelogin_args["pubkey"])
            #
            self.postdata = self.get_postdata(self.su, self.sp, self.prelogin_args)
            login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_=%d' % int(
                time.time() * 1000)
            try:
                # 请求网页并将返回值存入loginpage
                login_page = self.session.post(login_url, data=self.postdata)
                return login_page
            except Exception as excep:
                # 捕捉异常
                logging.error("Get login page error:%s" % excep)
                # 返回False
                return False


def get_code():
    chaojiying = Chaojiying_Client('1456438724', 'nxbGxB9EXf9fCeD', '898615')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('pin.png', 'rb').read()
    return chaojiying.PostPic(im, 1902)['pic_str']


def get_cookies(username, password):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    # 实例化WeiboLogin() 并传入username, password两个变量值
    A = WeiboLogin(username=username, password=password)
    # 调用login()方法
    response = A.Login()
    all_cookies = response.cookies.items()
    if all_cookies:
        # for i in all_cookies:
        #     print(i)
        cookie = all_cookies[5]
        logging.debug('Get Cookies Succedss!')
        print(cookie)
        return cookie
    else:
        print("获取 " + username + " cookies失败")


# if __name__ == '__main__':
#     get_cookies("0012232080400", "gew25619")
