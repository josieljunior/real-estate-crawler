import json
import scrapy

from real_estate_crawler.items import RealEstateCrawlerItem
from real_estate_crawler.spiders import initLopes

PAGE_SIZE = 23

class LopesSpider(initLopes):
    name = "lopes"
    allowed_domains = ["lopes.com.br"]

    start_url = 'https://apis.lopes.com.br/portal-home/v2/search/cache/sale/br/sp/sao-paulo?' \
                'score.boost.product.address.city=São Paulo' \
                '&placeId=ChIJ0WGkg4FEzpQRrlsz_whLqZs' \
                '&isGeolocation=true' \
                '&page={previus}' \
                '&linesPerPage={size}' \
                '&fieldScore=new' \
                '&isFeature=false' \
                '&isToSearchWithAddress=false' \
                '&isToRandom=false' \
                '&isToSearchWithAddressOfPlaces=false'
    
    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, previus=(page - 1) * PAGE_SIZE)
            yield scrapy.Request(url=req_url)
            page += 1


    def parse(self, response):
        conteudo_bytes = response.body
        conteudo_string = conteudo_bytes.decode('utf-8')
        json_response = json.loads(conteudo_string)

        for item in json_response['products']['content']:
            yield RealEstateCrawlerItem(
                crawler         =self.name,
                link            =self.get_link(item),
                address         =self.mount_address(item),
                price           =self.get_price(item),
                area            =self.get_area(item['attributes']),
                bathrooms       =self.get_bathrooms(item['attributes']),
                bedrooms        =self.get_bedrooms(item['attributes']),
                parking_spaces  =self.get_parking_lots(item['attributes']),
                lat             =item['lat'],
                lng             =item['lng'],
                type            =item['type'],
            )

    def get_link(self, item):
        return "lopes.com.br/imovel/" + item['id']
    
    def mount_address(self, item):
        return item['street'] + " - " + item['neighborhood']
    
    def get_price(self, item):
        return item['priceFormat'].replace("R$", "").strip()
    
    def get_area(self, attributes):
        for attr in attributes:
            if attr["type"] == "area_attr":
                return attr["value"].replace("m²", "").strip()
        return None

    def get_bedrooms(self, attributes):
        for attr in attributes:
            if attr["type"] == "bedroom_attr":
                return attr["value"]
        return None

    def get_bathrooms(self, attributes):
        for attr in attributes:
            if attr["type"] == "bathroom_attr":
                return attr["value"]
        return None

    def get_parking_lots(self, attributes):
        for attr in attributes:
            if attr["type"] == "parking_lots_attr":
                return attr["value"]
        return None