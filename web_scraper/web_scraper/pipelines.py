from typing import List, Dict
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import Result
from .settings import SCRAP_SETTINGS
from .settings import DATABASE_SETTINGS, DATABASE_CREATOR, DATABASE_INSERT



class WebScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        result = Result()

        # link
        if SCRAP_SETTINGS['SCRAP_LINK']:
            result['link'] = adapter.get('link')

        # price
        if SCRAP_SETTINGS['SCRAP_PRICE']:
            result['price'] = self.replace_value(adapter.get('price'))
            result['price_per_m2'] = self.replace_value(adapter.get('price_per_m2'))
            result['rent'] = self.replace_value(adapter.get('rent'))

        # building info
        if SCRAP_SETTINGS['SCRAP_BUILDING_INFO']:
            result['meters'] = self.replace_value(adapter.get('meters'))
            result['rooms'] = self.replace_value(str(adapter.get('rooms')))
            result['heating'] = self.parse_heating(heating=adapter.get('heating'))

            floor, floor_max = self.parse_floor(floor=adapter.get('floor'))
            result['floor'], result['max_floor'] = floor, floor_max

            result['finish_level'] = self.parse_finish_level(adapter.get("finish_level"))
            result.update(self.parse_building_and_materials(year_of_building=adapter.get('year_of_building'),
                                                            elevator=adapter.get('elevator'),
                                                            type_of_building=adapter.get('type_of_building'),
                                                            windows_material=adapter.get('windows_material'),
                                                            safety=adapter.get('safety')))

        # location
        if SCRAP_SETTINGS['SCRAP_LOCATION']:
            street, city, state = self.parse_location(adapter.get('location'))
            result['street'], result['city'], result['state'] = street, city, state

        # additional info
        if SCRAP_SETTINGS['SCRAP_ADD_INFO']:
            result.update(self.parse_additional_info(adapter.get('additional_info') or []))

        # equipment
        if SCRAP_SETTINGS['SCRAP_EQUIPMENT']:
            equipment_1, equipment_2 = adapter.get('equipment_1'), adapter.get('equipment_2')
            result.update(self.parse_equipment(equipment_1 + equipment_2))

        # sell info
        if SCRAP_SETTINGS['SCRAP_SELL_INFO']:
            result['type_of_advertiser'] = self.parse_type_of_advertiser(adapter.get('type_of_advertiser'))
            result['market_type'] = self.parse_market_type(adapter.get('market_type'))

        return result

    @staticmethod
    def replace_value(x):
        if not isinstance(x, str):
            return x

        replace_values = ['zł/m²', 'zł', 'm²', " ", 'pokój', 'pokoje', 'pokoi'] 
        for replace_value in replace_values:
            if replace_value in x:
                x = x.replace(replace_value, "")
        if x.replace(".", '').isdigit():
            return float(x)
        else:
            return None
    
    @staticmethod
    def parse_location(location: str):
        splitted_locations = location.split(",")
        splitted_locations = [item.strip() for item in splitted_locations]
        posses = ['ul.', 'al.', 'aleja', 'bulw.', 'bulwar', 'droga', 'trasa', 'most', 'trasa', 'gen.', 'marsz.', 'ks.', 'prof.', 'os.', 'osiedle']
        ends = ('a', 'skiej', 'o', 'ego', 'ej', 'y', 'ów')
        # Street
        if any(prefix in splitted_locations[0] for prefix in posses) or splitted_locations[0].endswith(ends) or bool(re.search(r'\d', splitted_locations[0])) :
            street = splitted_locations[0] 
        else:
            street = None
        
        # city
        if splitted_locations[-2].endswith('ki'):
            city = splitted_locations[0 if street == None else 1]
        else:
            city = splitted_locations[-2]

        # state
        state = splitted_locations[-1]

        return street, city, state
    
    @staticmethod
    def parse_floor(floor: str):
        if floor == 'brak informacji':
            return None, None
        floor_split = floor.replace(">", "").replace(" ", "").split("/")
        if floor_split[0] == 'parter':
            floor_split[0] = 1
        floor = float(floor_split[0])
        floor_max = float(floor_split[1]) if len(floor_split) > 1 else float(floor)

        return floor, floor_max
    
    @staticmethod
    def parse_heating(heating: str):
        heating_map = {
            "brak informacji": 0,
            "miejskie": 1,
            "gazowe": 2,
            "inne": 3,
            "kotłownia": 4,
            "elektryczne": 5
        }
        return heating_map[heating]

    @staticmethod
    def parse_finish_level(finish_level: str):
        finish_level_map ={
            "brak informacji": 0,
            "do wykończenia": 1,
            "do zamieszkania": 2,
            "do remontu": 3
        }
        return finish_level_map[finish_level]

    @staticmethod
    def parse_market_type(market_type: str):
        market_type_map = {
            'pierwotny': 1,
            'wtórny': 2
        }
        return market_type_map[market_type.strip()]

    @staticmethod
    def parse_type_of_advertiser(advertiser: str):
        type_of_advertiser_map = {
            'deweloper': 1,
            'biuro nieruchomości': 2,
            'prywatny': 3
        }
        return type_of_advertiser_map[advertiser.strip()]
            
    @staticmethod
    def parse_additional_info(additional_info: List) -> Dict:
        if not isinstance(additional_info, list):
            additional_info = []

        additional_info = [info.strip() for info in additional_info if isinstance(info, str)]

        return {"balcony": 1 if "balkon" in additional_info else 0,
                "garage": 1 if "garaż/miejsce parkingowe" in additional_info else 0,
                "utility_room": 1 if "pom. użytkowe" in additional_info else 0,
                "basement": 1 if "piwnica" in additional_info else 0, 
                "separate_kitchen" : 1 if "oddzielna kuchnia" in additional_info else 0, 
                "garden": 1 if "ogródek" in additional_info else 0,
                "patio": 1 if "taras" in additional_info else  0}
    
    @staticmethod
    def parse_equipment(equipment: List) -> Dict:
        equipment = [eq.strip() for eq in equipment if isinstance(eq, str)]
        return {"anti_burglary_doors_windows": 1 if "drzwi / okna antywłamaniowe" in equipment else 0 ,
                "anti_burglary_blinds": 1 if "rolety antywłamaniowe" in equipment else 0,
                "furniture": 1 if "meble" in equipment else 0,
                "air_conditioning": 1 if "klimatyzacja" in equipment else 0,
                "internet": 1 if "internet" in equipment else 0,
                "entryphone": 1 if "domofon / wideofon" in equipment else 0,
                "stove": 1 if "kuchenka" in equipment else 0,
                "alarm_system": 1 if "system alarmowy" in equipment else 0,
                "oven": 1 if "piekarnik" in equipment else 0,
                "tv": 1 if "telewizor" in equipment else 0 ,
                "washing_machine": 1 if "pralka" in equipment else 0, 
                "cable_tv": 1 if "telewizja kablowa" in equipment else 0,
                "dishwasher": 1 if "zmywarka" in equipment else 0,
                "fridge": 1 if "lodówka" in equipment else 0,
                "phone": 1 if "telefon" in equipment else 0,}
    
    @staticmethod
    def parse_building_and_materials(year_of_building = None,
                                 elevator = None,
                                 type_of_building = None,
                                 building_material = None,
                                 windows_material = None,
                                 safety = None):
    
        def parse_type_of_building(x):
            type_of_building_map = {
                None: 0,
                'kamienica': 1,
                'apartamentowiec': 2,
                'dom wolnostojący': 3,
                'blok': 4,
                'szeregowiec': 5
            }
            return type_of_building_map[type_of_building]
                
        def parse_building_material(x):
            building_material_map = {
                None: 0,
                'cegła': 1,
                'pustak': 2,
                'wielka płyta': 3,
                'silikat': 4,
                'żelbet': 5,
                'beton komórkowy': 6,
                'beton': 7,
                'inny': 8
            }
            return building_material_map[building_material]
            
        def parse_windows_material(x):
            windows_material_map = {
                None: 0,
                'plastikowe': 1,
                'drewniane': 2
            }
            return windows_material_map[windows_material]

        return {"year_of_building": int(year_of_building) if isinstance(year_of_building, str) else 0,
                "elevator": 1 if elevator == 'tak' else 0,
                "type_of_building": parse_type_of_building(type_of_building),
                "building_material": parse_building_material(building_material),
                'windows_material': parse_windows_material(windows_material),
                'monitoring_or_security': 1 if safety and 'monitoring / ochrona' in safety else 0,
                'closed_area': 1 if safety and 'teren zamknięty' in safety else 0 
                }

import mysql.connector  
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = DATABASE_SETTINGS['HOST'],
            user = DATABASE_SETTINGS['USER'],
            password = DATABASE_SETTINGS['PASSWORD'],
            database = DATABASE_SETTINGS['NAME']
        )

        self.cur = self.conn.cursor()

        # CREATING TABLES AND DATABASE STRUCTURE
        for table in DATABASE_CREATOR.values():
            self.cur.execute(table)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        COMMAND, DATA = DATABASE_INSERT['LISTING_INSERT'](adapter)
        self.cur.execute(COMMAND, DATA)

        listing_id = self.cur.lastrowid
        adapter['listing_id'] = listing_id

        for key, function in DATABASE_INSERT.items():
            if not DATABASE_INSERT['LISTING_INSERT']:
                COMMAND, DATA = function(adapter)
                self.cur.execute(COMMAND, DATA)

            self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close
