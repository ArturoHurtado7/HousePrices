#*************************************************************************************
# Date:     2021/02/11
# Objetive: Extract House prices data from - https://www.fincaraiz.com.co
#           Using request and lxml
#*************************************************************************************
import requests
import os.path
import time

from lxml import html
from bs4 import BeautifulSoup
from os import path

#*************************************************************************************
# Variables Globales del proyecto 
#*************************************************************************************
delay = 2
root_url = 'https://www.fincaraiz.com.co'
start_urls = [
    'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/',
    'https://www.fincaraiz.com.co/finca-raiz/venta/',
    'https://www.fincaraiz.com.co/finca-raiz/arriendos/',
    'https://www.fincaraiz.com.co/finca-raiz/alquiler-vacacional/'
]
add_str = '?ad=|#|||||||||||||||||||||||||||||||||||||||'

#*************************************************************************************
# Function to extract page info from colombia's departments
#*************************************************************************************
def parent_extraction(s_url):
    parents = {}
    page = requests.get(s_url)
    if page.status_code == 200:
        print('start_url: ', s_url)
        t = html.fromstring(page.content)
        places_list = t.xpath('//div[@id="gridLocations"]//div[@class="ContentCollapse"]//li')
        parent_info = {}
        for l in places_list:
            parent = int(l.xpath('input/@parentlevel')[0])
            #Extracts all parents, which are the input with @parentlevel equals zeroes
            if parent == 0:
                pid = l.xpath('input/@value')[0]
                name = l.xpath('input/@locationname')[0]
                url = l.xpath('a/@href')[0]
                parent_info[pid] = {
                    'name': name,
                    'url': url
                }
        item = s_url.split('/')[-2]
        parents[item] = {
            'parent_info': parent_info
        }
    time.sleep(delay)
    return parents

#*************************************************************************************
# 
#*************************************************************************************
def write_mode(file_name, type_mode):
    # Info logs
    print('*' * 25)
    print('Write Mode')
    print('*' * 25)

    # Extracts parents info
    parent_extrac = {}
    parent = {}
    for s_url in start_urls:
        # Write parents
        if type_mode == 'p':
            parent = parent_extraction(s_url)
            parent_extrac = {**parent_extrac, **parent}

    # Open file in write mode
    f = open(file_name,'w', encoding='utf-8')

    for p_e in parent_extrac:
        parent_info = parent_extrac[p_e]['parent_info']
        f.write(p_e + '\n')
        for p_i in parent_info:
            info = parent_info[p_i]['url']
            print(info)
            f.write(info + '\n')

#*************************************************************************************
# 
#*************************************************************************************
def read_mode():
    print('*' * 25)
    print('Read Mode')
    print('*' * 25)

    f = open('parent_info.txt','r', encoding='utf-8')
    lines = f.readlines()
    count = 0
    for l in lines:
        count += 1
        print('line {} : {}'.format(count,l.strip()))

#*************************************************************************************
# 
#*************************************************************************************
def main():
    exist = path.exists('parent_info.txt')
    
    print('*' * 25)
    print('File exist: ', exist)
    print('*' * 25)

    if not(exist):
        write_mode('parent_info.txt', 'p')
    else:
        size = os.path.getsize('parent_info.txt')

        print('*' * 25)
        print('File size: ', size)
        print('*' * 25)

        if size == 0:
            write_mode('parent_info.txt', 'p')
        else:
            read_mode()

if __name__ == '__main__':
    main()