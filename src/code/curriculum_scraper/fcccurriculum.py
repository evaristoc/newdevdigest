#!/usr/bin/env python3
import collections
import requests
from bs4 import BeautifulSoup
import pickle

def FCCcurriculum_extraction():
    headers = {'user-agent': 'simpleBot description/keywords_landing_page_no_crawler code/0.0.1'}
    directory = "/home/ec/Documents/MainComp_Programming/FreeCodeCamp/data_analysis/1_archive"
    page = "https://beta.freecodecamp.com/en/map"
    curriculum = collections.defaultdict(list)
    try:
        r = requests.get(page, headers=headers)
    except:
        print("error reaching the page ", page, '; code status ', r.status_code)
        return [-1,-1,-1]
    soup = BeautifulSoup(r.content)
    alla = soup.find_all('a')
    val = None
    count = 1
    for a in alla:
        if a.attrs.get('aria-controls'):
            val = '-'.join(a.attrs.get('aria-controls').lower().split(' '))
            curriculum[val].append(count)
            count += 1
        if val and a.attrs.get('href').find(val) >-1:             
            curriculum[val].append(a.attrs.get('href'))
    #pickle.dump(curriculum, open(directory+"/fcccurriculum.pkl",'bw'))
    return curriculum


#curriculum = FCCcurriculum_extraction()
