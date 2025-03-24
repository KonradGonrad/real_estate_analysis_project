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
        street, city, state = self.split_location(location)
        adapter['street'] = street
        adapter['city'] = city
        adapter['state'] = state

        floor = adapter.get('floor')
        floor, floor_max = self.parse_floor(floor=floor)
        adapter['floor'] = floor
        adapter['total_floors'] = floor_max

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
        return x
    
    @staticmethod
    def replace_elevator(x: str):
        x = 1 if x =='tak' else 0

        return x
    
    @staticmethod
    def split_location(location: str):
        if not isinstance(location, str):
            return None, None, None
        
        parts = [p.strip() for p in location.split(",")]
        street = parts[0] if len(parts) > 0 else None
        city = parts[-2] if len(parts) > 1 else None
        state = parts[-1] if len(parts) > 2 else None
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

