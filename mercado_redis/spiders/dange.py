import scrapy
import re
import datetime


#采集指定url
class QuotesSpider(scrapy.Spider):
    name = "dange"
    #allowed_domains = ["mercadolibre.com.mx"]
    start_urls = ["http://httpbin.org/get"]
    def parse(self,response):
        print(response.text)
    

   