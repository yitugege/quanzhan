# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


def dbHandle():
    conn = pymysql.connect(
        host = "192.168.3.200",
        user = "root1",
        password = "123456",
        charset = "utf8",
        port = 3306
    )
    return conn

class MercadoRedisPipeline:
    def process_item(self, item, spider):
        return item

    def process_item(self, item, spider):
       dbObject = dbHandle()
       cursor = dbObject.cursor()
       cursor.execute("USE scrapy")
       #判断如果存在则更新，如果不存在则插入
       sql = "INSERT INTO Mercadolibre(title,url,price,id,seller,like_count,Num_sell,time,days60_sell) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Num_sell=%s,title=%s,url=%s,price=%s,seller=%s,like_count=%s,time=%s,days60_sell=%s"
       try:
            cursor.execute(sql,(item['title'],item['url'],item['price'],item['id'],item['seller'],item['like_count'],item['Num_sell'],item['current_time'],item['days60_sell'],item['Num_sell'],item['title'],item['url'],item['price'],item['seller'],item['like_count'],item['current_time'],item['days60_sell']))
            cursor.connection.commit()
       except BaseException as e:
            print("The error is here>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<<The error is here")
            dbObject.close()
       return item