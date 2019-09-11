import time
from multiprocessing import Process
from SearchSpider.CookiePool.interface import app
from SearchSpider.CookiePool.generation import *
from SearchSpider.CookiePool.detection import *


class Scheduler(object):
    @staticmethod
    def Detector_Cookies(cycle=CYCLE):
        while True:
            try:
                CookiesDetector = WeiboCookiesDetector()
                CookiesDetector.run()
                print("Cookies检测完成!")
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def Generate_Cookies(cycle=CYCLE):
        while True:
            try:
                generator = WeiboCookiesGenerator()
                generator.find_empty_cookie()
                print("Cookies生成完成")
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print("API接口开始运行")
        app.run(host='127.0.0.1', port=4000)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()
        if GENERATOR_PROCESS:
            generator_process = Process(target=Scheduler.Generate_Cookies)
            generator_process.start()
        if DETECTOR_PROCESS:
            detector_process = Process(target=Scheduler.Detector_Cookies)
            detector_process.start()


# if __name__ == '__main__':
#     Scheduler().run()
