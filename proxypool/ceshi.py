import requests
ip = '110.172.168.244'
port = '8080'
proxy = ip + ':' + port
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}
test_url = 'http://httpbin.org/get'
try:
    res = requests.get(test_url, proxies=proxies, verify=False)
    print(res.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)


