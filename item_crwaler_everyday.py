import item_crawler
import schedule
import time
import requests
def crawler(url):
    schedule.every().day.at("01:00").do(item_crawler.item(url),'It is 01:00')
    while True:
        schedule.run_pending()
        time.sleep(60) # wait one minute
    