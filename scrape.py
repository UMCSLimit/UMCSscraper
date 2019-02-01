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
        ##print("news number: " +  str(i))

        # news title
        news_title = item.find("h4", {"class":"title"})
        news_title = news_title.text.replace('\n', "").strip()
        ##print(news_title)

        # type of news
        news_type = item.find("em", {"class":"label-area-A"})
        news_type = news_type.text.replace('\n', "").strip()
        d['news_type'] = news_type
        ##print(news_type)

        # news image
        news_image = item.find("img", {"class":"img"})
        news_image = news_image['src']
        d['news_image'] = news_image
        news_hires = news_image[0:25] + "r,480,360" + news_image[38:]
        ##print(news_hires)

        # news color
        news_color = getColor(news_type)
        ##print(news_color)
        #convert to JSO

        mainList.append({
            "id": i,
            "url": news_hires,
            "color": news_color,
            "title": news_title,
            "type": news_type
            })

        #print(json.dumps(jsondata))
        #mainList.append()
    return json.dumps(mainList)

if __name__ == "__main__":
    #print(scrape()[0])
    print(scrape())
    #print( getColor('tv umcs') )
