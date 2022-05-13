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
from urllib.parse import urljoin
from config import *

"""
Script to get the lists of artists from url https://online.11-12gallery.com/avtory/
"""

class List_Artists:
    
    def __init__(self, url):
        self.url = url
        self.list_of_artists = []
    
    def get_artists_list(self):

        response = requests.get(self.url)
        artists_page = BeautifulSoup(response.text, 'html.parser')
        
        base = response.url

        for link in artists_page.find_all("div", {"class":"et_pb_text_inner"}):
            self.list_of_artists.append(urljoin(base, link.find("a")['href']))
            
    def print_list(self):
        print(self.list_of_artists)
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Запуск получения списка художников')
    parser.add_argument('-url', '--url', help='Путь к странице')     
    args = parser.parse_args()
    
#     url = args.url or 'https://online.11-12gallery.com/avtory/'
    url = args.url or ARTISTS_LIST_URL
    get_list = List_Artists(url)
    get_list.get_artists_list()
    get_list.print_list()
    
    