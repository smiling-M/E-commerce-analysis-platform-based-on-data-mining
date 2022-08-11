import requests
import re
import time
def item(url):
    #print(url)
    #商品界面的网址
    # url = input("请输入你的网址：")
    item_resp = requests.get(url)
    item_page = item_resp.text
    #判断该商品是否打折
    item_obj = re.compile('"priceModule":{"activity":(?P<activity>.*?),"',re.S)
    item_result = item_obj.finditer(item_page)
    for it in item_result:
        activity = it.group("activity")
        #print(activity)
    #if activity == 'true':
        #爬虫该商品的信息
        activity_obj = re.compile('productId":(?P<product_id>.*?),.*?sellerAdminSeq":(?P<seller_id>.*?),.*?,"imagePathList":(?P<image>.*?)",.*?"spanishPlaza".*?title":"(?P<title>.*?)"},.*?{"activity":true,"discount":(?P<discount>.*?),"discountPromotion".*?"formatedActivityPrice":"￡(?P<activity_price>.*?)","formatedPrice":"￡(?P<original_price>.*?)","hiddenBigSalePrice".*?"averageStar":"(?P<star>.*?)",".*?fiveStarNum":(?P<fivestar>.*?),".*?fourStarNum":(?P<fourstar>.*?),".*?oneStarNum":(?P<onestar>.*?),".*?"threeStarNum":(?P<threestar>.*?),".*?"totalValidNum":(?P<comment>.*?),".*?"twoStarNum":(?P<twostar>.*?),".*?"formatTradeCount":"(?P<volume>.*?)","')
        activity_result = activity_obj.finditer(item_page)
        for it in activity_result:
            product_id = it.group("product_id")
            seller_id = it.group("seller_id")
            title = it.group("title")
            discount = it.group("discount")
            activity_price = it.group("activity_price")
            original_price = it.group("original_price")
            average_star = it.group("star")
            comment = it.group("comment")
            volume = it.group("volume")
            five_star = it.group("fivestar")
            four_star = it.group("fourstar")
            three_star = it.group("threestar")
            two_star = it.group("twostar")
            one_star = it.group("onestar")
            comment_url = 'https://feedback.aliexpress.com/display/productEvaluation.htm?v=2&productId='+product_id+'&ownerMemberId='+seller_id+'&memberType=seller'
            image = it.group("image")
            image = image.replace('[','')
            image = image.replace('"','')
            print(product_id)
            # print(image)
            #print(title)
            #print("discount:-%{},activity price:{},original price:{},average star:{},volume:{},comment:{}.".format(discount,activity_price,original_price,average_star,volume,comment))
            #print(five_star,four_star,three_star,two_star,one_star)
    return product_id,seller_id,image,original_price,activity_price,title
            # print(seller_id)
            # print(comment_url)
    #if activity == 'false':
        #print("the item doesn't have the discount")
def image_save(image):
    resp = requests.get(image)
    #img_name = image.split("/")[-1] #拿到url中的最后一个/以后的内容
    img = 'img.jpg'
    with open('static'+'/'+img ,mode="wb") as f:
        f.write(resp.content)  #图片内容写入文件




