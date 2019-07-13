# REDIS　地址＼端口\密码

REDIS_HOST = "127.0.0.1"

REDIS_PORT = 6379

REDIS_PASSWORD = "suchen"


# MONGODB 地址＼端口＼密码

MONGODB_HOST = "127.0.0.1"

MONGODB_PORT = 27017

# 产生器和验证器循环周期
CYCLE = 1200

# API地址和端口
API_HOST = '0.0.0.0'

API_PORT = 5000

# 产生模块类，如扩展其他站点，请再次配置

GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator'
}

# 测试模块类，如扩展其他站点，请在此配置

TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}

# 产生模块开关

GENERATOR_PROCESS = False

# 验证模块开关

VALID_PROCESS = False

# 接口模块开关

API_PROCESS = True