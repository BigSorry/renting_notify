import scrapy
import webbrowser
import time

class ParariusCrawler(scrapy.Spider):
    name = 'pararius_crawler'
    crawler_output_path = f"./json/{name}.json"
    allowed_domains = ["pararius.nl"]
    start_urls = ['https://www.pararius.nl/huurwoningen/'
                  'utrecht/500-1200/straal-25',
                  'https://www.pararius.nl/huurwoningen/'
                  'amersfoort/500-1200/straal-25'
                  ]
    huur_filter = '-te-huur'

    # test = webbrowser.open(response.url)
    def parse(self, response):
        time.sleep(1)
        links = [
            response.urljoin(link)
            for link in response.css('a.listing-search-item__link--title::attr(href)').getall()
            if 'huur' in link # filter out other links
        ]

        for url in links:
            yield response.follow(url, callback=self.parse_listing)

    def parse_listing(self, response):
        # extract details from the listing page
        url = response.url
        title = response.css("h1.listing-detail-summary__title::text").get(default="").strip()
        location = response.css(".listing-detail-summary__location::text").get(default="").strip()
        price = response.css(".listing-detail-summary__price-main::text").get(default="").strip()
        price_postfix = response.css(".listing-detail-summary__price-postfix::text").get(default="").strip()
        surface_area = response.css("li.illustrated-features__item--surface-area::text").get(default="").strip()
        number_of_rooms = response.css("li.illustrated-features__item--number-of-rooms::text").get(default="").strip()
        interior = response.css("li.illustrated-features__item--interior::text").get(default="").strip()
        main_description_information = response.css('span.listing-features__main-description::text').getall()
        date = main_description_information[1] # Assumes the second elements in the list is the stored date
        #print(date)
        if "weken" in date.lower():
            return
        yield {
            url: {
                "title": title,
                "location": location,
                "price": price,
                "price_postfix": price_postfix,
                "surface_area": surface_area,
                "number_of_rooms": number_of_rooms,
                "interior": interior,
                "date": date,
                "url": url,
                "email_sent": False
            },
            "date" : date # easier for sorting by date
        }