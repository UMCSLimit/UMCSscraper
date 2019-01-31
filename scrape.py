#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json

def getColor(string):
    if string.lower() in ['student']:
        return "#4bbe9d"
    elif string.lower() in ['lublin']:
        return "#dc462d"
    elif string.lower() in ['tv umcs']:
        return "#f38200"
    elif string.lower() in ['biznes']:
        return "#6b08ff"
    elif string.lower() in ['pracownik']:
        return  "#337b93"
    elif string.lower() in ['absolwent']:
        return "#60baf6"
    elif string.lower() in ['kandydat']:
        return "ff6600"
    else:
        return "#9399a5"
def scrape():
    base_url = 'https://www.umcs.pl/'
        # print(base_url)

    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    #print(base_url)
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
            "url": news_image,
            "color": news_color,
            "title": news_title,
            "type": news_type
            })
    
        #print(json.dumps(jsondata))
        #mainList.append()
    return mainList 

if __name__ == "__main__":
    print(scrape())