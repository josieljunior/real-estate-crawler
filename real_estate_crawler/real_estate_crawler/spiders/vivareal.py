import json
import scrapy

from real_estate_crawler.items import RealEstateCrawlerItem
from real_estate_crawler.spiders import initVivaReal

PAGE_SIZE = 36

class VivarealSpider(initVivaReal):
    name = "vivareal"
    allowed_domains = ["vivareal.com.br"]

    start_url = 'https://glue-api.vivareal.com/v2/listings?' \
                'addressCity=São Paulo' \
                '&addressLocationId=BR>Sao Paulo>NULL>Sao Paulo' \
                '&addressNeighborhood=' \
                '&addressState=São Paulo' \
                '&addressCountry=' \
                '&addressStreet=' \
                '&addressZone=' \
                '&addressPointLat=-23.555771' \
                '&addressPointLon=-46.639557' \
                '&business=SALE' \
                '&facets=amenities' \
                '&unitTypes=APARTMENT,HOME,HOME,APARTMENT,APARTMENT,HOME' \
                '&unitSubTypes=UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|CONDOMINIUM|PENTHOUSE|FLAT|TWO_STORY_HOUSE' \
                '&unitTypesV3=APARTMENT,HOME,CONDOMINIUM,PENTHOUSE,FLAT,TWO_STORY_HOUSE' \
                '&usageTypes=RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL,RESIDENTIAL' \
                '&listingType=USED' \
                '&parentId=null' \
                '&categoryPage=RESULT' \
                '&includeFields=search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount),page,seasonalCampaigns,fullUriFragments,nearby(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),expansion(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier,phones),facets,developments(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount)),owners(search(result(listings(listing(displayAddressType,amenities,usableAreas,constructionStatus,listingType,description,title,unitTypes,nonActivationReason,propertyType,unitSubTypes,id,portal,parkingSpaces,address,suites,publicationType,externalId,bathrooms,usageTypes,totalAreas,advertiserId,bedrooms,pricingInfos,showPrice,status,advertiserContact,videoTourLink,whatsappNumber,stamps),account(id,name,logoUrl,licenseNumber,showAddress,legacyVivarealId,phones,tier),medias,accountLink,link)),totalCount))' \
                '&size={size}' \
                '&from={previus}' \
                '&q=' \
                '&developmentsSize=5' \
                '&__vt=control,PBOT' \
                '&levels=CITY' \
                '&ref=' \
                '&pointRadius=' \
                '&isPOIQuery=' 
                
    headers = {
        'x-domain': 'www.vivareal.com.br'
    }

    def start_requests(self):
        page = self.start_page
        while page < self.start_page + self.pages_to_crawl:
            req_url = self.start_url.format(size=PAGE_SIZE, previus=(page - 1) * PAGE_SIZE)
            yield scrapy.Request(url=req_url, headers=self.headers)
            page += 1


    def parse(self, response):
        conteudo_bytes = response.body
        conteudo_string = conteudo_bytes.decode('utf-8')
        json_response = json.loads(conteudo_string)


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
        return "vivareal.com.br" + json_item['link']['href']
    
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
