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
from config import *
from pathlib import Path
import csv 

"""
Script to get the info on each work (ex. https://online.11-12gallery.com/product/ru-parkovkaenpark/) 
"""

def get_info_on_work(url, artist_url):
    
#     print(url)
    
    work_info = Work_Page(url)
    work_info.get_title()
    work_info.get_price()
    work_info.launch_details()
    work_info.get_link_on_picture()
   
    save_work_to_csv(work_info.work, artist_url)
    return work_info.work

    
def save_work_to_csv(work_info, artist):
#     output = Path(WORK_OUTPUT_DIR) 
#     artist_works = pd.read_csv(output, index_col = 0)
    
#     work_id = work_info['work_link']
#     print(work_id)
#     artist_works.loc[work_id] = None

#     for key in work_info:
#         artist_works.loc[work_id, key] = work_info[key]
        
#     artist_works.loc[work_id, 'artist_link'] = artist
# #     print(work_info)
#     artist_works.to_csv(output)
    
    # csv header
    fieldnames = WORK_HEAD
    work_info['artist_link'] = artist
    rows = [work_info]
#     print(rows)
    with open(Path(WORK_OUTPUT_DIR), 'a+', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows)

    
class Work_Page:
    
    def __init__(self, url):
        
        url = url
        response = requests.get(url)
        self.work_page = BeautifulSoup(response.text, 'html.parser')
        
        self.work = dict()
        for work_head in WORK_HEAD:
            self.work[work_head] = ''
#         self.work = {'title' : '', 'price': '', 'materials': '', 'year': '', 
#                      'measurements' : '', 'link_img': ''}
        self.work['work_link'] = url
    
    def get_title(self):
        
        main_info = self.work_page.find("div", {"class": "summary entry-summary"})
        title = main_info.find("h1", {"class": "product_title entry-title"}).get_text(strip=True)
        self.work['title'] = title
        
    def get_price(self):
        
        main_info = self.work_page.find("div", {"class": "summary entry-summary"})
        self.work['price'] = main_info.find("p", {"class": "price"}).get_text(strip=True)
        
    def launch_details(self):
        deatils = self.work_page.find("div", {"class": "woocommerce-Tabs-panel woocommerce-Tabs-panel--additional_information panel entry-content wc-tab"})
        
        try:
            self.work['measurements'] = deatils.find("tr", {"class": "woocommerce-product-attributes-item woocommerce-product-attributes-item--dimensions"}).find("td", {"class": "woocommerce-product-attributes-item__value"}).get_text(strip=True)
        except:
            next
        try:
            self.work['materials'] = deatils.find("tr", {"class": "woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_rutexnikaentechnique"}).find("td", {"class": "woocommerce-product-attributes-item__value"}).get_text(strip=True)
        except:
            next
        try:
            self.work['year'] = deatils.find("tr", {"class": "woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_rugodenyear"}).find("td", {"class": "woocommerce-product-attributes-item__value"}).get_text(strip=True)
        except:
            next
        
    def get_link_on_picture(self):
        
        self.work['link_img'] = self.work_page.find('figure', {'class' : 'woocommerce-product-gallery__wrapper'}).find('img')['src']
        
    def print_work_info(self):
        
        print(self.work.keys())
        for key in self.work:
            print(key, ':',self.work[key], '\n')
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Запуск получения информации по работе')
    parser.add_argument('-url', '--url', help='Путь к странице работы')     
    args = parser.parse_args()
    
    url = args.url or 'https://online.11-12gallery.com/product/ru-parkovkaenpark/'
#     full_info = get_info_on_work(url)
#     print(full_info)

    work_info = Work_Page(url)
    work_info.get_title()
    work_info.get_price()
    work_info.launch_details()
    work_info.get_link_on_picture()
    work_info.print_work_info()
#     print(work_info.work)
    
    