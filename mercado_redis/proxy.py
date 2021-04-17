import random
from scrapy.exceptions import CloseSpider
from .proxyip import PROXIES
class ProxyMiddleware(object):
    #def process_request(self, request, spider):
    #    request.meta['proxy'] = 'http://107.173.122.99:8888'
    def process_request(self, request, spider):
        ip = random.choice(PROXIES)
        #ip = random.randint(8,254)
        #ip = "http://23.231.106."+str(ip)+":8888"   
        print('测试IP:', ip)
        request.meta['proxy'] = ip

class CheckStatusMiddleware(object):
    #如何状态码大于400，则视为错误那么直接退出
    def process_response(self, request, response, spider):
        #if response.status >= 403:
        #    raise CloseSpider('%s爬虫异常,退出!'%response.url)
        #    return None
        #else:
        return response
 
  #def process_response(self, request, response, spider):
    #print('代理IP:', request.meta['proxy'])
   # return response

        
        