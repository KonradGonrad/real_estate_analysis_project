import scrapy
from olx_scraper.items import ApartmentItems
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

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
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=2)

    def parse(self, response):
        # listing_grid = response.css('div[data-testid="listing-grid"]')
        # appartaments = listing_grid.css('div[data-cy="l-card"] > div > div > div + div')
        page_index = response.meta.get('page_index', 2)
        driver = response.meta.get('driver')

        if driver is None:
             print("No driver found. Initializing one.")
             driver = webdriver.Chrome()
             driver.get(response.url)
        
        try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="navigation"]'))
                )

                navbar = driver.find_element(By.CSS_SELECTOR, 'div[role="navigation"]')
                print("✅ Navbar found after scrolling down", navbar.text)

                try:
                    next_page = navbar.find_element(By.CSS_SELECTOR, 'div > ul li[title="Go to next Page"]')
                    print("Next page is avaible")

                    page_index += 1
                    next_page_url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?viewType=listing&page={page_index}"
                except Exception as e:
                     print("Next page is not avaible")
                     
        
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
                    meta={'apartment_url': apartment_url}
                )

        if next_page is not None:
             yield SeleniumRequest(
                  url = next_page_url,
                  callback = self.parse,
                  wait_time=2,
                  meta={'driver': driver, 'page_index': page_index}
             )
        

            

    def parse_apartment_site(self, response):
        app_link = response.meta["apartment_url"]
        apartmentItems = ApartmentItems()

        # Different divs placement on sub_sites
        div_count, idx = len(response.xpath("//main/div")), 2
        if div_count != 3:
             idx = div_count - 1
             


        # Items assigment:       
        apartmentItems['div_count']             = div_count
        apartmentItems['link']                  = app_link      
        apartmentItems['title']                 = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(1) > h1::text").get()
        apartmentItems['location']              = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > a::text").get()
        apartmentItems['price']                 = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) strong::text").get()
        apartmentItems['price_per_m2']          = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div::text").get()
        apartmentItems['meters']                = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > button:nth-of-type(1) > div:nth-of-type(2)::text").get()
        apartmentItems['rooms']                 = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > button:nth-of-type(2) > div:nth-of-type(2)::text").get()
        
        apartmentItems['heating']               = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > p:nth-of-type(2)::text").get()
        apartmentItems['floor']                 = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(3) > p:nth-of-type(2)::text").get()
        apartmentItems['rent']                  = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(5) > p:nth-of-type(2)::text").get()
        apartmentItems['finish_level']          = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(7) > p:nth-of-type(2)::text").get()
        apartmentItems['market_type']           = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(9) > p:nth-of-type(2)::text").get()
        apartmentItems['form_of_ownership']     = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(11) > p:nth-of-type(2)::text").get()
        apartmentItems['type_of_advertiser']    = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(15) > p:nth-of-type(2)::text").get()
        apartmentItems['additional_info']       = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(17) > p:nth-of-type(2) span::text").getall()

        # Elevator error, cos its getting also year of building -> to repair
        apartmentItems['elevator']              = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(1) > p:nth-of-type(2)::text").get()
        apartmentItems['type_of_building']      = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(3) > p:nth-of-type(2)::text").get()
        apartmentItems['building_material']     = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(5) > p:nth-of-type(2)::text").get()
        apartmentItems['windows']               = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(7) > p:nth-of-type(2)::text").get()
        apartmentItems['energy_certificate']    = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(1) > div > div:nth-of-type(9) > p:nth-of-type(2)::text").get()

        apartmentItems['equipment']             = response.css(f"main > div:nth-of-type({idx}) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div[hidden]:nth-of-type(2) > div  p:nth-of-type(2)::text").get()

        yield apartmentItems