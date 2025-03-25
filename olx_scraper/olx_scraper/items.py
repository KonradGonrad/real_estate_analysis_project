# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from .settings import SCRAP_SETTINGS


class ApartmentItems(scrapy.Item):
    # define the fields for your item here like:
    # div_count = scrapy.Field()
    
    link = scrapy.Field()

    title = scrapy.Field()

    location = scrapy.Field()
    #From location:
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()

    price = scrapy.Field()
    price_per_m2 = scrapy.Field()
    meters = scrapy.Field()
    rooms = scrapy.Field()

    heating = scrapy.Field()
    floor = scrapy.Field()
    total_floors = scrapy.Field()
    rent = scrapy.Field()
    finish_level = scrapy.Field()
    market_type = scrapy.Field()
    form_of_ownership = scrapy.Field()
    type_of_advertiser = scrapy.Field()
    additional_info = scrapy.Field()

    #Building_and_materials
    # year_of_building = scrapy.Field()
    # elevator = scrapy.Field()
    # safety = scrapy.Field()

    # type_of_building = scrapy.Field()
    # building_material = scrapy.Field()
    # windows = scrapy.Field()
    # energy_certificate = scrapy.Field()
    equipment = scrapy.Field()


class Result(scrapy.Item):
    # price
    if SCRAP_SETTINGS["SCRAP_PRICE"]:
        price = scrapy.Field()
        price_per_m2 = scrapy.Field()
        rent = scrapy.Field()

    #building info
    if SCRAP_SETTINGS["SCRAP_BUILDING_INFO"]:
        meters = scrapy.Field()
        rooms = scrapy.Field()
        heating = scrapy.Field()
        floor = scrapy.Field()
        max_floor = scrapy.Field()
        finish_level = scrapy.Field()

    #location
    if SCRAP_SETTINGS["SCRAP_LOCATION"]:
        street = scrapy.Field()
        city = scrapy.Field()
        state = scrapy.Field()

    #additional info
    if SCRAP_SETTINGS["SCRAP_ADD_INFO"]:
        balcony = scrapy.Field()
        garage = scrapy.Field()
        utility_room = scrapy.Field()
        basement = scrapy.Field()
        separate_kitchen = scrapy.Field()
        patio = scrapy.Field()
        garden = scrapy.Field()

    #equipment
    if SCRAP_SETTINGS["SCRAP_EQUIPMENT"]:
        anti_burglary_doors_windows = scrapy.Field() 
        anti_burglary_blinds = scrapy.Field() 
        furniture = scrapy.Field() 
        air_conditioning = scrapy.Field() 
        internet = scrapy.Field() 
        entryphone = scrapy.Field()
        stove = scrapy.Field() 
        alarm_system = scrapy.Field() 

    #sell info
    if SCRAP_SETTINGS["SCRAP_SELL_INFO"]:
        type_of_advertiser = scrapy.Field()
        market_type = scrapy.Field()

    # other
    if SCRAP_SETTINGS["SCRAP_OTHER"]:
        link = scrapy.Field() 
