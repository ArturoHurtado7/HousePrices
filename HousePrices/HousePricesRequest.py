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
# Global variables
#*************************************************************************************
# Amount of time to wait between requests
delay = 2

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
    exist = path.exists(file_name)

    if not(exist):
        # in case that the file doesn't exist then the file is created
        if p_type == 'r':
            write_region_file(file_name)
    else:
        # in case that the file is empty then the file is created
        size = os.path.getsize(file_name)
        if size == 0:
            if p_type == 'r':
                write_region_file(file_name)

    # Reads the file lines
    try:
        if p_type == 'r':
            file_list = read_file(file_name)
            write_apartment_file(file_list)
    except:
        print('there is not regions file')
    

#*************************************************************************************
# Name:         write_region_file
# Description:  write into the region file
# file_name:    the file name with extension
#*************************************************************************************
def write_region_file(file_name):
    parent_extracted = {}
    parent = {}
    line_list = []

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
            line_list.append(info)

    write_file(file_name, line_list)

#*************************************************************************************
# Name:         process_regions
# Description:  to extract info from the header
# s_url:        String that recive the url page to requests
#*************************************************************************************
def process_regions(s_url):
    regions = {}
    page = requests.get(s_url)
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
    time.sleep(delay)
    return regions


#*************************************************************************************
#                               Utilities Functions
#*************************************************************************************

#*************************************************************************************
# Name:         write_file
# Description:  write lines into a file
# file_name:    the file name with extension
#*************************************************************************************
def write_file(file_name, line_list):
    # Open file in write mode
    f = open(file_name,'w', encoding='utf-8')

    # Write lines into the file
    for l_list in line_list:
        f.write(l_list + '\n')

#*************************************************************************************
# Name:         read_file
# Description:  extract the lines from a file
# file_name:    the file name with extension
# return:       line_list - list with lines from a file
#*************************************************************************************
def read_file(file_name):
    line_list = []

    # Open file in read mode
    f = open(file_name,'r', encoding='utf-8')

    # Read all the lines
    lines = f.readlines()

    # Save lines into a list
    for l in lines:
        line_list.append(l.strip())
    
    return line_list

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