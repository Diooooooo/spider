# *-* coding:utf-8 *-*
import datetime
import json
import socket

import requests


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self):
        self.proxies = []
        self.get_proxies_kuai()

    def get_proxies_kuai(self):
        socket.setdefaulttimeout(2)
        j = requests.get('http://mvip.piping.mogumiao.com/proxy/api/get_ip_bs?appKey=c1083312668747c0a182aa3fa863b6d3'
                         '&count=10&expiryDate=0&format=1&newLine=2')
        infoJson = json.loads(j.text)
        if '0' == infoJson['code']:
            for i in infoJson['msg']:
                self.proxies.append(i['ip']+':'+i['port'])
        else:
            with open('/root/spider/final_spider/error', 'a') as e:
                e.write(str(infoJson) + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    a = Proxies()
    with open('/root/spider/final_spider/proxy', 'w') as f:
        for proxy in a.proxies:
            f.write(proxy + '\n')
