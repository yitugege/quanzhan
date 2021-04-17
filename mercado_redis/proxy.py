import random
from scrapy.exceptions import CloseSpider
from .proxyip import PROXIES
import os
class ProxyMiddleware(object):
    #def process_request(self, request, spider):
    #    request.meta['proxy'] = 'http://107.173.122.99:8888'
    def process_request(self, request, spider):
        #获取当前服务器内网ip,执行对应代理
        ipv4 = os.popen('ip addr show ens18').read().split("inet ")[1].split("/")[0]
        ip = PROXIES.get(ipv4)
        #ip = random.choice(PROXIES)
        #ip = random.randint(8,254)
        #ip = "http://23.231.106."+str(ip)+":8888"   
        print('测试IP:',ip)
        print('本地IP:',ipv4)
        request.meta['proxy'] = ip

class CheckStatusMiddleware(object):
    #如何状态码大于400，则视为错误那么直接退出
    def process_response(self, request, response, spider):
        if response.status >= 403:
            print("--"*10+"返回403错误"+"--"*10)
            raise CloseSpider('%s爬虫异常,退出!'%response.url)
            return None
        else:
            return response
 
  #def process_response(self, request, response, spider):
    #print('代理IP:', request.meta['proxy'])
   # return response

        