import requests
import re
import pymysql
from yaml import emit
import web_crawler
import web_data_analysis
import comment_analysis
import comment_crawler
import item_crawler
import comment_analysis
import time
import emailUtil
from flask import  Flask,render_template,request,url_for
app=Flask(__name__,template_folder='./templates')


@app.route('/')
def index():
    return render_template("index.html")
@app.route('/item',methods=['POST','GET'])
def itempage():
    keyword=request.form['input'] #获取姓名文本框的输入值
    web_crawler.item_crawler(keyword) #爬取网站商品信息
    web_data_analysis.item_analysis(keyword)
    return render_template("item.html",data = keyword)   #使用跳转html页面路由
@app.route('/comment',methods=['POST','GET'])
def commentpage():
    # link = request.form.get('link')
    # seller_id,product_id = item_crawler.item(link)
    # comment_crawler.comment(seller_id,product_id)
    # comment_analysis.comment_analysis(product_id)
    return render_template("comment.html")
@app.route('/comment_visualization',methods=['POST','GET'])
def commentpage1():
    link = request.form.get('link')
    product_id,seller_id,imgage,original_price,activity_price,title = item_crawler.item(link)
    comment_crawler.comment(seller_id,product_id)
    comment_analysis.wordcloud(product_id)
    return render_template("comment_visualization.html",data = link)
@app.route('/comment_topic',methods=['POST','GET'])
def commentpage2():
    link = request.form.get('link1')
    product_id,seller_id,imgage,original_price,activity_price,title = item_crawler.item(link)
    comment_crawler.comment(seller_id,product_id)
    comment_analysis.topic(product_id)
    return render_template("comment_topic.html",data = link)
@app.route('/price_track',methods=['POST','GET'])
def pricepage():
    # link = request.form.get('link')
    # seller_id,product_id = item_crawler.item(link)
    # comment_crawler.comment(seller_id,product_id)
    # comment_analysis.comment_analysis(product_id)
    return render_template("price_track.html")
@app.route('/price_track1',methods=['POST','GET'])
def pricepage1():
    link = request.form.get('link3')
    product_id,seller_id,image,original_price,activity_price,title = item_crawler.item(link)
    item_crawler.image_save(image)
    return render_template("price_track1.html",data = link,data1 = original_price, data3=activity_price,data2 = title,val1=time.time())
@app.route('/price_track2',methods=['POST','GET'])
def pricepage2():
    email1 = request.form['email1']
    emailUtil.sendemail(email1)
    return render_template("price_track2.html",data=email1)
if __name__=="__main__":
    app.run(port=2020,host="127.0.0.1",debug=True)
