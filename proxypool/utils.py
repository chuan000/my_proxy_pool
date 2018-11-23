import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_page(url, options={}):
    """
    抓取代理页面
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('抓取成功', url, response.status_code)
            return response.text
        else:
            print('抓取失败', url, response.status_code)
    except ConnectionError:
        print('抓取失败', url)
        return None
