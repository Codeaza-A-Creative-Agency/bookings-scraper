# # import requests
# # r = requests.get("https://www.booking.com/reviewlist.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaLUBiAEBmAExuAEXyAEM2AED6AEB-AECiAIBqAIDuAKMhtGUBsACAdICJDFjMzNjMTBiLTgxZGYtNGViMC04MjM4LTkyZTBhMTRkOTk0MNgCBOACAQ&sid=1f151b43a32790c15dc498940c0c85c3&srpvid=b9961d4c6b62003e&;cc1=pt&pagename=casas-de-canavezes&r_lang=&review_topic_category_id=&type=total&score=&sort=&room_id=&time_of_year=&dist=1&offset=0&rows=35&rurl=&text=&translate=&length_of_stay=1&_=1653883988863")
# # print(r.status_code)


# import scrapy
# from scrapy.crawler import CrawlerProcess


# class bookingsScraper(scrapy.Spider):
#     name = "bookingsScraper"
#     allowed_domains = ['booking.com']
#     # url = "https://www.booking.com/reviewlist.html?aid=355028&sid=1549047c74a89e97aea3aceb98166ca9&srpvid=ad73237a01a2015b&;cc1=us&pagename=pod-times-square&r_lang=&review_topic_category_id=&type=total&score=&sort=&room_id=&time_of_year=&dist=1&offset=0&rows=10&rurl=&text=&translate=&_=1653886975201"
#     url = "https://www.booking.com/reviewlist.html?aid=355028&sid=1549047c74a89e97aea3aceb98166ca9&srpvid=ad73237a01a2015b&;cc1=us&pagename=park-lane-new-york&r_lang=&review_topic_category_id=&type=total&score=&sort=&room_id=&time_of_year=&dist=1&offset=0&rows=10&rurl=&text=&translate=&_=1653886977919"
#     custom_settings = {
#         'DOWNLOAD_DELAY' : 0.25,
#         'RETRY_TIMES': 10,
#         'COOKIES_ENABLED':True,
#         'COOKIES_DEBUG':True,
#         "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
#     }
#     headers = {
#   'Accept': '*/*',
#   'Accept-Language': 'en-US,en;q=0.9',
#   'Connection': 'keep-alive',
# #   'Cookie': 'cors_js=1; bkng_sso_session=e30; OptanonConsent=implicitConsentCountry=nonGDPR&implicitConsentDate=1652250839505; _pxvid=53139d84-d0f4-11ec-b414-7959636e556c; _gcl_au=1.1.1490827559.1652250842; _scid=3e8be222-10b6-4be2-b36a-45b1ff278aa4; _pin_unauth=dWlkPU9HSXlOV1E1TlRrdFpUZzJaQzAwTXpJeUxUaGpZbVV0WXpGa05UYzBPVEUwTmpJMA; bkng_frontend_sese_exp=1; _px_f394gi7Fvmc43dfg_user_id=OWQwMjI3ODAtZGRhMS0xMWVjLThkZjItNzc0MDk5MWEwZjgx; _sctr=1|1653591600000; g_state={"i_p":1654338449236,"i_l":3}; _pxhd=NJ8AqTVCYRod-PfwR4bM%2F7W-9Hz7fcqI0OkPooodSoLoEwufpQMlmlMyrMYFHByeMLEeD5W8vi9SYeLwwXfyuQ%3D%3D%3AnGVkLUautAQQOMHPP6y12kLLb6wIxe9UUPoo3EcmotUEXdxKEiF9tC-RBAGl028swTjuJqLz-5-9RTsiWin5FsViq7rJlgvELtfVwVkNSAE%3D; _gid=GA1.2.343120683.1653886933; BJS=-; pxcts=ab3e1ea3-dfd5-11ec-a462-56546b4c7271; _pxff_ddtc=1; bkng_prue=1; bkng_sso_ses=eyJib29raW5nX2dsb2JhbCI6W3siaCI6Ill1TUhzc2VSMkk4V3FwMW9vYVlnYk42T2pFb0ZyUERYcG9hbWhKTUUxdHciLCJhIjoxfV19; 11_srd=%7B%22features%22%3A%5B%7B%22id%22%3A16%7D%5D%2C%22score%22%3A3%2C%22detected%22%3Afalse%7D; _ga=GA1.1.717382070.1652250839; _px3=ff063b5a8722245e995ad04dd3a41d8459917454ad8e17a9c30165687e4937d7:3czTX2KPfFsXhEH1iI9beD2tn4HZJpe1p7//2545+CpJOXUo3JOP0ifIi6jaB+dPU3+xtu2KPfnbe9mrc9xTbg==:1000:Bn4Z83Z+CyrbJG6ZDOeVl/LzrNLX3P5OE+2JE45kdVupcclnBgTqM5ervSma3MAUJBQ35+O+A8h1HcEtxahn3Q/JK1OSRh0n3B7wovy5o1QDm7curdfDJalaBULSn333q1ZjEbBOEoKgjdOrn6qsbwCWkc4PUWXKIEb4Z3VwdODa1Hb84g0mkzO50ty8GOqUH1bwF8aCYMjh0QPMVDN60Q==; _derived_epik=dj0yJnU9QUtxQlBRa25KbElJVXFKUTU0QzUtU3BBTmlCNlZvVW0mbj1pTGJaTWxXME5wZXN1cHJJa1hKLWl3Jm09MSZ0PUFBQUFBR0tVVUFzJnJtPTEmcnQ9QUFBQUFHS1VVQXM; has_preloaded=1; _ga_FPD6YLJCJ7=GS1.1.1653886935.7.1.1653886992.0; bkng=11UmFuZG9tSVYkc2RlIyh9YSvtNSM2ADX0BnR0tqAEmjtfaSz3IhshRkxbrsKLmdxckGLIgUQGKIMLvXaiN6tnKa%2Bs3uZxnfblEobzT%2B6PSPJO%2Fk%2FOJUwoU57ulpq356hrqYFQDbKAmBHvTxZobn9LdGRP%2BvoBeSpGsCfy5mgmZpI8eu9yUSS67%2FPFxCS5SGwYI3%2BU%2Ft12dZ9ZBsPeQ9ZtlQ%3D%3D; lastSeen=0; _uetsid=acb59cc0dfd511ec9e5ca776b1397889; _uetvid=58b08320d0f411ec8155d7ccb80aa6ea; _pxde=b91c32f3a3ee3d4ddd2295d0aabf332f4bf4615bedbf08b0cde4debc389ae1cf:eyJ0aW1lc3RhbXAiOjE2NTM4ODY5OTM5NTAsImZfa2IiOjAsImlwY19pZCI6W119; _gat=1; _pxhd=2xwnoqmzukpyxkfOltf%2F%2F-NWaFah4glPdbHDhf9yUXRnKftUeZOhqgQG5FH110%2FJBRiKYSIZOeA-n7KtQPZngQ%3D%3D%3ACxAhmFmFZEtwv1bSGL%2FnsKLm%2F80xtPO%2FXWyHDrnWr1yDex0Z77NGKxVSDkxuwzaV5o5yrBhG4WZKadAGHOauOJtkzsnIG-iPQg4XkmdhXAw%3D; bkng=11UmFuZG9tSVYkc2RlIyh9YXSgTtYpR%2F1WOjMvuuinviGUt%2BY5upzWrjRXOTDUCNZtlDRh%2FgHYQjqSVLa75QmLEN5QhRM8m1sF4Vec4xxQW7SqJcjUYDH35sX7e3yJxjDTmcKkEaITeNSRyyZrUbTbZTCsvUuLApFyzmI7Cm0BDhTSqrwTkzWdY2CbkkYczMqP5pTBEDRJQyjaSX9V4SQfWA%3D%3D',
#   'Referer': 'https://www.booking.com/',
#   'Sec-Fetch-Dest': 'empty',
#   'Sec-Fetch-Mode': 'cors',
#   'Sec-Fetch-Site': 'same-origin',
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
# #   'X-Booking-AID': '355028',
# #   'X-Booking-CSRF': 'PYiUYgAAAAA=9UBPY45mQBMl7S7Kq3iM9h4xhejb3FIjbzGMbDdY4fH75ETfogopmT03XX0AXg6N4ZQrm2Q6kbzzyzK18JMdrcvsgFLbrW9MrbliZmqfeYMgWfq8u8Re91gfD3fOmJ5kNtvTYcP8egG77AJ6fIvcmpmSyHrfbmGTUMzmcvTRQ1kBSRANr1NjBUI4UHSr8YZzHPE2XXYrc7f_fzbh',
# #   'X-Booking-Client-Info': 'aaTBNZZJRLESPIDNJDPBFO|1,aaTBNZZJRLESPIDNJDPBFO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,eWHMADDbddHUYcLcDNTVXAeJXVbOMNMTKe|1,eWHMADDbddHUYcLcDNTVXAeJXVbOMNMTKe|2,eWHMADDbddHUYeSYIeBZSJGUO|1,eWHMADDbddHUYeSYIeBZSJGUO|2,eWHMADDbddHUYeSYIeBZSJGUO|4,ODREGZUTPOOOCaJebTZWKNUMEfTRe|1,ODREGZUTPOOOCaJebTZWKNUMEfTRe|3,OOGbIFBUMEfTQJNDYBFKYOeeIKdFHaO|2,OOGbIFBUMEfTQJNDYBFKYOeeIKdFHaO|4',
# #   'X-Booking-Info': '1464770,1522130,1522650,1527620,1528350,1528860,1531600,1531720,1532260,1534400,1535640,1536040,1536450,1536930,1538940,1539130,1540070,HINZJLeUXSaZbOTMXC|4,1531720|1,1539130|2,1539130|4,HINZJLeUXSaZbOTMXC|2,TcZJFHINZJLUOaQWEaffPSTbeeYSKGBYT|1,TcZJFHINZJLUOaQWEaffPSTbeeYSKGBYT|2,aaTBNZZJRLESPIDNJDPBFO|1,aaTBNZZJRLESPIDNJDPBFO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,eWHMADDbddHUYcLcDNTVXAeJXVbOMNMTKe|1,eWHMADDbddHUYcLcDNTVXAeJXVbOMNMTKe|2,eWHMADDbddHUYeSYIeBZSJGUO|1,eWHMADDbddHUYeSYIeBZSJGUO|2,eWHMADDbddHUYeSYIeBZSJGUO|4,ODREGZUTPOOOCaJebTZWKNUMEfTRe|1,ODREGZUTPOOOCaJebTZWKNUMEfTRe|3,OOGbIFBUMEfTQJNDYBFKYOeeIKdFHaO|2,OOGbIFBUMEfTQJNDYBFKYOeeIKdFHaO|4',
#   'X-Booking-Language-Code': 'en-us',
# #   'X-Booking-Pageview-Id': '5fbb237ee5200050',
# #   'X-Booking-Session-Id': '1549047c74a89e97aea3aceb98166ca9',
# #   'X-Booking-SiteType-Id': '1',
# #   'X-Partner-Channel-Id': '3',
#   'X-Requested-With': 'XMLHttpRequest',
#   'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"Windows"'
# }
#     def start_requests(self):
#         yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse_reviews)
#     def parse_reviews(self,response):
#         print(response.body)


# process = CrawlerProcess()
# process.crawl(bookingsScraper)
# process.start()

# date = "February 13, 2022"
# date_time_str = date.strftime("%Y-%m-%d")
# print('DateTime String:', date_time_str)
# import datetime
# month_name = "November"
# datetime_object = datetime.datetime.strptime(month_name, "%B")
# month_number = datetime_object.month
# print(month_number)


import pandas as pd
import json

path='scrapper.log'

log_data=open(path,'r')
result={}
i=0
for line in log_data:
    columns = line.split(" ") #or w/e you're delimiter/separator is
    data={}
    # for c in columns:
        # key = c.split('=')[0]
        # value=c.split('=')[1]
        # data[key]=value
    result[i]=columns
    i+=1
j=json.dumps(result)
# print(j)

df=pd.read_json(j)
print(df)