import scrapy


class ImovelwebSpider(scrapy.Spider):
    name = "imovelweb"
    allowed_domains = ["imovelweb.com.br"]
    start_urls = ["https://www.imovelweb.com.br/rplis-api/postings"]

    def parse(self, response):
        # Construir os parâmetros do formulário
        form_data = {
            "q": None,
            "direccion": None,
            "moneda": None,
            "preciomin": None,
            "preciomax": None,
            "services": "",
            "general": "",
            "searchbykeyword": "",
            "amenidades": "",
            "caracteristicasprop": None,
            "comodidades": "",
            "disposicion": None,
            "roomType": "",
            "outside": "",
            "areaPrivativa": "",
            "areaComun": "",
            "multipleRets": "",
            "tipoDePropiedad": "2",
            "subtipoDePropiedad": None,
            "tipoDeOperacion": "1",
            "garages": None,
            "antiguedad": None,
            "expensasminimo": None,
            "expensasmaximo": None,
            "habitacionesminimo": 0,
            "habitacionesmaximo": 0,
            "ambientesminimo": 0,
            "ambientesmaximo": 0,
            "banos": None,
            "superficieCubierta": 1,
            "idunidaddemedida": 1,
            "metroscuadradomin": None,
            "metroscuadradomax": None,
            "tipoAnunciante": "ALL",
            "grupoTipoDeMultimedia": "",
            "publicacion": None,
            "sort": "relevance",
            "etapaDeDesarrollo": "",
            "auctions": None,
            "polygonApplied": None,
            "idInmobiliaria": None,
            "excludePostingContacted": "",
            "banks": "",
            "city": None,
            "province": "265",
            "zone": None,
            "valueZone": None,
            "subZone": None,
            "coordenates": None
        }

        headers = {
        'Accept': '*/*'
        }

        # Enviar a solicitação POST
        yield scrapy.Request(url=self.start_url, headers=headers, method='POST', body=form_data)

    def parse_results(self, response):
      print(response)