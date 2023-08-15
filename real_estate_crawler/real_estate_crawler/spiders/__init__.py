import scrapy


class initZapImoveis(scrapy.Spider):
    custom_settings = {
        'FEEDS': {
            'data_zapimoveis.csv': {'format': 'csv', 'overwrite': True},
        }
    }

    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)

class initVivaReal(scrapy.Spider):
    custom_settings = {
        'FEEDS': {
            'data_vivareal.csv': {'format': 'csv', 'overwrite': True},
        }
    }
    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)

class initLopes(scrapy.Spider):
    custom_settings = {
        'FEEDS': {
            'data_lopes.csv': {'format': 'csv', 'overwrite': True},
        }
    }
    def __init__(self, start_page=1, pages_to_crawl=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.pages_to_crawl = int(pages_to_crawl)