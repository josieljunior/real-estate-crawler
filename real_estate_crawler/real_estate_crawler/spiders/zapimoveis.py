import json
import scrapy

from real_estate_crawler.items import RealEstateCrawlerItem

PAGE_SIZE = 24

class ZapimoveisSpider(scrapy.Spider):
    name = "zapimoveis"
    allowed_domains = ["zapimoveis.com.br"]
    start_urls = ["https://zapimoveis.com.br"]
    start_url = 'https://glue-api.zapimoveis.com.br/v2/listings?' \
                'categoryPage=RESULT' \
                '&business=SALE' \
                '&listingType=USED' \
                '&parentId=null' \
                '&unitTypes=APARTMENT,HOME,HOME' \
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
                '&from={from_}' \
                '&page={page}' \
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
        req_url = self.start_url.format(size=PAGE_SIZE, from_=0, page=1)
        yield scrapy.Request(url=req_url, headers=self.headers)

    def parse(self, response):
        json_response = response.json()

        for result in json_response['search']['result']['listings']:
            pp = result['listing']
            items = RealEstateCrawlerItem()

            items['lat'] = self.get_address(pp, 'lat')
            items['lon'] = self.get_address(pp, 'lon')
            items['area'] = pp['usableAreas'][0]
            items['type'] = pp['unitTypes'][0]
            items['bedrooms'] = pp['bedrooms'][0]
            items['bathrooms'] = pp['bathrooms'][0]
            items['parking_spaces'] = self.get_parking_space(pp)
            items['price'] = pp['pricingInfos'][0]['price']
            
            yield items

            

    def get_address(self, json, key):
        if 'address' in json and 'point' in json['address']:
            return json['address']['point'][key]
        else:
            return json['address']['zipCode']
            
    def get_parking_space(self, json):
        if 'parkingSpaces' in json and len(json['parkingSpaces']) > 0:
            return json['parkingSpaces'][0]
        return '0'