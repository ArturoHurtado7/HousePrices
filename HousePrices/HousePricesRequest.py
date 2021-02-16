#*************************************************************************************
# Name:     HousePricesRequest.py
# Date:     2021/02/11
# Objetive: Extract House prices from - https://www.fincaraiz.com.co
#           Using "request" and "lxml" libraries
#*************************************************************************************
import requests
import time

from file import file
from lxml import html
from bs4 import BeautifulSoup


#*************************************************************************************
# Global variables
#*************************************************************************************
# Amount of time to wait between requests in seconds
delay = 3

# Program Name
program_name = 'HousePricesRequest.py'

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
# Name:         validate_file
# Description:  Validate file existence
# p_type        process type
#                   r - region
#                   a - apartment
# file_name     processed file
#*************************************************************************************
def validate_file(p_type, file_name):
    try:
        f = file(file_name)
        exist = f.val_file()
        if not(exist):
            # in case that the file doesn't exist then it's created
            if p_type == 'r':
                write_region_file(file_name)
        else:
            # in case that the file is empty then it's created
            size = len(f.read_file())
            if size == 0:
                if p_type == 'r':
                    write_region_file(file_name)
    except Exception as e:
        print(10, program_name, "Error validate_file:", e)


#*************************************************************************************
# Name:         process_file
# Description:  process file existence
# p_type        process type
#                   r - region
#                   a - apartment
# file_name     processed file
#*************************************************************************************
def process_file(p_type, file_name):
    # Reads the file lines
    try:
        f = file(file_name)
        file_list = f.read_file()
        # case type region
        if p_type == 'r':
            #for s_url in file_list:
            #    apartments_pages(s_url)
            print('file_list[0]', file_list[0])
            apartments_pages(file_list[0])
    except Exception as e:
        print(20, program_name, "Error process_file:", e)


#*************************************************************************************
# Name:         apartments_pages
# Description:  write into the apartment file
# s_url:        url to search
#*************************************************************************************
def apartments_pages(s_url):
    # Join the root url with the rest of the url
    url = root_url + s_url
    # Make the request 
    page = requests.get(url)
    # delay beetween requests
    time.sleep(delay)
    # Case when the code is OK
    if page.status_code == 200:

        t = html.fromstring(page.content)
        links_aptos = t.xpath('//div[@id="divAdverts"]//ul[starts-with(@id,"rowIndex")]/li[@class="title-grid"]/@onclick')

        for i_aptos in range(len(links_aptos)):

            links_aptos[i_aptos] = links_aptos[i_aptos].replace(root_url,'\'')
            links_aptos[i_aptos] = links_aptos[i_aptos].split('\'')[-2]
            print('links_aptos['+str(i_aptos)+']', links_aptos[i_aptos])

            #extract_info_apto(links_aptos[i_aptos])

        return links_aptos
    else:
        print(30, "Error apartments_pages: Request with code ", page.status_code)


#*************************************************************************************
# Name:         extract_info_apto
# Description:  request from each 
# file_list:    list with all the url to search
#*************************************************************************************
def extract_info_apto(link_apto):
    url = root_url + link_apto
    print('url: ', url)
    apto_page = requests.get(url)
    print('status_code', apto_page.status_code)
    time.sleep(delay)

    if apto_page.status_code == 200:
        t = html.fromstring(apto_page.content)
        title = t.xpath('//div[@class = "title"]//div[@class="box"]/h1/text()')[0]
        neigh= t.xpath('//div[@class = "title"]//div[@class="box"]/span/span/text()')[0]
        adress = t.xpath('//div[@class = "title"]//div[@class="box"]/div/span/text()')[0]
        print('title: ', title, 'neigh: ', neigh, 'adress: ', adress)

        imn_type = t.xpath('//div[@id="typology"]//tbody/tr')
        for i_type in  imn_type:
            print(i_type.xpath('//td/text()'))


#*************************************************************************************
# Name:         write_region_file
# Description:  write into the region file
# file_name:    the file name with extension
#*************************************************************************************
def write_region_file(file_name):
    # Define function variables
    parent_extracted = {}
    parent = {}
    info_list = []
    f = file(file_name)
    # Iterate all the start_urls 
    for s_url in start_urls:
        # Write regions
        parent = process_regions(s_url)
        # concatenate the current result with the previous results
        parent_extracted = {**parent_extracted, **parent}
    # Iterate all the parent_extracted list
    for p_e in parent_extracted:
        regions_info = parent_extracted[p_e]['regions_info']
        for p_i in regions_info:
            info = regions_info[p_i]['url']
            info_list.append(info)
    # Write the file
    f.write_file(info_list)


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
    # Validate regions file
    validate_file('r', 'regions_info.txt')
    process_file('r', 'regions_info.txt')

if __name__ == '__main__':
    main()