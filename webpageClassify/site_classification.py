############# ############# #############
# stat_plotter v1.0
# by JAG3
#
# Basic stats plotting
############# ############# #############
import urllib2
import re
from bs4 import BeautifulSoup
import nltk


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def url_to_soup(url):
    response = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
    return BeautifulSoup(response.read(), "html.parser")

def assign_type(site, link_url):
    # 0 - article
    # 1 - internal link
    # 2 - external link
    if site == "http://fivethirtyeight.com":
        n_backslash, n_dash = 0,0
        for char in link_url:
            if char == "/":
                n_backslash = n_backslash+1
            elif char == "-":
                n_dash = n_dash + 1
        if link_url.find(site)!=-1 and n_backslash==5 and n_dash>1:
            return 0
        elif link_url.find(site[7:])==-1 and link_url.find("http")!=-1:
            return 2
        else:
            return 1
    elif site == "http://www.nytimes.com":
        if link_url.find("2015/09")!=-1:
            return 0
        elif link_url.find("www.nytime")!=-1:
            return 1
        else:
            return 2
    elif site == "http://buzzfeed.com":
        if link_url == None:
            return 4
        elif link_url.find("http")!=-1:
            return 2
        else:
            n_backslash, n_dash = 0, 0
            for char in link_url:
                if char=="/":
                    n_backslash = n_backslash + 1
                elif char=="-":
                    n_dash = n_dash + 1
            if n_backslash==2 and n_dash>1:
                return 0
            else:
                return 1

def sent_to_word_list(sentence):
    sentence = re.sub('[\s]',' ',sentence.lower(), flags=re.UNICODE)
    sentence = re.sub('[^\w\s@]', '', sentence, flags=re.UNICODE)
    l_words = sentence.strip().split(' ')
    l_filtered = []
    for word in l_words:
        if word == "" or word == None : continue                                #just in case
        if '@' in word: continue                                                #remove email addresses
        if ('http' in word) or ('href' in word) or ('www' in word): continue    #and websites
        if len(word) < 3: continue                                              #and smallish words
        l_filtered.append(word)
    return l_filtered

def paragraph_to_word_list_list(str_in, tokenizer):
    raw_sentences = tokenizer.tokenize(str_in.strip())
    l_sentences = []
    for sentence in raw_sentences:
        if len(sentence) > 0:
            l_sentences.append(sent_to_word_list(sentence))
    return l_sentences

def story_stats(site, link_url, tokenizer):
    story_soup = url_to_soup(link_url)
    if site == "http://fivethirtyeight.com":
        l_ret = []
        for par in story_soup.find_all("p"):

        return l_ret
    elif site == "http://www.nytimes.com":
        l_ret = []
        for par in story_soup.find_all("p"):
            if par.find("story-body-text")!=-1 \
                and par.string != None\
                and par.string.lower() != 'advertisement':
                l_ret.extend(paragraph_to_word_list_list(par.string, tokenizer))
        return l_ret
    else:
        return []

if __name__ == "__main__":
sites = {}
sites["http://fivethirtyeight.com"] = {}
#sites["http://www.nytimes.com"] = {}
#sites["http://buzzfeed.com"] = {}

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

for site, obj in sites.iteritems():
    soup = url_to_soup(site)
    n_external  = 0
    site_links = set()
    for link in soup.find_all('a'):
        link_url = link.get('href')
        link_type = assign_type(site, link_url)
        if link_type==0:
            if site == "http://buzzfeed.com":
                link_url = "http://buzzfeed.com" + link_url
            site_links.add(link_url)
        if link_type==2:
            n_external = n_external +1
    obj["links"] = list(site_links)
    obj["external"] = n_external

        l_words = []
        l_num_words = []
        for story in obj["links"]:
            l_story_words = story_stats(site, story, tokenizer)
            num_words = 0
            for story_words in l_story_words:
                num_words = num_words + len(story_words)
            l_num_words.append(num_words)
            l_words.extend(l_story_words)
            print num_words
            if num_words < 20:
                print l_story_words
