import urllib2
import re
from bs4 import BeautifulSoup
from math import sqrt
import numpy as np
import codecs
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def url_to_soup(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
    req = urllib2.Request(url,headers=hdr)
    response = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(req)
    return BeautifulSoup(response.read(), "html.parser")

def money_to_int(str_gross):
    return int(re.sub('[^\w]','',str_gross))

def process_year_page(year_url):
    max_money = 0
    l_horror_gross = []
    year_sou = url_to_soup(year_url)
    for row in year_sou.find_all("tr"):
        try:
            if row['bgcolor']=="#ffffff":
                n_cell = 0
                rank_one = False
                b_is_horror = False
                for cell in row.find_all("td"):
                    #Check if this is the top grossing movie of the year
                    if n_cell == 0 and cell.text == "1":
                        rank_one = True
                    #If so, store this number as part of the return value
                    if n_cell == 3 and rank_one == True:
                        max_money = money_to_int(cell.text)
                        rank_one = False
                    if n_cell == 3 and b_is_horror == True:
                        l_horror_gross.append(money_to_int(cell.text))
                    if n_cell == 1:
                        for link in cell.find_all("a"):
                            move_sou = url_to_soup("http://www.boxofficemojo.com" + link["href"])
                            for move_cell in move_sou.find_all("td"):
                                if move_cell.text == "Genre: Horror":
                                    b_is_horror = True
                    n_cell = n_cell + 1
        except:
            continue
    return (max_money, l_horror_gross)

def parse_year(year_front_url):
    year_sou = url_to_soup(year_url)
    other_pages = set([year_front_url])
    for link in year_sou.find_all("a"):
        if len(link.text) > 3:
            if link.text[0] == "#" and link.text[2] == "0":
                other_pages.add("http://www.boxofficemojo.com"+link["href"])

    max_gross = 0
    l_horror_gross = []
    for page in other_pages:
        (temp_gross, temp_list) = process_year_page(page)
        if temp_gross != 0: max_gross=temp_gross
        l_horror_gross.extend(temp_list)

    return (max_gross, l_horror_gross)

if __name__ == "__main__":
    base_url = "http://www.boxofficemojo.com/yearly/"
    base_sou = url_to_soup(base_url)

    year_links = set()
    for row in base_sou.find_all("tr"):
        for link in row.find_all("a"):
            if link.text[:3] in ["201", "200", "199", "198"]:
                year_links.add(base_url+link["href"])

    horror_data = {}
    for year_url in year_links:
        (max_gross, l_gross)  = parse_year(year_url)
        i_yr = year_url.find("yr")
        year = year_url[i_yr+3:i_yr+7]
        horror_data[year] = {"max":max_gross,"h_gross":l_gross}

    for k, v in horror_data.iteritems():
        print "***\nYear:",k,"\tMax:",v["max"],"\nHorror Grosses",v["h_gross"]

    with codecs.open("movieData.json", encoding="utf-8",mode="wb") as fOut:
        json.dump(horror_data, fOut)
