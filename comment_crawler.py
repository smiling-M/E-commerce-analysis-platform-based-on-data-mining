import requests
import re
import pymysql
import item_crawler
def comment(seller_id,product_id):
    # product_id = item_crawler.product_id
    conn=pymysql.connect(host = '127.0.0.1' # 连接名称，默认127.0.0.1
        ,user = 'root' # 用户名
        ,passwd='ml20sm2shiyao' # 密码
        ,port= 3306 # 端口，默认为3306
        ,db='final_project' # 数据库名称
        ,charset='utf8' # 字符编码
    )
    cur = conn.cursor() # 生成游标对象
    sql = "create table if not exists comment_%s"%product_id+"(rate varchar(255),comment_type varchar(255),comment varchar(3000),time varchar(255))"
    cur.execute(sql)
    def comment(str,str1):
        
        post_url = 'https://feedback.aliexpress.com/display/productEvaluation.htm#feedback-list'
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"}
        i=0
        for n in range(1,100):
            dat1 = {
                    "ownerMemberId":seller_id,
                    "memberType":'seller',
                    "productId":product_id,
                    "evaStarFilterValue": str,
                    "page":n-1,
                    "currentPage":n,
                    "v":2
            }
            comment_resp = requests.post(post_url,data=dat1,headers=headers)
            comment_page = comment_resp.text
            comment_obj = re.compile('<div class="f-rate-info">.*?<span style="width:(?P<rate>.*?)"></span>.*?<Strong>Logistics:</Strong>.*?<dt class="buyer-feedback">.*?<span>(?P<comment>.*?)</span>.*?<span class="r-time-new">(?P<time>.*?)</span>',re.S)
            negetive_comment_result = comment_obj.finditer(comment_page)
            for it in negetive_comment_result:
                i = i+1
                rate = it.group('rate')
                comment = it.group('comment')
                time = it.group('time')
                sql1 = "insert into comment_%s"%product_id+" values(%s,%s,%s,%s)"
                print(rate,str1,comment,time)
                param = (rate,str1,comment,time)
                cur.execute(sql1,param)
                conn.commit()
                #print(i,str1,rate,comment,time)
            if(len(comment_page)<10000):
                break

    comment('All cricital','negetive')
    comment('All positive','positive')
    cur.close()
    conn.close()