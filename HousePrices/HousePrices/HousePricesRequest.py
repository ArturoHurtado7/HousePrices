import requests
from lxml import html
from bs4 import BeautifulSoup

start_urls = [
    'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/bogota'
]

page = requests.get(start_urls[0])

if (page.status_code == 200):
    comp = html.fromstring(page.content)
    links = tre