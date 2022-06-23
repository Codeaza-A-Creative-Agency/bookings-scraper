import json
import aiohttp
import asyncio
from scrapy import Selector
import mysql.connector as mysql
import time
import pandas as pd
from logs import logger

async def main(cc, name, offset, rows, query_id):
    url = f"https://www.booking.com/reviewlist.html?cc1={cc}&pagename={name}&r_lang=en&sort=f_recent_desc&offset={offset}&rows={rows}"
    print("The url for query {} is {}".format(query_id, url))
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://www.booking.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-Booking-Language-Code': 'en-us',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.text()
                response = Selector(text=data)
                # complete reviews data
                # reviewer_name,review_title,reviewer_location,stay_time,reviewed_time,room_type
                re_scrape_query = "SELECT reviewer_name,reviewer_location,review_title,stay_time,reviewed_time,room_type FROM reviews_data WHERE query_id=%s"
                vall = (int(query_id),)              
                cursor.execute(re_scrape_query,vall)  
                db_review_data = cursor.fetchall()
                # scraping work
                reviews_list_xpath = "//ul[contains(@class,'review_list')]/li"
                reviews_list = response.xpath(reviews_list_xpath)
                reviewer_names = []
                reviewer_locations = []
                room_types = []
                stay_timess = []
                stay_dates = []
                stay_likes = []
                review_times = []
                review_titles = []
                # review_texts = []
                # 
                positive_review_texts = []
                negative_review_texts = []

                review_ratings = []
                hotel_responses = []
                photos_count = []

                for review in reviews_list:
                    user_details = review.xpath(
                        ".//div[contains(@class,'c-review-block__left')]")
                    reviewer_name = user_details.xpath(
                        ".//span[contains(@class,'bui-avatar-block__title')]/text()").extract_first()
                    try:
                        reviewer_location = user_details.xpath(
                            ".//span[contains(@class,'bui-avatar-block__subtitle')]/text()").extract_first()
                    except:
                        reviewer_location = 'none'
                    if reviewer_location == '':
                        reviewer_location = 'none'
                    elif reviewer_location is None:
                        reviewer_location = 'none'

                    try:
                        room_type = user_details.xpath(
                            ".//a[contains(@class,'c-review-block__room-link')]/div/text()").extract_first()
                    except:
                        room_type = None
                    if room_type is None:
                        room_type = None
                    stay_time_date = user_details.xpath(
                        ".//ul[contains(@class,'c-review-block__stay-date')]/li/div")
                    stay_time = stay_time_date.xpath('./text()').extract_first().strip().split(" ")[0]
        
                    stay_date = stay_time_date.xpath(
                        "./span/text()").extract_first()
                    if stay_date:
                        stay_date = stay_date.strip()

                    stay_like = user_details.xpath(
                        ".//ul[contains(@class,'review-panel-wide__traveller_type')]/li/div/text()").extract_first().strip()
                    review_details = review.xpath(
                        ".//div[contains(@class,'c-review-block__right')]")

                    review_title = review_details.xpath(
                        ".//h3[contains(@class,'c-review__title--ltr')]/text()").extract_first()
                    if review_title:
                        review_title = review_title.strip()

                    # review_text = ''
                    positive_review_text = ''
                    negative_review_text = ''

                    review_body = review_details.xpath(
                        ".//span[contains(@class,'c-review__body')]/text()").extract()
                    if len(review_body) == 1:
                        if "There are no comments" in review_body[0]:
                            pass
                        else:
                            positive_review_text = review_body[0]
                    else:
                        positive_review_text = review_body[0]
                        negative_review_text = review_body[1]
        
                    # for data in review_body:
                    #     review_text = review_text + data

                    temp_review_time = review_details.xpath(
                        "./div/span/text()").extract()
                    review_time = ''
                    for data in temp_review_time:
                        if "Reviewed:" in data:
                            data = data.replace('Reviewed:', '')
                            review_time = data
                    review_rating = review_details.xpath(
                        ".//div[contains(@class,'bui-review-score__badge')]/text()").extract_first()
                    review_rating = float(review_rating)
                    try:
                        hotel_response = review_details.xpath(
                            ".//span[contains(@class,'c-review-block__response__body')]/text()").extract_first()
                    except:
                        hotel_response = 'none'
                    if hotel_response is None:
                        hotel_response = 'none'

                    # review photos count
                    photos = len(review.xpath(".//ul[contains(@class,'c-review-block__photos')]/li").extract())
                    
                    reviewer_names.append(reviewer_name)
                    reviewer_locations.append(reviewer_location)
                    room_types.append(room_type)
                    stay_timess.append(stay_time)
                    stay_dates.append(stay_date)
                    stay_likes.append(stay_like)
                    review_times.append(review_time)
                    review_titles.append(review_title)
                    # review_texts.append(review_text)
                    positive_review_texts.append(positive_review_text)
                    negative_review_texts.append(negative_review_text)
                    review_ratings.append(review_rating)
                    hotel_responses.append(hotel_response)
                    photos_count.append(photos)

                count = 0
                for reviewer_name in reviewer_names:
                    room_type = room_types[count].strip() if room_types[count] else room_types[count]
                    reviewer_name = None if reviewer_name == "Anonymous" else reviewer_name
                    # reviewer_name,review_title,reviewer_location,stay_time,reviewed_time,room_type
                    cond_check = [i for i in db_review_data if (reviewer_name in i) and (review_titles[count] in i) and (reviewer_locations[count] in i) and (stay_timess[count] in i) and (review_times[count].strip() in i) and (room_type in i)]
                    # cond_check = [i for i in db_review_data if (reviewer_locations[count] in i) and (review_titles[count] in i)]
                    if not cond_check:
                        cursor.execute("INSERT INTO reviews_data(query_id,reviewer_name, reviewer_location, room_type, stay_time,stayed_date,stay_like,reviewed_time,review_title, positive_review_text, negative_review_text,photos, review_rating,hotel_response ) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (int(query_id), reviewer_name, reviewer_locations[count], room_type, stay_timess[count],  stay_dates[count], stay_likes[count], review_times[count].strip(), review_titles[count],positive_review_texts[count],negative_review_texts[count],photos_count[count], review_ratings[count], hotel_responses[count],))
                        db.commit()
                        count = count + 1
                    else:
                        print("NOTHING BREAKING")
                        break
                # update anonymous to null
                # query1 = "UPDATE reviews_data SET reviewer_name = NULL WHERE reviewer_name = 'Anonymous'"
                # cursor.execute(query1)
                # db.commit()
                # update query status
                query = "UPDATE query SET review_data = %s WHERE query_id=%s"
                val = (1,int(query_id))
                cursor.execute(query,val)
                db.commit()
    except asyncio.TimeoutError:
        print("Timeout Error")


async def gathered_tasks(link, query_id, total_reviews,prev_reviews):
    # url to be scraped
    # link = "https://www.booking.com/hotel/us/park-lane-new-york.html?aid=355028&sid=1549047c74a89e97aea3aceb98166ca9&dest_id=20088325;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=7;hpos=7;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1653886966;srpvid=ad73237a01a2015b;type=total;ucfs=1"
    
    link = link.split('/')
    cc = link[4]
    link = link[5]
    name = link.split('.')
    name = name[0]
    limit = (abs(int(prev_reviews)-int(total_reviews))//25) + 1
    # limit = (int(total_reviews)//25) + 1  # here must change limit value
    limit = int(limit)

    await asyncio.gather(*[main(cc, name, (i*25), 25, query_id) for i in range(0, limit)]) 


async def main_scraper_func():
    table_data = pd.read_sql(
        "SELECT q.query_id,q.business_link,hd.english_review,hd.prev_eng_review FROM query q INNER JOIN hotel_data hd ON q.query_id = hd.query_id WHERE q.review_data=0", db)
    await asyncio.gather(*[gathered_tasks(table_data['business_link'][i], table_data['query_id'][i], table_data['english_review'][i],table_data['prev_eng_review'][i]) for i in range(len(table_data['business_link']))])


# log files
log = logger()
scraper_logger = log.scrapper_logger("reviews_data","review_scrapper.log")

scraper_logger.info("Review Scraper Started")

# db connection
with open("config.json","r") as file:
    configuration = json.load(file)
try:
    db = mysql.connect(
        host = configuration["db_host"],
        user=configuration["db_username"],
        password=configuration["db_password"],
        database=configuration["db_name"])

    cursor = db.cursor()
    scraper_logger.info("DB Conecction Established")
except:
    scraper_logger.error("Error while Establishing Connection")
    
# scraper driver code
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)

initial = time.time()
asyncio.get_event_loop().run_until_complete(main_scraper_func())
# asyncio.run(main_scraper_func())
scraper_logger.info("Taken {} time to complete".format(time.time()-initial))
print("Taken {} time to complete".format(time.time()-initial))
