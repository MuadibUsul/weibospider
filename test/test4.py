from multiprocessing import Process


def api():
    while True:
        print("this is api model")


def Generate_Cookies():
    print("this is Generate_Cookies model")


def Detector_Cookies():
    print("this is Detector_Cookies model")


def run():
    api_process = Process(target=api())
    generator_process = Process(target=Generate_Cookies())
    detector_process = Process(target=Detector_Cookies())
    generator_process.start()
    detector_process.start()
    api_process.start()


if __name__ == '__main__':
    run()
