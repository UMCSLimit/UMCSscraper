#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json

def getColor(string):
    colors = {
        'student': '#4bbe9d',
        'lublin': '#dc462d',
        'tv umcs': '#f38200',
        'biznes': '#6b08ff',
        'pracownik': '#337b93',
        'absolwent': '#60baf6',
        'kandydat': '#ff6600',
    }
    try:
        picked = colors[string.lower()]
        return picked
    except:
        return '#9399a5'

SMALL_IMAGE = 'c,270,164,t,c'
MEDIUM_IMAGE = 'r,480,360'
BIG_IMAGE = 'r,1024,800'

"""
SCRAPER CLASS FOR TESTING

To do:
# Only change main object if new update
# Dont change main object if it's not working
# Change success message to 'False' if last update was over 2h
# On __init__ make first scrape
"""
class Scraper:
    def __init__(self, url='https://www.umcs.pl/', timeout=500):
        self.url = url
        self.timeout = timeout
        self.news = []
        self.retries = 3
        self.success_load = False
        self.jsonData = ''

    def _soup(self):
        iter = 0
        while not self.success_load and iter <= self.retries:
            try:
                self.req = requests.get(self.url)
                self.soup = BeautifulSoup(self.req.text, "html.parser")
                self.all_news = self.soup.find_all('a', class_="box-news")
                self.success_load = True
            except:
                print('Error, retrying {}/{}'.format(iter, self.retries))
                iter += 1

    def start(self):
        self._soup()
        if not self.success_load:
            print('Page has not loaded, please reload or change url')
            return
        # Check for fails !
        data = {
            'success': True,
            'payload': self._getItems()
            }

        self.jsonData = json.dumps(data)

    def _getItems(self):
        i = 0
        itemList = []
        for item in self.all_news:
            d = {}
            i += 1
            # Getting titles
            news_title = item.find("h4", {"class":"title"})
            news_title = news_title.text.replace('\n', "").strip()
            # Getting news type
            news_type = item.find("em", {"class":"label-area-A"})
            news_type = news_type.text.replace('\n', "").strip()
            d['news_type'] = news_type
            # Getting image url
            news_image = item.find("img", {"class":"img"})
            news_image = news_image['src']
            d['news_image'] = news_image
            news_hires = news_image[0:25] + BIG_IMAGE + news_image[38:]
            # Change News Type to a color for styling
            news_color = getColor(news_type)
            # Adding scraped data to list
            itemList.append({
                "id": i,
                "url": news_hires,
                "color": news_color,
                "title": news_title,
                "type": news_type
            })
        return itemList

"""
### Use this code for fail checking in 'start()' ###

def checkIfBroken(news):
	item_dict = json.loads(news)
	if len(item_dict) == 8:
		return 0
	else:
		return 1

def updateNewsFeed():
    global newsFeed
    feed = scrape()
    broken = checkIfBroken(feed)
    if broken == 0:
    	newsFeed = feed
"""

if __name__ == "__main__":
    scrap = Scraper()
