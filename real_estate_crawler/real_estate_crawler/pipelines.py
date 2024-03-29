# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import googlemaps
import os
from dotenv import load_dotenv

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Property, Price
from .database import engine
import logging
from scrapy.exceptions import DropItem

class RealEstateCrawlerPipeline:
    REQUIRED_FIELDS = [
            'area',
            'type',
            'bedrooms',
            'bathrooms',
            'parking_spaces',
            'price',
            'address'
        ]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.check_required_fields(adapter)
        self.decode_address(adapter)
        self.get_type(adapter)
        self.format_number(adapter)

        return item

    def decode_address(self, adapter):
        adapter['address'] = adapter.get('address').encode('latin-1').decode('unicode_escape')

    def get_type(self, adapter):
        type_mapping = {
            "casa": "home",
            "home": "home",
            "sobrado": "home",
            "two_story_house": "home",
            "casa térrea": "home",
            "condomínio": "home",
            "apartamento": "apartment",
            "cobertura": "apartment",
            "penthouse": "apartment",
        }
        value_type = adapter.get('type').lower()
        adapter['type'] = type_mapping.get(value_type, value_type)
    
    def format_number(self, adapter):
        formatted_value = adapter.get('price').replace(".", "")
        adapter['price'] = int(formatted_value)

    def check_required_fields(self, adapter):
        missing_fields = [field for field in self.REQUIRED_FIELDS if not adapter.get(field)]
        if missing_fields:
            raise DropItem(f"Item missing required fields: {', '.join(missing_fields)}")

class SQLAlchemyPipeline:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        price_value = item.pop('price')
        session = self.Session()
        try:
            existing_property = session.query(Property).filter_by(link=item['link']).first()
            
            if existing_property:
                existing_price = existing_property.prices[-1] if existing_property.prices else None

                if existing_price and existing_price.price != float(price_value):
                    price_item = Price(price=price_value)
                    existing_property.prices.append(price_item)
                    session.add(price_item)
                    session.commit()
                else:
                    raise DropItem(f"Already exists link:{item['link']}")  
            else:
                self.geocoding_active(item)
                property_item = Property(**item)
                price_item = Price(price=price_value)
                property_item.prices.append(price_item)
                session.add(property_item)
                session.commit()
            session.close()
        except SQLAlchemyError as e:
            session.rollback()
            session.close()
            logging.error(f"Error saving item to the database: {e}")
        return item

    def geocoding(self, adapter):
        if adapter.get('lat') == 'null':
            geocode = self.gmaps.geocode(adapter.get('address'))

            if geocode:
                result = geocode[0]['geometry']['location']
                adapter['lat'] = result['lat']
                adapter['lng'] = result['lng']
            else:
                raise DropItem("Geolocation not found")


    def geocoding_active(self, item):
        load_dotenv()
        adapter = ItemAdapter(item)
        env_geolocation = os.getenv("GEOCODING_ACTIVE")
        
        if env_geolocation == 'true':
            self.gmaps = googlemaps.Client(key=os.getenv("GEOCODING_KEY"))
            self.geocoding(adapter)
        else:
            raise DropItem("Geolocation is null")
    