#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import datetime
import time 
from helpers import date_handler, default_json_response

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

class Scraper:
    def __init__(self, url='https://www.umcs.pl/', timeout=500):
        self.url = url
        self.timeout = timeout
        self.reload_time = 5
        self.retries = 3
        self.last_updated = ''
        self.jsonData = json.dumps(default_json_response)
        # Run on __init__
        self.start()

    def _soup(self):
        iter = 0
        success_load = False
        all_news = []
        while not success_load and iter <= self.retries:
            try:
                req = requests.get(self.url)
                soup = BeautifulSoup(req.text, "html.parser")
                all_news = soup.find_all('a', class_="box-news")
                success_load = True
            except:
                print('Error, retrying {}/{}, waiting {} seconds.'.format(iter, self.retries, self.reload_time))
                # Make this async 
                # Doesn't work on first load
                # time.sleep(self.reload_time)
                iter += 1
        return success_load, all_news

    def start(self):
        success_response, news = self._soup()
        payload_data = self._getItems(news)
        if success_response and len(payload_data) > 0:
            last_updated = datetime.datetime.now()
            data = {
                'success': success_response,
                'payload': payload_data,
                'last_updated': last_updated
                }
            self.jsonData = json.dumps(data, default=date_handler)

    def _getItems(self, news):
        i = 0
        itemList = []
        try:
            for item in news:
                i += 1
                # Getting titles
                news_title = item.find("h4", {"class":"title"})
                news_title = news_title.text.replace('\n', "").strip()
                # Getting news type
                news_type = item.find("em", {"class":"label-area-A"})
                news_type = news_type.text.replace('\n', "").strip()
                # Getting image url
                news_image = item.find("img", {"class":"img"})
                news_image = news_image['src']
                # New url
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
        except:
            return []
        return itemList

if __name__ == "__main__":
    scrap = Scraper()
