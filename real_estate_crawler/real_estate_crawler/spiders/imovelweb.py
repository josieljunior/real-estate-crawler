import scrapy
import json


class ImovelwebSpider(scrapy.Spider):
    name = "imovelweb"
    allowed_domains = 'imovelweb.com.br'
    
   
    
    def start_requests(self):
        url = "https://www.imovelweb.com.br/rplis-api/postings"
        payload = [
            {
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
                "city": "109668",
                "province": None,
                "zone": None,
                "valueZone": None,
                "subZone": None,
                "coordenates": None
            }]

        HEADERS = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
            'Referer':'https://www.imovelweb.com.br/apartamentos-venda.html',
            'Origin':'https://www.imovelweb.com.br',
            'Host':'www.imovelweb.com.br',
            'Content-Type':'application/json'
            }

        yield scrapy.Request(url, method='POST', headers=HEADERS, body=json.dumps(payload))
    
    def parse(self, response):
        if response.status == 200:
            self.log("A solicitação foi bem-sucedida.")
        else:
            self.log("A solicitação falhou. Status: {}".format(response.status))