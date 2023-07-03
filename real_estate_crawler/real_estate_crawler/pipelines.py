# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import googlemaps
import os
from dotenv import load_dotenv
import codecs

class RealEstateCrawlerPipeline:
    load_dotenv()
    gmaps = googlemaps.Client(key=os.getenv("GEOCODING_KEY"))

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.lowercase(adapter)
        self.decode_address(adapter)
        self.geocoding_active(adapter)

        return item

    def lowercase(self, adapter):   
        value = adapter.get('type')
        adapter['type'] = value.lower()

    def decode_address(self, adapter):
        adapter['address'] = adapter.get('address').encode('latin-1').decode('unicode_escape')

    def geocoding(self, adapter):
        if adapter.get('lat') == 'null':
            geocode = self.gmaps.geocode(adapter.get('address'))

            if geocode:
                result = geocode[0]['geometry']['location']
                adapter['lat'] = result['lat']
                adapter['lng'] = result['lng']
            else:
                adapter['lat'] = "erro"
                adapter['lng'] = "erro"


    def geocoding_active(self, adapter):
        env_geolocation = os.getenv("GEOCODING_ACTIVE")
        if env_geolocation:
            self.geocoding(adapter)