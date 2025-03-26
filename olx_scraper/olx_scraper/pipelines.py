from typing import List, Dict
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import Result
from .settings import SCRAP_SETTINGS


class OlxScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        result = Result()

        # link
        if SCRAP_SETTINGS['SCRAP_LINK']:
            result['link'] = adapter.get('link')

        # price
        if SCRAP_SETTINGS['SCRAP_PRICE']:
            price_value = adapter.get('price')
            price_value = self.replace_value(price_value)
            result['price'] = price_value

            price_per_m_value = adapter.get('price_per_m2')
            price_per_m_value = self.replace_value(price_per_m_value)
            result['price_per_m2'] = price_per_m_value

            rent_value = adapter.get('rent')
            rent_value = self.replace_value(rent_value)
            result['rent'] = rent_value

        # building info
        if SCRAP_SETTINGS['SCRAP_BUILDING_INFO']:
            meters_value = adapter.get('meters')
            meters_value = self.replace_value(meters_value)
            result['meters'] = meters_value

            rooms_value = str(adapter.get('rooms'))
            rooms_value = self.replace_value(rooms_value)
            result['rooms'] = rooms_value

            heating = adapter.get('heating')
            heating = self.parse_heating(heating=heating)
            result['heating'] = heating

            floor = adapter.get('floor')
            floor, floor_max = self.parse_floor(floor=floor)
            result['floor'] = floor
            result['max_floor'] = floor_max

            finish_level = adapter.get("finish_level")
            finish_level = self.parse_finish_level(finish_level)
            result['finish_level'] = finish_level

        # location
        if SCRAP_SETTINGS['SCRAP_LOCATION']:
            location = adapter.get('location')
            street, city, state = self.parse_location(location)
            result['street'] = street
            result['city'] = city
            result['state'] = state

        # additional info
        if SCRAP_SETTINGS['SCRAP_ADD_INFO']:
            additional_info = adapter.get('additional_info')
            result.update(self.parse_additional_info(additional_info))

        # equipment
        if SCRAP_SETTINGS['SCRAP_EQUIPMENT']:
            equipment = adapter.get('equipment')
            # result['anti_burglary_doors_windows'], result['anti_burglary_blinds'], result['furniture'], result['air_conditioning'], result['internet'], result['entryphone'], result['stove'], result['alarm_system'] = self.parse_equipment(equipment)
            result.update(self.parse_equipment(equipment))


        # elevator_value = adapter.get('elevator')
        # elevator_value = self.replace_elevator(elevator_value)
        # adapter['elevator'] = elevator_value
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
    def replace_elevator(x: str):
        x = 1 if x =='tak' else 0

        return x
    
    @staticmethod
    def parse_location(location: str):
        splitted_locations = location.split(",")
        splitted_locations = [item.strip() for item in splitted_locations]
        
        # Street
        if 'ul' in splitted_locations[0] or splitted_locations[0].endswith(('a', 'skiej', 'o')) :
            street = "ul. "+ splitted_locations[0] if "ul" not in splitted_locations[0] else splitted_locations[0]
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
    

    # I'll split all provided below parsing functions into one or at least I'll use other method than case
    @staticmethod
    def parse_heating(heating: str):
        """
        Added this function to change strings into binary notation, for better performance of model.
        0 = brak
        1 = miejskie
        2 = gazowe
        3 = inne
        4 = kotłownia
        5 = elektryczne
        """
        match heating:
            case 'brak informacji':
                return 0
            case 'miejskie':
                return 1
            case 'gazowe':
                return 2
            case 'inne':
                return 3
            case 'kotłownia':
                return 4
            case 'elektryczne':
                return 5

    @staticmethod
    def parse_finish_level(finish_level: str):
        """
        -||-
        0 = brak
        1 = do wykończenia
        2 = do zamieszkania
        3 = do remontu
        """
        match finish_level:
            case "brak informacji":
                return 0
            case "do wykończenia":
                return 1
            case "do zamieszkania":
                return 2
            case "do remontu":
                return 3

    @staticmethod
    def parse_market_type(market_type: str):
        """
        -||-
        1 = pierwotny
        2 = wtorny

        """
        match market_type:
            case "pierwotny":
                return 1
            case "wtorny":
                return 2

    @staticmethod
    def parse_type_of_advertiser(advertiser: str):
        """
        -||-
        deweloper = 1
        biuro nieruchomosci = 2
        prywatny = 3
        """
        match advertiser:
            case 'deweloper':
                return 1
            case 'biuro nieruchomości':
                return 2
            case 'prywatny':
                return 3
            
    @staticmethod
    def parse_additional_info(additional_info: List) -> Dict:
        """
        returns informations from additional info scraped in order:
        balcony, garage, utility_room, basement, separete_kitchen, garden, patio, 
        """
        additional_info = [info.strip() for info in additional_info if isinstance(info, str)]
        balcony = 1 if "balkon" in additional_info else 0
        garage = 1 if "garaż/miejsce parkingowe" in additional_info else 0
        utility_room = 1 if "pom. użytkowe" in additional_info else 0
        basement = 1 if "piwnica" in additional_info else 0
        separate_kitchen = 1 if "oddzielna kuchnia" in additional_info else 0
        garden = 1 if "ogródek" in additional_info else 0
        patio = 1 if "taras" in additional_info else  0

        return {"balcony": balcony,
                "garage": garage, 
                "utility_room": utility_room, 
                "basement":basement, 
                "separate_kitchen" : separate_kitchen, 
                "garden": garden, 
                "patio": patio}
    
    @staticmethod
    def parse_equipment(equipment: List) -> Dict:
        """
        returns int 1 or 0 depends on scraped equipment in order:
        anti-burglary doors and windows, anti-burglary blinds, furniture, air_conditioning, internet, entryphone, stove, alarm system
        """
        equipment = [eq.strip() for eq in equipment if isinstance(eq, str)]
        anti_burglary_doors_windows = 1 if "drzwi / okna antywłamaniowe" in equipment else 0 
        furniture = 1 if "meble" in equipment else 0 
        air_conditioning = 1 if "klimatyzacja" in equipment else 0 
        internet = 1 if "internet" in equipment else 0 
        entryphone= 1 if "domofon / wideofon" in equipment else 0 
        anti_burglary_blinds = 1 if "rolety antywłamaniowe" in equipment else 0
        stove = 1 if "kuchenka" in equipment else 0
        alarm_system = 1 if "system alarmowy" in equipment else 0

        return {"anti_burglary_doors_windows": anti_burglary_doors_windows,
                "anti_burglary_blinds": anti_burglary_blinds,
                "furniture": furniture,
                "air_conditioning": air_conditioning,
                "internet": internet,
                "entryphone": entryphone,
                "stove": stove,
                "alarm_system": alarm_system}