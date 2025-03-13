import scrapy


class OlxSiteScraperSpider(scrapy.Spider):
    name = "olx_site_scraper"
    allowed_domains = ["www.olx.pl"]
    start_urls = ["https://www.olx.pl/nieruchomosci/mieszkania/"]

    def parse(self, response):
        pass
