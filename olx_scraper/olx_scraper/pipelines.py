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
        adapter['price'] = float(price_value)

        price_per_m_value = adapter.get('price_per_m2')
        price_per_m_value = self.replace_value(price_per_m_value)
        adapter['price_per_m2'] = float(price_per_m_value)

        meters_value = adapter.get('meters')
        meters_value = self.replace_value(meters_value)
        adapter['meters'] = float(meters_value)

        rooms_value = str(adapter.get('rooms'))
        rooms_value = self.replace_value(rooms_value)
        adapter['rooms'] = float(rooms_value)

        rent_value = adapter.get('rent')
        rent_value = self.replace_value(rent_value)
        adapter['rent'] = float(rent_value)

        # elevator_value = adapter.get('elevator')
        # elevator_value = self.replace_elevator(elevator_value)
        # adapter['elevator'] = elevator_value

        return item

    @staticmethod
    def replace_value(x):
        if not isinstance(x, str):
            return x

        replace_values = ['zł/m²', 'zł', 'm²', " ", 'pokój', 'pokoje'] 
        for replace_value in replace_values:
            if replace_value in x:
                x = x.replace(replace_value, "")
        return x
    
    @staticmethod
    def replace_elevator(x: str):
        x = 1 if x =='tak' else 0

        return x
