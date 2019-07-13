from SearchSpider.scrapy_redis.detector import WeiboValidTester
from SearchSpider.scrapy_redis.generation import Generator
from SearchSpider.scrapy_redis.setting import *
from SearchSpider.scrapy_redis.interface import app
from multiprocessing import Process
import time


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                WeiboValidTester().run_detector()
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                generator = Generator()
                generator.set_all_account_info()
                generator.set_all_cookies_info()
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()


if __name__ == '__main__':
    Scheduler().run()