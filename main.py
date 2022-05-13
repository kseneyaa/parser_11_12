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
import os
import name_artists
import artist_page
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool as Pool
from config import *
import shutil
import artist_page
import work_page
from itertools import repeat
import csv

def start_parsing(artist):
    
    
    work_links = artist_page.get_all_artist_info(artist)
    
#     list_of_works = work_page.get_info_on_work()
#         for work in list_of_works:
    
    PROCESSES = cpu_count()
    pool = Pool(PROCESSES)
    
    for _ in tqdm(pool.starmap(work_page.get_info_on_work, zip(work_links, repeat(artist)))):
        pass
#     for _ in tqdm(pool.imap(work_page.get_info_on_work, work_links, artist), total=len(work_links)):
#         pass
        
    pool.close()
    pool.join()
    
#     for work_link in work_links:
#         work_page.get_info_on_work(work_link, artist)
        
           
    
if __name__ == '__main__':
    
    try:
        shutil.rmtree(MAIN_OUTPUT)
    except:
        next
    os.makedirs(MAIN_OUTPUT, exist_ok = True)
    
    artist_info = pd.DataFrame(columns = ARTIST_HEAD)
    artist_info.to_csv(ARTIST_OUTPUT_DIR, index = False)
    
    artist_works = pd.DataFrame(columns = WORK_HEAD)
    artist_works.to_csv(WORK_OUTPUT_DIR, index = False)
    
    
#     url = 'https://online.11-12gallery.com/avtory/'
    get_list = name_artists.List_Artists(ARTISTS_LIST_URL)
    get_list.get_artists_list()
    list_of_artists = get_list.list_of_artists
    
#     while True:
#         if list_of_artists:
    PROCESSES = cpu_count()
    pool = Pool(PROCESSES)

    for _ in tqdm(pool.imap(start_parsing, list_of_artists), total=len(list_of_artists)):
        break
#     for _ in tqdm(pool.imap(artist_page.get_all_artist_info, list_of_artists), total=len(list_of_artists)):
#         pass

    pool.close()
    pool.join()

    
    
    