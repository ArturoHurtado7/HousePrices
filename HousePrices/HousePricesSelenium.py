import scrapy
from scrapy.crawler import CrawlerProcess

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os
import time

start_urls = [
    'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/bogota'
]

def main():
    print("path: " + os.getcwd() + "*" * 20)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path = os.getcwd()+'/HousePrices/Driver/chromedriver.exe', chrome_options=chrome_options)
    driver.get(start_urls[0])
    
    delay = 5
    try:
        places_list = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'navbar-form')))
    except TimeoutException:
        print("Loading took too much time!")
    
    places_list = driver.find_elements_by_xpath('//div[@class="navbar-form"]//div[@class="form-group"]')
    

    for pl in places_list:
        print(pl)

    print(len(places_list))



    aux = input("Ingresa un numero: ")
    driver.quit()


if __name__ == "__main__":
    main()

#scrapy crawl HousePriceSpider