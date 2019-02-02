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

"""
MAIN FUNCTION FOR SCRAPERING
"""
def scrape():
    base_url = 'https://www.umcs.pl/'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    all_news = soup.find_all('a', class_="box-news")
    #print("number of news: " + str(len(all_news)))
    i = 0
    mainList = []

    for item in all_news:
        d = { }
        # news number
        i = i + 1

        # news title
        news_title = item.find("h4", {"class":"title"})
        news_title = news_title.text.replace('\n', "").strip()

        # type of news
        news_type = item.find("em", {"class":"label-area-A"})
        news_type = news_type.text.replace('\n', "").strip()
        d['news_type'] = news_type

        # news image
        news_image = item.find("img", {"class":"img"})
        news_image = news_image['src']
        d['news_image'] = news_image
        news_hires = news_image[0:25] + "r,480,360" + news_image[38:]

        news_color = getColor(news_type)

        mainList.append({
            "id": i,
            "url": news_hires,
            "color": news_color,
            "title": news_title,
            "type": news_type
            })

    return json.dumps(mainList)

"""
SCRAPER CLASS FOR TESTING
"""
class Scraper:
    def __init__(self, url='https://www.umcs.pl/'):
        self.url = url
        self.news = []
        self.retries = 3
        self.success_load = False
        # self._soup()

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

    def getNews(self):
        return self.news

    def start(self):
        if not self.success_load:
            print('Page has not loaded, please reload or change url')
            return
        self._soup()


    def getItems(self):
        i = 0
        itemList = []
        for item in self.all_news:
            d = {}
            i += 1
            news_title = item.find("h4", {"class":"title"})
            news_title = news_title.text.replace('\n', "").strip()

            news_type = item.find("em", {"class":"label-area-A"})
            news_type = news_type.text.replace('\n', "").strip()
            d['news_type'] = news_type

            news_image = item.find("img", {"class":"img"})
            news_image = news_image['src']
            d['news_image'] = news_image
            news_hires = news_image[0:25] + "r,480,360" + news_image[38:]

            news_color = getColor(news_type)

            itemList.append({
                "id": i,
                "url": news_hires,
                "color": news_color,
                "title": news_title,
                "type": news_type
                })
        return itemList

if __name__ == "__main__":
    scrap = Scraper()
    #print(scrap.getItems())
    #print(scrape()[0])
    #print(scrape())
    #print( getColor('tv umcs') )
