import scrapy
from scrapy.crawler import CrawlerProcess
from sqlalchemy import null
from config import connection, close_connection
import datetime
import json
import time
import pandas as pd
import re
# import pyautogui

# //a[@id='hotel_header']/@data-atlas-latlng (xpath for latitude,longitude)

with open('config.json', 'r') as c:
    configuration = json.load(c) 
    # params = json.load(c)["params"]
from logs import logger

log = logger()
scraper_logger = log.scrapper_logger("hotel_data","scrapper.log")


class BusinessSpider(scrapy.Spider):
    allowed_domains = ['booking.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        "AUTOTHROTTLE_ENABLED" : True,   #  Enable and configure the AutoThrottle extension (disabled by default)
        # "AUTOTHROTTLE_START_DELAY" : 0.2,   # The initial download delay
        # "AUTOTHROTTLE_TARGET_CONCURRENCY" : 32,  # The average number of requests Scrapy should be sending in parallel
        "DOWNLOAD_TIMEOUT": 360,     # Default: 180
        'RETRY_TIMES': 10,
        # 'COOKIES_ENABLED': True,
        # 'COOKIES_DEBUG': True,
        # "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
        # proxy implementation
        "ROTATING_PROXY_LIST" : configuration['proxy_list'],
        "DOWNLOADER_MIDDLEWARES" : {
            "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
            "rotating_proxies.middlewares.BanDetectionMiddleware" : 620
        }
    }

    name = "business_spider"
    cursor, db = connection()
    # url = "https://www.booking.com/hotel/us/park-lane-new-york.html?aid=355028&sid=1549047c74a89e97aea3aceb98166ca9&dest_id=20088325;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=7;hpos=7;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1653886966;srpvid=ad73237a01a2015b;type=total;ucfs=1&#hotelTmpl"
    # self.url = "https://www.booking.com/hotel/pt/casas-de-canavezes.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaLUBiAEBmAExuAEXyAEM2AED6AEB-AECiAIBqAIDuAKMhtGUBsACAdICJDFjMzNjMTBiLTgxZGYtNGViMC04MjM4LTkyZTBhMTRkOTk0MNgCBOACAQ&sid=1f151b43a32790c15dc498940c0c85c3&all_sr_blocks=251207404_103625995_2_2_0;checkin=2022-05-30;checkout=2022-05-31;dist=0;group_adults=2;group_children=0;hapos=2;highlighted_blocks=251207404_103625995_2_2_0;hpos=2;matching_block_id=251207404_103625995_2_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=251207404_103625995_2_2_0__6300;srepoch=1653883801;srpvid=b9961d4c6b62003e;type=total;ucfs=1&#hotelTmpl"

    def start_requests(self):
        # cursor, db = connection()
        urls = pd.read_sql("SELECT * FROM query WHERE hotel_data=0",self.db)['business_link']
        for url in urls:
            scraper_logger.info(f"Link is \'{url}\'")
            yield scrapy.Request(url=url, callback=self.parse,meta={"url":url})

    def hotel_data(self, response):
        # scraper_logger.info(f"Link is \'{response.meta.get('url')}\'")
        name_xpath = "//h2[contains(@id,'hp_hotel_name')]/text()"
        address_xpath = '//p[contains(@id,"showMap2")]/span[1]/text()'
        description_xpath = '//div[contains(@class,"k2-hp--description")]/div/div/div/div[3]/p/text()'
        choosen_reasons_xpath = '//div[contains(@class,"bui-text--variant-emphasized_1")]/text()'
        total_reviews_xpath = '//a[contains(@id,"show_reviews_tab")]/span/text()'
        # hotel_class and recommended_stay
        hotel_class_xpath = "//span[@data-testid='rating-stars']/span"
        hotel_class_xpath_01 = "//span[@data-testid='rating-circles']/span"
        hotel_class_xpath_02 = "//span[@data-testid='rating-squares']/span"

        recommended_stay_xpath = "//span[contains(@class,'facility-badge__tooltip-title')]/text()"

        name = response.xpath(name_xpath).extract()
        name = name[1]
        address = response.xpath(address_xpath).extract_first()
        temp_description = response.xpath(description_xpath).extract()
        description = ''
        for data in temp_description:
            description = description + data
        choose = response.xpath(choosen_reasons_xpath).extract()
        reason = ''
        for data in choose:
            if not data == '\n' and not data == '':
                reason = reason + data

        # manipulated as output required
        if reason:
            reason = reason.strip()
            reason = reason.replace("\n","")
            reason = re.sub(r"\s{2}",",",reason)
        
        total_reviews = response.xpath(total_reviews_xpath).extract()
        total_reviews = total_reviews[1]
        total_reviews = total_reviews.replace(' ', '')
        total_reviews = total_reviews.replace('(', '')
        total_reviews = total_reviews.replace(')', '')
        total_reviews = total_reviews.replace(',', '')
        total_reviews = int(total_reviews)
    
        # hotel class and class source of Hotel
        if response.xpath(hotel_class_xpath).extract():
            hotel_class = len(response.xpath(hotel_class_xpath).extract())
            class_source = "official"
        elif response.xpath(hotel_class_xpath_01).extract():
            hotel_class = len(response.xpath(hotel_class_xpath_01).extract())
            class_source = "assessed"
        elif response.xpath(hotel_class_xpath_02).extract():
            hotel_class = len(response.xpath(hotel_class_xpath_02).extract())
            class_source = "website"
        else:
            hotel_class = None
            class_source = None
        
        recommended_stay = response.xpath(recommended_stay_xpath).extract()
        # hotel english reviews for reviews scraper
        english_reviews = response.xpath("//div[contains(@id,'review_lang_filter')]//ul[@class='bui-dropdown-menu__items']/li//button[contains(@data-value,'en')]/text()").extract()
        data = " ".join(english_reviews).split(" ")[-1].strip()
        # data = data.replace("(","")
        # data = data.replace(")","")

        data = " ".join(english_reviews)
        data = re.findall("\d+",data)

        english_review = data[0] if data else 0
        # english_review = data

        return name, address, description, reason, total_reviews,hotel_class,class_source,recommended_stay,english_review

    def guest_reviews(self, response):
        staff_rating = ''
        facility_rating = ''
        cleaning_rating = ''
        comfort_rating = ''
        value_for_money_rating = ''
        location_rating = ''
        free_wifi_rating = ''
        rating_xpath = '//div[contains(@data-testid,"review-score-component")]/div/text()'
        rating = response.xpath(rating_xpath).extract_first()
        other_ratings_xpath = "//div[contains(@class,'hp_subscore_explanation_container')]"
        other_ratings = response.xpath(other_ratings_xpath)
        other_rating = other_ratings[1]
        category_type = other_rating.xpath(
            './div/div/ul/li/div/span[1]/text()').extract()
        category_rating = other_rating.xpath(
            './div/div/ul/li/div/span[2]/text()').extract()
        count = 0
        for category in category_type:
            if "Staff" in category:
                staff_rating = category_rating[count]
            elif "Facilities" in category:
                facility_rating = category_rating[count]
            elif "Cleanliness" in category:
                cleaning_rating = category_rating[count]
            elif "Comfort" in category:
                comfort_rating = category_rating[count]
            elif "Value for money" in category:
                value_for_money_rating = category_rating[count]
            elif "Location" in category:
                location_rating = category_rating[count]
            elif "Free WiFi" in category:
                free_wifi_rating = category_rating[count]
            count = count + 1
        return rating, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating

    def property_Q_and_A(self, response):
        questions = []
        answers = []
        Q_and_A_xpath = "//li[contains(@class,'js-guest-question-carousel-card')]//div[contains(@class,'qa_item_text')]/span/text()"
        data = response.xpath(Q_and_A_xpath).extract()
        j = 0
        k = 1
        for i in range(0, len(data)):
            try:
                questions.append(data[j])
                answers.append(data[k])
                j = j + 2
                k = k + 2
            except:
                break
        return questions, answers

    def Facilities(self, response):
        popular_facilities_xpath = "//div[contains(@class,'hotel-facilities__most-popular')]//div[contains(@class,'important_facility')]/text()"
        popular_facilities = response.xpath(popular_facilities_xpath).extract()
        facilities = ''
        for popular_facility in popular_facilities:
            if not popular_facility == "\n":
                popular_facility = popular_facility.replace("\n", '')
                facilities = facilities + popular_facility
                facilities = facilities + ","
        # adding additional amenities
        additional_amenities = response.xpath("//div[contains(@class,'hotel-facilities__list')]//ul/li/div/div/text()").extract()
        amenities = ""
        for amenity in additional_amenities:
            if amenity != "\n":
                amenity = amenity.replace("\n","")
                amenities = amenities + amenity + ","

        facility_list_xpath = "//div[contains(@class,'hotel-facilities__list')]"
        facility_list = response.xpath(facility_list_xpath)
        allData = facility_list.xpath('./div')
        facility_titles = []
        facility_texts = []
        for data in allData:
            names = data.xpath(
                './/div[contains(@class,"bui-title__text")]/text()').extract()
            for name in names:
                if not name == '\n':
                    name = name.replace('\n', '')
                    facility_titles.append(name)
            descriptions = data.xpath(
                './/div[contains(@class,"bui-list__description")]/text()').extract()
            temp_description = ''
            for description in descriptions:
                if not description == '\n':
                    temp_description = temp_description + description
                    temp_description = temp_description + ','
            temp_description = temp_description.replace('\n', '')
            facility_texts.append(temp_description)
            try:
                food_type = response.xpath(
                    '//p[contains(@class,"cuisines")]/text()')[1].extract()
            except:
                food_type = 'none'
        return facilities+amenities, facility_titles, facility_texts, food_type

    def hotel_surrounding(self, response):
        hotel_surroundings_xpath = "//div[contains(@class,'hp_location_block__content_container')]"
        hotel_surroundings = response.xpath(hotel_surroundings_xpath)
        allData = hotel_surroundings.xpath('./div')
        surroundings = []
        descriptionss = []
        for data in allData:
            names = data.xpath(
                './/span[contains(@class,"bui-title__text")]/text()').extract()
            for name in names:
                if not name == '\n':
                    name = name.replace('\n', '')
                    surroundings.append(name)
            descriptions = data.xpath(
                './/div[contains(@class,"bui-list__description")]/text()').extract()
            temp_description = ''
            for description in descriptions:
                if not description == '\n':
                    temp_description = temp_description + description
                    temp_description = temp_description + ','
            temp_description = temp_description.replace('\n', '')
            descriptionss.append(temp_description)

        return surroundings, descriptionss

    def db_hotel(self, query_id, name,hotel_class,class_source,recommended_stay, description, address, rating,english_review, total_reviews, reason_to_choose, facilities, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating, food_type):
        # cursor, db = connection()
        self.cursor.execute(
            "SELECT * FROM hotel_data WHERE query_id=%s", (query_id,))
        hotel_data = self.cursor.fetchall()

        if hotel_data: #means we need to update hotel data
            update_query = "UPDATE hotel_data SET name=%s,hotel_class=%s,class_source=%s,recommended_stay=%s,description=%s,address=%s,rating=%s,prev_eng_review=english_review,english_review=%s,total_reviews=%s,reason_to_choose=%s,popular_amenities=%s,staff_rating=%s,facilities_rating=%s,cleaning_rating=%s,comfort_rating=%s,value_for_money_rating=%s,location_rating=%s,free_wifi_rating=%s,food_type=%s WHERE query_id=%s"
            update_val = (name.strip(),hotel_class,class_source,",".join(recommended_stay), description, address.strip(), rating,english_review, total_reviews,  reason_to_choose, facilities, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating, food_type,query_id)
            self.cursor.execute(update_query,update_val)
            self.db.commit()

            hotel_data_id = hotel_data[0][0]
            scraper_logger.info("Hotel Data Updated Successfully")
        else:
            print("HELLO WORLD: ",name," reviews is: ",english_review)
            try:
                # print("The data is: ",query_id, name, description, address, rating, total_reviews,  reason_to_choose, facilities, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating, food_type)
                self.cursor.execute("INSERT INTO hotel_data(query_id,name,hotel_class,class_source,recommended_stay,description, address, rating,english_review, total_reviews,  reason_to_choose, popular_amenities, staff_rating, facilities_rating, cleaning_rating, comfort_rating,value_for_money_rating,location_rating, free_wifi_rating, food_type ) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (query_id, name.strip(),hotel_class,class_source,",".join(recommended_stay), description, address.strip(), rating,english_review, total_reviews,  reason_to_choose, facilities, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating, food_type,))
                self.db.commit()
                scraper_logger.info("Hotel Data Inserted Successfully!")

            except:
            #     print("Description is: ",description)
                scraper_logger.error("Error in inserting hotel data")
            self.cursor.execute(
                "SELECT * FROM hotel_data WHERE query_id=%s", (query_id,))
            hotel_data = self.cursor.fetchall()
            hotel_data_id = hotel_data[0][0]
        # close_connection(cursor, db)
        return hotel_data_id

    def db_facilities(self, hotel_data_id, type, description):
        types = type
        descriptions = description
        # cursor, db = connection()
        self.cursor.execute(
            "SELECT * FROM hotel_facilities WHERE hotel_data_id=%s", (hotel_data_id,))
        facilities_data = self.cursor.fetchall()

        if not facilities_data:
            count = 0
            for type in types:
                self.cursor.execute(
                    "INSERT INTO hotel_facilities( hotel_data_id,  type, description) VALUES ( %s, %s,%s)", (hotel_data_id, type, descriptions[count],))
                self.db.commit()
                count = count + 1
        # close_connection(cursor, db)
 
    def db_question_answers(self, hotel_data_id, question, answer):
        questions = question
        answers = answer

        # cursor, db = connection()
        self.cursor.execute(
            "SELECT * FROM hotel_question_answers WHERE hotel_data_id=%s", (hotel_data_id,))
        question_answer_data = self.cursor.fetchall()
        if not question_answer_data:
            count = 0
            for question in questions:
                self.cursor.execute(
                    "INSERT INTO hotel_question_answers( hotel_data_id,  question, answer) VALUES ( %s, %s,%s)", (hotel_data_id, question, answers[count],))
                self.db.commit()
                count = count + 1
            # scraper_logger.info(
                # "Data inserted into hotel_question_answers table Scucessfully!")
        else:
            scraper_logger.info(
                "Data already exists in hotel_question_answers table")

        # close_connection(cursor, db)

    def parse(self, response):
        scraper_logger.info(f"Link is \'{response.meta.get('url')}\'")
        start_time = time.perf_counter()
        # query_id = self.query_data()
        cursor, db = connection()
        query="SELECT * FROM query WHERE business_link=%s"
        val = (response.meta.get("url"),)
        cursor.execute(query,val)
        query_id=cursor.fetchone()
        query_id=query_id[0]

        self.hotel_surrounding(response)
        questions = []
        answers = []
        questions, answers = self.property_Q_and_A(response)
        facility_titles = []
        facility_texts = []
        facilities, facility_titles, facility_texts, food_type = self.Facilities(
            response)
        rating, staff_rating, facility_rating, cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating = self.guest_reviews(
            response)
        name, address, description, reason_to_choose, total_reviews,hotel_class,class_source,recommended_stay,english_review = self.hotel_data(
            response)
        surroundings = []
        surrounding_descriptions = []
        surroundings, surrounding_descriptions = self.hotel_surrounding(
            response)
        new_titles = facility_titles + surroundings
        new_descriptions = facility_texts + surrounding_descriptions
        hotel_data_id = self.db_hotel(query_id, name,hotel_class,class_source,recommended_stay, description, address, rating,english_review, total_reviews, reason_to_choose, facilities, staff_rating, facility_rating,
                                      cleaning_rating, comfort_rating, value_for_money_rating, location_rating, free_wifi_rating, food_type)
        self.db_facilities(hotel_data_id, new_titles, new_descriptions)
        self.db_question_answers(hotel_data_id, questions, answers)
        end_time = time.perf_counter()
        
        # update query status 
        # print("Where: ",query_id)
        query = "UPDATE query SET hotel_data=%s WHERE query_id=%s"
        val = (1,query_id)
        cursor.execute(query,val)
        db.commit()
        close_connection(cursor, db)
        
        total_time = end_time - start_time
        scraper_logger.info(f"Data inserted in {total_time} seconds")


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BusinessSpider)
    process.start()
