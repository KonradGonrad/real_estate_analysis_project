from my_data import *
DATABASE_NAME = DATABASE_NAME
DATABASE_PASSWORD = DATABASE_PASSWORD
DATABASE_HOST = DATABASE_HOST
DATABASE_USER = DATABASE_USER


DATABASE_LISTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS Listings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    link VARCHAR(255) NOT NULL,
    type_of_advertiser INT,
    marketplace INT
)
"""

DATABASE_LOCATION_TABLE = """
CREATE TABLE IF NOT EXISTS Location(
    id INT PRIMARY KEY,
    street VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    FOREIGN KEY (id) REFERENCES Listings(id) ON DELETE CASCADE 
)
"""

DATABASE_PRICES_TABLE = """
CREATE TABLE IF NOT EXISTS Prices(
    id INT PRIMARY KEY,
    total_cost FLOAT,
    cost_per_m2 FLOAT,
    rent FLOAT,
    FOREIGN KEY (id) REFERENCES Listings(id) ON DELETE CASCADE 
)
"""

DATABASE_BUILDING_INFO_TABLE = """
CREATE TABLE IF NOT EXISTS Building_informations(
    id INT PRIMARY KEY,
    heating INT,
    max_floor INT,
    finish_level INT,
    year_of_building INT,
    type_of_building INT,
    elevator INT,
    building_material INT,
    windows_material INT,
    closed_area INT,
    monitoring_or_security INT,
    FOREIGN KEY (id) REFERENCES Listings(id) ON DELETE CASCADE 
)
"""

DATABASE_APARTMENT_INFO_TABLE = """
CREATE TABLE IF NOT EXISTS Apartment_informations(
    id INT PRIMARY KEY,
    meters FLOAT,
    rooms INT,
    floor INT,
    balcony INT,
    garage INT,
    garden INT,
    patio INT,
    separate_kitchen INT,
    basement INT,
    utility_room INT,
    FOREIGN KEY (id) REFERENCES Listings(id) ON DELETE CASCADE 
)
"""

DATABASE_EQUIPMENT_TABLE = """
CREATE TABLE IF NOT EXISTS Equipment(
    id INT PRIMARY KEY,
    furniture INT,
    air_conditioning INT,
    internet INT,
    entryphone INT,
    stove INT,
    alarm_system INT,
    oven INT,
    tv INT,
    washing_machine INT,
    cable_tv INT,
    dishwasher INT,
    fridge INT,
    phone INT,
    anti_burglary_doors_or_windows INT,
    anti_burglary_blinds INT,
    FOREIGN KEY (id) REFERENCES Listings(id) ON DELETE CASCADE 
)
"""

def LISTINGS_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Listings (link, type_of_advertiser, marketplace)
    VALUES (%s, %s, %s)
    """
    DATA = (VALUES['link'], VALUES['type_of_advertiser'], VALUES['market_type'])

    return COMMAND, DATA

def LOCATION_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Location (id, street, city, state)
    VALUES (%s, %s, %s, %s)
    """
    DATA = (VALUES['listing_id'], VALUES['street'], VALUES['city'], VALUES['state'])
    return COMMAND, DATA

def PRICES_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Prices (id, total_cost, cost_per_m2, rent)
    VALUES (%s, %s, %s, %s)
    """
    DATA = (VALUES['listing_id'], VALUES['price'], VALUES['price_per_m2'], VALUES['rent'])
    return COMMAND, DATA

def BUILDING_INFO_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Building_informations (id, heating, max_floor, finish_level, year_of_building, type_of_building, elevator, building_material, windows_material, closed_area, monitoring_or_security)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    DATA = (VALUES['listing_id'], VALUES['heating'], VALUES['max_floor'], VALUES['finish_level'], VALUES['year_of_building'], VALUES['type_of_building'], VALUES['elevator'], VALUES['building_material'], VALUES['windows_material'], VALUES['closed_area'], VALUES['monitoring_or_security'])
    return COMMAND, DATA

def APARTMENT_INFO_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Apartment_informations (id, meters, rooms, floor, balcony, garage, garden, patio, separate_kitchen, basement, utility_room)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    DATA = (VALUES['listing_id'], VALUES['meters'], VALUES['rooms'], VALUES['floor'], VALUES['balcony'], VALUES['garage'], VALUES['garden'], VALUES['patio'], VALUES['separate_kitchen'], VALUES['basement'], VALUES['utility_room'])
    return COMMAND, DATA

def EQUIPMENT_TABLE_INSERT(VALUES: dict):
    COMMAND = """
    INSERT INTO Equipment (id, furniture, air_conditioning, internet, entryphone, stove, alarm_system, oven, tv, washing_machine, cable_tv, dishwasher, fridge, phone, anti_burglary_doors_or_windows, anti_burglary_blinds)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    DATA = (VALUES['listing_id'], VALUES['furniture'], VALUES['air_conditioning'], VALUES['internet'], VALUES['entryphone'], VALUES['stove'], VALUES['alarm_system'], VALUES['oven'], VALUES['tv'], VALUES['washing_machine'], VALUES['cable_tv'], VALUES['dishwasher'], VALUES['fridge'], VALUES['phone'], VALUES['anti_burglary_doors_windows'], VALUES['anti_burglary_blinds'])
    return COMMAND, DATA