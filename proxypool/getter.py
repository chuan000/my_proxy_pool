from proxypool.proxy_db import RedisClient
from proxypool.crawler import Crawler
from proxypool.settings import *
import sys


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到代理池数量限制
        :return:
        """
        if self.redis.count() > POOL_UPPER_LIMIT:
            return True
        else:
            return False

    def run(self):
        print('代理获取器开始执行')
        if not self.is_over_threshold():
            for crawl_func in self.crawler.__CrawlFunc__:
                proxies = self.crawler.get_proxies(crawl_func)
                # 在这的目的？
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
