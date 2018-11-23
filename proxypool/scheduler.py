import time
from proxypool.tester import Tester
from proxypool.getter import Getter
from proxypool.settings import *
from proxypool.api import app
from multiprocessing import Process


class Scheduler(object):
    def scheduler_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self, cycle=TESTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
    # scheduler.schedule_api()
