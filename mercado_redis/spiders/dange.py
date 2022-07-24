import scrapy
from ..items import MercadoRedisItem
import re
from datetime import date


#采集指定url
class QuotesSpider(scrapy.Spider):
    name = "quanzhan"
    #allowed_domains = ["mercadolibre.com.mx"]
    #start_urls = ["https://articulo.mercadolibre.com.mx"]
    #base_urls ='https://computacion.mercadolibre.com.mx/'


    def start_requests(self):
        urls = [
            #  'https://www.mercadolibre.com.mx/guitarra-electrica-yamaha-pac012100-series-112v-de-aliso-vintage-white-brillante-con-diapason-de-palo-de-rosa/p/MLM17517052',
            #  'https://articulo.mercadolibre.com.mx/MLM-1300005017-4-altavoz-motorola-g7-power-g7-play-g8-power-original-4pzs-_JM',
            #  'https://www.mercadolibre.com.mx/anteojos-de-sol-ray-ban-round-frank-legend-standard-con-marco-de-metal-color-polished-gold-lente-light-blue-degradada-varilla-polished-gold-de-metal-rb3857/p/MLM17380290',
            #  'https://www.mercadolibre.com.mx/sniper-elite-iii-ultimate-edition-505-games-xbox-one-fisico/p/MLM6165822#reco_item_pos=13&reco_backend=machinalis-pdp-v2p&reco_backend_type=low_level&reco_client=pdp-v2p&reco_id=15d78e2e-7533-4c4f-908e-822347a7aa9f',
            #  'https://articulo.mercadolibre.com.mx/MLM-1367897814-auricular-con-flex-compatible-con-iphone-x-_JM#position=1&search_layout=stack&type=pad&tracking_id=8407e428-916d-4214-84f6-5d5cd4caf4c4&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=1&ad_click_id=ZDBjOTQzNTgtMjcwMC00ZjhkLWIyMTYtNmY1NDEwNmExZDQ4',
            #  'https://www.mercadolivre.com.br/processador-gamer-amd-ryzen-5-3600-100-100000031box-de-6-nucleos-e-42ghz-de-frequncia/p/MLB15143240?hide_psmb=true',
            #  'https://www.mercadolivre.com.br/processador-gamer-amd-ryzen-5-3600x-100-100000022box-de-6-nucleos-e-44ghz-de-frequncia/p/MLB15080182'
            'https://www.mercadolibre.com.mx/control-joystick-inalambrico-sony-playstation-dualshock-3-urban-camouflage/p/MLM10350491'
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
        id = re.findall(r"/M\w\w(\d{7,}|-\d{7,}|/)",url)
        print(id)
        #id = re.findall(r"\d{7,}",url)
        if  id != []:
            id = abs(int("".join([str(x) for x in id])))
        else:
            url=response.request.meta.get('redirect_urls')[0]
            id = re.findall(r"/M\w\w(\d{7,}|-\d{7,}|/)",url)
            id = abs(int("".join([str(x) for x in id])))
        

         #获取价格 没有价格删除连接
        price = response.xpath("//div[@class='ui-pdp-price mt-16 ui-pdp-price--size-large']/div[@class='ui-pdp-price__second-line']/span[@class='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact']/span[@class='andes-money-amount__fraction']/text()").get()
        if  price == None:
            title = "delete"
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
        #获取销量为0不抓,判读是否为usado,如果不是那么取整数，如果是不做操作,
        Num_sell = response.xpath('//div[@class="ui-pdp-header"]/div[@class="ui-pdp-header__subtitle"]/span[@class="ui-pdp-subtitle"]/text()').get()
        if  Num_sell is None:
            pass
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
            pass
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
        current_time = date.today()

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
