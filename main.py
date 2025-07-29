from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from renting_scraper.renting_scraper.spiders.funda_crawler import FundaCrawler
from renting_scraper.renting_scraper.spiders.pararrius_crawler import ParariusCrawler
from renting_scraper.renting_scraper.spiders.huur_woningen_crawler import HuurWoningenCrawler
import util
import datetime
import time
import notify_user as notify

def filterDate(new_scraped_json):
    for item in new_scraped_json:
        for url, json_values in item.items():
            date = "json_"

def runSpider(crawler_class, file_path):
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                file_path: {"format": "json", "overwrite": True},
            },
            "LOG_LEVEL" : "INFO"
        }
    )
    process.crawl(crawler_class)
    process.start()



if __name__ == "__main__":
    outputs = ['./json/huurwoningen.json',
               './json/pararius.json']

    # crawler_class = HuurWoningenCrawler
    # scraped_path = outputs[0]

    crawler_class = ParariusCrawler
    scraped_path = outputs[1]

    runSpider(crawler_class, file_path=scraped_path)

    # JSON with all processed links
    new_scraped_json = util.readJson(scraped_path)
    # Sort on date for emails
    sorted_date_items = sorted(
        new_scraped_json,
        key=lambda x: datetime.datetime.strptime(x["date"], "%d-%m-%Y")
    )
    for item in sorted_date_items:
        print(item)
    # Sent mail and save the mail sent attribute
    old_scraped_json_path = 'json/output.json'
    old_scraped_json = util.readJson(old_scraped_json_path)
    notify.send_telegram_notifications(sorted_date_items, old_scraped_json, always_send=False)
    util.saveJson(old_scraped_json_path, old_scraped_json)
