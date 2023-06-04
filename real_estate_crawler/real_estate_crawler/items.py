# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class RealEstateCrawlerItem(scrapy.Item):
    crawler = Field()
    link = Field()
    lat = Field()
    lng = Field()
    area = Field()
    type = Field()
    bedrooms = Field()
    bathrooms = Field()
    parking_spaces = Field()
    price = Field()
    address = Field()

