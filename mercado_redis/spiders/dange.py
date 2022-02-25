import scrapy
from ..items import MercadoRedisItem
import re
import datetime


#采集指定url
class QuotesSpider(scrapy.Spider):
    name = "quanzhan"
    #allowed_domains = ["mercadolibre.com.mx"]
    #start_urls = ["https://articulo.mercadolibre.com.mx"]
    #base_urls ='https://computacion.mercadolibre.com.mx/'


    def start_requests(self):
        urls = [
            'https://www.mercadolibre.com.mx/guitarra-electrica-yamaha-pac012100-series-112v-de-aliso-vintage-white-brillante-con-diapason-de-palo-de-rosa/p/MLM17517052',
            'https://articulo.mercadolibre.com.mx/MLM-1300005017-4-altavoz-motorola-g7-power-g7-play-g8-power-original-4pzs-_JM'
            ]
        for url in urls:
            yield scrapy.Request(url=url,dont_filter=True,callback=self.parse)

    def parse (self,response):
        print('--------------------当前连接----------------')
        print(response.url)
        #print(response.request.meta['redirect_urls'][0])
        items = MercadoRedisItem()
        #没有标题说明连接挂了，不抓,标记为delete
        title = response.xpath('//h1[@class="ui-pdp-title"]/text()').get()
        if  title == None:
            title = "delete"
        #链接
        url = response.url
        #获取商品ID非空那么插入，否则抓取302之前的url获取id从数据库删除
        id = re.findall(r"\d{6,}",url)
        if  id != []:
            id = int("".join([str(x) for x in id]))
        else:
            url=response.request.meta['redirect_urls'][0]
            id = re.findall(r"\d{7,}",url)
            id = int("".join([str(x) for x in id]))
        print(id)

         #获取价格
        price = response.xpath('//div[@class="ui-pdp-price__second-line"]/span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript"]/span[@class="andes-money-amount__fraction"]/text()').get()
        if  price == None:
            price = 0
        #打印点赞人数,把数组中的数字提取出来转换城数字
        like_count = response.xpath('//a[@class="ui-pdp-review__label ui-pdp-review__label--link"]/span[@class="ui-pdp-review__amount"]/text()').get()
        if like_count != None:
            like_count = re.findall(r"\d{1,}",like_count)
            like_count = list(map(int,like_count))
            like_count = like_count = like_count[0]
        else:
            like_count = None

        #print("-----------------------------------likeaccount--------------------------")
        #print(like_count)
        #打印店铺
        #seller = response.xpath('//a[@class="ui-pdp-action-modal__link"]/span[@class="ui-pdp-color--BLUE"]/text()').get()
        #获取分类
        category = response.xpath('//li[@class="andes-breadcrumb__item"][1]/a[@class="andes-breadcrumb__link"]/@title').get()
        #获取销量,判读是否为usado,如果不是那么取整数，如果是不做操作
        Num_sell = response.xpath('//div[@class="ui-pdp-header"]/div[@class="ui-pdp-header__subtitle"]/span[@class="ui-pdp-subtitle"]/text()').get()
        if  Num_sell is None:
            Num_sell = 0
        #    return
        #print("-----------------------------------Num_sell--------------------------")
        #print(Num_sell)
        #print(type(Num_sell))
        elif bool(re.findall(r'\d+',Num_sell)):
            Num_sell = re.findall(r"\d+",Num_sell)
            Num_sell = list(map(int,Num_sell))
            Num_sell = Num_sell[0]
            #print("-----------------------------------Num_sell--------------------------")
            #print(Num_sell)
            #print(type(Num_sell))
        else:
            Num_sell = None
        #获取60天销量
        days60_sell=response.xpath('//strong[@class="ui-pdp-seller__sales-description"]/text()').get()
        if days60_sell is None:
            days60_sell = 0
        #    return
        elif bool(re.findall(r'\d+',days60_sell)):
            days60_sell = re.findall(r'\d+',days60_sell)
            days60_sell = list(map(int,days60_sell))
            days60_sell = days60_sell[0]
        else:
            days60_sell = None
        #记录爬取的时间
        #GMT_FORMAT = '%D %H:%M:%S'
        GMT_FORMAT = '%D'
        current_time = datetime.datetime.utcnow().strftime(GMT_FORMAT)

        items['title']=title
        items['url']=url
        items['price']=price
        items['like_count']=like_count
        items['id']=id
        items['category']=category
        items['Num_sell']=Num_sell
        items['current_time']=current_time
        items['days60_sell']=days60_sell
        items['tablename'] =self.name
        return items
