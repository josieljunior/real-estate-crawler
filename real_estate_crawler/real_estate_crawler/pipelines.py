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
        # self.decode_address(adapter)
        # self.geocoding(adapter)

        return item

    def lowercase(self, adapter):   
        value = adapter.get('type')
        adapter['type'] = value.lower()

    def decode_address(self, adapter):
        adapter['address'] = codecs.decode(adapter.get('address'), 'unicode_escape')

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
