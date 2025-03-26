from shutil import which
from olx_scraper.api_keys import MYSCRAPEOPS_API_KEY 
# from olx_scraper.api_keys_example import MYSCRAPEOPS_API_KEY 

# Scrapy settings for olx_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "olx_scraper"

SPIDER_MODULES = ["olx_scraper.spiders"]
NEWSPIDER_MODULE = "olx_scraper.spiders"

DOWNLOAD_DELAY = 1

SCRAPEOPS_API_KEY = MYSCRAPEOPS_API_KEY
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = "/opt/homebrew/bin/chromedriver" 
SELENIUM_DRIVER_ARGUMENTS = ['--headless']
SELENIUM_BROWSER_EXECUTABLE_PATH = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'

FEEDS = {
    'apps_data.json'    :   {'format':'json'}
}

# Settings about results

SCRAP_PRICE = False
SCRAP_BUILDING_INFO = True
SCRAP_LOCATION = True
SCRAP_ADD_INFO = True
SCRAP_EQUIPMENT = True
SCRAP_SELL_INFO = True
SCRAP_OTHER = True
SCRAP_LINK = True

SCRAP_SETTINGS = {"SCRAP_PRICE": SCRAP_PRICE,
                  "SCRAP_BUILDING_INFO": SCRAP_BUILDING_INFO,
                  "SCRAP_LOCATION": SCRAP_LOCATION,
                  "SCRAP_ADD_INFO": SCRAP_ADD_INFO,
                  "SCRAP_EQUIPMENT": SCRAP_EQUIPMENT,
                  "SCRAP_SELL_INFO": SCRAP_SELL_INFO,
                  "SCRAP_OTHER": SCRAP_OTHER,
                  "SCRAP_LINK": SCRAP_LINK}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "olx_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "olx_scraper.middlewares.OlxScraperSpiderMiddleware": None,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'olx_scraper.middlewares.SeleniumMiddleware': 200,
    "olx_scraper.middlewares.OlxScraperFakeBrowserHeaders": 404,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "olx_scraper.pipelines.OlxScraperPipeline": 600,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
