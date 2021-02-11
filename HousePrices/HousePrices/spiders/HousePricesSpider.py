import scrapy
from selenium import webdriver

class HousePricesSpider(scrapy.Spider):
    name='HousePriceSpider'
    start_urls = [
        'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/bogota'
    ]

    def __init__(self):
        self.driver = webdriver.Chrome('../Driver/chromedriver.exe')

    def parse(self,response):
        self.driver.get(start_urls[0])