import pandas as pd
from sqlalchemy import create_engine
from web_scraper.web_scraper.my_data import *

engine = create_engine(f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

Listings = engine