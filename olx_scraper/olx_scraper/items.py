# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApartmentItems(scrapy.Item):
    # define the fields for your item here like:
    div_count = scrapy.Field()
    link = scrapy.Field()

    title = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    price_per_m2 = scrapy.Field()
    meters = scrapy.Field()
    rooms = scrapy.Field()
    heating = scrapy.Field()
    floor = scrapy.Field()
    rent = scrapy.Field()
    finish_level = scrapy.Field()
    market_type = scrapy.Field()
    form_of_ownership = scrapy.Field()
    type_of_advertiser = scrapy.Field()
    additional_info = scrapy.Field()
    elevator = scrapy.Field()
    type_of_building = scrapy.Field()
    building_material = scrapy.Field()
    windows = scrapy.Field()
    energy_certificate = scrapy.Field()
    equipment = scrapy.Field()