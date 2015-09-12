############# ############# #############
# stat_plotter v1.0
# by JAG3
#
# Basic stats plotting
############# ############# #############
import urllib2
import re
from bs4 import BeautifulSoup


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def url_to_soup(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return BeautifulSoup(html, "html.parser")

def assign_type(site, link_url):
    # 0 - article
    # 1 - internal link
    # 2 - external link
    if site == "http://fivethirtyeight.com":
        n_backslash = 0
        for char in link_url:
            if char == "/":
                n_backslash = n_backslash+1
        if link_url.find(site)!=-1 and n_backslash==5:
            return 0
        elif link_url.find(site[7:])==-1 and link_url.find("http")!=-1:
            return 2
        else:
            return 1
    elif site == "http://www.nytimes.com":
        if link_url.find("2015/09/1")!=-1 or link_url.find("2015/09/0")!=-1:
            return 0
        elif

if __name__ == "__main__":
    sites = {}
    sites["http://fivethirtyeight.com"] = {}
    sites["http://www.nytimes.com"]

    for site, obj in sites.iteritems():
        soup = url_to_soup(site)
        n_stories, n_internal, n_external  = 0, 0, 0
        story_urls = set()
        for link in soup.find_all('a'):
            link_url = link.get('href')
            link_type = assign_type(site, link_url)


        print n_stories, len(story_urls), n_internal, n_external