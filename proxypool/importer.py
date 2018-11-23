from proxypool.proxy_db import RedisClient


class Importer(object):
    def __init__(self):
        self.conn = RedisClient()

    def set(self, proxy):
        result = self.conn.add(proxy)
        print(proxy)
        print('录入成功' if result else '录入失败')

    def scan(self):
        print('请输入代理， 输入exit退出')
        while True:
            proxy = input()
            if proxy == 'exit':
                break
            set(proxy)


if __name__ == '__main__':
    importer = Importer()
    importer.scan()
