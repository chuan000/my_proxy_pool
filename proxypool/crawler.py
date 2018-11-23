"""免费代理获取类"""
from proxypool.utils import get_page
from lxml import etree
from random import randint
import requests
import time
import re

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self):
        """
        抓取代理66
        :param page_count: 页数
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/areaindex_35/index.html'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            selector = etree.HTML(html)
            trs = selector.xpath('//*[@id="footer"]/div/table/tr')[1:]
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                yield '%s:%s' % (ip, port)

    def crawl_3wei360(self, page_count=10):
        """
        抓取三维360代理
        :param page_count: 页数
        :return: 代理
        """
        start_url = 'http://www.swei360.com/?page={}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                trs = selector.xpath('//div[@id="list"]/table/tbody/tr')
                for tr in trs:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        抓取goubanjia
        :return: 代理
        """
        ntime = int(time.time())
        pre_url = 'http://z13.cnzz.com/stat.htm'
        pre_data = {
            'id': '1253707717',
            'r': 'http://www.goubanjia.com/',
            'lg': 'zh-cn',
            'ntime': ntime,
            'cnzz_eid': '1004880314-1542071942-null',
            'showp': '1536x864',
            't': '全网代理IP-高匿HTTP代理IP服务器供应商',
            'umuuid': '1670ab7a25d52f-0c920b02d8830d-8383268-144000-1670ab7a25ebd0',
            'h': '1',
            'rnd': randint(500000000, 2000000000)
        }
        pre_headers = {
            'Referer': 'http://www.goubanjia.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/69.0.3497.100 Safari/537.36'
        }
        pre_res = requests.get(pre_url, data=pre_data, headers=pre_headers)
        print('goubanjia pre_url content', pre_res.text)
        start_url = 'http://www.goubanjia.com/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'UM_distinctid=1670ab7a25d52f-0c920b02d8830d-8383268-144000-1670ab7a25ebd0; \
            JSESSIONID=6E019E33396649769C8A0DB0C53B2122; CNZZDATA1253707717=1004880314-1542071942-null%7C{}'.format(ntime),
            'Host': 'www.goubanjia.com',
            'Referer': 'http://www.goubanjia.com/buy/dynamic.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/69.0.3497.100 Safari/537.36'
        }
        res = requests.get(start_url, headers=headers)
        print('goubanjia status code', res.status_code)
        html = res.text
        # with open('../pages/goubanjia.html', 'w', encoding='utf-8') as f:
        #     f.write(html)
        if html:
            selector = etree.HTML(html)
            tds = selector.xpath('//*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr/td[1]')
            for td in tds:
                nodes = td.xpath('./child::node()')
                proxy = ''
                for node in nodes:
                    if node == ':':
                        proxy += ':'
                    elif node.xpath('./@style') and 'none' in node.xpath('./@style')[0]:
                        continue
                    elif not node.xpath('./text()'):
                        continue
                    else:
                        proxy += node.xpath('./text()')[0]
                yield proxy

    def crawl_ip3366(self):
        """
        抓取云代理
        :return:代理
        """
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype={}&page={}'
            for type in [1, 3]:
                for page in range(1, 8):
                    url = start_url.format(type, page)
                    html = get_page(url)
                    if html:
                        selector = etree.HTML(html)
                        trs = selector.xpath('//*[@id="list"]/table/tbody/tr')
                        for tr in trs:
                            ip = tr.xpath('./td[1]/text()')[0]
                            port = tr.xpath('./td[2]/text()')[0]
                            proxy = ':'.join([ip, port])
                            yield proxy
                    time.sleep(1.5)

    def crawl_kuaidaili(self):
        """
        抓取快代理
        :return: 代理
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        for page in range(1, 4):
            url = start_url.format(page)
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                trs = selector.xpath('//*[@id="list"]/table/tbody/tr')
                for tr in trs:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    proxy = ':'.join([ip, port])
                    yield proxy
            time.sleep(1)

    def crawl_xicidaili(self):
        """
        抓取西刺代理
        :return: 代理
        """
        start_url = 'http://www.xicidaili.com/nn/{}'
        for page in range(1, 4):
            url = start_url.format(page)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWZlZjg0YTY5ZGQ2YmE1NzEzM2IyZjIzZmZjN2M3ZjIzBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXhnUzNzLzdBVVdldjJXd1NXTjFybXo3TFBPdUZOcVNCYk1GQlA0YmR3cFU9BjsARg%3D%3D--7f5a128c858c50d4915b943a074f560a8126a974; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1542073245,1542261074; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59={}'.format(int(time.time())),
                'Host': 'www.xicidaili.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            print('正在抓取', url)
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                print('抓取失败', url, res.status_code)
                continue
            print('抓取成功', url, res.status_code)
            html = res.text
            if html:
                selector = etree.HTML(html)
                trs = selector.xpath('//table[@id="ip_list"]/tr')[1:]
                for tr in trs:
                    ip = tr.xpath('./td[2]/text()')[0]
                    port = tr.xpath('./td[3]/text()')[0]
                    proxy = ':'.join([ip, port])
                    yield proxy

    def crawl_iphai(self):
        """
        抓取ip海代理
        :return:
        """
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            selector = etree.HTML(html)
            trs = selector.xpath('/html/body/div[4]/div[2]/table/tr')[1:]
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0].strip()
                port = tr.xpath('./td[2]/text()')[0].strip()
                proxy = ':'.join([ip, port])
                yield proxy

    def crawl_89ip(self):
        """
        抓取89免费代理
        :return:
        """
        start_url = 'http://www.89ip.cn/tqdl.html?api=1&num=1000&port=&address=&isp='
        html = get_page(start_url)
        if html:
            find_ips = re.compile(r'\d+.\d+.\d+.\d+:\d+')
            ip_ports = find_ips.findall(html)
            for proxy in ip_ports:
                yield proxy

    def crawl_data5u(self):
        """
        抓取无忧代理
        :return:
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=82E460AD96E45F1A4CC0BBBB4BDD4300',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        start_url = 'http://www.data5u.com/free/{}/index.shtml'
        type_list = ['gngn', 'gwgn']
        for type in type_list:
            url = start_url.format(type)
            html = get_page(url, options=headers)
            if html:
                ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
                re_ip_address = ip_address.findall(html)
                for address, port in re_ip_address:
                    result = address + ':' + port
                    yield result.replace(' ', '')

    def crawl_seofangfa(self):
        start_url = 'http://ip.seofangfa.com/'
        html = get_page(start_url)
        if html:
            selector = etree.HTML(html)
            trs = selector.xpath('//div[@class="container theme-showcase"]/tbody[1]/div[1]/table/tbody/tr')
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                proxy = ':'.join([ip, port])
                yield proxy


if __name__ == '__main__':
    crawler = Crawler()
    proxies = list(crawler.crawl_seofangfa())
    print(proxies)
    print(len(proxies))


