import scrapy
from olx_scraper.items import ApartmentItems
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OlxSiteScraperSpider(scrapy.Spider):
    name = "olx_site_scraper"
    allowed_domains = ["www.otodom.pl"]
    # start_urls = ["https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?viewType=listing"]

    custom_settings = {
        'FEEDS' :   {
            'apps_data.json'    :   {'format':'json', 'overwrite':True},
        }
    }

    def start_requests(self):
        url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?viewType=listing"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=5, meta={'use_selenium': True})

    def parse(self, response):
        # listing_grid = response.css('div[data-testid="listing-grid"]')
        # appartaments = listing_grid.css('div[data-cy="l-card"] > div > div > div + div')

        driver = response.request.meta.get('driver', None)

        try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-cy="new-element-after-scroll"]'))
                )

                navbar = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="search-list-pagination"]')
                print("✅ Navbar znaleziony po przewinięciu:", navbar.text)
        
        except Exception as e:
            print("Navbar nieznaleziony.", e)

        apartments = response.css('div[data-cy="search.listing.organic"] > span + ul > li')
        for apartment in apartments:
            relative_url = apartment.css('div + div > a::attr(href)').get()
            if relative_url:
                apartment_url = "https://www.otodom.pl/" + relative_url
                yield SeleniumRequest(
                    url = apartment_url,
                    callback = self.parse_apartment_site,
                    wait_time=2,
                )
        

            

    def parse_apartment_site(self, response):
        apartmentItems = ApartmentItems()

        # Items assigment:
        apartmentItems['title']                 = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h1::text").get()
        apartmentItems['location']              = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > a::text").get()
        apartmentItems['price']                 = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) strong::text").get()
        apartmentItems['price_per_m2']          = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div::text").get()
        apartmentItems['meters']                = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > button:nth-of-type(1) > div:nth-of-type(2)::text").get()
        apartmentItems['rooms']                 = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > button:nth-of-type(2) > div:nth-of-type(2)::text").get()
        
        apartmentItems['heating']               = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(2)::text").get()
        apartmentItems['floor']                 = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(3) > p:nth-of-type(2)::text").get()
        apartmentItems['rent']                  = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(5) > p:nth-of-type(2)::text").get()
        apartmentItems['finish_level']          = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(7) > p:nth-of-type(2)::text").get()
        apartmentItems['market_type']           = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(9) > p:nth-of-type(2)::text").get()
        apartmentItems['form_of_ownership']     = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(11) > p:nth-of-type(2)::text").get()
        apartmentItems['type_of_advertiser']    = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(15) > p:nth-of-type(2)::text").get()
        apartmentItems['additional_info']       = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(17) > p:nth-of-type(2) span::text").getall()

        # apartmentItems['elevator']              = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(1) > p:nth-of-type(2)::text").get()
        # apartmentItems['type_of_building']      = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(3) > p:nth-of-type(2)::text").get()
        # apartmentItems['building_material']     = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(5) > p:nth-of-type(2)::text").get()
        # apartmentItems['windows']               = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(7) > p:nth-of-type(2)::text").get()
        # apartmentItems['energy_certificate']    = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(9) > p:nth-of-type(2)::text").get()

        # apartmentItems['equipment']             = response.css("main > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(2) > div  p:nth-of-type(2)::text").get()

        yield apartmentItems