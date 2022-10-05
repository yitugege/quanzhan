import scrapy
from ..items import MercadoRedisItem
import re
import datetime
import os


#采集指定url
class QuotesSpider(scrapy.Spider):
    name = "test"
    #allowed_domains = ["mercadolibre.com.mx"]
    start_urls = ["http://httpbin.org/get"]
    #base_urls ='https://computacion.mercadolibre.com.mx/'


    def parse(self,response):
        print(response.text)
        
    