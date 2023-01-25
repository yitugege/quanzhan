import scrapy
from ..items import MercadoRedisItem
import re
from datetime import date


#采集指定url
class QuotesSpider(scrapy.Spider):
    name = "dange"
    #allowed_domains = ["mercadolibre.com.mx"]
    #start_urls = ["https://articulo.mercadolibre.com.mx"]
    #base_urls ='https://computacion.mercadolibre.com.mx/'


    def start_requests(self):
        urls = [
            #  'https://www.mercadolibre.com.mx/guitarra-electrica-yamaha-pac012100-series-112v-de-aliso-vintage-white-brillante-con-diapason-de-palo-de-rosa/p/MLM17517052',
            #  'https://articulo.mercadolibre.com.mx/MLM-1300005017-4-altavoz-motorola-g7-power-g7-play-g8-power-original-4pzs-_JM',
            #  'https://articulo.mercadolibre.com.mx/MLM-1367897814-auricular-con-flex-compatible-con-iphone-x-_JM#position=1&search_layout=stack&type=pad&tracking_id=8407e428-916d-4214-84f6-5d5cd4caf4c4&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=1&ad_click_id=ZDBjOTQzNTgtMjcwMC00ZjhkLWIyMTYtNmY1NDEwNmExZDQ4',
            #  'https://www.mercadolivre.com.br/processador-gamer-amd-ryzen-5-3600-100-100000031box-de-6-nucleos-e-42ghz-de-frequncia/p/MLB15143240?hide_psmb=true',
            #'https://produto.mercadolivre.com.br/MLB-2202573186-camisa-termica-masculina-proteco-solar-50-tecido-uv-gelado-_JM?attributes=SIZE:Rw==,COLOR_SECONDARY_COLOR:QnJhbmNv',
            # 'https://www.mercadolibre.com.mx/control-joystick-inalambrico-sony-playstation-dualshock-3-urban-camouflage/p/MLM10350491'
            #'https://www.mercadolibre.com.mx/amazon-echo-dot-3rd-gen-con-asistente-virtual-alexa-carbon-110v240v/p/MLM15534261?pdp_filters=deal:MLM779363-1#searchVariation=MLM15534261&position=1&search_layout=grid&type=product&tracking_id=ecd21790-35d9-4df8-9a68-42a89b2c9264&c_id=/home/promotions-recommendations/element&c_element_order=1&c_uid=c6d5fad0-4ab2-408d-ab0f-55b3c09adb83',
            #'https://articulo.mercadolibre.com.mx/MLM-1387799026-cable-hdmi-20-metros-full-hd-1080p-ps3-xbox-x-laptop-pc-tv-_JM#is_advertising=true&position=9&search_layout=stack&type=pad&tracking_id=2f3c11a6-0ae1-46de-a4ae-dc5293a81025&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=9&ad_click_id=M2ZiZDE5YjYtYWMxZi00MzUyLTgwNWYtZjUwMmI1MzNlMDA5'
            #'https://articulo.mercadolibre.com.mx/MLM-1409310041-botella-de-agua-deportiva-anti-fugas-no-toxico-capacidad-2-l-_JM?variation=174427702295&hide_psmb=true',
            #'https://www.mercadolibre.com.mx/mas-vendidos/MLM189026#origin=vip'
            'https://www.mercadolibre.com.mx/figura-de-accion-toy-story-woody-talking-figure-de-disney/p/MLM10204068'
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
        #获取分类
        category = response.xpath('//li[@class="andes-breadcrumb__item"][1]/a[@class="andes-breadcrumb__link"]/@title').get()    
        #链接
        url = response.url
        if "vendidos" not in url:
        #获取商品ID非空那么插入，否则抓取302之前的url获取id从数据库删除
            id = re.findall(r"/M\w\w(\d{7,}|-\d{7,}|/)",url)
            print(id)
        #id = re.findall(r"\d{7,}",url)
            if  id != []:
                id = abs(int("".join([str(x) for x in id])))
            else:
                url=response.request.meta.get('redirect_urls')[0]
                id = re.findall(r"/M\w\w(\d{5,}|-\d{5,}|/)",url)
                id = abs(int("".join([str(x) for x in id])))
        else:        
                id = re.findall(r"/M\w\w(\d{5,}|-\d{5,}|/)",url)
                category = "mas-vendidos"

         #获取价格 没有价格删除连接
        price = response.xpath("//div[@class='ui-pdp-price mt-16 ui-pdp-price--size-large']/div[@class='ui-pdp-price__second-line']/span[@class='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact']/span[@class='andes-money-amount__fraction']/text()").get()
        if  price == None:
            title = "delete"
        #打印点赞人数,把数组中的数字提取出来转换城数字
        like_count = response.xpath('//span[@class="ui-pdp-review__amount"]/text()').get() 
        print("-----------------------------------likeaccount--------------------------")
        print(like_count)
        if like_count is not None:
            like_count = re.findall(r"\d{1,}",like_count)
            like_count = list(map(int,like_count))
            like_count = like_count = like_count[0]
        else:
            like_count = None


        #打印店铺
        #seller = response.xpath('//a[@class="ui-pdp-action-modal__link"]/span[@class="ui-pdp-color--BLUE"]/text()').get()
        
        #获取销量为0不抓,判读是否为usado,如果不是那么取整数，如果是不做操作,
        Num_sell = response.xpath('//div[@class="ui-pdp-header"]/div[@class="ui-pdp-header__subtitle"]/span[@class="ui-pdp-subtitle"]/text()').get()
        print("-----------------------------------Num_sell--------------------------")
        print(Num_sell)
        if  Num_sell is None:
            return
            
        elif Num_sell == "Nuevo":
            return

        #print(type(Num_sell))
        elif bool(re.findall(r'\d{1,}',Num_sell)):
            if "mil" in Num_sell:
                Num_sell = re.findall(r"\d{1,}",Num_sell) 
                Num_sell = list(map(int,Num_sell))
                Num_sell = Num_sell[0]*1000
            else:
                Num_sell = re.findall(r"\d{1,}",Num_sell) 
                Num_sell = list(map(int,Num_sell))
                Num_sell = Num_sell[0]
            print("-----------------------------------Num_sell--------------------------")
            print(Num_sell)
            #print(type(Num_sell))
        else:
            pass
        #获取60天销量
        days60_sell=response.xpath('//strong[@class="ui-pdp-seller__sales-description"]/text()').get()
        if days60_sell is None:
            days60_sell = 0
        #    return
        elif bool(re.findall(r'\d+',days60_sell)):
            if "mil" in days60_sell:
                days60_sell = re.findall(r'\d+',days60_sell)
                days60_sell = list(map(int,days60_sell))
                days60_sell = days60_sell[0]*1000
            else:
                days60_sell = re.findall(r'\d+',days60_sell)
                days60_sell = list(map(int,days60_sell))
                days60_sell = days60_sell[0]
        else:
            days60_sell = None
        #记录爬取的时间
        current_time = date.today()
        # if ((Num_sell == "delete") or (price == "delete" ) or (title == "delete")):
        #     print("------------------------------------delete--------------------");
        #     return
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
