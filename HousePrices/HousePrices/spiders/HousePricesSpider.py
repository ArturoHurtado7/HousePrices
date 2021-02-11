import scrapy

class HousePricesSpider(scrapy.Spider):
    name='HousePriceSpider'
    start_urls = [
        'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/bogota'
    ]

    def parse(self,response):
        print('wait')