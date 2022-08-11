import requests
import re
import pymysql
import os
def item_crawler(keyword):
    conn=pymysql.connect(host = '127.0.0.1' # 连接名称，默认127.0.0.1
    ,user = 'root' # 用户名
    ,passwd='ml20sm2shiyao' # 密码
    ,port= 3306 # 端口，默认为3306
    ,db='final_project' # 数据库名称
    ,charset='utf8' # 字符编码
    )
    cur = conn.cursor() # 生成游标对象

    url = 'https://www.aliexpress.com/wholesale?SearchText='+keyword+'&SortType=total_tranpro_desc'
#print(url)
    web_resp = requests.get(url)
    web_page = web_resp.text
    web_obj = re.compile('productId":"(?P<product_id>.*?)".*?storeName":"(?P<store_name>.*?)","storeId":(?P<store_id>.*?)},.*?"displayTitle":"(?P<item_name>.*?)".*?starRating":(?P<star>.*?),.*?formatted_price":"￡(?P<price>.*?)",.*?"tradeDesc":"(?P<sold>.*?) sold',re.S)
    web_result = web_obj.finditer(web_page)
    i = 0
    cur.execute("create table if not exists %s"%keyword+"(id int,url varchar(255),store_name varchar(255),store_id int,item_name varchar(255),star float,price float,sold int);")

    for it in web_result:
        i = i+1
        product_id = it.group("product_id")
        store_name = it.group("store_name")
        store_id = it.group("store_id")
        item_name = it.group("item_name")
        star = it.group("star")
        price = it.group("price")
        sold = it.group("sold")
        url1 = 'https://www.aliexpress.com/item/'+product_id+'.html'
        #print(url)
        # print(store_id)
        # print(item_name)
        #print(i,store_name,store_id,item_name,star,price,sold)
        sql = "insert into %s"%keyword+" values(%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (i,url1,store_name,store_id,item_name,star,price,sold)
        cur.execute(sql,param)
        conn.commit()
    cur.close()
    conn.close()