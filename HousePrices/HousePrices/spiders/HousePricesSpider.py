import scrapy

#scrapy crawl HousePriceSpider

class HousePricesSpider(scrapy.Spider):
    name='HousePriceSpider'
    start_urls = [
        'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/',
        'https://www.fincaraiz.com.co/finca-raiz/venta/',
        'https://www.fincaraiz.com.co/finca-raiz/arriendos/',
        'https://www.fincaraiz.com.co/finca-raiz/alquiler-vacacional/'
    ]

    def parse(self,response):
        parent_info = {}
        places_list = response.xpath('//div[@id="gridLocations"]//div[@class="ContentCollapse"]//li/input/@type').getall()
        for l in places_list:
            print(l)