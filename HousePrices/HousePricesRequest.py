#*************************************************************************************
# Date:     2021/02/11
# Objetive: Extract House prices data from - https://www.fincaraiz.com.co
#           Using request and lxml
#*************************************************************************************
import requests
import time

from file import file
from lxml import html
from bs4 import BeautifulSoup

#*************************************************************************************
# Global variables
#*************************************************************************************
# Amount of time to wait between requests
delay = 4

# base url to scrape
root_url = 'https://www.fincaraiz.com.co'

# tree urls to scrape
start_urls = [
    'https://www.fincaraiz.com.co/proyectos-vivienda-nueva/',
    'https://www.fincaraiz.com.co/finca-raiz/venta/',
    'https://www.fincaraiz.com.co/finca-raiz/arriendos/',
    'https://www.fincaraiz.com.co/finca-raiz/alquiler-vacacional/'
]

# String to concatenate
add_str = '?ad=|#|||||||||||||||||||||||||||||||||||||||'

#*************************************************************************************
#                               Logic Functions
#*************************************************************************************

#*************************************************************************************
# Name:         process_file
# Description:  flux to creates an process a file
# p_type        process type
#                   r - region
#                   a - apartment
# file_name     processed file name
#*************************************************************************************
def process_file(p_type, file_name):
    # Validate the existence of the regions file
    f = file(file_name)
    exist = f.val_file()

    if not(exist):
        # in case that the file doesn't exist then the file is created
        if p_type == 'r':
            write_region_file(file_name)
    else:
        # in case that the file is empty then the file is created
        size = len(f.read_file())
        if size == 0:
            if p_type == 'r':
                write_region_file(file_name)

    # Reads the file lines
    #try:
        if p_type == 'r':
            file_list = f.read_file()
            write_apartment_file(file_list)
    #except:
    #    print('there is not regions file')

#*************************************************************************************
# Name:         write_apartment_file
# Description:  write into the apartment file
# file_list:    list with all the url to search
#*************************************************************************************
def write_apartment_file(file_list):
    #for fl in file_list:
    #    print('start_url: ', fl)

    url = root_url + file_list[0]
    print('url: ', url)
    page = requests.get(root_url + file_list[0])
    time.sleep(delay)
    if page.status_code == 200:
        
        t = html.fromstring(page.content)
        links_aptos = t.xpath('//div[@id="divAdverts"]//li[@class="title-grid"]/@onclick')
        print(len(links_aptos))
        count = 0

        for l_aptos in links_aptos:
            link_apto = l_aptos.split('\'')[-2]
            url = root_url + link_apto
            apto_page = requests.get(url)
            print('url: ', url)
            time.sleep(delay)

            if apto_page.status_code == 200:
                t = html.fromstring(apto_page.content)
                title = t.xpath('//div[@class = "title"]//div[@class="box"]/h1/text()')[0]
                print('title: ', title)
                neighborhood = t.xpath('//div[@class = "title"]//div[@class="box"]/span/span/text()')[0]
                print('neighborhood: ', neighborhood)
                adress = t.xpath('//div[@class = "title"]//div[@class="box"]/div/span/text()')[0]
                print('adress: ', adress)

                imn_type = t.xpath('//div[@id="typology"]//tbody/tr')

            

#*************************************************************************************
# Name:         write_region_file
# Description:  write into the region file
# file_name:    the file name with extension
#*************************************************************************************
def write_region_file(file_name):
    parent_extracted = {}
    parent = {}
    info_list = []

    # Iterate all the start_urls 
    for s_url in start_urls:
        # Write regions
        parent = process_regions(s_url)

        # concatenate the current result with the previous results
        parent_extracted = {**parent_extracted, **parent}

    for p_e in parent_extracted:
        regions_info = parent_extracted[p_e]['regions_info']
        for p_i in regions_info:
            info = regions_info[p_i]['url']
            info_list.append(info)

    file(file_name).write_file(info_list)

#*************************************************************************************
# Name:         process_regions
# Description:  to extract info from the header
# s_url:        String that recive the url page to requests
#*************************************************************************************
def process_regions(s_url):
    regions = {}
    page = requests.get(s_url)
    time.sleep(delay)
    # continues if everything is ok
    if page.status_code == 200:
        print('start_url: ', s_url)
        t = html.fromstring(page.content)
        places_list = t.xpath('//div[@id="gridLocations"]//div[@class="ContentCollapse"]//li')
        regions_info = {}
        for l in places_list:
            parent = int(l.xpath('input/@parentlevel')[0])
            #Extracts all regions info, which are the input with @parentlevel equals zeroes
            if parent == 0:
                pid = l.xpath('input/@value')[0]
                name = l.xpath('input/@locationname')[0]
                url = l.xpath('a/@href')[0]
                regions_info[pid] = {
                    'name': name,
                    'url': url
                }
        item = s_url.split('/')[-2]
        regions[item] = {
            'regions_info': regions_info
        }
    # wait for a few seconds
    return regions

#*************************************************************************************
#                                   Main Function
#*************************************************************************************

#*************************************************************************************
# Name:         main
# Description:  where the program started
#*************************************************************************************
def main():
    process_file('r', 'regions_info.txt')

if __name__ == '__main__':
    main()