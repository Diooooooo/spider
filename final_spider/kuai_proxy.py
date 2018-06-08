# *-* coding:utf-8 *-*
import json
import socket
import urllib
from datetime import time

from bs4 import BeautifulSoup


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=3):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        # self.get_proxies()
        # self.get_proxies_nn()
        self.get_proxies_kuai()

    def get_proxies_kuai(self):
        socket.setdefaulttimeout(2)
        infoJson = json.loads(str(
            BeautifulSoup(urllib.request.urlopen(
                urllib.request.
                    Request('http://dps.kdlapi.com/api/getdps/?orderid=902836790419538&num=100&ut=1&format=json&sep=1')).read(),
                          "html.parser")))
        for i in infoJson['data']['proxy_list']:
            self.proxies.append(i)
            self.verify_pro.append(i)


if __name__ == '__main__':
    a = Proxies()
    with open('c:\\work\\kuai_proxy', 'w') as f:
        for proxy in a.proxies:
            f.write(proxy + '\n')
