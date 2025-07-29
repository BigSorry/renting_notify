from scrapy.crawler import CrawlerProcess
from renting_scraper.renting_scraper.spiders.pararrius_crawler import ParariusCrawler
from renting_scraper.renting_scraper.spiders.huur_woningen_crawler import HuurWoningenCrawler
import util
import datetime
import notify_user as notify
from scrapy.utils.project import get_project_settings

def runCrawlers(crawlers_with_files):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for crawler_class, file_path in crawlers_with_files:
        process.crawl(
            crawler_class,
            feed_path=file_path  # pass the file path as a spider argument
        )

    process.start()

def getScrapedItems():
    items_to_send = {}
    for crawler_class, file_path in crawlers:
        # JSON with all processed links
        new_scraped_json = util.readJson(file_path)
        # Sort on date for emails
        sorted_date_items = sorted(
            new_scraped_json,
            key=lambda x: datetime.datetime.strptime(x["date"], "%d-%m-%Y")
        )

        items_to_send[file_path] = sorted_date_items

    return items_to_send

if __name__ == "__main__":
    old_scraped_json_path = 'json/output.json'
    crawlers = [(HuurWoningenCrawler, './json/huurwoningen.json'),
               (ParariusCrawler, './json/pararius.json')]
    runCrawlers(crawlers)
    items_to_send = getScrapedItems()

    for path, scraped_items in items_to_send.items():
        print(*items_to_send, sep="\n")
        old_scraped_json = util.readJson(old_scraped_json_path)
        # Send telegram notifications and bookkeep what we have sent
        notify.send_telegram_notifications(scraped_items, old_scraped_json, always_send=False)
        util.saveJson(old_scraped_json_path, old_scraped_json)
