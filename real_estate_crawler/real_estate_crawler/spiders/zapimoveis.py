import json
import scrapy

from real_estate_crawler.items import RealEstateCrawlerItem
from real_estate_crawler.spiders import initZapImoveis

PAGE_SIZE = 100

class ZapimoveisSpider(initZapImoveis):
    name = "zapimoveis"
    allowed_domains = ["zapimoveis.com.br"]

    start_url = 'https://glue-api.zapimoveis.com.br/v2/listings?' \
                'categoryPage=RESULT' \
                '&business=SALE' \
                '&listingType=USED' \
                '&parentId=null' \
                '&unitTypes=APARTMENT,HOME' \
                '&unitSubTypes=UnitSubType_NONE,DUPLEX,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,KITNET|TWO_STORY_HOUSE' \
                '&usageTypes=RESIDENTIAL,RESIDENTIAL,RESIDENTIAL' \
                '&unitTypesV3=APARTMENT,HOME,TWO_STORY_HOUSE' \
                '&addressCity=São Paulo' \
                '&addressZone=' \
                '&addressStreet=' \
                '&addressLocationId=BR>Sao Paulo>NULL>Sao Paulo' \
                '&addressState=São Paulo' \
                '&addressNeighborhood=' \
                '&addressPointLat=-23.555771' \
                '&addressPointLon=-46.639557' \
                '&size={size}' \
                '&from={previus}' \
                '&includeFields=search(result(listings(listing(listingsCount,sourceId,displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status,priceSuggestion,contractType),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,createdDate,minisite,tier),medias,accountLink,link)),totalCount),page,facets,fullUriFragments,developments(search(result(listings(listing(listingsCount,sourceId,displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status,priceSuggestion,contractType),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,createdDate,minisite,tier),medias,accountLink,link)),totalCount)),superPremium(search(result(listings(listing(listingsCount,sourceId,displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,stamps,createdAt,floors,unitTypes,nonActivationReason,providerId,propertyType,unitSubTypes,unitsOnTheFloor,legacyId,id,portal,unitFloor,parkingSpaces,updatedAt,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,advertiserContact,whatsappNumber,bedrooms,acceptExchange,pricingInfos,showPrice,resale,buildings,capacityLimit,status,priceSuggestion,contractType),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,legacyZapId,createdDate,minisite,tier),medias,accountLink,link)),totalCount)),schema' \
                '&developmentsSize=3' \
                '&superPremiumSize=3' \
                '&levels=CITY' \
                '&ref=' \
                '&addressType=city' \
                
    headers = {
        'x-domain': 'www.zapimoveis.com.br'
    }

    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, previus=(page - 1) * PAGE_SIZE)
            yield scrapy.Request(url=req_url, headers=self.headers)
            page += 1


    def parse(self, response):
        json_response = response.json()

        for result in json_response['search']['result']['listings']:
            json_item = result['listing']
            items = RealEstateCrawlerItem()

            items['lat'] = self.get_geocode(json_item, 'lat')
            items['lng'] = self.get_geocode(json_item, 'lon')
            items['area'] = json_item['usableAreas'][0]
            items['type'] = json_item['unitTypes'][0]
            items['bedrooms'] = json_item['bedrooms'][0]
            items['bathrooms'] = json_item['bathrooms'][0]
            items['parking_spaces'] = self.get_parking_space(json_item)
            items['price'] = json_item['pricingInfos'][0]['price']
            items['address'] = self.get_address(result)

            items['crawler'] = self.name
            items['link'] = self.mount_link(result)
            
            yield items

            

    def get_geocode(self, json_item, key):
        if 'address' in json_item and 'point' in json_item['address']:
            return json_item['address']['point'][key]
        else:
            return "null"
            
    def get_parking_space(self, json_item):
        if 'parkingSpaces' in json_item and len(json_item['parkingSpaces']) > 0:
            return json_item['parkingSpaces'][0]
        return '0'
    
    def mount_link(self, json_item):
        return "zapimoveis.com.br" + json_item['link']['href']
    
    def get_address(self, json_item):
        data = json_item['link']['data']
        street = data['street']
        streetNumber = data['streetNumber']
        neighborhood = data['neighborhood']
        city = data['city']
        state = data['state']
        if street:
            return f"{street}, {streetNumber}, {neighborhood}, {city} - {state}"
        else:
            return json_item['listing']['address']['zipCode']
