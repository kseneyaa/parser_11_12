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

"""
Script to get the work links for each artist (ex. https://online.11-12gallery.com/avtor/rualeksej-alpatovenalexey-alpatov/)
"""

def get_works_list(artist_link):
#     links = []
    
#     for work_link in artist_page.find("ul", {'class': 'products columns-3'}).find_all("li"):
        
#         links.append(work_link.find('a')['href'])
#     return links

    links = []
    for page_number in range(1, 10000):
        try:
            response = requests.get(f'{artist_link}page/{page_number}')
            artist_page = BeautifulSoup(response.text, 'lxml')

            for work_link in artist_page.find("ul", {'class': 'products columns-3'}).find_all("li"):

                links.append(work_link.find('a')['href']) 
        except:
            break
            
    return links
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Запуск получения списка ссылок на работы')
    parser.add_argument('-url', '--url', help='Путь к странице')     
    args = parser.parse_args()
    
    url = args.url or 'https://online.11-12gallery.com/avtor/rualeksej-alpatovenalexey-alpatov/'
    
#     response = requests.get(url)
#     artist_page = BeautifulSoup(response.text, 'html.parser')
    
#     links = get_works_list(artist_page)
    links = get_works_list(url)
    [print(i) for i in links]
    print('Count links:', len(links))