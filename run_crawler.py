from scrapy.crawler import CrawlerProcess
from renting_scraper.renting_scraper.spiders.pararrius_crawler import ParariusCrawler
import util
import datetime
import notify_user as notify

def runCrawler(crawler_class, file_path):
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

def getScrapedItems():
    # JSON with all processed links
    new_scraped_json = util.readJson(scraped_path)
    # Sort on date for emails
    sorted_date_items = sorted(
        new_scraped_json,
        key=lambda x: datetime.datetime.strptime(x["date"], "%d-%m-%Y")
    )

    return sorted_date_items

if __name__ == "__main__":
    output_log_json_path = 'json/daily_output_log.json'
    scraped_path = './json/pararius.json'
    crawler_class = ParariusCrawler


    runCrawler(crawler_class, file_path=scraped_path)
    items_to_send = getScrapedItems()
    print(*items_to_send, sep="\n")
    # Read previously sent items
    sent_items_json = util.readJson(output_log_json_path)
    # Send telegram notifications and bookkeep what we have sent
    notify.send_telegram_notifications(items_to_send, sent_items_json, always_send=False)
    # Save updated sent items to output log
    util.saveJson(output_log_json_path, sent_items_json)
