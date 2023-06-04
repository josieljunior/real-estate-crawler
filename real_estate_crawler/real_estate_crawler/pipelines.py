# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RealEstateCrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.lowercase(adapter)

        return item

    def lowercase(self, adapter):   
        value = adapter.get('type')
        adapter['type'] = value.lower()