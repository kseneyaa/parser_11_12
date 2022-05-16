import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.common.action_chains
import random
import argparse
import get_list_work
from pathlib import Path
from config import *
import work_page
import csv 


def get_all_artist_info(url):
    
    get_artist = Artists_Page(url)
    
    get_artist.get_info_under_name()
    get_artist.get_name()
    get_artist.get_info()
    
    save_to_csv(get_artist.artist)
    
    get_artist.get_list_works()
    get_artist.links
          
#     return get_artist.artist
    return get_artist.links



def save_to_csv(artist_result):
    
#     output = Path(ARTIST_OUTPUT_DIR)    
#     artist_info = pd.read_csv(output, index_col = 0)
    
#     artist_id = artist_result['link']
#     artist_info.loc[artist_id] = None
#     for key in artist_result:
#         artist_info.loc[artist_id, key] = artist_result[key]
#     artist_info.to_csv(output)
    
    # csv header
    fieldnames = ARTIST_HEAD
    rows = [artist_result]
#     print(rows)
    with open(Path(ARTIST_OUTPUT_DIR), 'a+', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows)

        
        
class Artists_Page:
    
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        self.artist_page = BeautifulSoup(response.text, 'html')
#         self.artist = {'name' : '', 'info': '', 'bio': '', 
#                        'exhibitions': '', 'fairs':'','literature':'', 'link':''}
        self.artist = dict()
        for art_head in ARTIST_HEAD:
            self.artist[art_head] = ''
        self.artist['link'] = url
        self.links = []
        
    def get_name(self):
        name = self.artist_page.find("div", {"class":"et_pb_text_inner"}).find('h2').text
        self.artist['name'] = name
    
    def get_info_under_name(self):
        info = str()
        for text in self.artist_page.find("div", {"class":"et_pb_text_inner"}).find_all('p'):
            info += text.text + ' '
        self.artist['info'] = info
    
    
    def get_list_works(self):
#         self.links = get_list_work.get_works_list(self.artist_page)
        self.links = get_list_work.get_works_list(self.artist['link'])
        
#         for work_link in self.artist_page.find("ul", {'class': 'products columns-3'}).find_all("li"):
#             self.links.append(work_link.find('a')['href'])

    def get_info(self):
        
        try:
            el_0 = self.artist_page.find('div', {'class' : 'et_pb_tab et_pb_tab_0 clearfix et_pb_active_content'}).get_text(strip=True)
        except:
            el_0 = ''
            
        try:
            el_1 = self.artist_page.find('div', {'class': 'et_pb_tab et_pb_tab_1 clearfix'}).text
        except:
            el_1 = ''
            
        try:
            el_2 = self.artist_page.find('div', {'class': 'et_pb_tab et_pb_tab_2 clearfix'}).text
        except:
            el_2 = ''
            
        try:
            el_3 = self.artist_page.find('div', {'class': 'et_pb_tab et_pb_tab_3 clearfix'}).text
        except:
            el_3 = ''
            
        ele = []
        ele.append(el_0)
        ele.append(el_1)
        ele.append(el_2)
        ele.append(el_3)    
        
        list_elements = [element.text for element in self.artist_page.find('ul', {'class' : 'et_pb_tabs_controls clearfix'}).find_all('li')]        
        for i,el in enumerate(list_elements):
            if el == 'Выставки':
                self.artist['exhibitions'] = ele[i]
            elif el == 'Биография':
                self.artist['bio'] = ele[i]
            elif el == 'Ярмарки':
                self.artist['fairs'] = ele[i]
            elif el == 'Библиография':
                self.artist['literature'] = ele[i]   
                
#         self.work['bio'] = self.work_page.find('div', {'class' : 'et_pb_tab et_pb_tab_0 clearfix et_pb_active_content'}).get_text(strip=True)
#         self.work['exhibitions'] = self.work_page.find('div', {'class': 'et_pb_tab et_pb_tab_1 clearfix'}).text
#         self.work['fairs'] = self.work_page.find('div', {'class': 'et_pb_tab et_pb_tab_2 clearfix'}).text
#         self.work['literature'] = self.work_page.find('div', {'class': 'et_pb_tab et_pb_tab_3 clearfix'}).text
    
    def print_result(self):
        print(self.artist.keys())
        for key in self.artist:
            print(key, ':',self.artist[key], '\n')
#         print(self.artist)
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Запуск получения информации по художнику')
    parser.add_argument('-url', '--url', help='Путь к странице художника')     
    args = parser.parse_args()
    
    url = args.url or 'https://online.11-12gallery.com/avtor/rualeksej-alpatovenalexey-alpatov/'
    
    get_artist = Artists_Page(url)
    get_artist.get_info_under_name()
    get_artist.get_name()
    get_artist.get_info()
    get_artist.print_result()
    
#     links = get_all_artist_info(url)
#     pd.read_csv(ARTIST_OUTPUT_DIR)   
#     print(links)
    
    
    
    
    
    