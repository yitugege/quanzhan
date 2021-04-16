# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadoRedisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()    #string
    price = scrapy.Field()    #string
    Num_sell = scrapy.Field() #int 
    like_count = scrapy.Field()  #int
    seller = scrapy.Field()  #string
    id = scrapy.Field()   #string
    url = scrapy.Field()  #string
    current_time = scrapy.Field()   #string
    days60_sell = scrapy.Field()   #string
    pass