# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class OlxScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        price_value = adapter.get('price')
        price_value = self.replace_value(price_value)
        adapter['price'] = price_value

        price_per_m_value = adapter.get('price_per_m2')
        price_per_m_value = self.replace_value(price_per_m_value)
        adapter['price_per_m2'] = price_per_m_value

        meters_value = adapter.get('meters')
        meters_value = self.replace_value(meters_value)
        adapter['meters'] = meters_value

        rooms_value = str(adapter.get('rooms'))
        rooms_value = self.replace_value(rooms_value)
        adapter['rooms'] = rooms_value

        rent_value = adapter.get('rent')
        rent_value = self.replace_value(rent_value)
        adapter['rent'] = rent_value

        location = adapter.get('location')
        street, city, state = self.parse_location(location)
        adapter['street'] = street
        adapter['city'] = city
        adapter['state'] = state

        floor = adapter.get('floor')
        floor, floor_max = self.parse_floor(floor=floor)
        adapter['floor'] = floor
        adapter['total_floors'] = floor_max

        heating = adapter.get('heating')
        heating = self.parse_heating(heating=heating)
        adapter['heating'] = heating

        # elevator_value = adapter.get('elevator')
        # elevator_value = self.replace_elevator(elevator_value)
        # adapter['elevator'] = elevator_value

        return item

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
        if 'ul' in splitted_locations[0] or splitted_locations[0].endswith('a') or splitted_locations[0].endswith('skiej'):
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


