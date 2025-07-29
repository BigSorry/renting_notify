import scrapy
import webbrowser
import time

class FundaCrawler(scrapy.Spider):
    name = 'funda_crawler'
    allowed_domains = ["funda.nl"]
    start_urls = ['https://www.funda.nl/zoeken/huur/'
                  '?selected_area=["utrecht"]&price="500-1250"']


    def parse(self, response):
        time.sleep(5)
        all_links = response.css('a::attr(href)').getall()
        # Extract individual property links
        property_links = response.css('a[data-test-id="object-image-link"]::attr(href)').getall()

        if not property_links:
            # Alternative selectors in case the structure changes
            property_links = response.css('a[href*="/huur/"]::attr(href)').getall()
        webbrowser.open(response.url)
        for listing in all_links:
            yield {
                'title': listing.css('h3.search-result__header-title a::text').get(),
                'price': listing.css('span.search-result-price::text').get(),
                'url': response.urljoin(listing.css('h3.search-result__header-title a::attr(href)').get())
            }

        # Follow pagination links (next page)
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
