from typing import List, Dict

loc_1 = "ul. Natalińska, Otrębusy, Brwinów, pruszkowski, mazowieckie"
loc_2 =  "Heleny Żybutowskiej, Stargard, stargardzki, zachodniopomorskie"
loc_3 = "ul. Wierzbowa, Porosły, Choroszcz, białostocki, podlaskie"
loc_4 = "ul. Armii Krajowej, Sobótka, Sobótka, wrocławski, dolnośląskie"
loc_5 = "Kiełczów, Długołęka, wrocławski, dolnośląskie"
loc_6 = "ul. Chorwacka, Różanka, Psie Pole, Wrocław, dolnośląskie"
loc_7 = "ul. Kolorowa, Ustka, słupski, pomorskie"
loc_8 = "Krasowa, Krzeszowice, Krzeszowice, krakowski, małopolskie"
loc_9 = "ul. Graniczna 1, Ustroń, cieszyński, śląskie"

locations = [loc_1, loc_2, loc_3, loc_4, loc_5, loc_6, loc_7, loc_8, loc_9]

def parse_location(location: str):
    splitted_locations = location.split(",")
    splitted_locations = [item.strip() for item in splitted_locations]
    
    # Street
    if 'ul' in splitted_locations[0] or splitted_locations[0].endswith('a') or splitted_locations[0].endswith('skiej'):
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





for location in locations:
    print(parse_location(location=location))


add_1 = ["balkon", " garaż/miejsce parkingowe", " pom. użytkowe"]
add_2 = ["piwnica", " oddzielna kuchnia"]
add_3 = ["ogródek", " taras", " garaż/miejsce parkingowe"]
add_4 = ["garaż/miejsce parkingowe", " oddzielna kuchnia"]
add_5 = [None]

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

balcony, garage, utility_room, basement, separate_kitchen, garden, patio = parse_additional_info(add_5)

print(f"""Balcony: {balcony},
        \nGarage; {garage},
        \nUtility room: {utility_room}, 
        \nBasement: {basement}, 
        \nSeperate kitchen: {separate_kitchen},
        \nGarden: {garden},
        \nPatio: {patio}""")

eq_1 = ["drzwi / okna antywłamaniowe"]
eq_2 = ["meble"]
eq_3 = ["klimatyzacja"]
eq_4 = ["internet"]
eq_5 = ["domofon / wideofon"]
eq_6 = ["rolety antywłamaniowe"]
eq_7 = ["kuchenka"]
eq_8 = ["system alarmowy"]
eq_9 = [""]
eq_10 = [None]

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

anti_burglary_doors_windows, anti_burglary_blinds, furniture, air_conditioning, internet, entryphone, stove, alarm_system = parse_equipment(eq_10)

print(f"""anti_burglary_doors_windows: {anti_burglary_doors_windows},
        \nanti_burglary_blinds; {anti_burglary_blinds},
        \nfurniture: {furniture}, 
        \nair_conditioning: {air_conditioning}, 
        \ninternet: {internet},
        \nentryphone: {entryphone},
        \nstove: {stove}
        \nalarm_system: {alarm_system}""")


SCRAP_PRICE = True
SCRAP_BUILDING_INFO = True
SCRAP_LOCATION = True
SCRAP_ADD_INFO = True
SCRAP_EQUIPMENT = True
SCRAP_SELL_INFO = True
SCRAP_OTHER = True

SCRAP_SETTINGS = {"SCRAP_PRICE": SCRAP_PRICE,
                  "SCRAP_BUILDING_INFO": SCRAP_BUILDING_INFO,
                  "SCRAP_LOCATION": SCRAP_LOCATION,
                  "SCRAP_ADD_INFO": SCRAP_ADD_INFO,
                  "SCRAP_EQUIPMENT": SCRAP_EQUIPMENT,
                  "SCRAP_SELL_INFO": SCRAP_SELL_INFO,
                  "SCRAP_OTHER": SCRAP_OTHER}


print(SCRAP_SETTINGS["SCRAP_PRICE"])

x = [1, 2]
y = ["1", 3]
print(x + y)

eq_1 = ("domofon / wideofon", "telewizja kablowa", " internet", "system alarmowy")
eq_2 = ("zmywarka", " lodówka", " meble", " piekarnik", " kuchenka", " telewizor", " pralka", " klimatyzacja", "drzwi / okna antywłamaniowe", " domofon / wideofon", "telewizja kablowa", " internet", " telefon")
eq_3 = ("zmywarka", " lodówka", " meble", " piekarnik", " kuchenka", " telewizor", " pralka", "drzwi / okna antywłamaniowe", " domofon / wideofon", "telewizja kablowa", " internet")
eq_4 = ("zmywarka", " lodówka", " meble", " kuchenka", " telewizor", " pralka", "drzwi / okna antywłamaniowe", " domofon / wideofon", "telewizja kablowa", " internet")


eq = set(i.strip() for i in (eq_1 + eq_2 + eq_3 + eq_4))
print(eq, len(eq))